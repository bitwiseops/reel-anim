"""Render programmatico di una scena Manim da contenuti/animazioni/<slug>.py."""
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import sys
from pathlib import Path
from types import ModuleType
from typing import NamedTuple

from manim import tempconfig

from ..anim.base import ScenaReel
from ..anim.config import Config, carica, opzioni_manim

RADICE = Path(__file__).resolve().parents[2]


class AnimazioneMancante(RuntimeError):
    pass


class Render(NamedTuple):
    video: Path
    avvisi: list[str]   # ScenaReel.avvisi: beat in ritardo, scena che sfora


def file_animazione(slug: str) -> Path:
    return RADICE / "contenuti" / "animazioni" / f"{slug}.py"


def carica_modulo(path: Path) -> ModuleType:
    if not path.exists():
        raise AnimazioneMancante(f"manca il file delle animazioni {path.relative_to(RADICE)} (lo scrive l'animatore)")
    nome = f"animazioni_{path.stem.replace('-', '_')}"
    spec = importlib.util.spec_from_file_location(nome, path)
    mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
    sys.modules[nome] = mod
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


def classe_scena(mod: ModuleType, n: int) -> type[ScenaReel]:
    nome = f"Scena{n:02d}"
    cls = getattr(mod, nome, None)
    if cls is None or not (inspect.isclass(cls) and issubclass(cls, ScenaReel)):
        presenti = [k for k, v in vars(mod).items() if inspect.isclass(v) and issubclass(v, ScenaReel) and v is not ScenaReel]
        raise AnimazioneMancante(f"manca la classe {nome}(ScenaReel) in {mod.__file__} (presenti: {', '.join(presenti) or 'nessuna'})")
    return cls


def hash_classe(cls: type) -> str:
    try:
        src = inspect.getsource(cls)
    except OSError:
        src = cls.__name__
    return hashlib.sha256(src.encode("utf-8")).hexdigest()[:16]


def hash_sorgenti(animazione: Path) -> str:
    """Hash di tutto ciò da cui dipende il render Manim: file delle animazioni, libreria tools/anim, config."""
    h = hashlib.sha256()
    for p in [animazione, *sorted((RADICE / "tools" / "anim").glob("*.py")), RADICE / "config.toml", RADICE / "config.local.toml"]:
        if p.exists():
            h.update(p.name.encode() + p.read_bytes())
    return h.hexdigest()[:16]


def renderizza(cls: type[ScenaReel], durata_s: float, scena: dict, out_dir: Path, nome: str, qualita: str = "h",
               trasparente: bool = False, debug: bool = False, cfg: Config | None = None) -> Render:
    """Renderizza la scena (Manim la scrive in out_dir/videos/<risoluzione>/<nome>.(mp4|mov)); ritorna file e avvisi."""
    cfg = cfg or carica()
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempconfig(opzioni_manim(cfg, qualita, trasparente=trasparente, media_dir=out_dir, output_file=nome)):
        s = cls(durata_s=durata_s, scena=scena, debug=debug)
        s.render()
        return Render(Path(s.renderer.file_writer.movie_file_path), list(s.avvisi))
