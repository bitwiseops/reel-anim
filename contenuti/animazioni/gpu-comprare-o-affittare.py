"""Animazioni di «Scheda per l'IA? Conviene solo se la usi tanto»
(contenuti/sceneggiature/2026-09-22-gpu-comprare-o-affittare.md).

Regime «il reel si guarda muto» (docs/animazioni.md §0): nessuna frase a schermo. A schermo solo figure, numeri
(2028, 1 €, 0,53 €, 0,16 €, 300 h, 1.500 €, 42 €, 110 h, ≈ 4 h, 24 GB, 90 h, 110) ed etichette marcate
(«TrendForce, 2026», «RunPod + IVA, set. 2026», «500 W · ARERA», «esempio»).

Scene animate: 3, 5, 6, 8. La 1 e la 9 sono il presentatore a tutto schermo, la 2, la 4 e la 7 filmati `[broll]`:
nessuna classe. Continuità (docs/animazioni.md §2 e §5): la 5 parte dall'ultimo fotogramma della 3 (`fine_3`), la 6
dall'ultimo della 5 (`fine_5`), la 8 dall'ultimo della 6 (`fine_6`): dopo il filmato si entra con un taglio su uno
stato che chi guarda riconosce, e il primo cambiamento parte subito.

Il filo visivo (stesso aspetto, sempre ricostruito dalle stesse funzioni):
- la **scheda video** (`Scheda`): corpo, staffa, pettine, due ventole, otto alloggi con i chip; si scala con
  `Transform` verso un'altra `Scheda` della stessa struttura;
- il **server a cassetti** (`Server`, secondario, disegnato qui: nessuna icona Lucide adatta): nella 3 porta sopra
  la **rete neurale** (`Rete`, tre strati di nodi e archi: l'IA) e riceve per primo i moduli di memoria della
  fabbrica (Icona `memory-stick`), un cassetto per modulo; solo dopo due moduli vanno alla rastrelliera d'uscita;
  dalla 5 la rete si spegne ed esce e il server resta come noleggio (la riga piatta cade da lì, nella 6 sta
  nell'area del noleggio, nella 8 ci vola il modello troppo grande). Decisione del presentatore, 2026-09-22;
- le **ore**: la linea del tempo nella 3, l'asse del grafico nella 5-6, l'orologio nella 6, la barra nella 8.

Mosse wow (manuale §11bis): 3 contrasto di scala (zoom 1,4× sulla rastrelliera: due schede, e i sei posti vuoti
che pulsano insieme; poi la rastrelliera che cresce al centro), 5 metamorfosi
(la pila di monete si sfoglia in 36 fette), 6 rivelazione a tratto (l'incrocio a 110 h), 8 carica e rimbalzo (il
modello troppo grande che vola nel server).

Posizioni in px della tela (origine in alto a sinistra) con `punto()`; l'area contenuto è 60..960 × 604..1356 px.
"""
from __future__ import annotations

import numpy as np
from manim import (BOLD, DOWN, LEFT, ORIGIN, PI, RIGHT, TAU, UP, AnnularSector, ArcBetweenPoints, Circle, Create,
                   Arrow, DashedLine, DashedVMobject, Dot, FadeIn, FadeOut, GrowArrow, Line, Rectangle, RoundedRectangle, Transform,
                   ManimColor, UpdateFromAlphaFunc, VGroup, VMobject, interpolate_color, linear, rate_functions, smooth,
                   squish_rate_func, there_and_back)

from tools.anim.base import ScenaReel
from tools.anim.componenti import Croce, Freccia, Icona, Sagome, Spunta, etichetta, testo
from tools.anim.config import carica
from tools.anim.misure import PX_PER_UNITA, px, tratto
from tools.anim.pattern import controlla_zoom, rimbalzo

CFG = carica()
P = CFG.palette
ease_out_cubic = rate_functions.ease_out_cubic
ease_out_back = rate_functions.ease_out_back
ease_in_quad = rate_functions.ease_in_quad
rush_into = rate_functions.rush_into

# --- numeri del conto (Note di produzione, «Il conto a due tempi») -------------------------------------------
RIGA_E = 0.531          # RunPod RTX 3090 0,50 $/h, cambio BCE, + IVA 22 %
CORR_E = 0.158          # 0,5 kW × 31,63 c€/kWh (ARERA)
RATA = 1500 / 36        # 41,67 € al mese
H_INCROCIO = RATA / (RIGA_E - CORR_E)   # 111,7 h: a schermo «110 h»
ORE_GIORNO = 3.7        # 110 / 30

# --- misure condivise (px della tela) ------------------------------------------------------------------------
W_S, H_S = 380, 240                      # la scheda a scala 1
# scena 3 (rifatta il 2026-09-23): la fabbrica in alto, il server con la rete a sinistra, sotto la fabbrica la
# rastrelliera d'uscita della produzione (otto posti in due file da quattro), la linea del tempo in fondo
FAB3, FAB3_H = (625, 720), 170           # la fabbrica (Icona `factory`): centro e altezza in px
FAB3_NUOVA = (855, 720)                  # la fabbrica nuova, solo tratteggiata (in costruzione)
MODULO_H = 80                            # il modulo di memoria (Icona `memory-stick`): alto 80, largo 133 px
RAST_C, RAST_PASSO, S_POSTO = (625, 1020), (128, 190), 0.3    # centro, passo (x, y) dei posti, scala della scheda
POSTO_W, POSTO_H = 122, 86               # il posto tratteggiato attorno alla scheda piccola
RAST_FINE, RAST_SCALA = (430, 1085), 1.4  # fine della 3: la rastrelliera al centro, più grande
Q3 = (880, 1085)
Y_TEMPO, X_SBARRA = 1282, 900            # la linea del tempo e la sbarra del 2028 (il filo dalla fabbrica nuova)
C5, SCALA5 = (780, 1240), 0.8            # scene 5-6: in basso a destra, sotto il grafico
C6_PICCOLA, SCALA6 = (700, 718), 0.3     # scena 6: nell'area «conviene comprare»
C8 = (400, 1080)                         # scena 8: la scheda contenitore
PIENO = 0.22                             # il velo accento del cassetto che ha ricevuto la memoria
SRV3 = (160, 1010, 210)                  # (x, y, altezza) del server a cassetti; la rete gli sta sopra
RETE3 = (160, 895, 150)                  # (x del centro, y del lato basso, larghezza) della rete neurale
SRV3_FINE, RETE3_FINE = (150, 732, 100), (150, 674, 70)   # fine della 3: piccoli, in alto a sinistra
SRV5 = (262, 642, 70)
SRV6 = (322, 893, 96)                    # nell'area del noleggio, fra la riga piatta e la tratteggiata
SRV8 = (150, 690, 120)
# il grafico: assi, scala verticale 1 € = 340 px, orizzontale 300 h = 710 px
X0, XF, Y0, H1 = 205, 900, 1010, 340
PICCOLO, ANCORA_PICCOLO, META_PICCOLO = 0.6, (X0, Y0 - H1), (80, 622)   # scena 6: il grafico ridotto in alto
OROLOGIO, R_OROLOGIO = (260, 1060), 140
# il calendario del mese (righe da 7, condizione del revisore 2026-09-23): nella 6 a destra dell'orologio, nella 8
# piccolo accanto al server
CAL6 = (560, 948, 40, 52)                # (x sinistra, y alto, lato, passo) in px
CAL8 = (228, 640, 16, 21)
# scena 8: il blocco-modello (uno che ci sta, uno largo il doppio che sborda) e la barra delle ore pagate
BLOCCO_W = 340
BLOCCO_SU = (430, 850)                   # dove aspetta la copia larga, sopra la scheda, prima di volare al server
BAR_X, BAR_W, BAR_Y0, BAR_H, BAR_MAX = 830, 60, 1260, 500, 160


def punto(x: float, y: float) -> np.ndarray:
    return np.array([px(x) - CFG.frame_width / 2, CFG.frame_height / 2 - px(y), 0.0])


def w_px(m) -> float:
    return m.width * PX_PER_UNITA


def h_px(m) -> float:
    return m.height * PX_PER_UNITA


def colloca(m, x: float, y: float, h: str = "c", v: str = "c"):
    """Mette m con il bordo `h` (l | c | r) sulla x e il bordo `v` (t | c | b) sulla y, in px della tela."""
    dx = {"l": w_px(m) / 2, "c": 0, "r": -w_px(m) / 2}[h]
    dy = {"t": h_px(m) / 2, "c": 0, "b": -h_px(m) / 2}[v]
    return m.move_to(punto(x + dx, y + dy))


def hx(h: float) -> float:
    return X0 + (XF - X0) * h / 300


def ey(e: float) -> float:
    return Y0 - H1 * e


def fra(a: float, b: float = 1.0, f=smooth):
    """Curva `f` compressa nella frazione [a, b] della play (movimenti sfalsati in un solo passaggio)."""
    return squish_rate_func(f, max(0.0, a), min(1.0, b))


class Server(VGroup):
    """Il server a cassetti (i server dell'IA, poi il noleggio): corpo pieno, quattro cassetti, ognuno con la fessura
    a sinistra e la lucina a destra (accesa in accento quando il cassetto ha ricevuto la memoria). Pochi dettagli,
    così regge anche a 60 px; stessa struttura a ogni grandezza, quindi si passa da uno stato all'altro con Transform.
    I tratti non si scalano: vanno scelti sulla grandezza finale."""

    def __init__(self, altezza: float = 170, centro=(175, 1000), accese: int = 4, riempite: int | None = None,
                 **kw):
        super().__init__(**kw)
        h = altezza
        w = 0.78 * h
        c = punto(*centro)
        k = min(1.0, 0.4 + 0.6 * h / 170)

        def off(dx, dy):
            return c + np.array([px(dx), -px(dy), 0.0])

        self.corpo = RoundedRectangle(corner_radius=px(0.07 * h), width=px(w), height=px(h), stroke_color=P.secondario,
                                      stroke_width=tratto(max(2.0, 4.5 * k)), fill_color=P.sfondo,
                                      fill_opacity=1).move_to(c)
        pad, gap = 0.09 * h, 0.045 * h
        hc = (h - 2 * pad - 3 * gap) / 4
        wc = w - 2 * pad
        riempite = accese if riempite is None else riempite
        self.cassetti, self.fessure, self.luci = VGroup(), VGroup(), VGroup()
        for i in range(4):
            y = -h / 2 + pad + hc / 2 + i * (hc + gap)
            self.cassetti.add(RoundedRectangle(corner_radius=px(0.03 * h), width=px(wc), height=px(hc),
                                               stroke_color=P.secondario, stroke_width=tratto(max(1.5, 3 * k)),
                                               fill_color=P.accento,
                                               fill_opacity=PIENO if i < riempite else 0).move_to(off(0, y)))
            x0 = -wc / 2 + 0.09 * h
            self.fessure.add(Line(off(x0, y), off(x0 + 0.42 * wc, y), stroke_color=P.attenuato,
                                  stroke_width=tratto(max(1.5, 4 * k))))
            self.luci.add(Dot(off(wc / 2 - 0.1 * h, y), radius=px(max(2.5, 0.032 * h)),
                              color=P.accento if i < accese else P.attenuato))
        self.add(self.corpo, self.cassetti, self.fessure, self.luci)

    def fessura(self, i: int) -> np.ndarray:
        return self.fessure[i].get_center()


class Rete(VGroup):
    """La piccola rete neurale (l'IA) appoggiata sul server: tre strati di nodi (3-4-3) e gli archi fra strati
    vicini, niente testo. `base` = (x del centro, y del lato basso, larghezza) in px."""

    def __init__(self, x: float = 175, y_basso: float = 905, larghezza: float = 133, **kw):
        super().__init__(**kw)
        w = larghezza
        r = max(3.0, 0.065 * w)
        passo = 0.26 * w
        h = 3 * passo + 2 * r
        cy = y_basso - h / 2
        strati = []
        for xs, n in ((-0.36 * w, 3), (0.0, 4), (0.36 * w, 3)):
            strati.append([punto(x + xs, cy + (j - (n - 1) / 2) * passo) for j in range(n)])
        self.archi = VGroup(*[Line(a, b, stroke_color=P.attenuato, stroke_width=tratto(max(1.2, 2.5 * w / 133)))
                              for s0, s1 in zip(strati, strati[1:]) for a in s0 for b in s1])
        self.nodi = VGroup(*[Circle(radius=px(r), stroke_width=0, fill_color=P.secondario, fill_opacity=1).move_to(p)
                             for s in strati for p in s])
        self.add(self.archi, self.nodi)


def server_da(t: tuple, accese: int = 4, riempite: int | None = None) -> Server:
    return Server(t[2], t[:2], accese=accese, riempite=riempite)


def rete_da(t: tuple) -> Rete:
    return Rete(*t)


def mescola(a: str, b: str, k: float):
    return interpolate_color(ManimColor(a), ManimColor(b), float(k))


def colora_rete(rete: Rete, k: float, verso: str | None = None) -> None:
    """Nodi e archi dal colore di riposo verso `verso` (accento per l'accensione, attenuato per lo spegnimento)."""
    verso = verso or P.accento
    for n in rete.nodi:
        n.set_fill(mescola(P.secondario, verso, k))
    for e in rete.archi:
        e.set_stroke(mescola(P.attenuato, verso, 0.85 * k))


def illumina(rete: Rete, istanti: list[float], durata_play: float, largo: float = 0.4) -> UpdateFromAlphaFunc:
    """La rete si accende in accento e cresce appena a ogni arrivo (secondi dall'inizio della play), poi si calma."""
    base = rete.copy()

    def f(m, a):
        t = a * durata_play
        k = max([np.sin(np.pi * (t - s) / largo) for s in istanti if 0 <= t - s <= largo] or [0.0])
        m.become(base.copy().scale(1 + 0.1 * k, about_edge=DOWN))
        colora_rete(m, k)

    return UpdateFromAlphaFunc(rete, f, rate_func=linear)


def accendi_luce(luce, t_arrivo: float, durata_play: float) -> UpdateFromAlphaFunc:
    """La lucina del cassetto passa di colpo all'accento quando il chip ci entra."""
    return UpdateFromAlphaFunc(luce, lambda m, a: m.set_fill(P.accento if a * durata_play >= t_arrivo
                                                             else P.attenuato), rate_func=linear)


def riempi_cassetto(cassetto, t_arrivo: float, durata_play: float, lampo: float = 0.35) -> UpdateFromAlphaFunc:
    """Il cassetto si riempie di un velo accento quando il chip ci entra: un lampo più acceso che si calma su
    `PIENO` e ci resta. La lucina da sola (11 px) non si vede; il cassetto pieno sì, anche nel server piccolo."""
    base = cassetto.copy()

    def f(m, a):
        t = a * durata_play
        if t < t_arrivo:
            m.become(base.copy())
            return
        k = max(0.0, 1 - (t - t_arrivo) / lampo)
        m.become(base.copy().set_fill(P.accento, opacity=PIENO + (0.62 - PIENO) * k))

    return UpdateFromAlphaFunc(cassetto, f, rate_func=linear)


def pulsa(mob, istanti: list[float], durata_play: float, ampiezza: float = 0.16, largo: float = 0.26, attorno=None):
    """Un'animazione sola che fa pulsare `mob` una volta per ogni istante (secondi dall'inizio della play): due
    `.animate` sullo stesso oggetto nella stessa play non si sommano. `attorno` = punto fisso della scala (serve per
    le forme il cui centro di ingombro non è il centro vero, come lo spicchio dell'orologio)."""
    base = mob.copy()

    def f(m, a):
        t = a * durata_play
        k = sum(np.sin(np.pi * (t - s) / largo) for s in istanti if 0 <= t - s <= largo)
        c = base.copy()
        m.become(c.scale(1 + ampiezza * k, about_point=attorno) if attorno is not None
                 else c.scale(1 + ampiezza * k))

    return UpdateFromAlphaFunc(mob, f, rate_func=linear)


# --- la scheda video -----------------------------------------------------------------------------------------

class Scheda(VGroup):
    """La scheda video fatta di forme: staffa, pettine, corpo, due ventole, otto alloggi e otto chip (quelli non in
    `pieni` sono trasparenti, così la struttura è sempre la stessa e si passa da uno stato all'altro con Transform)."""

    def __init__(self, scala: float = 1.0, centro=(720, 930), pieni=tuple(range(8)), spenta: bool = False, **kw):
        super().__init__(**kw)
        s = scala
        c = punto(*centro)

        def off(dx, dy):
            return c + np.array([px(dx * s), -px(dy * s), 0.0])

        def tr(n):
            return tratto(max(1.5, n * min(1.0, 0.45 + 0.55 * s)))

        col = P.attenuato if spenta else P.testo
        self.corpo = RoundedRectangle(corner_radius=px(18 * s), width=px(W_S * s), height=px(H_S * s),
                                      stroke_color=col, stroke_width=tr(4), fill_color=P.sfondo, fill_opacity=1)
        self.corpo.move_to(c)
        self.staffa = Rectangle(width=px(14 * s), height=px((H_S + 30) * s), stroke_color=P.attenuato,
                                stroke_width=tr(3), fill_opacity=0).move_to(off(-W_S / 2 - 7, 0))
        self.pettine = Rectangle(width=px(170 * s), height=px(12 * s), stroke_color=P.attenuato, stroke_width=tr(3),
                                 fill_opacity=0).move_to(off(-40, H_S / 2 + 6))
        ventole = []
        for dx in (-92, 92):
            cv = off(dx, 28)
            anello = Circle(radius=px(62 * s), stroke_color=col, stroke_width=tr(4), fill_opacity=0).move_to(cv)
            mozzo = Circle(radius=px(15 * s), stroke_width=0, fill_color=P.attenuato, fill_opacity=1).move_to(cv)
            pale = []
            for k in range(5):
                th = TAU * k / 5 + 0.3
                a = cv + px(17 * s) * np.array([np.cos(th), np.sin(th), 0])
                b = cv + px(54 * s) * np.array([np.cos(th + 0.9), np.sin(th + 0.9), 0])
                pale.append(ArcBetweenPoints(a, b, angle=-0.9, stroke_color=col, stroke_width=tr(3)))
            ventole.append(VGroup(anello, mozzo, *pale))
        self.ventole = VGroup(*ventole)
        self.alloggi = VGroup(*[
            RoundedRectangle(corner_radius=px(4 * s), width=px(32 * s), height=px(24 * s), stroke_color=P.attenuato,
                             stroke_width=tr(3), fill_opacity=0).move_to(off(-154 + 44 * k, -82)) for k in range(8)])
        self.chip = VGroup(*[
            RoundedRectangle(corner_radius=px(4 * s), width=px(32 * s), height=px(24 * s), stroke_width=0,
                             fill_color=P.attenuato if spenta else P.accento,
                             fill_opacity=1 if k in pieni else 0).move_to(off(-154 + 44 * k, -82)) for k in range(8)])
        self.add(self.staffa, self.pettine, self.corpo, self.ventole, self.alloggi, self.chip)

    def riga_chip(self) -> np.ndarray:
        """Il centro della fila degli alloggi (la memoria)."""
        return self.alloggi.get_center()


def volo(chip, tappe_px: list, t0: float, durata: float, durata_play: float, angolo0: float = 0.0,
         cassetto: bool = False, curva=smooth) -> UpdateFromAlphaFunc:
    """Il chip segue un percorso morbido per le tappe (px) fra t0 e t0 + durata (secondi dall'inizio della play);
    con `cassetto` nell'ultimo tratto si schiaccia nella fessura (resta pieno, niente dissolvenza) e all'arrivo
    sparisce di netto: è entrato."""
    percorso = VMobject().set_points_smoothly([punto(*p) for p in tappe_px])
    modello = chip.copy().rotate(-angolo0).move_to(np.zeros(3))
    modello.set_fill(opacity=1)

    def f(m, a):
        t = a * durata_play
        u = curva(min(1.0, max(0.0, (t - t0) / durata)))
        nuovo = modello.copy().rotate(angolo0 * (1 - u))
        if cassetto:
            q = max(0.0, (u - 0.8) / 0.2)
            nuovo.stretch(1 - 0.85 * q, 1)
            if u >= 0.999:
                nuovo.set_fill(opacity=0)
        m.become(nuovo.move_to(percorso.point_from_proportion(u)))

    return UpdateFromAlphaFunc(chip, f, rate_func=linear)


# --- il grafico delle scene 5-6 ------------------------------------------------------------------------------

def etichetta_asse(s: str, colore: str | None = None):
    return testo(s, "etichetta", colore=colore or P.attenuato)


class Grafico:
    """Assi, riga piatta, curva della rata, tratteggiata della corrente, incrocio e aree. Gli stati di fine delle
    scene 5 e 6 si costruiscono da qui, così la scena dopo riparte esattamente da dove era rimasta."""

    def __init__(self):
        a = dict(stroke_color=P.attenuato, stroke_width=tratto(3))
        self.asse_x = Line(punto(X0, Y0), punto(XF + 18, Y0), **a)
        self.asse_y = Line(punto(X0, Y0), punto(X0, Y0 - H1 - 18), **a)
        self.tacche = VGroup(Line(punto(XF, Y0), punto(XF, Y0 + 12), **a),
                             Line(punto(X0 - 12, Y0 - H1), punto(X0, Y0 - H1), **a),
                             Line(punto(X0 - 12, ey(RIGA_E)), punto(X0, ey(RIGA_E)), **a))
        self.tacca_corr = Line(punto(X0 - 12, ey(CORR_E)), punto(X0, ey(CORR_E)), **a)
        self.assi = VGroup(self.asse_x, self.asse_y, self.tacche[0], self.tacche[1])
        self.l0 = colloca(etichetta_asse("0"), X0, Y0 + 14, "c", "t")
        self.l300 = colloca(etichetta_asse("300 h"), XF, Y0 + 14, "c", "t")
        self.l1 = colloca(etichetta_asse("1 €"), X0 - 20, Y0 - H1, "r", "c")
        self.l053 = colloca(etichetta_asse("0,53 €", P.testo), X0 - 20, ey(RIGA_E), "r", "c")
        self.l016 = colloca(etichetta_asse("0,16 €"), X0 - 20, ey(CORR_E), "r", "c")
        self.riga = Line(punto(X0, ey(RIGA_E)), punto(XF, ey(RIGA_E)), stroke_color=P.testo, stroke_width=tratto(6))
        self.fonte_riga = etichetta(testo("RunPod + IVA, set. 2026", "piede", colore=P.attenuato))
        colloca(self.fonte_riga, XF, ey(RIGA_E) - 12, "r", "b")
        self.tratt = DashedLine(punto(X0, ey(CORR_E)), punto(XF, ey(CORR_E)), dash_length=px(16), dashed_ratio=0.55,
                                stroke_color=P.attenuato, stroke_width=tratto(4))
        self.fonte_corr = etichetta(testo("500 W · ARERA", "piede", colore=P.attenuato))
        # sotto il capo destro della tratteggiata: a sinistra ci passerebbe sopra la verticale dell'incrocio
        colloca(self.fonte_corr, XF, ey(CORR_E) + 8, "r", "t")
        self.curva = VMobject(stroke_color=P.accento, stroke_width=tratto(6))
        self.curva.set_points_smoothly([punto(hx(h), ey(RATA / h)) for h in np.linspace(50, 300, 60)])
        self.punti = VGroup(*[Dot(punto(hx(h), ey(RATA / h)), radius=px(10), color=P.accento) for h in (50, 150, 300)])
        xi, yi = hx(H_INCROCIO), ey(RIGA_E)
        self.incrocio = Dot(punto(xi, yi), radius=px(15), color=P.accento)
        self.incrocio.set_stroke(P.sfondo, width=tratto(4))
        self.verticale = Line(punto(xi, yi + 15), punto(xi, Y0), stroke_color=P.accento, stroke_width=tratto(4))
        self.l110 = colloca(testo("110 h", "caption", colore=P.testo, peso=BOLD), xi, Y0 + 20, "c", "t")
        self.cornice110 = RoundedRectangle(corner_radius=px(12), width=self.l110.width + px(28),
                                           height=self.l110.height + px(16), stroke_color=P.accento,
                                           stroke_width=tratto(4), fill_opacity=0).move_to(self.l110)
        self.area_sx = Rectangle(width=px(xi - X0), height=px(H1), stroke_width=0, fill_color=P.secondario,
                                 fill_opacity=0).move_to(punto((X0 + xi) / 2, Y0 - H1 / 2))
        self.area_dx = Rectangle(width=px(XF - xi), height=px(H1), stroke_width=0, fill_color=P.terziario,
                                 fill_opacity=0).move_to(punto((xi + XF) / 2, Y0 - H1 / 2))
        self.db = server_da(SRV5)

    def alzata(self) -> np.ndarray:
        return UP * px(H1 * CORR_E)

    def etichette(self) -> list:
        return [self.l0, self.l300, self.l1, self.l053, self.l016, self.fonte_riga, self.fonte_corr]

    def figura(self) -> list:
        """Tutto ciò che si riduce nella scena 6 (niente testi: sotto i 36 px non si scala)."""
        return [self.area_sx, self.area_dx, self.assi, self.tacche[2], self.tacca_corr, self.tratt, self.riga,
                self.curva, self.punti, self.verticale, self.incrocio, self.db]


FETTA_W, FETTA_H, FETTA_X0, FETTA_X1, FETTA_Y = 6, 76, 235, 557, 1300


def fette_in_fila() -> VGroup:
    """Le 36 fette sottili, una per mese, in fila sotto il grafico, a destra della pila (così la pila si sfoglia
    senza che le fette passino sopra le monete rimaste)."""
    passo = (FETTA_X1 - FETTA_X0) / 35
    return VGroup(*[RoundedRectangle(corner_radius=px(3), width=px(FETTA_W), height=px(FETTA_H), stroke_width=0,
                                     fill_color=P.accento, fill_opacity=1).move_to(punto(FETTA_X0 + passo * k, FETTA_Y))
                    for k in range(36)])


def sfoglia(pezzo, fetta, t0: float, durata: float, durata_play: float) -> UpdateFromAlphaFunc:
    """Una striscia della pila (130 × 3 px, orizzontale) vola al posto della sua fetta ruotando di 90° e cambiando
    misure: un pezzo solo, sempre pieno, mai una forma intermedia fra sagome diverse."""
    p0, p1 = pezzo.get_center().copy(), fetta.get_center().copy()

    def f(m, a):
        u = smooth(min(1.0, max(0.0, (a * durata_play - t0) / durata)))
        w, h = 130 + (FETTA_H - 130) * u, 3 + (FETTA_W - 3) * u
        r = RoundedRectangle(corner_radius=px(min(1.5 + 1.5 * u, h / 2)), width=px(w), height=px(h), stroke_width=0,
                             fill_color=P.accento, fill_opacity=1).rotate(PI / 2 * u)
        m.become(r.move_to(p0 + (p1 - p0) * u))

    return UpdateFromAlphaFunc(pezzo, f, rate_func=linear)


def in_px(p) -> tuple[float, float]:
    """Da un punto di Manim alle coordinate in px della tela (inverso di `punto`)."""
    return ((p[0] + CFG.frame_width / 2) * PX_PER_UNITA, (CFG.frame_height / 2 - p[1]) * PX_PER_UNITA)


def spegni_fetta(f) -> None:
    f.set_fill(P.attenuato, opacity=0.45)


def testi_prezzo(esempio: str = "esempio"):
    """«1.500 €» e accanto, su due righe, l'etichetta «3090 usata» / «esempio» (decisione del presentatore,
    2026-09-22: su una riga sola sarebbe andata sopra la staffa della scheda)."""
    mille = colloca(testo("1.500 €", "messaggio", colore=P.testo, peso=BOLD), 80, 1092, "l", "t")
    es = etichetta(testo(f"3090 usata\n{esempio}", "piede", colore=P.attenuato, interlinea=0.15))
    colloca(es, 80 + w_px(mille) + 24, 1092 + h_px(mille) / 2, "l", "c")
    return mille, es


def orologio():
    c = punto(*OROLOGIO)
    cerchio = Circle(radius=px(R_OROLOGIO), stroke_color=P.testo, stroke_width=tratto(5), fill_opacity=0).move_to(c)
    tacche = VGroup()
    for k in range(24):
        th = PI / 2 - TAU * k / 24
        r0 = R_OROLOGIO - (26 if k % 6 == 0 else 16)
        d = np.array([np.cos(th), np.sin(th), 0])
        tacche.add(Line(c + px(r0) * d, c + px(R_OROLOGIO - 6) * d, stroke_color=P.attenuato,
                        stroke_width=tratto(4 if k % 6 == 0 else 3)))
    return cerchio, tacche


def spicchio(frazione: float = 1.0) -> AnnularSector:
    ang = -TAU * ORE_GIORNO / 24 * max(frazione, 1e-3)
    return AnnularSector(inner_radius=0, outer_radius=px(R_OROLOGIO - 30), angle=ang, start_angle=PI / 2,
                         fill_color=P.accento, fill_opacity=0.9, stroke_width=0).move_arc_center_to(punto(*OROLOGIO))


def etichetta_ore_giorno():
    """«≈ 4 h» sotto l'orologio, centrato."""
    return colloca(testo("≈ 4 h", "messaggio", colore=P.accento, peso=BOLD),
                   OROLOGIO[0], OROLOGIO[1] + R_OROLOGIO + 28, "c", "t")


def calendario(cal: tuple) -> VGroup:
    """Trenta quadratini in righe da 7 (4 righe piene e 2 giorni): si legge come un mese."""
    x0, y0, lato, passo = cal
    return VGroup(*[RoundedRectangle(corner_radius=px(lato * 0.2), width=px(lato), height=px(lato),
                                     stroke_color=P.attenuato, stroke_width=tratto(3 if lato > 24 else 2),
                                     fill_color=P.accento, fill_opacity=0)
                    .move_to(punto(x0 + lato / 2 + passo * (k % 7), y0 + lato / 2 + passo * (k // 7)))
                    for k in range(30)])


def etichetta_mese(q: VGroup):
    """«30 gg» piccolo sotto il calendario, allineato a destra."""
    et = etichetta(testo("30 gg", "piede", colore=P.attenuato))
    return colloca(et, in_px(q.get_right())[0], in_px(q.get_bottom())[1] + 14, "r", "t")


def entra_e_accendi(q, entra: tuple, accendi: tuple, durata_play: float) -> UpdateFromAlphaFunc:
    """Un giorno del calendario: entra vuoto (bordo grigio) nella finestra `entra`, si accende pieno in accento nella
    finestra `accendi` (secondi dall'inizio della play). Un'animazione sola: due sullo stesso oggetto non si sommano."""
    base = q.copy()

    def f(m, a):
        t = a * durata_play
        u = smooth(min(1.0, max(0.0, (t - entra[0]) / (entra[1] - entra[0]))))
        k = ease_out_cubic(min(1.0, max(0.0, (t - accendi[0]) / (accendi[1] - accendi[0]))))
        m.become(base.copy())
        m.set_stroke(P.accento if k >= 1 else mescola(P.attenuato, P.accento, k), opacity=u)
        m.set_fill(P.accento, opacity=k * u)

    return UpdateFromAlphaFunc(q, f, rate_func=linear)


def accendi_giorno(g):
    return g.set_fill(P.accento, opacity=1).set_stroke(P.accento)


# --- la scena 3: fabbrica, moduli di memoria, rastrelliera d'uscita --------------------------------------------

def fabbrica() -> Icona:
    """La fabbrica della memoria (Icona `factory`), in alto al centro della scena 3."""
    return Icona("factory", altezza_px=FAB3_H, colore=P.testo).move_to(punto(*FAB3))


def fabbrica_nuova() -> VGroup:
    """La fabbrica in costruzione: la stessa icona, solo tratteggiata e attenuata (i puntini dell'icona restano
    fuori: tratteggiati diventerebbero macchie)."""
    base = Icona("factory", altezza_px=FAB3_H, colore=P.attenuato).move_to(punto(*FAB3_NUOVA))
    pezzi = [m for m in base.svg.family_members_with_points() if m.get_arc_length() > px(30)]
    return VGroup(*[DashedVMobject(m.copy(), num_dashes=max(5, int(m.get_arc_length() / px(46))), dashed_ratio=0.5)
                    for m in pezzi])


def modulo() -> Icona:
    """Un modulo di memoria (Icona `memory-stick`): grande, in accento, una stecca riconoscibile."""
    m = Icona("memory-stick", altezza_px=MODULO_H, colore=P.accento)
    m.set_z_index(3)
    return m


def posto_xy(k: int) -> tuple[float, float]:
    """Il centro del posto k della rastrelliera (due file da quattro)."""
    return (RAST_C[0] + (k % 4 - 1.5) * RAST_PASSO[0], RAST_C[1] + (k // 4 - 0.5) * RAST_PASSO[1])


def posti() -> VGroup:
    """Gli otto posti tratteggiati, «in attesa di memoria»: niente ripiani, niente numeri."""
    return VGroup(*[DashedVMobject(RoundedRectangle(corner_radius=px(8), width=px(POSTO_W), height=px(POSTO_H),
                                                    stroke_color=P.attenuato, stroke_width=tratto(2.5)),
                                   num_dashes=26, dashed_ratio=0.55).move_to(punto(*posto_xy(k)))
                    for k in range(8)])


def rastrelliera():
    """La rastrelliera come è a fine beat 2: gli otto posti e le due schede nei primi due (niente cartellino né
    freccia: il presentatore, 2026-09-23). Stessi pezzi nella scena e nello stato di fine."""
    return posti(), [Scheda(S_POSTO, posto_xy(k)) for k in (0, 1)]


def in_fondo_rastrelliera(pezzi) -> None:
    """Porta i pezzi dove stanno a fine scena 3: la rastrelliera al centro, più grande."""
    VGroup(*pezzi).scale(RAST_SCALA, about_point=punto(*RAST_C)).shift(punto(*RAST_FINE) - punto(*RAST_C))


def sforna(m, tappe_px: list, t0: float, durata: float, durata_play: float, esce: float = 0.25,
           dentro: bool = False, poi=None) -> UpdateFromAlphaFunc:
    """Il modulo esce dalla fabbrica (cresce da 0,4 e si accende in `esce` secondi) e segue le tappe fra t0 e
    t0 + durata. Con `dentro` nell'ultimo tratto si schiaccia nella fessura del cassetto e sparisce di netto.
    `poi` = (punto, t1, durata1): arrivato al posto, scivola sulla fila della memoria della scheda che nasce lì,
    si schiaccia e si spegne (diventa la memoria della scheda). Prima di t0 è trasparente: niente puntini."""
    base = m.copy().move_to(ORIGIN)
    percorso = VMobject().set_points_smoothly([punto(*p) for p in tappe_px])

    def f(mob, a):
        t = a * durata_play
        if t < t0:
            mob.become(base.copy().scale(0.4).move_to(percorso.get_start()).set_stroke(opacity=0))
            return
        u = smooth(min(1.0, (t - t0) / durata))
        e = ease_out_cubic(min(1.0, (t - t0) / esce))
        n = base.copy().scale(0.4 + 0.6 * e)
        o = min(1.0, (t - t0) / esce)
        c = percorso.point_from_proportion(u)
        if dentro:
            q = max(0.0, (u - 0.82) / 0.18)
            n.stretch(1 - 0.85 * q, 1)
            if u >= 0.999:
                o = 0.0
        if poi is not None and t >= poi[1]:
            v = smooth(min(1.0, (t - poi[1]) / poi[2]))
            n.stretch(1 - 0.12 * v, 0).stretch(1 - 0.8 * v, 1)
            c = c + (poi[0] - c) * v
            o = 1.0 - max(0.0, (v - 0.6) / 0.4)
        mob.become(n.move_to(c).set_stroke(opacity=o))

    return UpdateFromAlphaFunc(m, f, rate_func=linear)


def pulsa_posti(vuoti: VGroup, istanti: list[float], durata_play: float, ampiezza: float = 0.1,
                largo: float = 0.32) -> UpdateFromAlphaFunc:
    """I posti vuoti pulsano insieme, ognuno attorno al suo centro, e a ogni battito il tratteggio si schiarisce:
    sono le schede che mancano per la vendita."""
    base = vuoti.copy()
    w0 = tratto(2.5)

    def f(m, a):
        t = a * durata_play
        k = sum(np.sin(np.pi * (t - s) / largo) for s in istanti if 0 <= t - s <= largo)
        for dst, src in zip(m, base):
            dst.become(src.copy().scale(1 + ampiezza * k)
                       .set_stroke(mescola(P.attenuato, P.testo, k), width=w0 * (1 + 0.9 * k)))

    return UpdateFromAlphaFunc(vuoti, f, rate_func=linear)


# --- stati di fine -------------------------------------------------------------------------------------------

def fine_3(sc: ScenaReel):
    """L'ultimo fotogramma della scena 3: la rastrelliera al centro, più grande (due schede, sei posti in attesa), il
    «?» accanto; in alto a sinistra, piccoli, il server pieno e la rete."""
    ps, schede = rastrelliera()
    in_fondo_rastrelliera([ps, *schede])
    q = colloca(testo("?", "punch", colore=P.accento, peso=BOLD), *Q3)
    server, rete = server_da(SRV3_FINE), rete_da(RETE3_FINE)
    sc.add(server, rete, ps, *schede, q)
    return schede[1], q, server, rete, [ps, schede[0]]


def fine_5(sc: ScenaReel):
    """L'ultimo fotogramma della scena 5: assi, riga piatta, curva della rata con i tre punti, la scheda in basso a
    destra con gli alloggi pieni, «1.500 €», «esempio» e le 36 fette spente."""
    g = Grafico()
    scheda = Scheda(SCALA5, C5)
    mille, es = testi_prezzo()
    fette = fette_in_fila()
    for f in fette:
        spegni_fetta(f)
    sc.add(g.assi, g.tacche[2], g.riga, g.l0, g.l300, g.l1, g.l053, g.fonte_riga, g.db, g.curva, g.punti,
           scheda, mille, es, fette)
    return g, scheda, mille, es, fette


def fine_6(sc: ScenaReel):
    """L'ultimo fotogramma della scena 6: il grafico ridotto in alto a sinistra (curva alzata, incrocio, aree con
    il server e la scheda piccoli), «110 h» incorniciato, l'orologio con lo spicchio e sotto «≈ 4 h», a destra il
    calendario del mese acceso con «30 gg»."""
    g = Grafico()
    g.curva.shift(g.alzata())
    g.punti.shift(g.alzata())
    g.area_sx.set_fill(opacity=0.16)
    g.area_dx.set_fill(opacity=0.16)
    g.db = server_da(SRV6)
    piccola = Scheda(SCALA6, C6_PICCOLA)
    grafico = VGroup(*g.figura()[:-1], g.db, piccola)
    grafico.scale(PICCOLO, about_point=punto(*ANCORA_PICCOLO)).shift(punto(*META_PICCOLO) - punto(*ANCORA_PICCOLO))
    tag = VGroup(g.cornice110, g.l110)
    colloca(tag, META_PICCOLO[0] + (XF + 18 - X0) * PICCOLO + 40, META_PICCOLO[1] + H1 * PICCOLO / 2, "l", "c")
    cerchio, tacche = orologio()
    fetta = spicchio()
    ore = etichetta_ore_giorno()
    gg = calendario(CAL6)
    for x in gg:
        accendi_giorno(x)
    mese = etichetta_mese(gg)
    g.area_sx.set_z_index(-1)
    g.area_dx.set_z_index(-1)
    sc.add(grafico, tag, cerchio, tacche, fetta, ore, gg, mese)
    return g, piccola, grafico, tag, VGroup(cerchio, tacche, fetta), ore, gg, mese


# --- scene ---------------------------------------------------------------------------------------------------

class Scena03(ScenaReel):
    """Cinque beat. La fabbrica della memoria pulsa (b0); sforna i moduli uno dopo l'altro e vanno tutti al server
    con la rete: cassetto pieno, lucina, la rete pulsa (b1); solo adesso due moduli prendono il filo verso la
    rastrelliera d'uscita della produzione, la camera entra, diventano due schede, sei posti restano in attesa e
    pulsano insieme (b2); la fabbrica nuova tratteggiata e la linea del tempo che sbatte
    sul 2028 (b3); la rastrelliera al centro, grande, e il «?» (b4)."""

    def costruisci(self):
        testi = self.scena.get("testo") or ["TrendForce, 2026"]
        assert testi[0] == "TrendForce, 2026", "TESTO: della scena 3 cambiato: aggiorna la didascalia"
        fab = fabbrica()
        server = server_da(SRV3, accese=0, riempite=0)
        rete = rete_da(RETE3)
        ps = posti()
        via_rast = Line(punto(FAB3[0], FAB3[1] + FAB3_H / 2 + 6), punto(RAST_C[0], RAST_C[1] - RAST_PASSO[1] / 2
                                                                           - POSTO_H / 2 - 6),
                        stroke_color=P.attenuato, stroke_width=tratto(2.5))
        self.add(server, rete, fab, via_rast, ps)          # fotogramma 0 già pieno (dopo il filmato)

        # beat 0 · «E non è solo impressione.» — la fabbrica pulsa una volta
        self.wait(0.1)
        self.play(fab.animate(rate_func=there_and_back).scale(1.1), run_time=self.arrotonda(0.45))

        # beat 1 · «C'entra la memoria, che in questo momento viene mandata prima all'intelligenza artificiale,»
        # la fabbrica sforna i moduli uno dopo l'altro e vanno tutti al server, uno per cassetto: la priorità è un
        # ordine (i primi vanno lì). A ogni arrivo il cassetto si riempie, la lucina si accende, la rete pulsa
        self.beat(1)
        T = self.arrotonda(4.8)
        mods = [modulo() for _ in range(4)]
        partenze, d_volo = [0.15 + 1.0 * i for i in range(4)], 1.25
        anims, arrivi = [], []
        uscita = (FAB3[0] - 30, FAB3[1] + 50)
        for i, m in enumerate(mods):
            m.move_to(punto(*uscita))
            xf, yf = in_px(server.cassetti[i].get_center())
            tappe = [uscita, (470, 818), (305, 868), (292, yf), (xf, yf)]
            anims.append(sforna(m, tappe, partenze[i], d_volo, T, dentro=True))
            arrivi.append(partenze[i] + d_volo)
        anims.append(illumina(rete, arrivi, T))
        anims += [accendi_luce(server.luci[i], arrivi[i], T) for i in range(4)]
        anims += [riempi_cassetto(server.cassetti[i], arrivi[i], T) for i in range(4)]
        self.play(*anims, run_time=T)
        self.remove(*mods)

        # beat 2 · «e quindi sulle schede ne resta meno.»
        # GRANDE (contrasto di scala): solo adesso due moduli prendono il filo verso la rastrelliera mentre la camera
        # entra; ognuno diventa una scheda piccola (si schiaccia sulla sua fila della memoria), sei posti restano in
        # attesa e pulsano insieme su «ne resta meno»: sono le schede che mancano. Poi la camera torna
        self.beat(2)
        inizio = self.t
        _, schede = rastrelliera()
        rast = VGroup(ps, *schede)
        # lo zoom (1,4×) non porta la rastrelliera al centro dell'area ma a sinistra e un po' in basso (centro a 440,
        # 1040 px dello schermo): così la fabbrica, ingrandita sopra di lei, resta fuori dal riquadro del presentatore
        ZOOM3 = 1.4
        controlla_zoom(self, [rast], ZOOM3)
        larghezza = self.cfg.frame_width / ZOOM3
        centro = punto(*RAST_C) - punto(440, 1040) / ZOOM3
        T2 = self.arrotonda(1.0)
        mods = [modulo().scale(0.88) for _ in range(2)]      # un filo più stretti: stanno nel posto
        anims = []
        for j, m in enumerate(mods):
            xk, yk = posto_xy(j)
            partenza = (FAB3[0], FAB3[1] + 40)
            m.move_to(punto(*partenza))
            tappe = [partenza, (FAB3[0], RAST_C[1] - RAST_PASSO[1] / 2 - POSTO_H / 2 - 30), (xk, yk)]
            anims.append(sforna(m, tappe, 0.12 * j, 0.55, T2, esce=0.18,
                                poi=(schede[j].riga_chip(), 0.7, 0.26)))
        anims += [FadeIn(s, scale=0.6, rate_func=fra(0.68, 0.95, ease_out_cubic)) for s in schede]
        anims.append(self.camera.frame.animate(rate_func=fra(0, 0.6, ease_out_cubic)).set(width=larghezza)
                     .move_to(centro))
        self.play(*anims, run_time=T2)
        self.remove(*mods)
        # i sei posti vuoti pulsano insieme, due volte: «ne resta meno»
        vuoti = VGroup(*ps[2:])
        T_P = self.arrotonda(0.7)
        self.play(pulsa_posti(vuoti, [0.0, 0.34], T_P), run_time=T_P)
        self.play(self.camera.frame.animate(rate_func=smooth).set(width=self.cfg.frame_width).move_to(ORIGIN),
                  run_time=self.arrotonda(0.45))

        # beat 3 · «E le fabbriche nuove, secondo TrendForce, conteranno solo dal duemilaventotto.»
        self.beat(3)
        inizio = self.t
        nuova = fabbrica_nuova()
        linea = Line(punto(90, Y_TEMPO), punto(940, Y_TEMPO), stroke_color=P.attenuato, stroke_width=tratto(4))
        sbarra = Line(punto(X_SBARRA, Y_TEMPO - 45), punto(X_SBARRA, Y_TEMPO + 45), stroke_color=P.accento,
                      stroke_width=tratto(9))
        segno = Dot(punto(104, Y_TEMPO), radius=px(15), color=P.accento)
        anno = testo("2028", "messaggio", colore=P.testo, peso=BOLD)
        x_anno = min(X_SBARRA, 955 - w_px(anno) / 2)
        colloca(anno, x_anno, Y_TEMPO - 52, "c", "b")
        # la fonte a 40 px (ruolo `etichetta`, non `piede`): con la virgola il `piede` misura 35 px d'inchiostro
        fonte = etichetta(testo(testi[0], "etichetta", colore=P.attenuato))
        colloca(fonte, X_SBARRA - 26, Y_TEMPO + 20, "r", "t")
        filo = DashedLine(punto(X_SBARRA, FAB3_NUOVA[1] + FAB3_H / 2 + 8), punto(X_SBARRA, in_px(anno.get_top())[1] - 14),
                          dash_length=px(12), dashed_ratio=0.5, stroke_color=P.attenuato, stroke_width=tratto(3))
        # (niente Create a finestra: a progresso zero un tratto a capi tondi si vede come un puntino)
        self.play(FadeIn(nuova, scale=0.85, rate_func=ease_out_cubic), run_time=self.arrotonda(0.45))
        self.play(Create(linea, rate_func=fra(0, 0.7)), FadeIn(sbarra, scale=0.5, rate_func=fra(0.45, 0.85)),
                  FadeIn(segno, scale=0.4, rate_func=fra(0.6, 1)), run_time=self.arrotonda(0.6))
        self.attendi_fino(inizio + 1.45)                                        # «secondo TrendForce»
        self.play(FadeIn(fonte, shift=UP * px(8)), run_time=self.arrotonda(0.4))
        # il segno parte su «conteranno» e sbatte contro la sbarra su «duemilaventotto»
        self.attendi_fino(inizio + 2.55)
        self.play(segno.animate(rate_func=ease_in_quad).move_to(punto(X_SBARRA - 20, Y_TEMPO)),
                  run_time=self.arrotonda(1.4))
        self.play(sbarra.animate(rate_func=there_and_back).shift(RIGHT * px(10)),
                  segno.animate(rate_func=there_and_back).stretch(0.6, 0),
                  FadeIn(anno, scale=0.4, rate_func=ease_out_back), run_time=self.arrotonda(0.4))
        # la fabbrica nuova è legata al 2028: il filo scende da lei fino all'anno
        self.play(Create(filo), run_time=self.arrotonda(0.45))

        # beat 4 · «Quindi ti conviene davvero ==comprarla==?»
        # escono la linea del tempo e le fabbriche; server e rete si fanno piccoli in alto a sinistra; la rastrelliera
        # scivola al centro e cresce (due schede, sei posti in attesa); poi il «?»
        self.beat(4)
        inizio = self.t
        q = colloca(testo("?", "punch", colore=P.accento, peso=BOLD), *Q3)
        meta = rast.copy()
        in_fondo_rastrelliera([meta])
        uscite = [anno, fonte, segno, sbarra, linea, filo, nuova, fab, via_rast]
        self.play(*[FadeOut(m, rate_func=fra(0, 0.35)) for m in uscite],
                  Transform(server, server_da(SRV3_FINE), rate_func=fra(0.1, 0.55, ease_out_cubic)),
                  Transform(rete, rete_da(RETE3_FINE), rate_func=fra(0.1, 0.55, ease_out_cubic)),
                  Transform(rast, meta, rate_func=fra(0.4, 1, ease_out_cubic)), run_time=self.arrotonda(1.0))
        self.play(FadeIn(q, scale=0.4, rate_func=ease_out_back), run_time=self.arrotonda(0.4))   # «davvero»
        self.attendi_fino(inizio + 1.55)                                        # «comprarla?»
        self.play(q.animate(rate_func=there_and_back).scale(1.18), run_time=self.arrotonda(0.45))


def spegni_rete(rete: Rete) -> UpdateFromAlphaFunc:
    """La rete si spegne a grigio, poi rientra nel server rimpicciolendo e sparisce."""
    base = rete.copy()

    def f(m, a):
        spento = min(1.0, a / 0.5)
        via = max(0.0, (a - 0.5) / 0.5)
        m.become(base.copy().scale(1 - 0.6 * via, about_edge=DOWN))
        colora_rete(m, spento, P.attenuato)
        for n in m.nodi:
            n.set_fill(opacity=1 - via)
        for e in m.archi:
            e.set_stroke(opacity=1 - via)

    return UpdateFromAlphaFunc(rete, f, rate_func=linear)


class Scena05(ScenaReel):
    """Cinque beat. La rete si spegne ed esce, il server resta (è il noleggio), si disegnano gli assi (b0); la riga
    piatta cade dal server, «0,53 €», la fonte, e su «sempre quello» pulsa: poi non si muove più (b1); la scheda pulsa e la
    pila di monete, «1.500 €» (b2); la pila si sfoglia in 36 fette (b3); una fetta si sbriciola sulle ore e i punti
    disegnano la curva che scende (b4)."""

    def costruisci(self):
        testi = self.scena.get("testo") or ["esempio"]
        assert testi[0] == "esempio", "TESTO: della scena 5 cambiato: aggiorna l'etichetta"
        scheda, q, server, rete, resto = fine_3(self)    # fotogramma 0 = ultimo della scena 3
        g = Grafico()

        # beat 0 · «Qui è uguale.» (meno di un secondo): la rete si spegne ed esce, il server resta ed è il noleggio;
        # la scheda scende piccola in basso a destra, si disegnano gli assi
        # (la rastrelliera della 3 si svuota: resta la seconda scheda, che scende al suo posto)
        self.play(FadeOut(q, rate_func=fra(0, 0.3)), *[FadeOut(m, rate_func=fra(0, 0.3)) for m in resto],
                  spegni_rete(rete).set_rate_func(fra(0, 0.45, linear)),
                  Transform(server, server_da(SRV5), rate_func=fra(0.4, 0.95, ease_out_cubic)),
                  Transform(scheda, Scheda(SCALA5, C5), rate_func=fra(0.15, 0.8, ease_out_cubic)),
                  Create(g.assi, rate_func=fra(0.35, 0.9)),         # quando posti e «?» sono già usciti
                  *[FadeIn(m, rate_func=fra(0.75, 1)) for m in (g.l0, g.l300, g.l1)], run_time=self.arrotonda(0.8))
        self.remove(rete)

        # beat 1 · «Se affitti, sei attorno a mezzo euro l'ora, tasse comprese, e sempre quello.»
        # (tempi misurati sulla voce di prova: «mezzo euro» ~1,6 s, «tasse comprese» ~2,8 s, «sempre» ~4,05 s)
        # la riga cade dal server e si allunga per tutto il grafico: da qui in poi non si muove né si ridisegna
        # (richiesta del revisore, 2026-09-22: il noleggio costa uguale a ogni ora)
        self.beat(1)
        inizio = self.t
        x_s = SRV5[0]
        y_c = SRV5[1] + SRV5[2] / 2 + 9
        corta = Line(punto(x_s - 28, y_c), punto(x_s + 28, y_c), stroke_color=P.testo, stroke_width=tratto(6))
        self.attendi_fino(inizio + 0.3)                                                    # «affitti»
        self.play(FadeIn(corta, shift=DOWN * px(20)), run_time=self.arrotonda(0.2))
        self.play(corta.animate(rate_func=rush_into).move_to(punto(x_s, ey(RIGA_E))), run_time=self.arrotonda(0.4))
        self.play(Transform(corta, g.riga, rate_func=ease_out_cubic), Create(g.tacche[2], rate_func=fra(0.5, 1)),
                  run_time=self.arrotonda(0.8))
        self.remove(corta)
        self.add(g.riga)
        self.attendi_fino(inizio + 1.7)                                                    # «mezzo euro»
        self.play(FadeIn(g.l053, shift=RIGHT * px(10)), run_time=self.arrotonda(0.4))
        self.attendi_fino(inizio + 2.8)                                                    # «tasse comprese»
        self.play(FadeIn(g.fonte_riga, shift=UP * px(8)), run_time=self.arrotonda(0.4))
        self.attendi_fino(inizio + 4.05)                                                   # «sempre quello»
        w0 = g.riga.get_stroke_width()
        self.play(UpdateFromAlphaFunc(g.riga, lambda m, a: m.set_stroke(width=w0 * (1 + 1.3 * np.sin(np.pi * a))),
                                      rate_func=linear), run_time=self.arrotonda(0.5))
        g.riga.set_stroke(width=w0)

        # beat 2 · «Se compri, mettiamo millecinquecento euro tra scheda e computer,»
        self.beat(2)
        inizio = self.t
        fette = fette_in_fila()
        pila = VGroup()
        for m in range(9):                            # nove monete, quattro strisce ciascuna (= le 36 fette)
            dx = (4, -3, 5, -4, 2, -5, 3, -2, 4)[m]
            for s in range(4):
                pila.add(RoundedRectangle(corner_radius=px(1.5), width=px(130), height=px(3), stroke_width=0,
                                          fill_color=P.accento, fill_opacity=1)
                         .move_to(punto(145 + dx, 1340 - 17 * m - 4 * s - 1.5)))
        mille, es = testi_prezzo(testi[0])
        monete = [VGroup(*pila[4 * m:4 * m + 4]) for m in range(9)]
        self.attendi_fino(inizio + 0.15)                                                     # «Se compri»
        self.play(scheda.animate(rate_func=there_and_back).scale(1.06), run_time=self.arrotonda(0.4))
        # il mucchio non arriva già fatto: sette monete per la scheda, le ultime due per il computer
        self.attendi_fino(inizio + 1.25)                                                     # «millecinquecento euro»
        self.play(*[FadeIn(mo, shift=DOWN * px(50), rate_func=fra(0.09 * m, 0.09 * m + 0.35, ease_out_cubic))
                    for m, mo in enumerate(monete[:7])],
                  FadeIn(mille, shift=UP * px(10), rate_func=fra(0.62, 0.9)), run_time=self.arrotonda(1.5))
        self.attendi_fino(inizio + 2.85)                                                     # «tra scheda»
        self.play(FadeIn(es, shift=RIGHT * px(10)), run_time=self.arrotonda(0.4))
        self.attendi_fino(inizio + 3.3)                                                      # «e computer»
        self.play(*[FadeIn(mo, shift=DOWN * px(40), rate_func=fra(0.3 * m, 0.3 * m + 0.55, ease_out_cubic))
                    for m, mo in enumerate(monete[7:])], run_time=self.arrotonda(0.6))

        # beat 3 · «spalmati su tre anni.»
        # GRANDE (metamorfosi): la pila si sfoglia dall'alto, ogni striscia vola al suo posto nella fila e ruota in
        # piedi: 36 fette sottili, una per mese
        self.beat(3)
        T_M, d = self.arrotonda(1.0), 0.3
        self.play(*[sfoglia(pila[j], fette[j], (35 - j) * (T_M - d) / 35, d, T_M) for j in range(36)], run_time=T_M)
        quarantadue = colloca(testo("42 €", "caption", colore=P.accento, peso=BOLD), FETTA_X1 + 4, 1250, "r", "b")
        self.play(*[pila[j].animate.set_fill(P.attenuato, opacity=0.45) for j in range(35)],
                  FadeIn(quarantadue, shift=UP * px(8), rate_func=fra(0.3, 1)), run_time=self.arrotonda(0.4))

        # beat 4 · «Quella rata poi la dividi per le ore che fai ==davvero==.»
        self.beat(4)
        fetta = pila[35].copy()
        self.add(fetta)
        # la fetta sale nel varco fra l'etichetta e la scheda, senza passare sopra i testi
        x_f, y_f = in_px(pila[35].get_center())
        x_v = (in_px(es.get_right())[0] + in_px(scheda.staffa.get_left())[0]) / 2
        T_V = self.arrotonda(0.7)
        self.play(FadeOut(quarantadue, rate_func=fra(0, 0.3)),
                  volo(fetta, [(x_f, y_f), (x_v, y_f - 20), (x_v, 1090), (hx(25), Y0 - 60)], 0.21, 0.49, T_V,
                       curva=smooth),
                  pila[35].animate(rate_func=fra(0.4, 0.7)).set_fill(P.attenuato, opacity=0.45), run_time=T_V)
        # la fetta si sbriciola sulle ore: pochi pezzi grossi a 50 h, più piccoli a 150, briciole a 300
        n = 24

        def stato(gruppi: int, ore: float, lato: float) -> VGroup:
            v = VGroup()
            for j in range(n):
                k = j * gruppi // n
                v.add(Rectangle(width=px(lato), height=px(lato), stroke_width=0, fill_color=P.accento,
                                fill_opacity=1).move_to(punto(hx(ore * (k + 0.5) / gruppi), Y0 - lato / 2 - 4)))
            return v

        pezzi = VGroup(*[Rectangle(width=px(FETTA_W), height=px(FETTA_H / n), stroke_width=0, fill_color=P.accento,
                                   fill_opacity=1).move_to(fetta.get_top() + DOWN * px(FETTA_H / n * (j + 0.5)))
                         for j in range(n)])
        self.remove(fetta)
        self.add(pezzi)
        for (gruppi, ore, lato), pt in zip(((4, 50, 22), (8, 150, 13), (24, 300, 7)), g.punti):
            self.play(Transform(pezzi, stato(gruppi, ore, lato), rate_func=fra(0, 0.75, ease_out_cubic)),
                      FadeIn(pt, scale=0.3, rate_func=fra(0.5, 1, ease_out_back)), run_time=self.arrotonda(0.4))
        self.play(Create(g.curva), FadeOut(pezzi, rate_func=fra(0.3, 1)), run_time=self.arrotonda(0.6))


class Scena06(ScenaReel):
    """Tre beat. La corrente alza la curva (resta un attimo l'ombra grigia della vecchia, con due frecce) (b0);
    l'incrocio si accende e nasce «110 h», poi le due aree dicono chi conviene (b1); il grafico si fa piccolo,
    l'orologio del giorno si riempie per quasi quattro ore e, dopo, il mese (calendario a righe da 7, «30 gg») si
    accende tutto e lo spicchio pulsa: ogni giorno (b2)."""

    def costruisci(self):
        testi = self.scena.get("testo") or ["110 h"]
        assert testi[0] == "110 h", "TESTO: della scena 6 cambiato: aggiorna l'etichetta dell'incrocio"
        g, scheda, mille, es, fette = fine_5(self)        # fotogramma 0 = ultimo della scena 5

        # beat 0 · «Solo che a casa ci aggiungi anche la corrente, ogni ora.»
        self.attendi_fino(0.95)                                                            # «ci aggiungi»
        self.play(Create(g.tratt, rate_func=fra(0, 0.85)), Create(g.tacca_corr, rate_func=fra(0.6, 1)),
                  FadeIn(g.l016, rate_func=fra(0.6, 1)), FadeIn(g.fonte_corr, rate_func=fra(0.7, 1)),
                  run_time=self.arrotonda(0.75))
        # la curva sale tutta insieme: l'alzata è solo 54 px (0,158 € × 340 px/€), quindi **prima** crescono le due
        # frecce che dicono di quanto, poi la curva si stacca dalla sua ombra grigia in 1,1 s con un piccolo
        # rimbalzo, e l'ombra resta come «prima» fino all'inizio del beat 1
        self.attendi_fino(1.8)                                                             # «la corrente, ogni ora»
        ombra = g.curva.copy().set_stroke(P.attenuato, width=tratto(4))
        self.add(ombra)
        self.bring_to_front(g.curva, g.punti)
        frecce = VGroup()
        for h in (50, 150):        # due sole frecce: a 300 h la freccia finirebbe sopra «500 W · ARERA»
            x = hx(h) + 24
            frecce.add(Arrow(punto(x, ey(RATA / h) + 4), punto(x, ey(RATA / h + CORR_E) - 2), buff=0,
                             stroke_width=tratto(5), color=P.testo, tip_length=px(18),
                             max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=20))
        self.play(*[GrowArrow(f, rate_func=fra(0.02 + 0.06 * i, 0.3 + 0.06 * i)) for i, f in enumerate(frecce)],
                  g.curva.animate(rate_func=fra(0.2, 0.95, rimbalzo(0.15))).shift(g.alzata()),
                  g.punti.animate(rate_func=fra(0.2, 0.95, rimbalzo(0.15))).shift(g.alzata()),
                  run_time=self.arrotonda(1.2))

        # beat 1 · «E con i prezzi di oggi le due curve si incontrano attorno a ==centodieci== ore al mese,»
        self.beat(1)
        inizio, durata = self.t, self.durata_beat(1)
        anello = Circle(radius=px(18), stroke_color=P.accento, stroke_width=tratto(5), fill_opacity=0)
        anello.move_to(g.incrocio)
        # «1.500 €» e l'etichetta escono subito («110 h» nasce appena sopra di loro), e con loro se ne vanno
        # l'ombra della curva vecchia e le frecce: hanno fatto il loro lavoro per quasi due secondi
        self.play(FadeOut(mille), FadeOut(es), FadeOut(ombra), *[FadeOut(f) for f in frecce],
                  run_time=self.arrotonda(0.3))
        # «con i prezzi di oggi»: i due prezzi del conto si fanno notare, uno dopo l'altro
        self.attendi_fino(inizio + 0.45)
        self.play(g.l053.animate(rate_func=fra(0, 0.55, there_and_back)).scale(1.18),
                  g.l016.animate(rate_func=fra(0.45, 1, there_and_back)).scale(1.18), run_time=self.arrotonda(0.9))
        # «si incontrano»: l'incrocio si accende
        self.attendi_fino(inizio + 1.85)
        self.add(anello)
        self.play(FadeIn(g.incrocio, scale=0.2, rate_func=ease_out_back),
                  anello.animate(rate_func=ease_out_cubic).scale(2.4).set_stroke(opacity=0),
                  run_time=self.arrotonda(0.55))
        self.remove(anello)
        # GRANDE (rivelazione a tratto) su «centodieci ore al mese»: la verticale scende all'asse, nasce «110 h», il
        # tratto gli corre intorno, e subito dopo le due aree dicono chi conviene
        for a_ in (g.area_sx, g.area_dx):
            a_.set_z_index(-1)
        self.add(g.area_sx, g.area_dx)
        piccola = Scheda(SCALA6, C6_PICCOLA)
        self.attendi_fino(inizio + 3.05)                                  # «centodieci»
        self.play(Create(g.verticale, rate_func=fra(0, 0.24, ease_in_quad)),
                  FadeIn(g.l110, shift=UP * px(10), rate_func=fra(0.24, 0.44)),
                  Create(g.cornice110, rate_func=fra(0.44, 0.66)),
                  *[FadeOut(f, rate_func=fra(0.6, 0.78)) for f in fette],
                  FadeOut(scheda, rate_func=fra(0.6, 0.8)),
                  g.area_sx.animate(rate_func=fra(0.7, 1)).set_fill(opacity=0.16),
                  g.area_dx.animate(rate_func=fra(0.7, 1)).set_fill(opacity=0.16),
                  Transform(g.db, server_da(SRV6), rate_func=fra(0.7, 1)),
                  FadeIn(piccola, scale=0.5, rate_func=fra(0.82, 1, ease_out_cubic)), run_time=self.arrotonda(1.2))

        # beat 2 · «cioè quasi quattro ore al giorno.» — un passaggio solo, a finestre che non si accavallano: le
        # etichette escono, il grafico si fa piccolo in alto, l'orologio si disegna e accanto il mese (vuoto); lo
        # spicchio si riempie per quasi quattro ore su ventiquattro, «≈ 4 h»; **dopo** si accendono i trenta giorni
        # (condizione del revisore, 2026-09-23: un calendario, righe da 7, e resta fino a fine scena) e lo spicchio
        # pulsa: ogni giorno
        self.beat(2)
        grafico = VGroup(*g.figura()[:-1], g.db, piccola)
        tag = VGroup(g.cornice110, g.l110)
        meta_tag = tag.copy()
        colloca(meta_tag, META_PICCOLO[0] + (XF + 18 - X0) * PICCOLO + 40, META_PICCOLO[1] + H1 * PICCOLO / 2,
                "l", "c")
        via = [g.l0, g.l300, g.l1, g.l053, g.l016, g.fonte_riga, g.fonte_corr]
        cerchio, tacche = orologio()
        fetta = spicchio(0.001)
        self.add(fetta)
        ore = etichetta_ore_giorno()
        gg = calendario(CAL6)
        mese = etichetta_mese(gg)
        T = self.arrotonda(2.2)

        def s_(a_, b_, f=smooth):          # finestra in secondi della play
            return fra(a_ / T, b_ / T, f)

        t_pulsa = 1.95

        def riempi_e_pulsa(m, a_):
            t = a_ * T
            u = ease_out_cubic(min(1.0, max(0.0, (t - 0.85) / 0.5)))
            nuovo = spicchio(max(u, 0.001))
            k = np.sin(np.pi * (t - t_pulsa) / 0.22) if 0 <= t - t_pulsa <= 0.22 else 0.0
            m.become(nuovo.scale(1 + 0.18 * k, about_point=punto(*OROLOGIO)))

        self.play(*[FadeOut(m, rate_func=s_(0, 0.25)) for m in via],
                  grafico.animate(rate_func=s_(0.2, 0.75)).scale(PICCOLO, about_point=punto(*ANCORA_PICCOLO))
                  .shift(punto(*META_PICCOLO) - punto(*ANCORA_PICCOLO)),
                  # «110 h» non viaggia (attraverserebbe la riga piatta mentre il grafico si stringe): si spegne
                  # dov'è insieme alle etichette e si riaccende al suo posto quando il grafico è fermo
                  FadeOut(tag, rate_func=s_(0, 0.2)),
                  FadeIn(meta_tag, shift=LEFT * px(12), rate_func=s_(0.8, 1.05, ease_out_cubic)),
                  Create(cerchio, rate_func=s_(0.45, 0.85)), FadeIn(tacche, rate_func=s_(0.6, 0.85)),
                  *[entra_e_accendi(x, (0.6, 0.9), (1.4 + 0.014 * i, 1.54 + 0.014 * i), T) for i, x in enumerate(gg)],
                  FadeIn(mese, rate_func=s_(0.7, 0.95)),
                  UpdateFromAlphaFunc(fetta, riempi_e_pulsa, rate_func=linear),
                  FadeIn(ore, shift=UP * px(10), rate_func=s_(1.2, 1.45)), run_time=T)
        self.remove(tag)


class Scena08(ScenaReel):
    """Cinque beat. Il tetto di memoria: «24 GB», il modello che ci sta entra nella scheda, Spunta (b0); quello largo
    il doppio sborda, la scheda si spegne con la Croce, e il blocco intero vola nel server, il noleggio (b1); la
    Croce esce, la fattura e il mese di noleggio (b2); la riga della fattura si accende, «90 h» vola accanto alla
    barra con la tacca a 110 (b3); la barra si ferma sotto la tacca e la freccia sceglie il noleggio (b4)."""

    def costruisci(self):
        testi = self.scena.get("testo") or ["esempio"]
        assert testi[0] == "esempio", "TESTO: della scena 8 cambiato: aggiorna l'etichetta"
        g, piccola, grafico, tag, oro, ore, gg, mese = fine_6(self)   # fotogramma 0 = ultimo della scena 6

        # beat 0 · «La mossa sensata è questa: prima controlla se il modello che vuoi usare ci entra nella memoria
        # della scheda.»
        inizio = self.t
        scheda = piccola
        db = g.db
        gb = colloca(testo("24 GB", "caption", colore=P.testo, peso=BOLD), C8[0], C8[1] + H_S / 2 + 28, "c", "t")
        resto = [m for m in grafico if m is not db and m is not scheda]
        self.play(FadeOut(tag, rate_func=fra(0, 0.3)), FadeOut(ore, rate_func=fra(0, 0.3)),
                  FadeOut(mese, rate_func=fra(0, 0.3)),
                  FadeOut(oro, rate_func=fra(0.05, 0.4)), *[FadeOut(x, rate_func=fra(0.05, 0.4)) for x in gg],
                  *[FadeOut(m, rate_func=fra(0.05, 0.4)) for m in resto],
                  Transform(db, server_da(SRV8), rate_func=fra(0.3, 1, ease_out_cubic)),
                  Transform(scheda, Scheda(1.0, C8), rate_func=fra(0.3, 1, ease_out_cubic)),
                  run_time=self.arrotonda(0.9))
        self.attendi_fino(inizio + 1.4)                                         # «prima controlla»
        self.play(FadeIn(gb, shift=UP * px(8)), run_time=self.arrotonda(0.35))
        riga = scheda.riga_chip()
        piccolo = RoundedRectangle(corner_radius=px(8), width=px(BLOCCO_W), height=px(40), stroke_width=0,
                                   fill_color=P.accento, fill_opacity=1).move_to(riga)
        piccolo.set_z_index(2)
        self.attendi_fino(inizio + 2.55)                                        # «il modello che vuoi usare»
        self.play(FadeIn(piccolo, shift=DOWN * px(150), rate_func=rimbalzo(0.05)), run_time=self.arrotonda(0.6))
        spunta = Spunta(altezza_px=80).move_to(punto(138, C8[1]))
        self.attendi_fino(inizio + 4.5)                                         # «nella memoria della scheda»
        self.play(spunta.entra(), run_time=self.arrotonda(0.35))

        # beat 1 · «Se non ci entra, fine, la ==affitti==.»
        self.beat(1)
        inizio = self.t
        self.play(FadeOut(piccolo, shift=UP * px(150), rate_func=rush_into), FadeOut(spunta),
                  run_time=self.arrotonda(0.3))
        grande = RoundedRectangle(corner_radius=px(8), width=px(2 * BLOCCO_W + 8), height=px(40), stroke_width=0,
                                  fill_color=P.accento, fill_opacity=1).move_to(riga)
        grande.set_z_index(2)
        self.play(FadeIn(grande, shift=DOWN * px(150), rate_func=rimbalzo(0.05)), run_time=self.arrotonda(0.5))
        croce = Croce(altezza_px=76).move_to(punto(138, C8[1]))
        self.play(Transform(scheda, Scheda(1.0, C8, spenta=True)), croce.entra(), run_time=self.arrotonda(0.35))

        # GRANDE (carica e rimbalzo) su «la affitti»: il blocco largo, intero (nessuno sdoppiamento: la voce non
        # dice «prendilo più piccolo»), arretra un attimo, vola verso il server stringendosi, lo supera di poco, ci
        # torna e si infila nella fessura del secondo cassetto; il server pulsa e la scheda si riaccende
        p0 = grande.get_center().copy()
        p1 = db.fessura(1).copy()
        base = grande.copy()
        durata_volo, fine_volo, entra = self.arrotonda(1.2), 0.66, 0.08
        largo_fessura = w_px(db.fessure[1]) / (2 * BLOCCO_W + 8)
        indietro, oltre = 0.06, 0.12

        def corsa(t: float) -> float:
            if t < 0.2:
                return -indietro * np.sin(np.pi / 2 * t / 0.2)
            if t < 0.72:
                return -indietro + (1 + oltre + indietro) * smooth((t - 0.2) / 0.52)
            return 1 + oltre - oltre * smooth((t - 0.72) / 0.28)

        def vola(m, a):
            t = min(1.0, a / fine_volo)
            k = smooth(min(1.0, max(0.0, (t - 0.15) / 0.6)))
            nuovo = base.copy().stretch(1 - (1 - largo_fessura) * k, 0).stretch(1 - 0.55 * k, 1)
            q = min(1.0, max(0.0, (a - fine_volo) / entra))
            if q > 0:
                nuovo.stretch(1 - 0.85 * q, 1)
            if q >= 1:
                nuovo.set_fill(opacity=0)
            m.become(nuovo.move_to(p0 + (p1 - p0) * corsa(t)))

        self.attendi_fino(inizio + 1.3)                                         # «la affitti»
        self.play(UpdateFromAlphaFunc(grande, vola, rate_func=linear),
                  pulsa(db, [(fine_volo + entra) * durata_volo - 0.05], durata_volo, ampiezza=0.28, largo=0.36),
                  FadeOut(croce, rate_func=fra(0.55, 0.75)),
                  Transform(scheda, Scheda(1.0, C8), rate_func=fra(0.8, 1)),
                  run_time=durata_volo)
        self.remove(grande)

        # beat 2 · «Se ci entra, affittala un mese»: (la Croce è già uscita, prima che la scheda si riaccendesse) entra la fattura (intera, righe-sagoma) e accanto
        # al server il mese di noleggio, lo stesso calendario della scena 6 in piccolo, che si accende in fretta
        self.beat(2)
        inizio = self.t
        carta = RoundedRectangle(corner_radius=px(18), width=px(300), height=px(350), stroke_color=P.attenuato,
                                 stroke_width=tratto(3), fill_color=P.sfondo, fill_opacity=1)
        colloca(carta, 630, 795, "l", "t")
        righe = Sagome([0.5, 0.95, 0.8, 0.9, 0.7, 0.6], larghezza_px=230, altezza_px=18, passo_px=48)
        righe.move_to(carta)
        fattura = VGroup(carta, righe)
        self.attendi_fino(inizio + 0.85)                                        # «affittala»
        self.play(FadeIn(fattura, shift=LEFT * px(60), rate_func=ease_out_cubic), run_time=self.arrotonda(0.5))
        cal = calendario(CAL8)
        T_C = self.arrotonda(0.73)
        self.attendi_fino(inizio + 1.55)                                        # «un mese»
        self.play(*[entra_e_accendi(x, (0, 0.2), (0.2 + 0.012 * i, 0.33 + 0.012 * i), T_C) for i, x in enumerate(cal)],
                  run_time=T_C)

        # beat 3 · «e guarda in fattura quante ore hai pagato.»
        self.beat(3)
        inizio = self.t
        accesa = righe.righe[3]
        self.attendi_fino(inizio + 0.55)                                        # «in fattura»
        self.play(righe.accendi(3), run_time=self.arrotonda(0.3))
        novanta = testo("90 h", "caption", colore=P.testo, peso=BOLD)
        novanta.move_to(accesa.get_left() + RIGHT * novanta.width / 2 + UP * px(34))
        novanta.set_z_index(3)
        # «90 h» nasce dalla riga accesa, ma solo quando intorno non c'è più niente: prima escono la carta, le
        # altre righe e il mese, poi la riga si spegne mentre il numero sale al suo posto (mai sopra un'altra riga)
        altre = [r for k, r in enumerate(righe.righe) if k != 3]
        self.attendi_fino(inizio + 1.0)                                         # «quante ore»
        self.play(FadeOut(carta, rate_func=fra(0, 0.4)), *[FadeOut(r, rate_func=fra(0, 0.4)) for r in altre],
                  *[FadeOut(x, rate_func=fra(0, 0.4)) for x in cal],
                  FadeOut(accesa, shift=UP * px(12), rate_func=fra(0.4, 0.62)),
                  FadeIn(novanta, shift=UP * px(20), scale=0.6, rate_func=fra(0.6, 1, ease_out_back)),
                  run_time=self.arrotonda(0.5))
        es = etichetta(testo(testi[0], "piede", colore=P.attenuato))
        y90 = BAR_Y0 - BAR_H * 90 / BAR_MAX
        y110 = BAR_Y0 - BAR_H * 110 / BAR_MAX
        meta90 = novanta.copy()
        colloca(meta90, BAR_X - BAR_W / 2 - 18, y90, "r", "c")
        colloca(es, BAR_X - BAR_W / 2 - 18, y90 + h_px(meta90) / 2 + 6, "r", "t")
        pista = Rectangle(width=px(BAR_W), height=px(BAR_H), stroke_color=P.attenuato, stroke_width=tratto(3),
                          fill_opacity=0).move_to(punto(BAR_X, BAR_Y0 - BAR_H / 2))
        tacca = Line(punto(BAR_X - BAR_W / 2 - 10, y110), punto(BAR_X + BAR_W / 2 + 10, y110),
                     stroke_color=P.accento, stroke_width=tratto(7))
        l110 = colloca(testo("110", "etichetta", colore=P.accento, peso=BOLD), BAR_X + BAR_W / 2 + 18, y110, "l", "c")
        # «90 h» vola accanto alla barra, che si disegna mentre arriva
        self.play(novanta.animate(rate_func=fra(0, 0.6, ease_out_cubic)).move_to(meta90),
                  Create(pista, rate_func=fra(0.2, 0.8)), Create(tacca, rate_func=fra(0.35, 0.9)),
                  FadeIn(l110, rate_func=fra(0.5, 0.9)), FadeIn(es, rate_func=fra(0.65, 1)),
                  run_time=self.arrotonda(0.8))

        # beat 4 · «Se stai sotto centodieci, comprarla ti costava di più.» — finale calmo: due passaggi, poi fermo
        self.beat(4)
        inizio = self.t
        pieno = Rectangle(width=px(BAR_W - 8), height=px(BAR_H * 90 / BAR_MAX), stroke_width=0,
                          fill_color=P.secondario, fill_opacity=1)
        pieno.move_to(punto(BAR_X, BAR_Y0 - BAR_H * 90 / BAR_MAX / 2))
        freccia = Freccia(punto(BAR_X - 10, BAR_Y0 - BAR_H - 14), db.get_right() + RIGHT * px(16),
                          colore=P.accento, spessore_px=7)
        self.attendi_fino(inizio + 0.25)                                        # «sotto centodieci»
        self.play(GrowFromEdgeBasso(pieno, ease_out_cubic), run_time=self.arrotonda(0.8))
        self.attendi_fino(inizio + 1.5)                                         # «comprarla»
        T_F = self.arrotonda(0.73)
        self.play(GrowArrow(freccia.freccia, rate_func=fra(0, 0.75)),
                  pulsa(db, [0.5], T_F, ampiezza=0.15, largo=0.22), run_time=T_F)


def GrowFromEdgeBasso(mob, rate_func):
    """La barra si riempie dal basso (GrowFromEdge con la sua curva)."""
    from manim import GrowFromEdge
    return GrowFromEdge(mob, DOWN, rate_func=rate_func)
