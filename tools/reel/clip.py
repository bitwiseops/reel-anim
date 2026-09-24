"""Clip del presentatore: una per scena in contenuti/media/<slug>/scena-NN.(mov|mp4|webm|m4v).
Accanto a una clip tagliata da `reel registra` c'è scena-NN.json con gli inizi delle frasi seguiti nella presa."""
from __future__ import annotations

import json
from pathlib import Path

from .ffmpeg import ffprobe

from ..anim.config import RADICE
ESTENSIONI = (".mov", ".mp4", ".webm", ".m4v")
SILENZIO_S = 0.5   # silenzio che il gobbo chiede prima e dopo la voce: gli inizi delle frasi si stimano tra questi margini


def cartella(slug: str) -> Path:
    return RADICE / "contenuti" / "media" / slug


def nome_atteso(n: int) -> str:
    return f"scena-{n:02d}.mov"


def trova(slug: str, n: int) -> Path | None:
    base = cartella(slug)
    for est in ESTENSIONI:
        p = base / f"scena-{n:02d}{est}"
        if p.exists():
            return p
    return None


def sidecar(clip: Path) -> Path:
    return clip.with_suffix(".json")


def tempi_presa(clip: Path) -> list[float] | None:
    """Gli inizi delle frasi salvati da `reel registra` accanto alla clip (relativi all'inizio della clip), se ci sono."""
    p = sidecar(clip)
    if not p.exists():
        return None
    try:
        inizi = json.loads(p.read_text(encoding="utf-8")).get("inizi_frasi_s")
    except (json.JSONDecodeError, AttributeError):
        return None
    return [float(x) for x in inizi] if isinstance(inizi, list) else None


def voce_presa(clip: Path | None) -> list[str] | None:
    """Il testo mostrato nel karaoke durante la presa (righe grezze, con ==evidenzia==), se il sidecar lo ha: è quello
    che il presentatore ha recitato, e le caption si fanno da qui. None per le prese più vecchie, che non lo salvavano."""
    if clip is None or not sidecar(clip).exists():
        return None
    try:
        voce = json.loads(sidecar(clip).read_text(encoding="utf-8")).get("voce")
    except (json.JSONDecodeError, AttributeError):
        return None
    return [str(x) for x in voce] if isinstance(voce, list) else None


# --- il testo corretto in registrazione -------------------------------------------------------------------------
# contenuti/media/<slug>/parlato.json = {"3": ["riga", ...]}: solo le scene che il presentatore ha cambiato nella
# finestra di `reel registra`, righe grezze, tante quante le VOCE della scena (i beat sono legati alle frasi).

def file_parlato(slug: str) -> Path:
    return cartella(slug) / "parlato.json"


def carica_parlato(slug: str) -> dict[int, list[str]]:
    try:
        dati = json.loads(file_parlato(slug).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {int(k): [str(x) for x in v] for k, v in dati.items() if isinstance(v, list)}


def salva_parlato(slug: str, n: int, righe: list[str] | None) -> Path:
    """Scrive le righe della scena n (None = torna alla VOCE della sceneggiatura)."""
    dati = carica_parlato(slug)
    if righe is None:
        dati.pop(n, None)
    else:
        dati[n] = list(righe)
    p = file_parlato(slug)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({str(k): v for k, v in sorted(dati.items())}, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def stato(slug: str, scene_n: list[int]) -> list[dict]:
    """Per ogni scena: file trovato, durata, probe e da dove vengono i tempi delle frasi (presa | stimati)."""
    out = []
    for n in scene_n:
        p = trova(slug, n)
        info = {"scena": n, "atteso": nome_atteso(n), "file": str(p.relative_to(RADICE)) if p else None, "presente": p is not None}
        if p:
            pr = ffprobe(p)
            info["durata_s"] = pr.get("durata_s")
            info["ffprobe"] = pr
            info["tempi"] = "presa" if tempi_presa(p) is not None else "stimati"
        out.append(info)
    return out
