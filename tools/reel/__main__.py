"""CLI: uv run reel <comando> <file.md> [opzioni]"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .model import Diagnostica, Reel, errore
from .parser import ErroreParse, parse
from .validate import check, ha_errori

RADICE = Path(__file__).resolve().parents[2]


def _stampa(diagnostiche: list[Diagnostica]) -> None:
    for d in diagnostiche:
        print(d, file=sys.stderr)


def _carica(path: Path) -> tuple[Reel, list[Diagnostica]]:
    try:
        r, avvisi = parse(path)
    except ErroreParse as e:
        _stampa(e.diagnostiche)
        print(f"-> {len(e.diagnostiche)} errori di sintassi in {path}", file=sys.stderr)
        sys.exit(2)
    return r, avvisi + check(r)


def _riepilogo(diag: list[Diagnostica]) -> tuple[str, int, int]:
    n_err = sum(1 for d in diag if d.livello == "errore")
    n_avv = len(diag) - n_err
    return ("ERRORI" if n_err else ("OK con avvisi" if n_avv else "OK")), n_err, n_avv


def cmd_valida(args) -> int:
    from collections import Counter
    from . import clip
    from .stima import durata_stimata_s
    r, diag = _carica(Path(args.file))
    _stampa(diag)
    stato, n_err, n_avv = _riepilogo(diag)
    tipi = Counter(s.tipo for s in r.scene)
    tot = 0.0
    righe = []
    for s in r.scene:
        c = clip.trova(r.slug, s.n)
        d = durata_stimata_s(s)
        tot += d
        cl = f"clip ✔ {clip.ffprobe(c).get('durata_s')}s" if c else "clip ✘"
        righe.append(f"{s.n}:{s.tipo[:5]} {s.parole_voce}p → ~{d:.0f}s [{cl}]")
    print(f"[{stato}] reel stimato {tot:.0f}s · {len(r.scene)} scene ({', '.join(f'{v} {k}' for k, v in tipi.items())}) · "
          f"{r.parole_voce} parole di voce\n          " + "\n          ".join(righe))
    return 1 if n_err or (args.strict and n_avv) else 0


def cmd_gobbo(args) -> int:
    from .gobbo import gobbo
    r, diag = _carica(Path(args.file))
    testo = gobbo(r)
    if args.scrivi:
        dest = RADICE / "contenuti" / "media" / r.slug / "gobbo.txt"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(testo, encoding="utf-8")
        print(f"-> {dest}")
    else:
        print(testo)
    return 0


def _tabella_clip(r: Reel, poi: str = "") -> int:
    from . import clip
    from .stima import durata_stimata_s
    st = clip.stato(r.slug, [s.n for s in r.scene])
    mancanti = 0
    for s, c in zip(r.scene, st):
        target = durata_stimata_s(s)
        if c["presente"]:
            d = c.get("durata_s") or 0
            delta = (d - target) / target * 100 if target else 0
            nota = "  ← durata molto diversa dalla stima" if abs(delta) > 30 else ""
            beat = " · beat dalla presa" if c.get("tempi") == "presa" else " · beat stimati"
            v = clip.voce_presa(clip.trova(r.slug, s.n))
            testo = " · ✎ testo cambiato" if v is not None and v != list(s.voce) else ""
            print(f"scena {s.n}: ✔ {c['file']}  {d:.1f}s (stima {target:.0f}s, {delta:+.0f} %){beat}{testo}{nota}")
        else:
            mancanti += 1
            print(f"scena {s.n}: ✘ manca {c['atteso']}  (target ~{target:.0f}s)")
    print(f"-> {len(st) - mancanti}/{len(st)} clip presenti in contenuti/media/{r.slug}/{poi if not mancanti else ''}")
    if clip.carica_parlato(r.slug):
        print(f"   testo corretto in registrazione per le scene {', '.join(map(str, sorted(clip.carica_parlato(r.slug))))}: "
              "`uv run reel parlato <file>` lo confronta con la sceneggiatura, `--applica` ce lo riporta")
    return 1 if mancanti else 0


def cmd_parlato(args) -> int:
    from . import parlato
    path = Path(args.file)
    r, _ = _carica(path)
    cambi = parlato.recitato(r)
    if not cambi:
        print("-> il testo recitato coincide con la VOCE della sceneggiatura")
        return 0
    print(parlato.confronto(r, cambi))
    if not args.applica:
        print(f"-> {len(cambi)} scene con il testo cambiato in registrazione: `uv run reel parlato {args.file} --applica` "
              "lo riporta nel .md")
        return 0
    n = parlato.applica(path, cambi)
    r2, diag = _carica(path)
    _stampa(diag)
    print(f"-> {n} righe VOCE riscritte in {path}. Se hai cambiato numeri o fatti, passa quelle frasi al revisore; "
          "l'anteprima --prova resta valida (cambia solo il testo) anche se `registra` la segnala come vecchia")
    return 1 if ha_errori(diag) else 0


def cmd_clip(args) -> int:
    r, _ = _carica(Path(args.file))
    return _tabella_clip(r)


def cmd_registra(args) -> int:
    from ..anim.config import carica
    from . import clip
    from .ffmpeg import FfmpegMancante, trova_ffmpeg
    from .registra import (ReportNonPronto, carica_timeline, elenca_dispositivi, indice_dispositivo, opzioni,
                           presa_dal_registro, spezza)
    try:
        trova_ffmpeg()
    except FfmpegMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    if args.dispositivi:
        video, audio = elenca_dispositivi()
        print("video:\n" + "\n".join(f"  [{i}] {n}" for i, n in video) + "\naudio:\n" + "\n".join(f"  [{i}] {n}" for i, n in audio))
        print("-> scegli con --video N --audio N, o in config.local.toml [registrazione] video/audio (indice o parte del nome); "
              "senza audio si usa il microfono predefinito di sistema")
        return 0
    if not args.file:
        print("-> serve la sceneggiatura: uv run reel registra <file>", file=sys.stderr)
        return 2
    r, diag = _carica(Path(args.file))
    _stampa(diag)
    if ha_errori(diag):
        print("-> errori di validazione: niente registrazione", file=sys.stderr)
        return 1
    cfg = carica()
    opz = opzioni(cfg, args.video, args.audio)
    liste = dict(zip(("video", "audio"), elenca_dispositivi()))
    for k in ("video", "audio"):
        if opz[k] is None:
            continue
        try:
            opz[k] = indice_dispositivo(opz[k], liste[k])
        except ValueError as e:
            if k == "video" or str(opz[k]).isdigit():
                print(f"-> {e}", file=sys.stderr)
                return 1
            print(f"-> {e}: uso il microfono predefinito", file=sys.stderr)   # il mic scelto l'altra volta non è collegato
            opz[k] = None
    out = Path(args.out) if args.out else RADICE / "contenuti" / "render" / r.slug   # come monta.out_dir, senza importare Manim
    try:
        tl, avvisi = carica_timeline(r, out, cfg)
    except ReportNonPronto as e:
        print(f"-> {e}: prima esegui `uv run reel monta {args.file} --prova --anteprima`", file=sys.stderr)
        return 1
    _stampa(avvisi)
    cartella = clip.cartella(r.slug)
    cartella.mkdir(parents=True, exist_ok=True)
    poi = f"; poi: uv run reel monta {args.file} --anteprima"
    if args.spezza:
        p = presa_dal_registro(cartella, args.spezza)
        fatte = spezza(tl, p, cartella, opz, lambda i, n, s: print(f"taglio la scena {s.n} ({i + 1}/{n})…"))
        print(f"{p.nome}: {len(fatte)} scene tagliate")
        return _tabella_clip(r, poi)
    from .registra_app import AppRegistra
    AppRegistra(r, tl, opz, cfg, cartella, out, [str(d) for d in avvisi], da_scena=args.da_scena, dispositivi=liste).esegui()
    return _tabella_clip(r, poi)


def cmd_voce(args) -> int:
    from .monta import out_dir
    from .percorsi import lavoro_per
    from .voce import sintetizza_frasi
    r, _ = _carica(Path(args.file))
    lav = lavoro_per(r.slug, out_dir(r, args.out))
    for s in r.scene:
        if s.voce:
            v = sintetizza_frasi(s.voce, lav / "_voce" / f"{s.n:02d}.m4a")
            print(f"scena {s.n}: {v.audio}  {v.durata_s:.2f} s · frasi a {' / '.join(f'{x:.2f}' for x in v.inizi_s)} s")
    return 0


def cmd_anima(args) -> int:
    import json
    from .manim_render import AnimazioneMancante
    from .monta import anima, out_dir
    r, diag = _carica(Path(args.file))
    if not args.json:
        _stampa(diag)
    out = out_dir(r, args.out)
    n0 = len(diag)
    info: list[dict] = []
    if ha_errori(diag):
        diag.append(errore("errori di validazione: nessun render"))
    else:
        import contextlib
        # con --json stdout è solo il JSON: gli avvisi che Manim o Pango stampano durante il render vanno su stderr
        uscita = contextlib.redirect_stdout(sys.stderr) if args.json else contextlib.nullcontext()
        try:
            with uscita:
                info = anima(r, diag, out, args.qualita or "l", args.scena, args.debug)
        except AnimazioneMancante as e:
            diag.append(errore(str(e)))
    ok = not ha_errori(diag)
    if args.json:   # per l'agente animatore: un solo oggetto JSON su stdout
        print(json.dumps({"ok": ok, "cartella": str(out), "scene": info, "diagnostica": [d.to_dict() for d in diag]},
                         ensure_ascii=False, indent=1))
        return 0 if ok else 1
    for i in info:
        if "errore" in i:
            print(f"scena {i['scena']}: ERRORE {i['errore']}\n{i['traceback']}")
            continue
        beat = " / ".join(f"{x:.1f}" for x in i["inizi_frasi_s"]) or "nessuno"
        print(f"scena {i['scena']} [{i['tipo_scena']}] {i['durata_s']:.1f}s · beat {beat} s ({i['origine_tempi']}) · "
              f"manim {i['tempo_manim_s']}s → {out / i['png']}  {out / i['filmstrip']}")
        for a in i["avvisi_tempi"]:
            print(f"   ⚠ {a}")
        for c in i["controlli"]:
            print(f"   ✗ {c}")
    _stampa([d for d in diag[n0:] if d.scena is None or d.livello == "errore"])
    return 0 if ok else 1


def cmd_monta(args) -> int:
    from .monta import monta, out_dir
    r, diag = _carica(Path(args.file))
    _stampa(diag)
    if ha_errori(diag):
        print("-> errori di validazione: nessun montaggio", file=sys.stderr)
        return 1
    return monta(args, r, diag, out_dir(r, args.out))


def cmd_strisce(args) -> int:
    import json
    from .ffmpeg import ffprobe
    from ..anim.config import carica
    from . import clip
    from .fotogrammi import copri_volto, strisce_fitte, tempi_dal_report, video_scena
    from .percorsi import lavoro_per
    r, _ = _carica(Path(args.file))
    cfg = carica()
    out = Path(args.out) if args.out else RADICE / "contenuti" / "render" / r.slug   # come monta.out_dir, senza importare Manim
    lav = lavoro_per(r.slug, out, cfg)      # video delle scene e strisce fitte: transitori, fuori dal progetto
    tempi = tempi_dal_report(out)
    scene: list[dict] = []
    for s in r.scene:
        if args.scena and s.n != args.scena:
            continue
        video = video_scena(lav, s.n, args.sorgente)
        if video is None:       # con `anima` le scene a filmato e a volto pieno non hanno un video: si saltano
            continue
        avvisi = []
        durata = ffprobe(video).get("durata_s") or 0.0
        t = tempi.get(s.n)
        if t is None:
            avvisi.append(f"scena {s.n}: nessun report con i tempi in {out}: solo la striscia dell'intera scena")
        elif durata and abs(durata - t["durata_s"]) > 0.5:
            avvisi.append(f"scena {s.n}: il video dura {durata:.1f} s, il report dice {t['durata_s']:.1f} s: i beat sono di un "
                          "altro render, solo la striscia dell'intera scena (rilancia `monta` o `anima`)")
            t = None
        durata = durata or (t["durata_s"] if t else 0.0)
        if not durata:
            avvisi.append(f"scena {s.n}: durata di {video.name} non leggibile: saltata")
            scene.append({"scena": s.n, "video": str(video), "strisce": [], "avvisi": avvisi})
            continue
        inizi = t["inizi_frasi_s"] if t else []
        cop = None
        if args.sorgente == "scene" and clip.trova(r.slug, s.n) is not None and (t is None or t.get("clip_vera") is not False):
            # il volto lo guarda solo lui: nel dubbio (report vecchio o assente) si copre
            cop = copri_volto(cfg, s.riquadro_effettivo(), RADICE / cfg.presentatore.avatar, t["caption"] if t else None)
        png = strisce_fitte(video, durata, inizi, lav / "fotogrammi", s.n, args.fps, args.finestra, args.sorgente, copri=cop)
        scene.append({"scena": s.n, "video": str(video), "durata_s": durata, "inizi_frasi_s": inizi,
                      "strisce": [str(p) for p in png], "avvisi": avvisi})
    if not scene:
        quale = f"la scena {args.scena}" if args.scena else "nessuna scena"
        print(f"-> {quale} non ha un video in {lav} (sorgente «{args.sorgente}»): prima "
              f"`uv run reel {'anima' if args.sorgente == 'anima' else 'monta'} {args.file}`", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps({"ok": True, "cartella": str(out), "sorgente": args.sorgente, "scene": scene}, ensure_ascii=False, indent=1))
        return 0
    for i in scene:
        for a in i["avvisi"]:
            print(f"   ⚠ {a}", file=sys.stderr)
        if i["strisce"]:
            beat = " / ".join(f"{x:.1f}" for x in i["inizi_frasi_s"]) or "nessuno"
            print(f"scena {i['scena']} {i['durata_s']:.1f}s · beat {beat} s · {Path(i['video']).name}\n   " + "\n   ".join(i["strisce"]))
    return 0


def cmd_uscite(args) -> int:
    import shlex
    from datetime import date
    from ..anim.config import carica
    from . import uscite
    idea = Path(args.file)
    modelli = [m.strip() for m in args.modelli.split(",") if m.strip()]
    try:
        rr = uscite.richieste(idea.read_text(encoding="utf-8"))
    except (OSError, uscite.ErroreUscite) as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    slug, _ = uscite.slug_e_data(idea)
    dest = uscite.CARTELLA / f"{slug}-{date.today().isoformat()}.md"
    n = len(rr) * len(modelli) * args.per_modello
    if args.prova_a_secco:
        for r in rr:
            s = uscite.sigle(r, modelli, args.per_modello)
            print(f"{r.sigla} · {r.nome}  ({s[0][0]}…{s[-1][0]})\n   {r.testo}")
            for m in modelli:
                print(f"   $ {shlex.join(uscite.comando(r, m))}")
        print(f"-> a secco: {len(rr)} richieste × {len(modelli)} modelli × {args.per_modello} = {n} chiamate, niente lanciato; "
              f"il file sarebbe {dest}{' (ESISTE: serve --forza)' if dest.exists() else ''}")
        return 0
    if dest.exists() and not args.forza:
        print(f"-> {dest} esiste già: --forza per rigenerare e sovrascrivere", file=sys.stderr)
        return 1
    print(f"{len(rr)} richieste ({' '.join(r.sigla for r in rr)}) × {', '.join(modelli)} × {args.per_modello}: {n} chiamate a claude -p, "
          f"{uscite.IN_PARALLELO} alla volta…", file=sys.stderr)
    try:
        fatte = uscite.genera(rr, modelli, args.per_modello, args.timeout,
                              lambda s, k, tot: print(f"   {s} ({k}/{tot})", file=sys.stderr))
        esito = uscite.scrivi_file(dest, slug, date.today().isoformat(), uscite.versione_claude(), rr, fatte, modelli, args.per_modello,
                                   uscite.termini_account(*uscite.account_git(), carica()), forza=args.forza)
        percorso = str(dest.relative_to(RADICE)) if dest.is_relative_to(RADICE) else str(dest)
        idea.write_text(uscite.riga_uscite(idea.read_text(encoding="utf-8"), percorso), encoding="utf-8")
    except uscite.ErroreUscite as e:     # pipeline T0b: se `claude -p` fallisce ci si ferma, senza uscite vere non si scrive
        print(f"-> {e}", file=sys.stderr)
        return 1
    print(f"-> {dest}: {esito['uscite']} uscite · dati dell'account in {len(esito['ritoccate'])} ({esito['sostituzioni']} sostituzioni)"
          f" · riga **Uscite:** in {idea}")
    for s, spie in esito["segnalate"].items():
        print(f"   ⚠ {s} nomina {', '.join(spie)}: da ricontrollare a mano (connettori, inferenze personali)")
    return 0


def cmd_copione(args) -> int:
    from datetime import date
    from ..anim.config import carica
    from . import copione as cp
    from .stile import trascrizioni
    from .stima import parole_al_secondo
    from .validate import LIMITI
    cfg = carica()
    conf = cfg.dati.get("copione", {})
    idea_p = Path(args.file)
    try:
        testo_idea = idea_p.read_text(encoding="utf-8")
        idea = cp.leggi_idea(testo_idea)
    except (OSError, cp.ErroreCopione) as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    parole = int(args.parole or conf.get("parole", 235))
    pas = parole_al_secondo(cfg)
    voci = cp.scegli_trascrizioni(trascrizioni(cfg, lingua="it"), idea_p.stem, int(conf.get("trascrizioni", 6)),
                                  cp.secondi_per(parole, pas))
    if not voci:
        print("   ⚠ nessuna trascrizione di reelkit ([stile] indice e trascrizioni): il prompt parte senza l'orecchio", file=sys.stderr)
    tr = [(v["id"], v["file"].read_text(encoding="utf-8")) for v in voci]
    prompt = cp.componi_prompt(cp.TEMPLATE.read_text(encoding="utf-8"), idea, tr, parole, args.nota or "", pas)
    modelli = [args.modello] if args.modello else list(conf.get("modelli", ["gpt-5.4", cp.CLAUDE]))
    chiave = cp.chiave_poe()
    poe = cp.Poe(chiave, int(conf.get("token_uscita", 6000)), int(conf.get("punti_minimi", 1500))) if chiave else None
    dest = cp.CARTELLA / f"{idea_p.stem}.md"
    scelte = ", ".join(f"{v['id']} ({v['account']})" for v in voci) or "nessuna"
    riepilogo = (f"{len(idea.tappe)} tappe · {parole} parole (~{cp.secondi_per(parole, pas)} s) · trascrizioni "
                 f"{scelte} · prompt {len(prompt)} caratteri")
    if args.prova_a_secco:
        print(prompt)
        print(f"-> a secco: {riepilogo}", file=sys.stderr)
        for m in modelli:
            if m == cp.CLAUDE:
                print(f"   {m}: claude -p --model {conf.get('claude_modello', 'opus')}, niente punti", file=sys.stderr)
            elif poe is None:
                print(f"   {m}: manca POE_API_KEY (ambiente o .env)", file=sys.stderr)
            else:
                perche = poe.salta(m, prompt)
                print(f"   {m}: stima {poe.stima_punti(m, prompt) or '?'} punti · "
                      f"{'si salterebbe: ' + perche if perche else 'si chiamerebbe'}", file=sys.stderr)
        if poe is not None:
            print(f"   saldo Poe: {poe.saldo()} punti", file=sys.stderr)
        print(f"   il file sarebbe {dest}{' (ESISTE: serve --forza o --nota)' if dest.exists() else ''}", file=sys.stderr)
        return 0
    if dest.exists() and not (args.forza or args.nota):
        print(f"-> {dest} esiste già: --forza per rigenerarlo, o --nota \"…\" per una versione con una richiesta", file=sys.stderr)
        return 1

    def salta(m: str, p: str) -> str | None:
        if m == cp.CLAUDE:
            return None
        return "manca POE_API_KEY (ambiente o .env)" if poe is None else poe.salta(m, p)

    def chiama(m: str, p: str) -> str:
        if m == cp.CLAUDE:
            return cp.chiama_claude(p, str(conf.get("claude_modello", "opus")))
        return poe.chiama(m, p)

    print(f"copione: {riepilogo}\n   catena: {' → '.join(modelli)}", file=sys.stderr)
    saldo_prima = poe.saldo() if poe is not None else None
    try:
        esito = cp.catena(prompt, modelli, len(idea.tappe), parole, chiama, salta,
                          lambda s: print(f"   {s}", file=sys.stderr), tetto=int(LIMITI["reel_errore_s"] * pas))
    except cp.ErroreCopione as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    spesi = saldo_prima - poe.saldo() if poe is not None and saldo_prima is not None else None
    rel = lambda q: str(q.relative_to(RADICE)) if q.resolve().is_relative_to(RADICE) else str(q)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(cp.componi_file(rel(idea_p.resolve()), idea, esito, date.today().isoformat(), spesi, args.nota or ""),
                    encoding="utf-8")
    dest.with_suffix(".prompt.md").write_text(prompt, encoding="utf-8")
    idea_p.write_text(cp.riga_copione(testo_idea, rel(dest)), encoding="utf-8")
    print(f"-> {dest}: {esito.modello}, {cp.parole_totali(esito.scene)} parole"
          f"{f' · {spesi} punti Poe' if spesi is not None else ''} · riga **Copione:** in {idea_p}")
    for a in esito.esame.avvisi:
        print(f"   ⚠ {a}")
    return 0


def cmd_pulisci(args) -> int:
    """Svuota il lavoro transitorio (tools/reel/percorsi.py): il riepilogo in contenuti/render/ resta."""
    import shutil
    from .percorsi import lavoro, radice_lavoro
    radice = radice_lavoro()
    if args.tutto:
        cartelle = sorted(p for p in radice.glob("*") if p.is_dir()) if radice.is_dir() else []
    elif args.slug:
        cartelle = [lavoro(args.slug)]
    else:
        print("-> serve uno slug o --tutto (il lavoro sta in {})".format(radice), file=sys.stderr)
        return 2
    tot = 0
    for c in cartelle:
        if not c.is_dir():
            print(f"{c}: niente da pulire")
            continue
        n = sum(f.stat().st_size for f in c.rglob("*") if f.is_file())
        tot += n
        if args.prova_a_secco:
            print(f"{c}: {n / 1e6:.0f} MB (a secco)")
        else:
            shutil.rmtree(c)
            print(f"{c}: {n / 1e6:.0f} MB tolti")
    print(f"-> {tot / 1e6:.0f} MB{' da togliere' if args.prova_a_secco else ' liberati'}; il riepilogo in contenuti/render/ non si tocca")
    return 0


def cmd_setup(args) -> int:
    from ..anim.config import carica, registra_font
    from .compositing import maschera_riquadro, maschera_schermo
    from .ffmpeg import FfmpegMancante, trova_ffmpeg
    cfg = carica()
    try:
        ff, probe = trova_ffmpeg()
        print(f"ffmpeg: {ff}")
    except FfmpegMancante as e:
        print(f"ffmpeg: MANCA ({e})")
        return 1
    try:
        import manim
        print(f"manim: {manim.__version__}")
    except ImportError:
        print("manim: MANCA (uv sync)")
        return 1
    print(f"font registrati: {', '.join(f.name for f in registra_font(cfg))}")
    avatar = RADICE / cfg.presentatore.avatar
    if not avatar.exists() or args.forza:
        _avatar_segnaposto(avatar, cfg)
        print(f"avatar segnaposto: {avatar}")
    else:
        print(f"avatar: {avatar}")
    print(f"maschere: {maschera_riquadro(cfg).name}, {maschera_schermo(cfg).name}")
    import shutil
    print(f"voce sintetica ({cfg.dati['voce_sintetica'].get('comando')}): {'ok' if shutil.which(cfg.dati['voce_sintetica'].get('comando', 'say')) else 'non disponibile'}")
    return 0


def cmd_stile(args) -> int:
    from ..anim.config import carica
    from .stile import stato, trascrizioni
    cfg = carica()
    if args.trascrizioni:
        tr = trascrizioni(cfg, lingua=args.lingua, account=args.account)
        if not tr:
            print("-> nessuna trascrizione: controlla [stile] indice e trascrizioni nel config", file=sys.stderr)
            return 1
        for x in sorted(tr, key=lambda x: (x["account"], x["id"])):
            passo = f"{x['parole_al_s']:.1f} parole/s" if x["parole_al_s"] else "—"
            print(f"  {x['id']}  {x['account']:<24} {x['lingua']:<4} {x['durata_s']:5.0f} s  {x['parole']:4d} parole  {passo:<14} {x['file']}")
        print(f"-> {len(tr)} trascrizioni: leggine alcune INTERE (Read) prima di scrivere la VOCE; si prende il passo, non le frasi")
        return 0
    s = stato(cfg)
    c = s["corpus"]
    if c is None:
        print("corpus: nessuno ([stile].corpus vuoto)")
    elif not s["corpus_esiste"]:
        print(f"corpus: {c} (assente: in reelkit, `./reelkit export` dopo aver analizzato dei reel)")
    else:
        print(f"corpus: {c} ({s['reel']} reel, modificato il {s['corpus_data']})")
    g = s["guida"]
    if not s["guida_esiste"]:
        print(f"guida: {g} (assente)")
    else:
        print(f"guida: {g} (letta il {s['guida_data'] or '?'}, {s['guida_reel'] if s['guida_reel'] is not None else '?'} reel)")
    pt = s["pattern"]
    if pt is None:
        print("pattern: nessuno ([stile].pattern vuoto)")
    elif not s["pattern_esiste"]:
        print(f"pattern: {pt} (assente: in reelkit, `./reelkit pattern`)")
    else:
        n = "?" if s["pattern_reel"] is None else s["pattern_reel"]
        m = "?" if s["pattern_tag"] is None else s["pattern_tag"]
        print(f"pattern: {pt} ({n} reel, {m} tag, modificato il {s['pattern_data']})")
    if s["trascrizioni_n"]:
        print(f"trascrizioni: {s['trascrizioni']} ({s['trascrizioni_n']} reel, {s['trascrizioni_it']} in italiano: "
              "`uv run reel stile --trascrizioni`)")
        if s["corpus_esiste"] and s["trascrizioni_n"] > s["reel"]:
            print(f"  ⚠ {s['trascrizioni_n']} reel trascritti ma il corpus ne ha {s['reel']}: in reelkit `./reelkit export` "
                  "(entrano quelli analizzati), poi la guida sarà da rifare")
    spiega = {"manca": "lancia l'agente stilista",
              "provvisoria": "nata dalle regole dei docs, senza reel veri: si rifà quando il corpus ha dei reel",
              "aggiornata": "distillata da tutti i reel del corpus",
              "da rifare": "il corpus è cambiato dopo la guida: rilancia l'agente stilista"}
    print(f"verdetto: {s['verdetto']} ({spiega[s['verdetto']]})")
    return 0


def _avatar_segnaposto(dest: Path, cfg) -> None:
    """Un cerchio pieno con le iniziali del presentatore: sta nel riquadro finché non c'è la clip vera."""
    from PIL import Image, ImageDraw, ImageFont
    d = int(cfg.dati["riquadro"]["dimensione_px"]) * 2
    im = Image.new("RGB", (d, d), cfg.palette.secondario)
    dr = ImageDraw.Draw(im)
    iniziali = "".join(p[0] for p in str(cfg.presentatore.nome).split()[:2]).upper() or "P"
    try:
        f = ImageFont.truetype(str(RADICE / "assets" / "fonts" / "InterVariable.ttf"), d // 3)
    except OSError:
        f = ImageFont.load_default()
    dr.text((d / 2, d / 2), iniziali, font=f, fill=cfg.palette.sfondo, anchor="mm")
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="reel", description="Reel esplicativi con Manim e riquadro del presentatore")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def comune(p):
        p.add_argument("file")
        p.add_argument("--out", help="cartella di output (default contenuti/render/<slug>/)")
        p.add_argument("--strict", action="store_true", help="gli avvisi fanno fallire il comando")

    p = sub.add_parser("valida", help="parse + validazione + durate stimate, senza render"); p.add_argument("file"); p.add_argument("--strict", action="store_true")
    p.set_defaults(fn=cmd_valida)
    p = sub.add_parser("gobbo", help="teleprompter per registrare le clip"); p.add_argument("file"); p.add_argument("--scrivi", action="store_true")
    p.set_defaults(fn=cmd_gobbo)
    p = sub.add_parser("clip", help="stato delle clip registrate per scena"); p.add_argument("file")
    p.set_defaults(fn=cmd_clip)
    p = sub.add_parser("parlato", help="il testo recitato in registrazione contro la VOCE; --applica lo riporta nel .md")
    p.add_argument("file"); p.add_argument("--applica", action="store_true")
    p.set_defaults(fn=cmd_parlato)
    p = sub.add_parser("voce", help="genera le voci sintetiche di prova"); comune(p)
    p.set_defaults(fn=cmd_voce)
    p = sub.add_parser("anima", help="solo Manim: fotogrammi chiave e filmstrip per l'animatore"); comune(p)
    p.add_argument("--scena", type=int, default=None); p.add_argument("--qualita", choices="lmh", default=None); p.add_argument("--debug", action="store_true")
    p.add_argument("--json", action="store_true", help="un solo oggetto JSON su stdout (per l'agente animatore)")
    p.set_defaults(fn=cmd_anima)
    p = sub.add_parser("monta", help="Manim + compositing + concat → reel-9x16.mp4, cover, report"); comune(p)
    p.add_argument("--prova", action="store_true", help="senza clip: voce sintetica e avatar segnaposto (non pubblicabile)")
    p.add_argument("--scena", type=int, default=None); p.add_argument("--qualita", choices="lmh", default=None)
    p.add_argument("--anteprima", action="store_true", help="qualità ridotta, più veloce (solo per guardare)")
    p.set_defaults(fn=cmd_monta)
    p = sub.add_parser("registra", help="registra il presentatore in presa unica sull'anteprima --prova e taglia le clip per scena")
    p.add_argument("file", nargs="?"); p.add_argument("--out", help="cartella dell'anteprima (default contenuti/render/<slug>/)")
    p.add_argument("--video", help="dispositivo video avfoundation: indice o parte del nome"); p.add_argument("--audio", help="dispositivo audio")
    p.add_argument("--dispositivi", action="store_true", help="elenca fotocamere e microfoni ed esci")
    p.add_argument("--da-scena", type=int, default=None, help="scena di partenza (default: la prima senza clip)")
    p.add_argument("--spezza", metavar="PRESA", help="ritaglia le scene da una presa già registrata (es. presa-02), senza aprire la finestra")
    p.set_defaults(fn=cmd_registra)
    p = sub.add_parser("setup", help="controlla ffmpeg/manim/font, genera avatar segnaposto e maschere"); p.add_argument("--forza", action="store_true")
    p.set_defaults(fn=cmd_setup)
    p = sub.add_parser("stile", help="corpus di reelkit e stato della guida docs/stile-parlato.md")
    p.add_argument("--trascrizioni", action="store_true", help="elenca i reel trascritti (il parlato vero) con il percorso del testo")
    p.add_argument("--lingua", help="con --trascrizioni: solo questa lingua (es. it)")
    p.add_argument("--account", help="con --trascrizioni: solo questo account")
    p.set_defaults(fn=cmd_stile)
    p = sub.add_parser("strisce", help="fotogrammi fitti attorno a ogni beat e lungo la scena: ciò che il filmstrip a 6 istanti non mostra")
    p.add_argument("file"); p.add_argument("--out", help="cartella di render (default contenuti/render/<slug>/)")
    p.add_argument("--scena", type=int, default=None, help="solo questa scena (default: tutte quelle che hanno il video)")
    p.add_argument("--fps", type=float, default=8, help="fotogrammi al secondo nelle finestre dei beat (default 8)")
    p.add_argument("--finestra", type=float, default=1.3, help="secondi guardati attorno a ogni inizio di beat (default 1.3)")
    p.add_argument("--sorgente", choices=("scene", "anima"), default="scene", help="scene = _scene/NN.mp4 montata → NN-fitti-….png; anima = il video Manim di `anima` → NN-fitti-anima-….png")
    p.add_argument("--json", action="store_true", help="un solo oggetto JSON su stdout")
    p.set_defaults(fn=cmd_strisce)
    p = sub.add_parser("uscite", help="tappa T0b: le uscite vere dei testi attribuiti a un modello (claude -p) → contenuti/idee/uscite/")
    p.add_argument("file", help="l'idea con «Testi del modello: richieste da generare» nelle Note per il reel")
    p.add_argument("--per-modello", type=int, default=5, help="uscite per richiesta e per modello (default 5)")
    p.add_argument("--modelli", default="opus,sonnet", help="modelli di `claude --model`, nell'ordine delle sigle (default opus,sonnet)")
    p.add_argument("--timeout", type=float, default=300.0, help="secondi per chiamata (default 300)")
    p.add_argument("--prova-a-secco", action="store_true", help="stampa richieste e comandi senza lanciare niente")
    p.add_argument("--forza", action="store_true", help="sovrascrive il file delle uscite di oggi se esiste")
    p.set_defaults(fn=cmd_uscite)
    p = sub.add_parser("copione", help="il parlato del reel da un modello esterno (catena di [copione]) → contenuti/copioni/")
    p.add_argument("file", help="l'idea, con «## Tappe del parlato»")
    p.add_argument("--modello", help="un solo anello (es. gpt-5.4, deepseek-v4-pro, claude) invece della catena")
    p.add_argument("--nota", help="una richiesta del presentatore per questa versione (rigenera il copione)")
    p.add_argument("--parole", type=int, help="parole in tutto (default [copione] parole)")
    p.add_argument("--prova-a-secco", action="store_true", help="stampa il prompt, le trascrizioni, saldo e stime; non chiama")
    p.add_argument("--forza", action="store_true", help="rigenera anche se il copione c'è già")
    p.set_defaults(fn=cmd_copione)
    p = sub.add_parser("pulisci", help="svuota il lavoro transitorio di un reel ([percorsi] lavoro); il riepilogo resta")
    p.add_argument("slug", nargs="?"); p.add_argument("--tutto", action="store_true", help="tutti i reel")
    p.add_argument("--prova-a-secco", action="store_true", help="dice quanto toglierebbe, non tocca niente")
    p.set_defaults(fn=cmd_pulisci)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
