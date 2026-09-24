"""Render programmatico di una scena Manim da contenuti/animazioni/<slug>.py."""
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import re
import sys
from pathlib import Path
from types import ModuleType
from typing import NamedTuple

from manim import tempconfig

from ..anim.base import ScenaReel
from ..anim.config import Config, carica, opzioni_manim

from ..anim.config import RADICE


class AnimazioneMancante(RuntimeError):
    pass


class Render(NamedTuple):
    video: Path
    avvisi: list[str]      # ScenaReel.avvisi: beat in ritardo, scena che sfora
    controlli: list[str]   # ScenaReel.controlli: testo piccolo/fuori/coperto/sovrapposto, riquadro, colori


_LINT = [
    (re.compile(r"\b(MathTex|Tex|SingleStringMathTex|BraceLabel|BarChart|IntegerTable|DecimalTable|MathTable|Variable)\s*\("),
     "usa LaTeX (vietato): vedi docs/animazioni.md §10"),
    (re.compile(r"\b(DecimalNumber|Integer)\s*\((?![^)]*mob_class)"), "DecimalNumber/Integer usano LaTeX senza mob_class=Text"),
    (re.compile(r"\.get_(tex|text)\s*\("), "Brace.get_text/get_tex usano LaTeX: brace.put_at_tip(testo(...))"),
    (re.compile(r"\.to_(edge|corner)\s*\("), "to_edge/to_corner misurano dal bordo della tela: usa area.metti(...)"),
    (re.compile(r"stroke_width\s*=\s*px\("), "spessore con px(): usa tratto(px)"),
    (re.compile(r"(?<![\w&])#[0-9A-Fa-f]{6}\b"), "colore scritto a mano: usa self.cfg.palette"),
    (re.compile(r"gradient", re.I), "gradienti vietati"),
    (re.compile(r"\bThreeDScene\b"), "niente 3D"),
]


def lint_animazione(path: Path) -> list[tuple[int, str]]:
    """Controllo statico del file delle animazioni: (riga, problema) per i costrutti vietati dalle regole del repo."""
    out = []
    for n, riga in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if riga.lstrip().startswith("#"):
            continue
        codice = re.sub(r"\s#\s.*$", "", riga)
        for rx, msg in _LINT:
            if rx.search(codice):
                out.append((n, msg))
    return out


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
        return Render(Path(s.renderer.file_writer.movie_file_path), list(s.avvisi), [str(v) for v in s.controlli])
