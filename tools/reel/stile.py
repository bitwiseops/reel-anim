"""Stato della guida di stile (docs/stile-parlato.md) rispetto al corpus di reelkit (export.md).

È un controllo informativo, non una regola: dice se la guida che lo sceneggiatore legge è stata distillata da tutti i
reel del corpus. La guida la scrive l'agente `stilista`; la sezione «## Corpus» ha un formato fisso che si legge qui.
Riporta anche il file dei pattern narrativi di reelkit (pattern.md), che gli agenti leggono direttamente.
"""
from __future__ import annotations

import json

import datetime as dt
import re
from pathlib import Path

_RE_REEL = re.compile(r"^### \S+ · ", re.M)          # un titolo per reel nell'export di reelkit
_RE_LETTI = re.compile(r"Reel letti:\s*(\d+)")
_RE_DATA = re.compile(r"Letto il:\s*(\d{4}-\d{2}-\d{2})")
_RE_PATTERN = re.compile(r"^(\d+) reel analizzati, (\d+) tag distinti", re.M)


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


def leggi_pattern(p: Path | None) -> dict:
    """Reel, tag e data di modifica dalla riga «N reel analizzati, M tag distinti» di pattern.md (None se mancano)."""
    if p is None or not p.is_file():
        return {"esiste": False, "reel": None, "tag": None, "data": None}
    m = _RE_PATTERN.search(p.read_text(encoding="utf-8"))
    return {"esiste": True, "reel": int(m.group(1)) if m else None, "tag": int(m.group(2)) if m else None,
            "data": dt.date.fromtimestamp(p.stat().st_mtime).isoformat()}


def trascrizioni(cfg, lingua: str | None = None, account: str | None = None) -> list[dict]:
    """I reel trascritti di reelkit, dall'indice: chi parla, in che lingua, per quanto, e dov'è il testo.

    La guida `docs/stile-parlato.md` dà le regole; le trascrizioni danno l'orecchio. Lo sceneggiatore ne legge
    alcune **intere** prima del monologo, perché il ritmo del parlato (gli attacchi, le riprese, le frasi lasciate
    a metà) non sopravvive a una regola. `parole_al_s` dice quanto corre chi parla: serve a scegliere reel del
    passo del presentatore. Si leggono solo le voci che hanno davvero il file del testo.
    """
    indice, cartella = cfg.percorso("stile", "indice"), cfg.percorso("stile", "trascrizioni")
    if indice is None or cartella is None or not indice.is_file() or not cartella.is_dir():
        return []
    try:
        voci = json.loads(indice.read_text(encoding="utf-8")).get("voci", [])
    except (json.JSONDecodeError, AttributeError):
        return []
    out = []
    for v in voci:
        f = cartella / f"{v.get('id')}.txt"
        if not f.is_file():
            continue
        if (lingua and v.get("lingua") != lingua) or (account and v.get("account") != account):
            continue
        parole = len(f.read_text(encoding="utf-8").split())
        durata = float((v.get("registrazione") or {}).get("durata_s") or 0)
        out.append({"id": v["id"], "account": v.get("account") or "?", "lingua": v.get("lingua") or "?",
                    "durata_s": durata, "parole": parole, "parole_al_s": round(parole / durata, 1) if durata else None,
                    "analizzato": v.get("stato") == "analizzato", "file": f})
    return out


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
    pattern = cfg.percorso("stile", "pattern")
    pt = leggi_pattern(pattern)
    tr = trascrizioni(cfg)
    return {"trascrizioni": cfg.percorso("stile", "trascrizioni"), "trascrizioni_n": len(tr),
            "trascrizioni_it": sum(1 for x in tr if x["lingua"] == "it"),
            "corpus": corpus, "corpus_esiste": corpus_esiste, "corpus_data": corpus_data, "reel": reel,
            "guida": guida, "guida_esiste": guida_esiste, "guida_data": g["data"], "guida_reel": g["reel"],
            "verdetto": verdetto, "pattern": pattern, "pattern_esiste": pt["esiste"], "pattern_reel": pt["reel"],
            "pattern_tag": pt["tag"], "pattern_data": pt["data"]}
