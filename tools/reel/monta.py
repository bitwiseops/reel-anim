"""Montaggio del reel: per ogni scena durata (clip o voce sintetica) → Manim → compositing; poi concat, fotogrammi, report."""
from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime
from pathlib import Path

from ..anim.config import Config, carica
from . import clip as clipmod
from . import compositing, fotogrammi
from .contact_sheet import genera as contact
from .ffmpeg import ffprobe
from .manim_render import AnimazioneMancante, carica_modulo, classe_scena, file_animazione, hash_classe, renderizza
from .model import Diagnostica, Reel, avviso, errore
from .stima import durata_stimata_s
from .voce import VoceNonDisponibile, durata_s as durata_audio, sintetizza

RADICE = Path(__file__).resolve().parents[2]
CODA_VOCE_S = 0.5


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
    if abs((probe.get("durata_s") or 0) - durata) > 0.35:
        diag.append(errore(f"video reel: durata {probe.get('durata_s')} s, attesa {durata:.2f} s"))


def _cache(out: Path) -> dict:
    p = out / "_manim" / "cache.json"
    return json.loads(p.read_text()) if p.exists() else {}


def _salva_cache(out: Path, c: dict) -> None:
    (out / "_manim").mkdir(parents=True, exist_ok=True)
    (out / "_manim" / "cache.json").write_text(json.dumps(c, indent=1))


def anima(r: Reel, diag: list[Diagnostica], out: Path, qualita: str = "l", solo: int | None = None, debug: bool = False,
          cfg: Config | None = None) -> list[dict]:
    """Solo Manim: per l'animatore. Produce _manim/scena-NN.*, scene/NN.png e fotogrammi/NN-filmstrip.png."""
    cfg = cfg or carica()
    mod = carica_modulo(file_animazione(r.slug))
    info = []
    for s in r.scene:
        if solo and s.n != solo:
            continue
        durata = durata_scena(r, s)[0]
        try:
            cls = classe_scena(mod, s.n)
        except AnimazioneMancante as e:
            diag.append(errore(str(e), s.riga, s.n))
            continue
        t0 = time.time()
        video = renderizza(cls, durata, s.to_dict(), out / "_manim", f"scena-{s.n:02d}", qualita, trasparente=False, debug=debug, cfg=cfg)
        png = fotogrammi.fotogramma_chiave(video, durata, out / "scene" / f"{s.n:02d}.png")
        fs = fotogrammi.filmstrip_scena(video, durata, out / "fotogrammi" / f"{s.n:02d}-filmstrip.png")
        info.append({"scena": s.n, "tipo_scena": s.tipo, "durata_s": durata, "grafica": str(video.relative_to(out)),
                     "png": str(png.relative_to(out)), "filmstrip": str(fs.relative_to(out)), "tempo_manim_s": round(time.time() - t0, 1)})
    return info


def durata_scena(r: Reel, s, prova: bool = False, out: Path | None = None, cfg: Config | None = None) -> tuple[float, str, Path | None]:
    """(durata_s, origine, audio_sintetico). Origine: clip | voce-sintetica | attributo | stima."""
    c = clipmod.trova(r.slug, s.n)
    if c:
        d = float(ffprobe(c).get("durata_s") or 0)
        if d > 0:
            return round(d, 3), "clip", None
    if s.durata_min_s is not None and not s.voce:
        return float(s.durata_min_s), "attributo", None
    if prova and s.voce and out is not None:
        audio = sintetizza(s.voce_piena, out / "_voce" / f"{s.n:02d}.m4a", cfg)
        d = durata_audio(audio) + CODA_VOCE_S
        if s.durata_min_s is not None:
            d = max(d, s.durata_min_s)
        return round(d, 3), "voce-sintetica", audio
    return durata_stimata_s(s, cfg), "stima", None


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
    usa_prova = False
    for s in r.scene:
        if solo and s.n != solo:
            continue
        try:
            durata, origine, audio = durata_scena(r, s, prova, out, cfg)
        except VoceNonDisponibile as e:
            diag.append(errore(str(e), s.riga, s.n))
            return _chiudi(r, diag, out, elementi, clip_info, None, tempi, prova, args)
        if origine == "stima":
            if prova:
                origine = "stima"
            else:
                diag.append(errore(f"clip mancante: registra {clipmod.nome_atteso(s.n)} in contenuti/media/{r.slug}/ oppure usa --prova", s.riga, s.n))
                continue
        usa_prova = usa_prova or origine in ("voce-sintetica", "stima")
        try:
            cls = classe_scena(mod, s.n)
        except AnimazioneMancante as e:
            diag.append(errore(str(e), s.riga, s.n))
            continue
        schermo = (clipmod.cartella(r.slug) / s.schermo) if s.schermo else None
        chiave = f"{hash_classe(cls)}:{durata}:{qualita}:{bool(schermo)}:{json.dumps(s.to_dict(), sort_keys=True)}"
        grafica = out / "_manim" / (f"scena-{s.n:02d}" + (".mov" if schermo else ".mp4"))
        t1 = time.time()
        if cache.get(f"{s.n:02d}") == chiave and grafica.exists():
            pass
        else:
            grafica = renderizza(cls, durata, s.to_dict(), out / "_manim", f"scena-{s.n:02d}", qualita, trasparente=bool(schermo), cfg=cfg)
            cache[f"{s.n:02d}"] = chiave
            _salva_cache(out, cache)
        tm = time.time() - t1
        tempi["manim"] += tm
        t2 = time.time()
        riq = s.riquadro_effettivo()
        c = clipmod.trova(r.slug, s.n) if origine == "clip" else None
        src = compositing.Sorgenti(grafica=grafica, durata_s=durata, riquadro=riq, video_presentatore=c,
                                   avatar=avatar if (c is None and riq != "no" and avatar.exists()) else None, audio=audio, schermo=schermo)
        dest = compositing.componi_scena(src, out / "_scene" / f"{s.n:02d}.mp4", cfg, anteprima=args.anteprima)
        tc = time.time() - t2
        tempi["compositing"] += tc
        png = fotogrammi.fotogramma_chiave(dest, durata, out / "scene" / f"{s.n:02d}.png")
        fs = fotogrammi.filmstrip_scena(dest, durata, out / "fotogrammi" / f"{s.n:02d}-filmstrip.png")
        elementi.append({"ordine": s.n, "tipo": "png", "file": str(png.relative_to(out)), "scena": s.n, "tipo_scena": s.tipo,
                         "durata_s": durata, "parole_voce": s.parole_voce, "durata_stimata_s": durata_stimata_s(s, cfg),
                         "origine_durata": origine, "riquadro": riq, "schermo": s.schermo, "filmstrip": str(fs.relative_to(out)),
                         "grafica": str(grafica.relative_to(out)), "video": str(dest.relative_to(out)),
                         "tempo_manim_s": round(tm, 1), "tempo_ffmpeg_s": round(tc, 1)})
        pezzi.append((dest, durata))

    reel_info = None
    if pezzi and not solo and not any(d.livello == "errore" for d in diag):
        t3 = time.time()
        tr = cfg.dati["transizioni"]
        tipo_tr, d_tr = str(tr.get("tipo", "dissolvenza")), float(tr.get("durata_s", 0.25))
        finale = compositing.concatena(pezzi, out / "reel-9x16.mp4", tipo_tr, d_tr, cfg, anteprima=args.anteprima)
        durata_tot = compositing.durata_concat(pezzi, tipo_tr, d_tr)
        tempi["concat"] = time.time() - t3
        t_acc = 0.0
        for e in elementi:
            e["t_inizio_s"] = round(t_acc, 2)
            t_acc += e["durata_s"] - (d_tr if tipo_tr == "dissolvenza" else 0)
            e["t_fine_s"] = round(e["t_inizio_s"] + e["durata_s"], 2)
        fs = fotogrammi.filmstrip(finale, fotogrammi.tempi_campione(durata_tot, 10), out / "fotogrammi" / "reel-filmstrip.png", 220)
        hook = elementi[0]
        cop, cop45 = fotogrammi.cover(out / hook["video"], hook["durata_s"], out, cfg)
        probe = ffprobe(finale)
        _verifica_probe(probe, cfg, durata_tot, diag)
        reel_info = {"file": "reel-9x16.mp4", "formato": "9:16", "durata_s": durata_tot, "fps": cfg.fps, "transizione": tipo_tr,
                     "filmstrip": str(fs.relative_to(out)), "copertina": cop.name, "copertina_4x5": cop45.name, "ffprobe": probe}
    tempi = {k: round(v, 1) for k, v in tempi.items()}
    tempi["totale"] = round(time.time() - t0, 1)
    return _chiudi(r, diag, out, elementi, clip_info, reel_info, tempi, usa_prova, args)


def _chiudi(r: Reel, diag, out: Path, elementi, clip_info, reel_info, tempi, prova: bool, args) -> int:
    celle = [{"file": out / e["file"], "etichetta": f"{e['scena']:02d} · {e['tipo_scena']} · {e['durata_s']:.1f} s ({e['origine_durata']})",
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
