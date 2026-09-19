"""Montaggio del reel: per ogni scena tempi (clip o voce sintetica) → Manim → compositing; poi concat, fotogrammi, report."""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from ..anim.base import inizi_per_parole
from ..anim.config import Config, carica
from . import clip as clipmod
from . import compositing, fotogrammi
from .contact_sheet import genera as contact
from .ffmpeg import ffprobe
from .manim_render import (AnimazioneMancante, carica_modulo, classe_scena, file_animazione, hash_sorgenti, lint_animazione,
                           renderizza)
from .model import Diagnostica, Reel, Scena, avviso, errore
from .stima import CODA_S as CODA_STIMA_S
from .stima import durata_stimata_s
from .voce import CODA_VOCE_S, VoceNonDisponibile, sintetizza_frasi

RADICE = Path(__file__).resolve().parents[2]


def out_dir(r: Reel, out: str | None) -> Path:
    return Path(out) if out else RADICE / "contenuti" / "render" / r.slug


def _verifica_probe(probe: dict, cfg: Config, durata: float, diag: list[Diagnostica]) -> None:
    if "errore" in probe:
        diag.append(avviso("ffprobe non disponibile: reel non verificato"))
        return
    if (probe.get("larghezza"), probe.get("altezza"), probe.get("codec"), probe.get("pix_fmt")) != (cfg.larghezza, cfg.altezza, "h264", "yuv420p"):
        diag.append(errore(f"video reel: atteso {cfg.larghezza}x{cfg.altezza} h264 yuv420p, trovato {probe}"))
    if probe.get("audio") != "aac":
        diag.append(errore(f"video reel: audio atteso aac, trovato {probe.get('audio')}"))
    if probe.get("audio_canali") not in (None, 2):   # in mono alcuni lettori non fanno sentire la voce
        diag.append(errore(f"video reel: audio atteso stereo, trovato {probe.get('audio_canali')} canali"))
    if abs((probe.get("durata_s") or 0) - durata) > 0.35:
        diag.append(errore(f"video reel: durata {probe.get('durata_s')} s, attesa {durata:.2f} s"))


def _cache(out: Path) -> dict:
    p = out / "_manim" / "cache.json"
    return json.loads(p.read_text()) if p.exists() else {}


def _salva_cache(out: Path, c: dict) -> None:
    (out / "_manim").mkdir(parents=True, exist_ok=True)
    (out / "_manim" / "cache.json").write_text(json.dumps(c, indent=1))


@dataclass
class TempiScena:
    durata_s: float
    origine: str                      # della durata: clip | voce-sintetica | attributo | stima
    audio: Path | None = None         # voce sintetica (m4a), se c'è
    inizi_frasi_s: list[float] = field(default_factory=list)
    origine_tempi: str = "senza-voce"  # degli inizi delle frasi: voce-sintetica | presa | parole-clip | parole-stima | senza-voce


def tempi_scena(r: Reel, s: Scena, voce: bool = False, out: Path | None = None, cfg: Config | None = None,
                ignora_clip: bool = False) -> TempiScena:
    """Durata della scena e istante d'inizio di ogni frase della VOCE. In ordine: clip registrata (durata vera; frasi
    esatte dal sidecar di `reel registra`, altrimenti stimate a parole tra i silenzi chiesti dal gobbo; saltata con
    ignora_clip, cioè `monta --prova`) → scena senza voce con durata= → voce sintetica frase per frase (inizi esatti;
    solo con voce=True) → stima a parole."""
    c = None if ignora_clip else clipmod.trova(r.slug, s.n)
    if c:
        d = float(ffprobe(c).get("durata_s") or 0)
        if d > 0:
            presa = clipmod.tempi_presa(c)
            if presa is not None and len(presa) == len(s.voce):
                return TempiScena(round(d, 3), "clip", None, presa, "presa" if s.voce else "senza-voce")
            da = min(clipmod.SILENZIO_S, d * 0.1)
            a = max(da, d - clipmod.SILENZIO_S)
            return TempiScena(round(d, 3), "clip", None, inizi_per_parole(s.voce, da, a), "parole-clip" if s.voce else "senza-voce")
    if s.durata_min_s is not None and not s.voce:
        return TempiScena(float(s.durata_min_s), "attributo")
    if voce and s.voce and out is not None:
        v = sintetizza_frasi(s.voce, out / "_voce" / f"{s.n:02d}.m4a", cfg)
        d = v.durata_s + CODA_VOCE_S
        if s.durata_min_s is not None:
            d = max(d, s.durata_min_s)
        return TempiScena(round(d, 3), "voce-sintetica", v.audio, v.inizi_s, "voce-sintetica")
    d = durata_stimata_s(s, cfg)
    return TempiScena(d, "stima", None, inizi_per_parole(s.voce, 0.0, max(0.0, d - CODA_STIMA_S)),
                      "parole-stima" if s.voce else "senza-voce")


def dati_scena(s: Scena, t: TempiScena) -> dict:
    """Ciò che la scena Manim riceve in self.scena (e che entra nella chiave di cache)."""
    return {**s.to_dict(), "inizi_frasi_s": t.inizi_frasi_s}


def anima(r: Reel, diag: list[Diagnostica], out: Path, qualita: str = "l", solo: int | None = None, debug: bool = False,
          cfg: Config | None = None) -> list[dict]:
    """Solo Manim, per l'animatore: stessi tempi dell'anteprima (voce sintetica in cache se non c'è la clip), controllo
    statico del file, controlli automatici sulle scene, errori di una scena che non fermano le altre.
    Produce _anima/…/scena-NN.mp4, scene/NN.png e fotogrammi/NN-filmstrip.png."""
    cfg = cfg or carica()
    path = file_animazione(r.slug)
    mod = carica_modulo(path)
    for n, msg in lint_animazione(path):
        diag.append(avviso(f"{path.name}:{n}: {msg}"))
    info = []
    con_voce = True
    for s in r.scene:
        if solo and s.n != solo:
            continue
        if s.a_filmato:            # [broll] o hook a filmato: nessuna classe Manim, il file lo prepara `broll rendi`
            continue
        t = None
        if con_voce:
            try:
                t = tempi_scena(r, s, voce=True, out=out, cfg=cfg)
            except VoceNonDisponibile as e:
                con_voce = False
                diag.append(avviso(f"{e}: tempi stimati a parole, diversi da quelli dell'anteprima"))
        if t is None:
            t = tempi_scena(r, s, cfg=cfg)
        base = {"scena": s.n, "tipo_scena": s.tipo, "durata_s": t.durata_s, "inizi_frasi_s": t.inizi_frasi_s,
                "origine_tempi": t.origine_tempi}
        try:
            cls = classe_scena(mod, s.n)
        except AnimazioneMancante as e:
            diag.append(errore(str(e), s.riga, s.n))
            info.append({**base, "errore": str(e), "traceback": ""})
            continue
        t0 = time.time()
        try:
            res = renderizza(cls, t.durata_s, dati_scena(s, t), out / "_anima", f"scena-{s.n:02d}", qualita, trasparente=False,
                             debug=debug, cfg=cfg)
        except Exception as e:  # noqa: BLE001 — l'errore di una scena non deve fermare le altre
            diag.append(errore(f"render fallito: {type(e).__name__}: {e}", s.riga, s.n))
            info.append({**base, "errore": f"{type(e).__name__}: {e}",
                         "traceback": "".join(traceback.format_exception(e))[-1500:]})
            continue
        for a in res.avvisi + res.controlli:
            diag.append(avviso(a, s.riga, s.n))
        png = fotogrammi.fotogramma_chiave(res.video, t.durata_s, out / "scene" / f"{s.n:02d}.png")
        fs = fotogrammi.filmstrip_scena(res.video, t.durata_s, out / "fotogrammi" / f"{s.n:02d}-filmstrip.png")
        info.append({**base, "avvisi_tempi": res.avvisi, "controlli": res.controlli, "grafica": str(res.video.relative_to(out)),
                     "png": str(png.relative_to(out)), "filmstrip": str(fs.relative_to(out)),
                     "tempo_manim_s": round(time.time() - t0, 1)})
    return info


def _scena_broll(r: Reel, s: Scena, t: TempiScena, out: Path, avatar: Path, args, cfg: Config,
                 diag: list[Diagnostica]) -> dict | None:
    """Una scena a filmato ([broll], o l'hook con `SCHERMO:`): niente Manim, il file di `SCHERMO:` fa da grafica a
    tutta tela, col riquadro sopra."""
    filmato = clipmod.cartella(r.slug) / (s.schermo or "")
    if not s.schermo or not filmato.exists():
        diag.append(errore(f"filmato '{s.schermo}' non trovato in contenuti/media/{r.slug}/ "
                           f"(`uv run --project broll broll rendi {r.slug}`)", s.riga, s.n))
        return None
    avvisi_tempi: list[str] = []
    video = filmato.suffix.lower() in (".mp4", ".mov", ".webm", ".m4v")
    durata_filmato = (ffprobe(filmato).get("durata_s") or 0.0) if video else None
    if durata_filmato is not None and durata_filmato < t.durata_s - 1.5 / cfg.fps:
        # il filmato è stato reso sulla durata di prima (stima, voce di prova): la presa vera è più lunga
        avvisi_tempi.append(f"il filmato dura {durata_filmato:.2f} s, la scena {t.durata_s:.2f} s: l'ultimo fotogramma resta "
                            f"fermo per {t.durata_s - durata_filmato:.2f} s. Rifai `broll piano` e `broll rendi`")
    for a in avvisi_tempi:
        diag.append(avviso(a, s.riga, s.n))
    t2 = time.time()
    riq = s.riquadro_effettivo()
    c = clipmod.trova(r.slug, s.n) if t.origine == "clip" else None
    src = compositing.Sorgenti(grafica=filmato, durata_s=t.durata_s, riquadro=riq, video_presentatore=c,
                               avatar=avatar if (c is None and riq != "no" and avatar.exists()) else None, audio=t.audio,
                               filmato=True)
    dest = compositing.componi_scena(src, out / "_scene" / f"{s.n:02d}.mp4", cfg, anteprima=args.anteprima)
    tc = time.time() - t2
    png = fotogrammi.fotogramma_chiave(dest, t.durata_s, out / "scene" / f"{s.n:02d}.png")
    fs = fotogrammi.filmstrip_scena(dest, t.durata_s, out / "fotogrammi" / f"{s.n:02d}-filmstrip.png")
    return {"ordine": s.n, "tipo": "png", "file": str(png.relative_to(out)), "scena": s.n, "tipo_scena": s.tipo,
            "durata_s": t.durata_s, "parole_voce": s.parole_voce, "durata_stimata_s": durata_stimata_s(s, cfg),
            "origine_durata": t.origine, "inizi_frasi_s": t.inizi_frasi_s, "origine_tempi": t.origine_tempi,
            "avvisi_tempi": avvisi_tempi, "controlli": [], "riquadro": riq, "schermo": s.schermo, "filmato": True,
            "filmstrip": str(fs.relative_to(out)), "grafica": str(filmato.relative_to(RADICE)) if filmato.is_relative_to(RADICE) else str(filmato),
            "video": str(dest.relative_to(out)), "tempo_manim_s": 0.0, "tempo_ffmpeg_s": round(tc, 1)}


def monta(args, r: Reel, diag: list[Diagnostica], out: Path, cfg: Config | None = None) -> int:
    cfg = cfg or carica()
    out.mkdir(parents=True, exist_ok=True)
    for sub in ("_manim", "_scene", "scene", "fotogrammi"):
        (out / sub).mkdir(exist_ok=True)
    prova = bool(args.prova)
    qualita = args.qualita or ("l" if args.anteprima else "h")
    solo = getattr(args, "scena", None)
    try:
        mod = carica_modulo(file_animazione(r.slug))
    except AnimazioneMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    avatar = RADICE / cfg.presentatore.avatar
    t0 = time.time()
    tempi = {"manim": 0.0, "compositing": 0.0, "concat": 0.0}
    elementi: list[dict] = []
    clip_info = clipmod.stato(r.slug, [s.n for s in r.scene])
    pezzi: list[tuple[Path, float]] = []
    cache = _cache(out)
    firma = hash_sorgenti(file_animazione(r.slug))
    for n, msg in lint_animazione(file_animazione(r.slug)):
        diag.append(avviso(f"{file_animazione(r.slug).name}:{n}: {msg}"))
    usa_prova = False
    for s in r.scene:
        if solo and s.n != solo:
            continue
        try:
            t = tempi_scena(r, s, prova, out, cfg, ignora_clip=prova)   # --prova: sempre voce sintetica e avatar, anche con le clip
        except VoceNonDisponibile as e:
            diag.append(errore(str(e), s.riga, s.n))
            return _chiudi(r, diag, out, elementi, clip_info, None, tempi, prova, args)
        if t.origine == "stima" and not prova:
            diag.append(errore(f"clip mancante: registra {clipmod.nome_atteso(s.n)} in contenuti/media/{r.slug}/ oppure usa --prova", s.riga, s.n))
            continue
        if t.origine_tempi == "parole-clip" and (presa := clipmod.tempi_presa(clipmod.trova(r.slug, s.n))) is not None:
            diag.append(avviso(f"tempi della presa ignorati: {len(presa)} frasi nel sidecar, {len(s.voce)} nella sceneggiatura: "
                               "registra di nuovo la scena", s.riga, s.n))
        usa_prova = usa_prova or t.origine in ("voce-sintetica", "stima")
        if s.a_filmato:
            pezzo = _scena_broll(r, s, t, out, avatar, args, cfg, diag)
            if pezzo:
                elementi.append(pezzo)
                pezzi.append((out / pezzo["video"], t.durata_s))
            continue
        try:
            cls = classe_scena(mod, s.n)
        except AnimazioneMancante as e:
            diag.append(errore(str(e), s.riga, s.n))
            continue
        schermo = (clipmod.cartella(r.slug) / s.schermo) if s.schermo else None
        dati = dati_scena(s, t)
        chiave = f"{firma}:{cls.__name__}:{t.durata_s}:{qualita}:{bool(schermo)}:{json.dumps(dati, sort_keys=True)}"
        voce_cache = cache.get(f"{s.n:02d}")
        t1 = time.time()
        if (isinstance(voce_cache, dict) and voce_cache.get("chiave") == chiave and voce_cache.get("grafica")
                and (out / voce_cache["grafica"]).exists()):
            grafica = out / voce_cache["grafica"]
            avvisi_tempi, controlli = list(voce_cache.get("avvisi", [])), list(voce_cache.get("controlli", []))
        else:
            try:
                res = renderizza(cls, t.durata_s, dati, out / "_manim", f"scena-{s.n:02d}", qualita, trasparente=bool(schermo), cfg=cfg)
            except Exception as e:  # noqa: BLE001 — l'errore di una scena non deve fermare le altre
                diag.append(errore(f"render fallito: {type(e).__name__}: {e}", s.riga, s.n))
                continue
            grafica, avvisi_tempi, controlli = res.video, res.avvisi, res.controlli
            cache[f"{s.n:02d}"] = {"chiave": chiave, "grafica": str(grafica.relative_to(out)), "avvisi": avvisi_tempi,
                                   "controlli": controlli}
            _salva_cache(out, cache)
        for a in avvisi_tempi + controlli:
            diag.append(avviso(a, s.riga, s.n))
        tm = time.time() - t1
        tempi["manim"] += tm
        t2 = time.time()
        riq = s.riquadro_effettivo()
        c = clipmod.trova(r.slug, s.n) if t.origine == "clip" else None
        src = compositing.Sorgenti(grafica=grafica, durata_s=t.durata_s, riquadro=riq, video_presentatore=c,
                                   avatar=avatar if (c is None and riq != "no" and avatar.exists()) else None, audio=t.audio,
                                   schermo=schermo)
        dest = compositing.componi_scena(src, out / "_scene" / f"{s.n:02d}.mp4", cfg, anteprima=args.anteprima)
        tc = time.time() - t2
        tempi["compositing"] += tc
        png = fotogrammi.fotogramma_chiave(dest, t.durata_s, out / "scene" / f"{s.n:02d}.png")
        fs = fotogrammi.filmstrip_scena(dest, t.durata_s, out / "fotogrammi" / f"{s.n:02d}-filmstrip.png")
        elementi.append({"ordine": s.n, "tipo": "png", "file": str(png.relative_to(out)), "scena": s.n, "tipo_scena": s.tipo,
                         "durata_s": t.durata_s, "parole_voce": s.parole_voce, "durata_stimata_s": durata_stimata_s(s, cfg),
                         "origine_durata": t.origine, "inizi_frasi_s": t.inizi_frasi_s, "origine_tempi": t.origine_tempi,
                         "avvisi_tempi": avvisi_tempi, "controlli": controlli, "riquadro": riq, "schermo": s.schermo,
                         "filmstrip": str(fs.relative_to(out)), "grafica": str(grafica.relative_to(out)),
                         "video": str(dest.relative_to(out)), "tempo_manim_s": round(tm, 1), "tempo_ffmpeg_s": round(tc, 1)})
        pezzi.append((dest, t.durata_s))

    reel_info = None
    if pezzi and not solo and not any(d.livello == "errore" for d in diag):
        t3 = time.time()
        tr = cfg.dati["transizioni"]
        tipo_tr, d_tr = str(tr.get("tipo", "dissolvenza")), float(tr.get("durata_s", 0.25))
        # fra animazione e filmato si stacca: grafica scura e filmato chiaro sciolti insieme lasciano il fantasma
        # dei testi sopra l'immagine ([transizioni] filmato = "dissolvenza" per riavere la dissolvenza ovunque)
        tagli = frozenset(k for k in range(1, len(elementi))
                          if (elementi[k - 1].get("filmato") or elementi[k].get("filmato"))
                          and str(tr.get("filmato", "taglio")) == "taglio")
        finale = compositing.concatena(pezzi, out / "reel-9x16.mp4", tipo_tr, d_tr, cfg, anteprima=args.anteprima, tagli=tagli)
        durata_tot = compositing.durata_concat(pezzi, tipo_tr, d_tr, tagli)
        tempi["concat"] = time.time() - t3
        t_acc = 0.0
        for k, e in enumerate(elementi):
            e["t_inizio_s"] = round(t_acc, 2)
            sciolta = tipo_tr == "dissolvenza" and (k + 1) not in tagli
            t_acc += e["durata_s"] - (d_tr if sciolta else 0)
            e["t_fine_s"] = round(e["t_inizio_s"] + e["durata_s"], 2)
        fs = fotogrammi.filmstrip(finale, fotogrammi.tempi_campione(durata_tot, 10), out / "fotogrammi" / "reel-filmstrip.png", 220)
        hook = elementi[0]
        s_hook = r.hook if r.hook is not None and hook.get("filmato") else None   # a filmato il titolo non è a schermo
        cop, cop45 = fotogrammi.cover(out / hook["video"], hook["durata_s"], out, cfg,
                                      titolo=s_hook.titolo if s_hook else None,
                                      sottotitolo=s_hook.sottotitolo if s_hook else None)
        probe = ffprobe(finale)
        _verifica_probe(probe, cfg, durata_tot, diag)
        reel_info = {"file": "reel-9x16.mp4", "formato": "9:16", "durata_s": durata_tot, "fps": cfg.fps, "transizione": tipo_tr,
                     "filmstrip": str(fs.relative_to(out)), "copertina": cop.name, "copertina_4x5": cop45.name, "ffprobe": probe}
    tempi = {k: round(v, 1) for k, v in tempi.items()}
    tempi["totale"] = round(time.time() - t0, 1)
    return _chiudi(r, diag, out, elementi, clip_info, reel_info, tempi, usa_prova, args)


def _chiudi(r: Reel, diag, out: Path, elementi, clip_info, reel_info, tempi, prova: bool, args) -> int:
    celle = [{"file": out / e["file"], "etichetta": f"{e['scena']:02d} · {e['tipo_scena']}\n{e['durata_s']:.1f} s · {e['origine_durata']}",
              "animata": True, "problema": any(d.scena == e["scena"] and d.livello == "errore" for d in diag)} for e in elementi]
    if reel_info:
        celle.append({"file": out / reel_info["copertina_4x5"], "etichetta": "cover 4:5", "animata": False})
        celle.append({"file": out / reel_info["filmstrip"], "etichetta": f"reel · {reel_info['durata_s']:.0f} s", "animata": True})
    if celle:
        contact(celle, diag, out / "contact-sheet.png")
    path = Path(args.file)
    anim = file_animazione(r.slug)
    report = {
        "slug": r.slug, "formato": "reel-manim", "sorgente": str(path), "hash_md": hashlib.sha256(path.read_bytes()).hexdigest()[:16],
        "hash_animazione": hashlib.sha256(anim.read_bytes()).hexdigest()[:16] if anim.exists() else None,
        "generato_il": datetime.now().isoformat(timespec="seconds"), "cartella": str(out), "prova": bool(prova),
        "elementi": elementi, "clip": clip_info, "reel": reel_info, "diagnostica": [d.to_dict() for d in diag],
        "tempi_s": tempi, "ordine_upload": ["reel-9x16.mp4"] if reel_info else [],
    }
    (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if prova and reel_info and not any(d.livello == "errore" for d in diag):
        # copia stabile per `reel registra`: il montaggio con le clip vere sovrascrive report.json e reel-9x16.mp4
        shutil.copyfile(out / reel_info["file"], out / "reel-prova.mp4")
        (out / "report-prova.json").write_text(json.dumps({**report, "reel": {**reel_info, "file": "reel-prova.mp4"}},
                                                          ensure_ascii=False, indent=2), encoding="utf-8")
    for d in diag:
        if d.livello == "errore":
            print(d, file=sys.stderr)
    n_err = sum(1 for d in diag if d.livello == "errore")
    n_avv = len(diag) - n_err
    if reel_info:
        print(f"-> {out}  (reel {reel_info['durata_s']:.0f} s, {len(elementi)} scene{', ANTEPRIMA con voce sintetica' if prova else ''}; "
              f"{n_err} errori, {n_avv} avvisi; manim {tempi['manim']}s, compositing {tempi['compositing']}s, concat {tempi['concat']}s)")
    else:
        print(f"-> {out}  ({len(elementi)} scene montate, nessun reel finale; {n_err} errori, {n_avv} avvisi)")
    if n_err or (getattr(args, "strict", False) and n_avv):
        return 1
    return 0
