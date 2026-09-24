"""Animazioni di «Prima di comprare una GPU, conta le ore»
(contenuti/sceneggiature/2026-09-24-gpu-comprare-affittare.md).

Scene animate: 2, 4, 6, 8. La 1 e la 9 sono il presentatore a volto pieno, la 3, la 5 e la 7 sono filmati ([broll]):
nessuna classe. La 2 parte da uno stacco dal volto pieno (fotogramma 0 pieno); la 4, la 6 e la 8 arrivano da un
filmato e ripartono dall'ultimo fotogramma della scena animata prima (`mondo_2`, `mondo_4`, `mondo_6`, usati da tutte e
due le scene del raccordo).

Filo visivo: la sagoma della scheda (`scheda`, una forma sola scalata: 2, 6, 8), i moduli di memoria (2 e 4), il
cartellino del prezzo (`cartellino`: nasce nella 2, torna piccolo nella 8 e si spezza in 36 fettine), il contatore
(il cartellino che corre, il quadrante del tassametro, il calendario delle ore). Codice dei colori: accento =
affitto (e «guarda qui»), grigio = comprare, testo = la scheda di casa accesa.
Coordinate in px dal vertice in alto a sinistra dell'area contenuto (900 × 752): `punto(a, x, y)`.
"""
from __future__ import annotations

import numpy as np
from manim import (BOLD, DOWN, LEFT, ORIGIN, RIGHT, TAU, UP, ArcBetweenPoints, Circle, Create, CubicBezier,
                   DashedLine, Dot, FadeIn, FadeOut, GrowFromCenter, GrowFromEdge, Indicate, Line, MoveToTarget, Polygon,
                   Rectangle, Restore, Rotate, RoundedRectangle, Transform, ValueTracker, VGroup, always_redraw, linear, rush_into,
                   smooth, squish_rate_func)

from tools.anim.base import ScenaReel
from tools.anim.componenti import ContatoreScorre, etichetta, testo
from tools.anim.misure import px, tratto
from tools.anim.pattern import rimbalzo


# --- aiuti comuni --------------------------------------------------------------------------------------------

def punto(a, x: float, y: float) -> np.ndarray:
    """Un punto dell'area contenuto, in px dal suo vertice in alto a sinistra (y verso il basso)."""
    return np.array([a.x0 + px(x), a.y1 - px(y), 0.0])


def fin(a: float, b: float, f=smooth):
    """La finestra [a, b] di una play (frazioni della sua durata): più movimenti in una play sola, sfalsati."""
    return squish_rate_func(f, a, b)


# I TESTO delle scene che vengono ricostruite nella scena dopo (una scena vede solo i propri dati): la scena che li
# mostra per prima li prende da `self.scena`, e `testi_di` controlla che siano ancora questi.
TESTI = {2: ["32 GB", "5.300 €"], 4: ["domanda", "offerta"], 6: ["1,06 €/h", "0,18 €/h"]}


def testi_di(scena, n: int) -> list[str]:
    """I TESTO della scena n: quelli della sceneggiatura se la scena è la n, altrimenti la copia qui sopra."""
    if scena.scena.get("n") == n and scena.scena.get("testo"):
        assert list(scena.scena["testo"]) == TESTI[n], f"TESTO della scena {n} cambiato: aggiorna TESTI"
    return TESTI[n]


def et(s: str, ruolo: str = "etichetta", colore=None, **kw):
    """Un'etichetta di una figura (una-due parole, un numero): marcata per il controllo `parole-leggibili`."""
    return etichetta(testo(s, ruolo, colore=colore, **kw))


# --- la scheda: una forma sola, scalata (il tratto non si scala) ---------------------------------------------

SCHEDA_L, SCHEDA_H = 560, 220


def ventola(colore, r: float = 82) -> VGroup:
    """Una ventola: cerchio, mozzo e cinque pale curve. Il cerchio è il pezzo [0] (centro e misura della ventola)."""
    cerchio = Circle(radius=px(r), stroke_color=colore, stroke_width=tratto(4))
    mozzo = Circle(radius=px(18), stroke_color=colore, stroke_width=tratto(4))
    pale = []
    for k in range(5):
        a0 = k * TAU / 5
        p1 = np.array([np.cos(a0), np.sin(a0), 0]) * px(24)
        p2 = np.array([np.cos(a0 + 0.9), np.sin(a0 + 0.9), 0]) * px(r - 10)
        pale.append(ArcBetweenPoints(p1, p2, angle=-0.9, stroke_color=colore, stroke_width=tratto(3)))
    return VGroup(cerchio, mozzo, *pale)


def scheda(scena, larghezza_px: float = SCHEDA_L, colore=None) -> VGroup:
    """La sagoma della scheda: corpo scuro, staffa a sinistra, due ventole. `.corpo`, `.staffa`, `.ventole`."""
    col = scena.cfg.palette
    c = colore or col.testo
    corpo = RoundedRectangle(width=px(SCHEDA_L), height=px(SCHEDA_H), corner_radius=px(22), stroke_color=c,
                             stroke_width=tratto(4), fill_color=col.sfondo, fill_opacity=1)
    staffa = RoundedRectangle(width=px(20), height=px(256), corner_radius=px(6), stroke_color=c, stroke_width=tratto(4),
                              fill_color=col.sfondo, fill_opacity=1).move_to(corpo.get_left() + LEFT * px(8))
    v1, v2 = ventola(c).move_to(LEFT * px(135)), ventola(c).move_to(RIGHT * px(135))
    g = VGroup(staffa, corpo, v1, v2)
    g.scale(larghezza_px / SCHEDA_L)
    g.corpo, g.staffa, g.ventole = corpo, staffa, VGroup(v1, v2)
    return g


def metti_scheda(s: VGroup, centro: np.ndarray) -> VGroup:
    """Porta la scheda con il centro del corpo in `centro`."""
    return s.shift(centro - s.corpo.get_center())


def colora_scheda(s: VGroup, colore, ventole: bool = True, opacita: float = 1.0, **kw) -> list:
    """Le animazioni che cambiano il colore della scheda (accesa, spenta). `ventole=False` se nella stessa play le
    ventole girano con `Rotate` (due animazioni sullo stesso oggetto: vale solo l'ultima)."""
    anim = [s.corpo.animate(**kw).set_stroke(colore, opacity=opacita),
            s.staffa.animate(**kw).set_stroke(colore, opacity=opacita)]
    if ventole:
        anim += [v.animate(suspend_mobject_updating=False, **kw).set_stroke(colore, opacity=opacita)
                 for v in s.ventole]
    return anim


def fai_girare(scena, ventole, fino_s: float | None = None, giri_s: float = 0.3) -> None:
    """Le ventole girano piano fino a `fino_s` (di default la fine della scena) e si fermano su un angolo multiplo di
    72°: la ventola ferma è identica a quella disegnata, così la scena dopo la ricostruisce uguale. L'angolo dipende
    dal tempo della scena, non dai fotogrammi: una play che sposta la scheda (con `suspend_mobject_updating=False`)
    non la fa scattare."""
    t0 = scena.t
    fine = scena.durata_s if fino_s is None else fino_s
    passo = TAU / 5
    durata = max(0.1, fine - t0)
    w = max(1, round(TAU * giri_s * durata / passo)) * passo / durata
    for v in ventole:
        base = v.copy()
        c0, r0 = misura_ventola(base)

        def gira(m, dt, base=base, c0=c0, r0=r0):
            c, r = misura_ventola(m)
            nuova = base.copy().rotate(-w * (min(scena.t, fine) - t0), about_point=c0)
            nuova.scale(r / r0, about_point=c0).shift(c - c0)
            nuova.match_style(m)
            m.become(nuova)
        v.add_updater(gira)


def misura_ventola(v) -> tuple[np.ndarray, float]:
    """Centro e raggio del cerchio della ventola dai suoi punti: il riquadro d'ingombro cambia un poco ruotando (i punti
    di controllo delle curve stanno fuori dal cerchio), e un fattore di scala preso da lì si accumulerebbe."""
    c = v[0].get_center_of_mass()
    return c, float(np.linalg.norm(v[0].points[0] - c))


def ferma(ventole) -> None:
    for v in ventole:
        v.clear_updaters()


# --- i moduli di memoria (scene 2 e 4) -----------------------------------------------------------------------

MODULO_L, MODULO_H = 110, 44


def modulo(scena, colore=None) -> VGroup:
    """Un modulo di memoria (come l'icona memory-stick): il corpo e i piedini sotto. Il corpo è il pezzo [0]."""
    c = colore or scena.cfg.palette.attenuato
    corpo = RoundedRectangle(width=px(MODULO_L), height=px(MODULO_H), corner_radius=px(6), stroke_color=c,
                             stroke_width=tratto(3))
    piedini = VGroup(*[Line(UP * 0, DOWN * px(8), stroke_color=c, stroke_width=tratto(3)) for _ in range(6)])
    piedini.arrange(RIGHT, buff=px(14)).next_to(corpo, DOWN, buff=0)
    return VGroup(corpo, piedini)


def pesi_modulo(scena, m: VGroup) -> VGroup:
    """Gli 8 × 3 quadratini che riempiono un modulo fino all'orlo."""
    q = VGroup(*[Rectangle(width=px(9.5), height=px(9.5), stroke_width=0, fill_color=scena.cfg.palette.attenuato,
                           fill_opacity=0.9) for _ in range(24)])
    q.arrange_in_grid(rows=3, cols=8, buff=px(2.5))
    return q.move_to(m[0])


# --- il cartellino del prezzo (scene 2 e 8) ------------------------------------------------------------------

CART_L, CART_H, CART_TAGLIO = 220, 92, 28


def numero_prezzo(scena, s: str) -> VGroup:
    return etichetta(testo(s, "token", colore=scena.cfg.palette.accento, peso=BOLD, mono=True))


def cartellino(scena, s: str = "5.300 €", scala: float = 1.0) -> VGroup:
    """Il cartellino appeso: forma con gli angoli alti tagliati, foro, il prezzo. Il vertice alto al centro è in
    ORIGIN prima di `scala`; `.forma`, `.foro`, `.num`, `.aggancio()` (il punto del foro dove arriva il filo)."""
    col = scena.cfg.palette
    W, H, T = px(CART_L), px(CART_H), px(CART_TAGLIO)
    forma = Polygon([-W / 2 + T, 0, 0], [W / 2 - T, 0, 0], [W / 2, -T, 0], [W / 2, -H, 0], [-W / 2, -H, 0],
                    [-W / 2, -T, 0], stroke_color=col.accento, stroke_width=tratto(4), fill_color=col.sfondo,
                    fill_opacity=1)
    foro = Circle(radius=px(7), stroke_color=col.accento, stroke_width=tratto(3)).move_to([0, -px(14), 0])
    num = numero_prezzo(scena, s).move_to([0, -(T + H) / 2 - px(4), 0])
    g = VGroup(forma, foro, num)
    g.scale(scala, about_point=ORIGIN)
    g.forma, g.foro, g.num = forma, foro, num
    g.aggancio = lambda: foro.get_top()
    return g


# --- scena 2: la scheda, i pesi, il prezzo -------------------------------------------------------------------

S2_SCHEDA = (450, 232)       # centro del corpo, a fine scena (dopo che il cartellino l'ha tirata giù)
S2_GIU = 164                 # di quanto sta più in basso nei beat 0-1 (sopra c'è il posto per il blocco dei pesi)
S2_CEDE = 30                 # di quanto si abbassa sotto il peso del cartellino
S2_FILO_X = 580
S2_GONFIO = 2.2


def mondo_2(scena) -> dict:
    """L'ultimo fotogramma della scena 2 (e il primo della 4): scheda con i quattro moduli pieni, «32 GB», il filo,
    il cartellino gonfio con «5.300 €», «esempio · 24/09»."""
    a = scena.area.contenuto
    testi = testi_di(scena, 2)
    s = metti_scheda(scheda(scena), punto(a, *S2_SCHEDA))
    alto = s.corpo.get_top()[1]
    moduli = []
    for k in range(4):
        m = modulo(scena, scena.cfg.palette.testo)
        m.move_to(punto(a, 450 + (k - 1.5) * 130, 0), aligned_edge=DOWN)
        m.shift(UP * (alto - m.get_bottom()[1]))
        moduli.append(m)
    pesi = [pesi_modulo(scena, m) for m in moduli]
    gb = et(testi[0], "caption", colore=scena.cfg.palette.testo, peso=BOLD)
    gb.move_to(punto(a, 190, 368), aligned_edge=UP + LEFT)
    cart = cartellino(scena, testi[1], S2_GONFIO)
    cart.move_to(punto(a, S2_FILO_X, 372), aligned_edge=UP)
    filo = Line(np.array([punto(a, S2_FILO_X, 0)[0], s.corpo.get_bottom()[1], 0]), cart.aggancio(),
                stroke_color=scena.cfg.palette.testo, stroke_width=tratto(3))
    nota = et(f"esempio · {data_prezzo()}", "etichetta", colore=scena.cfg.palette.attenuato)
    nota.next_to(cart, DOWN, buff=px(16))
    return {"scheda": s, "moduli": moduli, "pesi": pesi, "gb": gb, "cart": cart, "filo": filo, "nota": nota}


def data_prezzo() -> str:
    return "24/09"


class Scena02(ScenaReel):
    """La scheda da 32 GB: i moduli si accendono, un blocco di pesi li riempie, il cartellino corre fino a 5.300 € e
    si gonfia tirando giù la scheda (carica e rimbalzo)."""

    def costruisci(self):
        a, col, T = self.area.contenuto, self.cfg.palette, self.inizi_frasi
        m = mondo_2(self)
        s, moduli, pesi, gb = m["scheda"], m["moduli"], m["pesi"], m["gb"]
        giu = DOWN * px(S2_GIU)
        for x in (s, gb, *moduli, *pesi):
            x.shift(giu)
        for mo in moduli:
            mo.set_stroke(col.attenuato)
        # fotogramma 0 pieno: la scheda con le ventole che girano e i moduli spenti
        self.add(s, *moduli)
        fai_girare(self, s.ventole)

        # beat 0 — «Se punti a una scheda da trentadue giga»: i moduli si accendono uno dopo l'altro, poi «32 GB»
        self.play(*[mo.animate(rate_func=fin(0.1 + 0.2 * k, 0.4 + 0.2 * k)).set_stroke(col.accento)
                    for k, mo in enumerate(moduli)], run_time=self.arrotonda(1.2))
        self.attendi_fino(T[0] + 1.2)
        self.play(FadeIn(gb, shift=UP * px(14)), run_time=self.arrotonda(0.4))

        # beat 1 — «la più grande fra le schede da gioco»: il blocco di pesi scende e riempie i moduli fino all'orlo
        self.beat(1)
        blocco = VGroup(*[Rectangle(width=px(26), height=px(26), stroke_width=0, fill_color=col.attenuato,
                                    fill_opacity=0.9) for _ in range(96)])
        blocco.arrange_in_grid(rows=6, cols=16, buff=px(5))
        blocco.move_to(punto(a, 450, 14), aligned_edge=UP)
        self.play(FadeIn(blocco, shift=DOWN * px(40)), run_time=self.arrotonda(0.4))
        self.wait(0.1)
        # il blocco scende sulla fila dei moduli e ci si schiaccia dentro (copre i moduli), poi si ordina nei quattro
        fila = VGroup(*[mo[0] for mo in moduli])
        self.play(blocco.animate(rate_func=rush_into).stretch_to_fit_height(fila.height * 0.8)
                  .stretch_to_fit_width(fila.width).move_to(fila), run_time=self.arrotonda(0.45))
        bersagli = []
        for i in range(96):
            r, c = divmod(i, 16)
            k, lc = divmod(c, 4)
            bersagli.append(pesi[k][r * 4 + lc])
        self.play(*[Transform(blocco[i], bersagli[i], rate_func=fin(0.01 * (i % 16), 0.7 + 0.01 * (i % 16)))
                    for i in range(96)],
                  *[mo.animate(rate_func=fin(0.8, 1)).set_stroke(col.testo) for mo in moduli],
                  run_time=self.arrotonda(0.6))
        self.remove(blocco)
        self.add(*pesi)

        # beat 2 — «oggi in Italia la trovi intorno ai cinquemilatrecento euro»: la scheda sale, il cartellino si
        # appende, il prezzo corre, e sull'ultima cifra il cartellino si gonfia e tira giù la scheda
        self.beat(2)
        su = UP * px(S2_GIU + S2_CEDE)
        corpo_scheda = VGroup(s, gb, *moduli, *pesi)
        self.play(corpo_scheda.animate(suspend_mobject_updating=False).shift(su), run_time=self.arrotonda(0.5))
        cart = m["cart"]
        piccolo = cartellino(self, "0 €", 1.0).move_to(cart.get_top() + UP * px(S2_CEDE), aligned_edge=UP)
        filo = Line(m["filo"].get_start() + UP * px(S2_CEDE), piccolo.aggancio(), stroke_color=col.testo,
                    stroke_width=tratto(3))
        self.play(Create(filo, rate_func=fin(0, 0.5)), FadeIn(piccolo, shift=DOWN * px(16), rate_func=fin(0.35, 1)),
                  run_time=self.arrotonda(0.4))
        prezzo = ValueTracker(0)
        centro_num = piccolo.num.get_center().copy()

        def corri(n):
            v = int(round(prezzo.get_value() / 100.0)) * 100
            s_ = f"{v:,}".replace(",", ".") + " €"
            if s_ != getattr(n, "_scritto", None):
                nuovo = numero_prezzo(self, s_).move_to(centro_num)
                n.become(nuovo)
                n._scritto = s_
                for vecchia, adesso in zip(n.righe, nuovo.righe, strict=False):
                    vecchia.piano = adesso.piano
                etichetta(n)
        piccolo.num.add_updater(corri)
        fine_corsa = T[2] + 0.68 * self.durata_beat(2)
        self.play(prezzo.animate.set_value(5300), run_time=self.arrotonda(max(0.8, fine_corsa - self.t)),
                  rate_func=rush_into)
        piccolo.num.clear_updaters()
        # sull'ultima cifra: il cartellino si gonfia (rimbalzo corto, resta nell'area) e la scheda cede sotto il peso
        grande = cart.copy()
        self.play(Transform(piccolo, grande, rate_func=rimbalzo(0.05)),
                  filo.animate(rate_func=rimbalzo(0.05)).put_start_and_end_on(m["filo"].get_start(), m["filo"].get_end()),
                  corpo_scheda.animate(suspend_mobject_updating=False, rate_func=rimbalzo(0.05)).shift(DOWN * px(S2_CEDE)),
                  run_time=self.arrotonda(0.5))
        self.play(FadeIn(m["nota"], shift=UP * px(10)), run_time=self.arrotonda(0.3))


# --- scena 4: la memoria di Micron ---------------------------------------------------------------------------

ANNI = {"2026": 140, "2027": 420, "2028": 700}
ASSE_Y = 640
X_INIZIO, X_2028, X_FINE = 80, 700, 860


def domanda_y(x: float) -> float:
    return 500 - 0.35 * (x - X_INIZIO)


def offerta_y(x: float) -> float:
    """L'offerta sale più piano della domanda; dopo il 2028 (tratteggiata) un po' più decisa, ma non la tocca."""
    if x <= X_2028:
        return 590 - 0.2 * (x - X_INIZIO)
    return offerta_y(X_2028) - 0.55 * (x - X_2028)


def fascia(scena, x0: float, x1: float, opacita: float = 0.22) -> Polygon:
    """Il vuoto fra domanda e offerta, da x0 a x1, nel colore caldo."""
    a = scena.area.contenuto
    xs = np.linspace(x0, max(x1, x0 + 0.5), 2)
    alto = [punto(a, x, domanda_y(x)) for x in xs]
    basso = [punto(a, x, offerta_y(x)) for x in reversed(xs)]
    return Polygon(*alto, *basso, stroke_width=0, fill_color=scena.cfg.palette.accento, fill_opacity=opacita)


def memoria_4(scena, moduli, pesi) -> list[VGroup]:
    """I quattro moduli pieni, piccoli, in fila in alto a sinistra (il simbolo della memoria nella scena 4)."""
    a = scena.area.contenuto
    out = []
    for k, (m, p) in enumerate(zip(moduli, pesi)):
        g = VGroup(m, p).copy().scale(0.45)
        g.move_to(punto(a, 26 + k * 58, 30))
        out.append(g)
    return out


def mondo_4(scena, finale: bool = True) -> dict:
    """I pezzi della scena 4. Con `finale` nello stato dell'ultimo fotogramma (primo della 6): il grafico attenuato e
    il tratto del 2028 acceso."""
    a, col = scena.area.contenuto, scena.cfg.palette
    m2 = mondo_2(scena)
    mem = VGroup(*memoria_4(scena, m2["moduli"], m2["pesi"]))
    micron = et("Micron, 2026", "etichetta", colore=col.testo)
    micron.next_to(mem, RIGHT, buff=px(24))
    asse = Line(punto(a, 40, ASSE_Y), punto(a, 880, ASSE_Y), stroke_color=col.attenuato, stroke_width=tratto(4))
    tacche = VGroup(*[Line(punto(a, x, ASSE_Y - 10), punto(a, x, ASSE_Y + 10), stroke_color=col.attenuato,
                           stroke_width=tratto(4)) for x in ANNI.values()])
    anni = VGroup(*[et(s, "etichetta", colore=col.attenuato).move_to(punto(a, x, ASSE_Y + 38)) for s, x in ANNI.items()])
    dom = Line(punto(a, X_INIZIO, domanda_y(X_INIZIO)), punto(a, X_2028, domanda_y(X_2028)), stroke_color=col.accento,
               stroke_width=tratto(7))
    off = Line(punto(a, X_INIZIO, offerta_y(X_INIZIO)), punto(a, X_2028, offerta_y(X_2028)),
               stroke_color=col.attenuato, stroke_width=tratto(7))
    testi = testi_di(scena, 4)
    et_dom = et(testi[0], "etichetta", colore=col.accento, peso=BOLD)
    et_dom.move_to(punto(a, 470, domanda_y(470) - 44), aligned_edge=LEFT)
    et_off = et(testi[1], "etichetta", colore=col.testo, peso=BOLD)
    et_off.move_to(punto(a, 470, offerta_y(470) + 44), aligned_edge=LEFT)
    dom2 = Line(punto(a, X_2028, domanda_y(X_2028)), punto(a, X_FINE, domanda_y(X_FINE)), stroke_color=col.accento,
                stroke_width=tratto(7))
    off2 = DashedLine(punto(a, X_2028, offerta_y(X_2028)), punto(a, X_FINE, offerta_y(X_FINE)),
                      dash_length=px(16), dashed_ratio=0.55, stroke_color=col.testo, stroke_width=tratto(7))
    band = fascia(scena, X_INIZIO, X_2028)
    band2 = fascia(scena, X_2028, X_FINE, 0.3)
    p = {"mem": mem, "micron": micron, "asse": asse, "tacche": tacche, "anni": anni, "band": band, "dom": dom,
         "off": off, "et_dom": et_dom, "et_off": et_off, "band2": band2, "dom2": dom2, "off2": off2}
    if finale:
        for k in ("dom", "off", "band", "mem", "micron"):
            p[k].fade(0.55)
        for k in (0, 1):
            p["anni"][k].fade(0.55)
        p["tacche"][2].set_stroke(col.accento)
        p["anni"][2].set_color(col.accento)
    return p


def ordine_4(p: dict) -> list:
    """L'ordine di disegno dei pezzi della scena 4 (fasce sotto, testi sopra)."""
    return [p[k] for k in ("band", "band2", "asse", "tacche", "anni", "off", "off2", "dom", "dom2", "et_dom", "et_off",
                           "mem", "micron")]


class Scena04(ScenaReel):
    """Micron: la domanda di memoria sopra l'offerta oltre il 2027; zoom sul 2028, dove l'offerta (tratteggiata) sale
    un po' più decisa ma non la tocca (contrasto di scala)."""

    def costruisci(self):
        a, col, T = self.area.contenuto, self.cfg.palette, self.inizi_frasi
        m2 = mondo_2(self)
        # fotogramma 0: l'ultimo della scena 2
        self.add(m2["filo"], m2["scheda"], *m2["moduli"], *m2["pesi"], m2["gb"], m2["cart"], m2["nota"])
        p = mondo_4(self, finale=False)
        mem = [VGroup(mo, pe) for mo, pe in zip(m2["moduli"], m2["pesi"])]
        for g, dest in zip(mem, p["mem"]):
            g.target = dest.copy()

        # beat 0 — «Micron, giugno 2026, dice una cosa molto semplice»: via prezzo e scheda, i moduli salgono in alto a
        # sinistra e diventano il simbolo della memoria; poi la linea del tempo
        self.play(FadeOut(m2["cart"], scale=0.8, rate_func=fin(0, 0.4, rush_into)),
                  FadeOut(m2["filo"], rate_func=fin(0, 0.3)), FadeOut(m2["nota"], rate_func=fin(0, 0.3)),
                  FadeOut(m2["scheda"], rate_func=fin(0.05, 0.45)), FadeOut(m2["gb"], rate_func=fin(0.05, 0.4)),
                  *[MoveToTarget(g, rate_func=fin(0.2 + 0.04 * k, 0.72 + 0.04 * k)) for k, g in enumerate(mem)],
                  FadeIn(p["micron"], shift=RIGHT * px(16), rate_func=fin(0.9, 1)),
                  run_time=self.arrotonda(1.1))
        # i moduli arrivati sono identici al simbolo di `mondo_4`: si scambiano senza che si veda
        self.remove(*m2["moduli"], *m2["pesi"])
        self.add(p["mem"])
        self.play(Create(p["asse"], rate_func=fin(0, 0.7)), FadeIn(p["tacche"], rate_func=fin(0.4, 0.8)),
                  FadeIn(p["anni"], shift=UP * px(10), rate_func=fin(0.5, 1)), run_time=self.arrotonda(1.0))
        self.attendi_fino(T[0] + 2.2)
        self.play(Indicate(p["micron"], scale_factor=1.08, color=col.testo), run_time=self.arrotonda(0.6))
        # «dice una cosa molto semplice»: un punto corre sulla linea del tempo dal 2026 al 2028 e si spegne
        corsa = Dot(punto(a, ANNI["2026"], ASSE_Y), radius=px(9), color=col.accento)
        self.play(FadeIn(corsa, scale=0.5, rate_func=fin(0, 0.12)),
                  corsa.animate(rate_func=fin(0, 0.85, linear)).move_to(punto(a, ANNI["2028"], ASSE_Y)),
                  run_time=self.arrotonda(1.2))
        self.play(FadeOut(corsa, scale=0.5), run_time=self.arrotonda(0.2))

        # beat 1 — «La domanda di memoria resta sopra l'offerta oltre il 2027»: le due linee avanzano insieme,
        # il vuoto fra le due si colora
        self.beat(1)
        xt = ValueTracker(X_INIZIO + 1)
        band = always_redraw(lambda: fascia(self, X_INIZIO, xt.get_value()))
        self.add(band)
        self.bring_to_back(band)
        durata = self.arrotonda(min(2.6, 0.7 * self.durata_beat(1)))
        self.play(Create(p["dom"], rate_func=linear), Create(p["off"], rate_func=linear),
                  xt.animate(rate_func=linear).set_value(X_2028),
                  FadeIn(p["et_dom"], shift=UP * px(10), rate_func=fin(0.62, 0.82)),
                  FadeIn(p["et_off"], shift=DOWN * px(10), rate_func=fin(0.72, 0.92)),
                  run_time=durata)
        band.clear_updaters()

        # beat 2 — «E l'aria cambia piano solo nel 2028»: zoom sul 2028, il resto si attenua, l'offerta diventa
        # tratteggiata e sale un po' più decisa senza toccare la domanda; poi si torna al grafico intero
        self.beat(2)
        fuoco = Dot(punto(a, 675, 470), radius=0.01)
        self.play(FadeOut(p["mem"]), FadeOut(p["micron"]), run_time=self.arrotonda(0.2))
        self.play(self.zoom_su(fuoco, 1.6),
                  *[x.animate.fade(0.55) for x in (p["dom"], p["off"], band, p["anni"][0], p["anni"][1])],
                  p["tacche"][2].animate.set_stroke(col.accento), p["anni"][2].animate.set_color(col.accento),
                  run_time=self.arrotonda(0.7))
        self.play(Create(p["dom2"]), Create(p["off2"]), FadeIn(p["band2"], rate_func=fin(0.3, 1)),
                  run_time=self.arrotonda(0.9))
        self.wait(0.3)
        p["mem"].fade(0.55)
        p["micron"].fade(0.55)
        self.play(self.torna(), FadeIn(p["mem"], rate_func=fin(0.4, 1)), FadeIn(p["micron"], rate_func=fin(0.4, 1)),
                  run_time=self.arrotonda(0.6))


# --- scena 6: affitto al secondo contro corrente di casa ------------------------------------------------------

S6_SX, S6_DX = 215, 685                      # centri delle due metà
S6_SCHEDA_L = 250
S6_METRO_Y = 470
GIRI_AFFITTO = (-0.8 * TAU, -0.35 * TAU)     # quanto corre il quadrante dell'affitto nelle due accensioni


def quadrante(scena, centro: np.ndarray, colore_lancetta) -> VGroup:
    """Il quadrante del tassametro: cerchio, lancetta (il pezzo [1]) e perno."""
    c = scena.cfg.palette.testo
    cerchio = Circle(radius=px(30), stroke_color=c, stroke_width=tratto(4)).move_to(centro)
    lancetta = Line(centro, centro + UP * px(22), stroke_color=colore_lancetta, stroke_width=tratto(4))
    perno = Dot(centro, radius=px(5), color=c)
    return VGroup(cerchio, lancetta, perno)


def tassametro(scena, cx: float, cifra: str | None, colore_cifra) -> dict:
    """Riquadro, quadrante, cifra e «€/h» centrati in (cx, S6_METRO_Y). Con `cifra=None` la cifra la mette chi chiama
    (il contatore che scorre), nel punto `sx_cifra`."""
    a, col = scena.area.contenuto, scena.cfg.palette
    riq = RoundedRectangle(width=px(420), height=px(120), corner_radius=px(22), stroke_color=col.attenuato,
                           stroke_width=tratto(3), fill_color=col.sfondo, fill_opacity=1)
    riq.move_to(punto(a, cx, S6_METRO_Y))
    campione = testo("0,00", "messaggio", peso=BOLD, mono=True)
    unita = et("€/h", "caption", colore=col.testo)
    larga = px(60) + px(22) + campione.width + px(14) + unita.width
    x0 = riq.get_center()[0] - larga / 2
    quad = quadrante(scena, np.array([x0 + px(30), riq.get_center()[1], 0]), colore_cifra)
    sx_cifra = x0 + px(60) + px(22)
    num = None
    if cifra is not None:
        num = etichetta(testo(cifra, "messaggio", colore=colore_cifra, peso=BOLD, mono=True))
        num.move_to([sx_cifra, riq.get_center()[1], 0], aligned_edge=LEFT)
    unita.move_to([sx_cifra + campione.width + px(14), 0, 0], aligned_edge=LEFT)
    unita.align_to(campione.move_to([sx_cifra, riq.get_center()[1], 0], aligned_edge=LEFT), DOWN)
    return {"riq": riq, "quad": quad, "num": num, "unita": unita, "sx_cifra": sx_cifra, "cy": riq.get_center()[1]}


def armadio(scena, cx: float) -> VGroup:
    """L'armadio dei server: il contorno e tre unità impilate (la scheda va in quella di mezzo)."""
    a, col = scena.area.contenuto, scena.cfg.palette
    c = col.attenuato
    fuori = RoundedRectangle(width=px(340), height=px(360), corner_radius=px(14), stroke_color=c, stroke_width=tratto(4))
    fuori.move_to(punto(a, cx, 200))
    unita = VGroup()
    for y, h in ((52, 60), (200, 164), (348, 60)):
        u = RoundedRectangle(width=px(300), height=px(h), corner_radius=px(8), stroke_color=c, stroke_width=tratto(3))
        u.move_to(punto(a, cx, y))
        unita.add(u)
        if h < 100:
            for k in range(3):
                unita.add(Dot(u.get_left() + RIGHT * px(26 + 20 * k), radius=px(5), color=c))
            unita.add(Line(u.get_center() + LEFT * px(20), u.get_right() + LEFT * px(24), stroke_color=c,
                           stroke_width=tratto(3)))
    return VGroup(fuori, unita)


def casa(scena, cx: float) -> VGroup:
    """La casa: il contorno con il tetto, vuoto finché non entra la scheda."""
    a, col = scena.area.contenuto, scena.cfg.palette
    pts = [(cx - 150, 380), (cx - 150, 120), (cx - 172, 120), (cx, 22), (cx + 172, 120), (cx + 150, 120), (cx + 150, 380)]
    g = Polygon(*[punto(a, x, y) for x, y in pts], stroke_color=col.attenuato, stroke_width=tratto(4))
    return VGroup(g)


def spina(scena, s: VGroup) -> VGroup:
    """Il cavo che scende dalla scheda di casa fino alla spina infilata nella presa sul muro (la presa ha i due fori,
    la spina il corpo e i due denti)."""
    a, col = scena.area.contenuto, scena.cfg.palette
    inizio = s.corpo.get_right() + DOWN * px(20) + LEFT * px(6)
    presa_c = punto(a, S6_DX + 112, 340)
    presa = RoundedRectangle(width=px(40), height=px(56), corner_radius=px(10), stroke_color=col.testo,
                             stroke_width=tratto(4), fill_color=col.sfondo, fill_opacity=1).move_to(presa_c)
    fori = VGroup(*[Dot(presa_c + UP * d, radius=px(4), color=col.testo) for d in (px(10), -px(10))])
    corpo, denti = forma_spina(scena, col.testo)
    VGroup(corpo, denti).next_to(presa, LEFT, buff=0)
    fine = corpo.get_left()
    cavo = CubicBezier(inizio, inizio + RIGHT * px(30) + DOWN * px(20), fine + LEFT * px(40), fine,
                       stroke_color=col.testo, stroke_width=tratto(4))
    return VGroup(presa, cavo, corpo, denti, fori)


def forma_spina(scena, colore, scala: float = 1.0) -> VGroup:
    """La spina: corpo e due denti verso destra (scene 6 e 8, stessa forma; il tratto non si scala)."""
    col = scena.cfg.palette
    corpo = RoundedRectangle(width=px(34), height=px(38), corner_radius=px(6), stroke_color=colore,
                             stroke_width=tratto(4), fill_color=col.sfondo, fill_opacity=1)
    denti = VGroup(*[Line(corpo.get_right() + UP * d, corpo.get_right() + UP * d + RIGHT * px(14),
                          stroke_color=colore, stroke_width=tratto(5)) for d in (px(10), -px(10))])
    g = VGroup(corpo, denti)
    g.scale(scala)
    return g


def spia(scena, s: VGroup, colore) -> Dot:
    """La spia della scheda, nell'angolo in alto a destra del corpo."""
    return Dot(s.corpo.get_corner(UP + RIGHT) + (LEFT + DOWN) * px(16), radius=px(7), color=colore)


def mondo_6(scena) -> dict:
    """L'ultimo fotogramma della scena 6 (e il primo della 8): a sinistra l'armadio con la scheda spenta e il
    tassametro a 1,06; a destra la casa con la scheda accesa, la spina e il contatore a 0,18."""
    a, col = scena.area.contenuto, scena.cfg.palette
    testi = testi_di(scena, 6)
    cifre = [t.split()[0] for t in testi]
    arm = armadio(scena, S6_SX)
    s_aff = metti_scheda(scheda(scena, S6_SCHEDA_L, col.attenuato), punto(a, S6_SX, 200))
    t_aff = tassametro(scena, S6_SX, cifre[0], col.accento)
    t_aff["quad"][1].rotate(sum(GIRI_AFFITTO), about_point=t_aff["quad"][0].get_center())
    f_aff = et("RunPod + IVA", "etichetta", colore=col.attenuato).move_to(punto(a, S6_SX, 570))
    ca = casa(scena, S6_DX)
    s_casa = metti_scheda(scheda(scena, S6_SCHEDA_L, col.testo), punto(a, S6_DX, 240))
    sp = spina(scena, s_casa)
    spia_aff = spia(scena, s_aff, col.attenuato)
    spia_casa = spia(scena, s_casa, col.terziario)
    t_casa = tassametro(scena, S6_DX, cifre[1], col.testo)
    f_casa = et("ARERA", "etichetta", colore=col.attenuato).move_to(punto(a, S6_DX, 570))
    return {"arm": arm, "s_aff": s_aff, "t_aff": t_aff, "f_aff": f_aff, "casa": ca, "s_casa": s_casa, "spina": sp,
            "t_casa": t_casa, "f_casa": f_casa, "spia_aff": spia_aff, "spia_casa": spia_casa}


def pezzi_tassametro(t: dict) -> list:
    return [t["riq"], t["quad"], t["unita"]] + ([t["num"]] if t["num"] is not None else [])


class Scena06(ScenaReel):
    """Affitto contro casa: il tassametro corre solo quando la scheda in affitto è accesa; «al secondo» arriva enorme
    e spinge tutto (tipografia cinetica); a casa la scheda è sempre attaccata alla spina, 0,18 €/h."""

    def costruisci(self):
        a, col, T = self.area.contenuto, self.cfg.palette, self.inizi_frasi
        # fotogramma 0: l'ultimo della scena 4
        p4 = mondo_4(self, finale=True)
        self.add(*ordine_4(p4))
        m = mondo_6(self)
        t_aff, t_casa = m["t_aff"], m["t_casa"]
        quad_aff = t_aff["quad"]
        quad_aff[1].rotate(-sum(GIRI_AFFITTO), about_point=quad_aff[0].get_center())

        # beat 0 — «in affitto quella stessa scheda sta a circa un euro l'ora, con iva»: via il grafico, entra
        # l'armadio con la scheda; poi il tassametro a 1,06; la scheda si accende e il quadrante corre, si spegne e
        # si ferma, due volte; la fonte
        self.play(*[FadeOut(x, shift=LEFT * px(40), rate_func=fin(0, 0.45)) for x in ordine_4(p4)],
                  FadeIn(m["arm"], shift=LEFT * px(30), rate_func=fin(0.4, 0.85)),
                  FadeIn(m["s_aff"], shift=LEFT * px(30), rate_func=fin(0.45, 0.9)),
                  FadeIn(m["spia_aff"], shift=LEFT * px(30), rate_func=fin(0.45, 0.9)),
                  FadeIn(m["casa"], rate_func=fin(0.6, 1)),
                  run_time=self.arrotonda(0.9))
        self.attendi_fino(T[0] + 1.3)
        self.play(*[FadeIn(x, shift=UP * px(14)) for x in pezzi_tassametro(t_aff)], run_time=self.arrotonda(0.5))
        self.attendi_fino(T[0] + 2.4)
        centro_q = quad_aff[0].get_center()
        for k, (giro, acceso, spento) in enumerate(zip(GIRI_AFFITTO, (0.8, 0.4), (0.3, 0.3))):
            s = m["s_aff"]
            self.play(*colora_scheda(s, col.accento, ventole=False, rate_func=fin(0, 0.2)),
                      t_aff["riq"].animate(rate_func=fin(0, 0.2)).set_stroke(col.accento),
                      m["spia_aff"].animate(rate_func=fin(0, 0.15)).set_color(col.accento),
                      *[Rotate(v, -2 * TAU / 5 if k == 0 else -TAU / 5, about_point=v[0].get_center(), rate_func=smooth)
                        for v in s.ventole],
                      Rotate(quad_aff[1], giro, about_point=centro_q, rate_func=linear),
                      run_time=self.arrotonda(acceso))
            self.play(*colora_scheda(s, col.attenuato), t_aff["riq"].animate.set_stroke(col.attenuato),
                      m["spia_aff"].animate.set_color(col.attenuato),
                      run_time=self.arrotonda(0.2))
            self.wait(spento - 0.2)
        self.play(FadeIn(m["f_aff"], shift=UP * px(10)), run_time=self.arrotonda(0.3))

        # beat 1 — «e si paga al secondo»: «al secondo» arriva enorme e spinge le due metà in piccolo e in grigio
        self.beat(1)
        mondo = VGroup(m["arm"], m["s_aff"], m["spia_aff"], *pezzi_tassametro(t_aff), m["casa"])
        mondo.save_state()
        m["f_aff"].save_state()
        parola = testo("al secondo", "punto", colore=col.accento, peso=BOLD)
        parola.scale_to_fit_width(px(820)).move_to(punto(a, 450, 628))
        cima = punto(a, 450, 0)
        self.attendi_fino(T[1] + 0.25)
        self.play(GrowFromCenter(parola, rate_func=rimbalzo(0.05)),
                  mondo.animate(rate_func=fin(0, 0.8)).scale(0.8, about_point=cima).fade(0.6),
                  m["f_aff"].animate(rate_func=fin(0, 0.5)).scale(0.8, about_point=cima).set_opacity(0),
                  run_time=self.arrotonda(0.5))

        # beat 2 — «A casa la corrente pesa circa diciotto centesimi l'ora»: «al secondo» si ritira, le metà tornano;
        # a destra entra la scheda di casa con la spina, si accende e il contatore scorre lento fino a 0,18
        self.beat(2)
        self.play(FadeOut(parola, scale=0.3, shift=DOWN * px(30), rate_func=fin(0, 0.5, rush_into)),
                  Restore(mondo, rate_func=fin(0.25, 1)), Restore(m["f_aff"], rate_func=fin(0.55, 1)),
                  run_time=self.arrotonda(0.5))
        s_casa, sp = m["s_casa"], m["spina"]
        for x in (s_casa.corpo, s_casa.staffa, *s_casa.ventole):
            x.set_stroke(col.attenuato)
        spia_casa = m["spia_casa"].set_color(col.attenuato)
        self.play(FadeIn(s_casa, shift=DOWN * px(30), rate_func=fin(0, 0.6)),
                  FadeIn(spia_casa, shift=DOWN * px(30), rate_func=fin(0, 0.6)),
                  FadeIn(sp[0], sp[4], rate_func=fin(0.2, 0.6)), Create(sp[1], rate_func=fin(0.4, 0.85)),
                  FadeIn(sp[2], sp[3], shift=RIGHT * px(14), rate_func=fin(0.6, 1)),
                  run_time=self.arrotonda(0.7))
        fai_girare(self, s_casa.ventole)
        # la scheda di casa si accende e la sua spia resta accesa fissa (quella dell'affitto si accende e si spegne)
        self.play(*colora_scheda(s_casa, col.testo), spia_casa.animate.set_color(col.terziario),
                  run_time=self.arrotonda(0.3))
        conta = ContatoreScorre(0, None, decimali=2, colore=col.testo)
        conta.move_to([t_casa["sx_cifra"], t_casa["cy"], 0], aligned_edge=LEFT)
        self.play(*[FadeIn(x, shift=UP * px(14)) for x in (t_casa["riq"], t_casa["quad"], t_casa["unita"])],
                  FadeIn(conta, shift=UP * px(14)), run_time=self.arrotonda(0.4))
        quad_casa = t_casa["quad"]
        self.play(conta.scorri(0.18, rate_func=linear),
                  Rotate(quad_casa[1], -TAU, about_point=quad_casa[0].get_center(), rate_func=linear),
                  run_time=self.arrotonda(1.2))
        conta.ferma()
        self.play(FadeIn(m["f_casa"], shift=UP * px(10)), run_time=self.arrotonda(0.3))


# --- scena 8: il conto su tre anni ---------------------------------------------------------------------------

O8 = (140, 390)               # origine del grafico
PX_ORA, PX_EURO = 700 / 300, 1.0
QUOTA, AFFITTO_H, CASA_H = 5300 / 36, 1.0585, 0.1819   # €/mese, €/h (1,06 con IVA), €/h di corrente
ORE_PAREGGIO = QUOTA / (AFFITTO_H - CASA_H)            # ≈ 168 h/mese
S8_SCHEDA = (310, 52)
S8_SCHEDA_L = 160
S8_CART = 0.85


def g8(a, ore: float, euro: float) -> np.ndarray:
    return punto(a, O8[0] + ore * PX_ORA, O8[1] - euro * PX_EURO)


class Scena08(ScenaReel):
    """Il conto: il cartellino si spezza in 36 fettine, una fa il punto dei 150 € al mese; la linea dell'affitto si
    disegna ripida e taglia quella del comprare a 170 ore (rivelazione a tratto); il calendario pieno per 5,5 ore al
    giorno. Ultima scena animata: un passaggio per frase, finale fermo."""

    def costruisci(self):
        a, col, T = self.area.contenuto, self.cfg.palette, self.inizi_frasi
        testi = self.scena.get("testo") or ["170 h", "esempio"]
        # fotogramma 0: l'ultimo della scena 6
        m6 = mondo_6(self)
        s = m6["s_casa"]
        fuori = [m6["arm"], m6["s_aff"], m6["spia_aff"], *pezzi_tassametro(m6["t_aff"]), m6["f_aff"], m6["casa"],
                 m6["spina"], m6["spia_casa"], *pezzi_tassametro(m6["t_casa"]), m6["f_casa"]]
        self.add(m6["arm"], m6["s_aff"], m6["spia_aff"], *pezzi_tassametro(m6["t_aff"]), m6["f_aff"], m6["casa"], s,
                 m6["spina"], m6["spia_casa"], *pezzi_tassametro(m6["t_casa"]), m6["f_casa"])
        fai_girare(self, s.ventole, fino_s=T[3] - 0.1 + 0.85)

        # il grafico
        asse_x = Line(g8(a, 0, 0), g8(a, 310, 0), stroke_color=col.attenuato, stroke_width=tratto(4))
        asse_y = Line(g8(a, 0, 0), g8(a, 0, 350), stroke_color=col.attenuato, stroke_width=tratto(4))
        e_mese = et("€/mese", "etichetta", colore=col.attenuato)
        e_mese.move_to(punto(a, 0, 20), aligned_edge=LEFT)
        o_mese = et("ore/mese", "etichetta", colore=col.attenuato)
        o_mese.move_to(g8(a, 310, 0) + UP * px(30), aligned_edge=RIGHT)
        esempio = et(f"{testi[1]} · 3 anni", "etichetta", colore=col.attenuato)
        esempio.move_to(punto(a, 895, 22), aligned_edge=RIGHT)
        # la scheda nell'angolo con il suo cartellino (lo stesso della scena 2, piccolo)
        s_dest = metti_scheda(scheda(self, S8_SCHEDA_L, col.testo), punto(a, *S8_SCHEDA))
        cart = cartellino(self, "5.300 €", S8_CART)
        cart.move_to(s_dest.corpo.get_bottom() + DOWN * px(18), aligned_edge=UP)
        filo = Line(s_dest.corpo.get_bottom(), cart.aggancio(), stroke_color=col.testo, stroke_width=tratto(3))

        # beat 0 — «Se fai un esempio su tre anni»: via l'armadio e la casa; la scheda di casa va nell'angolo e le
        # riappare il cartellino; entrano gli assi
        s.generate_target()
        s.target.become(s_dest)
        # il primo cambio al primo fotogramma: il mondo della 6 sfuma mentre la scheda va nell'angolo e gli assi entrano
        self.play(*[FadeOut(x, rate_func=fin(0, 0.25, linear)) for x in fuori],
                  MoveToTarget(s, rate_func=fin(0, 0.45), suspend_mobject_updating=False),
                  Create(asse_x, rate_func=fin(0.15, 0.55)), Create(asse_y, rate_func=fin(0.15, 0.55)),
                  Create(filo, rate_func=fin(0.45, 0.58)), FadeIn(cart, shift=DOWN * px(12), rate_func=fin(0.5, 0.72)),
                  FadeIn(e_mese, rate_func=fin(0.5, 0.8)), FadeIn(o_mese, rate_func=fin(0.5, 0.8)),
                  FadeIn(esempio, rate_func=fin(0.6, 0.9)),
                  run_time=self.arrotonda(1.4))

        # beat 1 — «quella scheda ti pesa circa centocinquanta euro al mese prima ancora di usarla»: il cartellino si
        # spezza in 36 fettine; una vola sull'asse e diventa il punto dei 150 €; da lì la linea del comprare
        self.beat(1)
        forma = cart.forma
        l_f = forma.width / 36
        fettine = VGroup(*[Rectangle(width=l_f * 0.92, height=forma.height * 0.94, stroke_width=0,
                                     fill_color=col.attenuato, fill_opacity=0) for _ in range(36)])
        fettine.arrange(RIGHT, buff=l_f * 0.08).move_to(forma)
        aperte = fettine.copy().arrange(RIGHT, buff=px(2.4)).move_to(forma)
        punto150 = Dot(g8(a, 0, QUOTA), radius=px(10), color=col.testo)
        e150 = et("150 €", "etichetta", colore=col.testo, peso=BOLD, mono=True)
        e150.move_to(g8(a, 0, QUOTA) + LEFT * px(20), aligned_edge=RIGHT)
        compra = Line(g8(a, 0, QUOTA), g8(a, 300, QUOTA + 300 * CASA_H), stroke_color=col.attenuato,
                      stroke_width=tratto(7))
        # la spina (la stessa della scena 6, piccola e grigia) attaccata con un filo alla linea del comprare: la linea
        # sale per la corrente
        ore_sp = 245
        attacco = g8(a, ore_sp, QUOTA + ore_sp * CASA_H)
        sp8 = forma_spina(self, col.attenuato, 1.1)
        sp8.move_to(attacco + DOWN * px(72))
        filo_sp = Line(attacco, sp8[0].get_top(), stroke_color=col.attenuato, stroke_width=tratto(3))
        self.add(fettine)
        self.attendi_fino(T[1] + 0.2)
        # una animazione sola per fettina: le 35 si aprono a ventaglio, la prima vola sull'asse e diventa il punto
        self.play(FadeOut(cart.num, rate_func=fin(0, 0.12)), FadeOut(cart.foro, rate_func=fin(0, 0.12)),
                  FadeOut(forma, rate_func=fin(0.04, 0.2)),
                  *[fettine[i].animate(rate_func=fin(0.04, 0.34)).move_to(aperte[i]).set_fill(opacity=1)
                    for i in range(1, 36)],
                  Transform(fettine[0], punto150, rate_func=fin(0.1, 0.55)),
                  FadeIn(e150, shift=RIGHT * px(10), rate_func=fin(0.5, 0.66)),
                  Create(compra, rate_func=fin(0.6, 0.92)),
                  Create(filo_sp, rate_func=fin(0.84, 0.94)), FadeIn(sp8, shift=UP * px(10), rate_func=fin(0.88, 1)),
                  run_time=self.arrotonda(2.6))

        # beat 2 — «Comprare conviene sopra circa centosettanta ore al mese»: la linea dell'affitto si disegna da zero,
        # ripida, e taglia quella del comprare; l'incrocio si accende, 170 h; le due zone si colorano
        self.beat(2)
        affitta = Line(g8(a, 0, 0), g8(a, 300, 300 * AFFITTO_H), stroke_color=col.accento, stroke_width=tratto(7))
        inc = g8(a, ORE_PAREGGIO, ORE_PAREGGIO * AFFITTO_H)
        p_inc = Dot(inc, radius=px(11), color=col.accento)
        anello = Circle(radius=px(34), stroke_color=col.accento, stroke_width=tratto(5)).move_to(inc)
        giu = DashedLine(inc, g8(a, ORE_PAREGGIO, 0), dash_length=px(10), stroke_color=col.accento,
                         stroke_width=tratto(3))
        e170 = et(testi[0], "caption", colore=col.accento, peso=BOLD, mono=True)
        e170.move_to(g8(a, ORE_PAREGGIO, 0) + DOWN * px(34))
        zona_aff = Polygon(g8(a, 0, QUOTA), inc, g8(a, 0, 0), stroke_width=0, fill_color=col.accento, fill_opacity=0.2)
        zona_comp = Polygon(inc, g8(a, 300, 300 * AFFITTO_H), g8(a, 300, QUOTA + 300 * CASA_H), stroke_width=0,
                            fill_color=col.attenuato, fill_opacity=0.25)
        self.attendi_fino(T[2] + 0.3)
        self.play(FadeIn(zona_aff, rate_func=fin(0.72, 1)), FadeIn(zona_comp, rate_func=fin(0.78, 1)),
                  Create(affitta, rate_func=fin(0, 0.45, linear)),
                  GrowFromCenter(p_inc, rate_func=fin(0.4, 0.5)), Create(anello, rate_func=fin(0.45, 0.7)),
                  FadeIn(giu, rate_func=fin(0.5, 0.65)), FadeIn(e170, shift=UP * px(10), rate_func=fin(0.55, 0.75)),
                  run_time=self.arrotonda(2.2))
        for z in (zona_aff, zona_comp):
            self.bring_to_back(z)

        # beat 3 — «più di cinque ore al giorno»: il calendario del mese, ogni giorno pieno per 5,5 ore su 24;
        # la scheda nell'angolo si spegne
        self.beat(3)
        celle, pieni = VGroup(), VGroup()
        for g in range(30):
            # una casella per giorno, alta: le 24 ore in verticale, la parte piena è 5,5/24 in accento
            r, c = divmod(g, 10)
            cella = RoundedRectangle(width=px(38), height=px(80), corner_radius=px(6), stroke_color=col.attenuato,
                                     stroke_width=tratto(3))
            cella.move_to(punto(a, O8[0] + 19 + c * 44, 518 + r * 88))
            h = px(80 - 6) * 5.5 / 24
            pieno = Rectangle(width=px(38 - 6), height=h, stroke_width=0, fill_color=col.accento, fill_opacity=1)
            pieno.move_to(cella.get_bottom() + UP * (px(3) + h / 2))
            celle.add(cella)
            pieni.add(pieno)
        e55 = et("5,5 h/giorno", "caption", colore=col.testo, peso=BOLD)
        e55.move_to(punto(a, 604, 606), aligned_edge=LEFT)
        self.play(*[FadeIn(c_, rate_func=fin(0.01 * i, 0.25 + 0.01 * i)) for i, c_ in enumerate(celle)],
                  *[GrowFromEdge(p_, DOWN, rate_func=fin(0.3 + 0.012 * i, 0.5 + 0.012 * i)) for i, p_ in enumerate(pieni)],
                  FadeIn(e55, shift=LEFT * px(10), rate_func=fin(0.55, 0.85)),
                  *colora_scheda(s, col.attenuato, opacita=0.45, rate_func=fin(0.8, 1)),
                  run_time=self.arrotonda(1.0))
        ferma(s.ventole)
