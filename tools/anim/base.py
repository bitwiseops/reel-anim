"""Classe base delle scene del reel: durata nota (dalla clip del presentatore) e beat sincronizzati alla voce."""
from __future__ import annotations

import math
from dataclasses import dataclass

from manim import DOWN, LEFT, RIGHT, UP, Rectangle, Scene, VGroup
from manim import config as config_manim

from .config import Config, carica, registra_font
from .misure import px

ANTICIPO_S = 0.1   # il beat parte 3 fotogrammi prima della frase: l'occhio deve arrivare con la voce, non dopo
CODA_S = 0.5       # respiro dopo l'ultima frase quando i tempi delle frasi si stimano


def inizi_per_parole(frasi: list[str], da_s: float, a_s: float) -> list[float]:
    """Inizio stimato di ogni frase: l'intervallo [da_s, a_s] diviso in proporzione alle parole delle frasi.
    È il ripiego quando i tempi veri non ci sono (clip registrate senza allineamento, render diretti)."""
    if not frasi:
        return []
    pesi = [max(1, len(f.split())) for f in frasi]
    totale = sum(pesi)
    ampiezza = max(0.0, a_s - da_s)
    inizi, cumulate = [], 0
    for p in pesi:
        inizi.append(round(da_s + ampiezza * cumulate / totale, 3))
        cumulate += p
    return inizi


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

    def metti(self, mob, v: str = "alto", h: str = "sinistra", buff_px: float = 0):
        """Allinea mob dentro l'area: v = alto | centro | basso, h = sinistra | centro | destra (buff_px dal bordo)."""
        b = px(buff_px)
        x = {"sinistra": self.x0 + b + mob.width / 2, "centro": (self.x0 + self.x1) / 2,
             "destra": self.x1 - b - mob.width / 2}[h]
        y = {"alto": self.y1 - b - mob.height / 2, "centro": (self.y0 + self.y1) / 2,
             "basso": self.y0 + b + mob.height / 2}[v]
        return mob.move_to([x, y, 0])


@dataclass(frozen=True)
class Aree:
    contenuto: Area   # dove stanno testi e grafica
    riquadro: Area | None   # dove va il riquadro del presentatore (da lasciare libero)
    schermo: Area     # cornice del b-roll


def _da_px(cfg: Config, x_px: float, y_px: float) -> tuple[float, float]:
    """Da coordinate pixel (origine in alto a sinistra) a unità Manim (origine al centro, y in alto)."""
    return px(x_px) - cfg.frame_width / 2, cfg.frame_height / 2 - px(y_px)


def area_px(cfg: Config, x0: float, y0: float, x1: float, y1: float) -> Area:
    """Un Area da un rettangolo in px della tela (origine in alto a sinistra), es. un punto di un'immagine di b-roll."""
    ax0, ay1 = _da_px(cfg, x0, y0)
    ax1, ay0 = _da_px(cfg, x1, y1)
    return Area(ax0, ay0, ax1, ay1)


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
    `beat(i)` aspetta l'inizio della frase i della VOCE: `scena["inizi_frasi_s"]` (esatti con la voce sintetica di
    prova) oppure una stima proporzionale alle parole. Se una scena arriva tardi a un beat o sfora la durata, il
    problema finisce in `self.avvisi` (e nel report). `chiudi()` tiene l'ultimo fotogramma fino a `durata_s` ed è
    automatico.
    """

    def __init__(self, durata_s: float = 6.0, scena: dict | None = None, debug: bool = False, **kw):
        self.durata_s = float(durata_s)
        self.scena = scena or {}
        self.debug = debug
        self.cfg: Config = carica()
        registra_font(self.cfg)
        self.area: Aree = aree(self.cfg, self.scena.get("riquadro"))
        self.avvisi: list[str] = []
        voce = list(self.scena.get("voce") or [])
        inizi = self.scena.get("inizi_frasi_s")
        if inizi and len(inizi) == len(voce):
            self.inizi_frasi = [float(x) for x in inizi]
        else:
            self.inizi_frasi = inizi_per_parole(voce, 0.0, self.durata_s - CODA_S)
        super().__init__(**kw)

    # --- tempo ---------------------------------------------------------------------------------------
    @property
    def t(self) -> float:
        return float(self.renderer.time)

    def attendi_fino(self, secondi: float) -> None:
        resto = secondi - self.t
        if resto >= 1.0 / config_manim.frame_rate:   # sotto un fotogramma non si può aspettare
            self.wait(resto)

    def fino_a(self, frazione: float) -> None:
        self.attendi_fino(self.durata_s * max(0.0, min(1.0, frazione)))

    ANTICIPO_S = ANTICIPO_S

    @property
    def _fotogramma(self) -> float:
        return 1.0 / config_manim.frame_rate

    def beat(self, i: int) -> None:
        """Aspetta l'inizio della frase i (0-based) della VOCE, meno ANTICIPO_S. Se la scena è già oltre (le animazioni
        del beat precedente durano troppo) non può tornare indietro: lo annota in self.avvisi."""
        n = len(self.inizi_frasi)
        if n == 0:
            if i == 0:
                return
            raise ValueError(f"beat({i}): la scena non ha VOCE, usa fino_a(frazione)")
        if not 0 <= i < n:
            raise IndexError(f"beat({i}): la VOCE ha {n} frasi, i beat vanno da 0 a {n - 1}")
        obiettivo = max(0.0, self.inizi_frasi[i] - self.ANTICIPO_S)
        ritardo = self.t - obiettivo
        if ritardo > self._fotogramma + 1e-6:
            self.avvisi.append(f"beat({i}) parte {ritardo:.2f} s dopo l'inizio della frase {i + 1}: "
                               f"accorcia le animazioni del beat {i - 1}")
        self.attendi_fino(obiettivo)

    def arrotonda(self, secondi: float) -> float:
        """run_time arrotondato per difetto a fotogrammi interi (almeno uno). Manim allunga ogni play fino al
        fotogramma successivo: tante play corte in fila accumulano ritardo e il beat dopo parte tardi."""
        f = self._fotogramma
        return max(f, math.floor(secondi / f + 1e-9) * f)

    def durata_beat(self, i: int) -> float:
        """Secondi dall'inizio della frase i all'inizio della successiva (o alla fine della scena): il tempo del beat."""
        if not self.inizi_frasi:
            return self.durata_s
        fine = self.inizi_frasi[i + 1] if i + 1 < len(self.inizi_frasi) else self.durata_s
        return max(0.0, fine - self.inizi_frasi[i])

    def chiudi(self) -> None:
        if self.t > self.durata_s + self._fotogramma + 1e-6:
            self.avvisi.append(f"la scena dura {self.t:.2f} s ma la clip {self.durata_s:.2f} s: il finale viene tagliato")
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


__all__ = ["Area", "Aree", "ScenaReel", "aree", "area_px", "inizi_per_parole", "ANTICIPO_S", "CODA_S", "DOWN", "UP", "LEFT", "RIGHT"]
