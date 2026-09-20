"""Animazioni di «L'IA e il tuo lavoro: meno paura, più controllo»
(contenuti/sceneggiature/2026-09-20-ia-e-lavoro.md).

Le scene 1 (hook) e 4 sono a filmato: non hanno una classe. La scena 2 arriva da uno stacco sul filmato dell'hook e
la scena 5 da uno stacco sulla scena 4: il loro fotogramma 0 è già pieno e si regge da solo.

Filo visivo (Note di produzione della sceneggiatura), tre oggetti che tornano sempre uguali:
1. **le dieci icone `user`** (`fila`): spente e pulsanti (2), sei accese (2), sbarrate e poi tre e tre (3), piccole
   in alto (5-6), di nuovo al centro nella posizione e nella scala della scena 2 (7);
2. **il numero grande con la fonte piccola sotto**, sempre nello stesso punto (centro a `NUM_CY`, blocco della fonte
   ancorato in basso a `FONTE_CY`): «6 su 10 · esposti · economie avanzate · Fondo Monetario, 2024» (2-3-7),
   «+32%» e «19 punti in meno · Harvard, 2023» (5). Mai due numeri insieme a schermo;
3. **la tessera che si spezza**: «il tuo lavoro» in cinque pezzi senza parole (3), «resoconto del mese» in quattro
   pezzi con due parole ciascuno (6).

Regola del presentatore (niente testo denso): a schermo una-tre parole per volta, numeri grandi, fonte piccola,
icone. Nessun documento e nessun paragrafo: il massimo di parole leggibili di contenuto è 13 (scena 6, fine).
`parole_a_schermo()` le conta alla fine di ogni passaggio (REEL_CONTA_PAROLE=1 le stampa).

Come è fatto il file. Tutto quello che una scena mostra è costruito all'inizio dentro un solo gruppo (`mondo`), già
al suo posto; ciò che non si vede ancora ha opacità zero. Ogni passaggio è una sola animazione `Tappe` sul mondo:
una lista di modifiche, ognuna con la sua finestra (a, b) del passaggio, e le finestre di chi esce e di chi entra
non si accavallano mai (prima esce il testo vecchio, poi si muovono i riquadri, poi entra il testo nuovo). Così
nessun oggetto entra o esce dalla lista della scena e nessun riquadro finisce sopra un testo fermo.
"""
from __future__ import annotations

import math
import os
from dataclasses import dataclass
from typing import Callable

import numpy as np
from manim import (BOLD, LEFT, ORIGIN, RIGHT, UP, Animation, Circle, Line, Mobject, Rectangle, RoundedRectangle,
                   ValueTracker, VGroup, VMobject, linear, rate_functions, smooth, there_and_back)
from manim.utils.family import extract_mobject_family_members

from tools.anim.base import ScenaReel
from tools.anim.componenti import Etichetta, Icona, Riga, piano, testo, tratto
from tools.anim.misure import CORPO_PX, px

# --- testi a schermo (dalla sceneggiatura e dalle Note di produzione / condizioni del revisore) ----------------------

DIDA_FILA = "dieci posti di lavoro in un paese avanzato,\nper far vedere una proporzione"
FONTE_FMI = "Fondo Monetario, 2024"
MISURA_FMI = "esposti · economie avanzate"
FONTE_HARVARD = "Harvard, 2023"
MISURA_QUALITA = "qualità votata da umani,\ncontro chi non l'aveva"
FONTE_QUALITA = "18 compiti · Harvard, 2023"
MISURA_PUNTI = "risposte corrette, un compito solo"
DENTRO = "alla sua portata"
FUORI = "fuori"
ESEMPIO = "esempio"
TESSERA_TUA = "il tuo lavoro"
RISENTIRNE = "potrebbe\nrisentirne"
VANTAGGIO = "potrebbe trarne\nvantaggio"
PEZZI_6 = [("database", "i numeri"), ("file-text", "la bozza"), ("book-open", "l'ordine"), ("lightbulb", "la conclusione")]
TESSERA_RESOCONTO = "resoconto del mese"
NOSTRO = "esempio nostro"
GARANZIA = "nessuna garanzia sul posto"
PROMESSA = "come funziona e dove sbaglia"
SUBIRLA = "SUBIRLA"
SAPERLA = "SAPERLA\nUSARE"

# --- impaginazione, in px della tela (origine in alto a sinistra) ------------------------------------------------------

SX, DX, ALTO, BASSO = 60, 960, 220, 1196          # area contenuto con il riquadro in basso a destra
CX = 510

ICONA_PX = 120                                     # altezza dell'icona `user` a scala 1
PASSO_X, PASSO_Y = 170, 170                        # passo della fila 5 × 2
FILA_CASA = (CX, 430, 1.00)                        # scena 2 (fotogramma 0) e scena 7: la posizione di riferimento
FILA_SU = (CX, 370, 0.85)                          # scena 2 beat 3 e scena 3: spinta in alto dal numero
FILA_ALTA = (CX, 295, 0.50)                        # scene 5-6: contesto, piccola in alto
ACCESE = (0, 1, 2, 5, 6, 7)                        # le sei esposte: le tre colonne di sinistra, due righe

NUM_CY = 850                                       # centro del numero grande (e del «?» che ne prende il posto)
NUM_PICCOLO_CY = 530                               # dove il numero torna piccolo, sotto la fila (scena 3)
FONTE_CY = 1082                                    # riga della fonte: il blocco «cosa misura» cresce in su da qui
PASSO_RIGA = 48                                    # passo fra le righe piccole del blocco della fonte
NUM_PX, UNITA_PX, PICCOLO_PX = 140, 84, 44         # corpo del numero, dell'unità accanto, del numero rimpicciolito

# scena 3: la tessera «il tuo lavoro» e i suoi cinque pezzi
TESS3 = (CX, 850, 420, 220)                        # centro x, centro y, larghezza, altezza da chiusa
PEZZI3_CY, PEZZI3_LATO, PEZZI3_PASSO = 820, 110, 130
PAROLA_CY = 650                                    # «persi» grande, poi la pillola «esposto»

# scena 5: il bordo frastagliato, le diciotto tessere dentro e la tessera fuori
BLOB = (410, 615, 290, 145)                        # centro x, centro y, raggio x, raggio y dell'ellisse di base
GRIGLIA18 = (6, 3, 66, 50, 58, 42)                 # colonne, righe, passo x, passo y, larghezza, altezza
FUORI_C = (865, 615, 110, 84)                      # la tessera fuori dal bordo
FUORI_QM_CY, DENTRO_CY, FUORI_CY = 468, 400, 712
NUM5_CY, NUM5_PX = 870, 130                        # nella scena 5 il numero è un po' più basso e più corto

# scena 6: i quattro pezzi del resoconto
COL_SX, COL_DX, PEZZO_W = 280, 730, 440           # colonne dei pezzi e larghezza del pezzo
GRANDE6 = (60, 360, 950, 900)                      # la tessera cresciuta: x0, y0, x1, y1
SLOT_SX = (560, 700, 880)                          # le tre altezze della colonna di sinistra
SLOT_DX = (560, 700)                               # le due altezze della colonna del «bot»


def X(v: float) -> float:
    return (v - 540) / 120


def Y(v: float) -> float:
    return (960 - v) / 120


def C(x: float, y: float):
    return np.array([X(x), Y(y), 0.0])


def metti(mob, x: float, y: float):
    """Centra un mobject in (x, y) px."""
    return mob.move_to(C(x, y))


def posa_basso(blocco, x: float, cy_ultima: float):
    """Centra un blocco di righe in x, con il centro dell'ultima riga a cy_ultima px."""
    n = len(blocco.righe)
    return metti(blocco, x, cy_ultima - (n - 1) * PASSO_RIGA / 2)


RUOLI_GRANDI = ("punch", "titolo", "punto", "messaggio", "caption", "token", "piede")


def grande(s: str, alt_px: float, colore, mono: bool = False, allinea: str = "center"):
    """Un testo in grassetto alto esattamente alt_px (l'altezza «Hg» che misurano i controlli).

    Si compone nel corpo più grande che tiene la frase sulle righe volute e poi si scala. Due trappole insieme:
    `MarkupText` passa a Pango una larghezza di riga fissa (`pango_width=500` in manim/mobject/text/text_mobject.py),
    quindi nei corpi grandi una frase di 28 caratteri va a capo da sola; ma comporre tutto in un corpo piccolo e
    ingrandire di cinque volte moltiplica l'arrotondamento delle avanzate di Pango e le lettere si distanziano male
    («SU BIRL A»). Gli a capo qui li decide solo «\n»."""
    attese = len([r for r in str(s).split("\n") if r.strip()])
    for ruolo in RUOLI_GRANDI:
        b = testo(s, ruolo, colore=colore, peso=BOLD, mono=mono, allinea=allinea, interlinea=0.12)
        if len(b.righe) == attese and all(_una_riga_sola(r) for r in b.righe):
            return b.scale(alt_px / CORPO_PX[ruolo])
    return b.scale(alt_px / CORPO_PX[RUOLI_GRANDI[-1]])


def _una_riga_sola(riga) -> bool:
    """Pango ha mandato a capo da solo dentro la riga? (il numero di `Riga` non cambia: cambia l'altezza dei glifi)"""
    return not riga.allineata or riga.glifi.height < riga.puntello.height * 1.35


def sagoma_rett(x0: float, y0: float, x1: float, y1: float, raggio: float = 20) -> RoundedRectangle:
    r = RoundedRectangle(corner_radius=px(raggio), width=px(x1 - x0), height=px(y1 - y0), stroke_width=0, fill_opacity=0)
    return metti(r, (x0 + x1) / 2, (y0 + y1) / 2)


def rett(x0: float, y0: float, x1: float, y1: float, colore, raggio: float = 20, spessore: float = 3) -> RoundedRectangle:
    r = RoundedRectangle(corner_radius=px(raggio), width=px(x1 - x0), height=px(y1 - y0), stroke_color=colore,
                         stroke_width=tratto(spessore), fill_opacity=0)
    return metti(r, (x0 + x1) / 2, (y0 + y1) / 2)


def bordo_frastagliato(cx: float, cy: float, rx: float, ry: float, colore, n: int = 30, spessore: float = 5) -> VMobject:
    """La frontiera irregolare della scena 5: una polilinea chiusa con punte verso l'esterno, da disegnare con
    una tappa `traccia`. Non è un componente della libreria (vedi le Note di produzione della sceneggiatura)."""
    pts = []
    for k in range(n):
        th = 2 * math.pi * k / n
        d = 1.0 + (0.17 if k % 2 else -0.02) * (0.55 + 0.45 * math.sin(3.0 * th + 1.1))
        pts.append(C(cx + rx * d * math.cos(th), cy - ry * d * math.sin(th)))
    m = VMobject(stroke_color=colore, stroke_width=tratto(spessore))
    m.set_points_as_corners(pts + [pts[0]])
    return m


def fila_icone(col_spenta, scala: float, centro_x: float, centro_y: float) -> VGroup:
    """Le dieci icone `user`, 5 × 2, tutte spente: l'oggetto del loop di tutto il reel."""
    g = VGroup()
    for r in range(2):
        for c in range(5):
            ic = Icona("user", altezza_px=ICONA_PX, colore=col_spenta)
            metti(ic, CX + (c - 2) * PASSO_X, 430 + (r - 0.5) * PASSO_Y)
            g.add(ic)
    porta(g, scala, C(centro_x, centro_y))
    return g


def tessera(nome_icona: str, x: float, y: float, w: float, h: float, colore, icona_px: float) -> VGroup:
    """Un riquadro con la sola icona dentro: un *compito*, mai una persona (condizione ⚠️C del revisore)."""
    g = VGroup(rett(x - w / 2, y - h / 2, x + w / 2, y + h / 2, colore, raggio=min(16, h / 4), spessore=3))
    g.add(metti(Icona(nome_icona, altezza_px=icona_px, colore=colore), x, y))
    return g


def spezza(s: str, dopo: int) -> str:
    """Manda a capo dopo `dopo` parole (le CTA lunghe: `Etichetta` non va a capo da sola)."""
    p = s.split()
    return " ".join(p[:dopo]) + "\n" + " ".join(p[dopo:])


# --- opacità, tinte e scala che non toccano i puntelli ------------------------------------------------------------------

def foglie(m: Mobject) -> list:
    return m.family_members_with_points()


def segna(m: Mobject) -> Mobject:
    """Ricorda l'opacità piena di ogni foglia: i puntelli invisibili delle righe restano a zero qualunque cosa succeda."""
    for f in foglie(m):
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


def porta(g: Mobject, k: float, centro=None) -> None:
    """Scala il gruppo di k (spessori dei tratti compresi: le icone Lucide non scalano il contorno da sole) e,
    se dato, lo porta a `centro`."""
    g.scale(k)
    if abs(k - 1.0) > 1e-9:
        for f in foglie(g):
            w = f.get_stroke_width()
            if w > 0:
                f.set_stroke(width=w * k, family=False)
    if centro is not None:
        g.move_to(centro)


def etichetta(m: Mobject) -> Mobject:
    """Segna i testi di m come titoli, note o didascalie: `parole_a_schermo` li conta a parte."""
    for x in m.get_family():
        if isinstance(x, Riga):
            x._etichetta = True
    return m


def parole_a_schermo(scena) -> tuple[int, int, list[str]]:
    """Quante parole si leggono adesso: (contenuto, etichette, testi). Regola del presentatore: a fine beat, oltre
    una ventina di parole di contenuto (titoli ed etichette esclusi) è troppo."""
    contenuto, etichette, testi = 0, 0, []
    for m in extract_mobject_family_members(scena.mobjects):
        if not isinstance(m, Riga) or not m.allineata:
            continue
        gl, k, viste = m.glifi.submobjects, 0, []
        for w in m.piano.split():
            g = gl[k:k + len(w)]
            k += len(w)
            if any(c.isalnum() for c in w) and any(x.get_fill_opacity() > 0.3 for x in g):
                viste.append(w)
        if viste:
            if getattr(m, "_etichetta", False):
                etichette += len(viste)
            else:
                contenuto += len(viste)
                testi.append(" ".join(viste))
    return contenuto, etichette, testi


# --- l'animazione a tappe (copiata dal reel precedente: candidata alla libreria) -----------------------------------------

@dataclass
class Tappa:
    pezzo: Mobject
    fn: Callable
    a: float = 0.0
    b: float = 1.0
    rate: Callable = smooth
    traccia: bool = False      # il pezzo si disegna a tratto (come Create) invece di interpolare


class Tappe(Animation):
    """Più modifiche sulla stessa radice già in scena, ognuna nella sua finestra (a, b) del passaggio. `fn` riceve un
    gruppo con le foglie del pezzo e le porta allo stato d'arrivo; le tappe sullo stesso pezzo si concatenano."""

    def __init__(self, radice: Mobject, tappe: list, **kw):
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


def t_porta(pezzo, k, centro, a=0.0, b=1.0, rate=smooth) -> Tappa:
    return Tappa(pezzo, lambda g: porta(g, k, centro), a, b, rate)


def t_box(box, x0, y0, x1, y1, raggio=20, a=0.0, b=1.0, rate=smooth) -> Tappa:
    """Cambia la misura di un riquadro arrotondato senza toccarne i colori (stessa struttura di punti)."""
    tgt = sagoma_rett(x0, y0, x1, y1, raggio)

    def fn(g):
        g[0].set_points(tgt.get_points())
    return Tappa(box, fn, a, b, rate)


class Mondo(ScenaReel):
    """Base comune: il gruppo unico `mondo`, il conteggio delle parole leggibili e il passaggio a tappe."""

    def apri(self, mondo: VGroup) -> None:
        self.mondo = segna(mondo)
        self.add(mondo)

    def passa(self, tappe: list, run_time: float, **kw) -> None:
        self.play(Tappe(self.mondo, tappe), run_time=self.arrotonda(run_time), **kw)

    def beat(self, i: int) -> None:
        super().beat(i)
        self.conta(f"fine beat {i - 1}" if i else "inizio")

    def conta(self, quando: str) -> None:
        if os.environ.get("REEL_CONTA_PAROLE"):
            c, e, testi = parole_a_schermo(self)
            print(f"  [{self.scena.get('n')}] {quando}: {c} parole di contenuto, {e} di etichette | {testi}")

    def chiudi(self) -> None:
        self.conta("fine scena")
        super().chiudi()


# --- scena 2 ------------------------------------------------------------------------------------------------------------

class Scena02(Mondo):
    """Dieci posti di lavoro, il vuoto della scommessa, poi il «6» arriva enorme (tipografia cinetica).

    Fotogramma 0 già pieno: si arriva da uno stacco sul filmato dell'hook.
    """

    def costruisci(self):
        col = self.cfg.palette
        fila = fila_icone(col.attenuato, FILA_CASA[2], FILA_CASA[0], FILA_CASA[1])
        dida = etichetta(testo(DIDA_FILA, "piede", colore=col.attenuato, allinea="center"))
        metti(dida, CX, 661)
        trattino = metti(Rectangle(width=px(90), height=px(10), stroke_width=0, fill_color=col.attenuato, fill_opacity=1),
                         CX, NUM_CY)
        qm = metti(grande("?", 100, col.accento), CX, NUM_CY)
        num = metti(grande(self.scena["testo"][0], NUM_PX, col.accento, mono=True), CX, NUM_CY)
        misura = etichetta(testo(MISURA_FMI, "piede", colore=col.attenuato, allinea="center"))
        metti(misura, CX, FONTE_CY - PASSO_RIGA)
        fonte = etichetta(testo(self.scena["testo"][1], "piede", colore=col.attenuato, allinea="center"))
        metti(fonte, CX, FONTE_CY)

        mondo = VGroup(fila, dida, trattino, qm, num, misura, fonte)
        self.apri(mondo)
        for m in (trattino, qm, num, misura, fonte):
            op(m, 0)
        porta(num, 0.25, C(CX, NUM_CY))

        # beat 0 — le dieci icone pulsano una volta, in sequenza da sinistra
        ordine = [r * 5 + c for c in range(5) for r in range(2)]
        pulsa = []
        for k, i in enumerate(ordine):
            a = 0.05 * k
            pulsa.append(Tappa(fila[i], lambda g: (porta(g, 1.14, g.get_center()), tinta(g, col.testo)), a, a + 0.16))
            pulsa.append(Tappa(fila[i], lambda g: (porta(g, 1 / 1.14, g.get_center()), tinta(g, col.attenuato)),
                               a + 0.16, a + 0.34))
        self.passa(pulsa, 1.6)

        # beat 1 — la fonte al suo posto (lì starà per tutto il reel) e, dove andrà il numero, un trattino: niente da contare
        self.beat(1)
        self.passa([t_op(fonte, 1, 0, 1, rate_functions.ease_out_sine)], 0.6)
        self.attendi_fino(self.inizi_frasi[1] + 2.1)
        self.passa([t_op(trattino, 1)], 0.4)

        # beat 2 — il vuoto della scommessa: un «?» in accento al posto del numero, che pulsa
        self.beat(2)
        self.passa([t_op(trattino, 0, 0, 0.4), t_op(qm, 1, 0.45, 1.0)], 0.7)
        self.passa([Tappa(qm, lambda g: porta(g, 1.18, C(CX, NUM_CY)), 0, 1, there_and_back)], 0.9)

        # beat 3 — GRANDE (tipografia cinetica): «sei» accende sei icone e il numero arriva enorme
        self.beat(3)
        self.passa([t_op(qm, 0, 0, 0.16),
                    t_porta(fila, FILA_SU[2] / FILA_CASA[2], C(FILA_SU[0], FILA_SU[1]), 0.08, 0.7),
                    Tappa(dida, lambda g: g.shift(C(CX, 560) - C(CX, 661)), 0.08, 0.7),
                    *[t_tinta(fila[i], col.accento, 1, 0.3, 0.72) for i in ACCESE],
                    Tappa(num, lambda g: (porta(g, 4.0, C(CX, NUM_CY)), op(g, 1)), 0.2, 0.86,
                          rate_functions.ease_out_back),
                    t_op(misura, 1, 0.86, 1.0)], 1.25)


# --- scena 3 ------------------------------------------------------------------------------------------------------------

class Scena03(Mondo):
    """«Persi» è la lettura sbagliata: un lavoro è un mazzo di compiti (metamorfosi), e di quei sei metà e metà.

    Parte dall'ultimo fotogramma della scena 2. «persi» esce del tutto prima che entri «esposto» (condizione 6 del
    revisore) e la correzione dura molto più delle sagome sbarrate: «esposto» resta fino alla fine della scena.
    I cinque pezzi non si leggono come un conto: se ne accendono tre non contigui, con «esempio» sotto e
    «stime, non previsioni» in fondo (condizione 5).
    """

    ACCESI = (0, 1, 3)          # quali dei cinque pezzi si accendono: non contigui, non è un conto

    def costruisci(self):
        col = self.cfg.palette
        fila = fila_icone(col.attenuato, FILA_SU[2], FILA_SU[0], FILA_SU[1])
        for i in ACCESE:
            fila[i].set_stroke(col.accento)
        sbarre = VGroup()
        for i in ACCESE:
            c, w = fila[i].get_center(), fila[i].width / 2 + px(10)
            sbarre.add(Line(c + LEFT * w, c + RIGHT * w, stroke_color=col.attenuato, stroke_width=tratto(6)))
        dida = etichetta(metti(testo(DIDA_FILA, "piede", colore=col.attenuato, allinea="center"), CX, 560))
        persi = metti(grande("persi", 140, col.attenuato), CX, 370)

        viagg = Icona("user", altezza_px=ICONA_PX, colore=col.accento)
        porta(viagg, FILA_SU[2], fila[6].get_center())
        box = rett(CX - 210, 735, CX + 210, 905, col.secondario, raggio=24)
        box.set_points(sagoma_rett(CX - 58, 762, CX + 58, 878, 24).get_points())
        titolo = etichetta(metti(testo(TESSERA_TUA, "etichetta", colore=col.secondario, peso=BOLD, allinea="center"),
                                 CX, 661))
        pezzi = VGroup(*[tessera("file-text", CX + (k - 2) * PEZZI3_PASSO, PEZZI3_CY, PEZZI3_LATO, PEZZI3_LATO,
                                 col.attenuato, 54) for k in range(5)])
        esempio = etichetta(metti(testo(ESEMPIO, "piede", colore=col.attenuato, allinea="center"), CX, 920))

        esposto = etichetta(metti(Etichetta(self.scena["testo"][0]), CX, 679))
        ganci = VGroup()
        for dx_, k in ((-78, 0), (-18, 1), (52, 3)):
            ganci.add(Line(C(CX + dx_, 722), C(CX + (k - 2) * PEZZI3_PASSO, 762),
                           stroke_color=col.accento, stroke_width=tratto(4)))

        num = metti(grande("6 su 10", PICCOLO_PX, col.accento, mono=True), CX, 986)
        porta(num, NUM_PX / PICCOLO_PX, C(CX, NUM_CY))
        misura = etichetta(metti(testo(MISURA_FMI, "piede", colore=col.attenuato, allinea="center"), CX, FONTE_CY - PASSO_RIGA))
        fonte = etichetta(metti(testo(FONTE_FMI, "piede", colore=col.attenuato, allinea="center"), CX, FONTE_CY))
        stime = etichetta(metti(testo(self.scena["testo"][2], "piede", colore=col.attenuato, allinea="center"),
                                CX, FONTE_CY + PASSO_RIGA))

        meta = etichetta(metti(Etichetta(self.scena["testo"][1], pieno=False), CX, 800))
        sx = etichetta(metti(testo(RISENTIRNE, "piede", colore=col.attenuato, allinea="center"), 221, 544))
        dx = etichetta(metti(testo(VANTAGGIO, "piede", colore=col.attenuato, allinea="center"), 799, 544))

        mondo = VGroup(fila, sbarre, viagg, box, pezzi, dida, persi, titolo, esposto, ganci, esempio, num, misura,
                       fonte, stime, meta, sx, dx)
        self.apri(mondo)
        for m in (sbarre, viagg, box, pezzi, persi, titolo, esposto, ganci, esempio, stime, meta, sx, dx):
            op(m, 0)
        for k in range(5):                      # i cinque pezzi partono impilati dentro la tessera chiusa
            pezzi[k].shift(C(CX, 820) - C(CX + (k - 2) * PEZZI3_PASSO, PEZZI3_CY))

        # beat 0 — il «6» torna piccolo sotto la fila, le sei accese diventano sagome sbarrate, «persi» le copre
        self.passa([Tappa(num, lambda g: porta(g, PICCOLO_PX / NUM_PX, C(CX, 986)), 0, 0.5),
                    *[t_tinta(fila[i], col.attenuato, 1, 0.15, 0.55) for i in ACCESE],
                    t_op(fila, 0.4, 0.3, 0.75),
                    Tappa(sbarre, lambda g: op(g, 0.8), 0.35, 0.7),
                    t_op(persi, 1, 0.62, 1.0)], 1.5)
        self.verifica("«persi» a schermo")

        # beat 1 — GRANDE (metamorfosi): un'icona si stacca, diventa la tessera «il tuo lavoro», che si apre in cinque
        self.beat(1)
        self.passa([t_op(fila[6], 0.12, 0.05, 0.4),
                    t_op(viagg, 0.9, 0, 0.1),
                    Tappa(viagg, lambda g: porta(g, 1.02 / FILA_SU[2], C(CX, 820)), 0.0, 0.45,
                          rate_functions.ease_in_out_sine),
                    t_op(box, 1, 0.42, 0.52),
                    t_box(box, CX - 210, 735, CX + 210, 905, 24, 0.42, 0.66, rate_functions.ease_out_back),
                    t_op(titolo, 1, 0.54, 0.72),
                    t_op(viagg, 0, 0.74, 0.84),
                    t_op(box, 0, 0.74, 0.86),
                    t_op(pezzi, 1, 0.80, 0.88),
                    *[Tappa(pezzi[k], lambda g, k=k: g.shift(C(CX + (k - 2) * PEZZI3_PASSO, PEZZI3_CY) - C(CX, 820)),
                            0.84, 1.0, rate_functions.ease_out_back) for k in range(5)]], 2.0)
        self.attendi_fino(self.inizi_frasi[1] + 2.45)
        self.passa([*[t_tinta(pezzi[k], col.accento, 1, 0.12 * j, 0.5 + 0.12 * j) for j, k in enumerate(self.ACCESI)],
                    t_op(esempio, 1, 0.55, 1.0)], 0.9)

        # beat 2 — «persi» esce del tutto, poi entra «esposto», agganciato ai soli pezzi accesi
        self.beat(2)
        self.passa([t_op(persi, 0, 0, 0.22, rate_functions.rush_into),
                    t_op(titolo, 0, 0, 0.22),
                    t_op(sbarre, 0, 0.2, 0.46),
                    t_op(fila, 1, 0.24, 0.6),
                    *[t_tinta(fila[i], col.accento, 0.12 if i == 6 else 1, 0.24, 0.6) for i in ACCESE],
                    t_op(esposto, 1, 0.42, 0.68),
                    Tappa(ganci, lambda g: op(g, 1), 0.7, 0.92, smooth, traccia=True),
                    t_op(stime, 1, 0.86, 1.0)], 1.4)

        # beat 3 — la tessera si richiude e torna nella fila; le sei si staccano in due gruppi da tre
        self.beat(3)
        self.passa([t_op(ganci, 0, 0, 0.18),
                    t_op(dida, 0, 0, 0.18),
                    t_op(esempio, 0, 0.45, 0.6),
                    *[Tappa(pezzi[k], lambda g, k=k: g.shift(C(CX, 820) - C(CX + (k - 2) * PEZZI3_PASSO, PEZZI3_CY)),
                            0.2, 0.56, rate_functions.ease_in_sine) for k in range(5)],
                    t_op(pezzi, 0, 0.5, 0.6),
                    t_op(viagg, 0.9, 0.56, 0.64),
                    Tappa(viagg, lambda g: porta(g, FILA_SU[2] / 1.02, fila[6].get_center()), 0.58, 0.92,
                          rate_functions.ease_in_out_sine),
                    t_op(viagg, 0, 0.92, 0.98),
                    t_tinta(fila[6], col.accento, 1, 0.88, 1.0)], 1.5)
        self.attendi_fino(self.inizi_frasi[3] + 1.8)
        centri = {0: (111, 370), 1: (221, 370), 2: (331, 370), 5: (689, 370), 6: (799, 370), 7: (909, 370),
                  3: (455, 310), 4: (565, 310), 8: (455, 430), 9: (565, 430)}
        self.passa([*[Tappa(fila[i], lambda g, i=i: g.move_to(C(*centri[i])), 0.0, 0.45,
                            rate_functions.ease_in_out_sine) for i in (3, 4, 8, 9)],
                    *[Tappa(fila[i], lambda g, i=i: g.move_to(C(*centri[i])), 0.5, 1.0,
                            rate_functions.ease_out_back) for i in ACCESE]], 1.3)
        self.passa([t_op(sx, 1, 0, 0.45), t_op(dx, 1, 0, 0.45), t_op(meta, 1, 0.5, 1.0)], 0.9)


# --- il numero che sale (la libreria non ha un contatore nel corpo che serve qui: vedi le Note di animazione) ------------

class Numero(VGroup):
    """Un numero grande che sale fino al valore, con il bordo destro fermo (l'unità accanto non balla).
    Ha un updater: sta fuori dal `mondo` e va fermato con `ferma()` prima della fine del beat."""

    def __init__(self, valore: float, alt_px: float, colore, destra: float, cy: float, prefisso: str = "+",
                 suffisso: str = "%", **kw):
        super().__init__(**kw)
        self.alt_px, self.colore, self.prefisso, self.suffisso = alt_px, colore, prefisso, suffisso
        self.destra, self.cy = destra, cy
        self.v = ValueTracker(valore)
        self._scritto = self._scrivi(valore)
        self.corpo = self._posa(self._crea(self._scritto))
        self.add(self.corpo)
        self.corpo.add_updater(self._agg)

    def _scrivi(self, v: float) -> str:
        return f"{self.prefisso}{int(round(v))}{self.suffisso}"

    def _crea(self, s: str):
        return grande(s, self.alt_px, self.colore, mono=True)

    def _posa(self, b):
        return b.move_to([self.destra - b.width / 2, Y(self.cy), 0])

    def _agg(self, m) -> None:
        s = self._scrivi(self.v.get_value())
        if s != self._scritto:
            self._scritto = s
            m.become(self._posa(self._crea(s)))

    def sale(self, a: float, **kw):
        kw.setdefault("rate_func", rate_functions.ease_out_cubic)
        return self.v.animate(**kw).set_value(a)

    def ferma(self) -> None:
        self.corpo.clear_updaters()


def coppia_numero(num_s: str, unita_s: str, alt_px: float, cy: float, col_num, col_unita):
    """Il numero grande e la sua unità accanto, allineati sulla linea di base e centrati nell'area.
    Ritorna (numero, unità, x del bordo destro del numero) in unità Manim."""
    n = grande(num_s, alt_px, col_num, mono=True)
    u = testo(unita_s, "messaggio", colore=col_unita, peso=BOLD)
    tot = n.width + px(28) + u.width
    x0 = X(CX) - tot / 2
    n.move_to([x0 + n.width / 2, Y(cy), 0])
    u.move_to([x0 + n.width + px(28) + u.width / 2, Y(cy), 0])
    u.shift(UP * (n.righe[0].puntello.get_bottom()[1] - u.righe[0].puntello.get_bottom()[1]))
    return n, u, float(n.get_right()[0])


# --- scena 5 ------------------------------------------------------------------------------------------------------------

class Scena05(Mondo):
    """La frontiera frastagliata: dentro si guadagna (+32%), fuori si peggiora (punch «PEGGIO», 19 punti in meno).

    Fotogramma 0 già pieno: si arriva da uno stacco sul filmato della scena 4, ma lo stato è quello con cui finisce
    la scena 3 (le sei esposte divise in due gruppi da tre). Le diciotto tessere sono **compiti**, non persone:
    l'icona dentro non è `user` (condizione ⚠️C). L'etichetta «qualità votata da umani, contro chi non l'aveva ·
    18 compiti» entra insieme al contatore e resta finché resta il numero (condizione ⚠️A).
    """

    def costruisci(self):
        col = self.cfg.palette
        bx, by, brx, bry = BLOB
        nc, nr, px_, py_, tw, th = GRIGLIA18

        fila = fila_icone(col.attenuato, FILA_SU[2], FILA_SU[0], FILA_SU[1])
        for i in ACCESE:
            fila[i].set_stroke(col.accento)
        centri3 = {0: (111, 370), 1: (221, 370), 2: (331, 370), 5: (689, 370), 6: (799, 370), 7: (909, 370),
                   3: (455, 310), 4: (565, 310), 8: (455, 430), 9: (565, 430)}
        for i, c in centri3.items():
            fila[i].move_to(C(*c))
        esposto = etichetta(metti(Etichetta("esposto"), CX, 679))
        meta = etichetta(metti(Etichetta("metà e metà", pieno=False), CX, 800))
        sx = etichetta(metti(testo(RISENTIRNE, "piede", colore=col.attenuato, allinea="center"), 221, 544))
        dx = etichetta(metti(testo(VANTAGGIO, "piede", colore=col.attenuato, allinea="center"), 799, 544))
        num3 = metti(grande("6 su 10", PICCOLO_PX, col.accento, mono=True), CX, 986)
        mis3 = etichetta(metti(testo(MISURA_FMI, "piede", colore=col.attenuato, allinea="center"), CX, FONTE_CY - PASSO_RIGA))
        fon3 = etichetta(metti(testo(FONTE_FMI, "piede", colore=col.attenuato, allinea="center"), CX, FONTE_CY))
        stime = etichetta(metti(testo("stime, non previsioni", "piede", colore=col.attenuato, allinea="center"),
                                CX, FONTE_CY + PASSO_RIGA))
        vecchio = VGroup(esposto, meta, sx, dx, num3, mis3, fon3, stime)

        bordo = bordo_frastagliato(bx, by, brx, bry, col.secondario)
        dentro_et = etichetta(metti(testo(DENTRO, "piede", colore=col.secondario, allinea="center"), bx, DENTRO_CY))
        celle = VGroup()
        for r in range(nr):
            for c in range(nc):
                celle.add(tessera("file-text", bx + (c - (nc - 1) / 2) * px_, by + (r - (nr - 1) / 2) * py_,
                                  tw, th, col.attenuato, 26))
        sola = tessera("file-text", FUORI_C[0], FUORI_C[1], FUORI_C[2], FUORI_C[3], col.testo, 48)
        fuori_et = etichetta(metti(testo(FUORI, "piede", colore=col.attenuato, allinea="center"), FUORI_C[0], FUORI_CY))
        qm = metti(grande("?", 120, col.accento), FUORI_C[0], FUORI_QM_CY)

        n19, u19, _ = coppia_numero(*self.scena["testo"][1].split(" ", 1), NUM5_PX, NUM5_CY, col.accento, col.testo)
        mis_q1 = etichetta(metti(testo("qualità votata da umani,", "piede", colore=col.attenuato, allinea="center"),
                                 CX, FONTE_CY - 2 * PASSO_RIGA))
        mis_q2 = etichetta(metti(testo("contro chi non l'aveva · 18 compiti", "piede", colore=col.attenuato,
                                       allinea="center"), CX, FONTE_CY - PASSO_RIGA))
        mis_p = etichetta(metti(testo(MISURA_PUNTI, "piede", colore=col.attenuato, allinea="center"),
                                CX, FONTE_CY - PASSO_RIGA))
        fonte = etichetta(metti(testo(self.scena["testo"][2], "piede", colore=col.attenuato, allinea="center"), CX, FONTE_CY))

        _n32, u32, destra32 = coppia_numero(*self.scena["testo"][0].split(" ", 1), NUM5_PX, NUM5_CY, col.accento, col.testo)

        mondo = VGroup(vecchio, fila, bordo, dentro_et, celle, sola, fuori_et, qm, n19, u19, u32, mis_q1, mis_q2,
                       mis_p, fonte)
        self.apri(mondo)
        for m in (bordo, dentro_et, celle, sola, fuori_et, qm, n19, u19, u32, mis_q1, mis_q2, mis_p, fonte):
            op(m, 0)

        # il contatore vive fuori dal mondo (ha un updater che ricostruisce le cifre)
        cnt = Numero(0, NUM5_PX, col.accento, destra32, NUM5_CY)
        self.add(cnt)
        cnt.set_opacity(0)

        # beat 0 — esce tutto, le dieci icone si attenuano e salgono, e si disegna la frontiera irregolare
        self.passa([t_op(vecchio, 0, 0, 0.2, rate_functions.rush_into),
                    *[Tappa(fila[i], lambda g, i=i: g.move_to(C(CX + (i % 5 - 2) * PASSO_X, 430 + (i // 5 - 0.5) * PASSO_Y)),
                            0.18, 0.5, rate_functions.ease_in_out_sine) for i in range(10)],
                    Tappa(fila, lambda g: porta(g, FILA_ALTA[2] / FILA_SU[2], C(FILA_ALTA[0], FILA_ALTA[1])), 0.5, 0.72),
                    t_op(fila, 0.5, 0.5, 0.72),
                    Tappa(bordo, lambda g: op(g, 1), 0.66, 1.0, rate_functions.ease_in_out_sine, traccia=True)], 1.9)

        # beat 1 — dentro il bordo entrano le diciotto tessere (compiti, non persone) e arriva la fonte nuova
        self.beat(1)
        ordine = sorted(range(len(celle)), key=lambda k: (k % nc) + (k // nc) * 0.4)
        self.passa([*[Tappa(celle[k], lambda g: op(g, 1), 0.03 * j, 0.03 * j + 0.22, rate_functions.ease_out_sine)
                      for j, k in enumerate(ordine)],
                    t_op(fonte, 1, 0.78, 1.0)], 1.6)
        self.attendi_fino(self.inizi_frasi[1] + 2.9)
        self.passa([t_op(dentro_et, 1, 0, 1.0)], 0.6)

        # beat 2 — le diciotto si accendono e il numero sale a «+32%»: l'etichetta entra insieme, non a salita finita
        self.beat(2)
        self.play(Tappe(self.mondo, [*[t_tinta(celle[k], col.accento, 1, 0.04 * j, 0.04 * j + 0.3)
                                       for j, k in enumerate(ordine)],
                                     t_op(mis_q1, 1, 0.2, 0.6), t_op(mis_q2, 1, 0.2, 0.6), t_op(u32, 1, 0.45, 0.8)]),
                  cnt.animate.set_opacity(1), run_time=self.arrotonda(1.1))
        self.play(cnt.sale(32), run_time=self.arrotonda(1.5))
        cnt.ferma()

        # beat 3 — il «+32%» esce, fuori dal bordo si accende una sola tessera e sopra pulsa un «?»
        self.beat(3)
        # il numero e la sua etichetta escono insieme: nessun numero grande resta a schermo senza cosa misura
        self.play(Tappe(self.mondo, [t_op(u32, 0), t_op(mis_q1, 0), t_op(mis_q2, 0)]),
                  cnt.animate.set_opacity(0), run_time=self.arrotonda(0.4))
        self.passa([t_op(celle, 0.3, 0, 0.45), t_op(sola, 1, 0.4, 0.78), t_op(fuori_et, 1, 0.62, 1.0)], 1.0)
        self.passa([t_op(qm, 1, 0, 0.45),
                    Tappa(qm, lambda g: porta(g, 1.2, C(FUORI_C[0], FUORI_QM_CY)), 0.5, 1.0, there_and_back)], 1.3)

        # beat 4 — GRANDE (punch): «PEGGIO» a tutto schermo, e al ritorno il numero con la sua etichetta
        self.beat(4)
        op(qm, 0)
        op(n19, 1)
        op(u19, 1)
        op(mis_p, 1)
        self.punch("Peggio")
        self.passa([t_tinta(sola, col.accento, 1, 0, 1.0)], 0.7)
        self.attendi_fino(self.inizi_frasi[4] + 2.1)
        self.passa([Tappa(VGroup(n19, u19), lambda g: porta(g, 1.06, g.get_center()), 0, 1.0, there_and_back)], 0.8)


# --- scena 6 ------------------------------------------------------------------------------------------------------------

class Scena06(Mondo):
    """Il resoconto del mese spezzato in quattro: cosa dai all'IA, cosa ti tieni, cosa ricontrolli.

    GRANDE (contrasto di scala): la tessera entra piccola dove stavano le diciotto della scena 5 e cresce fino a
    riempire l'area (da 58 px a 890 px di larghezza) prima di spezzarsi. «esempio nostro» resta a schermo per tutta
    la scena: i quattro pezzi sono un esempio del canale, non un risultato.
    """

    def pezzo(self, nome_icona: str, parole: str, x: float, cy: float, h: float, col):
        """Un pezzo del resoconto: riquadro, icona a sinistra, due parole accanto (tutto centrato in verticale)."""
        w = PEZZO_W
        box = rett(x - w / 2, cy - h / 2, x + w / 2, cy + h / 2, col.secondario, raggio=24)
        ic = metti(Icona(nome_icona, altezza_px=60, colore=col.secondario), x - w / 2 + 50, cy)
        t = testo(parole, "token", colore=col.testo)
        t.move_to([X(x - w / 2 + 100) + t.width / 2, C(0, cy)[1], 0])
        return VGroup(box, ic, t)

    def costruisci(self):
        col = self.cfg.palette
        bx, by, brx, bry = BLOB
        nc, nr, px_, py_, tw, th = GRIGLIA18

        # --- quello con cui finisce la scena 5 (il fotogramma 0 di questa)
        fila = fila_icone(col.attenuato, FILA_ALTA[2], FILA_ALTA[0], FILA_ALTA[1])
        for i in ACCESE:
            fila[i].set_stroke(col.accento)
        bordo = bordo_frastagliato(bx, by, brx, bry, col.secondario)
        dentro_et = etichetta(metti(testo(DENTRO, "piede", colore=col.secondario, allinea="center"), bx, DENTRO_CY))
        celle = VGroup()
        for r in range(nr):
            for c in range(nc):
                celle.add(tessera("file-text", bx + (c - (nc - 1) / 2) * px_, by + (r - (nr - 1) / 2) * py_,
                                  tw, th, col.accento, 26))
        sola = tessera("file-text", FUORI_C[0], FUORI_C[1], FUORI_C[2], FUORI_C[3], col.accento, 48)
        fuori_et = etichetta(metti(testo(FUORI, "piede", colore=col.attenuato, allinea="center"), FUORI_C[0], FUORI_CY))
        n19, u19, _ = coppia_numero("19", "punti in meno", NUM5_PX, NUM5_CY, col.accento, col.testo)
        mis_p = etichetta(metti(testo(MISURA_PUNTI, "piede", colore=col.attenuato, allinea="center"),
                                CX, FONTE_CY - PASSO_RIGA))
        fon_h = etichetta(metti(testo(FONTE_HARVARD, "piede", colore=col.attenuato, allinea="center"), CX, FONTE_CY))
        vecchio = VGroup(bordo, dentro_et, celle, sola, fuori_et, n19, u19, mis_p, fon_h)

        # --- la tessera «resoconto del mese» e i suoi quattro pezzi
        x0, y0, x1, y1 = GRANDE6
        box = rett(x0, y0, x1, y1, col.secondario, raggio=28)
        box.set_points(sagoma_rett(bx - tw / 2, by - th / 2, bx + tw / 2, by + th / 2, 16).get_points())
        titolo = etichetta(metti(testo(TESSERA_RESOCONTO, "etichetta", colore=col.secondario, peso=BOLD,
                                       allinea="center"), (x0 + x1) / 2, y0 + 62))
        quad = [(COL_SX, 485), (COL_DX, 485), (COL_SX, 775), (COL_DX, 775)]
        nomi = [PEZZI_6[0], PEZZI_6[2], PEZZI_6[3], PEZZI_6[1]]     # numeri | ordine / conclusione | bozza
        pezzi = VGroup(*[self.pezzo(n, w, qx, qy, 250, col) for (n, w), (qx, qy) in zip(nomi, quad)])
        numeri, ordine, conclusione, bozza = pezzi
        nostro = etichetta(metti(testo(NOSTRO, "piede", colore=col.attenuato, allinea="center"), CX, 1000))

        bot = metti(Icona("bot", altezza_px=110, colore=col.secondario), COL_DX, 410)
        utente = metti(Icona("user", altezza_px=110, colore=col.terziario), COL_SX, 410)
        pillola = etichetta(metti(Etichetta(piano(self.scena["testo"][0])), CX, 280))
        lente = Circle(radius=px(86), stroke_color=col.accento, stroke_width=tratto(6))
        manico = Line(ORIGIN, ORIGIN + np.array([px(56), -px(56), 0]), stroke_color=col.accento, stroke_width=tratto(6))
        manico.shift(lente.point_at_angle(-math.pi / 4))
        occhiali = VGroup(lente, manico)
        metti(occhiali, COL_SX + 120, SLOT_SX[2])

        garanzia = etichetta(metti(testo(GARANZIA, "piede", colore=col.attenuato, allinea="center"), CX, 408))
        promessa = metti(grande(PROMESSA, 50, col.accento), CX, 850)

        mondo = VGroup(vecchio, fila, box, titolo, pezzi, nostro, bot, utente, pillola, occhiali, garanzia, promessa)
        self.apri(mondo)
        for m in (box, titolo, pezzi, nostro, bot, utente, pillola, occhiali, garanzia, promessa):
            op(m, 0)
        op(fila, 0.5)

        # beat 0 — GRANDE (contrasto di scala): esce la frontiera, entra una tessera piccola e cresce fino all'area
        self.passa([t_op(vecchio, 0, 0, 0.3, rate_functions.rush_into),
                    t_op(fila, 0, 0.1, 0.4),
                    t_op(box, 1, 0.42, 0.55),
                    t_box(box, x0, y0, x1, y1, 28, 0.45, 1.0, rate_functions.ease_out_cubic),
                    t_op(titolo, 1, 0.82, 1.0)], 2.1)
        self.verifica("tessera cresciuta")
        self.attendi_fino(2.2)
        # i quattro riquadri (con la loro icona) partono impilati al centro della tessera e si aprono a ventaglio;
        # le due parole di ogni pezzo compaiono solo quando il pezzo è arrivato, così due testi non si attraversano mai
        gusci = [VGroup(pz[0], pz[1]) for pz in pezzi]
        parole = [pz[2] for pz in pezzi]
        for k in range(4):
            gusci[k].shift(C((x0 + x1) / 2, (y0 + y1) / 2) - C(*quad[k]))
        self.passa([t_op(titolo, 0, 0, 0.18),
                    t_op(box, 0, 0.2, 0.34),
                    *[t_op(gusci[k], 1, 0.3, 0.46) for k in range(4)],
                    *[Tappa(gusci[k], lambda g, k=k: g.shift(C(*quad[k]) - C((x0 + x1) / 2, (y0 + y1) / 2)),
                            0.34, 0.82, rate_functions.ease_out_back) for k in range(4)],
                    *[t_op(parole[k], 1, 0.84, 1.0) for k in range(4)],
                    t_op(nostro, 1, 0.84, 1.0)], 1.4)

        # beat 1 — entra il «bot» e i pezzi si compattano: la bozza e l'ordine si posano sotto di lui
        self.beat(1)
        dest1 = {0: (COL_SX, SLOT_SX[0]), 1: (COL_DX, SLOT_DX[0]), 2: (COL_SX, SLOT_SX[1]), 3: (COL_DX, SLOT_DX[1])}
        self.passa([t_op(bot, 1, 0, 0.3),
                    *[Tappa(pezzi[k], self.stringi(pezzi[k], dest1[k], 120), 0.25, 0.8,
                            rate_functions.ease_in_out_sine) for k in range(4)],
                    t_op(pillola, 1, 0.8, 1.0)], 1.4)

        # beat 2 — entra l'utente, la bozza torna a sinistra (scende e poi va, senza passare sopra gli altri) e la lente
        self.beat(2)
        self.passa([t_op(utente, 1, 0, 0.45)], 0.8)
        self.attendi_fino(self.inizi_frasi[2] + 1.05)
        self.passa([Tappa(bozza, lambda g: g.shift(C(COL_DX, SLOT_SX[2]) - C(COL_DX, SLOT_DX[1])), 0.0, 0.45,
                          rate_functions.ease_in_out_sine),
                    Tappa(bozza, lambda g: g.shift(C(COL_SX, SLOT_SX[2]) - C(COL_DX, SLOT_SX[2])), 0.5, 1.0,
                          rate_functions.ease_in_out_sine)], 1.2)
        self.attendi_fino(self.inizi_frasi[2] + 2.45)
        self.passa([t_op(occhiali, 1, 0, 0.2),
                    Tappa(occhiali, lambda g: g.shift(C(COL_SX + 120, SLOT_SX[0]) - C(COL_SX + 120, SLOT_SX[2])),
                          0.25, 0.75, rate_functions.ease_in_out_sine),
                    t_tinta(numeri[2], col.accento, 1, 0.72, 1.0),
                    t_tinta(numeri[0], col.accento, 1, 0.72, 1.0),
                    t_tinta(numeri[1], col.accento, 1, 0.72, 1.0)], 1.2)

        # beat 3 — i quattro pezzi si attenuano e tornano in alto, piccole, le dieci icone con le sei accese
        self.beat(3)
        dest3 = {0: (COL_SX, 500), 1: (COL_DX, 500), 2: (COL_SX, 610), 3: (COL_SX, 720)}
        self.passa([t_op(occhiali, 0, 0, 0.2), t_op(bot, 0, 0, 0.2), t_op(utente, 0, 0, 0.2), t_op(pillola, 0, 0, 0.2),
                    *[Tappa(pezzi[k], self.stringi(pezzi[k], dest3[k], 90), 0.22, 0.7,
                            rate_functions.ease_in_out_sine) for k in range(4)],
                    t_op(pezzi, 0.34, 0.5, 0.8),
                    Tappa(nostro, lambda g: g.shift(C(CX, 945) - C(CX, 1000)), 0.5, 0.8)], 1.4)
        self.attendi_fino(self.inizi_frasi[3] + 1.6)
        self.passa([t_op(fila, 1, 0, 0.5), t_op(garanzia, 1, 0.5, 1.0)], 1.1)
        self.attendi_fino(self.inizi_frasi[3] + 3.1)
        self.passa([Tappa(promessa, lambda g: op(g, 1), 0, 1.0, rate_functions.ease_out_back)], 0.9)

    @staticmethod
    def stringi(pezzo, centro, h: float):
        """Una `fn` per `Tappa` che porta un pezzo (riquadro + icona + parole) all'altezza h e al centro dato: il
        riquadro si ridisegna, icona e parole traslano (i corpi del testo non cambiano mai). Le foglie arrivano in
        un gruppo piatto, quindi le parti si ritrovano contando le foglie di ciascuna."""
        nb, ni = len(foglie(pezzo[0])), len(foglie(pezzo[1]))
        x, y = centro
        punti = sagoma_rett(x - PEZZO_W / 2, y - h / 2, x + PEZZO_W / 2, y + h / 2, min(24, h / 4)).get_points()
        c_ic = np.array([X(x - PEZZO_W / 2 + 50), C(0, y)[1], 0.0])
        c_t = np.array([X(x - PEZZO_W / 2 + 100) + pezzo[2].width / 2, C(0, y)[1], 0.0])

        def fn(g):
            g[0].set_points(punti)
            VGroup(*g[nb:nb + ni]).move_to(c_ic)
            VGroup(*g[nb + ni:]).move_to(c_t)
        return fn


# --- scena 7 ------------------------------------------------------------------------------------------------------------

class Scena07(Mondo):
    """Chiusura: i sei restano esposti, poi «SUBIRLA» lascia il posto a «SAPERLA USARE» (tipografia cinetica).

    Le dieci icone tornano nella posizione e nella scala della scena 2 e restano dietro, attenuate, fino al
    messaggio (condizione ⚠️B). «SUBIRLA» esce del tutto prima che entri «SAPERLA USARE», nella stessa posizione.
    Il «6 su 10» torna con la sua etichetta («esposti · economie avanzate · Fondo Monetario, 2024»): nessun numero
    grande a schermo senza cosa misura e da dove viene.
    """

    def costruisci(self):
        col = self.cfg.palette
        # --- quello con cui finisce la scena 6
        fila = fila_icone(col.attenuato, FILA_ALTA[2], FILA_ALTA[0], FILA_ALTA[1])
        for i in ACCESE:
            fila[i].set_stroke(col.accento)
        garanzia = etichetta(metti(testo(GARANZIA, "piede", colore=col.attenuato, allinea="center"), CX, 408))
        promessa = metti(grande(PROMESSA, 50, col.accento), CX, 850)
        nostro = etichetta(metti(testo(NOSTRO, "piede", colore=col.attenuato, allinea="center"), CX, 945))
        pezzi = VGroup()
        for (nome, parole), (qx, qy) in zip([PEZZI_6[0], PEZZI_6[2], PEZZI_6[3], PEZZI_6[1]],
                                            [(COL_SX, 500), (COL_DX, 500), (COL_SX, 610), (COL_SX, 720)]):
            box = rett(qx - PEZZO_W / 2, qy - 45, qx + PEZZO_W / 2, qy + 45, col.secondario, raggio=22)
            ic = metti(Icona(nome, altezza_px=60, colore=col.secondario), qx - PEZZO_W / 2 + 50, qy)
            t = testo(parole, "token", colore=col.testo)
            t.move_to([X(qx - PEZZO_W / 2 + 100) + t.width / 2, C(0, qy)[1], 0])
            pezzi.add(VGroup(box, ic, t))
        vecchio = VGroup(pezzi, garanzia, promessa, nostro)

        num = metti(grande("6 su 10", PICCOLO_PX, col.accento, mono=True), CX, 986)
        misura = etichetta(metti(testo(MISURA_FMI, "piede", colore=col.attenuato, allinea="center"),
                                 CX, FONTE_CY - PASSO_RIGA))
        fonte = etichetta(metti(testo(FONTE_FMI, "piede", colore=col.attenuato, allinea="center"), CX, FONTE_CY))

        subirla = metti(grande(SUBIRLA, 172, col.testo), CX, 700)
        msg = self.scena["messaggio"]
        saperla = metti(grande(SAPERLA, 165, col.accento), CX, 700)
        coda = metti(testo(msg.split("==")[-1].strip(), "messaggio", colore=col.testo, peso=BOLD, allinea="center"),
                     CX, 985)
        cta = etichetta(metti(Etichetta(spezza(self.scena["cta"], 5)), CX, 1120))

        mondo = VGroup(vecchio, fila, num, misura, fonte, subirla, saperla, coda, cta)
        self.apri(mondo)
        for m in (num, misura, fonte, subirla, saperla, coda, cta):
            op(m, 0)
        op(VGroup(*pezzi), 0.34)
        porta(subirla, 0.72, C(CX, 700))      # arrivano da più piccoli: la crescita è il cambio grande
        porta(saperla, 0.86, C(CX, 700))

        # beat 0 — esce tutto, le dieci icone tornano al centro come nella scena 2 e sotto torna piccolo «6 su 10»
        self.passa([t_op(vecchio, 0, 0, 0.26, rate_functions.rush_into),
                    Tappa(fila, lambda g: porta(g, FILA_CASA[2] / FILA_ALTA[2], C(FILA_CASA[0], FILA_CASA[1])),
                          0.24, 0.85, rate_functions.ease_in_out_sine)], 1.4)
        self.attendi_fino(1.75)
        self.passa([t_op(num, 1, 0, 0.55), t_op(misura, 1, 0.5, 0.85), t_op(fonte, 1, 0.6, 1.0)], 0.9)

        # beat 1 — GRANDE (tipografia cinetica): «SUBIRLA» arriva enorme sopra la fila, esce del tutto, e al suo
        # posto entra «SAPERLA USARE» con la coda del messaggio e la CTA
        self.beat(1)
        self.attendi_fino(self.inizi_frasi[1] + 0.36)
        self.passa([t_op(num, 0, 0, 0.3, rate_functions.rush_into),
                    t_op(misura, 0, 0, 0.3), t_op(fonte, 0, 0, 0.3),
                    t_op(fila, 0.22, 0.15, 0.6),
                    Tappa(subirla, lambda g: op(g, 1), 0.35, 0.65),
                    Tappa(subirla, lambda g: porta(g, 1 / 0.72, C(CX, 700)), 0.35, 1.0,
                          rate_functions.ease_out_back)], 0.5)
        self.verifica("«SUBIRLA» a schermo")
        self.attendi_fino(self.inizi_frasi[1] + 1.86)
        self.passa([t_op(subirla, 0, 0, 1.0, rate_functions.rush_into)], 0.28)
        self.passa([Tappa(saperla, lambda g: (op(g, 1), porta(g, 1 / 0.86, C(CX, 700))), 0, 0.72,
                          rate_functions.ease_out_back),
                    t_op(coda, 1, 0.6, 0.85),
                    t_op(cta, 1, 0.78, 1.0)], 0.66)
