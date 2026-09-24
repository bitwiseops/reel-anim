"""Dove vanno i file di un reel: il riepilogo nel progetto, il lavoro transitorio fuori (dal 2026-09-23).

`contenuti/render/<slug>/` tiene solo quello che il presentatore guarda e che i comandi rileggono: `reel-9x16.mp4`,
`reel-prova.mp4`, `contact-sheet.png`, le copertine, `scene/NN.png`, i filmstrip di scena e `report.json`. Tutto il
resto — la cache e i video di Manim, le scene montate una per una, la voce di prova, le caption, le strisce fitte, i
provini dei filmati — si rigenera e va in `config.toml [percorsi] lavoro` (`~/Library/Caches/reel-anim/<slug>/`), che
`uv run reel pulisci` svuota. La cache dei filmati scaricati e delle immagini generate va invece in
`[percorsi] cache_broll`, che nessuno ripulisce da sé: dentro ci sono immagini Meshy pagate.
"""
from __future__ import annotations

from pathlib import Path

from ..anim.config import RADICE, Config, carica

LAVORO = "~/Library/Caches/reel-anim"
CACHE_BROLL = "~/Library/Application Support/reel-anim/cache-broll"


def riepilogo(slug: str, out: str | Path | None = None) -> Path:
    """La cartella del riepilogo di un reel (o quella data con `--out`)."""
    return Path(out) if out else RADICE / "contenuti" / "render" / slug


def radice_lavoro(cfg: Config | None = None) -> Path:
    cfg = cfg or carica()
    return cfg.percorso("percorsi", "lavoro") or Path(LAVORO).expanduser()


def lavoro(slug: str, cfg: Config | None = None) -> Path:
    """La cartella transitoria di un reel."""
    return radice_lavoro(cfg) / slug


def lavoro_per(slug: str, out: Path | None = None, cfg: Config | None = None) -> Path:
    """Con un `--out` esplicito (i test, le prove a mano) tutto resta insieme lì; altrimenti la cartella di lavoro."""
    if out is not None and Path(out).resolve() != riepilogo(slug).resolve():
        return Path(out)
    return lavoro(slug, cfg)


def cache_broll(cfg: Config | None = None) -> Path:
    cfg = cfg or carica()
    return cfg.percorso("percorsi", "cache_broll") or Path(CACHE_BROLL).expanduser()


def relativo(p: Path, base: Path = RADICE) -> str:
    """Relativo a `base` (la radice del repo) se ci sta dentro, altrimenti assoluto: `base / assoluto` resta lui."""
    try:
        return str(p.relative_to(base))
    except ValueError:
        return str(p)
