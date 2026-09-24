"""Da una scena alle query di ricerca del materiale.

Euristica della M1: le parole piene del brief `ANIMAZIONE:` (che è già la descrizione di cosa si vede)
e, in coda, quelle della `VOCE:`. Non serve trascrivere niente: il parlato è già testo nel `.md`.
Dalla M5 le query le scrive l'agente, che ha davanti il contesto della scena; questa resta il ripiego.
"""
from __future__ import annotations

import re
from collections import Counter

from tools.anim.config import Config
from tools.reel.model import Scena, testo_piano

PAROLE_PER_QUERY = 5

# parole che non descrivono niente di filmabile: articoli, preposizioni, ausiliari, e il gergo dei brief
VUOTE = {
    "a", "ad", "ai", "al", "alla", "alle", "allo", "agli", "anche", "ancora", "che", "chi", "ci", "co",
    "col", "come", "con", "cosa", "cui", "da", "dal", "dalla", "dalle", "dallo", "dagli", "dai", "degli",
    "dei", "del", "della", "delle", "dello", "di", "dove", "due", "e", "ecco", "ed", "gli", "ha", "hai",
    "hanno", "ho", "i", "il", "in", "io", "l", "la", "le", "lei", "li", "lo", "lui", "ma", "me", "mi",
    "ne", "nei", "nel", "nella", "nelle", "nello", "negli", "non", "noi", "o", "per", "però", "più",
    "poi", "può", "quando", "quel", "quella", "quelle", "quelli", "quello", "questa", "queste", "questi",
    "questo", "se", "sei", "si", "sì", "sia", "siamo", "sono", "su", "sua", "sue", "sui", "sul", "sulla",
    "sulle", "suo", "ti", "tra", "tre", "tu", "tua", "tue", "tuo", "un", "una", "uno", "va", "vai",
    "ve", "vi", "via", "già", "solo", "tutto", "tutta", "tutti", "tutte", "essere", "fare", "dire",
    # gergo dei brief di animazione: descrive il montaggio, non il soggetto
    "scena", "beat", "frase", "entra", "esce", "compare", "sparisce", "sinistra", "destra", "alto",
    "basso", "centro", "sopra", "sotto", "accanto", "riga", "righe", "testo", "titolo", "parola",
    "parole", "schermo", "grande", "piccolo", "colore", "accento", "attenuato", "dissolvenza",
    "animazione", "carta", "carte", "cartellino", "cartellini", "freccia", "barra", "contatore",
}


def _parole(testo: str) -> list[str]:
    piano = testo_piano(testo).lower()
    piano = re.sub(r"[«»\"'`()\[\]{}.,;:!?…–—/\\]", " ", piano)
    return [w for w in piano.split() if len(w) > 2 and w not in VUOTE and not w.isdigit()]


def _frase(parole: list[str], quante: int = PAROLE_PER_QUERY) -> str:
    """Le prime `quante` parole distinte, nell'ordine in cui compaiono."""
    viste, out = set(), []
    for w in parole:
        if w in viste:
            continue
        viste.add(w)
        out.append(w)
        if len(out) == quante:
            break
    return " ".join(out)


def query_scena(s: Scena, cfg: Config | None = None) -> list[str]:
    """Le query di una scena, dalla più descrittiva alla più generica; vuota se non c'è niente da dire.

    **Solo dal brief `ANIMAZIONE:`, che è già una descrizione di cosa si vede.** La VOCE entra soltanto
    se il brief manca: un sacchetto delle sue parole più frequenti non descrive un'immagine, e cercandolo
    tornano filmati a caso («pensa scegli fretta cambiata volte» riporta un traliccio e un'impalcatura).
    """
    query: list[str] = []
    for riga in s.animazione:
        q = _frase(_parole(riga))
        if q and q not in query:
            query.append(q)
        if len(query) == 2:
            break
    if query:
        return query

    parole_voce = _parole(s.voce_piena)
    if parole_voce:
        comuni = [w for w, _ in Counter(parole_voce).most_common(PAROLE_PER_QUERY)]
        # rimesse nell'ordine del parlato: «mail candidatura scrivere» si cerca meglio del contrario
        q = " ".join(sorted(comuni, key=parole_voce.index))
        if q:
            query.append(q)
    return query
