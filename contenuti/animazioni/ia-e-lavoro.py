"""Animazioni di «L'IA e il tuo lavoro: meno paura, più controllo»
(contenuti/sceneggiature/2026-09-20-ia-e-lavoro.md).

Regime «il reel si guarda muto» (docs/animazioni.md §0): le caption col parlato si bruciano in fondo, quindi qui
**non c'è nessuna frase da leggere**. A schermo: figure, tre numeri e sei etichette corte (cosa misura, da dove
viene), più le etichette «esempio», «esposto» e «decidi tu» dichiarate come `TESTO:` nella sceneggiatura.

Scene animate: 2, 3, 5, 6, 7. Le scene 1 e 4 sono a filmato (`[broll]`) e non hanno classe.

Filo visivo (quattro oggetti che tornano, sempre con lo stesso aspetto):
1. le **dieci figure** (`Fila`): una figura = un posto di lavoro per tutto il reel;
2. lo **slot del numero**, sotto la fila e sempre nello stesso punto, con le sue due etichette; vuoto e senza
   etichette finché non c'è niente da contare;
3. la **tessera che si spezza**: cinque pezzi-compito nella 3, quattro pezzi del resoconto nella 6;
4. il **bordo frastagliato**: nasce nella 5, torna piccolo nella 6 e nella 7.
"""
from __future__ import annotations

import random

import numpy as np
from manim import (BOLD, DOWN, LEFT, RIGHT, UP, AnimationGroup, Circle, Create, DashedLine, FadeIn, FadeOut,
                   FadeTransform, GrowFromEdge, Indicate, LaggedStart, Line, RoundedRectangle, Transform, Uncreate,
                   VGroup, VMobject, rate_functions, smooth, squish_rate_func, there_and_back)
from manim.constants import LineJointType

from tools.anim.base import ScenaReel
from tools.anim.componenti import (Croce, Etichetta, Fila, Icona, Lente, Messaggio, Sagome, Spunta, etichetta, piano,
                                   testo)
from tools.anim.misure import px, tratto
from tools.anim.pattern import rimbalzo

# --- misure condivise fra le scene (px della tela; l'area contenuto è 900 × 752) ---------------------------
FIG_PX = 100         # altezza di una figura umana: la stessa in tutto il reel
PASSO_PX = 134
FILA_ALTA = 10       # bordo alto della fila, px sotto il bordo alto dell'area contenuto
FILA_CENTRO = 200    # la fila «al centro»: scene 2 (beat 0-2) e 7 (beat 0)
NUM_BASSO = 6        # bordo basso del gruppo numero + etichette, px sopra il fondo dell'area
SLOT_SU = 92         # lo slot vuoto: dove starà il numero piccolo


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


def numero(sc, valore: str, cosa: str, fonte: str, scala: float = 1.0) -> VGroup:
    """Un numero grande **con le sue due etichette**: cosa misura e da dove viene. Entrano nella stessa
    animazione, si muovono ed escono insieme (Note di produzione, «regola dei numeri»)."""
    col = sc.cfg.palette
    n = testo(valore, "messaggio", colore=col.accento, peso=BOLD, allinea="center")
    if scala != 1.0:
        n.scale(scala)
    e = VGroup(testo(cosa, "etichetta", colore=col.testo, peso=BOLD, allinea="center"),
               testo(fonte, "piede", colore=col.attenuato, allinea="center")).arrange(DOWN, buff=px(10))
    etichetta(e)
    g = VGroup(n, e).arrange(DOWN, buff=px(18))
    g.numero, g.etich = n, e
    return g


def bordo_frastagliato(colore: str, larghezza_px: float, altezza_px: float, punte: int = 26,
                       ampiezza_px: float = 18, seme: int = 11, spessore_px: float = 4) -> VMobject:
    """La frontiera irregolare (*jagged frontier*): non è un componente, si disegna a mano su una polilinea chiusa
    con punte e rientranze. L'irregolarità è la tesi, quindi si deve vedere."""
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


def cornice(sc, larghezza_px: float, altezza_px: float, colore: str | None = None,
            raggio_px: float = 18, spessore_px: float = 3) -> RoundedRectangle:
    col = sc.cfg.palette
    return RoundedRectangle(corner_radius=px(raggio_px), width=px(larghezza_px), height=px(altezza_px),
                            stroke_color=colore or col.attenuato, stroke_width=tratto(spessore_px),
                            fill_color=col.sfondo, fill_opacity=1)


def tessera(sc, larghezza_px: float = 68, altezza_px: float = 40, colore: str | None = None) -> RoundedRectangle:
    """Una tessera-compito: un rettangolino, senza una parola dentro."""
    return cornice(sc, larghezza_px, altezza_px, colore=colore, raggio_px=8, spessore_px=2.5)


def freccia_tratteggiata(sc, da, a, colore: str) -> VGroup:
    """La condizionalità («potrebbe») si dice col tratteggio."""
    f = DashedLine(da, a, dash_length=px(15), dashed_ratio=0.55, stroke_color=colore, stroke_width=tratto(7))
    f.add_tip(tip_length=px(32), tip_width=px(28))
    f.tip.set_fill(colore, opacity=1).set_stroke(colore, width=0)
    return VGroup(f)


# --- i cinque pezzi-compito della scena 3 -------------------------------------------------------------------
ICONE_COMPITO = ("file-text", "message-square", "database", "search", "book-open")
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


# --- i quattro pezzi del resoconto della scena 6 -------------------------------------------------------------
# Quattro forme **diverse fra loro**, non varianti della stessa: si devono distinguere a scena ferma.
# 0 = blocco di cifre a griglia · 1 = lampadina · 2 = foglio di righe-sagoma con l'angolo piegato ·
# 3 = scaletta di tre blocchetti a gradini con il pallino davanti.
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
        pezzi.append(Icona("lightbulb", altezza_px=168, colore=c).move_to(box))
    elif i == 2:
        pezzi.append(_foglio(sc, c).move_to(box).shift(UP * px(12)))
        pezzi.append(_piega(sc, box, col.attenuato))
    else:
        pezzi.append(_scaletta(sc, c).move_to(box))
    if not contenuto:
        for p in pezzi[1:]:
            attenua(p, 0.0)
    return VGroup(*pezzi)


# ============================================================================================================
class Scena02(ScenaReel):
    """Dieci posti di lavoro. Lo slot resta vuoto finché non c'è niente da contare, poi il numero arriva enorme.
    GRANDE (tipografia cinetica) sul beat 3: «Sono sei, e lo dicono loro, non io.»"""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        self.fila = fila_dieci()
        giu(a, self.fila, FILA_CENTRO)
        self.add(self.fila)   # fotogramma 0 già pieno: dal filmato dell'hook si entra con un taglio

        # beat 0 — «Guarda, dieci posti di lavoro»: il conteggio passa su ciascuna, da sinistra
        self.play(LaggedStart(*[Indicate(f.svg, scale_factor=1.22, color=col.testo) for f in self.fila.figure],
                              lag_ratio=0.22, group=self.fila), run_time=self.arrotonda(2.6))

        # beat 1 — lo slot si apre vuoto: dentro un trattino, e sotto **niente** (nessuna etichetta sarebbe vera)
        self.beat(1)
        self.slot = cornice(self, 380, 128, raggio_px=22, spessore_px=3).set_fill(col.sfondo, opacity=0)
        su(a, self.slot, SLOT_SU)
        self.play(Create(self.slot), run_time=1.2)
        self.trattino = Line(LEFT * px(46), RIGHT * px(46), stroke_color=col.attenuato,
                             stroke_width=tratto(9)).move_to(self.slot)
        self.attendi_fino(self.inizi_frasi[1] + 2.2)
        self.play(FadeIn(self.trattino), run_time=0.5)

        # beat 2 — «Quanti, secondo te?»: il vuoto della scommessa, senza nessuna figura accesa
        self.beat(2)
        self.play(FadeOut(self.trattino), run_time=0.25)
        self.dom = testo("?", "messaggio", colore=col.accento, peso=BOLD).move_to(self.slot)
        self.play(FadeIn(self.dom, scale=0.7), run_time=0.35)
        self.play(self.dom.animate(rate_func=there_and_back).scale(1.18), run_time=1.0)

        # beat 3 — GRANDE (tipografia cinetica): sei si accendono una dopo l'altra e il numero arriva enorme,
        # spingendo la fila in alto; nella stessa animazione entrano le due etichette
        self.beat(3)
        self.play(FadeOut(self.dom, scale=1.4), FadeOut(self.slot), run_time=0.3)
        self.num = numero(self, self.scena["testo"][0], "esposti", "Fondo Monetario, 2024", scala=2.1)
        su(a, self.num, NUM_BASSO)
        self.num.numero.save_state()
        self.num.numero.scale(0.3).set_opacity(0)
        self.add(self.num.numero)   # le etichette entrano con FadeIn nella stessa play: mai dopo il numero
        salto = UP * px(FILA_CENTRO - FILA_ALTA)
        anims = []
        for i, f in enumerate(self.fila.figure):
            t = f.copy().shift(salto)
            if i < 6:
                t.svg.set_stroke(col.accento, opacity=1)
                p = 0.06 * i
                anims.append(Transform(f, t, rate_func=squish_rate_func(smooth, p, min(1.0, p + 0.6))))
            else:
                t.svg.set_stroke(col.attenuato, opacity=0.45)
                anims.append(Transform(f, t))
        self.play(*anims,
                  self.num.numero.animate(rate_func=rimbalzo(0.07)).restore(),
                  FadeIn(self.num.etich, shift=UP * 0.12),
                  run_time=1.5)


# ============================================================================================================
class Scena03(ScenaReel):
    """«Persi» è la lettura sbagliata: si vede e si disfa a vista. Poi il lavoro si apre in compiti, e i sei si
    dividono tre e tre. GRANDE (metamorfosi) sul beat 1."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        self.fila = vesti(fila_dieci(accese=6), col.accento, col.attenuato)
        giu(a, self.fila, FILA_ALTA)
        self.num = numero(self, "6 su 10", "esposti", "Fondo Monetario, 2024", scala=2.1)
        su(a, self.num, NUM_BASSO)
        self.add(self.fila, self.num)

        # beat 0 — il numero rientra nel suo slot con le etichette appresso; le sei si sbarrano e scivolano giù
        piccolo = numero(self, "6 su 10", "esposti", "Fondo Monetario, 2024")
        su(a, piccolo, NUM_BASSO)
        self.play(Transform(self.num, piccolo), run_time=0.55)
        self.barre = VGroup()
        for f in self.fila.figure[:6]:
            h, w, c = f.height * 0.60, f.width * 0.76, f.get_center()
            self.barre.add(Line(c + np.array([-w, -h, 0]), c + np.array([w, h, 0]),
                                stroke_color=col.attenuato, stroke_width=tratto(8)))
        self.play(LaggedStart(*[Create(b) for b in self.barre], lag_ratio=0.1),
                  *[f.svg.animate.set_stroke(col.attenuato, opacity=0.85) for f in self.fila.figure[:6]],
                  run_time=0.6)
        self.play(*[m.animate.shift(DOWN * px(26))
                    for m in list(self.fila.figure[:6]) + list(self.barre)], run_time=0.35)

        # beat 1 — GRANDE (metamorfosi): la barratura si disfa a vista, e una figura diventa una tessera in pezzi
        self.beat(1)
        self.play(LaggedStart(*[Uncreate(b) for b in reversed(list(self.barre))], lag_ratio=0.08), run_time=0.45)
        self.remove(self.barre)
        anims = []
        for f in self.fila.figure[:6]:
            t = f.copy().shift(UP * px(26))
            t.svg.set_stroke(col.accento, opacity=1)
            anims.append(Transform(f, t))
        self.play(*anims, run_time=0.35)

        fig = self.fila.figure[2]
        self.posto = fig.get_center()
        viagg = fig.copy()
        self.add(viagg)
        centro = np.array([a.centro[0], y_giu(a, 350), 0])
        self.play(fig.svg.animate.set_stroke(opacity=0),
                  viagg.animate(rate_func=rate_functions.ease_in_out_sine).move_to(centro).scale(1.6),
                  run_time=0.65)
        chiusa = cornice(self, 136, 176, colore=col.accento, raggio_px=16).move_to(centro)
        self.play(FadeTransform(viagg, chiusa), run_time=0.4)
        self.pezzi = VGroup(*[pezzo_compito(self, i) for i in range(5)]).arrange(RIGHT, buff=px(10))
        for p, ang in zip(self.pezzi, FAN_ANGOLI):
            p.rotate(ang * np.pi / 180)
        self.pezzi.move_to(centro)
        self.play(FadeTransform(chiusa, self.pezzi), run_time=0.65)
        self.esempio = etichetta(testo("esempio", "piede", colore=col.attenuato))
        giu(a, self.esempio, 486, dx_px=300)
        self.play(FadeIn(self.esempio), run_time=0.25)
        for k in (1, 3):   # due pezzi **non contigui**, accesi uno alla volta, grandi come gli altri
            acceso = pezzo_compito(self, k, colore=col.accento)
            acceso.rotate(FAN_ANGOLI[k] * np.pi / 180).move_to(self.pezzi[k])
            self.play(Transform(self.pezzi[k], acceso), run_time=0.3)

        # beat 2 — l'anello attorno ai **soli** pezzi accesi: essendo due e non contigui, sono due anelli
        self.beat(2)
        self.anelli = VGroup(*[RoundedRectangle(corner_radius=px(22), width=self.pezzi[k].width + px(26),
                                                height=self.pezzi[k].height + px(26), stroke_color=col.accento,
                                                stroke_width=tratto(5), fill_opacity=0).move_to(self.pezzi[k])
                               for k in (1, 3)])
        spenti = []
        for k in (0, 2, 4):
            s = pezzo_compito(self, k, opacita=0.5)
            spenti.append(s.rotate(FAN_ANGOLI[k] * np.pi / 180).move_to(self.pezzi[k]))
        self.play(*[Create(an) for an in self.anelli],
                  *[Transform(self.pezzi[k], s) for k, s in zip((0, 2, 4), spenti)], run_time=0.8)
        self.esposto = Etichetta(self.scena["testo"][0])
        giu(a, self.esposto, 466, dx_px=-280)
        self.play(self.esposto.entra(), run_time=0.4)

        # beat 3 — la tessera si richiude e rientra nella fila; quattro fuori dal conto, i sei tre e tre
        self.beat(3)
        chiusa2 = cornice(self, 136, 176, colore=col.accento, raggio_px=16).move_to(self.pezzi.get_center())
        self.play(FadeOut(self.anelli), FadeOut(self.esposto), FadeOut(self.esempio),
                  FadeTransform(self.pezzi, chiusa2), run_time=0.55)
        tornata = Icona("user", altezza_px=FIG_PX, colore=col.accento).move_to(self.posto)
        self.play(FadeTransform(chiusa2, tornata), run_time=0.6)
        self.remove(tornata)
        self.fila.figure[2].svg.set_stroke(col.accento, opacity=1)

        quattro = VGroup(*[self.fila.figure[i].copy() for i in range(6, 10)])
        quattro.arrange_in_grid(rows=2, cols=2, buff=px(PASSO_PX - FIG_PX))
        giu(a, quattro, 262)
        for q in quattro:
            q.svg.set_stroke(col.attenuato, opacity=0.3)
        self.play(*[Transform(self.fila.figure[6 + i], q) for i, q in enumerate(quattro)], run_time=0.8)

        g_giu = VGroup(*[self.fila.figure[i].copy() for i in (0, 1, 2)]).arrange(RIGHT, buff=px(PASSO_PX - FIG_PX))
        g_su = VGroup(*[self.fila.figure[i].copy() for i in (3, 4, 5)]).arrange(RIGHT, buff=px(PASSO_PX - FIG_PX))
        giu(a, g_giu, 130, dx_px=-250)
        giu(a, g_su, 130, dx_px=250)
        for m in g_giu:
            m.svg.set_stroke(col.secondario, opacity=1)
        for m in g_su:
            m.svg.set_stroke(col.terziario, opacity=1)
        self.play(*[Transform(self.fila.figure[i], g_giu[i]) for i in (0, 1, 2)],
                  *[Transform(self.fila.figure[3 + i], g_su[i]) for i in range(3)], run_time=1.0)
        y_a, y_b = y_giu(a, 8), y_giu(a, 116)
        f_giu = freccia_tratteggiata(self, np.array([dx(a, -250), y_a, 0]),
                                     np.array([dx(a, -250), y_b, 0]), col.secondario)
        f_su = freccia_tratteggiata(self, np.array([dx(a, 250), y_b, 0]),
                                    np.array([dx(a, 250), y_a, 0]), col.terziario)
        self.play(FadeIn(f_giu, shift=DOWN * 0.15), FadeIn(f_su, shift=UP * 0.15), run_time=0.7)


# ============================================================================================================
def pila(sc, quante: int, seme: int, mezzo_x: float, mezzo_y: float) -> VGroup:
    """Un mucchio indistinto: sagome minuscole sovrapposte e sfalsate, mai una griglia che si possa contare
    (condizione ⚠️ A del revisore). Le sagome sono diverse dalle figure dei dieci posti."""
    col = sc.cfg.palette
    r = random.Random(seme)
    g = VGroup()
    for _ in range(quante):
        c = Circle(radius=px(13), stroke_width=0, fill_color=col.attenuato, fill_opacity=0.8)
        c.move_to([px(r.uniform(-mezzo_x, mezzo_x)), px(r.uniform(-mezzo_y, mezzo_y)), 0])
        g.add(c)
    return g


def pile_due(sc) -> VGroup:
    """La pila con la macchina non è mai la più piccola (⚠️ O): differenza appena percettibile, da mucchio."""
    return VGroup(pila(sc, 46, 13, 56, 32), pila(sc, 41, 29, 50, 29))


class Scena05(ScenaReel):
    """La frontiera frastagliata: dentro, chi aveva l'IA fa la barra più alta; fuori, prende la croce.
    GRANDE (punch) sul beat 4: «Peggio.»"""

    BASE_SU = 191      # base comune delle due barre (px sopra il fondo dell'area): stessa base, da zero

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        self.fila = vesti(fila_dieci(accese=6), col.accento, col.attenuato)
        giu(a, self.fila, FILA_ALTA)
        self.num6 = numero(self, "6 su 10", "esposti", "Fondo Monetario, 2024")
        su(a, self.num6, NUM_BASSO)
        self.add(self.fila, self.num6)

        # beat 0 — le dieci salgono e si attenuano, il numero esce con le sue etichette, lo slot resta vuoto;
        # al centro si disegna a tratto il bordo frastagliato
        piccola = vesti(self.fila.copy().scale(0.36), col.accento, col.attenuato, 0.4, 0.28)
        giu(a, piccola, 0)
        self.play(Transform(self.fila, piccola), FadeOut(self.num6, shift=DOWN * 0.2), run_time=0.8)
        self.bordo = bordo_frastagliato(col.testo, 540, 230, ampiezza_px=20)
        giu(a, self.bordo, 100)
        self.play(Create(self.bordo), run_time=1.15)

        # beat 1 — due mucchi di sagome minuscole, non contabili; sopra uno, la macchina; sopra l'altro, niente
        self.beat(1)
        self.pile = pile_due(self)
        su(a, self.pile[0], 9, dx_px=-215)
        su(a, self.pile[1], 9, dx_px=-35)
        self.play(LaggedStart(FadeIn(self.pile[0], scale=0.8), FadeIn(self.pile[1], scale=0.8), lag_ratio=0.4),
                  run_time=1.0)
        self.macchina = Icona("bot", altezza_px=60, colore=col.testo)
        su(a, self.macchina, 110, dx_px=-215)
        self.play(FadeIn(self.macchina, shift=DOWN * 0.15), run_time=0.6)

        # beat 2 — diciotto tessere dentro il bordo; due barre che crescono insieme da zero, stessa base e
        # stessa larghezza; il numero si ancora al **divario** fra le due cime, non alla cima alta
        self.beat(2)
        self.tessere = VGroup(*[tessera(self, 52, 30, colore=col.secondario) for _ in range(18)])
        self.tessere.arrange_in_grid(rows=3, cols=6, buff=px(6)).move_to(self.bordo)
        self.play(LaggedStart(*[FadeIn(t, scale=0.5) for t in self.tessere], lag_ratio=0.05), run_time=1.0)
        base = a.y0 + px(self.BASE_SU)
        self.barre = VGroup()
        for dxp, alt, c in ((-215, 170, col.secondario), (-35, 129, col.terziario)):
            b = RoundedRectangle(corner_radius=px(8), width=px(90), height=px(alt), stroke_width=0,
                                 fill_color=c, fill_opacity=1)
            b.move_to([dx(a, dxp), base + px(alt) / 2, 0])
            self.barre.add(b)
        self.play(AnimationGroup(*[GrowFromEdge(b, DOWN) for b in self.barre]),
                  run_time=1.1, rate_func=rate_functions.ease_out_cubic)
        cima_a, cima_b = float(self.barre[0].get_top()[1]), float(self.barre[1].get_top()[1])
        self.graffa = VMobject(stroke_color=col.attenuato, stroke_width=tratto(3))
        self.graffa.set_points_as_corners([np.array([dx(a, -170), cima_a, 0]), np.array([dx(a, -125), cima_a, 0]),
                                           np.array([dx(a, -125), cima_b, 0]), np.array([dx(a, -80), cima_b, 0])])
        self.n32 = numero(self, self.scena["testo"][0], "qualità", "Harvard, 2023")
        self.n32.numero.move_to([dx(a, 240), (cima_a + cima_b) / 2, 0])
        self.n32.etich.next_to(self.n32.numero, DOWN, buff=px(18))
        self.play(Create(self.graffa), FadeIn(self.n32, scale=0.8), run_time=0.8)

        # beat 3 — tessere, barre e il numero con le sue etichette escono **insieme**: nessun numero a schermo.
        # Solo dopo, fuori dal bordo si accende una tessera e sopra di lei pulsa lo stesso «?» della scommessa
        self.beat(3)
        self.play(FadeOut(self.tessere), FadeOut(self.barre), FadeOut(self.graffa),
                  FadeOut(self.n32, shift=DOWN * 0.2), run_time=0.6)
        self.fuori = tessera(self, 72, 42, colore=col.testo)
        giu(a, self.fuori, 236, dx_px=370)
        self.dom = testo("?", "messaggio", colore=col.accento, peso=BOLD)
        giu(a, self.dom, 126, dx_px=370)
        self.play(FadeIn(self.fuori, scale=0.5), run_time=0.4)
        self.play(FadeIn(self.dom, scale=0.7), run_time=0.35)
        self.play(self.dom.animate(rate_func=there_and_back).scale(1.18), run_time=0.9)

        # beat 4 — GRANDE (punch): «Peggio.»; al ritorno croce, spunta e numero con le etichette in una sola
        # animazione, e restano insieme fino all'ultimo fotogramma (⚠️ B)
        self.beat(4)
        self.play(FadeOut(self.dom, scale=1.3), run_time=0.25)
        self.punch("Peggio")
        croce = Croce(altezza_px=72)
        su(a, croce, 182, dx_px=-215)
        spunta = Spunta(altezza_px=72)
        su(a, spunta, 182, dx_px=-35)
        n19 = numero(self, self.scena["testo"][1], "un compito", "Harvard, 2023", scala=1.15)
        giu(a, n19, 356, dx_px=205)
        self.play(AnimationGroup(FadeIn(n19, scale=0.82), croce.entra(), spunta.entra(), lag_ratio=0.2),
                  run_time=1.15)


# ============================================================================================================
def stato_fine_5(sc) -> tuple[VGroup, VGroup]:
    """L'ultimo fotogramma della scena 5, ricostruito: la scena 6 parte da lì (filo visivo)."""
    a, col = sc.area.contenuto, sc.cfg.palette
    fila = vesti(fila_dieci(accese=6).scale(0.36), col.accento, col.attenuato, 0.4, 0.28)
    giu(a, fila, 0)
    bordo = bordo_frastagliato(col.testo, 540, 230, ampiezza_px=20)
    giu(a, bordo, 100)
    macchina = Icona("bot", altezza_px=60, colore=col.testo)
    su(a, macchina, 110, dx_px=-215)
    pile = pile_due(sc)
    su(a, pile[0], 9, dx_px=-215)
    su(a, pile[1], 9, dx_px=-35)
    croce = Croce(altezza_px=72)
    su(a, croce, 182, dx_px=-215)
    spunta = Spunta(altezza_px=72)
    su(a, spunta, 182, dx_px=-35)
    n19 = numero(sc, "−19 punti", "un compito", "Harvard, 2023", scala=1.15)
    giu(a, n19, 356, dx_px=205)
    fuori = tessera(sc, 72, 42, colore=col.testo)
    giu(a, fuori, 236, dx_px=370)
    return VGroup(fila, bordo, macchina, pile, croce, spunta, n19), fuori


SCALA_PICCOLO = 0.55          # i pezzi quando sono in mano alla persona o alla macchina
POS_ICONE = 70                # riga delle due icone (persona e macchina)
POS_RIGA1, POS_RIGA2 = 206, 366   # le due righe dei pezzi


def pezzo_piccolo(sc, i: int, giu_px: float, dx_px: float, colore: str | None = None) -> VGroup:
    p = pezzo_resoconto(sc, i, colore=colore).scale(SCALA_PICCOLO)
    return giu(sc.area.contenuto, p, giu_px, dx_px)


def cluster_6(sc) -> VGroup:
    """La disposizione del beat 2 della scena 6 (persona, macchina, i quattro pezzi, la lente): la scena 7
    riparte da qui, così la dissolvenza fra le due scene non mostra due stati diversi."""
    a, col = sc.area.contenuto, sc.cfg.palette
    persona = giu(a, Icona("user", altezza_px=94, colore=col.testo), POS_ICONE, -220)
    macchina = giu(a, Icona("bot", altezza_px=94, colore=col.testo), POS_ICONE, 220)
    pezzi = [pezzo_piccolo(sc, 0, POS_RIGA1, -313, colore=col.accento),
             pezzo_piccolo(sc, 1, POS_RIGA1, -127),
             pezzo_piccolo(sc, 2, POS_RIGA2, -220),
             pezzo_piccolo(sc, 3, POS_RIGA1, 220)]
    lente = Lente(raggio_px=86, colore=col.testo).move_to(pezzi[0])
    return VGroup(persona, macchina, *pezzi, lente)


def stato_fine_6(sc) -> VGroup:
    """L'ultimo fotogramma della scena 6, ricostruito per la scena 7."""
    a, col = sc.area.contenuto, sc.cfg.palette
    fila = giu(a, vesti(fila_dieci(accese=6).scale(0.36), col.accento, col.attenuato, 1.0, 0.5), 20, -250)
    bordo = giu(a, bordo_frastagliato(col.testo, 280, 170), 14, 170)
    sp = Spunta(altezza_px=54).move_to(bordo)
    cr = Croce(altezza_px=46).move_to([dx(a, 390), bordo.get_center()[1], 0])
    basso = cluster_6(sc).scale(0.78)
    su(a, basso, 110)
    for f in basso:
        attenua(f, 0.5)
    decidi = Etichetta("decidi tu").move_to([dx(a, -200), a.y0 + px(48), 0])
    esempio = etichetta(testo("esempio", "piede", colore=col.attenuato))
    esempio.move_to([dx(a, 280), a.y0 + px(38), 0])
    return VGroup(fila, bordo, sp, cr, basso, decidi, esempio)


class Scena06(ScenaReel):
    """Il resoconto del mese si spezza in quattro: due pezzi alla macchina, due restano a te, e una lente
    ricontrolla. GRANDE (contrasto di scala) sul beat 0: la tessera piccola cresce fino a riempire l'area."""

    POS = {0: (-178, -135), 1: (-178, 135), 2: (178, -135), 3: (178, 135)}   # 0,1 a sinistra · 2,3 a destra

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        vecchio, piccola = stato_fine_5(self)
        self.add(vecchio, piccola)

        # beat 0 — GRANDE (contrasto di scala): la tessera cresce di dieci volte e si spezza in quattro pezzi
        centro_g = np.array([a.centro[0], y_giu(a, 288), 0])
        k = 356 / CARTA_W          # i quattro pezzi chiusi tappezzano la carta grande
        w, h = px(CARTA_W * k), px(CARTA_H * k)
        grande = cornice(self, CARTA_W * k * 2, CARTA_H * k * 2, colore=col.testo, raggio_px=24).move_to(centro_g)
        self.play(FadeOut(vecchio), piccola.animate.move_to(centro_g), run_time=0.6)
        self.play(Transform(piccola, grande), run_time=0.95, rate_func=rimbalzo(0.05))
        self.remove(piccola)
        self.pz = VGroup(*[pezzo_resoconto(self, i, contenuto=False).scale(k) for i in range(4)])
        for i, p in enumerate(self.pz):
            sx = -1 if i in (0, 1) else 1
            sy = 1 if i in (0, 2) else -1
            p.move_to(centro_g + np.array([sx * w / 2, sy * h / 2, 0]))
        self.add(self.pz)
        finali = VGroup(*[pezzo_resoconto(self, i) for i in range(4)])
        for i, p in enumerate(finali):
            p.move_to(centro_g + np.array([px(self.POS[i][0]), px(-self.POS[i][1]), 0]))
            p.rotate((-5 if i % 2 == 0 else 5) * np.pi / 180)
        self.play(LaggedStart(*[Transform(q, f) for q, f in zip(self.pz, finali)], lag_ratio=0.12),
                  run_time=1.2, rate_func=rate_functions.ease_out_cubic)
        self.esempio = etichetta(testo("esempio", "piede", colore=col.attenuato))
        su(a, self.esempio, 118)
        self.play(FadeIn(self.esempio), run_time=0.25)

        # beat 1 — entra la macchina e i due pezzi che le dai (foglio e scaletta) le scivolano sotto
        self.beat(1)
        self.macchina = giu(a, Icona("bot", altezza_px=94, colore=col.testo), POS_ICONE, 220)
        self.play(FadeIn(self.macchina, shift=DOWN * 0.2), run_time=0.35)
        self.play(Transform(self.pz[2], pezzo_piccolo(self, 2, POS_RIGA1, 127)),
                  Transform(self.pz[3], pezzo_piccolo(self, 3, POS_RIGA1, 313)),
                  run_time=1.0, rate_func=rate_functions.ease_in_out_sine)

        # beat 2 — entra la persona, cifre e lampadina si stringono sotto di lei, **solo** il foglio torna
        # indietro (la scaletta resta alla macchina) e la lente lo percorre e si ferma sulle cifre
        self.beat(2)
        self.persona = giu(a, Icona("user", altezza_px=94, colore=col.testo), POS_ICONE, -220)
        self.play(FadeIn(self.persona, shift=DOWN * 0.2), run_time=0.35)
        self.play(Transform(self.pz[0], pezzo_piccolo(self, 0, POS_RIGA1, -313)),
                  Transform(self.pz[1], pezzo_piccolo(self, 1, POS_RIGA1, -127)),
                  run_time=0.7, rate_func=rate_functions.ease_in_out_sine)
        self.play(Transform(self.pz[2], pezzo_piccolo(self, 2, POS_RIGA2, -220)),
                  Transform(self.pz[3], pezzo_piccolo(self, 3, POS_RIGA1, 220)),
                  run_time=0.7, rate_func=rate_functions.ease_in_out_sine)
        self.decidi = Etichetta(piano(self.scena["testo"][0]))
        giu(a, self.decidi, 524, dx_px=-220)
        self.play(FadeIn(self.decidi, scale=0.85), run_time=0.3)
        self.lente = Lente(raggio_px=86, colore=col.testo)
        self.lente.move_to(self.pz[2].get_center() + LEFT * px(70))
        self.play(self.lente.entra(), run_time=0.35)
        self.play(self.lente.animate.move_to(self.pz[0]),
                  Transform(self.pz[0], pezzo_piccolo(self, 0, POS_RIGA1, -313, colore=col.accento)), run_time=0.7)

        # beat 3 — tutto si stringe in basso e si attenua; tornano la fila piccola e il bordo, con la spunta
        # dentro e la croce fuori
        self.beat(3)
        gruppo = VGroup(self.persona, self.macchina, *self.pz, self.lente)
        finale = gruppo.copy().scale(0.78)
        su(a, finale, 110)
        for f in finale:
            attenua(f, 0.5)
        self.play(*[Transform(m, f) for m, f in zip(gruppo, finale)],
                  self.decidi.animate.move_to([dx(a, -200), a.y0 + px(48), 0]),
                  self.esempio.animate.move_to([dx(a, 280), a.y0 + px(38), 0]), run_time=0.8)
        fila = giu(a, vesti(fila_dieci(accese=6).scale(0.36), col.accento, col.attenuato, 1.0, 0.5), 20, -250)
        bordo = giu(a, bordo_frastagliato(col.testo, 280, 170), 14, 170)
        self.play(FadeIn(fila, shift=DOWN * 0.15), Create(bordo), run_time=0.9)
        sp = Spunta(altezza_px=54).move_to(bordo)
        cr = Croce(altezza_px=46).move_to([dx(a, 390), bordo.get_center()[1], 0])
        self.play(AnimationGroup(sp.entra(), cr.entra(), lag_ratio=0.35), run_time=0.85)


# ============================================================================================================
class Scena07(ScenaReel):
    """Chiusura: quei sei restano esposti, e una di loro fa un passo avanti verso il bordo. Non si distingue in
    niente dalle altre cinque (⚠️ J). GRANDE (tipografia cinetica) sul beat 1."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        # continuità: l'ultimo fotogramma della scena 6, ricostruito pezzo per pezzo
        vecchio = stato_fine_6(self)
        self.add(vecchio)

        # beat 0 — esce tutto, e le dieci figure tornano nella posizione e nella scala della scena 2
        self.fila = vesti(fila_dieci(accese=6), col.accento, col.attenuato)
        giu(a, self.fila, FILA_CENTRO)
        self.play(FadeOut(vecchio[1:]), FadeOut(vecchio[0], scale=0.8), run_time=0.5)
        self.play(FadeIn(self.fila, scale=0.9), run_time=0.8, rate_func=rimbalzo(0.05))

        # beat 1 — GRANDE (tipografia cinetica): una si stacca e fa un passo avanti verso il bordo, che rientra
        # piccolo; la fila resta dietro, attenuata, e il messaggio arriva grande
        self.beat(1)
        piccola = vesti(self.fila.copy().scale(0.62), col.accento, col.attenuato, 0.5, 0.3)
        giu(a, piccola, 16, dx_px=-190)
        bordo = bordo_frastagliato(col.testo, 190, 120)
        giu(a, bordo, 10, dx_px=250)
        self.play(Transform(self.fila, piccola), FadeIn(bordo), run_time=0.7)
        self.play(self.fila.figure[4].animate.shift(RIGHT * px(22) + DOWN * px(30)), run_time=0.4)
        self.msg = Messaggio(self.scena["messaggio"], larghezza_px=880)
        giu(a, self.msg, 200)
        self.play(self.msg.per_righe(lag=0.22), run_time=1.1)
        self.cta = Etichetta("Mandalo a chi ha paura\nche l'IA gli tolga il lavoro")
        su(a, self.cta, 14)
        self.play(self.cta.entra(), run_time=0.5)
