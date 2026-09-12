"""Calibrazione una tantum: quanti pixel è alto un testo Manim per unità di font_size, con il font del config.

Uso: uv run python -m tools.anim.calibra   → stampa il fattore e verifica che il font in grassetto sia quello giusto.
Il valore va copiato in misure.FATTORE_FONT_SIZE.
"""
from __future__ import annotations

import sys

from manim import BOLD, Text, tempconfig

from .config import carica, opzioni_manim, registra_font


def misura(font: str, peso: str = "NORMAL", font_size: float = 48) -> float:
    """Altezza in px (a piena risoluzione) del testo "Hg" con quel font e peso."""
    cfg = carica()
    with tempconfig(opzioni_manim(cfg, "h")):
        t = Text("Hg", font=font, weight=peso, font_size=font_size)
        return t.height * cfg.px_per_unita


def main() -> int:
    cfg = carica()
    registrati = registra_font(cfg)
    print(f"font registrati: {', '.join(f.name for f in registrati) or 'nessuno'}")
    import manimpango
    fam = cfg.font.famiglia
    presenti = [f for f in manimpango.list_fonts() if fam.lower() in f.lower()]
    print(f"famiglie Pango con '{fam}': {presenti or 'NESSUNA (Pango userà un fallback)'}")
    h48 = misura(fam, "NORMAL", 48)
    hb = misura(fam, BOLD, 48)
    print(f"'Hg' a font_size 48: normale {h48:.1f} px, bold {hb:.1f} px → FATTORE_FONT_SIZE = {h48/48:.4f}")
    if abs(h48 - hb) > 6:
        print("attenzione: normale e bold differiscono molto in altezza: il bold potrebbe essere un fallback")
    return 0


if __name__ == "__main__":
    sys.exit(main())
