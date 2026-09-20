"""Animazioni di «Generativa non vuol dire creativa» (contenuti/sceneggiature/2026-09-20-generativa-probabile.md).

Le scene 1 e 5 sono a filmato: non hanno una classe. Le scene 2 e 6 arrivano da uno stacco netto: fotogramma 0 pieno.
Filo visivo: le tre schede in alto, le tre linee nel varco fra schede e foglio, il foglio «prima | dopo» (sopra il
confine la richiesta, sotto la mail, dietro la mail una pila di fogli senza testo), la didascalia degli inventati.

Regola del presentatore (2026-09-20): niente testo denso che resta. Ogni riga lunga è una `Fuoco`: i suoi segmenti
sono testo solo nel beat in cui la VOCE ne parla, altrimenti barrette-sagoma; le caselle dei segnaposto restano.

Tecnica: tutto quello che una scena mostra sta in un solo gruppo (`mondo`), già al suo posto; ciò che non si vede ha
opacità zero. Ogni passaggio è una sola animazione `Tappe` con finestre che non si accavallano: prima esce il testo
vecchio, poi si muovono i riquadri, poi entra il nuovo (docs/animazioni.md §10).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Callable

import numpy as np
from manim import (BOLD, DOWN, LEFT, ORIGIN, RIGHT, UP, Animation, Brace, CubicBezier, DashedLine, DashedVMobject, Dot,
                   Line, Mobject, MoveAlongPath, Rectangle, RoundedRectangle, VGroup, linear, rate_functions, rush_from,
                   rush_into, smooth, there_and_back)

from tools.anim.base import ScenaReel
from tools.anim.componenti import Etichetta, Icona, Messaggio, Punch, Token, piano, testo, tratto
from tools.anim.misure import px

# --- i testi (alla lettera dalle Note di produzione e dall'idea) ---------------------------------------------------------
# tipo di segmento: "t" resta testo nello stato ridotto · "b" diventa barretta · "c" casella del segnaposto · "p" «[…]»

SCHEDE = [("Ilaria, 26", ["reception", "di un", "campeggio"]), ("Dario, 43", ["banco di una", "ferramenta"]),
          ("Nadia, 35", ["cassa e", "reclami al", "supermercato"])]
RICHIESTA = [[("Devo rispondere a questo annuncio di", "b")], [("lavoro. Mi scrivi la mail di candidatura?", "b")]]
ANNUNCIO = [[("«Torrefazione Tostavento (Pesaro):", "b")], [("assistenza clienti.", "b")]]
SII = "Sii originale."
RIGA_DARIO = [[("Da tre anni lavoro al banco di", "t")],
              [("una ", "t"), ("ferramenta", "t"), (": al telefono rispondo io,", "b")],
              [("una trentina di chiamate al giorno, e i", "b")], [("clienti arrabbiati li passano a me.", "b")]]
A10 = {0: [("Gentile Torrefazione Tostavento,", "b")],
       1: [("vi scrivo per candidarmi alla posizione di", "b")], 2: [("assistenza clienti che avete pubblicato.", "b")],
       4: [("Ho ", "t"), ("[numero]", "c"), (" anni", "t"), (" di esperienza", "b")],
       5: [("di lavoro a contatto con il", "b")],
       6: [("pubblico, maturata ", "b"), ("come ", "t"), ("[ruolo]", "c")],
       7: [("presso ", "t"), ("[azienda/luogo]", "c"), (".", "t"), (" […]", "p")]}
B9 = {0: [("Gentile team di Tostavento,", "b")],
      1: [("ho letto il vostro annuncio con il ", "b"), ("caffè", "t")], 2: [("accanto, che mi sembrava il minimo.", "b")],
      3: [("[…]", "p")],
      4: [("Ho ", "t"), ("[X anni]", "c"), (" di esperienza a", "b")],
      5: [("contatto con il pubblico ", "b"), ("come", "t")],
      6: [("[ruolo]", "c"), (" presso ", "t"), ("[azienda/luogo]", "c"), (".", "t"), (" […]", "p")]}
C10 = {0: [("Gentile Torrefazione Tostavento,", "b")], 1: [("[…]", "p")],
       2: [("Da tre anni lavoro al banco di", "t")],
       3: [("una ferramenta", "t"), (", a contatto diretto con", "b"), (" […]", "p")]}
RAMI = [("(vi) scrivo…", "6", 18), ("mi chiamo…", "3", 10), ("ho letto il vostro annuncio…", "1", 4)]
SALUTO_A10 = ["Gentile", "Torrefazione", "Tostavento,"]
DIDA_INVENTATI = "annuncio, azienda e persone inventati"
DIDA_DARIO = "candidato e dettaglio inventati"
DIDA_RILEGGI = "poi rileggi: ogni fatto dev'essere tuo"
DIDA_BIVIO = "dopo il saluto · 10 prove, 2 modelli"

# --- impaginazione, in px della tela (origine in alto a sinistra) ---------------------------------------------------------

FX0, FX1, TX = 70, 950, 94                  # foglio e margine del testo
SCH_Y0, SCH_Y1 = 224, 418                   # le schede
SCH_X = [(60, 348), (366, 654), (672, 960)]
ALTO_2, ALTO, ALTO_6 = 478, 570, 510        # cima del foglio: scena 2 all'inizio · dopo · scena 6
CONF, CONF_6 = 720, 790                     # riga di confine
BASSO, BASSO_4, BASSO_6 = 1094, 1136, 988
PASSO = 44
DIDA_Y = 1152


def X(v: float) -> float:
    return (v - 540) / 120


def Y(v: float) -> float:
    return (960 - v) / 120


def P(x: float, y: float) -> np.ndarray:
    return np.array([X(x), Y(y), 0.0])


def posa(blocco, x: float, y: float, passo: float = PASSO, da: str = "sx"):
    """La riga k ha la cima del puntello «Hg» a y + k·passo e parte da x (da="dx": finisce a x; "c": centrata)."""
    for k, r in enumerate(blocco.righe):
        p = r.puntello if r.allineata else r
        rif = {"sx": r.glifi.get_left()[0], "dx": r.glifi.get_right()[0], "c": r.glifi.get_center()[0]}[da]
        r.shift([X(x) - rif, Y(y + k * passo) - p.get_top()[1], 0])
    return blocco


def scatola(x0, y0, x1, y1, colore, raggio: float = 20, spessore: float = 3, pieno=None) -> RoundedRectangle:
    r = RoundedRectangle(corner_radius=px(raggio), width=px(x1 - x0), height=px(y1 - y0), stroke_color=colore,
                         stroke_width=tratto(spessore), fill_color=pieno or colore, fill_opacity=1 if pieno else 0)
    return r.move_to(P((x0 + x1) / 2, (y0 + y1) / 2))


def barretta(x0, x1, yc, colore, h: float = 12) -> RoundedRectangle:
    r = RoundedRectangle(corner_radius=px(min(h, max(2.0, x1 - x0)) / 2.01), width=px(max(4.0, x1 - x0)), height=px(h),
                         stroke_width=0, fill_color=colore, fill_opacity=0.38)
    return r.move_to(P((x0 + x1) / 2, yc))


def in_px(p) -> tuple[float, float]:
    return p[0] * 120 + 540, 960 - p[1] * 120


# --- opacità e tinte che non toccano i puntelli delle righe ----------------------------------------------------------------

def foglie(m: Mobject) -> list:
    return m.family_members_with_points()


def segna(m: Mobject) -> Mobject:
    for f in foglie(m):
        if not hasattr(f, "_pieno"):
            f._pieno = (float(f.get_fill_opacity()), float(f.get_stroke_opacity()) if f.get_stroke_width() > 0 else 0.0)
    return m


def op(g: Mobject, k: float) -> None:
    for f in foglie(g):
        fo, so = f._pieno
        f.set_fill(opacity=fo * k, family=False)
        f.set_stroke(opacity=so * k, family=False)


def tinta(g: Mobject, colore, k: float = 1.0) -> None:
    for f in foglie(g):
        fo, so = f._pieno
        if fo > 0:
            f.set_fill(colore, opacity=fo * k, family=False)
        if so > 0:
            f.set_stroke(colore, opacity=so * k, family=False)


# --- il passaggio a tappe -------------------------------------------------------------------------------------------------

@dataclass
class Tappa:
    pezzo: Mobject
    fn: Callable
    a: float = 0.0
    b: float = 1.0
    rate: Callable = smooth
    traccia: bool = False


class Tappe(Animation):
    """Più modifiche sulla stessa radice già in scena, ognuna nella sua finestra (a, b) del passaggio."""

    def __init__(self, radice: Mobject, tappe: list[Tappa], **kw):
        self.tappe = [t for t in tappe if t is not None]
        super().__init__(radice, rate_func=linear, **kw)

    def create_starting_mobject(self) -> Mobject:
        return Mobject()

    def begin(self) -> None:
        self._fam = self.mobject.get_family()
        indice = {id(m): k for k, m in enumerate(self._fam)}
        stato = self.mobject.copy().get_family()
        self._piani = []
        for t in self.tappe:
            idx = [indice[id(m)] for m in foglie(t.pezzo)]
            prima = [stato[i].copy() for i in idx]
            t.fn(VGroup(*[stato[i] for i in idx]))
            dopo = [stato[i].copy() for i in idx]
            passi = [(i, p, d, _punti_diversi(p, d), _colori_diversi(p, d)) for i, p, d in zip(idx, prima, dopo)]
            self._piani.append(([x for x in passi if x[3] or x[4] or t.traccia], t))
        super().begin()

    def interpolate_mobject(self, alpha: float) -> None:
        for passi, t in self._piani:
            if alpha < t.a and t.a > 0:
                continue
            s = 1.0 if t.b <= t.a else min(1.0, max(0.0, (alpha - t.a) / (t.b - t.a)))
            s = float(t.rate(s))
            sc = min(1.0, max(0.0, s))
            for i, p, d, muove, colora in passi:
                m = self._fam[i]
                if t.traccia:
                    if sc < 1e-3:
                        continue
                    m.pointwise_become_partial(d, 0, sc)
                    m.interpolate_color(d, d, 1)
                    continue
                if muove:
                    m.points = (1 - s) * p.points + s * d.points
                if colora:
                    m.interpolate_color(p, d, sc)


def _punti_diversi(p, d) -> bool:
    return p.points.shape != d.points.shape or not np.allclose(p.points, d.points, atol=1e-9)


def _colori_diversi(p, d) -> bool:
    for a, b in ((p.get_fill_rgbas(), d.get_fill_rgbas()), (p.get_stroke_rgbas(), d.get_stroke_rgbas())):
        if a.shape != b.shape or not np.allclose(a, b, atol=1e-9):
            return True
    return abs(p.get_stroke_width() - d.get_stroke_width()) > 1e-9


def t_op(pezzo, k, a=0.0, b=1.0, rate=smooth) -> Tappa:
    return Tappa(pezzo, lambda g: op(g, k), a, b, rate)


def t_tinta(pezzo, colore, k=1.0, a=0.0, b=1.0, rate=smooth) -> Tappa:
    return Tappa(pezzo, lambda g: tinta(g, colore, k), a, b, rate)


def t_sposta(pezzo, v, a=0.0, b=1.0, rate=smooth) -> Tappa:
    return Tappa(pezzo, lambda g: g.shift(v), a, b, rate)


def t_entra(pezzo, a=0.0, b=1.0, sposta=None, scala: float = 1.0, rate=smooth, k: float = 1.0, colore=None) -> Tappa:
    """Il pezzo (nascosto) parte spostato di -sposta e scalato, e arriva al suo posto acceso."""
    v = np.array(ORIGIN if sposta is None else sposta, dtype=float)
    g0 = VGroup(*foglie(pezzo))
    g0.scale(scala).shift(-v)

    def fn(g):
        g.shift(v).scale(1 / scala)
        if colore is None:
            op(g, k)
        else:
            tinta(g, colore, k)
    return Tappa(pezzo, fn, a, b, rate)


def t_esce(pezzo, a=0.0, b=1.0, sposta=None, rate=smooth) -> Tappa:
    v = np.array(ORIGIN if sposta is None else sposta, dtype=float)

    def fn(g):
        g.shift(v)
        op(g, 0)
    return Tappa(pezzo, fn, a, b, rate)


def t_punti(pezzo, copia, a=0.0, b=1.0, rate=smooth) -> Tappa:
    """Il pezzo prende i punti di una copia fatta prima (riquadri che cambiano misura, ritorni a casa)."""
    sorg = foglie(copia)

    def fn(g):
        for m, s in zip(g.submobjects, sorg):
            m.points = s.points.copy()
    return Tappa(pezzo, fn, a, b, rate)


def t_traccia(pezzo, a=0.0, b=1.0, rate=smooth) -> Tappa:
    return Tappa(pezzo, lambda g: op(g, 1), a, b, rate, traccia=True)


def t_fn(pezzo, fn, a=0.0, b=1.0, rate=smooth) -> Tappa:
    return Tappa(pezzo, fn, a, b, rate)


def t_sale(tratteggio, a=0.0, b=1.0, colore=None, k=1.0) -> list[Tappa]:
    """Una linea tratteggiata che sale: i trattini si accendono uno dopo l'altro, dal foglio verso la scheda."""
    dd = list(tratteggio.submobjects)
    n = max(1, len(dd))
    passo = (b - a) / n
    if colore is None:
        return [t_op(d, k, a + j * passo, a + (j + 1.6) * passo) for j, d in enumerate(dd)]
    return [t_tinta(d, colore, k, a + j * passo, a + (j + 1.6) * passo) for j, d in enumerate(dd)]


def applica(*tappe) -> None:
    for t in piatte(tappe):
        t.fn(VGroup(*foglie(t.pezzo)))


def piatte(tappe) -> list[Tappa]:
    out = []
    for x in tappe:
        if x is None:
            continue
        out += piatte(x) if isinstance(x, (list, tuple)) else [x]
    return out


# --- la riga a fuoco --------------------------------------------------------------------------------------------------------

class Fuoco(VGroup):
    """Una riga di testo a segmenti. Stati: vuoto · testo (tutto leggibile) · ridotto (restano i segmenti "t", le caselle
    "c" in accento e «[…]»; il resto è barretta) · sagoma (solo barrette e «[…]»)."""

    def __init__(self, segmenti, x: float, y: float, c_testo: str, c_barra: str, c_accento: str, ruolo: str = "piede", **kw):
        super().__init__(**kw)
        self.c_testo, self.c_accento = c_testo, c_accento
        self.blocco = posa(testo("".join(s for s, _ in segmenti), ruolo), x, y)
        riga = self.blocco.righe[0]
        yc = in_px(riga.puntello.get_center())[1] + 1
        self.seg, k = [], 0
        self.barre, self.caselle = VGroup(), VGroup()
        for s, tipo in segmenti:
            n = len(re.sub(r"\s", "", s))
            g = VGroup(*riga.glifi.submobjects[k:k + n])
            k += n
            x0, x1 = in_px(g.get_left())[0], in_px(g.get_right())[0]
            barra = cas = None
            if tipo != "p":
                barra = barretta(x0, x1, yc, c_barra)
                self.barre.add(barra)
            if tipo == "c":
                cas = DashedVMobject(scatola(x0 - 5, yc - 22, x1 + 4, yc + 22, c_accento, raggio=9, spessore=3), num_dashes=22)
                self.caselle.add(cas)
            self.seg.append((tipo, g, barra, cas))
        self.add(self.blocco, self.barre, self.caselle)
        self.ora: dict[int, tuple[float, str]] = {}

    def glifi(self, tipo: str | None = None) -> VGroup:
        return VGroup(*[g for t, g, _, _ in self.seg if tipo is None or t == tipo])

    def _mira_seg(self, stato: str, tipo, g, barra, cas):
        testo_on = {"vuoto": False, "testo": True, "ridotto": tipo in "tcp", "sagoma": tipo == "p"}[stato]
        colore = self.c_accento if (tipo == "c" and stato == "ridotto") else self.c_testo
        out = [(g, 1.0 if testo_on else 0.0, colore)]
        if barra is not None:
            out.append((barra, 0.0 if (testo_on or stato == "vuoto") else 1.0, None))
        if cas is not None:
            out.append((cas, 1.0 if stato == "ridotto" else 0.0, None))
        return out

    def _mira(self, stato: str):
        """(pezzo, opacità, colore) di ogni pezzo nello stato."""
        return [x for tipo, g, barra, cas in self.seg for x in self._mira_seg(stato, tipo, g, barra, cas)]

    def metti(self, stato: str) -> "Fuoco":
        for pezzo, k, colore in self._mira(stato):
            tinta(pezzo, colore, k) if colore else op(pezzo, k)
            self.ora[id(pezzo)] = (k, colore)
        return self

    def verso(self, stato: str, a=0.0, b=1.0, finestre=None) -> list[Tappa]:
        """Prima (a → 45 %) si spegne quello che esce, poi (55 % → b) si accende quello che entra: mai insieme.
        `finestre`: iteratore di (a, b), una per segnaposto, per accenderli uno dopo l'altro (con la loro casella)."""
        m, n = a + (b - a) * 0.45, a + (b - a) * 0.55
        out = []
        for tipo, g, barra, cas in self.seg:
            fin = next(finestre, None) if (finestre is not None and tipo == "c" and stato == "ridotto") else None
            for pezzo, k, colore in self._mira_seg(stato, tipo, g, barra, cas):
                k0, c0 = self.ora.get(id(pezzo), (0.0, None))
                self.ora[id(pezzo)] = (k, colore)
                if k < k0:
                    out.append(t_op(pezzo, 0, a, m))
                elif k > k0 or (k > 0 and colore != c0):
                    fa, fb = fin if (fin and pezzo is not barra) else (n, b)
                    out.append(t_tinta(pezzo, colore, k, fa, fb) if colore else t_op(pezzo, k, fa, fb))
        return out


def righe_fuoco(spec, x, y0, col, passo=PASSO) -> dict[int, Fuoco]:
    voci = spec.items() if isinstance(spec, dict) else enumerate(spec)
    return {k: Fuoco(seg, x, y0 + k * passo, str(col.testo), str(col.attenuato), str(col.accento)) for k, seg in voci}


def verso(righe, stato, a=0.0, b=1.0, solo=None, finestre=None) -> list[Tappa]:
    fin = iter(finestre) if finestre else None
    out = []
    for k, r in righe.items():
        if solo is None or k in solo:
            out += r.verso(stato, a, b, finestre=fin)
    return out


# --- gli oggetti del filo visivo ----------------------------------------------------------------------------------------------

class Scheda(VGroup):
    """Una persona: icona, nome ed età, il mestiere su due o tre righe (testo o barrette)."""

    def __init__(self, k: int, col, **kw):
        super().__init__(**kw)
        nome, righe = SCHEDE[k]
        x0, x1 = SCH_X[k]
        self.xc = (x0 + x1) / 2
        self.box = scatola(x0, SCH_Y0, x1, SCH_Y1, str(col.attenuato), raggio=18)
        self.icona = Icona("user", altezza_px=40, colore=str(col.testo)).move_to(P(x0 + 36, SCH_Y0 + 36))
        self.nome = posa(testo(nome, "piede", peso=BOLD), x0 + 66, SCH_Y0 + 18)
        self.mestiere = righe_fuoco([[(r, "b")] for r in righe], x0 + 18, SCH_Y0 + 68, col, passo=42)
        self.add(self.box, self.icona, self.nome, *self.mestiere.values())


class Linee:
    """Le tre linee nel varco fra le schede e il foglio: tratteggiate (la domanda), piene (la risposta), monche (scena 4)."""

    def __init__(self, col, y_foglio: float):
        self.tratt, self.piene, self.monche = [], [], []
        for k in range(3):
            x = sum(SCH_X[k]) / 2
            giu, su = P(x, y_foglio - 6), P(x, SCH_Y1 + 8)
            self.tratt.append(DashedLine(giu, su, dash_length=px(13), stroke_color=str(col.testo), stroke_width=tratto(4)))
            self.piene.append(Line(giu, su, stroke_color=str(col.testo), stroke_width=tratto(5)))
            self.monche.append(DashedLine(su, P(x, SCH_Y1 + 8 + 0.4 * (y_foglio - SCH_Y1)), dash_length=px(13),
                                          stroke_color=str(col.attenuato), stroke_width=tratto(4)))
        self.tutte = VGroup(*self.tratt, *self.piene, *self.monche)


def fogli_pila(conf: float, basso: float, col) -> VGroup:
    """Quattro fogli senza testo dietro la mail, ruotati e sfalsati: bordi che spuntano, mai due, senza numeri."""
    out = VGroup()
    for ang, dx, dy in ((-2.3, 3, 14), (1.7, -4, 11), (-1.0, 5, 8), (2.6, -2, 5)):
        f = scatola(FX0, conf + 10, FX1, basso, str(col.attenuato), pieno=str(col.sfondo))
        f.set_stroke(opacity=0.75)
        out.add(f.rotate(ang * np.pi / 180).shift([px(dx), -px(dy), 0]))
    return out


class Banco:
    """Tutto quello che le scene 2, 3, 4 e 6 hanno in comune, costruito acceso al suo posto."""

    def __init__(self, scena: ScenaReel, alto: float = ALTO, conf: float = CONF, basso: float = BASSO, dida: str = DIDA_INVENTATI):
        col = self.col = scena.cfg.palette
        self.alto, self.conf, self.basso = alto, conf, basso
        self.schede = [Scheda(k, col) for k in range(3)]
        self.linee = Linee(col, alto)
        self.pila = fogli_pila(conf, basso, col)
        self.carta = scatola(FX0, alto, FX1, basso, str(col.attenuato), pieno=str(col.sfondo))
        self.confine = Line(P(FX0 + 16, conf), P(FX1 - 16, conf), stroke_color=str(col.secondario), stroke_width=tratto(4))
        # la metà alta: cinque barrette sottili (richiesta e annuncio a sagoma) e una riga libera per l'aggiunta
        self.sottili = VGroup(*[barretta(x0, x1, alto + 24 + 14 * j, str(col.attenuato), h=8)
                                for j, (x0, x1) in enumerate(((TX, 806), (TX, 835), (TX + 22, 752), (TX + 22, 830), (TX + 22, 640)))])
        self.sii = posa(testo(SII, "etichetta", colore=str(col.accento), peso=BOLD), TX, alto + 92)
        self.dida = posa(testo(dida, "piede", colore=str(col.attenuato)), FX0, DIDA_Y)
        self.domanda = testo("?", "punto", colore=str(col.accento), peso=BOLD)
        self.mondo = VGroup(*self.schede, self.linee.tutte, self.pila, self.carta, self.confine, self.sottili, self.sii,
                            self.dida, self.domanda)
        segna(self.mondo)

    def aggiungi(self, *mobs) -> None:
        for m in mobs:
            self.mondo.add(segna(m))

    def mail(self, spec) -> dict[int, Fuoco]:
        righe = righe_fuoco(spec, TX, self.conf + 16, self.col)
        self.aggiungi(*righe.values())
        for r in righe.values():
            r.metti("vuoto")
        return righe

    def mestieri(self, stato: str) -> None:
        for s in self.schede:
            for r in s.mestiere.values():
                r.metti(stato)

    def t_mestieri(self, stato: str, a=0.0, b=1.0, solo=None) -> list[Tappa]:
        return [t for k, s in enumerate(self.schede) if solo is None or k in solo for t in verso(s.mestiere, stato, a, b)]

    def stato_linee(self, quale: str, colore=None, k: float = 1.0) -> None:
        """quale = niente | tratteggiate | piene: lo stato fermo delle tre linee."""
        op(self.linee.tutte, 0)
        for g in {"niente": [], "tratteggiate": self.linee.tratt, "piene": self.linee.piene}[quale]:
            tinta(g, colore or str(self.col.testo), k)


class ScenaFoglio(ScenaReel):
    """Aiuti comuni: il passaggio a tappe sul mondo, gli istanti delle parole, il punch che tiene la didascalia."""

    def fai(self, durata_s: float, *tappe, altre=()) -> None:
        self.play(Tappe(self.banco.mondo, piatte(tappe)), *altre, run_time=self.arrotonda(durata_s))

    def alle(self, s: float) -> None:
        self.attendi_fino(s)

    def istante(self, i: int, parola: str) -> float:
        """Quando la voce arriva a `parola` nella frase i, in proporzione ai caratteri (voce di prova: 0,3 s di pausa
        fra le frasi, 0,5 s di coda). È una stima: gli agganci fini si riguardano con le clip vere."""
        frase = piano(self.scena["voce"][i]).lower()
        k = max(0, frase.find(parola.lower()))
        ini = self.inizi_frasi[i]
        fine = self.inizi_frasi[i + 1] - 0.3 if i + 1 < len(self.inizi_frasi) else self.durata_s - 0.5
        return ini + (fine - ini) * k / max(1, len(frase))

    def fine_beat(self, i: int) -> float:
        return (self.inizi_frasi[i + 1] if i + 1 < len(self.inizi_frasi) else self.durata_s) - self.ANTICIPO_S

    def punch_con_didascalia(self, s: str, dida: Mobject, tenuta_s: float = 1.0) -> None:
        """Come ScenaReel.punch (taglio, battuta a tutto schermo, taglio indietro), ma la didascalia degli inventati
        resta al suo posto anche durante la battuta: il revisore la vuole leggibile per tutta la scena."""
        sotto = list(self.mobjects)
        self.remove(*sotto)
        p = Punch(s, self.area.contenuto)
        resta = dida.copy()
        self.add(resta)
        entrata = self.arrotonda(0.15)
        soglia = self.t + self._fotogramma + 1e-6
        prossimi = [x - self.ANTICIPO_S for x in self.inizi_frasi if x - self.ANTICIPO_S > soglia]
        if prossimi:
            tenuta_s = max(0.3, min(tenuta_s, prossimi[0] - self.t - entrata))
        self.play(p.entra(), run_time=entrata)
        self.verifica(f"punch «{s}»")
        self.wait(tenuta_s)
        self.remove(p, resta)
        self.add(*sotto)


RIMBALZO = rate_functions.ease_out_back
PROVE_SU_10 = "10 prove su 10"


def etichetta_caffe(s: str, caffe, colore: str):
    """«4 su 10» agganciato alla sola parola «caffè» con un trattino corto che attraversa il confine."""
    et = testo(s, "etichetta", colore=colore, peso=BOLD)
    et.move_to([caffe.get_right()[0] - et.width / 2, Y(CONF - 34), 0])
    x = caffe.get_center()[0]
    trattino = Line([x, et.get_bottom()[1] - px(8), 0], [x, caffe.get_top()[1] + px(8), 0], stroke_color=colore,
                    stroke_width=tratto(5))
    return et, trattino


def graffa_prove(s: str, colore: str):
    """La graffa piccola sulle righe delle tre caselle (non sulla mail intera) con «10 prove su 10» su due righe."""
    fant = Rectangle(width=px(10), height=px(4 * PASSO - 8)).move_to(P(704, CONF + 16 + 4 * PASSO + (4 * PASSO - 8) / 2))
    graffa = Brace(fant, direction=RIGHT, buff=0, color=colore)
    etich = testo(s.replace(" su ", "\nsu "), "etichetta", colore=colore, peso=BOLD)
    etich.next_to(graffa, RIGHT, buff=px(14))
    return graffa, etich


# --- le scene -------------------------------------------------------------------------------------------------------------------

class Scena02(ScenaFoglio):
    """Tre schede, la stessa richiesta che si fonde in una, una delle mail che tornano; «Di chi è?» con le linee
    tratteggiate e il vuoto; GRANDE (punch) «TUTTI E TRE»; poi le tre caselle vuote con «10 prove su 10»."""

    def costruisci(self):
        b = self.banco = Banco(self, alto=ALTO)
        col = b.col
        c_testo, c_acc, c_att = str(col.testo), str(col.accento), str(col.attenuato)
        # la metà alta all'inizio: la cima del foglio è più su, richiesta e annuncio a righe intere
        carta_dopo = b.carta.copy()
        b.carta.become(scatola(FX0, ALTO_2, FX1, BASSO, c_att, pieno=str(col.sfondo)))
        segna(b.carta)
        rich = righe_fuoco(RICHIESTA, TX, ALTO_2 + 16, col)
        ann = righe_fuoco(ANNUNCIO, TX + 22, ALTO_2 + 16 + 2 * PASSO, col)
        y3, y4 = ALTO_2 + 16 + 3 * PASSO + 19, ALTO_2 + 16 + 4 * PASSO + 19
        coda = VGroup(barretta(TX + 22 + 336 + 16, 830, y3, c_att), barretta(TX + 22, 640, y4, c_att))
        filo = Line(P(TX + 4, ALTO_2 + 16 + 2 * PASSO), P(TX + 4, ALTO_2 + 16 + 5 * PASSO - 8), stroke_color=c_att,
                    stroke_width=tratto(4))
        a10 = b.mail(A10)
        gettoni = VGroup()
        for s in b.schede:
            g = VGroup(scatola(s.xc - 80, SCH_Y1 + 14, s.xc + 80, SCH_Y1 + 70, c_testo, raggio=12, pieno=str(col.sfondo)),
                       barretta(s.xc - 60, s.xc + 60, SCH_Y1 + 33, c_testo, h=8), barretta(s.xc - 60, s.xc + 20, SCH_Y1 + 51, c_testo, h=8))
            gettoni.add(g)
        graffa, etich = graffa_prove(self.scena["testo"][0], c_acc)
        b.aggiungi(*rich.values(), *ann.values(), coda, filo, gettoni, graffa, etich)
        # stato d'inizio: schede e didascalia; il resto spento
        b.mestieri("testo")
        for r in (*rich.values(), *ann.values()):
            r.metti("vuoto")
        b.stato_linee("niente")
        op(VGroup(b.pila, b.carta, b.confine, b.sottili, b.sii, b.domanda, coda, filo, gettoni, graffa, etich), 0)
        b.domanda.move_to(P(842, 990))
        self.add(b.mondo)                                     # fotogramma 0 pieno: si arriva dallo stacco sul filmato

        # beat 0 «Guarda, tre persone rispondono allo stesso annuncio e all'IA chiedono la stessa cosa.»
        d0 = self.durata_beat(0)
        foglio = VGroup(b.carta, b.confine)
        self.fai(0.9, [t_fn(s, lambda g: g.scale(1.07), 0.08 + 0.2 * k, 0.5 + 0.2 * k, there_and_back) for k, s in enumerate(b.schede)],
                 t_entra(foglio, 0.25, 1.0, sposta=UP * px(160), rate=RIMBALZO))
        self.alle(self.istante(0, "allo stesso annuncio") - 0.25)
        # l'annuncio: per un istante la prima riga si legge, poi è sagoma
        self.fai(0.5, verso(ann, "testo", 0, 0.8), t_entra(VGroup(coda, filo), 0.3, 1, sposta=UP * px(12)))
        self.alle(self.istante(0, "all'IA") - 0.2)
        arrivo = P(TX + 370, ALTO_2 + 16 + PASSO - 4)

        def converge(g, arrivo=arrivo):
            g.move_to(arrivo)
        self.fai(1.15, verso(ann, "sagoma", 0, 0.3),
                 [t_entra(g, 0.05 + 0.06 * k, 0.3 + 0.06 * k, sposta=DOWN * px(26), rate=rush_from) for k, g in enumerate(gettoni)],
                 [t_fn(g, converge, 0.36, 0.72, rate_functions.ease_in_out_cubic) for g in gettoni],
                 t_op(gettoni, 0, 0.72, 0.82), verso(rich, "testo", 0.72, 1.0))

        # beat 1 «Questa è una delle mail che tornano. Di chi è?»
        self.beat(1)
        d1 = self.durata_beat(1)
        bersagli = [(rich[0].barre[0], b.sottili[0]), (rich[1].barre[0], b.sottili[1]), (ann[0].barre[0], b.sottili[2]),
                    (ann[1].barre[0], b.sottili[3]), (coda[0], b.sottili[3]), (coda[1], b.sottili[4])]
        self.fai(1.5, verso(rich, "sagoma", 0, 0.3), t_op(filo, 0, 0, 0.14),
                 # la richiesta si stringe in cinque barrette sottili e la cima del foglio scende: il varco si apre
                 [t_punti(v, n.copy(), 0.3, 0.55, rate_functions.ease_in_out_cubic) for v, n in bersagli],
                 t_punti(b.carta, carta_dopo, 0.3, 0.55, rate_functions.ease_in_out_cubic),
                 # la mail si scrive dal confine in giù: saluto e attacco a testo, la frase dei segnaposto a sagoma
                 [verso({k: a10[k]}, "testo", 0.18 + 0.12 * k, 0.5 + 0.12 * k) for k in (0, 1, 2)],
                 [verso({k: a10[k]}, "sagoma", 0.5 + 0.05 * j, 0.72 + 0.05 * j) for j, k in enumerate((4, 5, 6, 7))],
                 [t_entra(f, 0.74 + 0.05 * j, 0.9 + 0.05 * j, sposta=UP * px(14)) for j, f in enumerate(b.pila)])
        op(VGroup(*[v for v, _ in bersagli]), 0)              # da qui valgono le barrette sottili del banco
        op(b.sottili, 1)
        self.alle(self.istante(1, "Di chi") - 0.3)
        # «Di chi è?»: le tre linee salgono tratteggiate, il punto di domanda arriva sulla mail e pulsa: nessuna si decide
        self.fai(0.75, [t_sale(l, 0.0, 0.7) for l in b.linee.tratt], t_entra(b.domanda, 0.45, 1.0, scala=0.4, rate=RIMBALZO))

        # beat 2 «Non lo puoi dire, va bene per tutti e tre,»: il vuoto, poi GRANDE (punch)
        self.beat(2)
        t_punch = self.istante(2, "tutti e tre") - 0.15
        while t_punch - self.t > 0.72:
            self.fai(0.66, t_fn(b.domanda, lambda g: g.scale(1.22), rate=there_and_back),
                     [t_fn(l, lambda g: op(g, 0.35), rate=there_and_back) for l in b.linee.tratt])
        self.alle(t_punch)
        b.stato_linee("piene", c_acc)                         # compare al ritorno, col taglio: tre linee piene, niente «?»
        op(b.domanda, 0)
        self.punch_con_didascalia("TUTTI\nE TRE", b.dida, tenuta_s=1.05)

        # beat 3 «perché al posto della persona ci sono dei buchi.»
        self.beat(3)
        t0 = self.t
        t_buchi = self.istante(3, "ci sono") - 0.1
        self.fai(0.55, verso(a10, "sagoma", 0, 1, solo=(0, 1, 2)), [t_tinta(l, c_testo, 0.55, 0, 0.5) for l in b.linee.piene])
        self.alle(t0 + 0.65)
        self.fai(1.2, verso(a10, "ridotto", 0, 0.3, solo=(4, 5, 6, 7), finestre=[(0.3, 0.5), (0.52, 0.72), (0.74, 0.94)]))
        self.alle(max(self.t, t_buchi + 0.55))
        self.fai(0.5, t_entra(graffa, 0, 0.6, scala=0.4, rate=RIMBALZO), t_entra(etich, 0.35, 1, sposta=RIGHT * px(18)))


class Scena03(ScenaFoglio):
    """«Sii originale.» entra nella richiesta, A10 esce del tutto e solo a foglio vuoto entra B9; GRANDE (contrasto di
    scala): zoom sull'attacco e poi sulla sola parola «caffè» con «4 su 10»; tornano le linee, le caselle vuote, il «?»."""

    def costruisci(self):
        b = self.banco = Banco(self)
        col = b.col
        c_testo, c_acc, c_att = str(col.testo), str(col.accento), str(col.attenuato)
        a10, b9 = b.mail(A10), b.mail(B9)
        graffa, etich = graffa_prove(PROVE_SU_10, c_acc)
        caffe = b9[1].glifi("t")
        pill, trattino = etichetta_caffe(self.scena["testo"][0], caffe, c_acc)
        disco = Dot(radius=px(54), color=str(col.sfondo)).move_to(P(893, CONF))
        b.mondo.remove(b.domanda)
        b.aggiungi(graffa, etich, trattino, pill, disco, b.domanda)
        # stato d'inizio = fine della scena 2
        b.mestieri("testo")
        for k, r in a10.items():
            r.metti("sagoma" if k < 3 else "ridotto")
        b.stato_linee("piene", c_testo, 0.55)
        b.domanda.move_to(P(893, CONF))
        op(VGroup(b.sii, b.domanda, disco, pill, trattino), 0)
        self.add(b.mondo)

        # beat 0 «Allora aggiungi «sii originale», e qualcosa cambia,»
        self.fai(0.6, t_op(VGroup(graffa, etich), 0, 0, 0.4), verso(a10, "vuoto", 0, 0.9), b.t_mestieri("sagoma", 0.1, 1),
                 [t_tinta(l, c_att, 0.6) for l in b.linee.piene])
        self.alle(self.istante(0, "sii originale") - 0.35)
        lettere = list(b.sii.righe[0].glifi.submobjects)
        op(b.sii, 0)
        self.fai(0.8, [t_entra(VGroup(g), 0.06 * j, 0.06 * j + 0.2, sposta=UP * px(10), rate=rush_from) for j, g in enumerate(lettere)])
        self.alle(self.istante(0, "qualcosa cambia") - 0.25)
        # solo a foglio vuoto entra B9: saluto a sagoma, attacco a testo, «[…]», la frase dei segnaposto a sagoma
        ordine = [(0, "sagoma"), (1, "testo"), (2, "testo"), (3, "testo"), (4, "sagoma"), (5, "sagoma"), (6, "sagoma")]
        self.fai(min(1.0, self.fine_beat(0) - self.t - 0.1),
                 [verso({k: b9[k]}, st, 0.1 * j, 0.4 + 0.1 * j) for j, (k, st) in enumerate(ordine)])

        # beat 1 «su dieci prove, quattro adesso cominciano dal caffè.»: GRANDE (contrasto di scala)
        self.beat(1)
        attacco = VGroup(b9[1].glifi(), b9[2].glifi())
        fuori_campo = VGroup(*[VGroup(s.icona, s.nome) for s in b.schede], b.sii, b.dida, b9[3].glifi(), b9[6].glifi("p"))
        self.fai(0.7, t_op(fuori_campo, 0, 0, 0.4), altre=[self.zoom_su(attacco, 1.2)])
        self.alle(self.istante(1, "quattro") - 0.1)
        self.fai(0.7, verso(b9, "ridotto", 0, 0.7, solo=(1, 2)), t_tinta(caffe, c_acc, 1, 0.5, 1),
                 altre=[self.zoom_su(caffe, 2.4)])
        self.fai(0.4, t_entra(pill, 0, 0.8, scala=0.5, rate=RIMBALZO), t_traccia(trattino, 0.6, 1))
        self.alle(self.fine_beat(1) - 0.55)
        self.fai(0.5, altre=[self.torna()])

        # beat 2 «Ma di chi è? I buchi sono ancora lì.»
        self.beat(2)
        self.fai(0.45, t_op(fuori_campo, 1, 0, 0.8), [t_op(l, 0, 0, 0.3) for l in b.linee.piene])
        self.fai(0.7, [t_sale(l, 0.0, 0.6) for l in b.linee.tratt], [t_op(l, 0, 0.62, 0.7) for l in b.linee.tratt],
                 [t_tinta(l, c_testo, 1, 0.7, 1) for l in b.linee.piene])
        self.alle(max(self.t, self.istante(2, "I buchi") - 0.2))
        self.fai(min(1.0, self.fine_beat(2) - self.t - 0.15),
                 verso(b9, "ridotto", 0, 0.3, solo=(4, 5, 6), finestre=[(0.3, 0.5), (0.5, 0.7), (0.7, 0.9)]))

        # beat 3 «Eppure gliel'hai chiesto, di essere originale. Dov'è il trucco?»
        self.beat(3)
        self.alle(self.istante(3, "originale") - 0.2)
        self.fai(0.6, t_fn(b.sii, lambda g: g.scale(1.14, about_point=g.get_left()), rate=there_and_back))
        self.alle(self.istante(3, "Dov'è") - 0.15)
        self.fai(0.5, t_op(disco, 1, 0, 0.2), t_entra(b.domanda, 0.1, 1, scala=0.3, rate=RIMBALZO))
        self.alle(self.durata_s - 1.3)
        self.fai(0.6, t_fn(b.domanda, lambda g: g.scale(1.15), rate=there_and_back))


class Scena04(ScenaFoglio):
    """«continua»: la mail ricomincia a cartellini oltre il confine; GRANDE (rivelazione a tratto): dal nodo «saluto» si
    disegnano tre strade di spessore diverso (6, 3, 1) e due punti le percorrono; poi «lei parte da qui» e «di loro, niente»."""

    def costruisci(self):
        b = self.banco = Banco(self)
        col = b.col
        c_testo, c_acc, c_att, c_sfondo = str(col.testo), str(col.accento), str(col.attenuato), str(col.sfondo)
        t_continua, t_parte, t_niente = self.scena["testo"]
        b9 = b.mail(B9)
        caffe = b9[1].glifi("t")
        et_caffe, trattino = etichetta_caffe("4 su 10", caffe, c_acc)
        disco = Dot(radius=px(54), color=c_sfondo).move_to(P(893, CONF))
        carta_4 = scatola(FX0, ALTO, FX1, BASSO_4, c_att, pieno=c_sfondo)
        continua = Etichetta(t_continua).move_to(P(806, CONF))
        # i cartellini del saluto di A10 e il nodo «saluto»
        gettoni = VGroup(*[Token(w).scale(0.9) for w in SALUTO_A10]).arrange(RIGHT, buff=px(14))
        gettoni.move_to(P(TX, 828), aligned_edge=LEFT)
        raccolti = gettoni.copy().arrange(RIGHT, buff=px(5)).move_to(P(TX, 828), aligned_edge=LEFT)
        saluto = posa(testo("saluto", "piede", colore=c_att), TX + 4, 744)
        # il bivio: tre strade dal nodo, spessori 16 / 9 / 3 px, conti in punta ed etichette alla lettera
        origine = P(172, 872)
        strade, conti, nomi = VGroup(), VGroup(), VGroup()
        for k, (nome, conto, spessore) in enumerate(RAMI):
            # le etichette finiscono tutte a destra (x = 926): la strada grossa è anche la più lunga
            y = 928 + 60 * k
            et = posa(testo(nome, "piede", colore=c_testo if k < 2 else c_att), 926, y - 18, da="dx")
            x_et = in_px(et.get_left())[0]
            cifra = posa(testo(conto, "etichetta", colore=c_testo, peso=BOLD, mono=True), x_et - 18, y - 20, da="dx")
            x_arrivo = in_px(cifra.get_left())[0] - 16
            arrivo = P(x_arrivo, y)
            strada = CubicBezier(origine, origine + DOWN * px(y - 872), arrivo + LEFT * px(0.55 * (x_arrivo - 172)), arrivo)
            strada.set_stroke(c_testo if k < 2 else c_att, width=tratto(spessore), opacity=(0.95, 0.75, 1.0)[k])
            strade.add(strada)
            conti.add(cifra)
            nomi.add(et)
        dida_bivio = posa(testo(DIDA_BIVIO, "piede", colore=c_att), TX, 1086)
        # «tu parti da te»: persona → foglio bianco; «lei parte da qui»: la graffa sulla sola metà alta
        tu = Icona("user", altezza_px=92, colore=c_testo).move_to(P(150, 1020))
        freccia = Line(P(212, 1020), P(292, 1020), stroke_color=c_testo, stroke_width=tratto(5))
        punta = VGroup(Line(P(292, 1020), P(274, 1006), stroke_color=c_testo, stroke_width=tratto(5)),
                       Line(P(292, 1020), P(274, 1034), stroke_color=c_testo, stroke_width=tratto(5)))
        bianco = scatola(312, 974, 382, 1066, c_testo, raggio=8)
        fant = Rectangle(width=px(10), height=px(CONF - ALTO - 24)).move_to(P(556, (ALTO + CONF) / 2))
        graffa = Brace(fant, direction=RIGHT, buff=0, color=c_testo)
        parte = testo(t_parte, "etichetta", colore=c_testo, peso=BOLD).next_to(graffa, RIGHT, buff=px(14))
        niente = testo(t_niente, "etichetta", colore=c_acc, peso=BOLD).next_to(graffa, RIGHT, buff=px(14))
        banda = barretta(TX - 8, TX + 452, ALTO + 24, c_acc, h=16)
        banda.set_fill(opacity=0.7)
        b.mondo.remove(b.domanda)
        b.aggiungi(et_caffe, trattino, disco, b.domanda, continua, gettoni, saluto, strade, conti, nomi, dida_bivio, tu, freccia,
                   punta, bianco, graffa, parte, niente, banda)
        # stato d'inizio = fine della scena 3
        b.mestieri("sagoma")
        for k, r in b9.items():
            r.metti({0: "sagoma", 3: "testo"}.get(k, "ridotto"))
        tinta(caffe, c_acc)
        b.stato_linee("piene", c_testo)
        b.domanda.move_to(P(893, CONF))
        op(VGroup(continua, gettoni, saluto, strade, conti, nomi, dida_bivio, tu, freccia, punta, bianco, graffa, parte, niente, banda), 0)
        self.add(b.mondo)

        # beat 0 «Beh, generativa vuol dire che continua quello che trova,»
        def parcheggia(g):
            g.scale(0.62).move_to(P(916, (SCH_Y1 + ALTO) / 2))
            tinta(g, c_att, 0.9)
        self.fai(0.8, verso(b9, "vuoto", 0, 0.8), t_op(VGroup(et_caffe, trattino, disco), 0, 0, 0.36),
                 t_esce(b.sii, 0, 0.36, sposta=LEFT * px(22), rate=rush_into), t_op(b.pila, 0, 0, 0.36),
                 [t_tinta(l, c_att, 0.6, 0, 0.5) for l in b.linee.piene], t_fn(b.domanda, parcheggia, 0.3, 0.9),
                 t_punti(b.carta, carta_4, 0.45, 1, rate_functions.ease_in_out_cubic))
        self.alle(self.istante(0, "continua") - 0.2)
        self.fai(0.45, t_entra(continua, scala=0.4, rate=RIMBALZO))
        self.alle(self.istante(0, "quello che trova") - 0.3)
        # il testo attraversa il confine: i cartellini scendono da sopra, un pezzo alla volta
        self.fai(min(1.1, self.fine_beat(0) - self.t - 0.1),
                 [t_entra(g, 0.3 * j, 0.3 * j + 0.38, sposta=DOWN * px(90), rate=RIMBALZO) for j, g in enumerate(gettoni)])

        # beat 1 «un pezzo alla volta, e a ogni bivio prende una delle strade più battute.»: GRANDE (rivelazione a tratto)
        self.beat(1)
        self.fai(0.75, [t_fn(g, lambda m: m.shift(UP * px(12)), 0.25 * j, 0.25 * j + 0.5, there_and_back) for j, g in enumerate(gettoni)])
        self.alle(self.istante(1, "a ogni bivio") - 0.45)
        self.fai(0.45, [t_tinta(g.testo.glifi, c_att, 0.9, 0, 0.5) for g in gettoni],
                 t_punti(gettoni, raccolti, 0.2, 0.8), t_entra(saluto, 0.5, 1, sposta=DOWN * px(10)))
        self.fai(1.0, [t_traccia(st, 0.12 * k, 0.12 * k + 0.5, rate_functions.ease_out_cubic) for k, st in enumerate(strade)],
                 [t_entra(VGroup(conti[k], nomi[k]), 0.45 + 0.13 * k, 0.7 + 0.13 * k, sposta=RIGHT * px(20), rate=rush_from) for k in range(3)],
                 t_op(dida_bivio, 1, 0.8, 1))
        # un punto accento corre sulla strada grossa; poi un secondo prende la media (non sempre la stessa)
        for k in (0, 1):
            punto = Dot(radius=px(13), color=c_acc).move_to(origine)
            resto = self.fine_beat(1) - self.t
            durata = self.arrotonda(min(0.62, max(0.3, resto / (2 - k) - 0.2)))
            self.add(punto)
            self.play(MoveAlongPath(punto, strade[k].copy()), run_time=durata, rate_func=rate_functions.ease_in_out_sine)
            self.fai(0.2, t_fn(conti[k], lambda g: tinta(g, c_acc), rate=there_and_back),
                     altre=[punto.animate.set_opacity(0)])
            self.remove(punto)

        # beat 2 «Tu parti da te, lei solo da quello che c'è scritto sopra,»
        self.beat(2)

        def rimpicciolisce(g):
            g.scale(0.45, about_point=origine)
            for f in foglie(g):
                f.set_stroke(width=max(tratto(2.5), f.get_stroke_width() * 0.55), family=False)
        self.fai(0.5, t_op(VGroup(conti, nomi, dida_bivio), 0, 0, 0.4), t_op(VGroup(*[g.testo for g in gettoni]), 0, 0, 0.4),
                 t_fn(strade, rimpicciolisce, 0.45, 1))
        self.fai(0.6, t_entra(tu, 0, 0.5, scala=0.5, rate=RIMBALZO), t_traccia(freccia, 0.4, 0.75), t_op(punta, 1, 0.7, 0.85),
                 t_entra(bianco, 0.7, 1, sposta=RIGHT * px(16)))
        self.alle(self.istante(2, "lei solo") - 0.2)

        def stringe(g):
            g.stretch(0.58, 0, about_point=P(TX, ALTO + 24))
        self.fai(0.9, t_fn(b.sottili, stringe, 0, 0.4, rate_functions.ease_in_out_cubic), t_entra(graffa, 0.35, 0.75, scala=0.3, rate=RIMBALZO),
                 t_entra(parte, 0.65, 1, sposta=RIGHT * px(18)))

        # beat 3 «e quello che lì sopra non c'è, non lo sa.»
        self.beat(3)
        self.fai(1.35, t_op(banda, 1, 0, 0.06), t_sposta(banda, DOWN * px(CONF - ALTO - 50), 0.04, 0.5, linear), t_op(banda, 0, 0.5, 0.58),
                 [t_op(l, 0, 0.3, 0.45) for l in b.linee.piene], b.t_mestieri("testo", 0.4, 0.85),
                 [t_sale(l, 0.72, 1.0) for l in b.linee.monche])
        self.fai(0.55, t_esce(parte, 0, 0.4, sposta=RIGHT * px(14)), t_entra(niente, 0.5, 1, sposta=RIGHT * px(18), rate=rush_from))


# --- scene 6 e 7: l'allestimento della 6 serve anche come primo fotogramma della 7 ---------------------------------------------

def parole_di(riga: Fuoco) -> list[VGroup]:
    r = riga.blocco.righe[0]
    out, k = [], 0
    for w in r.piano.split():
        out.append(VGroup(*r.glifi.submobjects[k:k + len(w)]))
        k += len(w)
    return out


class Allestimento6:
    """Gli oggetti della scena 6 nella geometria d'arrivo (cima 510, confine 790, fondo 1030)."""

    def __init__(self, scena: ScenaFoglio):
        b = self.b = scena.banco = Banco(scena, alto=ALTO_6, conf=CONF_6, basso=BASSO_6, dida=DIDA_DARIO)
        col = b.col
        c_testo, c_acc, c_att = str(col.testo), str(col.accento), str(col.attenuato)
        self.c_testo, self.c_acc, self.c_att = c_testo, c_acc, c_att
        self.dario = righe_fuoco(RIGA_DARIO, TX, ALTO_6 + 98, col)
        self.c10 = b.mail(C10)
        self.ferramenta = self.dario[1].seg[1][1]
        self.frase_su = VGroup(self.dario[0].glifi(), self.dario[1].seg[0][1], self.ferramenta)
        self.frase_giu = VGroup(self.c10[2].glifi(), self.c10[3].glifi("t"))
        self.salto = self.dario[0].blocco.get_top()[1] - self.c10[2].blocco.get_top()[1]
        r2, r3 = self.c10[2].blocco.righe[0], self.c10[3].blocco.righe[0]
        y2, y3 = r2.puntello.get_bottom()[1] - px(3), r3.puntello.get_bottom()[1] - px(3)
        g3 = self.c10[3].glifi("t")
        self.sotto = VGroup(Line([r2.glifi.get_left()[0], y2, 0], [r2.glifi.get_right()[0], y2, 0], stroke_color=c_acc, stroke_width=tratto(4)),
                            Line([g3.get_left()[0], y3, 0], [g3.get_right()[0], y3, 0], stroke_color=c_acc, stroke_width=tratto(4)))
        yc = r2.puntello.get_center()[1]
        self.su10 = testo(scena.scena.get("testo", ["10 su 10"])[0] if scena.scena.get("n") == 6 else "10 su 10", "etichetta",
                          colore=c_acc, peso=BOLD)
        self.su10.move_to([X(722) + self.su10.width / 2, yc, 0])
        self.aggancio = Line([r2.glifi.get_right()[0] + px(12), yc, 0], [X(710), yc, 0], stroke_color=c_acc, stroke_width=tratto(4))
        self.rileggi = posa(testo(DIDA_RILEGGI, "etichetta", colore=c_testo, peso=BOLD), FX0, 1062)
        fant = Rectangle(width=px(10), height=px(CONF_6 - ALTO_6 - 24)).move_to(P(662, (ALTO_6 + CONF_6) / 2))
        self.graffa = Brace(fant, direction=RIGHT, buff=0, color=c_att)
        self.scritto = testo("l'ha scritto\nlui", "etichetta", colore=c_att, peso=BOLD).next_to(self.graffa, RIGHT, buff=px(12))
        self.continua = Etichetta("continua").scale(0.9).move_to(P(838, CONF_6))
        x = X(640)
        y_su, y_giu = self.dario[0].blocco.righe[0].puntello.get_center()[1], yc + px(34)
        self.freccia = VGroup(Line([x, y_su - px(24), 0], [x, y_giu, 0], stroke_color=c_acc, stroke_width=tratto(5)),
                              Line([x, y_giu, 0], [x - px(14), y_giu + px(18), 0], stroke_color=c_acc, stroke_width=tratto(5)),
                              Line([x, y_giu, 0], [x + px(14), y_giu + px(18), 0], stroke_color=c_acc, stroke_width=tratto(5)))
        b.aggiungi(*self.dario.values(), self.sotto, self.su10, self.aggancio, self.rileggi, self.graffa, self.scritto,
                   self.continua, self.freccia)
        # le barrette che la corsia della freccia e la graffa chiedono più corte
        self.lunghe = VGroup(*[r.barre for r in (self.dario[1], self.dario[2], self.dario[3], self.c10[0], self.c10[3])],
                             b.sottili)

    def stringi(self, g=None) -> None:
        """Le barrette-sagoma si fermano prima della corsia della freccia (x = 640)."""
        for m in foglie(g if g is not None else self.lunghe):
            x0, x1 = in_px(m.get_left())[0], in_px(m.get_right())[0]
            if x1 > 612:
                m.stretch((612 - x0) / (x1 - x0), 0, about_point=m.get_left())
        if g is None:
            self.accosta()

    def accosta(self, g=None) -> None:
        """«[…]» in coda alla mail segue la barretta accorciata."""
        coda = g if g is not None else self.c10[3].glifi("p")
        coda.shift([X(630) - coda.get_left()[0], 0, 0])

    def stato_finale(self) -> None:
        b = self.b
        b.mestieri("sagoma")
        for r in b.schede[1].mestiere.values():
            r.metti("testo")
            tinta(r.glifi(), self.c_acc)
        b.stato_linee("niente")
        tinta(b.linee.piene[1], self.c_acc)
        b.schede[1].box.set_stroke(self.c_testo)
        op(VGroup(b.sii, b.domanda), 0)
        for k, r in self.dario.items():
            r.metti("ridotto")
        tinta(self.ferramenta, self.c_acc)
        for k, st in ((0, "sagoma"), (1, "testo"), (2, "testo"), (3, "ridotto")):
            self.c10[k].metti(st)
        self.stringi()


class Scena06(ScenaFoglio):
    """Esce «Sii originale.», Dario scrive la sua riga; la frase scende oltre il confine nella mail C10 con «10 su 10»;
    «Di chi è?» e GRANDE (punch) «UNO SOLO»: resta la linea di Dario; poi «l'ha scritto lui», la freccia, «poi rileggi…»."""

    def costruisci(self):
        al = Allestimento6(self)
        b, col = al.b, al.b.col
        c_testo, c_acc, c_att, c_sfondo = al.c_testo, al.c_acc, al.c_att, str(col.sfondo)
        assert self.scena["testo"][1].startswith("l'ha scritto") and self.scena["testo"][2] == "continua"
        b9 = righe_fuoco(B9, TX, CONF + 16, col)
        b.aggiungi(*b9.values())
        # il fotogramma 0 è la geometria della scena 3 (cima 570, confine 720): gli oggetti partono da lì
        carta_6, conf_6, pila_6 = b.carta.copy(), b.confine.copy(), b.pila.copy()
        b.carta.become(scatola(FX0, ALTO, FX1, BASSO, c_att, pieno=c_sfondo))
        b.confine.become(Line(P(FX0 + 16, CONF), P(FX1 - 16, CONF), stroke_color=str(col.secondario), stroke_width=tratto(4)))
        for f, g in zip(b.pila, fogli_pila(CONF, BASSO, col)):
            f.become(g)
        for m in (b.carta, b.confine, b.pila):
            for f in foglie(m):
                del f._pieno
            segna(m)
        giu = DOWN * px(ALTO - ALTO_6)
        b.sottili.shift(giu)
        b.sii.shift(giu)
        prima = Linee(col, ALTO)
        piene_6 = [l.copy() for l in b.linee.piene]
        for l, v in zip(b.linee.piene, prima.piene):
            l.become(v)
            segna(l)
        b.mestieri("sagoma")
        b.stato_linee("piene", c_att, 0.6)
        for k, r in b9.items():
            r.metti("sagoma")
        for r in (*al.dario.values(), *al.c10.values()):
            r.metti("vuoto")
        b.domanda.scale(0.62).move_to(P(916, (SCH_Y1 + ALTO) / 2))
        tinta(b.domanda, c_att, 0.9)
        op(VGroup(al.sotto, al.su10, al.aggancio, al.rileggi, al.graffa, al.scritto, al.continua, al.freccia), 0)
        self.add(b.mondo)                                     # fotogramma 0 pieno: stacco dal filmato della scena 5

        # beat 0 «Allora Dario toglie «sii originale» e scrive una riga che sa solo lui.»
        dario = b.schede[1]
        self.fai(0.5, t_fn(dario, lambda g: g.scale(1.07), 0.1, 0.9, there_and_back),
                 t_fn(dario.box, lambda g: g.set_stroke(c_testo), 0.1, 0.6))
        self.alle(self.istante(0, "toglie") - 0.15)
        su = UP * px(ALTO - ALTO_6)
        lento = rate_functions.ease_in_out_cubic
        self.fai(1.0, t_esce(b.sii, 0, 0.3, sposta=LEFT * px(22), rate=rush_into), verso(b9, "vuoto", 0, 0.66),
                 t_punti(b.carta, carta_6, 0.4, 1, lento), t_punti(b.confine, conf_6, 0.4, 1, lento), t_punti(b.pila, pila_6, 0.4, 1, lento),
                 t_sposta(b.sottili, su, 0.4, 1, lento), [t_punti(l, v, 0.4, 1, lento) for l, v in zip(b.linee.piene, piene_6)],
                 t_sposta(b.domanda, su / 2, 0.4, 1, lento))
        self.alle(self.istante(0, "scrive") - 0.1)
        parole = [(w, k) for k in range(4) for w in parole_di(al.dario[k])]
        n = len(parole)
        tappe = []
        for j, (w, k) in enumerate(parole):
            colore = c_acc if (k == 1 and j - len(parole_di(al.dario[0])) == 1) else c_testo
            tappe.append(t_entra(w, j / (n + 3), (j + 3.5) / (n + 3), sposta=UP * px(8), rate=rush_from, colore=colore))
        self.fai(max(1.0, self.fine_beat(0) - self.t - 0.12), tappe)
        for r in al.dario.values():
            for tipo, g, barra, cas in r.seg:
                r.ora[id(g)] = (1.0, c_testo)

        # beat 1 «E adesso la mail parla della ferramenta. Di chi è?»
        self.beat(1)
        self.fai(0.6, verso(al.dario, "ridotto", 0, 1))
        self.alle(self.istante(1, "parla della") - 0.35)
        # la frase scende in copia dalla metà alta, attraversa il confine e si posa in testa al secondo capoverso
        al.c10[2].ora.update({id(al.c10[2].seg[0][1]): (1.0, c_testo)})
        al.c10[3].ora.update({id(al.c10[3].seg[0][1]): (1.0, c_testo)})
        self.fai(0.8, t_entra(al.frase_giu, 0, 1, sposta=DOWN * al.salto, rate=lento))
        # saluto a sagoma e «[…]» entrano solo a frase posata: nella discesa la frase non passa sopra nessun testo
        self.fai(0.7, verso(al.c10, "sagoma", 0, 0.4, solo=(0,)), verso(al.c10, "testo", 0, 0.4, solo=(1,)),
                 verso(al.c10, "ridotto", 0, 0.5, solo=(3,)),
                 [t_traccia(l, 0.15 + 0.3 * j, 0.5 + 0.3 * j) for j, l in enumerate(al.sotto)], t_traccia(al.aggancio, 0.6, 0.8),
                 t_entra(al.su10, 0.7, 1, sposta=RIGHT * px(14), rate=rush_from))
        self.alle(max(self.t, self.istante(1, "Di chi") - 0.25))
        self.fai(min(0.75, self.fine_beat(1) - self.t - 0.05), [t_op(l, 0, 0, 0.2) for l in b.linee.piene],
                 [t_sale(l, 0.2, 0.8) for l in b.linee.tratt], t_tinta(b.domanda, c_acc, 1, 0.5, 0.8),
                 t_fn(b.domanda, lambda g: g.scale(1.35), 0.5, 1, there_and_back))

        # beat 2 «Stavolta lo sai, e lei è la stessa di prima,»: GRANDE (punch), il secondo e ultimo del reel
        self.beat(2)
        b.stato_linee("niente")                               # compare al ritorno: una linea sola, piena, fino a Dario
        tinta(b.linee.piene[1], c_acc)
        op(b.domanda, 0)
        for r in dario.mestiere.values():
            r.metti("testo")
            tinta(r.glifi(), c_acc)
        self.punch_con_didascalia("UNO\nSOLO", b.dida, tenuta_s=1.0)
        self.alle(self.istante(2, "lei è la stessa") + 0.1)
        self.fai(0.6, t_fn(dario, lambda g: g.scale(1.06), rate=there_and_back))

        # beat 3 «ha solo continuato un inizio che ha scritto lui.»
        self.beat(3)
        self.fai(0.45, t_entra(al.rileggi, sposta=UP * px(14), rate=rush_from))       # subito: resta leggibile più di 2 s
        self.fai(0.8, t_fn(al.lunghe, al.stringi, 0, 0.35, lento), t_fn(al.c10[3].glifi("p"), al.accosta, 0, 0.35, lento), [t_traccia(l, 0.35, 0.8) for l in al.freccia[:1]],
                 t_op(VGroup(*al.freccia[1:]), 1, 0.8, 0.95), t_entra(al.continua, 0.55, 1, scala=0.4, rate=RIMBALZO))
        self.alle(max(self.t, self.istante(3, "ha scritto lui") - 0.3))
        self.fai(0.6, t_entra(al.graffa, 0, 0.6, scala=0.3, rate=RIMBALZO), t_entra(al.scritto, 0.4, 1, sposta=RIGHT * px(16)))


class Scena07(ScenaFoglio):
    """Resta solo il confine. GRANDE (tipografia cinetica): «GENERATIVA» enorme, sotto piccolo «vuol dire»; oltre il
    confine «creativa», barrata, poi «continua». Poi la definizione intera sale piccola, la scheda «tu» e il messaggio."""

    def costruisci(self):
        al = Allestimento6(self)
        b, col = al.b, al.b.col
        c_testo, c_acc, c_att = al.c_testo, al.c_acc, al.c_att
        al.stato_finale()
        resto = VGroup(*[m for m in b.mondo.submobjects if m is not b.confine])
        y_conf, y_conf_fine = 690, 426
        gen = testo("GENERATIVA", "titolo", peso=BOLD)
        gen.scale(px(860) / gen.width)
        posa_blocco(gen, 60, 440)
        vuol = posa(testo("vuol dire", "caption", colore=c_testo), 64, 598)
        creativa = posa(testo("creativa", "punto", colore=c_testo, peso=BOLD), 60, 736)
        continua = posa(testo("continua", "punto", colore=c_acc, peso=BOLD), 60, 736)
        yb = creativa.righe[0].glifi.get_center()[1] - px(6)
        barra = Line([creativa.get_left()[0] - px(10), yb, 0], [creativa.get_right()[0] + px(10), yb, 0], stroke_color=c_acc,
                     stroke_width=tratto(11))
        confine_centro = Line(P(60, y_conf), P(960, y_conf), stroke_color=str(col.secondario), stroke_width=tratto(4))
        confine_fine = Line(P(60, y_conf_fine), P(960, y_conf_fine), stroke_color=str(col.secondario), stroke_width=tratto(4))
        # la chiusura: la scheda «tu» (stessa forma delle tre schede), la riga bianca col cursore, messaggio e CTA
        tu_box = scatola(60, 312, 236, 392, c_att, raggio=18)
        tu_icona = Icona("user", altezza_px=40, colore=c_testo).move_to(P(96, 352))
        tu_nome = posa(testo("tu", "etichetta", peso=BOLD), 130, 332)
        riga_bianca = Line(P(262, 384), P(960, 384), stroke_color=c_testo, stroke_width=tratto(3))
        cursore = Rectangle(width=px(7), height=px(50), stroke_width=0, fill_color=c_testo, fill_opacity=1).move_to(P(272, 352))
        msg = Messaggio(self.scena["messaggio"], larghezza_px=900)
        msg.move_to(P(60, y_conf_fine + 34), aligned_edge=UP + LEFT)
        parole_cta = self.scena["cta"].split()
        meta = len(parole_cta) // 2 + 1
        cta = Etichetta(" ".join(parole_cta[:meta]) + "\n" + " ".join(parole_cta[meta:]))
        cta.move_to([X(60) + cta.width / 2, Y(1192) + cta.height / 2, 0])
        if msg.get_bottom()[1] < cta.get_top()[1] + px(30):
            msg.scale((msg.get_top()[1] - cta.get_top()[1] - px(30)) / msg.height, about_point=msg.get_corner(UP + LEFT))
        b.aggiungi(gen, vuol, creativa, continua, barra, tu_box, tu_icona, tu_nome, riga_bianca, cursore, msg, cta)
        nuovi = VGroup(gen, vuol, creativa, continua, barra, tu_box, tu_icona, tu_nome, riga_bianca, cursore, msg, cta)
        op(nuovi, 0)
        self.add(b.mondo)

        # beat 0 «Generativa non vuol dire creativa, vuol dire che continua.»
        self.fai(0.45, t_op(resto_senza(resto, nuovi), 0, 0, 0.75, rush_into), t_punti(b.confine, confine_centro, 0.3, 1))
        self.fai(0.5, t_entra(gen, scala=0.25, rate=RIMBALZO))
        self.alle(max(self.t, self.istante(0, "non vuol dire") - 0.1))
        self.fai(0.35, t_entra(vuol, sposta=DOWN * px(14), rate=rush_from))
        self.alle(max(self.t, self.istante(0, "creativa") - 0.1))
        self.fai(0.35, t_entra(creativa, sposta=DOWN * px(30), rate=RIMBALZO))
        self.alle(max(self.t, self.istante(0, ", vuol dire") - 0.12))
        self.fai(0.3, t_traccia(barra, rate=rush_from), t_tinta(creativa, c_att, 0.8, 0.4, 1))
        self.alle(max(self.t, min(self.istante(0, "continua") - 0.45, self.fine_beat(0) - 1.0)))
        self.fai(0.7, t_esce(VGroup(creativa, barra), 0, 0.38, sposta=DOWN * px(26), rate=rush_into),
                 t_entra(continua, 0.45, 1, scala=0.45, rate=RIMBALZO))

        # beat 1 «E da dove si parte, glielo scrivi tu.»: un solo passaggio calmo, poi fermo
        self.beat(1)
        k_gen, k_con = 50 / 127.0, 50 / 92.0

        def piccola(g, k, x):
            g.scale(k, about_point=g.get_corner(DOWN + LEFT))
            g.shift([X(x) - g.get_left()[0], Y(284) - g.get_bottom()[1], 0])
        x_vuol = 60 + gen.width * 120 * k_gen + 22
        x_con = x_vuol + vuol.width * 120 + 22
        lento = rate_functions.ease_in_out_cubic
        # uno alla volta, così i tre testi non si attraversano: la definizione resta sempre intera a schermo
        self.fai(1.8, t_fn(gen, lambda g: piccola(g, k_gen, 60), 0, 0.15, lento),
                 t_fn(vuol, lambda g: piccola(g, 1.0, x_vuol), 0.15, 0.27, lento),
                 t_fn(continua, lambda g: g.shift([X(x_con) - g.get_left()[0], 0, 0]), 0.27, 0.33, lento),   # prima di lato, sotto il confine
                 t_fn(continua, lambda g: piccola(g, k_con, x_con), 0.33, 0.42, lento),                       # poi su
                 t_punti(b.confine, confine_fine, 0.33, 0.42, lento),
                 t_entra(VGroup(tu_box, tu_icona, tu_nome), 0.4, 0.58, sposta=RIGHT * px(24), rate=rush_from),
                 t_traccia(riga_bianca, 0.46, 0.64), t_op(cursore, 1, 0.6, 0.66),
                 [t_entra(r, 0.54 + 0.05 * j, 0.74 + 0.05 * j, sposta=UP * px(22)) for j, r in enumerate(msg.righe)],
                 t_entra(cta, 0.86, 1, scala=0.8, rate=RIMBALZO))
        if self.durata_s - self.t > 1.6:
            self.fai(0.5, t_fn(cursore, lambda g: op(g, 0), rate=there_and_back))


def posa_blocco(blocco, x: float, y: float):
    """Come posa, per un blocco già scalato: cima del puntello a y, bordo sinistro a x."""
    r = blocco.righe[0]
    blocco.shift([X(x) - r.glifi.get_left()[0], Y(y) - r.puntello.get_top()[1], 0])
    return blocco


def resto_senza(resto: VGroup, nuovi: VGroup) -> VGroup:
    esclusi = {id(m) for m in nuovi.submobjects}
    return VGroup(*[m for m in resto.submobjects if id(m) not in esclusi])
