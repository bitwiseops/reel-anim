"""Configurazione del repo (config.toml + config.local.toml) e sua applicazione a Manim.

Tutto ciò che è identità (palette, font, handle, riquadro) vive nei TOML: il codice non conosce nessun brand.
"""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any

RADICE = Path(__file__).resolve().parents[2]
CONFIG = RADICE / "config.toml"
CONFIG_LOCALE = RADICE / "config.local.toml"


def _fondi(base: dict, sopra: dict) -> dict:
    out = dict(base)
    for k, v in sopra.items():
        out[k] = _fondi(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


@dataclass(frozen=True)
class Config:
    dati: dict[str, Any] = field(default_factory=dict)

    def __getattr__(self, sezione: str) -> Any:
        try:
            return _Sezione(self.dati[sezione])
        except KeyError as e:
            raise AttributeError(f"sezione '{sezione}' assente in config.toml") from e

    # --- misure derivate -------------------------------------------------------------------------
    @property
    def larghezza(self) -> int:
        return int(self.dati["video"]["larghezza"])

    @property
    def altezza(self) -> int:
        return int(self.dati["video"]["altezza"])

    @property
    def fps(self) -> int:
        return int(self.dati["video"]["fps"])

    @property
    def frame_width(self) -> float:
        """Larghezza della scena in unità Manim: 9 unità per 1080 px → 1 unità = 120 px (vedi misure.px)."""
        return 9.0

    @property
    def frame_height(self) -> float:
        return self.frame_width * self.altezza / self.larghezza

    @property
    def px_per_unita(self) -> float:
        return self.larghezza / self.frame_width

    def font_file(self) -> list[Path]:
        return [RADICE / f for f in self.dati["font"]["file"]]

    def percorso(self, sezione: str, chiave: str) -> Path | None:
        """Un percorso del config: `~` espanso, relativo alla radice del repo se non è assoluto; None se vuoto o assente."""
        v = self.dati.get(sezione, {}).get(chiave)
        if not v:
            return None
        p = Path(str(v)).expanduser()
        return p if p.is_absolute() else RADICE / p


class _Sezione:
    def __init__(self, d: dict):
        self._d = d

    def __getattr__(self, k: str) -> Any:
        try:
            return self._d[k]
        except KeyError as e:
            raise AttributeError(k) from e

    def get(self, k: str, default: Any = None) -> Any:
        return self._d.get(k, default)

    def __repr__(self) -> str:
        return repr(self._d)


@lru_cache(maxsize=4)
def carica(percorso: Path = CONFIG, locale: Path = CONFIG_LOCALE) -> Config:
    dati = tomllib.loads(percorso.read_text(encoding="utf-8"))
    if locale.exists():
        dati = _fondi(dati, tomllib.loads(locale.read_text(encoding="utf-8")))
    return Config(dati)


_FONT_REGISTRATI: set[Path] = set()


def registra_font(cfg: Config) -> list[Path]:
    """Registra in Pango i file font del config (idempotente). Ritorna i file registrati con successo."""
    import manimpango
    ok = []
    for f in cfg.font_file():
        if f in _FONT_REGISTRATI:
            ok.append(f)
            continue
        if f.exists() and manimpango.register_font(str(f)):
            _FONT_REGISTRATI.add(f)
            ok.append(f)
    return ok


QUALITA = {"l": "low_quality", "m": "medium_quality", "h": "high_quality"}


def opzioni_manim(cfg: Config, qualita: str = "h", trasparente: bool = False, media_dir: Path | None = None,
                  output_file: str | None = None) -> dict:
    """Dizionario per `manim.tempconfig`: tela verticale, sfondo dal config, niente cache (determinismo semplice).
    qualita: l (fotogrammi ridotti, per guardare in fretta) | m | h (piena risoluzione)."""
    scala = {"l": 0.5, "m": 0.75, "h": 1.0}[qualita]
    fps = {"l": 15, "m": cfg.fps, "h": cfg.fps}[qualita]
    d = {
        "pixel_width": int(cfg.larghezza * scala), "pixel_height": int(cfg.altezza * scala),
        "frame_width": cfg.frame_width, "frame_height": cfg.frame_height, "frame_rate": fps,
        "background_color": cfg.palette.sfondo, "disable_caching": True, "write_to_movie": True,
        "verbosity": "WARNING", "progress_bar": "none", "preview": False, "format": "mov" if trasparente else "mp4",
        "transparent": trasparente, "movie_file_extension": ".mov" if trasparente else ".mp4",
    }
    if media_dir is not None:
        d["media_dir"] = str(media_dir)
    if output_file:
        d["output_file"] = output_file
    return d
