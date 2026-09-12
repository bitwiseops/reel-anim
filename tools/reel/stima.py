"""Stima della durata di una scena dalla VOCE, quando non c'è ancora la clip del presentatore. Fonte unica."""
from __future__ import annotations

from ..anim.config import Config, carica
from .model import Scena

MINIMO_S = 2.5
CODA_S = 0.8            # respiro dopo l'ultima frase
HOOK_SENZA_VOCE_S = 3.5


def parole_al_secondo(cfg: Config | None = None) -> float:
    cfg = cfg or carica()
    return float(cfg.dati["voce_sintetica"].get("parole_al_secondo", 2.8))


def durata_stimata_s(scena: Scena, cfg: Config | None = None) -> float:
    if scena.durata_min_s is not None and not scena.voce:
        return max(MINIMO_S, scena.durata_min_s)
    if not scena.voce:
        base = HOOK_SENZA_VOCE_S if scena.tipo == "hook" else MINIMO_S
    else:
        base = scena.parole_voce / parole_al_secondo(cfg) + CODA_S
    d = max(MINIMO_S, base)
    if scena.durata_min_s is not None:
        d = max(d, scena.durata_min_s)
    return round(d, 2)
