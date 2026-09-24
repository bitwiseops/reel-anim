"""`broll scrivi`: porta nella sceneggiatura le scene già rese, come `[broll]` con la loro riga `SCHERMO:`.

È l'unico punto in cui il sottosistema tocca il `.md`, e di suo lo fa il più tardi possibile: **quando i file
esistono già**. Cambia due cose per scena e nient'altro: il tipo nell'intestazione e la riga `SCHERMO:`. La
VOCE non si tocca, e nemmeno il brief `ANIMAZIONE:`, che resta a dire cosa si vede.

Con `--presto` marca le scene a filmato del piano **prima** che siano scelte e rese, col nome di file che
`broll rendi` scriverà: così l'animatore sa subito quali scene non sono sue (`reel anima` le salta) e lavora
mentre si scelgono i filmati. `reel valida` sul file che manca avvisa e basta; a pretenderlo è `reel monta`.

Quello che non sa decidere lo lascia al presentatore: una scena con `TESTO:` non la converte, perché
sopra il filmato non va nessuna grafica e togliere un'etichetta è una scelta editoriale, non un dettaglio
tecnico. Prima di scrivere rilegge il risultato con il parser e i controlli del repo: se esce un errore,
il file resta com'era. Il ritorno indietro è `git checkout` del `.md`.
"""
from __future__ import annotations

from pathlib import Path

from tools.reel.clip import cartella as cartella_media
from tools.reel.model import Diagnostica, avviso, errore
from tools.reel.parser import RE_H2_SCENA, ErroreParse, parse_testo
from tools.reel.validate import check

from .piano import Piano, ScenaBroll

RE_TESTO = "testo:"
RE_SCHERMO = "schermo:"


def _blocco(righe: list[str], n: int) -> tuple[int, int] | None:
    """Gli indici [inizio, fine) delle righe della scena `n`, intestazione compresa."""
    inizio = None
    for i, riga in enumerate(righe):
        m = RE_H2_SCENA.match(riga.rstrip())
        if m and int(m.group(1)) == n:
            inizio = i
        elif inizio is not None and riga.startswith("## "):
            return inizio, i
    return (inizio, len(righe)) if inizio is not None else None


def _intestazione(riga: str) -> str:
    """`## Scena 4 [spiegazione, durata=9s]` → `## Scena 4 [broll, durata=9s]`: gli attributi restano.

    L'hook resta `[hook]`: la Scena 1 dev'esserlo, e il suo TITOLO serve alla copertina. A renderlo un hook
    a filmato è la riga `SCHERMO:`.
    """
    m = RE_H2_SCENA.match(riga.rstrip())
    parti = [p.strip() for p in (m.group(2) or "").split(",") if p.strip()]
    tipo = "hook" if parti and parti[0].lower() == "hook" else "broll"
    return f"## Scena {m.group(1)} [{', '.join([tipo, *[p for p in parti if '=' in p]])}]"


def applica(testo: str, scene: list[ScenaBroll], media: Path,
            presto: bool = False) -> tuple[str, list[int], list[Diagnostica]]:
    """Il testo della sceneggiatura con le scene rese convertite. Ritorna (testo, scene scritte, diagnostica).

    Con `presto` si convertono tutte le scene non animate del piano, anche senza il file: il filmato arriva dopo.
    """
    righe = testo.split("\n")
    diag: list[Diagnostica] = []
    scritte: list[int] = []
    for s in scene:
        if s.registro == "animazione":
            continue
        if not presto and (s.stato != "reso" or not s.file or not (media / s.file).exists()):
            diag.append(avviso("non ancora resa: prima `broll scegli` e `broll rendi`", scena=s.n))
            continue
        dove = _blocco(righe, s.n)
        if dove is None:
            diag.append(errore("è nel piano ma non nella sceneggiatura: rifai `broll piano`", scena=s.n))
            continue
        inizio, fine = dove
        corpo = righe[inizio + 1:fine]
        if any(r.strip().lower().startswith(RE_TESTO) for r in corpo):
            diag.append(avviso("ha un TESTO: sopra il filmato non va nessuna grafica. Toglilo tu dalla "
                               "sceneggiatura (o lascia la scena animata), poi rilancia", scena=s.n))
            continue
        if any(r.strip().lower().replace(" ", "") == "riquadro:no" for r in corpo):
            diag.append(avviso("ha RIQUADRO: no: sopra il filmato il presentatore non si vedrà. Se è l'hook, "
                               "togli quella riga: il titolo non è più a schermo", scena=s.n))
        nuova = [_intestazione(righe[inizio]), f"SCHERMO: {s.nome_file()}"]
        nuova += [r for r in corpo if not r.strip().lower().startswith(RE_SCHERMO)]
        if righe[inizio:fine] != nuova:
            righe[inizio:fine] = nuova
            scritte.append(s.n)
    return "\n".join(righe), scritte, diag


def scrivi(p: Piano, md: Path, presto: bool = False) -> tuple[list[int], list[Diagnostica]]:
    """Applica al `.md` e lo salva solo se il risultato regge `valida`. Non tocca il piano."""
    testo, scritte, diag = applica(md.read_text(encoding="utf-8"), p.scene, cartella_media(p.slug), presto)
    if not scritte:
        return [], diag
    try:
        r, _ = parse_testo(testo, md)
        errori = [d for d in check(r) if d.livello == "errore"]
    except ErroreParse as e:
        errori = e.diagnostiche
    if errori:
        return [], diag + [errore(f"la sceneggiatura riscritta non passa `valida`, non la salvo: {d}") for d in errori]
    tmp = md.with_suffix(md.suffix + ".tmp")
    tmp.write_text(testo, encoding="utf-8")
    tmp.replace(md)
    return scritte, diag
