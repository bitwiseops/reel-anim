"""Misure in pixel ↔ unità Manim e minimi di leggibilità sul telefono (1080 px di larghezza visti a ~400 px)."""
from __future__ import annotations

from .config import carica

PX_PER_UNITA = 120.0   # con frame_width = 9 su 1080 px


def px(n: float) -> float:
    """Da pixel a unità Manim."""
    return n / PX_PER_UNITA


def unita(u: float) -> float:
    """Da unità Manim a pixel."""
    return u * PX_PER_UNITA


# Altezza delle MAIUSCOLE in px (misurata con calibra.py) per ogni ruolo tipografico. Nulla sotto MINIMO_PX.
CORPO_PX = {"titolo": 104, "messaggio": 84, "punto": 92, "caption": 48, "etichetta": 40, "token": 44, "voce": 40, "piede": 28}
MINIMO_PX = 36

# Fattore font_size (Manim/Pango) → altezza in px del testo "Hg" a piena risoluzione; lo scrive calibra.py.
FATTORE_FONT_SIZE = 1.5723   # misurato con calibra.py: "Hg" in Inter Variable, font_size 48 → 75.5 px


def font_size_per(px_altezza: float) -> float:
    """font_size di Manim che produce un testo alto circa `px_altezza` pixel (righe di "Hg")."""
    return px_altezza / FATTORE_FONT_SIZE


def safe_area_px() -> dict[str, int]:
    s = carica().dati["safe_area"]
    return {"alto": int(s["alto"]), "destra": int(s["destra"]), "basso": int(s["basso"]), "sinistra": int(s.get("sinistra", 60))}
