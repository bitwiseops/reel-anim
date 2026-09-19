"""`CREDITI.md`: di chi sono i filmati del reel, pronto per la didascalia.

La licenza Pexels non obbliga al credito, ma il servizio lo chiede e a noi costa una riga. Il file sta
accanto al piano e va in git: è la prova di provenienza di quello che si pubblica.
"""
from __future__ import annotations

from pathlib import Path

from .piano import Piano, cartella


def testo(p: Piano) -> str:
    righe = [f"# Crediti — {p.slug}", "", "Materiale esterno usato nel reel, in ordine di scena.", ""]
    autori: list[str] = []
    for s in p.scene:
        for t in s.scelti:
            autore = t.get("autore") or "autore non indicato"
            firma = f"[{autore}]({t['autore_url']})" if t.get("autore_url") else autore
            righe.append(f"- Scena {s.n}: {firma} · {t['fornitore'].capitalize()} · "
                         f"{t.get('url_pagina') or t['candidato']} · {t.get('licenza') or 'licenza da verificare'}")
            if autore not in autori:
                autori.append(autore)
    if not autori:
        righe.append("Nessun filmato scelto.")
    else:
        fornitori = sorted({t["fornitore"].capitalize() for s in p.scene for t in s.scelti})
        righe += ["", "## Per la didascalia", "", f"Filmati: {', '.join(autori)} ({', '.join(fornitori)})"]
    return "\n".join(righe) + "\n"


def scrivi(p: Piano) -> Path:
    dest = cartella(p.slug) / "CREDITI.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".md.tmp")
    tmp.write_text(testo(p), encoding="utf-8")
    tmp.replace(dest)
    return dest
