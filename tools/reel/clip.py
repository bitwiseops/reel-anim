"""Clip del presentatore: una per scena in contenuti/media/<slug>/scena-NN.(mov|mp4|webm|m4v)."""
from __future__ import annotations

from pathlib import Path

from .ffmpeg import ffprobe

RADICE = Path(__file__).resolve().parents[2]
ESTENSIONI = (".mov", ".mp4", ".webm", ".m4v")


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


def stato(slug: str, scene_n: list[int]) -> list[dict]:
    """Per ogni scena: file trovato, durata e probe."""
    out = []
    for n in scene_n:
        p = trova(slug, n)
        info = {"scena": n, "atteso": nome_atteso(n), "file": str(p.relative_to(RADICE)) if p else None, "presente": p is not None}
        if p:
            pr = ffprobe(p)
            info["durata_s"] = pr.get("durata_s")
            info["ffprobe"] = pr
        out.append(info)
    return out
