"""Fotogrammi chiave, filmstrip e cover: ciò che Claude Code (che non vede il video) guarda al posto del video."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

from ..anim.config import Config, carica
from .ffmpeg import estrai_fotogramma, filmstrip, tempi_campione


def ritaglio_4x5(cfg: Config) -> tuple[int, int, int, int]:
    """Banda centrale 4:5 della tela 9:16 (1080x1350 su 1080x1920)."""
    h = int(cfg.larghezza * 5 / 4)
    y = (cfg.altezza - h) // 2
    return (0, y, cfg.larghezza, y + h)


def fotogramma_chiave(video: Path, durata_s: float, dest: Path, frazione: float = 0.6) -> Path:
    return estrai_fotogramma(video, durata_s * frazione, dest)


def filmstrip_scena(video: Path, durata_s: float, dest: Path, quanti: int = 6) -> Path:
    return filmstrip(video, tempi_campione(durata_s, quanti), dest, 300)


def cover(video_hook: Path, durata_s: float, out: Path, cfg: Config | None = None, frazione: float = 0.97) -> tuple[Path, Path]:
    """Copertina: l'ultimo fotogramma dell'hook, quando titolo e sottotitolo sono tutti in scena (al 70 % cadeva
    sull'ingresso del sottotitolo)."""
    cfg = cfg or carica()
    intera = estrai_fotogramma(video_hook, durata_s * frazione, out / "copertina.png")
    ritagliata = out / "copertina-4x5.png"
    Image.open(intera).crop(ritaglio_4x5(cfg)).save(ritagliata)
    return intera, ritagliata
