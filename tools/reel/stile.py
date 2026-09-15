"""Stato della guida di stile (docs/stile-parlato.md) rispetto al corpus di reelkit (export.md).

È un controllo informativo, non una regola: dice se la guida che lo sceneggiatore legge è stata distillata da tutti i
reel del corpus. La guida la scrive l'agente `stilista`; la sezione «## Corpus» ha un formato fisso che si legge qui.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

_RE_REEL = re.compile(r"^### \S+ · ", re.M)          # un titolo per reel nell'export di reelkit
_RE_LETTI = re.compile(r"Reel letti:\s*(\d+)")
_RE_DATA = re.compile(r"Letto il:\s*(\d{4}-\d{2}-\d{2})")


def conta_reel(corpus: Path | None) -> int:
    if corpus is None or not corpus.is_file():
        return 0
    return len(_RE_REEL.findall(corpus.read_text(encoding="utf-8")))


def leggi_guida(guida: Path | None) -> dict:
    """Data e numero di reel dichiarati nella sezione «## Corpus» della guida (None se mancano)."""
    if guida is None or not guida.is_file():
        return {"data": None, "reel": None}
    t = guida.read_text(encoding="utf-8")
    m, d = _RE_LETTI.search(t), _RE_DATA.search(t)
    return {"data": d.group(1) if d else None, "reel": int(m.group(1)) if m else None}


def stato(cfg) -> dict:
    """verdetto: manca (niente guida) · provvisoria (corpus assente o vuoto) · aggiornata · da rifare."""
    corpus, guida = cfg.percorso("stile", "corpus"), cfg.percorso("stile", "guida")
    reel = conta_reel(corpus)
    g = leggi_guida(guida)
    guida_esiste = guida is not None and guida.is_file()
    corpus_esiste = corpus is not None and corpus.is_file()
    corpus_data = dt.date.fromtimestamp(corpus.stat().st_mtime).isoformat() if corpus_esiste else None
    if not guida_esiste:
        verdetto = "manca"
    elif reel == 0:
        verdetto = "provvisoria"
    elif g["reel"] == reel and g["data"] is not None and corpus_data <= g["data"]:
        verdetto = "aggiornata"
    else:
        verdetto = "da rifare"
    return {"corpus": corpus, "corpus_esiste": corpus_esiste, "corpus_data": corpus_data, "reel": reel,
            "guida": guida, "guida_esiste": guida_esiste, "guida_data": g["data"], "guida_reel": g["reel"],
            "verdetto": verdetto}
