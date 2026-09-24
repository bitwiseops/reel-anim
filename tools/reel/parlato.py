"""Il testo recitato contro la VOCE della sceneggiatura: `uv run reel parlato <file> [--applica]`.

La VOCE la rivede il presentatore mentre registra: nella finestra di `reel registra` corregge le righe
(contenuti/media/<slug>/parlato.json) e la presa scrive nel sidecar `scena-NN.json` il testo che ha recitato. Le
caption si fanno già da lì (`monta.voce_recitata`); questo comando mostra cosa è cambiato e, con `--applica`, lo
riporta nelle righe `VOCE:` del .md, così la sceneggiatura resta uguale al parlato vero (pacchetto social).
Le revisioni del presentatore hanno l'ultima parola: le righe si copiano così come sono.
"""
from __future__ import annotations

from pathlib import Path

from . import clip as clipmod
from .model import Reel
from .parser import RE_CAMPO, RE_H2, RE_H2_SCENA, _frontmatter, _senza_commenti


def recitato(r: Reel) -> dict[int, list[str]]:
    """Per scena, le righe recitate che differiscono dalla VOCE: la `voce` del sidecar della presa, altrimenti la
    correzione in parlato.json. Solo con lo stesso numero di righe (i beat sono legati alle frasi)."""
    parlato = clipmod.carica_parlato(r.slug)
    out = {}
    for s in r.scene:
        v = clipmod.voce_presa(clipmod.trova(r.slug, s.n))
        if v is None or len(v) != len(s.voce):
            v = parlato.get(s.n)
        if v is not None and len(v) == len(s.voce) and v != list(s.voce):
            out[s.n] = v
    return out


def confronto(r: Reel, cambi: dict[int, list[str]]) -> str:
    righe = []
    for s in r.scene:
        if s.n not in cambi:
            continue
        righe.append(f"## Scena {s.n}")
        for vecchia, nuova in zip(s.voce, cambi[s.n]):
            if vecchia == nuova:
                righe.append(f"  = {vecchia}")
            else:
                righe += [f"  - {vecchia}", f"  + {nuova}"]
    return "\n".join(righe)


def applica(path: Path, cambi: dict[int, list[str]]) -> int:
    """Riscrive nel .md le righe `VOCE:` delle scene cambiate (la k-esima VOCE della scena con la k-esima riga
    recitata). Restituisce quante righe ha cambiato."""
    testo = path.read_text(encoding="utf-8")
    righe = testo.split("\n")
    pulite = _senza_commenti(testo).split("\n")     # stessa numerazione: le righe dentro un commento non si toccano
    _, inizio, _ = _frontmatter(testo)
    scena, k, cambiate = None, 0, 0
    for i in range(inizio, len(righe)):
        riga = pulite[i].rstrip()
        m = RE_H2_SCENA.match(riga)
        if m:
            scena, k = int(m.group(1)), 0
            continue
        if RE_H2.match(riga):
            scena = None
            continue
        m = RE_CAMPO.match(riga)
        if scena is None or not m or m.group(1).upper() != "VOCE" or not m.group(2).strip():
            continue
        if scena in cambi and k < len(cambi[scena]):
            nuova = f"VOCE: {cambi[scena][k]}"
            if righe[i].rstrip() != nuova:
                righe[i] = nuova
                cambiate += 1
        k += 1
    if cambiate:
        path.write_text("\n".join(righe), encoding="utf-8")
    return cambiate
