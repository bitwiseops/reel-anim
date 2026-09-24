"""Animazioni di «Non scappare dal cloud, sappi quale interruttore hai toccato»
(contenuti/sceneggiature/2026-09-24-dove-finiscono-chat.md).

Scene animate: 3, 5, 7, 8 (1 e 9 sono il presentatore a volto pieno, 2, 4, 6 filmati). Il reel si guarda muto: a
schermo solo figure ed etichette. Filo visivo: la **carta-chat** (riquadro, icona della chat, tre righe-sagoma, il
referto), l'**interruttore** (pillola con pallino: spento, a metà, acceso) e la **rete** (l'IA come piccola rete
neurale a tre strati, mai un database). Ogni scena dopo un filmato riparte dall'ultimo fotogramma della scena animata
prima (`fine_03`, `fine_05`, `fine_07`), e la 8 dall'ultimo della 7: le posizioni si calcolano solo qui.

Le icone Lucide di cestino, lucchetto, casa, interruttore e nuvola non ci sono in `assets/icone/`: sono forme
semplici disegnate qui (`cestino`, `lucchetto`, `casa`, `Interruttore`, `nuvola`).
"""
from __future__ import annotations

import numpy as np
from manim import (DOWN, LEFT, PI, RIGHT, UP, AnimationGroup, Arc, Circle, Circumscribe, Create, DashedLine, FadeIn,
                   FadeOut, FadeTransform, GrowFromPoint, Indicate, LaggedStart, Line, ManimColor,
                   Polygon, Rectangle, RoundedRectangle, Transform, Union,
                   UpdateFromAlphaFunc, VGroup, interpolate_color, linear, rate_functions, smooth,
                   squish_rate_func)

from tools.anim.base import ScenaReel
from tools.anim.componenti import Croce, Didascalia, Etichetta, Icona, Indice, etichetta, testo
from tools.anim.misure import px, tratto
from tools.anim.pattern import rimbalzo


# --- geometria ----------------------------------------------------------------------------------------------

def P(x: float, y: float) -> np.ndarray:
    """Un punto in px della tela (origine in alto a sinistra, 1080×1920) in unità Manim."""
    return np.array([px(x - 540), px(960 - y), 0.0])


def fin(anim, a: float, b: float):
    """L'animazione occupa solo la finestra [a, b] della play (curve sfalsate in una sola play)."""
    if hasattr(anim, "build"):
        anim = anim.build()
    anim.rate_func = squish_rate_func(anim.rate_func, a, b)
    return anim


# --- il filo visivo: carta-chat, interruttore, rete ------------------------------------------------------------

def carta_chat(col, larghezza_px: float, x: float, y: float) -> VGroup:
    """La chat: riquadro, icona della chat, tre righe-sagoma e il referto. Si costruisce alla misura voluta (i tratti
    restano gli stessi), sempre con gli stessi quattro pezzi: fra due misure si passa con Transform."""
    w = px(larghezza_px)
    box = RoundedRectangle(corner_radius=0.1 * w, width=w, height=0.7 * w, stroke_color=col.testo,
                           stroke_width=tratto(4), fill_color=col.sfondo, fill_opacity=1)
    chat = Icona("message-square", altezza_px=0.2 * larghezza_px, colore=col.testo)
    chat.move_to(box.get_center() + np.array([-0.3 * w, 0.18 * w, 0]))
    righe = VGroup()
    for i, q in enumerate((0.56, 0.46, 0.36)):
        r = RoundedRectangle(corner_radius=0.025 * w, width=q * w, height=0.05 * w, stroke_width=0,
                             fill_color=col.attenuato, fill_opacity=0.6)
        r.move_to(box.get_center() + np.array([-0.4 * w + q * w / 2, -0.02 * w - i * 0.1 * w, 0]))
        righe.add(r)
    referto = Icona("file-text", altezza_px=0.26 * larghezza_px, colore=col.secondario)
    referto.move_to(box.get_center() + np.array([0.3 * w, -0.13 * w, 0]))
    g = VGroup(box, chat, righe, referto)
    return g.move_to(P(x, y))


def carta_sagoma(col, larghezza_px: float) -> VGroup:
    """Una carta del mucchio che allena: riquadro e due righe, niente icone."""
    w = px(larghezza_px)
    box = RoundedRectangle(corner_radius=0.1 * w, width=w, height=0.7 * w, stroke_color=col.attenuato,
                           stroke_width=tratto(3), fill_color=col.sfondo, fill_opacity=1)
    righe = VGroup(*[RoundedRectangle(corner_radius=0.025 * w, width=q * w, height=0.05 * w, stroke_width=0,
                                      fill_color=col.attenuato, fill_opacity=0.6) for q in (0.6, 0.42)])
    righe.arrange(DOWN, buff=0.07 * w, aligned_edge=LEFT).move_to(box).align_to(box, LEFT).shift(RIGHT * 0.12 * w)
    return VGroup(box, righe)


def mucchio(col, x: float, y: float, larghezza_px: float = 110, n: int = 3) -> VGroup:
    """Le carte che allenano, impilate un po' sfalsate; (x, y) è il centro della carta più in basso."""
    return VGroup(*[carta_sagoma(col, larghezza_px).move_to(P(x + 6 * k, y - 8 * k)) for k in range(n)])


class Interruttore(VGroup):
    """L'interruttore: pillola con pallino. «spento» (pallino a sinistra, grigio), «meta» (al centro, chiaro),
    «acceso» (a destra, pillola in accento). `scatta(stato)` ritorna l'animazione: il pallino arriva con un piccolo
    rimbalzo e i colori sfumano. I tratti non scalano con la misura."""

    def __init__(self, col, altezza_px: float, stato: str = "spento", **kw):
        super().__init__(**kw)
        self.col = col
        h = px(altezza_px)
        self.pill = RoundedRectangle(corner_radius=h / 2, width=2 * h, height=h,
                                     stroke_width=Interruttore.spessore(altezza_px))
        self.knob = Circle(radius=h * 0.36, stroke_width=0, fill_opacity=1)
        self.add(self.pill, self.knob)
        self.stato = stato
        self._metti(stato)

    @staticmethod
    def spessore(altezza_px: float) -> float:
        return tratto(max(3.0, altezza_px * 0.07))

    def _colori(self, stato: str):
        c = self.col
        return {"spento": (c.sfondo, c.attenuato, c.attenuato), "meta": (c.sfondo, c.testo, c.testo),
                "acceso": (c.accento, c.accento, c.sfondo)}[stato]

    def _dx(self, stato: str) -> float:
        w, h = self.pill.width, self.pill.height
        return {"spento": -(w / 2 - h / 2), "meta": 0.0, "acceso": w / 2 - h / 2}[stato]

    def _metti(self, stato: str) -> None:
        f, s, k = self._colori(stato)
        self.pill.set_fill(f, opacity=1).set_stroke(s)
        self.knob.set_fill(k, opacity=1)
        self.knob.move_to(self.pill.get_center() + RIGHT * self._dx(stato))

    def scatta(self, stato: str, oltre: float = 0.12):
        da, self.stato = self.stato, stato
        c0 = [ManimColor(c) for c in self._colori(da)]
        c1 = [ManimColor(c) for c in self._colori(stato)]
        curva = rimbalzo(oltre)

        def passo(m, a):
            x0, x1 = m._dx(da), m._dx(stato)
            c = smooth(a)
            m.pill.set_fill(interpolate_color(c0[0], c1[0], c), opacity=1).set_stroke(interpolate_color(c0[1], c1[1], c))
            m.knob.set_fill(interpolate_color(c0[2], c1[2], c), opacity=1)
            m.knob.move_to(m.pill.get_center() + RIGHT * (x0 + (x1 - x0) * curva(a)))
        return UpdateFromAlphaFunc(self, passo, rate_func=linear)

    def esita(self):
        """Il pallino accenna a destra e a sinistra e torna al centro («te lo fa scegliere»)."""
        def passo(m, a):
            ampiezza = (m.pill.width / 2 - m.pill.height / 2) * 0.55
            m.knob.move_to(m.pill.get_center() + RIGHT * ampiezza * np.sin(2 * PI * 2 * a) * (1 - a))
        return UpdateFromAlphaFunc(self, passo, rate_func=linear)


def rete(col, larghezza_px: float, altezza_px: float, strati=(3, 4, 2), raggio_px: float = 12,
         tratto_px: float = 3, colore_nodi=None) -> VGroup:
    """L'IA come piccola rete neurale: tre strati di nodi uniti da archi. [0] = archi, [1] = nodi."""
    w, h, r = px(larghezza_px), px(altezza_px), px(raggio_px)
    xs = np.linspace(-w / 2 + r, w / 2 - r, len(strati))
    colonne, nodi = [], VGroup()
    for x, n in zip(xs, strati):
        ys = np.linspace(h / 2 - r, -h / 2 + r, n) if n > 1 else [0.0]
        c = [Circle(radius=r, stroke_color=colore_nodi or col.testo, stroke_width=tratto(tratto_px),
                    fill_color=col.sfondo, fill_opacity=1).move_to([x, y, 0]) for y in ys]
        colonne.append(c)
        nodi.add(*c)
    archi = VGroup(*[Line(a.get_center(), b.get_center(), stroke_color=col.attenuato, stroke_width=tratto(tratto_px * 0.7))
                     for c1, c2 in zip(colonne, colonne[1:]) for a in c1 for b in c2])
    return VGroup(archi, nodi)


def accendi_rete(r: VGroup, col, **kw):
    return AnimationGroup(r[0].animate.set_stroke(col.accento), r[1].animate.set_fill(col.accento, opacity=1).set_stroke(col.accento),
                          lag_ratio=0.3, **kw)


def rete_accesa(r: VGroup, col) -> VGroup:
    r[0].set_stroke(col.accento)
    r[1].set_fill(col.accento, opacity=1).set_stroke(col.accento)
    return r


def opacita_carta(carta: VGroup, o: float) -> VGroup:
    """Opacità di una carta-chat senza accendere il riempimento delle icone (set_opacity lo farebbe)."""
    box, chat, righe, referto = carta
    box.set_fill(opacity=o).set_stroke(opacity=o)
    righe.set_fill(opacity=0.6 * o)
    for ic in (chat, referto):
        ic.set_stroke(opacity=o)
    return carta


def cade(carta: VGroup, meta: np.ndarray):
    """Una carta compare, cade in `meta` accelerando e ci sparisce rimpicciolendo (dentro il cestino)."""
    partenza = carta.get_center().copy()
    base = carta.copy()
    opacita_carta(base, 1)

    def passo(m, a):
        o = min(1.0, a / 0.15) if a < 0.7 else max(0.0, 1 - (a - 0.7) / 0.3)
        t = rate_functions.ease_in_quad(a)
        s = 1 - 0.4 * max(0.0, (a - 0.6) / 0.4)
        m.become(opacita_carta(base.copy().scale(s).move_to(partenza + (meta - partenza) * t), o))
    return UpdateFromAlphaFunc(carta, passo, rate_func=linear)


def traccia(mob, colore=None):
    """Create senza il puntino: prima della sua finestra (alpha 0) il tratto non si vede. Con le estremità tonde,
    un Create a progresso zero disegna un puntino per ogni tratto, visibile per tutta l'attesa della finestra."""
    base = mob.copy()
    pezzi = [(m, b) for m, b in zip(mob.family_members_with_points(), base.family_members_with_points())]

    def passo(m, a):
        for sub, b in pezzi:
            if a <= 1e-3:
                sub.set_stroke(opacity=0)
                continue
            sub.pointwise_become_partial(b, 0, min(1.0, a))
            sub.set_stroke(opacity=b.get_stroke_opacity())
    return UpdateFromAlphaFunc(mob, passo, rate_func=linear)


def lampo(scena, linea, colore, spessore_px: float):
    """Un lampo che corre lungo `linea` (ShowPassingFlash senza il puntino prima e dopo). Ritorna (animazione, copia):
    la copia va tolta dalla scena dopo la play."""
    copia = linea.copy().set_stroke(colore, width=tratto(spessore_px))
    base = copia.copy()

    def passo(m, a):
        if a <= 1e-3 or a >= 1 - 1e-3:
            m.set_stroke(opacity=0)
            return
        m.pointwise_become_partial(base, max(0.0, a * 1.5 - 0.5), min(1.0, a * 1.5))
        m.set_stroke(opacity=1)
    return UpdateFromAlphaFunc(copia, passo, rate_func=linear), copia


def arriva(carta: VGroup, meta: np.ndarray):
    """Una carta compare ferma (opacità piena prima di muoversi), poi scivola in `meta` e ci si posa con un rimbalzo.
    Così non passa mai semitrasparente sopra le altre."""
    partenza = carta.get_center().copy()
    base = carta.copy()
    opacita_carta(base, 1)

    def passo(m, a):
        o = min(1.0, a / 0.2)
        t = rate_functions.ease_out_bounce(max(0.0, (a - 0.2) / 0.8))
        m.become(opacita_carta(base.copy().move_to(partenza + (meta - partenza) * t), o))
    return UpdateFromAlphaFunc(carta, passo, rate_func=linear)


def curva_verso(sw: "Interruttore", gomito: np.ndarray, meta: np.ndarray, altezza_px: float):
    """L'interruttore rimpicciolisce e va in `meta` lungo una curva che passa vicino a `gomito` (prima di lato, poi
    su): così non attraversa la carta che gli sta sopra."""
    p0 = sw.get_center().copy()
    h0, h1 = sw.pill.height, px(altezza_px)

    def passo(m, a):
        t = smooth(a)
        p = (1 - t) ** 2 * p0 + 2 * (1 - t) * t * gomito + t ** 2 * meta
        m.scale((h0 + (h1 - h0) * t) / m.pill.height)
        m.pill.set_stroke(width=Interruttore.spessore(m.pill.height * 120))   # il tratto segue la misura
        m.move_to(p)
    return UpdateFromAlphaFunc(sw, passo, rate_func=linear)


def parola(col, s: str, ruolo: str = "etichetta", colore=None) -> VGroup:
    return etichetta(testo(s, ruolo, colore=colore or col.testo, peso="BOLD"))


# --- scena 3: tre corsie ----------------------------------------------------------------------------------------

Y_TESTA, Y_INT, Y_CARTA = 660, 765, 880
X_CORSIE = (210, 510, 810)
H_INT = 60
L_MINI = 110


def testata(col, icona: str, s: str, x: float) -> VGroup:
    g = VGroup(Icona(icona, altezza_px=56, colore=col.testo), parola(col, s))
    g.arrange(RIGHT, buff=px(14))
    return g.move_to(P(x, Y_TESTA))


def cancello(col) -> VGroup:
    """Il cancello chiuso davanti al mucchio delle aziende: due sbarre."""
    return VGroup(*[Line(P(690, y), P(850, y), stroke_color=col.testo, stroke_width=tratto(9)) for y in (988, 1010)])


def pezzi_03(col) -> dict:
    """Tutti gli oggetti della scena 3 nella loro posizione finale. La scena 3 ci arriva, la 5 ci riparte."""
    d = {}
    d["testa1"] = testata(col, "user", "ChatGPT", X_CORSIE[0])
    d["int1"] = Interruttore(col, H_INT, "spento").move_to(P(X_CORSIE[0], Y_INT))
    d["mucchio1"] = mucchio(col, 150, 1080)
    d["carta_mucchio"] = carta_chat(col, L_MINI, 168, 1056)
    d["legame1"] = Line(P(156, 1122), P(205, 1200), stroke_color=col.attenuato, stroke_width=tratto(3))
    d["rete1"] = rete(col, 170, 120).move_to(P(210, 1265))
    d["carta_fuori"] = carta_chat(col, L_MINI, 300, 1125)
    d["testa2"] = testata(col, "user", "Claude", X_CORSIE[1])
    d["int2"] = Interruttore(col, H_INT, "meta").move_to(P(X_CORSIE[1], Y_INT))
    d["domanda"] = parola(col, "?", "punto", col.testo).move_to(P(622, Y_INT))
    d["testa3"] = testata(col, "factory", "API", X_CORSIE[2])
    d["mucchio3"] = mucchio(col, 760, 1080)
    d["cancello"] = cancello(col)
    d["legame3"] = Line(P(766, 1122), P(770, 1200), stroke_color=col.attenuato, stroke_width=tratto(3))
    d["rete3"] = rete(col, 150, 110).move_to(P(770, 1265))
    d["carta_api1"] = carta_chat(col, 100, 905, 1290)
    d["carta_api2"] = carta_chat(col, 100, 905, 1205)
    return d


def fine_03(col) -> dict:
    d = pezzi_03(col)
    rete_accesa(d["rete1"], col)
    return d


def ordine_03(d: dict) -> list:
    """L'ordine di disegno a fine scena 3 (come ci arriva la scena)."""
    return [d[k] for k in ("mucchio1", "legame1", "rete1", "testa1", "int1", "carta_mucchio", "carta_fuori", "testa2",
                           "int2", "domanda", "testa3", "cancello", "mucchio3", "legame3", "rete3", "carta_api1",
                           "carta_api2")]


class Scena03(ScenaReel):
    """L'interruttore grande a metà, poi acceso; tre corsie: ChatGPT (acceso → spento), Claude (a metà), aziende/API
    (cancello chiuso)."""

    def costruisci(self):
        col = self.cfg.palette
        d = fine_03(col)
        d["rete1"] = rete(col, 170, 120).move_to(P(210, 1265))   # spenta: si accende nel beat 1

        # beat 0 — la carta sola al primo fotogramma; cresce l'interruttore grande, fermo a metà ~1 s, poi acceso
        carta = carta_chat(col, 300, 510, 760)
        self.add(carta)
        grande = Interruttore(col, 220, "meta").move_to(P(510, 1095))
        self.play(carta.animate.set_stroke(col.attenuato),
                  FadeIn(grande, scale=0.25, rate_func=rimbalzo(0.06)), run_time=0.6)
        self.attendi_fino(1.6)
        self.play(grande.scatta("acceso"), run_time=0.45)

        # beat 1 — ChatGPT: l'interruttore torna piccolo nella corsia, la carta scende nel mucchio e la rete si accende;
        # spento, la carta dopo rimbalza fuori
        self.beat(1)
        self.play(fin(curva_verso(grande, P(X_CORSIE[0], 1095), P(X_CORSIE[0], Y_INT), H_INT), 0.0, 0.6),
                  fin(Transform(carta, carta_chat(col, L_MINI, X_CORSIE[1], Y_CARTA)), 0.45, 1.0),
                  fin(FadeIn(d["testa1"]), 0.35, 0.8),
                  fin(FadeIn(d["mucchio1"], shift=UP * 0.1), 0.45, 0.9),
                  fin(FadeIn(d["legame1"]), 0.55, 0.95),
                  fin(FadeIn(d["rete1"]), 0.55, 1.0), run_time=0.85)
        self.play(carta.animate.move_to(P(X_CORSIE[0], Y_CARTA)), run_time=0.35)   # sulla sua riga, sotto l'interruttore
        self.bring_to_front(carta)
        self.play(carta.animate(rate_func=rate_functions.ease_in_quad).move_to(d["carta_mucchio"]), run_time=0.45)
        corsa, scia = lampo(self, d["legame1"], col.accento, 7)
        self.play(corsa, accendi_rete(d["rete1"], col), run_time=0.55)
        self.remove(scia)
        self.attendi_fino(self.inizi_frasi[1] + 2.35)                  # «…finché non lo spegni»
        self.play(grande.scatta("spento", oltre=0.08), run_time=0.35)
        nuova = carta_chat(col, L_MINI, X_CORSIE[0], Y_CARTA)
        sopra = P(166, 985)
        self.play(FadeIn(nuova, run_time=0.2))
        self.play(nuova.animate(rate_func=rate_functions.ease_in_quad).move_to(sopra), run_time=0.3)
        arco = Arc(start_angle=PI * 0.95, angle=-PI * 0.9, radius=1).put_start_and_end_on(sopra, d["carta_fuori"].get_center())
        from manim import MoveAlongPath
        self.play(MoveAlongPath(nuova, arco, rate_func=rate_functions.ease_out_quad), run_time=0.45)

        # beat 2 — Claude: a metà, il pallino accenna e resta a metà
        self.beat(2)
        self.play(FadeIn(d["testa2"]), FadeIn(d["int2"], scale=0.8), FadeIn(d["domanda"]), run_time=0.45)
        self.play(d["int2"].esita(), run_time=0.8)

        # beat 3 — aziende e API: cancello chiuso, due carte scendono accanto al mucchio, la rete resta spenta
        self.beat(3)
        self.play(fin(FadeIn(d["testa3"]), 0.0, 0.5),
                  fin(FadeIn(d["mucchio3"], shift=UP * 0.1), 0.2, 0.65),
                  fin(FadeIn(d["legame3"]), 0.3, 0.7), fin(FadeIn(d["rete3"]), 0.3, 0.75),
                  fin(traccia(d["cancello"]), 0.5, 1.0), run_time=0.9)
        self.attendi_fino(self.inizi_frasi[3] + 1.2)
        c1 = carta_chat(col, 100, 905, 790)
        c2 = carta_chat(col, 100, 905, 790)
        self.play(fin(FadeIn(c1), 0.0, 0.12),
                  fin(c1.animate(rate_func=rate_functions.ease_in_out_quad).move_to(d["carta_api1"]), 0.1, 0.6),
                  fin(FadeIn(c2), 0.4, 0.52),
                  fin(c2.animate(rate_func=rate_functions.ease_in_out_quad).move_to(d["carta_api2"]), 0.5, 1.0),
                  run_time=1.7)
        self.attendi_fino(self.inizi_frasi[3] + 3.4)                   # «…nessuno dei due addestra»
        self.play(Indicate(d["cancello"], color=col.accento, scale_factor=1.08), run_time=0.7)


# --- scena 5: l'orologio dei giorni -----------------------------------------------------------------------------

X_CARTA5, Y_ALTO5 = 135, 665
L_CARTA5 = 150
H_INT5 = 56
X_INT5 = 290
Y_FILA = 1000
COLONNE, RIGHE_BANDA = 73, 5
X0_MURO, X1_MURO, Y0_MURO = 64, 956, 752
PASSO_BANDA, PASSO_RIGA = 112, 15


def puntino(col, x: float, y: float, r_px: float, colore) -> Circle:
    return Circle(radius=px(r_px), stroke_width=0, fill_color=colore, fill_opacity=1).move_to(P(x, y))


def fila(col, piccola: bool, accesa: bool) -> VGroup:
    """I 30 giorni: grandi al centro, o nell'angolo del muro (prima riga della prima banda)."""
    colore = col.accento if accesa else col.attenuato
    if piccola:
        passo = (X1_MURO - X0_MURO) / (COLONNE - 1)
        return VGroup(*[puntino(col, X0_MURO + i * passo, Y0_MURO, 4.5, colore) for i in range(30)])
    return VGroup(*[puntino(col, 510 + (i - 14.5) * 28, Y_FILA, 8, colore) for i in range(30)])


def muro(col) -> VGroup:
    """1.825 giorni = 5 bande (anni) da 5 × 73 = 365 puntini; senza i 30 della fila, che stanno nell'angolo."""
    passo = (X1_MURO - X0_MURO) / (COLONNE - 1)
    bande = VGroup()
    for k in range(5):
        b = VGroup()
        for r in range(RIGHE_BANDA):
            for c in range(COLONNE):
                if k == 0 and r == 0 and c < 30:
                    continue
                b.add(puntino(col, X0_MURO + c * passo, Y0_MURO + k * PASSO_BANDA + r * PASSO_RIGA, 4.5, col.secondario))
        bande.add(b)
    return bande


def eti_giorni(col) -> Etichetta:
    e = Etichetta("30 giorni", colore=col.accento, pieno=False)
    return e.move_to(P(510, 1078))


def pezzi_05(col, area) -> dict:
    d = {"carta": carta_chat(col, L_CARTA5, X_CARTA5, Y_ALTO5),
         "int": Interruttore(col, H_INT5, "spento").move_to(P(X_INT5, Y_ALTO5)),
         "fila": fila(col, piccola=False, accesa=True),
         "giorni": eti_giorni(col),
         "fonte": Didascalia("Anthropic, 2025", area=area)}
    return d


def fine_05(col, area) -> dict:
    return pezzi_05(col, area)


class Scena05(ScenaReel):
    """Trenta puntini a interruttore spento; acceso, un muro di 1.825; rispento, il muro rientra nei trenta accesi."""

    def costruisci(self):
        col, a = self.cfg.palette, self.area.contenuto
        prima = fine_03(col)
        self.add(*ordine_03(prima))
        d = pezzi_05(col, a)
        fila_g = fila(col, piccola=False, accesa=False)

        # beat 0 — dalla scena 3 restano solo l'interruttore (senza nome) e una carta; la fonte in fondo; la fila grigia
        nomi = [prima[k] for k in ("testa1", "testa2", "testa3", "domanda")]
        via = [m for k, m in prima.items() if k not in ("int1", "carta_fuori", "testa1", "testa2", "testa3", "domanda")]
        interr = prima["int1"]
        carta = prima["carta_fuori"]
        self.play(*[fin(FadeOut(m), 0.0, 0.1) for m in nomi], *[fin(FadeOut(m), 0.0, 0.3) for m in via],
                  fin(curva_verso(interr, (interr.get_center() + d["int"].get_center()) / 2, d["int"].get_center(), H_INT5), 0.25, 0.7),
                  fin(Transform(carta, d["carta"]), 0.25, 0.75),
                  fin(FadeIn(d["fonte"]), 0.35, 0.6), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in fila_g], lag_ratio=0.04), run_time=0.6)

        # beat 1 — i 30 giorni si accendono; «30 giorni»
        self.beat(1)
        self.play(LaggedStart(*[p.animate.set_fill(col.accento) for p in fila_g], lag_ratio=0.12), run_time=0.7)
        self.play(d["giorni"].entra(), run_time=0.3)

        # beat 2 — acceso: la fila va nell'angolo e da lì esplode il muro dei 5 anni
        self.beat(2)
        m = muro(col)
        angolo = fila(col, piccola=True, accesa=True)
        centro_angolo = angolo.get_center()
        anni = Etichetta("5 anni", colore=col.secondario, pieno=False)
        anni.move_to(P(850, Y_ALTO5))
        self.play(fin(interr.scatta("acceso"), 0.0, 0.22), fin(FadeOut(d["giorni"]), 0.0, 0.16),
                  fin(Transform(fila_g, angolo), 0.12, 0.38),
                  fin(LaggedStart(*[GrowFromPoint(b, centro_angolo) for b in m], lag_ratio=0.18), 0.32, 0.9),
                  fin(anni.entra(), 0.72, 0.92), run_time=1.3)

        # beat 3 — rispento: il muro rientra nella fila, che torna grande e resta accesa
        self.beat(3)
        self.play(interr.scatta("spento", oltre=0.08), run_time=0.3)
        self.play(fin(FadeOut(anni), 0.0, 0.25),
                  fin(LaggedStart(*[FadeOut(b, target_position=centro_angolo, scale=0.05) for b in reversed(m)],
                                  lag_ratio=0.15), 0.0, 0.62),
                  fin(Transform(fila_g, d["fila"]), 0.6, 0.95),
                  fin(FadeIn(d["giorni"]), 0.8, 1.0), run_time=1.1)
        self.play(Circumscribe(fila_g, color=col.accento, buff=px(18), stroke_width=tratto(5)), run_time=0.9)


# --- scena 7: il cestino e la sbarra ---------------------------------------------------------------------------

X_CESTINO, Y_BOCCA = 510, 1100
L_CARTA7 = 240


def cestino(col) -> VGroup:
    """Il cestino: corpo a trapezio con tre costole, coperchio con maniglia. [0] corpo, [1] costole, [2] coperchio."""
    cx, top, h, lt, lb = X_CESTINO, Y_BOCCA, 230, 320, 250
    corpo = Polygon(P(cx - lt / 2, top), P(cx + lt / 2, top), P(cx + lb / 2, top + h), P(cx - lb / 2, top + h),
                    stroke_color=col.testo, stroke_width=tratto(5), fill_color=col.sfondo, fill_opacity=1)
    costole = VGroup(*[Line(P(cx + dx, top + 35), P(cx + dx * 0.8, top + h - 30), stroke_color=col.attenuato,
                            stroke_width=tratto(4)) for dx in (-70, 0, 70)])
    coperchio = RoundedRectangle(corner_radius=px(6), width=px(lt + 24), height=px(18), stroke_color=col.testo,
                                 stroke_width=tratto(5), fill_color=col.sfondo, fill_opacity=1).move_to(P(cx, top - 11))
    manico = RoundedRectangle(corner_radius=px(6), width=px(80), height=px(16), stroke_color=col.testo,
                              stroke_width=tratto(5), fill_color=col.sfondo, fill_opacity=1).move_to(P(cx, top - 28))
    return VGroup(corpo, costole, VGroup(manico, coperchio))


APERTURA = -0.44 * PI          # il coperchio, alzato, sta appoggiato in piedi a destra del cestino
COPERCHIO_APERTO = (728, 932)


def coperchio_aperto(coperchio: VGroup) -> VGroup:
    return coperchio.rotate(APERTURA).move_to(P(*COPERCHIO_APERTO))


def apri(coperchio: VGroup):
    """Il coperchio si alza, ruota e scivola a destra: resta basso finché è sopra la bocca."""
    base = coperchio.copy()
    da, a_ = base.get_center().copy(), P(*COPERCHIO_APERTO)

    def passo(m, a):
        sale = smooth(min(1.0, a / 0.35))
        p = da + (a_ - da) * smooth(a) + UP * px(30) * sale * (1 - smooth(a))
        m.become(base.copy().rotate(APERTURA * smooth(a)).move_to(p))
    return UpdateFromAlphaFunc(coperchio, passo, rate_func=linear)
SBARRA = ((330, 1050), (690, 1050))
ALZATA = PI * 0.47


def sbarra(col) -> Line:
    return Line(P(*SBARRA[0]), P(*SBARRA[1]), stroke_color=col.testo, stroke_width=tratto(12))


def perno(col) -> Circle:
    """Il perno della sbarra, all'estremo sinistro: quando si alza si capisce che ruota, non che vola via."""
    return Circle(radius=px(12), stroke_width=0, fill_color=col.testo, fill_opacity=1).move_to(P(*SBARRA[0]))


def lucchetto(col, x: float, y: float) -> VGroup:
    corpo = RoundedRectangle(corner_radius=px(6), width=px(46), height=px(38), stroke_color=col.testo,
                             stroke_width=tratto(4), fill_color=col.sfondo, fill_opacity=1)
    arco = Arc(radius=px(14), start_angle=0, angle=PI, stroke_color=col.testo, stroke_width=tratto(5))
    arco.next_to(corpo, UP, buff=0)
    return VGroup(arco, corpo).move_to(P(x, y - 8))


def pillola_anno(col, s: str) -> Etichetta:
    e = Etichetta(s, colore=col.accento, pieno=False)
    return e.move_to(P(60, 650), aligned_edge=LEFT)


def pezzi_07_fine(col) -> dict:
    """L'ultimo fotogramma della 7: pillola «set 2025», «New York», cestino aperto, sbarra alzata."""
    c = cestino(col)
    coperchio_aperto(c[2])
    s = sbarra(col).rotate(ALZATA, about_point=P(*SBARRA[0]))
    pill = pillola_anno(col, "set 2025")
    ny = parola(col, "New York", colore=col.attenuato)
    ny.next_to(pill, RIGHT, buff=px(24))
    return {"pillola": pill, "ny": ny, "cestino": c, "sbarra": s, "perno": perno(col)}


def fine_07(col) -> dict:
    return pezzi_07_fine(col)


class Scena07(ScenaReel):
    """La carta trascinata nel cestino si ferma su una sbarra e finisce in una scatola chiusa; finito l'ordine, la
    sbarra si alza e le carte nuove cadono."""

    def costruisci(self):
        col, a = self.cfg.palette, self.area.contenuto
        prima = fine_05(col, a)
        self.add(prima["fonte"], prima["fila"], prima["giorni"], prima["carta"], prima["int"])

        # beat 0 — la fila diventa la pillola «2025», la carta al centro, il cestino; il puntatore la porta sopra
        pill = pillola_anno(col, "2025")
        ny = parola(col, "New York", colore=col.attenuato)
        ny.next_to(pillola_anno(col, "set 2025"), RIGHT, buff=px(24))
        c = cestino(col)
        carta = prima["carta"]
        self.play(fin(FadeOut(prima["int"]), 0.0, 0.3), fin(FadeOut(prima["fonte"]), 0.0, 0.3),
                  fin(FadeOut(prima["giorni"]), 0.0, 0.3),
                  fin(FadeOut(prima["fila"], target_position=pill.get_center(), scale=0.15), 0.0, 0.45),
                  fin(FadeIn(pill, scale=0.8), 0.62, 0.85), fin(FadeIn(ny), 0.7, 0.95),
                  fin(Transform(carta, carta_chat(col, L_CARTA7, 360, 810)), 0.2, 0.7),
                  fin(FadeIn(c, shift=UP * 0.2), 0.4, 0.9), run_time=0.9)
        mano = Indice()
        mano.move_to(carta.get_center() + np.array([mano.width / 2 - px(10), -mano.height / 2 + px(10), 0]))
        self.attendi_fino(1.3)
        self.play(mano.entra(), run_time=0.3)
        self.attendi_fino(1.9)
        sopra = P(X_CESTINO, 868)
        self.play(fin(apri(c[2]), 0.0, 0.5), fin(mano.trascina(carta, sopra), 0.3, 1.0), run_time=1.2)
        self.play(FadeOut(mano, shift=DOWN * 0.2), run_time=0.3)

        # beat 1 — la sbarra si disegna sulla bocca, la carta ci sbatte e si ferma; la scatola col lucchetto si chiude;
        # arrivano altre due carte
        self.beat(1)
        s = sbarra(col)
        pr = perno(col)
        ferma = P(X_CESTINO, 1050 - 0.35 * L_CARTA7 - 6)
        self.play(fin(Create(s), 0.0, 0.45), fin(FadeIn(pr, scale=0.5), 0.0, 0.2),
                  fin(carta.animate(rate_func=rate_functions.ease_out_bounce).move_to(ferma), 0.4, 1.0), run_time=0.9)
        altre = [carta_chat(col, L_CARTA7, 182, 880) for _ in range(2)]   # da sinistra, già piene
        mete = [ferma + np.array([px(10 * (i + 1)), px(18 * (i + 1)), 0]) for i in range(2)]
        for c_ in altre:
            opacita_carta(c_, 0)
        self.add(*altre)
        self.play(fin(arriva(altre[0], mete[0]), 0.0, 0.55), fin(arriva(altre[1], mete[1]), 0.45, 1.0), run_time=0.9)
        scatola = RoundedRectangle(corner_radius=px(18), width=px(300), height=px(236), stroke_color=col.testo,
                                   stroke_width=tratto(9), fill_opacity=0).move_to(P(X_CESTINO + 10, 1040 - 118))
        chiave = lucchetto(col, X_CESTINO + 10, 1040 - 236)
        self.play(fin(Create(scatola), 0.0, 0.8), fin(FadeIn(chiave, scale=0.6), 0.6, 1.0), run_time=0.6)
        self.play(Indicate(VGroup(scatola, chiave), color=col.accento, scale_factor=1.06), run_time=0.5)   # si chiude

        # beat 2 — l'ordine del giudice: la sbarra si accende
        self.beat(2)
        self.play(s.animate.set_stroke(col.accento), run_time=0.3)
        self.play(Indicate(s, color=col.accento, scale_factor=1.1), run_time=0.6)

        # beat 3 — «set 2025»: la scatola esce chiusa, la sbarra si alza, le carte nuove cadono nel cestino
        self.beat(3)
        fine = pezzi_07_fine(col)
        scatola_g = VGroup(scatola, chiave, carta, *altre)
        self.play(fin(FadeTransform(pill, fine["pillola"]), 0.0, 0.45),
                  fin(scatola_g.animate(rate_func=rate_functions.rush_into).shift(LEFT * px(760)), 0.3, 1.0), run_time=1.0)
        self.remove(scatola, chiave, carta, *altre)
        nuove = [carta_chat(col, L_CARTA7, X_CESTINO + 30, 790) for _ in range(2)]
        for n in nuove:
            opacita_carta(n, 0)
        self.add(*nuove)
        self.bring_to_back(*nuove)
        dentro = P(X_CESTINO + 10, 1215)
        self.play(fin(Transform(s, fine["sbarra"].copy().set_stroke(col.accento)), 0.0, 0.4),
                  fin(cade(nuove[0], dentro), 0.28, 0.68), fin(cade(nuove[1], dentro), 0.62, 1.0), run_time=1.2)
        self.remove(*nuove)


# --- scena 8: la casa -----------------------------------------------------------------------------------------

CASA = (480, 930, 900, 1340)   # corpo: x0, y0, x1, y1
FINESTRA = (540, 985)
CARTA8 = (785, 1062)
L_CARTA8 = 150


def casa(col) -> VGroup:
    """Tetto a triangolo, corpo quadrato, una finestra. [0] tetto, [1] corpo, [2] finestra, [3] muro sinistro."""
    x0, y0, x1, y1 = CASA
    tetto = Polygon(P(x0 - 25, y0), P(x1 + 25, y0), P((x0 + x1) / 2, 710), stroke_color=col.testo,
                    stroke_width=tratto(5), fill_opacity=0)
    corpo = Rectangle(width=px(x1 - x0), height=px(y1 - y0), stroke_color=col.testo, stroke_width=tratto(5),
                      fill_opacity=0).move_to(P((x0 + x1) / 2, (y0 + y1) / 2))
    finestra = Rectangle(width=px(52), height=px(52), stroke_color=col.testo, stroke_width=tratto(4),
                         fill_opacity=0).move_to(P(*FINESTRA))
    muro_sx = Line(P(x0, y0), P(x0, y1), stroke_color=col.testo, stroke_width=tratto(5))
    return VGroup(tetto, corpo, finestra, muro_sx)


def portatile(col) -> VGroup:
    schermo = RoundedRectangle(corner_radius=px(10), width=px(190), height=px(116), stroke_color=col.testo,
                               stroke_width=tratto(4), fill_color=col.sfondo, fill_opacity=1).move_to(P(700, 1190))
    base = Polygon(P(575, 1252), P(825, 1252), P(840, 1268), P(560, 1268), stroke_color=col.testo,
                   stroke_width=tratto(4), fill_color=col.sfondo, fill_opacity=1)
    return VGroup(schermo, base)


def nuvola(col) -> VGroup:
    """La nuvola: tre cerchi e una base fusi in un solo contorno (disegnata una volta, alla sua misura)."""
    pezzi = [Circle(radius=px(72)).move_to(P(150, 765)), Circle(radius=px(95)).move_to(P(240, 708)),
             Circle(radius=px(72)).move_to(P(330, 760)),
             RoundedRectangle(corner_radius=px(40), width=px(300), height=px(90)).move_to(P(240, 790))]
    forma = Union(*pezzi, stroke_color=col.attenuato, stroke_width=tratto(5), fill_color=col.sfondo, fill_opacity=1)
    return VGroup(forma)


class Scena08(ScenaReel):
    """La chat rimbalza sul muro di casa; in casa una rete più piccola che sta in 16 GB; niente esce."""

    def costruisci(self):
        col = self.cfg.palette
        prima = fine_07(col)
        self.add(prima["cestino"], prima["sbarra"].set_stroke(col.accento), prima["perno"], prima["pillola"], prima["ny"])

        # beat 0 — (una sola play) via la scena 7, entrano casa, portatile, nuvola con la rete grande e la carta;
        # la carta carica, parte verso la nuvola, sbatte sul muro e rimbalza dentro
        h = casa(col)
        pc = portatile(col)
        nv = nuvola(col)
        grande = rete(col, 200, 108, (3, 4, 3), raggio_px=11).move_to(P(240, 765))
        carta = carta_chat(col, L_CARTA8, *CARTA8)
        base = opacita_carta(carta.copy(), 1)
        opacita_carta(carta, 0)
        riposo = carta.get_center().copy()
        urto = P(CASA[0] + 8 + L_CARTA8 / 2, 960)                  # verso la nuvola: in alto a sinistra, contro il muro
        carica = riposo + (riposo - urto) * 0.14
        larga = base.width

        def volo(m, a):
            """Compare (0-0,1), carica all'indietro, vola verso la nuvola, si schiaccia sul muro, rimbalza dentro."""
            sx, o = 1.0, min(1.0, a / 0.1)
            if a < 0.1:
                p = riposo
            elif a < 0.3:
                p = riposo + (carica - riposo) * smooth((a - 0.1) / 0.2)
            elif a < 0.5:
                p = carica + (urto - carica) * rate_functions.rush_into((a - 0.3) / 0.2)
            else:
                b = (a - 0.5) / 0.5
                p = urto + (riposo - urto) * rimbalzo(0.12)(b)
                if b < 0.2:
                    sx = 1 - 0.3 * np.sin(PI * b / 0.2)   # schiacciata contro il muro
            c = opacita_carta(base.copy().stretch_to_fit_width(larga * sx), o)
            m.become(c.move_to(p + LEFT * (larga * (1 - sx) / 2)))

        # il colpo sul muro: il muro sinistro e la falda del tetto si accendono spessi e si spengono, tre scintille fuori
        x0, y0 = CASA[0], CASA[1]
        bordo = VGroup(Line(P(x0, CASA[3]), P(x0, y0)), Line(P(x0 - 25, y0), P((x0 + CASA[2]) / 2, 710)))
        bordo.set_stroke(col.accento, width=tratto(14))
        scintille = VGroup(*[Line(P(462, 960 + dy), P(462 - 46, 960 + dy * 2.2)) for dy in (-30, 0, 30)])
        scintille.set_stroke(col.accento, width=tratto(7))
        colpo = VGroup(bordo, scintille).set_stroke(opacity=0)

        def botta(m, a):
            o = 0.0 if a <= 0 or a >= 1 else (1 - a) ** 1.5
            m.set_stroke(opacity=o)
            sc = m[1]
            for i, l in enumerate(sc):
                dy = (-30, 0, 30)[i]
                l.put_start_and_end_on(P(462 - 10 * a, 960 + dy), P(462 - 20 - 50 * a, 960 + dy * (1.6 + a)))

        self.add(carta)
        self.play(*[fin(FadeOut(m), 0.0, 0.12) for m in prima.values()],
                  fin(traccia(VGroup(h[0], h[1], h[2])), 0.08, 0.3),
                  fin(FadeIn(pc), 0.14, 0.28), fin(FadeIn(nv), 0.12, 0.26), fin(FadeIn(grande), 0.16, 0.3),
                  fin(UpdateFromAlphaFunc(carta, volo, rate_func=linear), 0.26, 1.0),
                  fin(UpdateFromAlphaFunc(colpo, botta, rate_func=linear), 0.62, 0.84), run_time=2.3)
        self.remove(colpo)

        # beat 1 — (una sola play) la chiavetta con la barra che si riempie, «16 GB», la fonte, la rete piccola
        self.beat(1)
        chiavetta = Icona("memory-stick", altezza_px=64, colore=col.testo).move_to(P(100, 1040))
        guscio = RoundedRectangle(corner_radius=px(8), width=px(270), height=px(30), stroke_color=col.attenuato,
                                  stroke_width=tratto(3), fill_opacity=0).move_to(P(290, 1040))
        riempi = RoundedRectangle(corner_radius=px(8), width=px(270), height=px(30), stroke_width=0,
                                  fill_color=col.accento, fill_opacity=1).move_to(guscio)
        gb = parola(col, "16 GB", "messaggio", col.accento)
        gb.move_to(P(60, 1128), aligned_edge=LEFT)
        fonte = etichetta(testo("OpenAI, 2025", "piede", colore=col.attenuato))
        fonte.move_to(P(60, 1200), aligned_edge=LEFT)
        piccola = rete(col, 116, 70, (2, 3, 2), raggio_px=8, tratto_px=2.5).move_to(P(700, 1190))
        self.play(fin(FadeIn(chiavetta), 0.0, 0.1), fin(FadeIn(guscio), 0.02, 0.12),
                  fin(GrowFromPoint(riempi, guscio.get_left(), rate_func=linear), 0.1, 0.45),
                  fin(FadeIn(gb, shift=UP * 0.1), 0.4, 0.55), fin(FadeIn(fonte), 0.48, 0.62),
                  fin(FadeIn(piccola, scale=0.4), 0.82, 1.0), run_time=4.0)

        # beat 2 — (una sola play) dalla finestra una freccia tratteggiata verso la nuvola si ferma su una croce;
        # accanto alla casa l'interruttore spento. È l'ultimo fotogramma animato del reel.
        self.beat(2)
        croce_p = P(330, 900)
        freccia = DashedLine(P(FINESTRA[0] - 30, FINESTRA[1]), croce_p + np.array([px(30), -px(12), 0]),
                             dash_length=px(16), stroke_color=col.attenuato, stroke_width=tratto(5))
        croce = Croce(altezza_px=52, spessore_px=10).move_to(croce_p)
        interr = Interruttore(col, 50, "spento").move_to(P(112, 1295))
        self.play(fin(Create(freccia), 0.0, 0.45), fin(traccia(croce), 0.42, 0.72),
                  fin(FadeIn(interr, scale=0.8), 0.7, 1.0), run_time=1.5)
