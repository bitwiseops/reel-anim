"""`CREDITI.md`: da dove viene il materiale esterno del reel, pronto per la didascalia.

La licenza Pexels non obbliga al credito, ma il servizio lo chiede e a noi costa una riga. Il file sta
accanto al piano e va in git: è la prova di provenienza di quello che si pubblica.

Un'immagine **generata** non ha un autore da citare, e attribuirgliene uno sarebbe falso: si dichiara per
quello che è — generata con Meshy, con quale modello, quando e da quale prompt. Il prompt è la parte che
conta, perché è l'unica cosa che rende ripetibile un'immagine che non sta in git.
"""
from __future__ import annotations

from pathlib import Path

from .piano import Piano, cartella


def _riga_generata(n: int, t: dict) -> str:
    """Una riga per un'immagine generata: niente autore, ma modello, data e prompt."""
    quando = f", {t['quando']}" if t.get("quando") else ""
    prompt = (t.get("prompt") or "").strip()
    return (f"- Scena {n}: immagine **generata** con {t['fornitore'].capitalize()} "
            f"({t.get('modello') or 'modello non indicato'}{quando}) · prompt: «{prompt}»")


def _riga_filmato(n: int, t: dict) -> tuple[str, str]:
    autore = t.get("autore") or "autore non indicato"
    firma = f"[{autore}]({t['autore_url']})" if t.get("autore_url") else autore
    return autore, (f"- Scena {n}: {firma} · {t['fornitore'].capitalize()} · "
                    f"{t.get('url_pagina') or t['candidato']} · "
                    f"{t.get('licenza') or 'licenza da verificare'}")


def testo(p: Piano) -> str:
    righe = [f"# Crediti — {p.slug}", "", "Materiale esterno usato nel reel, in ordine di scena.", ""]
    autori: list[str] = []
    generate: list[str] = []
    for s in p.scene:
        for t in s.scelti:
            if t.get("generata"):
                righe.append(_riga_generata(s.n, t))
                modello = t.get("modello") or ""
                if modello not in generate:
                    generate.append(modello)
                continue
            autore, riga = _riga_filmato(s.n, t)
            righe.append(riga)
            if autore not in autori:
                autori.append(autore)
    if not autori and not generate:
        righe.append("Nessun filmato scelto.")
        return "\n".join(righe) + "\n"

    righe += ["", "## Per la didascalia", ""]
    if autori:
        fornitori = sorted({t["fornitore"].capitalize() for s in p.scene for t in s.scelti
                            if not t.get("generata")})
        righe.append(f"Filmati: {', '.join(autori)} ({', '.join(fornitori)})")
    if generate:
        righe.append(f"Immagini generate con Meshy ({', '.join(m for m in generate if m)}): "
                     "nessuna è una fotografia, nessuna ritrae persone o luoghi reali.")
    return "\n".join(righe) + "\n"


def scrivi(p: Piano) -> Path:
    dest = cartella(p.slug) / "CREDITI.md"
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".md.tmp")
    tmp.write_text(testo(p), encoding="utf-8")
    tmp.replace(dest)
    return dest
