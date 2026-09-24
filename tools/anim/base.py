"""Classe base delle scene del reel: durata nota (dalla clip del presentatore) e beat sincronizzati alla voce."""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from manim import DOWN, LEFT, ORIGIN, RIGHT, UP, MovingCamera, MovingCameraScene, Rectangle, ScreenRectangle, VGroup
from manim import config as config_manim

from .config import Config, carica, registra_font
from .controlli import Violazione, contenuto_visibile, esegui_controlli
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
    caption: Area | None    # fascia dei sottotitoli, bruciati nel montaggio: qui l'animazione non disegna


def _da_px(cfg: Config, x_px: float, y_px: float) -> tuple[float, float]:
    """Da coordinate pixel (origine in alto a sinistra) a unità Manim (origine al centro, y in alto)."""
    return px(x_px) - cfg.frame_width / 2, cfg.frame_height / 2 - px(y_px)


def area_px(cfg: Config, x0: float, y0: float, x1: float, y1: float) -> Area:
    """Un Area da un rettangolo in px della tela (origine in alto a sinistra), es. un punto di un'immagine di b-roll."""
    ax0, ay1 = _da_px(cfg, x0, y0)
    ax1, ay0 = _da_px(cfg, x1, y1)
    return Area(ax0, ay0, ax1, ay1)


def _posizione_caption(c: dict, caption: str | bool | None) -> str | None:
    """Dove sta la fascia in questa scena: "basso" | "alto" | None (nessuna caption, es. chiusura e punch)."""
    if not c:
        return None
    if caption is None or caption is True or caption == "si":
        return str(c.get("posizione", "basso"))
    if caption is False or caption == "no":
        return None
    return str(caption)


def aree(cfg: Config, riquadro: str | None = None, caption: str | bool | None = None) -> Aree:
    """Aree utili in base alla safe area, alla posizione del riquadro (None/"no" = nessun riquadro, "pieno" =
    presentatore a tutta tela dietro la grafica) e alla fascia delle caption (`caption`: None/"si" = dal config,
    "no" = scena senza caption, "alto"/"basso" = deroga di scena)."""
    s = cfg.dati["safe_area"]
    W, H = cfg.larghezza, cfg.altezza
    x0, y1 = _da_px(cfg, s.get("sinistra", 60), s["alto"])
    x1, y0 = _da_px(cfg, W - s["destra"], H - s["basso"])
    contenuto = Area(x0, y0, x1, y1)
    r = cfg.dati["riquadro"]
    area_riq = None
    # "pieno": il presentatore sta *dietro* a tutta tela (apertura e chiusura), quindi non c'è nessuna fascia
    # da lasciargli libera: la grafica è trasparente e gli va sopra. Resta la fascia delle caption.
    if riquadro and riquadro not in ("no", "pieno"):
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
    area_cap = None
    c = cfg.dati.get("caption", {})
    pos_cap = _posizione_caption(c, caption)
    if pos_cap:
        h, m = c.get("altezza_px", 200), c.get("margine_px", 24)
        cy = H - s["basso"] - h if pos_cap == "basso" else s["alto"]
        cx0, cy1 = _da_px(cfg, s.get("sinistra", 60), cy)
        cx1, cy0 = _da_px(cfg, W - s["destra"], cy + h)
        area_cap = Area(cx0, cy0, cx1, cy1)
        # il contenuto lascia libera la fascia: le caption si bruciano sopra, dopo la registrazione
        if pos_cap == "basso":
            contenuto = Area(contenuto.x0, max(contenuto.y0, cy1 + px(m)), contenuto.x1, contenuto.y1)
        else:
            contenuto = Area(contenuto.x0, contenuto.y0, contenuto.x1, min(contenuto.y1, cy0 - px(m)))
    sc = cfg.dati["schermo"]
    sx0, sy1 = _da_px(cfg, sc["x"], sc["y"])
    sx1, sy0 = _da_px(cfg, sc["x"] + sc["larghezza"], sc["y"] + sc["altezza"])
    return Aree(contenuto, area_riq, Area(sx0, sy0, sx1, sy1), area_cap)


class CameraReel(MovingCamera):
    """MovingCamera con la cornice nelle proporzioni della tela del reel (quella predefinita di Manim è 16:9 e
    deformerebbe la tela verticale)."""

    def __init__(self, **kw):
        cfg = carica()
        cornice = ScreenRectangle(aspect_ratio=cfg.frame_width / cfg.frame_height, height=cfg.frame_height)
        cornice.set_stroke(width=0)
        super().__init__(frame=cornice, **kw)


class ScenaReel(MovingCameraScene):
    """Una scena del reel. `durata_s` è la durata della clip del presentatore: la scena dura esattamente tanto.

    Sottoclassi: implementa `costruisci()` usando `self.area`, `self.cfg`, `self.beat(i)` / `self.fino_a(f)`.
    `beat(i)` aspetta l'inizio della frase i della VOCE: `scena["inizi_frasi_s"]` (esatti con la voce sintetica di
    prova) oppure una stima proporzionale alle parole. Se una scena arriva tardi a un beat o sfora la durata, il
    problema finisce in `self.avvisi` (e nel report). `chiudi()` tiene l'ultimo fotogramma fino a `durata_s` ed è
    automatico. Cambi grandi: `self.punch("tu sì")` (parola a tutto schermo) e `self.zoom_su(mob)` / `self.torna()`.
    """

    def __init__(self, durata_s: float = 6.0, scena: dict | None = None, debug: bool = False, **kw):
        self.durata_s = float(durata_s)
        self.scena = scena or {}
        self.debug = debug
        self.cfg: Config = carica()
        registra_font(self.cfg)
        self.area: Aree = aree(self.cfg, self.scena.get("riquadro"), self.scena.get("caption"))
        self.avvisi: list[str] = []
        self.controlli: list[Violazione] = []
        self._visti: set[tuple[str, str]] = set()
        self._escludi: set[int] = set()   # guide di debug: fuori dai controlli
        self._inizio_visto = False
        voce = list(self.scena.get("voce") or [])
        inizi = self.scena.get("inizi_frasi_s")
        if inizi and len(inizi) == len(voce):
            self.inizi_frasi = [float(x) for x in inizi]
        else:
            self.inizi_frasi = inizi_per_parole(voce, 0.0, self.durata_s - CODA_S)
        super().__init__(camera_class=CameraReel, **kw)

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
        if i > 0:
            self.verifica(f"fine beat {i - 1}")
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

    # --- cambi grandi: camera e parola a tutto schermo -------------------------------------------------
    @property
    def zoom(self) -> float:
        """Ingrandimento attuale della camera (1 = tela intera)."""
        return self.cfg.frame_width / self.camera.frame.width

    def inquadratura(self, mob, fattore: float) -> tuple[float, np.ndarray]:
        """Larghezza e centro della camera che ingrandisce mob `fattore` volte e lo porta al centro dell'area contenuto
        (non della tela: con il riquadro in basso il centro della tela sta sopra il presentatore). Per partire già
        ingranditi: `l, c = self.inquadratura(mob, 1.5); self.camera.frame.set(width=l).move_to(c)`."""
        return self.cfg.frame_width / fattore, mob.get_center() - self.area.contenuto.centro / fattore

    def zoom_su(self, mob, fattore: float = 1.5):
        """Animazione da passare a self.play: la camera si avvicina a mob, ingrandita `fattore` volte, e lo porta al
        centro dell'area contenuto, senza disegni nuovi. Il riquadro del presentatore resta fermo sullo schermo: i
        controlli misurano quello che si vede (i testi del tutto fuori campo non contano)."""
        larghezza, centro = self.inquadratura(mob, fattore)
        return self.camera.frame.animate.set(width=larghezza).move_to(centro)

    def torna(self):
        """Animazione da passare a self.play: la camera torna alla tela intera."""
        return self.camera.frame.animate.set(width=self.cfg.frame_width).move_to(ORIGIN)

    def punch(self, s: str, tenuta_s: float = 0.9, colore: str | None = None, entrata_s: float = 0.15) -> None:
        """Il cambio grande della battuta: taglio secco a 1-3 parole a tutto schermo (componenti.Punch), tenute
        `tenuta_s` (ma mai oltre l'inizio del beat dopo: le battute corte durano meno), poi taglio indietro alla scena
        com'era, camera compresa. Ciò che si aggiunge o cambia subito prima compare solo al ritorno, con il taglio."""
        from .componenti import Punch
        cornice = self.camera.frame
        larghezza, centro = cornice.width, cornice.get_center().copy()
        sotto = list(self.mobjects)
        self.remove(*sotto)
        cornice.set(width=self.cfg.frame_width).move_to(ORIGIN)
        p = Punch(s, self.area.contenuto, colore=colore)
        entrata = self.arrotonda(entrata_s)
        # l'inizio del beat in corso non conta: beat(i) può fermarsi fino a un fotogramma prima del suo obiettivo
        # (attendi_fino salta le attese sotto un fotogramma), e quell'inizio non è «il beat dopo»
        soglia = self.t + self._fotogramma + 1e-6
        prossimi = [x - self.ANTICIPO_S for x in self.inizi_frasi if x - self.ANTICIPO_S > soglia]
        if prossimi:
            tenuta_s = max(0.3, min(tenuta_s, prossimi[0] - self.t - entrata))
        self.play(p.entra(), run_time=entrata)
        self.verifica(f"punch «{s}»")
        self.wait(tenuta_s)
        self.remove(p)
        cornice.set(width=larghezza).move_to(centro)
        self.add(*sotto)

    # --- controlli -----------------------------------------------------------------------------------
    def verifica(self, momento: str) -> None:
        """Controlli automatici sullo stato attuale (tools/anim/controlli.py). Li chiamano beat() e chiudi(): a mano
        solo per un istante particolare. Una violazione già vista in un beat precedente non si ripete."""
        for v in esegui_controlli(self, momento, self._escludi):
            chiave = (v.controllo, v.messaggio)
            if chiave not in self._visti:
                self._visti.add(chiave)
                self.controlli.append(v)

    def controlla_primo_fotogramma(self) -> None:
        """Il primo fotogramma dell'hook è quello che vede chi scorre: non può essere vuoto (docs/linguaggio-reel.md
        §1). Lo chiamano da sole la prima play e la prima attesa."""
        if self._inizio_visto:
            return
        self._inizio_visto = True
        if self.scena.get("tipo") == "hook" and not contenuto_visibile(self, self._escludi):
            self.controlli.append(Violazione("fotogramma-vuoto", "inizio", "il primo fotogramma dell'hook è vuoto: metti "
                                             "in scena il titolo con self.add prima della prima animazione"))

    def play(self, *args, **kwargs) -> None:
        self.controlla_primo_fotogramma()
        super().play(*args, **kwargs)

    def wait(self, *args, **kwargs) -> None:
        self.controlla_primo_fotogramma()
        super().wait(*args, **kwargs)

    def chiudi(self) -> None:
        self.verifica("fine scena")
        if self.t > self.durata_s + self._fotogramma + 1e-6:
            self.avvisi.append(f"la scena dura {self.t:.2f} s ma la clip {self.durata_s:.2f} s: il finale viene tagliato")
        self.attendi_fino(self.durata_s)

    # --- costruzione ---------------------------------------------------------------------------------
    def construct(self) -> None:
        if self.debug:
            g = self.guide()
            self._escludi.update(id(m) for m in g.get_family())
            self.add(g)
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
        if self.area.caption:
            g.add(self.area.caption.rettangolo(stroke_color=col.attenuato, stroke_width=2))
        return g


__all__ = ["Area", "Aree", "CameraReel", "ScenaReel", "aree", "area_px", "inizi_per_parole", "ANTICIPO_S", "CODA_S",
           "DOWN", "UP", "LEFT", "RIGHT"]
