"""Classe base delle scene del reel: durata nota (dalla clip del presentatore) e beat sincronizzati alla voce."""
from __future__ import annotations

from dataclasses import dataclass

from manim import DOWN, LEFT, RIGHT, UP, Rectangle, Scene, VGroup

from .config import Config, carica, registra_font
from .misure import px


@dataclass(frozen=True)
class Area:
    """Un rettangolo in unità Manim (origine al centro della tela, y verso l'alto), come in Manim."""
    x0: float
    y0: float
    x1: float
    y1: float

    @property
    def larghezza(self) -> float:
        return self.x1 - self.x0

    @property
    def altezza(self) -> float:
        return self.y1 - self.y0

    @property
    def centro(self):
        import numpy as np
        return np.array([(self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2, 0.0])

    def rettangolo(self, **kw) -> Rectangle:
        return Rectangle(width=self.larghezza, height=self.altezza, **kw).move_to(self.centro)


@dataclass(frozen=True)
class Aree:
    contenuto: Area   # dove stanno testi e grafica
    riquadro: Area | None   # dove va il riquadro del presentatore (da lasciare libero)
    schermo: Area     # cornice del b-roll


def _da_px(cfg: Config, x_px: float, y_px: float) -> tuple[float, float]:
    """Da coordinate pixel (origine in alto a sinistra) a unità Manim (origine al centro, y in alto)."""
    return px(x_px) - cfg.frame_width / 2, cfg.frame_height / 2 - px(y_px)


def aree(cfg: Config, riquadro: str | None = None) -> Aree:
    """Aree utili in base alla safe area e alla posizione del riquadro (None/"no" = nessun riquadro)."""
    s = cfg.dati["safe_area"]
    W, H = cfg.larghezza, cfg.altezza
    x0, y1 = _da_px(cfg, s.get("sinistra", 60), s["alto"])
    x1, y0 = _da_px(cfg, W - s["destra"], H - s["basso"])
    contenuto = Area(x0, y0, x1, y1)
    r = cfg.dati["riquadro"]
    area_riq = None
    if riquadro and riquadro != "no":
        pos = riquadro if riquadro != "si" else r["posizione"]
        d, m = r["dimensione_px"], r["margine_px"]
        rx = W - s["destra"] - m - d if "destra" in pos else s.get("sinistra", 60) + m
        ry = H - s["basso"] - d if "basso" in pos else s["alto"]
        ax0, ay1 = _da_px(cfg, rx, ry)
        ax1, ay0 = _da_px(cfg, rx + d, ry + d)
        area_riq = Area(ax0, ay0, ax1, ay1)
        # il contenuto lascia libera la fascia del riquadro
        if "basso" in pos:
            contenuto = Area(contenuto.x0, ay1 + px(m), contenuto.x1, contenuto.y1)
        else:
            contenuto = Area(contenuto.x0, contenuto.y0, contenuto.x1, ay0 - px(m))
    sc = cfg.dati["schermo"]
    sx0, sy1 = _da_px(cfg, sc["x"], sc["y"])
    sx1, sy0 = _da_px(cfg, sc["x"] + sc["larghezza"], sc["y"] + sc["altezza"])
    return Aree(contenuto, area_riq, Area(sx0, sy0, sx1, sy1))


class ScenaReel(Scene):
    """Una scena del reel. `durata_s` è la durata della clip del presentatore: la scena dura esattamente tanto.

    Sottoclassi: implementa `costruisci()` usando `self.area`, `self.cfg`, `self.beat(i)` / `self.fino_a(f)`.
    `chiudi()` tiene l'ultimo fotogramma fino a `durata_s` ed è automatico.
    """

    def __init__(self, durata_s: float = 6.0, scena: dict | None = None, debug: bool = False, **kw):
        self.durata_s = float(durata_s)
        self.scena = scena or {}
        self.debug = debug
        self.cfg: Config = carica()
        registra_font(self.cfg)
        self.area: Aree = aree(self.cfg, self.scena.get("riquadro"))
        super().__init__(**kw)

    # --- tempo ---------------------------------------------------------------------------------------
    @property
    def t(self) -> float:
        return float(self.renderer.time)

    def attendi_fino(self, secondi: float) -> None:
        resto = secondi - self.t
        if resto > 1.0 / self.cfg.fps:
            self.wait(resto)

    def fino_a(self, frazione: float) -> None:
        self.attendi_fino(self.durata_s * max(0.0, min(1.0, frazione)))

    def beat(self, i: int) -> None:
        """Aspetta l'inizio della frase i (0-based) della VOCE: le frasi si spartiscono la clip in parti uguali."""
        n = max(1, len(self.scena.get("voce") or [1]))
        self.fino_a(i / n)

    def chiudi(self) -> None:
        self.attendi_fino(self.durata_s)

    # --- costruzione ---------------------------------------------------------------------------------
    def construct(self) -> None:
        if self.debug:
            self.add(self.guide())
        self.costruisci()
        self.chiudi()

    def costruisci(self) -> None:
        raise NotImplementedError("implementa costruisci() nella scena")

    def guide(self) -> VGroup:
        """Contorni di safe area, area contenuto, riquadro e schermo (solo con debug=True)."""
        g = VGroup()
        col = self.cfg.palette
        g.add(self.area.contenuto.rettangolo(stroke_color=col.terziario, stroke_width=2))
        g.add(self.area.schermo.rettangolo(stroke_color=col.secondario, stroke_width=2))
        if self.area.riquadro:
            g.add(self.area.riquadro.rettangolo(stroke_color=col.accento, stroke_width=2))
        return g


__all__ = ["Area", "Aree", "ScenaReel", "aree", "DOWN", "UP", "LEFT", "RIGHT"]
