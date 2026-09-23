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

    from .piano import PianoMancante, carica_piano, da_sceneggiatura, eredita, esito, salva

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
    ereditate: list[int] = []
    if not args.da_capo:
        try:
            ereditate = eredita(p, carica_piano(p.slug))
        except PianoMancante:
            pass
    dest = salva(p)

    generate = [s for s in p.scene if s.registro == "immagini"]
    print(f"{p.slug} · {len(p.scene)} scene · {len(p.filmati)} a filmato"
          + (f" · {len(generate)} a immagini generate" if generate else ""))
    for s in p.scene:
        segno = {"filmato": "▣", "immagini": "▤"}.get(s.registro, "◻")
        coda = f" · «{s.query[0]}»" if s.query else ""
        if s.n in ereditate:
            coda += f" · {s.stato}, dal piano di prima" + (f" ({s.note})" if s.stato == "scelto" and s.note else "")
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
    for s in p.esterne:
        f = RADICE / "contenuti" / "media" / p.slug / (s.file or "")
        segno = "✔" if s.file and f.exists() else "✘"
        quanti = (f"{len(s.scelti)} immagini" if s.registro == "immagini"
                  else f"{len(s.candidati)} candidati")
        print(f"  {segno} scena {s.n} · {s.registro} · {s.stato} · {quanti} · {s.file or '—'}")
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
    # le scene già risolte con immagini generate non si cercano: non c'è niente da trovare su Pexels
    scene = [s for s in p.esterne if (args.scena is None or s.n == args.scena)
             and not any(t.get("generata") for t in s.scelti)]
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
        # una scena già scelta resta scelta: cercare ancora allarga la rosa, non disfa la decisione
        s.stato = "da-scegliere" if s.candidati and not s.scelti else s.stato
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
    from .provini import provini_immagini, provini_scena

    try:
        p = carica_piano(args.slug)
    except PianoMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    fatti = 0
    for s in p.esterne:
        if args.scena is not None and s.n != args.scena:
            continue
        if s.registro == "immagini":
            foglio, diag = provini_immagini(args.slug, s.n, s.scelti)
        else:
            scelto = s.scelti[0].get("candidato") if s.scelti else None
            foglio, diag = provini_scena(args.slug, s.n, s.candidati, s.durata_s, scelto)
        _stampa(diag)
        if foglio:
            print(f"  scena {s.n}: {_rel(foglio)}")
            fatti += 1
    if not fatti:
        print("-> nessun provino: prima `broll cerca` (o `broll genera`)", file=sys.stderr)
        return 1
    print("-> guardali e scegli con `broll scegli <slug> --scena N --candidato <fornitore:id>`")
    return 0


def cmd_scegli(args) -> int:
    from .piano import PianoMancante, carica_piano, salva
    from .scelta import SceltaNonValida, ancora, controlla_scelta, scegli

    try:
        p = carica_piano(args.slug)
    except PianoMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    s = p.scena(args.scena)
    if s is None:
        print(f"-> la scena {args.scena} non è nel piano", file=sys.stderr)
        return 2
    try:
        taglio = scegli(s, args.candidato, da_s=args.da, ancora_x=ancora(args.ancora), aggiungi=args.aggiungi)
    except SceltaNonValida as e:
        print(f"-> {e}", file=sys.stderr)
        return 2
    diag = controlla_scelta(s)
    print(f"  scena {s.n} · {s.durata_s:.1f}s · {len(s.scelti)} "
          f"{'taglio' if len(s.scelti) == 1 else 'tagli'}: " + ", ".join(t["candidato"] for t in s.scelti))
    print(f"  {taglio['candidato']} · da {taglio['da_s']:.1f}s · ancora {taglio['ancora']:.0%} · "
          f"{taglio.get('autore') or 'autore non indicato'}")
    _stampa(diag)
    print(f"-> {_rel(salva(p))}")
    if any(d.livello == "errore" for d in diag):
        print("-> così `broll rendi` si rifiuta: correggi la scelta", file=sys.stderr)
        return 1
    print(f"-> poi `broll rendi {p.slug}`")
    return 0


def cmd_genera(args) -> int:
    from .fornitori import FornitoreNonConfigurato, RichiestaFallita
    from .genera import PromptMancante, genera_scena
    from .piano import PianoMancante, carica_piano, salva
    from .provini import provini_immagini

    try:
        p = carica_piano(args.slug)
    except PianoMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    s = p.scena(args.scena)
    if s is None:
        print(f"-> la scena {args.scena} non è nel piano", file=sys.stderr)
        return 2
    try:
        schede, diag = genera_scena(s, args.prompt, quante=args.quante, forza=args.forza)
    except PromptMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 2
    except FornitoreNonConfigurato as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    except RichiestaFallita as e:
        print(f"-> {e}", file=sys.stderr)
        return 1

    print(f"  scena {s.n} · {s.durata_s:.1f}s · {len(schede)} immagini generate")
    for i, scheda in enumerate(schede, start=1):
        segno = "·" if scheda.get("da_cache") else "✚"
        print(f"  {segno} {i}. {scheda['file']}")
        print(f"      «{scheda['prompt'][:120]}»")
    _stampa(diag)
    foglio, avvisi = provini_immagini(p.slug, s.n, schede)
    _stampa(avvisi)
    print(f"-> {_rel(salva(p))}")
    if foglio:
        print(f"-> {_rel(foglio)}  (guardalo prima di rendere)")
    print(f"-> poi `broll rendi {p.slug} --scena {s.n}`")
    return 0


def cmd_rendi(args) -> int:
    from tools.reel.clip import cartella as cartella_media
    from tools.reel.ffmpeg import FfmpegMancante, filmstrip, tempi_campione, trova_ffmpeg

    from .crediti import scrivi as scrivi_crediti
    from .fornitori import RichiestaFallita
    from .immagini import finestre
    from .piano import PianoMancante, carica_piano, hash_sceneggiatura, salva
    from .provini import cartella as cartella_provini
    from .rendi import rendi_scena
    from .scelta import confini, controlla_scelta

    try:
        trova_ffmpeg()
        p = carica_piano(args.slug)
    except (FfmpegMancante, PianoMancante) as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    md = RADICE / p.sorgente
    if md.is_file() and hash_sceneggiatura(md) != p.hash_md:
        print(f"  ⚠ {p.sorgente} è cambiata dopo il piano: le durate delle scene possono non valere più "
              "(rifai `broll piano`)", file=sys.stderr)

    scene = [s for s in p.esterne if args.scena is None or s.n == args.scena]
    if not scene:
        print("-> nessuna scena a filmato o a immagini da rendere", file=sys.stderr)
        return 1
    falliti = 0
    for s in scene:
        dest = cartella_media(p.slug) / (s.file or f"broll-scena-{s.n:02d}.mp4")
        if s.stato == "reso" and dest.exists() and not args.forza:
            print(f"  ✔ scena {s.n}: già resa ({_rel(dest)}), `--forza` per rifarla")
            continue
        diag = controlla_scelta(s)
        _stampa(diag)
        if any(d.livello == "errore" for d in diag):
            falliti += 1
            continue
        try:
            video, avvisi = rendi_scena(p.slug, s)
        except (RichiestaFallita, RuntimeError) as e:
            print(f"  ✗ scena {s.n}: {e}", file=sys.stderr)
            falliti += 1
            continue
        _stampa(avvisi)
        salva(p)                                # una scena alla volta: se la prossima fallisce, questa resta
        # si guarda subito: l'inizio, la fine, e un fotogramma prima e dopo ogni stacco
        tempi = tempi_campione(s.durata_s, 5)
        if s.registro == "immagini":
            cambi = [i for i, _ in finestre(s.inizi_frasi_s, s.durata_s)[1:]]
        else:
            cambi = [i for i, _ in confini(len(s.scelti), s.inizi_frasi_s, s.durata_s)[1:]]
        for inizio in cambi:
            tempi += [max(0.0, inizio - 0.1), min(s.durata_s - 0.05, inizio + 0.1)]
        strip = filmstrip(video, sorted(tempi), cartella_provini(p.slug) / f"reso-scena-{s.n:02d}.png", 220)
        etichette = [t.get("candidato") or Path(t.get("file") or "?").name for t in s.scelti]
        print(f"  {'▤' if s.registro == 'immagini' else '▣'} scena {s.n}: {_rel(video)} · "
              f"{s.durata_s:.2f}s · " + " + ".join(etichette))
        print(f"    {_rel(strip)}")
    print(f"-> {_rel(scrivi_crediti(p))}")
    if falliti:
        print(f"-> {falliti} scene non rese", file=sys.stderr)
        return 1
    return 0


def cmd_scrivi(args) -> int:
    from .piano import PianoMancante, carica_piano, hash_sceneggiatura, salva
    from tools.reel.clip import cartella as cartella_media

    from .scrivi import nome_file, scrivi

    try:
        p = carica_piano(args.slug)
    except PianoMancante as e:
        print(f"-> {e}", file=sys.stderr)
        return 1
    md = RADICE / p.sorgente
    if not md.is_file():
        print(f"-> {p.sorgente} non esiste più: rifai `broll piano`", file=sys.stderr)
        return 1
    scritte, diag = scrivi(p, md, presto=args.presto)
    _stampa(diag)
    if any(d.livello == "errore" for d in diag):
        return 1
    if not scritte:
        print(f"-> niente da scrivere in {p.sorgente}")
        return 0
    p.hash_md = hash_sceneggiatura(md)          # il piano resta allineato al file che ha appena cambiato
    salva(p)
    print(f"  scene {', '.join(str(n) for n in scritte)} → [broll] con la loro riga SCHERMO:")
    print(f"-> {p.sorgente}  (si torna indietro con `git checkout`)")
    da_rendere = [s.n for s in p.scene if s.n in scritte and not (cartella_media(p.slug) / nome_file(s)).exists()]
    if da_rendere:
        # --presto: le scene sono marcate, i filmati no. L'animatore può partire (`reel anima` le salta), il
        # montaggio no: `reel monta` si ferma finché il file non c'è
        print(f"-> {len(da_rendere)} scene marcate, filmato da rendere ({', '.join(str(n) for n in da_rendere)}): "
              f"intanto `uv run reel anima {p.sorgente}`; per il montaggio prima `broll scegli` e `broll rendi {p.slug}`")
        return 0
    print(f"-> poi `uv run reel valida {p.sorgente}` e `uv run reel monta {p.sorgente} --prova --anteprima`")
    return 0


def cmd_prova_immagini(args) -> int:
    from tools.reel.ffmpeg import FfmpegMancante, filmstrip, trova_ffmpeg

    from .immagini import ImmaginiMancanti, componi, dissolvenza_s
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

    print(f"scena {args.scena} · {d['durata_s']:.2f}s · beat da {d['origine_tempi'] or 'ignoto'} · "
          f"dissolvenza {dissolvenza_s(tenute):.2f}s")
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
    p.add_argument("--da-capo", action="store_true", help="butta candidati e scelte del piano di prima")
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

    p = sub.add_parser("scegli", help="fissa nel piano il filmato di una scena")
    p.add_argument("slug")
    p.add_argument("--scena", type=int, required=True)
    p.add_argument("--candidato", required=True, help="<fornitore:id>, come nei provini")
    p.add_argument("--da", type=float, default=0.0, help="da che secondo del filmato partire (default 0)")
    p.add_argument("--ancora", default="centro", help="sinistra | centro | destra | 0-1: dove ritagliare un orizzontale")
    p.add_argument("--aggiungi", action="store_true", help="un taglio in più nella stessa scena, invece di sostituire")
    p.set_defaults(fn=cmd_scegli)

    p = sub.add_parser("genera", help="genera con Meshy le immagini di una scena e le mette nel piano")
    p.add_argument("slug")
    p.add_argument("--scena", type=int, required=True)
    p.add_argument("--prompt", action="append", default=[],
                   help="un prompt per immagine, ripetibile; senza, si ricava dal brief ANIMAZIONE:")
    p.add_argument("--quante", type=int, default=3,
                   help="quante immagini quando i prompt non li passi (default 3)")
    p.add_argument("--forza", action="store_true", help="rigenera anche quello che è già in cache (costa)")
    p.set_defaults(fn=cmd_genera)

    p = sub.add_parser("rendi", help="scarica i filmati scelti e scrive broll-scena-NN.mp4")
    p.add_argument("slug")
    p.add_argument("--scena", type=int)
    p.add_argument("--forza", action="store_true", help="rifà anche le scene già rese")
    p.set_defaults(fn=cmd_rendi)

    p = sub.add_parser("scrivi", help="porta nella sceneggiatura le scene rese, come [broll] con SCHERMO:")
    p.add_argument("slug")
    p.add_argument("--presto", action="store_true",
                   help="marca anche le scene non ancora rese: l'animatore parte mentre si scelgono i filmati")
    p.set_defaults(fn=cmd_scrivi)

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
