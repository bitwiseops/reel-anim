"""CLI `broll`: stesso stile di `tools/reel/__main__.py` — un `cmd_*(args) -> int` per sottocomando,
0 = fatto, 1 = errore applicativo, 2 = errore di sintassi o di argomenti, e gli import pesanti dentro
la funzione che li usa, mai in cima.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]


def _stampa(diag) -> None:
    for d in diag:
        print(f"  {'✗' if d.livello == 'errore' else '⚠'} {d}", file=sys.stderr)


def _rel(p: Path) -> str:
    try:
        return str(p.relative_to(RADICE))
    except ValueError:
        return str(p)


def cmd_piano(args) -> int:
    from tools.reel.parser import ErroreParse

    from .piano import da_sceneggiatura, esito, salva

    md = Path(args.file)
    if not md.exists():
        print(f"-> {md} non esiste", file=sys.stderr)
        return 2
    try:
        p, diag = da_sceneggiatura(md)
    except ErroreParse as e:
        _stampa(e.diagnostiche)
        print(f"-> {len(e.diagnostiche)} errori di sintassi in {md}", file=sys.stderr)
        return 2
    dest = salva(p)

    print(f"{p.slug} · {len(p.scene)} scene · {len(p.filmati)} a filmato")
    for s in p.scene:
        segno = "▣" if s.registro == "filmato" else "◻"
        coda = f" · «{s.query[0]}»" if s.query else ""
        print(f"  {segno} scena {s.n} [{s.tipo}] {s.durata_s:.1f}s ({s.origine_durata}) · {s.registro}{coda}")
    _stampa(diag)
    print(f"-> {_rel(dest)}")
    if args.json:
        import json
        print(json.dumps(esito(p, diag), ensure_ascii=False, indent=2))
    return 0


def cmd_stato(args) -> int:
    from .piano import PianoMancante, carica_piano, controlla, esito

    try:
        p = carica_piano(args.slug)
    except PianoMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    diag = controlla(p)
    if args.json:
        import json
        print(json.dumps(esito(p, diag), ensure_ascii=False, indent=2))
        return 0
    print(f"{p.slug} · piano del {p.quando or '?'} · sceneggiatura {p.hash_md}")
    for s in p.scene:
        if s.registro != "filmato":
            continue
        f = RADICE / "contenuti" / "media" / p.slug / (s.file or "")
        segno = "✔" if s.file and f.exists() else "✘"
        print(f"  {segno} scena {s.n} · {s.stato} · {len(s.candidati)} candidati · {s.file or '—'}")
    _stampa(diag)
    return 0


def cmd_cerca(args) -> int:
    from .fornitori import FornitoreNonConfigurato, RichiestaFallita, pexels
    from .piano import PianoMancante, carica_piano, salva

    try:
        p = carica_piano(args.slug)
    except PianoMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    scene = [s for s in p.scene if s.registro in ("filmato", "immagini")
             and (args.scena is None or s.n == args.scena)]
    if not scene:
        print("-> nessuna scena a filmato in questo piano", file=sys.stderr)
        return 1

    for s in scene:
        visti: dict[str, dict] = {}
        for q in s.query:
            try:
                for c in pexels.cerca(q, durata_min_s=s.durata_s, limite=args.max):
                    visti.setdefault(c.chiave, c.to_dict())
            except FornitoreNonConfigurato as e:
                print(f"-> {e}", file=sys.stderr)
                return 1
            except RichiestaFallita as e:
                print(f"  ⚠ scena {s.n}, «{q}»: {e}", file=sys.stderr)
        s.candidati = list(visti.values())[:args.max]
        s.stato = "da-scegliere" if s.candidati else s.stato
        verticali = sum(1 for c in s.candidati if c["altezza"] > c["larghezza"])
        print(f"  scena {s.n}: {len(s.candidati)} candidati ({verticali} verticali) "
              f"da {len(s.query)} query")
        if not s.candidati:
            print(f"  ⚠ scena {s.n}: nessun filmato per «{' / '.join(s.query)}» — "
                  "è un caso da immagini generate", file=sys.stderr)
    print(f"-> {_rel(salva(p))}")
    return 0


def cmd_provini(args) -> int:
    from .piano import PianoMancante, carica_piano
    from .provini import provini_scena

    try:
        p = carica_piano(args.slug)
    except PianoMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    fatti = 0
    for s in p.scene:
        if s.registro == "animazione" or (args.scena is not None and s.n != args.scena):
            continue
        scelto = s.scelti[0].get("candidato") if s.scelti else None
        foglio, diag = provini_scena(args.slug, s.n, s.candidati, s.durata_s, scelto)
        _stampa(diag)
        if foglio:
            print(f"  scena {s.n}: {_rel(foglio)}")
            fatti += 1
    if not fatti:
        print("-> nessun provino: prima `broll cerca`", file=sys.stderr)
        return 1
    print("-> guardali e scegli con `broll scegli <slug> --scena N --candidato <fornitore:id>`")
    return 0


def cmd_prova_immagini(args) -> int:
    from tools.reel.ffmpeg import FfmpegMancante, filmstrip, trova_ffmpeg

    from .immagini import ImmaginiMancanti, componi
    from .piano import _durate_dal_report

    try:
        trova_ffmpeg()
    except FfmpegMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    d = _durate_dal_report(args.slug).get(args.scena)
    if not d:
        print(f"-> nessun report per {args.slug} scena {args.scena}: prima "
              f"`uv run reel monta <sceneggiatura> --prova`", file=sys.stderr)
        return 1

    out = RADICE / "contenuti" / "render" / args.slug / "broll"
    try:
        video, tenute = componi([Path(p) for p in args.immagini], d["inizi_frasi_s"],
                                d["durata_s"], out / f"immagini-scena-{args.scena:02d}.mp4")
    except ImmaginiMancanti as e:
        print(f"-> {e}", file=sys.stderr)
        return 2
    except RuntimeError as e:
        print(f"-> {e}", file=sys.stderr)
        return 1

    print(f"scena {args.scena} · {d['durata_s']:.2f}s · beat da {d['origine_tempi'] or 'ignoto'}")
    for i, (inizio, durata) in enumerate(tenute):
        print(f"  immagine {i + 1}: da {inizio:6.2f}s per {durata:5.2f}s")
    # campiona subito prima e subito dopo ogni cambio: è lì che si vede se lo stacco cade sul beat
    tempi = [0.2]
    for inizio, _ in tenute[1:]:
        tempi += [max(0.0, inizio - 0.15), min(d["durata_s"] - 0.05, inizio + 0.15)]
    strip = filmstrip(video, tempi, out / f"immagini-scena-{args.scena:02d}-filmstrip.png", 220)
    print(f"  {_rel(video)}")
    print(f"-> {_rel(strip)}  (i cambi devono cadere sugli inizi frase)")
    return 0


def cmd_chiavi(args) -> int:
    from .credenziali import configurati, mascherata, stato

    for r in stato():
        segno = "✔" if r["valore"] else "·"
        print(f"  {segno} {r['nome']:<26} {mascherata(r['valore']):<24} {r['ruolo']:<12} {r['dove']}")
    ricerca, generazione = configurati("ricerca"), configurati("generazione")
    if not ricerca:
        print("-> manca un fornitore di ricerca (PEXELS_API_KEY o PIXABAY_API_KEY).", file=sys.stderr)
        print("   Mettila in .env nella radice (è in .gitignore), una riga: NOME=valore", file=sys.stderr)
        return 1
    print(f"-> ricerca: {', '.join(ricerca)}"
          + (f" · generazione: {', '.join(generazione)}" if generazione
             else " · generazione: nessuna (senza MESHY_API_KEY non si generano immagini)"))
    return 0


def cmd_prova_inquadratura(args) -> int:
    from tools.reel.ffmpeg import FfmpegMancante, trova_ffmpeg

    from .inquadratura import prova_inquadratura

    try:
        trova_ffmpeg()
    except FfmpegMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    filmato = Path(args.filmato)
    if not filmato.exists():
        print(f"-> {filmato} non esiste", file=sys.stderr)
        return 2
    try:
        foglio, png, diag = prova_inquadratura(args.slug, filmato, t=args.t, riquadro=args.riquadro)
    except RuntimeError as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    for p in png:
        print(f"  {_rel(p)}")
    _stampa(diag)
    print(f"-> {_rel(foglio)}  (guardalo e scegli dove ancorare il ritaglio)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="broll", description="Materiale esterno dei reel: piano, ricerca, resa")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("piano", help="propone il piano visivo di una sceneggiatura")
    p.add_argument("file", help="contenuti/sceneggiature/<file>.md")
    p.add_argument("--json", action="store_true", help="stampa anche l'esito per la pipeline")
    p.set_defaults(fn=cmd_piano)

    p = sub.add_parser("stato", help="a che punto è il piano di un reel")
    p.add_argument("slug")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_stato)

    p = sub.add_parser("cerca", help="cerca i candidati per le scene a filmato e li mette nel piano")
    p.add_argument("slug")
    p.add_argument("--scena", type=int)
    p.add_argument("--max", type=int, default=8, help="quanti candidati per scena (default 8)")
    p.set_defaults(fn=cmd_cerca)

    p = sub.add_parser("provini", help="contact sheet dei candidati, dalle miniature")
    p.add_argument("slug")
    p.add_argument("--scena", type=int)
    p.set_defaults(fn=cmd_provini)

    p = sub.add_parser("prova-immagini", help="immagini ferme montate sugli inizi frase di una scena")
    p.add_argument("slug")
    p.add_argument("--scena", type=int, required=True)
    p.add_argument("--immagini", nargs="+", required=True, help="una o più immagini, in ordine")
    p.set_defaults(fn=cmd_prova_immagini)

    p = sub.add_parser("chiavi", help="quali chiavi dei servizi esterni sono configurate (mascherate)")
    p.set_defaults(fn=cmd_chiavi)

    p = sub.add_parser("prova-inquadratura", help="lo stesso filmato ritagliato a 9:16 in più punti, col riquadro sopra")
    p.add_argument("slug")
    p.add_argument("--filmato", required=True, help="un video o un'immagine, scelto a mano")
    p.add_argument("--t", type=float, default=1.0, help="istante del filmato da cui prendere il fotogramma")
    p.add_argument("--riquadro", default="si", help="no | si | alto-destra | … (dove sta il presentatore)")
    p.set_defaults(fn=cmd_prova_inquadratura)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
