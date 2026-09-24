"""Animazioni di «In Italia l'IA per ora non toglie lavoro, apre una forbice»
(contenuti/sceneggiature/2026-09-24-forbice-ia-lavoro.md).

Scene animate: 3, 5, 7, 8. La 1 e la 9 sono il presentatore a volto pieno, la 2, la 4 e la 6 sono filmati
([broll]): nessuna classe. La 3, la 5 e la 7 partono da uno stacco (fotogramma 0 pieno); la 8 riparte
dall'ultimo fotogramma della 7 (`blocco_posti`, `contatore_posti`, `camicia_su`, usati da tutte e due).

Filo visivo: i quadratini-impresa (3), la fabbrica (5 e 7), la forbice delle due linee (5, e piccola in 8: stessa
forma scalata, `pezzi_forbice`), il blocco 10×10 di sagome-persona (7, e i due blocchi della 8).
Coordinate in px dal vertice in alto a sinistra dell'area contenuto (900 × 752): `punto(a, x, y)`.
"""
from __future__ import annotations

import numpy as np
from manim import (BOLD, DOWN, LEFT, PI, RIGHT, UL, UP, AnnularSector, Circle, Create, DashedLine, Dot, FadeIn,
                   FadeOut, GrowFromCenter, GrowFromEdge, Indicate, Line, Rectangle, RoundedRectangle, Square,
                   Transform, UpdateFromAlphaFunc, VGroup, VMobject, linear, smooth, squish_rate_func, there_and_back)

from tools.anim.base import ScenaReel
from tools.anim.componenti import Contatore, ContatoreScorre, Croce, Icona, etichetta, testo
from tools.anim.misure import px, tratto
from tools.anim.pattern import controlla_zoom, rimbalzo


# --- aiuti comuni --------------------------------------------------------------------------------------------

def punto(a, x: float, y: float) -> np.ndarray:
    """Un punto dell'area contenuto, in px dal suo vertice in alto a sinistra (y verso il basso)."""
    return np.array([a.x0 + px(x), a.y1 - px(y), 0.0])


def fin(a: float, b: float, f=smooth):
    """La finestra [a, b] di una play (frazioni della sua durata): più movimenti in una play sola, sfalsati."""
    return squish_rate_func(f, a, b)


def cambia(vecchio, nuovo, a: float, b: float) -> list:
    """Un numero che lascia il posto a un altro nello stesso punto: prima esce, poi entra (mai due insieme)."""
    m = (a + b) / 2
    return [FadeOut(vecchio, shift=UP * px(14), rate_func=fin(a, m)),
            FadeIn(nuovo, shift=UP * px(14), rate_func=fin(m, b))]


def et(s: str, ruolo: str = "etichetta", colore=None, **kw):
    """Un'etichetta di una figura (una-due parole, un numero): marcata per il controllo `parole-leggibili`."""
    return etichetta(testo(s, ruolo, colore=colore, **kw))


# --- la forbice (scena 5, e piccola nella scena 8): una forma sola, scalata ----------------------------------

VALORI = ((24.1, 4.7), (32.5, 7.7), (53.1, 15.7))   # Istat, tavole: grandi e PMI nel 2023, 2024, 2025
PASSO_ANNO_PX = 225
PX_PER_PUNTO = 10.545


def vertici_forbice(origine: np.ndarray, s: float = 1.0) -> list[tuple[np.ndarray, np.ndarray]]:
    """(grandi, PMI) per anno; `origine` è il 2023 a quota zero, `s` la scala."""
    return [(origine + np.array([px(PASSO_ANNO_PX * i * s), px(g * PX_PER_PUNTO * s), 0]),
             origine + np.array([px(PASSO_ANNO_PX * i * s), px(p * PX_PER_PUNTO * s), 0]))
            for i, (g, p) in enumerate(VALORI)]


def pezzi_forbice(scena, origine, s: float = 1.0, grigia: bool = False) -> dict:
    """I pezzi della forbice: due tratti per lama, le due punte e la barra fra le punte (sul 2023).
    Il tratto non si scala: resta lo stesso a ogni misura."""
    col = scena.cfg.palette
    v = vertici_forbice(origine, s)
    c_g = col.attenuato if grigia else col.accento
    c_b = col.attenuato if grigia else col.testo
    lama_g = [Line(v[i][0], v[i + 1][0], stroke_color=c_g, stroke_width=tratto(7)) for i in range(2)]
    lama_p = [Line(v[i][1], v[i + 1][1], stroke_color=col.attenuato, stroke_width=tratto(7)) for i in range(2)]
    r = px(12 if s >= 0.6 else 8)
    punta_g = Dot(v[0][0], radius=r, color=c_g)
    punta_p = Dot(v[0][1], radius=r, color=col.attenuato)
    barra = Line(v[0][1], v[0][0], stroke_color=c_b, stroke_width=tratto(6))
    return {"v": v, "lama_g": lama_g, "lama_p": lama_p, "punta_g": punta_g, "punta_p": punta_p, "barra": barra}


def forbice_intera(scena, origine, s: float, grigia: bool = True) -> VGroup:
    """La forbice finita della scena 5 (punte e barra sul 2025), per il richiamo piccolo della scena 8."""
    p = pezzi_forbice(scena, origine, s, grigia)
    g, q = p["v"][2]
    p["punta_g"].move_to(g)
    p["punta_p"].move_to(q)
    p["barra"].put_start_and_end_on(q, g)
    return VGroup(*p["lama_g"], *p["lama_p"], p["barra"], p["punta_p"], p["punta_g"])


# --- sagome-persona (scene 7 e 8) ------------------------------------------------------------------------------

PASSO_SAGOME = 46


def sagoma(scena, colore=None, opacita: float = 0.75) -> VGroup:
    """Una persona senza ruolo: testa e busto, 32 × 40 px."""
    c = colore or scena.cfg.palette.attenuato
    testa = Circle(radius=px(7), stroke_width=0, fill_color=c, fill_opacity=opacita)
    busto = RoundedRectangle(width=px(32), height=px(23), corner_radius=px(11), stroke_width=0, fill_color=c,
                             fill_opacity=opacita)
    busto.next_to(testa, DOWN, buff=px(3))
    return VGroup(testa, busto)


def blocco_posti(scena, opacita: float = 0.75) -> VGroup:
    """Le 100 sagome della scena 7 (10 × 10), in basso a sinistra."""
    b = VGroup(*[sagoma(scena, opacita=opacita) for _ in range(100)])
    b.arrange_in_grid(rows=10, cols=10, buff=(px(PASSO_SAGOME - 32), px(PASSO_SAGOME - 40)))
    b.move_to(punto(scena.area.contenuto, 40, 250), aligned_edge=UL)
    return b


def contatore_posti(scena, blocco) -> Contatore:
    """Il contatore «100 posti», a destra del blocco e allineato al suo fondo."""
    c = Contatore(100, "posti", colore=scena.cfg.palette.testo)
    c.move_to(np.array([blocco.get_right()[0] + px(74), blocco.get_bottom()[1], 0]), aligned_edge=np.array([-1, -1, 0]))
    return c


def camicia_su(scena, s: VGroup) -> VGroup:
    """La sagoma con il colletto (camicia), in accento, nel posto della sagoma `s`."""
    col = scena.cfg.palette
    c = sagoma(scena, col.accento, 1.0).move_to(s)
    busto = c[1]
    alto = busto.get_top()
    colletto = VMobject(stroke_color=col.sfondo, stroke_width=tratto(3))
    colletto.set_points_as_corners([alto + np.array([-px(7), -px(1), 0]), alto + np.array([0, -px(9), 0]),
                                    alto + np.array([px(7), -px(1), 0])])
    c.add(colletto)
    return c


def casco_su(scena, s: VGroup) -> VGroup:
    """Il casco da cantiere sulla testa di `s`: con lui la sagoma diventa la tuta."""
    col = scena.cfg.palette
    testa = s[0]
    r = testa.width / 2
    calotta = AnnularSector(inner_radius=0, outer_radius=r * 1.2, angle=PI, start_angle=0, stroke_width=0,
                            fill_color=col.attenuato, fill_opacity=1)
    calotta.move_to(testa.get_center() + UP * r * 0.55, aligned_edge=DOWN)
    tesa = Line(calotta.get_corner(DOWN + LEFT) + LEFT * r * 0.35, calotta.get_corner(DOWN + RIGHT) + RIGHT * r * 0.35,
                stroke_color=col.attenuato, stroke_width=tratto(3))
    return VGroup(calotta, tesa)


# --- scena 3 -------------------------------------------------------------------------------------------------

LATO, PASSO = 44, 56


class Scena03(ScenaReel):
    """Su 100 imprese se ne accendono 5, poi 8, poi 16 (la copia degli 8 vola al suo posto); l'Europa sta a 20."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        T = self.inizi_frasi
        quad = VGroup(*[Square(side_length=px(LATO), stroke_width=0, fill_color=col.attenuato, fill_opacity=0.3)
                        for _ in range(100)])
        quad.arrange_in_grid(rows=10, cols=10, buff=px(PASSO - LATO))
        quad.move_to(punto(a, 20, 102), aligned_edge=UL)

        cont = ContatoreScorre(5, "su 100", colore=col.accento)
        cont.move_to(punto(a, 620, 280), aligned_edge=UL)
        domanda = etichetta(testo("?", "messaggio", colore=col.attenuato, peso=BOLD, mono=True))
        domanda.move_to(cont.numero, aligned_edge=LEFT)
        anno = et("2023", "token", col.testo, peso=BOLD, mono=True)
        anno.next_to(cont, DOWN, buff=px(56), aligned_edge=LEFT)
        fonte = VGroup(et("Istat", "piede", col.attenuato), et("≥10 addetti", "piede", col.attenuato))
        fonte.arrange(DOWN, buff=px(10), aligned_edge=LEFT).next_to(anno, DOWN, buff=px(56), aligned_edge=LEFT)

        # beat 0 — «Su cento imprese italiane, quante la usano?»: la griglia c'è già, tutta spenta
        self.add(quad)
        self.play(FadeIn(cont.etich), FadeIn(domanda, scale=0.7), run_time=0.3)
        self.attendi_fino(T[0] + 1.2)   # «cento imprese»: un'onda passa sulle cento, poi tutto fermo (la prova)
        ordine = sorted(range(100), key=lambda k: (k // 10 + k % 10, k))
        self.play(*[quad[k].animate(rate_func=fin(j / 100 * 0.6, j / 100 * 0.6 + 0.4, there_and_back))
                    .scale(1.2).set_fill(opacity=0.6) for j, k in enumerate(ordine)], run_time=1.2)

        # beat 1 — «Istat dice cinque nel duemilaventitré»
        self.beat(1)
        self.play(FadeOut(domanda, rate_func=fin(0, 0.5)), FadeIn(fonte, rate_func=fin(0.2, 1)), run_time=0.4)
        self.attendi_fino(T[1] + 0.4)
        self.play(*[q.animate(rate_func=fin(k * 0.08, k * 0.08 + 0.45)).set_fill(col.accento, opacity=1)
                    for k, q in enumerate(quad[:5])],
                  FadeIn(cont.numero, rate_func=fin(0.3, 0.7)), FadeIn(anno, shift=UP * px(14), rate_func=fin(0.6, 1)),
                  run_time=1.1)

        # beat 2 — «otto nel duemilaventiquattro»
        self.beat(2)
        anno24 = et("2024", "token", col.testo, peso=BOLD, mono=True).move_to(anno, aligned_edge=LEFT)
        self.play(*[q.animate(rate_func=fin(k * 0.12, k * 0.12 + 0.4)).set_fill(col.accento, opacity=1)
                    for k, q in enumerate(quad[5:8])],
                  cont.scorri(8, rate_func=fin(0.1, 0.6, linear)), *cambia(anno, anno24, 0.55, 1.0), run_time=1.0)

        # beat 3 — GRANDE (moltiplicazione) «sedici nel duemilaventicinque»: gli 8 si sdoppiano e la copia vola sui 9-16
        self.beat(3)
        copie = VGroup(*[q.copy() for q in quad[:8]])
        self.add(copie)
        self.play(*[c.animate(rate_func=fin(k * 0.03, k * 0.03 + 0.79)).scale(1.25).shift(UP * px(26))
                    for k, c in enumerate(copie)], run_time=0.3)
        anno25 = et("2025", "token", col.testo, peso=BOLD, mono=True).move_to(anno24, aligned_edge=LEFT)
        self.play(*[c.animate(rate_func=fin(k * 0.05, k * 0.05 + 0.6, rimbalzo(0.08)), path_arc=-0.9)
                    .scale(1 / 1.25).move_to(d) for k, (c, d) in enumerate(zip(copie, quad[8:16]))],
                  cont.scorri(16, rate_func=fin(0.8, 0.92, linear)), *cambia(anno24, anno25, 0.7, 1.0), run_time=1.2)

        # beat 4 — «È raddoppiata in un anno»: ×2, e i due gruppi da 8 fanno un colpo sul posto
        self.beat(4)
        cont.ferma()
        per2 = et("×2", "messaggio", col.accento, peso=BOLD)
        per2.next_to(cont.numero, RIGHT, buff=px(30))
        self.play(FadeIn(per2, scale=0.5, rate_func=fin(0, 0.5, rimbalzo(0.08))),
                  *[Indicate(q, color=col.accento, scale_factor=1.25, rate_func=fin(0.3, 0.75, there_and_back))
                    for q in quad[:8]],
                  *[Indicate(c, color=col.accento, scale_factor=1.25, rate_func=fin(0.5, 0.95, there_and_back))
                    for c in copie], run_time=1.1)

        # beat 5 — «però l'Europa sta a venti»: la linea tratteggiata chiude a 20; i 4 che mancano restano spenti
        self.beat(5)
        y = (quad[10].get_bottom()[1] + quad[20].get_top()[1]) / 2
        x_ue = punto(a, 620, 0)[0]
        linea = DashedLine([quad.get_left()[0] - px(4), y, 0], [x_ue - px(20), y, 0], dash_length=px(14),
                           stroke_color=col.secondario, stroke_width=tratto(4))
        ue = et("UE 20", "token", col.secondario, peso=BOLD)
        ue.move_to([x_ue, y, 0], aligned_edge=LEFT)
        self.play(Create(linea, rate_func=fin(0, 0.6)),
                  *[q.animate(rate_func=fin(0.3, 0.8)).set_fill(opacity=0).set_stroke(col.secondario, width=tratto(3),
                                                                                       opacity=1)
                    for q in quad[16:20]],
                  FadeIn(ue, shift=LEFT * px(16), rate_func=fin(0.5, 1)), run_time=1.1)


# --- scena 5 -------------------------------------------------------------------------------------------------

class Scena05(ScenaReel):
    """Grandi e PMI salgono tutte e due ma si allontanano come lame di forbice (20 → 25 → 37 punti); altrove la
    distanza cala di poco; poi la coppia grigia sparisce e la forbice riempie l'area."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        T = self.inizi_frasi
        base_y = 656
        origine = punto(a, 360, base_y)
        f = pezzi_forbice(self, origine)
        v = f["v"]

        base = Line(punto(a, 300, base_y), punto(a, 880, base_y), stroke_color=col.attenuato, stroke_width=tratto(2),
                    stroke_opacity=0.6)
        anni = VGroup(*[et(s, "token", col.attenuato, mono=True) for s in ("2023", "2024", "2025")])
        for i, t in enumerate(anni):
            t.move_to([v[i][0][0], punto(a, 0, 708)[1], 0])
        cont = ContatoreScorre(20, "punti", colore=col.testo)
        cont.move_to(punto(a, 0, 30), aligned_edge=UL)
        segnaposto = Line(cont.numero.get_corner(DOWN + LEFT) + UP * px(30),
                          cont.numero.get_corner(DOWN + LEFT) + UP * px(30) + RIGHT * px(84),
                          stroke_color=col.attenuato, stroke_width=tratto(6))
        fab_g = Icona("factory", altezza_px=88, colore=col.accento)
        fab_p = Icona("factory", altezza_px=52, colore=col.attenuato)
        fab_g.move_to(punto(a, 0, 230), aligned_edge=UL)
        fab_p.move_to(punto(a, 18, 350), aligned_edge=UL)
        et_g = et("grandi", "etichetta", col.testo).next_to(fab_g, RIGHT, buff=px(20))
        et_p = et("PMI", "etichetta", col.attenuato)
        et_p.move_to([et_g.get_left()[0], fab_p.get_center()[1], 0], aligned_edge=LEFT)
        istat = et("Istat", "piede", col.attenuato)
        istat.move_to(punto(a, 0, 450), aligned_edge=UL)

        # beat 0 — «Istat qui è molto chiara.»: il piano c'è già; entra la fonte e le due fabbriche fanno un colpo
        self.add(base, anni, cont.etich, segnaposto, fab_g, et_g, fab_p, et_p)
        self.play(FadeIn(istat, shift=UP * px(14), rate_func=fin(0, 0.7)),
                  fab_g.animate(rate_func=fin(0, 0.8, there_and_back)).scale(1.18),
                  fab_p.animate(rate_func=fin(0.2, 1, there_and_back)).scale(1.18), run_time=0.6)

        # beat 1 — «La distanza tra imprese grandi e piccole»: le due punte sul 2023 e la barra fra loro
        self.beat(1)
        self.attendi_fino(T[1] + 0.2)
        self.play(GrowFromCenter(f["punta_g"], rate_func=fin(0, 0.3)),
                  GrowFromCenter(f["punta_p"], rate_func=fin(0.15, 0.45)),
                  Create(f["barra"], rate_func=fin(0.4, 0.9)),
                  anni[0].animate(rate_func=fin(0.5, 0.9)).set_color(col.testo), run_time=1.2)
        self.add(f["punta_p"], f["punta_g"])   # le punte sopra la barra

        barra = f["barra"]
        barra.add_updater(lambda m: m.put_start_and_end_on(f["punta_p"].get_center(), f["punta_g"].get_center()))

        # beat 2 — «passa da venti punti a venticinque»: il contatore compare su 20, poi le lame vanno al 2024
        self.beat(2)
        self.attendi_fino(T[2] + 0.25)
        self.play(FadeOut(segnaposto, rate_func=fin(0, 0.4)), FadeIn(cont.numero, rate_func=fin(0.3, 1)), run_time=0.4)
        self.attendi_fino(T[2] + 0.75)
        self.lame(f, 1, cont, 25, anni, 0.8)

        # beat 3 — «poi a trentasette in due anni»: le lame si aprono sul 2025
        self.beat(3)
        self.lame(f, 2, cont, 37, anni, 1.0)
        barra.clear_updaters()
        cont.ferma()

        # beat 4 — «In tanto digitale si stringe.»: esce la legenda e al suo posto, grande quasi quanto la forbice,
        # una coppia grigia fa il movimento opposto: le punte si avvicinano (420 → 190 px) e restano aperte
        self.beat(4)
        la = Line(punto(a, 10, 230), punto(a, 250, 340), stroke_color=col.attenuato, stroke_width=tratto(6))
        lb = Line(punto(a, 10, 650), punto(a, 250, 530), stroke_color=col.attenuato, stroke_width=tratto(6))
        tra = Line(lb.get_start(), la.get_start(), stroke_color=col.attenuato, stroke_width=tratto(5))
        pa = Dot(la.get_start(), radius=px(10), color=col.attenuato)
        pb = Dot(lb.get_start(), radius=px(10), color=col.attenuato)
        tra.add_updater(lambda m: m.put_start_and_end_on(lb.get_end(), la.get_end()))
        pa.add_updater(lambda m: m.move_to(la.get_end()))
        pb.add_updater(lambda m: m.move_to(lb.get_end()))
        self.play(*[FadeOut(m, rate_func=fin(0, 0.2)) for m in (fab_g, et_g, fab_p, et_p, istat)],
                  FadeIn(tra, rate_func=fin(0.2, 0.3)), FadeIn(pa, rate_func=fin(0.2, 0.3)),
                  FadeIn(pb, rate_func=fin(0.2, 0.3)),
                  Create(la, rate_func=fin(0.2, 1)), Create(lb, rate_func=fin(0.2, 1)), run_time=1.6)
        for m in (tra, pa, pb):
            m.clear_updaters()

        # beat 5 — GRANDE (contrasto di scala) «Qui no, si apre.»: la coppia grigia esce con il resto del piano,
        # la forbice cresce fino a riempire l'area e la barra del 37 si accende
        self.beat(5)
        forbice = VGroup(*f["lama_g"], *f["lama_p"], barra, f["punta_p"], f["punta_g"])
        # bersagli in variabili a parte: `.animate` chiama generate_target() e sovrascriverebbe `.target`
        grande = forbice.copy().scale(1.35).move_to(a.centro + DOWN * px(6))
        grande[4].set_stroke(col.accento, width=tratto(10))
        tb = grande[4]
        dove = [tb.get_center()[0] - px(56) - cont.width / 2, tb.get_center()[1] - px(60), 0]
        dentro = cont.copy().move_to(dove)   # il 37 non vola attraverso la lama: si spegne e si riaccende dentro
        self.play(*[FadeOut(m, rate_func=fin(0, 0.3)) for m in (base, anni, la, lb, tra, pa, pb)],
                  Transform(forbice, grande, rate_func=fin(0.25, 0.85)),
                  FadeOut(cont, rate_func=fin(0, 0.25)), FadeIn(dentro, scale=0.8, rate_func=fin(0.7, 1)), run_time=1.1)

    def lame(self, f: dict, i: int, cont, valore: int, anni, durata: float) -> None:
        """Le due lame avanzano fino all'anno i: le punte corrono sulle linee, la barra le segue, il contatore scorre."""
        col = self.cfg.palette
        g, p = f["v"][i]
        self.play(Create(f["lama_g"][i - 1]), Create(f["lama_p"][i - 1]),
                  f["punta_g"].animate.move_to(g), f["punta_p"].animate.move_to(p),
                  anni[i - 1].animate(rate_func=fin(0, 0.5)).set_color(col.attenuato),
                  anni[i].animate(rate_func=fin(0.5, 1)).set_color(col.testo),
                  cont.scorri(valore, rate_func=fin(0.45, 1, linear)), run_time=durata)
        self.add(f["punta_p"], f["punta_g"])


# --- scena 7 -------------------------------------------------------------------------------------------------

ZOOM_07 = 3.0


class Scena07(ScenaReel):
    """La fabbrica che adotta l'IA produce un po' di più; le persone restano cento: una tuta esce, una camicia entra."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        T = self.inizi_frasi
        fab = Icona("factory", altezza_px=100, colore=col.attenuato)
        fab.move_to(punto(a, 40, 10), aligned_edge=UL)
        bi = et("Banca d'Italia", "etichetta", col.attenuato)
        bi.move_to(punto(a, 40, 128), aligned_edge=UL)
        blocco = blocco_posti(self)

        # beat 0 — «Uno studio di Banca d'Italia dice che dove arriva,»: la fabbrica si accende
        self.add(fab, blocco)
        self.play(fab.svg.animate.set_stroke(col.accento), FadeIn(bi, shift=UP * px(12)), run_time=0.5)
        self.attendi_fino(T[0] + 1.9)   # «dove arriva»
        self.play(fab.animate(rate_func=there_and_back).scale(1.12), run_time=0.5)

        # beat 1 — «chi la adotta produce circa il cinque per cento in più per addetto»
        self.beat(1)
        y0, alt = 30, 40
        base = Rectangle(width=px(500), height=px(alt), stroke_width=0, fill_color=col.attenuato, fill_opacity=0.9)
        base.move_to(punto(a, 190, y0), aligned_edge=UL)
        segno = Line(punto(a, 690, y0 - 14), punto(a, 690, y0 + alt + 14), stroke_color=col.testo,
                     stroke_width=tratto(4))
        piu = Rectangle(width=px(25), height=px(alt), stroke_width=0, fill_color=col.accento, fill_opacity=1)
        piu.move_to(punto(a, 690, y0), aligned_edge=UL)
        per_addetto = et("per addetto", "etichetta", col.attenuato)
        per_addetto.move_to(punto(a, 690, y0 + alt + 24), aligned_edge=UP + RIGHT)
        cinque = et("+5%", "token", col.accento, peso=BOLD)
        cinque.move_to(punto(a, 735, y0 + alt / 2), aligned_edge=LEFT)
        self.attendi_fino(T[1] + 0.1)
        self.play(Create(segno, rate_func=fin(0, 0.3)), GrowFromEdge(base, LEFT, rate_func=fin(0.15, 1)),
                  FadeIn(per_addetto, rate_func=fin(0.6, 1)), run_time=1.0)
        self.attendi_fino(T[1] + 1.7)   # «cinque per cento in più»
        self.play(GrowFromEdge(piu, LEFT, rate_func=fin(0, 0.6, rimbalzo(0.3))),
                  FadeIn(cinque, scale=0.6, rate_func=fin(0.3, 1)), run_time=0.7)

        # beat 2 — «e i posti totali, almeno per ora, non scendono»: il contatore fermo su 100, le sagome fanno un colpo
        self.beat(2)
        cont = contatore_posti(self, blocco)
        self.play(FadeIn(cont, shift=UP * px(16)), run_time=0.4)
        self.attendi_fino(T[2] + 2.2)   # «non scendono»
        self.play(*[s.animate(rate_func=there_and_back).scale(1.18) for s in blocco], run_time=0.5)

        # beat 3 — GRANDE (contrasto di scala) «Si spostano verso profili più qualificati»: via il resto, zoom
        # sull'angolo del blocco con il contatore in quadro; la tuta esce, la camicia entra, torna la vista intera
        self.beat(3)
        ultima = blocco[99]
        fuoco = VGroup(ultima, cont)
        controlla_zoom(self, [fuoco], ZOOM_07)
        self.play(*[FadeOut(m, rate_func=fin(0, 0.45)) for m in (fab, bi, base, segno, piu, per_addetto, cinque)],
                  self.zoom_su(fuoco, ZOOM_07), run_time=0.6)
        casco = casco_su(self, ultima)
        ultima_scura = ultima.copy().set_fill(opacity=0.4)
        # il casco è grigio pieno, il busto si scurisce: la tuta si riconosce senza lampi di bianco
        self.play(FadeIn(casco, shift=DOWN * px(6)), Transform(ultima, ultima_scura), run_time=0.35)
        self.wait(0.25)
        # dissolvenza incrociata: la tuta scende e sbiadisce mentre la camicia compare al suo posto (sempre 100)
        tuta = VGroup(ultima, casco)
        camicia = camicia_su(self, blocco_posti(self)[99])
        self.play(FadeOut(tuta, shift=DOWN * px(22), rate_func=fin(0, 0.8)),
                  FadeIn(camicia, scale=0.7, rate_func=fin(0.2, 1, rimbalzo(0.2))), run_time=0.55)
        blocco.remove(ultima)
        self.remove(casco)
        self.play(self.torna(), run_time=0.45)


# --- scena 8 -------------------------------------------------------------------------------------------------

PASSO_8 = 38


def blocco_8(scena, x: float, opacita: float = 0.75) -> VGroup:
    """Un blocco di 100 sagome della scena 8: lo stesso della 7, più piccolo (passo 38 invece di 46)."""
    b = blocco_posti(scena, opacita)
    b.scale(PASSO_8 / PASSO_SAGOME)
    b.move_to(punto(scena.area.contenuto, x, 240), aligned_edge=UL)
    return b


def porta(scena) -> VGroup:
    """Una porta chiusa, neutra: un rettangolo alto con la maniglia."""
    col = scena.cfg.palette
    anta = RoundedRectangle(width=px(72), height=px(240), corner_radius=px(6), stroke_color=col.attenuato,
                            stroke_width=tratto(3), fill_color=col.attenuato, fill_opacity=0.24)
    maniglia = Dot(anta.get_right() + LEFT * px(16), radius=px(6), color=col.attenuato)
    return VGroup(anta, maniglia)


class Scena08(ScenaReel):
    """Fra le persone si accendono 30 su 100 contro 12 (la forbice piccola si illumina, ferma); poi su sei porte su
    dieci cade una croce."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        T = self.inizi_frasi

        # fotogramma 0: l'ultimo della scena 7
        blocco = blocco_posti(self)
        camicia = camicia_su(self, blocco[99])
        blocco.remove(blocco[99])
        blocco.add(camicia)
        cont = contatore_posti(self, blocco_posti(self))
        self.add(blocco, cont)

        sx, dx = blocco_8(self, 50), blocco_8(self, 482)
        copia = dx.copy()
        partenza, arrivo = sx.get_center(), dx.get_center()

        def esce(m, t):
            u = smooth(t)
            m.move_to(partenza + (arrivo - partenza) * u)
            m.set_fill(opacity=0.75 * min(1.0, max(0.0, (u - 0.45) / 0.55)))
        mini = forbice_intera(self, np.zeros(3), 0.25)
        mini.move_to(punto(a, 450, 78))
        tastiera = Icona("keyboard", altezza_px=56, colore=col.attenuato)
        tastiera.move_to(punto(a, 50, 172), aligned_edge=UL)
        persona = Icona("user", altezza_px=56, colore=col.attenuato)
        persona.move_to(punto(a, 482, 172), aligned_edge=UL)

        # beat 0 — «E la stessa forbice c'è tra persone.»: il blocco torna neutro e si divide in due; torna la forbice
        self.play(FadeOut(cont, rate_func=fin(0, 0.12)),
                  Transform(blocco, sx, rate_func=fin(0.1, 0.4)),
                  UpdateFromAlphaFunc(copia, esce, rate_func=fin(0.35, 0.7, linear)),
                  FadeIn(mini, rate_func=fin(0.45, 0.75)),
                  FadeIn(tastiera, rate_func=fin(0.55, 0.85)), FadeIn(persona, rate_func=fin(0.6, 0.9)),
                  run_time=2.0)

        # beat 1 — «Inapp dice che la usa il trenta per cento di chi lavora da remoto»
        self.beat(1)
        inapp = et("Inapp", "piede", col.attenuato)
        inapp.move_to(punto(a, 450, 710))
        l30 = VGroup(et("30%", "token", col.accento, peso=BOLD), et("da remoto", "etichetta", col.attenuato))
        l30.arrange(RIGHT, buff=px(16), aligned_edge=DOWN).move_to(punto(a, 50, 632), aligned_edge=UL)
        self.play(FadeIn(inapp, rate_func=fin(0, 0.2)),
                  *[s.animate(rate_func=fin(0.5 + (k // 10) * 0.08, 0.5 + (k // 10) * 0.08 + 0.2))
                    .set_fill(col.accento, opacity=1) for k, s in enumerate(blocco[:30])],
                  FadeIn(l30, shift=UP * px(12), rate_func=fin(0.75, 1)), run_time=2.2)

        # beat 2 — «dodici tra gli altri.»: 12 a destra; la forbice in alto resta ferma e si illumina soltanto
        self.beat(2)
        l12 = VGroup(et("12%", "token", col.accento, peso=BOLD), et("altri", "etichetta", col.attenuato))
        l12.arrange(RIGHT, buff=px(16), aligned_edge=DOWN).move_to(punto(a, 482, 632), aligned_edge=UL)
        self.play(*[s.animate(rate_func=fin((k // 10) * 0.1, (k // 10) * 0.1 + 0.35)).set_fill(col.accento, opacity=1)
                    for k, s in enumerate(copia[:12])],
                  FadeIn(l12, shift=UP * px(12), rate_func=fin(0.25, 0.6)),
                  mini.animate(rate_func=fin(0.5, 1, there_and_back)).set_color(col.accento), run_time=1.3)

        # beat 3 — «E Istat dice che quasi sei imprese su dieci, tra quelle che ci hanno pensato,»: dieci porte neutre
        self.beat(3)
        porte = VGroup(*[porta(self) for _ in range(10)]).arrange(RIGHT, buff=px(16))
        porte.move_to(punto(a, 18, 210), aligned_edge=UL)
        x0, x1 = porte[0].get_left()[0], porte[5].get_right()[0]
        yb = porte.get_bottom()[1] - px(28)
        graffa = VMobject(stroke_color=col.attenuato, stroke_width=tratto(3))
        graffa.set_points_as_corners([[x0, yb + px(14), 0], [x0, yb, 0], [x1, yb, 0], [x1, yb + px(14), 0]])
        n586 = et("58,6%", "messaggio", col.testo, peso=BOLD, mono=True)
        n586.move_to([x0, yb - px(24), 0], aligned_edge=UL)
        istat = et("Istat", "piede", col.attenuato)
        istat.next_to(n586, DOWN, buff=px(16), aligned_edge=LEFT)
        via = (blocco, copia, tastiera, persona, l30, l12, inapp)
        self.play(*[FadeOut(m, rate_func=fin(0, 0.1)) for m in via],
                  *[FadeIn(p, shift=UP * px(20), rate_func=fin(0.1 + k * 0.035, 0.1 + k * 0.035 + 0.15))
                    for k, p in enumerate(porte)],
                  FadeIn(istat, rate_func=fin(0.15, 0.3)),
                  Create(graffa, rate_func=fin(0.5, 0.7)),
                  FadeIn(n586, shift=UP * px(14), rate_func=fin(0.6, 0.8)), run_time=3.0)

        # beat 4 — GRANDE (carica e rimbalzo) «si fermano perché mancano competenze.»: su sei porte cade una croce
        self.beat(4)
        croci = [Croce(altezza_px=56).move_to(p[0].get_center() + UP * px(20)) for p in porte[:6]]
        self.play(*[FadeIn(c, shift=DOWN * px(60), scale=1.3, rate_func=fin(k * 0.1, k * 0.1 + 0.4, rimbalzo(0.1)))
                    for k, c in enumerate(croci)],
                  *[p[0].animate(rate_func=fin(k * 0.1 + 0.15, k * 0.1 + 0.4)).set_fill(opacity=0.06)
                    .set_stroke(opacity=0.55) for k, p in enumerate(porte[:6])], run_time=1.7)
