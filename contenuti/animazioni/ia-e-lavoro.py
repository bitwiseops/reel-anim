"""Animazioni di «L'IA e il tuo lavoro: meno paura, più controllo»
(contenuti/sceneggiature/2026-09-20-ia-e-lavoro.md).

Regime «il reel si guarda muto» (docs/animazioni.md §0): le caption col parlato si bruciano in fondo, quindi qui
**non c'è nessuna frase da leggere**. A schermo: figure, tre numeri con le loro due etichette corte (cosa misura, da
dove viene), l'etichetta «esempio» e il «?» della scommessa.

Struttura del 2026-09-23 (VOCE dal copione, nove scene):
- scene 1 e 9 (volto pieno) e 3, 5, 8 (`[broll]`): **nessuna classe**.
- scene animate 2, 4, 6, 7: ognuna parte dall'ultimo fotogramma della scena animata prima (la 4 dalla 2 e la 6 dalla
  4, dopo un filmato; la 7 dalla 6, di fila), con le posizioni calcolate in un posto solo (`stato_fine_N`).

Filo visivo (sempre con lo stesso aspetto):
1. le **dieci figure** (`Fila`, icona `user`): sei accese = esposti; non si sbarrano, non escono, non si spengono;
2. il **numero con le sue due etichette** (cosa misura · fonte), che entrano ed escono insieme;
3. la **tessera che si spezza**: cinque pezzi-compito nella 4, il resoconto in quattro nella 7; le tessere nel bordo
   della 6 sono della stessa famiglia di icone;
4. il **bordo frastagliato**: nasce nella 6, torna piccolo nel richiamo della 7 (disegnato una volta, poi scalato);
5. l'IA è una **piccola rete neurale** (tre strati di nodi e archi), mai un'icona di database o di robot.
"""
from __future__ import annotations

import random

import numpy as np
from manim import (BOLD, DOWN, LEFT, RIGHT, UP, AnimationGroup, Circle, Create, DashedLine, FadeIn, FadeOut,
                   FadeTransform, GrowFromEdge, Indicate, LaggedStart, Line, RoundedRectangle, ShowPassingFlash,
                   Transform, UpdateFromAlphaFunc, VGroup, VMobject, linear, rate_functions, smooth, squish_rate_func,
                   there_and_back)
from manim.constants import LineJointType

from tools.anim.base import ScenaReel
from tools.anim.componenti import Croce, Fila, Icona, Lente, Sagome, Spunta, etichetta, testo
from tools.anim.misure import px, tratto
from tools.anim.pattern import rimbalzo

# --- misure condivise fra le scene (px; l'area contenuto è 900 × 752) --------------------------------------
FIG_PX = 100         # altezza di una figura umana: la stessa in tutto il reel
PASSO_PX = 134
FILA_ALTA = 10       # bordo alto della fila, px sotto il bordo alto dell'area contenuto
FILA_CENTRO = 150    # la fila «al centro della metà alta»: scena 2, beat 0-3
NUM_BASSO = 6        # bordo basso del gruppo numero + etichette, px sopra il fondo dell'area
NUM_6 = "6 su 10"    # il `TESTO:` della scena 2, che torna nella 4 e nella 6
FONTE_FMI = "Fondo Monetario, 2024"


# --- aiuti locali ------------------------------------------------------------------------------------------

def giu(a, m, giu_px: float, dx_px: float = 0.0):
    """Mette `m` con il bordo alto a `giu_px` px sotto il bordo alto dell'area, spostato di `dx_px` dal centro."""
    m.move_to([a.centro[0] + px(dx_px), a.y1 - px(giu_px) - m.height / 2, 0])
    return m


def su(a, m, su_px: float, dx_px: float = 0.0):
    """Mette `m` con il bordo basso a `su_px` px sopra il fondo dell'area."""
    m.move_to([a.centro[0] + px(dx_px), a.y0 + px(su_px) + m.height / 2, 0])
    return m


def y_giu(a, giu_px: float) -> float:
    return a.y1 - px(giu_px)


def dx(a, dx_px: float) -> float:
    return a.centro[0] + px(dx_px)


def fra(a: float, b: float = 1.0, f=smooth):
    """Curva `f` compressa nella frazione [a, b] della play (movimenti sfalsati in un solo passaggio)."""
    return squish_rate_func(f, max(0.0, a), min(1.0, b))


def a_tappe(mob, stati: list, confini: list[float], curve: list | None = None) -> UpdateFromAlphaFunc:
    """`mob` passa per gli `stati` (copie con la stessa struttura), raggiunti alle frazioni `confini` della play:
    una sola animazione anche quando il percorso ha più tratti (due `.animate` non si sommano).
    Aiuto locale (da contenuti/archivio/generativa-probabile/animazioni.py)."""
    curve = curve or [smooth] * (len(stati) - 1)
    pezzi = [m.family_members_with_points() for m in (mob, *stati)]

    def f(m, a):
        k = max((j for j, c in enumerate(confini) if a >= c), default=-1)
        if k < 0:
            i, u = 0, 0.0
        elif k >= len(stati) - 1:
            i, u = len(stati) - 2, 1.0
        else:
            i, u = k, curve[k]((a - confini[k]) / max(confini[k + 1] - confini[k], 1e-6))
        for sub, s1, s2 in zip(pezzi[0], pezzi[i + 1], pezzi[i + 2]):
            sub.interpolate(s1, s2, u)

    return UpdateFromAlphaFunc(mob, f, rate_func=linear)


def traccia(mob, a: float, b: float, f=smooth) -> UpdateFromAlphaFunc:
    """Come `Create` nella finestra [a, b] della play, ma invisibile prima di `a`: un Create compresso in una
    finestra, a progresso zero, disegna un puntino (il cappuccio del tratto) per tutta l'attesa."""
    pieno = mob.copy()
    mob.set_stroke(opacity=0)

    def g(m, t):
        u = f(min(1.0, max(0.0, (t - a) / (b - a))))
        if u <= 1e-3:
            m.set_stroke(opacity=0)
            return
        m.pointwise_become_partial(pieno, 0, u)
        m.set_stroke(opacity=pieno.get_stroke_opacity())

    return UpdateFromAlphaFunc(mob, g, rate_func=linear)


def attenua(m, fattore: float):
    """Abbassa l'intensità **senza toccare i colori**: `set_opacity` su un'icona SVG accende un riempimento che
    non è nella palette (Icona nasce con fill_opacity 0), e il controllo `colore` lo segnala."""
    for x in m.family_members_with_points():
        so, fo = x.get_stroke_opacity(), x.get_fill_opacity()
        if so > 0:
            x.set_stroke(opacity=so * fattore)
        if fo > 0:
            x.set_fill(opacity=fo * fattore)
    return m


def fila_dieci(accese: int = 0) -> Fila:
    """Le dieci figure, sempre identiche: due file da cinque, 526 × 234 px."""
    return Fila("user", quanti=10, per_riga=5, accese=accese, altezza_px=FIG_PX, passo_px=PASSO_PX)


def vesti(fila: Fila, accese: str, spente: str, op_accese: float = 1.0, op_spente: float = 0.45) -> Fila:
    for f in fila.figure[:6]:
        f.svg.set_stroke(accese, opacity=op_accese)
    for f in fila.figure[6:]:
        f.svg.set_stroke(spente, opacity=op_spente)
    return fila


def numero(sc, valore: str, cosa: str, fonte: str, scala: float = 1.0, circa: bool = False) -> VGroup:
    """Un numero grande **con le sue due etichette**: cosa misura e da dove viene. Entrano nella stessa
    animazione, si muovono ed escono insieme. Con `circa` davanti al numero c'è un «≈» (il Fondo dice «about»)."""
    col = sc.cfg.palette
    n = testo(valore, "messaggio", colore=col.accento, peso=BOLD, allinea="center")
    if scala != 1.0:
        n.scale(scala)
    e = VGroup(testo(cosa, "etichetta", colore=col.testo, peso=BOLD, allinea="center"),
               testo(fonte, "piede", colore=col.attenuato, allinea="center")).arrange(DOWN, buff=px(10))
    etichetta(e)
    if circa:
        c = testo("≈", "messaggio", colore=col.accento, peso=BOLD)
        riga = VGroup(c, n).arrange(RIGHT, buff=px(22))
    else:
        c, riga = None, n
    g = VGroup(riga, e).arrange(DOWN, buff=px(18))
    g.numero, g.etich, g.circa = n, e, c
    return g


def numero_6(sc, scala: float = 1.0, circa: bool = False) -> VGroup:
    """«6 su 10» nel suo slot, in fondo all'area: stesso posto in tutte le scene."""
    g = numero(sc, NUM_6, "esposti", FONTE_FMI, scala=scala, circa=circa)
    return su(sc.area.contenuto, g, NUM_BASSO)


def bordo_frastagliato(colore: str, larghezza_px: float, altezza_px: float, punte: int = 26,
                       ampiezza_px: float = 18, seme: int = 11, spessore_px: float = 4) -> VMobject:
    """La frontiera irregolare (*jagged frontier*): una polilinea chiusa con punte e rientranze."""
    r = random.Random(seme)
    rx, ry, amp = px(larghezza_px) / 2, px(altezza_px) / 2, px(ampiezza_px)
    punti = []
    for i in range(punte):
        th = 2 * np.pi * i / punte
        d = amp * (1.0 if i % 2 == 0 else -0.7) * (0.45 + r.random() * 0.75)
        punti.append(np.array([(rx + d) * np.cos(th), (ry + d) * np.sin(th), 0.0]))
    punti.append(punti[0])
    m = VMobject(stroke_color=colore, stroke_width=tratto(spessore_px))
    m.set_points_as_corners(punti)
    m.joint_type = LineJointType.MITER
    return m


BORDO_W, BORDO_H = 560, 236   # la frontiera «vera»: quella della scena 6


def bordo_largo(colore: str, larghezza_px: float = BORDO_W) -> VMobject:
    """La stessa frontiera a qualunque misura: disegnata una volta sola e scalata (stessa silhouette ovunque; con
    `scale` lo spessore del tratto non cambia, quindi la versione piccola non diventa un filo)."""
    b = bordo_frastagliato(colore, BORDO_W, BORDO_H, ampiezza_px=20)
    if larghezza_px != BORDO_W:
        b.scale(larghezza_px / BORDO_W)
    return b


def cornice(sc, larghezza_px: float, altezza_px: float, colore: str | None = None,
            raggio_px: float = 18, spessore_px: float = 3) -> RoundedRectangle:
    col = sc.cfg.palette
    return RoundedRectangle(corner_radius=px(raggio_px), width=px(larghezza_px), height=px(altezza_px),
                            stroke_color=colore or col.attenuato, stroke_width=tratto(spessore_px),
                            fill_color=col.sfondo, fill_opacity=1)


def freccia_tratteggiata(sc, da, a, colore: str) -> VGroup:
    """La condizionalità («potrebbe») si dice col tratteggio."""
    f = DashedLine(da, a, dash_length=px(15), dashed_ratio=0.55, stroke_color=colore, stroke_width=tratto(7))
    f.add_tip(tip_length=px(32), tip_width=px(28))
    f.tip.set_fill(colore, opacity=1).set_stroke(colore, width=0)
    return VGroup(f)


# --- l'IA: una piccola rete neurale (2026-09-22: mai l'icona database, mai un robot) --------------------------

def rete(sc, larghezza_px: float = 90) -> VGroup:
    """Tre strati di nodi (3-4-3) e gli archi fra strati vicini, niente testo. Centrata nell'origine."""
    col = sc.cfg.palette
    w = larghezza_px
    r, passo = max(4.0, 0.07 * w), 0.27 * w
    strati = [[np.array([px(xs), px((j - (n - 1) / 2) * passo), 0.0]) for j in range(n)]
              for xs, n in ((-0.38 * w, 3), (0.0, 4), (0.38 * w, 3))]
    archi = VGroup(*[Line(p, q, stroke_color=col.attenuato, stroke_width=tratto(max(1.5, 2.6 * w / 110)))
                     for s0, s1 in zip(strati, strati[1:]) for p in s0 for q in s1])
    nodi = VGroup(*[Circle(radius=px(r), stroke_width=0, fill_color=col.testo, fill_opacity=1).move_to(p)
                    for s in strati for p in s])
    g = VGroup(archi, nodi)
    g.archi, g.nodi = archi, nodi
    return g


# --- i cinque pezzi-compito della scena 4 (e le tessere della 6, stessa famiglia) ----------------------------
ICONE_COMPITO = ("phone", "pen-line", "keyboard", "calendar", "folder")
FAN_ANGOLI = (-14, -7, 0, 7, 14)


def pezzo_compito(sc, i: int, colore: str | None = None, opacita: float = 1.0) -> VGroup:
    col = sc.cfg.palette
    c = colore or col.attenuato
    box = cornice(sc, 116, 150, colore=c, raggio_px=14)
    ico = Icona(ICONE_COMPITO[i], altezza_px=62, colore=c).move_to(box)
    g = VGroup(box, ico)
    if opacita != 1.0:
        attenua(g, opacita)
        box.set_fill(col.sfondo, opacity=1)   # la cornice resta opaca: il pezzo si attenua, non sparisce
    return g


def tessera_compito(sc, i: int, colore: str | None = None, larghezza_px: float = 62,
                    altezza_px: float = 44) -> VGroup:
    """Una tessera-compito piccola: la cornice e l'icona del compito, nessuna parola."""
    c = colore or sc.cfg.palette.attenuato
    box = cornice(sc, larghezza_px, altezza_px, colore=c, raggio_px=8, spessore_px=2.5)
    ico = Icona(ICONE_COMPITO[i % 5], altezza_px=altezza_px * 0.58, colore=c).move_to(box)
    return VGroup(box, ico)


# ============================================================================================================
class Scena02(ScenaReel):
    """Dieci lavori. Lo slot resta vuoto finché non c'è niente da contare, poi il numero arriva enorme.
    GRANDE (tipografia cinetica) sull'ultima parola del beat 3, «sei»."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        self.fila = fila_dieci()
        giu(a, self.fila, FILA_CENTRO)
        self.add(self.fila)   # fotogramma 0 già pieno: stacco dalla faccia

        # beat 0 — «Su dieci lavori in un paese avanzato,»: il conteggio passa su ciascuna, da sinistra
        self.play(LaggedStart(*[Indicate(f.svg, scale_factor=1.22, color=col.testo) for f in self.fila.figure],
                              lag_ratio=0.22, group=self.fila), run_time=self.arrotonda(1.9))

        # beat 1 — «quanti sono esposti all'IA?»: lo slot si apre dove starà il numero; dentro un trattino, sotto
        # niente (nessuna etichetta sarebbe vera)
        self.beat(1)
        piccolo = numero_6(self)
        self.slot = cornice(self, 380, 128, raggio_px=22, spessore_px=3).set_fill(col.sfondo, opacity=0)
        self.slot.move_to(piccolo.numero)
        self.trattino = Line(LEFT * px(46), RIGHT * px(46), stroke_color=col.attenuato,
                             stroke_width=tratto(9)).move_to(self.slot)
        self.play(Create(self.slot), run_time=0.6)
        self.play(FadeIn(self.trattino, scale=0.6), run_time=0.3)

        # beat 2 — «Tu quanti dici?»: il vuoto della scommessa, nessuna figura accesa
        self.beat(2)
        self.play(FadeOut(self.trattino), run_time=0.2)
        self.dom = testo("?", "messaggio", colore=col.accento, peso=BOLD).move_to(self.slot)
        self.play(FadeIn(self.dom, scale=0.6), run_time=0.27)
        self.play(self.dom.animate(rate_func=there_and_back).scale(1.22), run_time=0.6)

        # beat 3 — «Il Fondo Monetario Internazionale, nel duemilaventiquattro, ha stimato sei.»: mentre la voce dice
        # la fonte l'impulso ripassa lento sulle dieci (conta, non ne accende nessuna); sull'ultima parola il wow
        self.beat(3)
        self.attendi_fino(self.inizi_frasi[3] + 1.0)
        self.play(LaggedStart(*[Indicate(f.svg, scale_factor=1.12, color=col.testo) for f in self.fila.figure],
                              lag_ratio=0.18, group=self.fila), run_time=self.arrotonda(1.6))
        # «sei» è l'ultima parola: si aggancia alla fine della frase (inizio della 5 meno pausa e parola)
        self.attendi_fino(self.inizi_frasi[4] - 0.95)
        self.num = numero_6(self, scala=2.1)
        self.num.numero.save_state()
        self.num.numero.scale(0.3).set_opacity(0)
        self.add(self.num.numero)   # le etichette entrano nella stessa play: mai dopo il numero
        salto = UP * px(FILA_CENTRO - FILA_ALTA)
        anims = []
        for i, f in enumerate(self.fila.figure):
            t = f.copy().shift(salto)
            if i < 6:
                t.svg.set_stroke(col.accento, opacity=0.8)
                p = 0.07 * i
                anims.append(Transform(f, t, rate_func=fra(p, p + 0.55)))
            else:
                t.svg.set_stroke(col.attenuato, opacity=0.32)
                anims.append(Transform(f, t, rate_func=fra(0.0, 0.55)))
        self.play(FadeOut(self.dom, scale=1.5, rate_func=fra(0.0, 0.25)),
                  FadeOut(self.slot, rate_func=fra(0.0, 0.25)),
                  *anims,
                  self.num.numero.animate(rate_func=fra(0.1, 1.0, rimbalzo(0.07))).restore(),
                  FadeIn(self.num.etich, shift=UP * 0.12, rate_func=fra(0.3, 1.0)),
                  run_time=self.arrotonda(0.8))

        # beat 4 — «Lo dicono loro, non io.»: il numero torna a misura di slot (con le etichette appresso), la fila
        # riprende colore; una sottolineatura corre una volta sotto la fonte
        self.beat(4)
        piccolo = numero_6(self)
        fila_fine = vesti(fila_dieci(accese=6), col.accento, col.attenuato)
        giu(a, fila_fine, FILA_ALTA)
        self.play(Transform(self.num, piccolo), Transform(self.fila, fila_fine),
                  run_time=self.arrotonda(0.55), rate_func=rate_functions.ease_in_out_cubic)
        fonte = self.num.etich[1]
        riga = Line(fonte.get_corner(DOWN + LEFT) + DOWN * px(10), fonte.get_corner(DOWN + RIGHT) + DOWN * px(10),
                    stroke_color=col.accento, stroke_width=tratto(6))
        self.play(ShowPassingFlash(riga, time_width=0.6), run_time=self.arrotonda(0.8))


def stato_fine_2(sc) -> tuple[Fila, VGroup]:
    """L'ultimo fotogramma della scena 2: le dieci in alto con le sei accese, «6 su 10» nello slot."""
    col = sc.cfg.palette
    fila = vesti(fila_dieci(accese=6), col.accento, col.attenuato)
    giu(sc.area.contenuto, fila, FILA_ALTA)
    return fila, numero_6(sc)


# ============================================================================================================
# Il tre e tre della scena 4: la scena 6 riparte da qui (dopo lo stacco sul filmato della 5).

# I due terzetti stanno sulla riga alta della fila: le cinque figure di sopra si spostano solo in orizzontale (due
# a sinistra, tre a destra) e la sesta, che sta sotto a sinistra, sale nel posto lasciato libero: nessun percorso ne
# incrocia un altro. Le frecce stanno sotto i gruppi, dove prima c'era la seconda riga.
GIU, SU = (0, 1, 5), (2, 3, 4)


def bersagli_tre_e_tre(sc, fila: Fila) -> tuple[VGroup, VGroup, VGroup]:
    """Le quattro non esposte al centro, attenuate e staccate; i sei in due terzetti ai lati, in due colori pari
    della palette (nessuno dei due più cupo o più spento dell'altro)."""
    a, col = sc.area.contenuto, sc.cfg.palette
    quattro = VGroup(*[fila.figure[i].copy() for i in range(6, 10)])
    quattro.arrange_in_grid(rows=2, cols=2, buff=px(PASSO_PX - FIG_PX))
    giu(a, quattro, 262)
    for q in quattro:
        q.svg.set_stroke(col.attenuato, opacity=0.3)
    g_giu = VGroup(*[fila.figure[i].copy() for i in GIU]).arrange(RIGHT, buff=px(PASSO_PX - FIG_PX))
    g_su = VGroup(*[fila.figure[i].copy() for i in SU]).arrange(RIGHT, buff=px(PASSO_PX - FIG_PX))
    giu(a, g_giu, FILA_ALTA, dx_px=-250)
    giu(a, g_su, FILA_ALTA, dx_px=250)
    for m in g_giu:
        m.svg.set_stroke(col.secondario, opacity=1)
    for m in g_su:
        m.svg.set_stroke(col.terziario, opacity=1)
    return quattro, g_giu, g_su


def frecce_tre_e_tre(sc) -> VGroup:
    a, col = sc.area.contenuto, sc.cfg.palette
    y_a, y_b = y_giu(a, 128), y_giu(a, 240)
    f_giu = freccia_tratteggiata(sc, np.array([dx(a, -250), y_a, 0]), np.array([dx(a, -250), y_b, 0]), col.secondario)
    f_su = freccia_tratteggiata(sc, np.array([dx(a, 250), y_b, 0]), np.array([dx(a, 250), y_a, 0]), col.terziario)
    return VGroup(f_giu, f_su)


def stato_fine_4(sc) -> tuple[Fila, VGroup, VGroup]:
    """L'ultimo fotogramma della scena 4: il tre e tre con le frecce, «≈ 6 su 10» nello slot."""
    col = sc.cfg.palette
    fila = vesti(fila_dieci(accese=6), col.accento, col.attenuato)
    giu(sc.area.contenuto, fila, FILA_ALTA)
    quattro, g_giu, g_su = bersagli_tre_e_tre(sc, fila)
    for i, b in zip(range(6, 10), quattro):
        fila.figure[i].become(b)
    for i, b in zip(GIU + SU, list(g_giu) + list(g_su)):
        fila.figure[i].become(b)
    return fila, numero_6(sc, circa=True), frecce_tre_e_tre(sc)


class Scena04(ScenaReel):
    """Un lavoro è tanti compiti: una delle sei si apre in cinque, due sono alla portata dell'IA, e torna intera al
    suo posto. Poi i sei si dividono tre e tre, e il numero diventa «≈». GRANDE (metamorfosi) sul beat 0."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        self.fila, self.num = stato_fine_2(self)
        self.add(self.fila, self.num)   # fotogramma 0 = ultimo della scena 2, com'era prima del filmato

        # beat 0 — «Esposto vuol dire che una parte dei compiti è alla sua portata,»: una delle sei vola al centro,
        # diventa tessera e si apre a ventaglio in cinque pezzi-compito; due non contigui si accendono
        fig = self.fila.figure[2]
        self.posto = fig.get_center()
        viagg = fig.copy()
        self.add(viagg)
        centro = np.array([a.centro[0], y_giu(a, 382), 0])
        self.play(fig.svg.animate.set_stroke(opacity=0),
                  viagg.animate(rate_func=rate_functions.ease_in_out_sine).move_to(centro).scale(1.6),
                  run_time=self.arrotonda(0.55))
        chiusa = cornice(self, 136, 176, colore=col.accento, raggio_px=16).move_to(centro)
        self.play(FadeTransform(viagg, chiusa), run_time=self.arrotonda(0.27))
        self.pezzi = VGroup(*[pezzo_compito(self, i) for i in range(5)]).arrange(RIGHT, buff=px(10))
        for p, ang in zip(self.pezzi, FAN_ANGOLI):
            p.rotate(ang * np.pi / 180)
        self.pezzi.move_to(centro)
        self.esempio = etichetta(testo(self.scena["testo"][0], "piede", colore=col.attenuato))
        giu(a, self.esempio, 486, dx_px=330)
        self.play(FadeTransform(chiusa, self.pezzi), FadeIn(self.esempio), run_time=self.arrotonda(0.47),
                  rate_func=rate_functions.ease_out_cubic)
        # due pezzi **non contigui**, accesi uno alla volta, grandi come gli altri
        accesi = []
        for k in (1, 3):
            acceso = pezzo_compito(self, k, colore=col.accento)
            accesi.append(acceso.rotate(FAN_ANGOLI[k] * np.pi / 180).move_to(self.pezzi[k]))
        self.play(Transform(self.pezzi[1], accesi[0], rate_func=fra(0.0, 0.5)),
                  Transform(self.pezzi[3], accesi[1], rate_func=fra(0.5, 1.0)),
                  run_time=self.arrotonda(0.47))
        # l'anello attorno ai **soli** due accesi; gli altri tre si attenuano ma restano, della stessa misura
        self.anelli = VGroup(*[RoundedRectangle(corner_radius=px(22), width=self.pezzi[k].width + px(26),
                                                height=self.pezzi[k].height + px(26), stroke_color=col.accento,
                                                stroke_width=tratto(5), fill_opacity=0).move_to(self.pezzi[k])
                               for k in (1, 3)])
        spenti = []
        for k in (0, 2, 4):
            s = pezzo_compito(self, k, opacita=0.5)
            spenti.append(s.rotate(FAN_ANGOLI[k] * np.pi / 180).move_to(self.pezzi[k]))
        self.play(*[Create(an) for an in self.anelli],
                  *[Transform(self.pezzi[k], s) for k, s in zip((0, 2, 4), spenti)],
                  run_time=self.arrotonda(0.47))

        # beat 1 — «non che il posto sparisce.»: la tessera si richiude, torna figura, rientra al suo posto
        # nella fila, accesa e intera, e lì fa un piccolo Indicate: il posto c'è ancora
        self.beat(1)
        chiusa2 = cornice(self, 136, 176, colore=col.accento, raggio_px=16).move_to(self.pezzi.get_center())
        self.play(FadeOut(self.anelli), FadeOut(self.esempio), FadeTransform(self.pezzi, chiusa2),
                  run_time=self.arrotonda(0.4))
        tornata = Icona("user", altezza_px=FIG_PX, colore=col.accento).move_to(self.posto)
        self.play(FadeTransform(chiusa2, tornata), run_time=self.arrotonda(0.47),
                  rate_func=rate_functions.ease_in_out_sine)
        self.remove(tornata)
        fig.svg.set_stroke(col.accento, opacity=1)
        self.play(Indicate(fig.svg, scale_factor=1.28, color=col.accento), run_time=self.arrotonda(0.5))

        # beat 2 — «Di quei sei, circa metà potrebbe rimetterci e metà guadagnarci, secondo loro.»: le quattro non
        # esposte al centro, attenuate; i sei tre e tre ai lati; una freccia in giù e una in su, tratteggiate.
        # I tre sotto la freccia in giù restano accesi, interi e in scena
        self.beat(2)
        quattro, g_giu, g_su = bersagli_tre_e_tre(self, self.fila)
        self.play(*[Transform(self.fila.figure[6 + i], q) for i, q in enumerate(quattro)],
                  run_time=self.arrotonda(0.6))
        self.attendi_fino(self.inizi_frasi[2] + 0.85)         # «circa metà»
        bers = dict(zip(GIU + SU, list(g_giu) + list(g_su)))
        self.play(*[Transform(self.fila.figure[i], bers[i], rate_func=fra(0.0, 0.6, rate_functions.ease_in_out_cubic))
                    for i in range(5)],
                  Transform(self.fila.figure[5], bers[5], rate_func=fra(0.35, 1.0, rate_functions.ease_in_out_cubic)),
                  run_time=self.arrotonda(0.9))
        f_giu, f_su = self.frecce = frecce_tre_e_tre(self)
        self.attendi_fino(self.inizi_frasi[2] + 1.75)         # «potrebbe rimetterci»
        self.play(FadeIn(f_giu, shift=DOWN * 0.2), run_time=self.arrotonda(0.4))      # «potrebbe rimetterci»
        self.attendi_fino(self.inizi_frasi[2] + 2.35)         # «e metà guadagnarci»
        self.play(FadeIn(f_su, shift=UP * 0.2), run_time=self.arrotonda(0.4))
        # «secondo loro»: la stessa sottolineatura della scena 2 corre sotto la fonte
        self.attendi_fino(self.inizi_frasi[3] - 1.2)
        fonte = self.num.etich[1]
        riga = Line(fonte.get_corner(DOWN + LEFT) + DOWN * px(10), fonte.get_corner(DOWN + RIGHT) + DOWN * px(10),
                    stroke_color=col.accento, stroke_width=tratto(6))
        self.play(ShowPassingFlash(riga, time_width=0.6), run_time=self.arrotonda(0.8))

        # beat 3 — «Ma sono stime.»: le frecce pulsano insieme e davanti al numero entra un «≈», che resta
        self.beat(3)
        dopo = numero_6(self, circa=True)
        self.play(self.frecce.animate(rate_func=there_and_back).scale(1.15),
                  self.num.numero.animate.move_to(dopo.numero),
                  FadeIn(dopo.circa, shift=RIGHT * px(30)),
                  run_time=self.arrotonda(0.6))


# ============================================================================================================
# La prova di Harvard: pile di consulenti, la frontiera, le barre.

PILA_DX = (-215, -35)      # la pila con la rete (a sinistra) e quella senza
PILA_SU = 8                # bordo basso delle pile, px sopra il fondo dell'area
RETE_SU = 112              # la rete sopra la pila di sinistra
BASE_SU = 204              # base comune delle due barre (px sopra il fondo): stessa base, da zero
VERDETTO_SU = 210          # croce e spunta
FUORI = (238, 372)         # la tessera fuori dal bordo: giu, dx
BORDO_GIU = 100


def omino(sc, colore: str) -> VGroup:
    """Una sagoma minuscola piena (testa e spalle): diversa dalle figure a tratto dei dieci posti. Il contorno del
    colore dello sfondo le stacca l'una dall'altra quando si sovrappongono."""
    col = sc.cfg.palette
    testa = Circle(radius=px(10), fill_color=colore, fill_opacity=1, stroke_color=col.sfondo, stroke_width=tratto(2.5))
    corpo = RoundedRectangle(corner_radius=px(10), width=px(34), height=px(20), fill_color=colore, fill_opacity=1,
                             stroke_color=col.sfondo, stroke_width=tratto(2.5))
    corpo.next_to(testa, DOWN, buff=px(1))
    return VGroup(corpo, testa)


def pila(sc, quante: int, seme: int, colore: str, mezzo_x: float = 62, mezzo_y: float = 24) -> VGroup:
    """Un mucchio indistinto: sagome sovrapposte e sfalsate dentro un'ellisse, mai una griglia che si possa contare.
    Le più in basso stanno davanti (ordine per y)."""
    r = random.Random(seme)
    posti = []
    while len(posti) < quante:
        x, y = r.uniform(-1, 1), r.uniform(-1, 1)
        if x * x + y * y <= 1:
            posti.append((x * mezzo_x, y * mezzo_y))
    posti.sort(key=lambda p: -p[1])
    return VGroup(*[omino(sc, colore).move_to([px(x), px(y), 0]) for x, y in posti])


def pile_due(sc, nuove: bool = False) -> VGroup:
    """Le due pile ai loro posti: la prima ha la rete sopra. Le «nuove» (altri consulenti) hanno un altro tono."""
    col = sc.cfg.palette
    a = sc.area.contenuto
    c = col.secondario if nuove else col.attenuato
    g = VGroup(pila(sc, 34, 23 if nuove else 13, c), pila(sc, 32, 41 if nuove else 29, c))
    for p, d in zip(g, PILA_DX):
        su(a, p, PILA_SU, d)
    return g


def rete_pila(sc) -> VGroup:
    return su(sc.area.contenuto, rete(sc, 84), RETE_SU, PILA_DX[0])


def tessera_fuori(sc) -> VGroup:
    return giu(sc.area.contenuto, tessera_compito(sc, 4, colore=sc.cfg.palette.testo, larghezza_px=72,
                                                  altezza_px=50), *FUORI)


def tratto_in_scala(fila: Fila, scala: float) -> Fila:
    """`scale` non tocca lo spessore del tratto: una fila rimpicciolita sembrerebbe fatta di sagome piene."""
    for f in fila.figure:
        f.svg.set_stroke(width=tratto(FIG_PX * scala * 2 / 24))
    return fila


def fila_piccola(sc) -> Fila:
    col = sc.cfg.palette
    f = tratto_in_scala(vesti(fila_dieci(accese=6).scale(0.36), col.accento, col.attenuato, 0.4, 0.28), 0.36)
    return giu(sc.area.contenuto, f, 0)


def verdetti(sc) -> tuple[Croce, Spunta, VGroup]:
    """Croce sopra la pila con la rete, spunta sopra l'altra, «−19 punti» con le sue etichette: sempre insieme."""
    a = sc.area.contenuto
    croce = su(a, Croce(altezza_px=70), VERDETTO_SU, PILA_DX[0])
    spunta = su(a, Spunta(altezza_px=70), VERDETTO_SU, PILA_DX[1])
    n19 = numero(sc, sc.scena_testo_19, "un compito", "Harvard, 2023", scala=1.1)
    giu(a, n19, 374, dx_px=240)
    return croce, spunta, n19


class Scena06(ScenaReel):
    """La frontiera frastagliata: dentro, chi aveva l'IA fa la barra più alta; fuori, prende la croce.
    GRANDE (punch) sul beat 6: «Peggio»."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        self.scena_testo_19 = self.scena["testo"][1]
        # fotogramma 0 = ultimo della scena 4 (dopo lo stacco sul filmato della 5)
        self.fila, self.num6, frecce = stato_fine_4(self)
        self.add(self.fila, self.num6, frecce)

        # beat 0 — «Harvard e Boston Consulting Group, nel duemilaventitré,»: le dieci si stringono piccole in alto
        # (le sei ancora accese), frecce e numero escono; al centro entra un mucchio indistinto di sagome minuscole
        piccola = fila_piccola(self)
        self.pile = pile_due(self)
        mucchio = self.pile.copy()
        r = random.Random(5)
        cx, cy = a.centro[0], y_giu(a, 400)
        for om in [o for p in mucchio for o in p]:
            while True:
                x, y = r.uniform(-1, 1), r.uniform(-1, 1)
                if x * x + y * y <= 1:
                    break
            om.move_to([cx + px(x * 170), cy + px(y * 62), 0])
        self.play(Transform(self.fila, piccola, rate_func=fra(0.0, 0.7)),
                  FadeOut(self.num6.numero, shift=DOWN * 0.2, rate_func=fra(0.0, 0.4)),
                  FadeOut(self.num6.circa, shift=DOWN * 0.2, rate_func=fra(0.0, 0.4)),
                  FadeOut(self.num6.etich, shift=DOWN * 0.2, rate_func=fra(0.0, 0.4)),
                  FadeOut(frecce, rate_func=fra(0.0, 0.4)),
                  run_time=self.arrotonda(0.8))
        omini = [o for p in mucchio for o in p]
        r.shuffle(omini)
        self.play(LaggedStart(*[FadeIn(o, scale=0.4) for o in omini], lag_ratio=0.012),
                  run_time=self.arrotonda(0.9), rate_func=rate_functions.ease_out_cubic)

        # beat 1 — «hanno diviso a sorte settecentocinquantotto consulenti.»: il mucchio si rimescola e si divide
        # in due pile affiancate, sempre indistinte; sopra una delle due la rete, sopra l'altra niente
        self.beat(1)
        self.play(Transform(mucchio, self.pile), run_time=self.arrotonda(1.2),
                  rate_func=rate_functions.ease_in_out_cubic)
        self.pile = mucchio
        self.rete = rete_pila(self)
        self.play(FadeIn(self.rete, shift=DOWN * 0.2, scale=0.7), run_time=self.arrotonda(0.5),
                  rate_func=rate_functions.ease_out_back)

        # beat 2 — «Dove l'IA arrivava,»: il bordo frastagliato si disegna a tratto e dentro si accendono a raffica
        # diciotto tessere-compito
        self.beat(2)
        self.bordo = giu(a, bordo_largo(col.testo), BORDO_GIU)
        self.tessere = VGroup(*[tessera_compito(self, (i * 2 + i // 6) % 5) for i in range(18)])
        self.tessere.arrange_in_grid(rows=3, cols=6, buff=px(9)).move_to(self.bordo)
        ordine = list(range(18))
        random.Random(3).shuffle(ordine)
        self.play(Create(self.bordo, rate_func=fra(0.0, 0.6)),
                  *[FadeIn(self.tessere[k], scale=0.5, rate_func=fra(0.4 + 0.025 * j, 0.55 + 0.025 * j))
                    for j, k in enumerate(ordine)],
                  run_time=self.arrotonda(1.15))

        # beat 3 — «chi l'aveva ha fatto lavori migliori del trentadue per cento.»: due barre da zero, stessa
        # larghezza e stessa base; il «+32%» sta nel **divario** fra le due cime, mai sulla cima alta
        self.beat(3)
        base = a.y0 + px(BASE_SU)
        self.barre = VGroup()
        for dxp, alt in zip(PILA_DX, (172, 130)):
            b = RoundedRectangle(corner_radius=px(8), width=px(90), height=px(alt), stroke_width=0,
                                 fill_color=col.secondario, fill_opacity=1)
            b.move_to([dx(a, dxp), base + px(alt) / 2, 0])
            self.barre.add(b)
        self.play(AnimationGroup(*[GrowFromEdge(b, DOWN) for b in self.barre]),
                  run_time=self.arrotonda(1.0), rate_func=rate_functions.ease_out_cubic)
        cima_a, cima_b = float(self.barre[0].get_top()[1]), float(self.barre[1].get_top()[1])
        meta = (cima_a + cima_b) / 2
        self.n32 = numero(self, self.scena["testo"][0], "qualità", "Harvard, 2023")
        self.n32.numero.move_to([dx(a, 230), meta, 0])
        self.n32.etich.next_to(self.n32.numero, DOWN, buff=px(18))
        gancio = VMobject(stroke_color=col.attenuato, stroke_width=tratto(3))
        gancio.set_points_as_corners([np.array([dx(a, -170), cima_a, 0]), np.array([dx(a, -125), cima_a, 0]),
                                      np.array([dx(a, -125), cima_b, 0]), np.array([dx(a, -80), cima_b, 0])])
        guida = Line(np.array([dx(a, -125), meta, 0]),
                     np.array([float(self.n32.numero.get_left()[0]) - px(20), meta, 0]),
                     stroke_color=col.attenuato, stroke_width=tratto(3))
        self.graffa = VGroup(gancio, guida)
        self.attendi_fino(self.inizi_frasi[4] - 1.9)          # «trentadue per cento»
        self.play(Create(gancio), Create(guida), FadeIn(self.n32, scale=0.8), run_time=self.arrotonda(0.7),
                  rate_func=rate_functions.ease_out_cubic)

        # beat 4 — «Poi ad altri hanno dato un compito fuori portata.»: tessere, barre, numero ed etichette escono
        # insieme (a schermo nessun numero); escono anche le due pile e ne entrano due nuove, di un altro tono,
        # di nuovo con la rete sopra una sola; fuori dal bordo si accende una tessera sola
        self.beat(4)
        self.play(FadeOut(self.tessere), FadeOut(self.barre), FadeOut(self.graffa),
                  FadeOut(self.n32.numero), FadeOut(self.n32.etich),
                  *[p.animate.scale(0.2).set_opacity(0) for p in self.pile],
                  FadeOut(self.rete, scale=0.6),
                  run_time=self.arrotonda(0.5), rate_func=rate_functions.rush_into)
        self.remove(self.pile, *[o for p in self.pile for o in p])
        self.pile = pile_due(self, nuove=True)
        self.rete = rete_pila(self)
        omini = [o for p in self.pile for o in p]   # nell'ordine della pila: lo stesso impilamento della scena 7
        self.play(LaggedStart(*[FadeIn(o, scale=0.4) for o in omini], lag_ratio=0.012),
                  FadeIn(self.rete, shift=DOWN * 0.2, scale=0.7, rate_func=fra(0.5, 1.0)),
                  run_time=self.arrotonda(0.8), rate_func=rate_functions.ease_out_cubic)
        self.fuori = tessera_fuori(self)
        self.attendi_fino(self.inizi_frasi[4] + 1.5)          # «un compito fuori portata»
        self.play(FadeIn(self.fuori, scale=0.4), run_time=self.arrotonda(0.4),
                  rate_func=rate_functions.ease_out_back)

        # beat 5 — «Indovina:»: sopra la tessera di fuori pulsa lo stesso «?» della scommessa della scena 2
        self.beat(5)
        self.dom = testo("?", "messaggio", colore=col.accento, peso=BOLD)
        giu(a, self.dom, FUORI[0] - 112, dx_px=FUORI[1])
        self.play(FadeIn(self.dom, scale=0.6), run_time=self.arrotonda(0.27))
        self.play(self.dom.animate(rate_func=there_and_back).scale(1.22), run_time=self.arrotonda(0.47))

        # beat 6 — GRANDE (punch): «Peggio»; il «?» se ne va col taglio; al ritorno, in una sola animazione, croce
        # sulla pila con la rete, spunta sull'altra e «−19 punti» con le sue etichette: restano insieme fino alla fine
        self.beat(6)
        self.remove(self.dom)
        self.punch("Peggio")
        croce, spunta, n19 = verdetti(self)
        # croce e spunta si stampano (dissolvenza con scala): un Create sfalsato le farebbe comparire a puntini
        self.play(FadeIn(croce, scale=0.4, rate_func=fra(0.0, 0.55, rimbalzo(0.08))),
                  FadeIn(spunta, scale=0.4, rate_func=fra(0.15, 0.7, rimbalzo(0.08))),
                  FadeIn(n19, scale=0.82, rate_func=fra(0.3, 1.0, rate_functions.ease_out_cubic)),
                  run_time=self.arrotonda(1.1))


def stato_fine_6(sc) -> tuple[VGroup, VGroup]:
    """L'ultimo fotogramma della scena 6, ricostruito: la scena 7 parte da lì (filo visivo)."""
    a, col = sc.area.contenuto, sc.cfg.palette
    sc.scena_testo_19 = "−19 punti"
    croce, spunta, n19 = verdetti(sc)
    vecchio = VGroup(fila_piccola(sc), giu(a, bordo_largo(col.testo), BORDO_GIU), rete_pila(sc),
                     pile_due(sc, nuove=True), croce, spunta, n19)
    return vecchio, tessera_fuori(sc)


# ============================================================================================================
# Il resoconto in quattro pezzi (scena 7). Quattro forme **diverse fra loro**, riconoscibili anche da ferme:
# 0 = blocco di cifre a griglia (numeri) · 1 = foglio di righe-sagoma con l'angolo piegato (bozza) ·
# 2 = scaletta di tre blocchetti a gradini (ordine) · 3 = lampadina (conclusione).
CARTA_W, CARTA_H = 330, 244


def _cifre(sc, colore: str) -> VGroup:
    """Blocchetti tutti uguali, righe e colonne regolari, una colonna più scura: una tabella di numeri."""
    col = sc.cfg.palette
    righe = VGroup()
    for _ in range(4):
        riga = VGroup()
        for c in range(5):
            scura = c == 3
            riga.add(RoundedRectangle(corner_radius=px(4), width=px(38), height=px(22), stroke_width=0,
                                      fill_color=col.attenuato if scura else colore,
                                      fill_opacity=0.5 if scura else 1))
        righe.add(riga.arrange(RIGHT, buff=px(12)))
    return righe.arrange(DOWN, buff=px(20))


def _foglio(sc, colore: str) -> VGroup:
    """Righe-sagoma corte, ravvicinate e di lunghezza irregolare: un testo scritto, che non si legge."""
    s = Sagome([0.98, 0.84, 0.95, 0.72, 0.99, 0.88, 0.66, 0.93], larghezza_px=228, altezza_px=11,
               passo_px=23, colore=colore)
    s.righe.set_fill(colore, opacity=0.85)
    return VGroup(s)


def _piega(sc, box, colore: str) -> VGroup:
    """L'angolo in basso piegato: il pezzo è un foglio."""
    lato = px(58)
    ang = box.get_corner(DOWN + RIGHT) + np.array([-px(22), px(20), 0])
    return VGroup(VMobject(stroke_color=colore, stroke_width=tratto(3)).set_points_as_corners(
        [ang + UP * lato, ang, ang + LEFT * lato, ang + UP * lato]))


def _scaletta(sc, colore: str) -> VGroup:
    """Tre blocchetti staccati, di lunghezze diverse, con un pallino davanti, disposti a gradini: una sequenza."""
    g = VGroup()
    for largo in (150, 108, 132):
        voce = VGroup(Circle(radius=px(11), stroke_width=0, fill_color=colore, fill_opacity=1),
                      RoundedRectangle(corner_radius=px(9), width=px(largo), height=px(20), stroke_width=0,
                                       fill_color=colore, fill_opacity=0.9))
        g.add(voce.arrange(RIGHT, buff=px(16)))
    g.arrange(DOWN, buff=px(44), aligned_edge=LEFT)
    for k, voce in enumerate(g):
        voce.shift(RIGHT * px(38 * k))
    return g


def pezzo_resoconto(sc, i: int, colore: str | None = None, contenuto: bool = True) -> VGroup:
    """Uno dei quattro pezzi. Struttura sempre uguale per lo stesso `i`, così due stati si trasformano l'uno
    nell'altro senza sciogliersi."""
    col = sc.cfg.palette
    c = colore or col.testo
    box = cornice(sc, CARTA_W, CARTA_H, raggio_px=20)
    pezzi = [box]
    if i == 0:
        pezzi.append(_cifre(sc, c).move_to(box))
    elif i == 1:
        pezzi.append(_foglio(sc, c).move_to(box).shift(UP * px(12)))
        pezzi.append(_piega(sc, box, col.attenuato))
    elif i == 2:
        pezzi.append(_scaletta(sc, c).move_to(box))
    else:
        pezzi.append(Icona("lightbulb", altezza_px=168, colore=c).move_to(box))
    if not contenuto:
        for p in pezzi[1:]:
            attenua(p, 0.0)
    return VGroup(*pezzi)


SCALA_PICCOLO = 0.55          # i pezzi quando sono in mano alla persona o alla rete
ICONE_GIU = 0                 # riga delle due icone (persona e rete), in cima all'area
COL_DX = 220                  # le due colonne: persona a sinistra, rete a destra
RIGA_GIU = (128, 288, 452)    # le righe dei pezzi piccoli (bordo alto, px sotto il bordo alto dell'area)
DOC_GIU = 376                 # centro del documento grande e della griglia dei quattro pezzi
# i quattro pezzi grandi, in senso orario dall'alto a sinistra: cifre, foglio, scaletta, lampadina; così i due che
# vanno alla rete (foglio e scaletta) stanno già nella colonna di destra e nessun percorso ne incrocia un altro
POS = {0: (-180, -134), 1: (180, -134), 2: (180, 134), 3: (-180, 134)}
TILT = {0: -4, 1: 4, 2: -4, 3: 4}


def pezzo_piccolo(sc, i: int, riga: int, dx_px: float, colore: str | None = None) -> VGroup:
    p = pezzo_resoconto(sc, i, colore=colore).scale(SCALA_PICCOLO)
    return giu(sc.area.contenuto, p, RIGA_GIU[riga], dx_px)


def richiamo(sc) -> tuple[Fila, VMobject, Spunta, Croce]:
    """L'ultima figura animata del reel: le dieci piccole a sinistra con le sei accese (nessuna spenta, nessuna
    cambiata di colore), il bordo piccolo a destra con la spunta dentro e la croce fuori. Fra la fila e la spunta
    c'è il bordo, così la croce non sta mai vicino ai sei."""
    a, col = sc.area.contenuto, sc.cfg.palette
    fila = giu(a, tratto_in_scala(vesti(fila_dieci(accese=6).scale(0.5), col.accento, col.attenuato, 1.0, 0.5), 0.5),
               14, -275)
    bordo = giu(a, bordo_largo(col.testo, 310), 10, 115)
    sp = Spunta(altezza_px=60).move_to(bordo)
    cr = Croce(altezza_px=56).move_to([dx(a, 372), bordo.get_center()[1], 0])
    return fila, bordo, sp, cr


class Scena07(ScenaReel):
    """Il resoconto del mese si spezza in quattro: due pezzi alla rete, due restano a te, e la lente ricontrolla.
    GRANDE (contrasto di scala) sul beat 0: la tessera piccola cresce fino a riempire l'area."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        vecchio, fuori = stato_fine_6(self)
        self.add(vecchio, fuori)   # fotogramma 0 = ultimo della scena 6 (di fila, senza filmato in mezzo)

        # beat 0 — GRANDE (contrasto di scala), «Prendi il resoconto mensile per il capo:»: tutto esce, la tessera
        # di fuori va al centro e cresce di dieci volte in un documento di righe-sagoma
        centro = np.array([a.centro[0], y_giu(a, DOC_GIU), 0])
        k = 390 / CARTA_W
        w, h = px(CARTA_W * k), px(CARTA_H * k)
        box, ico = fuori
        self.play(*[FadeOut(m, rate_func=fra(0.0, 0.7)) for m in vecchio],
                  fuori.animate(rate_func=fra(0.2, 1.0, rate_functions.ease_in_out_sine)).move_to(centro),
                  run_time=self.arrotonda(0.6))
        grande = cornice(self, CARTA_W * k * 2, CARTA_H * k * 2, colore=col.testo, raggio_px=26).move_to(centro)
        righe = Sagome([0.96, 0.9, 0.97, 0.7, 0.93, 0.99, 0.62, 0.9, 0.84, 0.95, 0.55], larghezza_px=640,
                       altezza_px=16, passo_px=46, colore=col.testo).move_to(centro)
        self.play(Transform(box, grande, rate_func=rimbalzo(0.04)), FadeOut(ico, rate_func=fra(0.0, 0.3)),
                  run_time=self.arrotonda(0.9))
        self.remove(fuori)
        self.add(box)             # prima delle righe: aggiunto dopo, il riquadro pieno le coprirebbe
        self.play(righe.entra(lag=0.08), run_time=self.arrotonda(0.5))

        # beat 1 — «numeri, bozza, ordine, conclusione.»: il documento si spezza in quattro pezzi che si aprono a
        # ventaglio, uno per parola, con quattro forme diverse; in fondo «esempio»
        self.beat(1)
        self.pz = VGroup(*[pezzo_resoconto(self, i, contenuto=False).scale(k) for i in range(4)])
        for i, p in enumerate(self.pz):
            sx = -1 if i in (0, 3) else 1
            sy = 1 if i in (0, 1) else -1
            p.move_to(centro + np.array([sx * w / 2, sy * h / 2, 0]))
        self.play(FadeOut(righe), run_time=self.arrotonda(0.2))
        self.remove(box)
        self.add(self.pz)
        finali = VGroup(*[pezzo_resoconto(self, i) for i in range(4)])
        for i, p in enumerate(finali):
            p.move_to(centro + np.array([px(POS[i][0]), px(-POS[i][1]), 0]))
            p.rotate(TILT[i] * np.pi / 180)
        self.esempio = etichetta(testo(self.scena["testo"][0], "piede", colore=col.attenuato))
        su(a, self.esempio, 40)
        finestre = ((0.0, 0.34), (0.22, 0.56), (0.44, 0.78), (0.66, 1.0))   # una per parola
        self.play(*[Transform(q, f, rate_func=fra(*fi, rate_functions.ease_out_cubic))
                    for q, f, fi in zip(self.pz, finali, finestre)],
                  FadeIn(self.esempio, rate_func=fra(0.7, 1.0)),
                  run_time=self.arrotonda(1.9))

        # beat 2 — «Bozza e ordine li fai fare a lei,»: a destra entra la rete; foglio e scaletta si stringono sotto
        # di lei, ognuno nella sua riga (nessun percorso incrocia l'altro); cifre e lampadina ferme
        self.beat(2)
        self.rete = giu(a, rete(self, 112), ICONE_GIU + 4, COL_DX)
        self.play(FadeIn(self.rete, shift=DOWN * 0.2, scale=0.7), run_time=self.arrotonda(0.4),
                  rate_func=rate_functions.ease_out_back)
        self.play(Transform(self.pz[1], pezzo_piccolo(self, 1, 0, COL_DX)),
                  Transform(self.pz[2], pezzo_piccolo(self, 2, 1, COL_DX)),
                  run_time=self.arrotonda(0.9), rate_func=rate_functions.ease_in_out_sine)

        # beat 3 — «numeri e conclusione li tieni tu,»: a sinistra entra la persona; sotto di lei si stringono il
        # blocco di cifre e la lampadina
        self.beat(3)
        self.persona = giu(a, Icona("user", altezza_px=100, colore=col.testo), ICONE_GIU, -COL_DX)
        self.play(FadeIn(self.persona, shift=DOWN * 0.2), run_time=self.arrotonda(0.4))
        self.play(Transform(self.pz[0], pezzo_piccolo(self, 0, 0, -COL_DX)),
                  Transform(self.pz[3], pezzo_piccolo(self, 3, 1, -COL_DX)),
                  run_time=self.arrotonda(0.9), rate_func=rate_functions.ease_in_out_sine)

        # beat 4 — «e ci ricontrolli la bozza.»: il solo foglio torna dalla rete verso la persona (prima in
        # orizzontale nella sua riga, poi giù in mezzo alle colonne: non passa sopra nessuno); la lente lo percorre,
        # poi passa sulle cifre e le accende
        self.beat(4)
        tappa = pezzo_piccolo(self, 1, 0, 0)
        arrivo = pezzo_piccolo(self, 1, 2, 0)
        self.lente = Lente(raggio_px=80, colore=col.testo)
        sx = arrivo.get_left() + RIGHT * px(40)
        self.lente.move_to(sx)
        dx_lente = arrivo.get_right() + LEFT * px(40)
        cifre = pezzo_piccolo(self, 0, 0, -COL_DX)
        cifre_acc = pezzo_piccolo(self, 0, 0, -COL_DX, colore=col.accento)
        # la lente entra (da trasparente a piena, sul posto), percorre il foglio e va sulle cifre: una sola
        # animazione a tappe, perché due animazioni sullo stesso oggetto non si sommano
        spenta = self.lente.copy()
        spenta.cerchio.set_stroke(opacity=0)
        lente_st = [spenta, self.lente.copy(), self.lente.copy().move_to(dx_lente), self.lente.copy().move_to(cifre)]
        self.lente.cerchio.set_stroke(opacity=0)
        self.add(self.lente)
        self.play(a_tappe(self.pz[1], [self.pz[1].copy(), tappa, arrivo], [0.0, 0.2, 0.42]),
                  a_tappe(self.lente, lente_st, [0.42, 0.52, 0.7, 0.92],
                          [smooth, rate_functions.ease_in_out_sine, rate_functions.ease_in_out_cubic]),
                  Transform(self.pz[0], cifre_acc, rate_func=fra(0.86, 1.0)),
                  run_time=self.arrotonda(1.6))

        # beat 5 — «Decidi tu cosa darle e cosa controllare.»: la persona pulsa una volta; poi tutto si stringe in
        # basso e si attenua, e in alto tornano le dieci con le sei accese e il bordo piccolo con la spunta dentro
        # e la croce fuori. È l'ultima figura del reel: un solo passaggio, poi fermo.
        self.beat(5)
        gruppo = VGroup(self.persona, self.rete, *self.pz, self.lente)
        finale = gruppo.copy().scale(0.7)
        su(a, finale, 90)
        for f in finale:
            attenua(f, 0.5)
        pulsata = self.persona.copy().scale(1.25)
        fila, bordo, sp, cr = richiamo(self)
        self.play(a_tappe(self.persona, [self.persona.copy(), pulsata, self.persona.copy(), finale[0]],
                          [0.0, 0.14, 0.3, 0.72]),
                  *[Transform(m, f, rate_func=fra(0.3, 0.72)) for m, f in zip(list(gruppo)[1:], list(finale)[1:])],
                  FadeIn(fila, shift=DOWN * 0.15, rate_func=fra(0.55, 0.85)),
                  traccia(bordo, 0.6, 0.9),
                  FadeIn(sp, scale=0.7, rate_func=fra(0.82, 1.0)),
                  FadeIn(cr, scale=0.7, rate_func=fra(0.82, 1.0)),
                  run_time=self.arrotonda(1.8))


# ============================================================================================================
# Scena 1 e Scena 9: il presentatore a tutto schermo con le sole caption (2026-09-21), nessuna classe.
# Scene 3, 5, 8: [broll], nessuna classe.
