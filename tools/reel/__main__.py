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


def cmd_clip(args) -> int:
    from . import clip
    from .stima import durata_stimata_s
    r, _ = _carica(Path(args.file))
    st = clip.stato(r.slug, [s.n for s in r.scene])
    mancanti = 0
    for s, c in zip(r.scene, st):
        target = durata_stimata_s(s)
        if c["presente"]:
            d = c.get("durata_s") or 0
            delta = (d - target) / target * 100 if target else 0
            nota = "  ← durata molto diversa dalla stima" if abs(delta) > 30 else ""
            print(f"scena {s.n}: ✔ {c['file']}  {d:.1f}s (stima {target:.0f}s, {delta:+.0f} %){nota}")
        else:
            mancanti += 1
            print(f"scena {s.n}: ✘ manca {c['atteso']}  (target ~{target:.0f}s)")
    print(f"-> {len(st) - mancanti}/{len(st)} clip presenti in contenuti/media/{r.slug}/")
    return 1 if mancanti else 0


def cmd_voce(args) -> int:
    from .monta import out_dir
    from .voce import sintetizza_frasi
    r, _ = _carica(Path(args.file))
    out = out_dir(r, args.out)
    for s in r.scene:
        if s.voce:
            v = sintetizza_frasi(s.voce, out / "_voce" / f"{s.n:02d}.m4a")
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
        try:
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
    p = sub.add_parser("setup", help="controlla ffmpeg/manim/font, genera avatar segnaposto e maschere"); p.add_argument("--forza", action="store_true")
    p.set_defaults(fn=cmd_setup)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
