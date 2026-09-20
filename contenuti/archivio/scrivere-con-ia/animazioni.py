"""Animazioni di «All'IA chiedi i problemi, non le parole» (contenuti/sceneggiature/2026-09-19-scrivere-con-ia.md).

Le scene 1 e 3 sono a filmato: non hanno una classe. Le scene 2 e 4 arrivano da uno stacco netto su un filmato, quindi
il loro fotogramma 0 è già pieno. Il filo visivo sono tre oggetti sempre allo stesso posto: la carta «richiesta» in
alto (A, B, C alla lettera), la carta «bozza» e il contatore a cavallo del bordo alto della bozza («tornate uguali»,
nella 7 «scritte da lei»). I testi attribuiti al modello (A8, A9, A10, B9, C2) sono alla lettera.

Regola del presentatore (2026-09-20): niente testo denso che resta a schermo. La mail di Giulia si legge intera solo
nel primo secondo della scena 2; poi ogni riga diventa una sagoma (`sagome()`: una barretta larga come la riga vera,
spezzata dove una parola dovrà accendersi) e la carta si compatta. Da lì la carta è una mappa: dice *dove*. Le parole
di cui parla la voce stanno nella «lente», la fascia libera sotto la carta, molto più grandi (44-58 px). Un testo
torna al suo posto nella riga solo quando il resto è spento (lo zoom della scena 6) o nella mail finale (tre
frammenti). `parole_a_schermo()` conta le parole leggibili alla fine di ogni passaggio (REEL_CONTA_PAROLE=file).

Come è fatto il file. Tutto quello che una scena mostra è costruito all'inizio dentro un solo gruppo (`mondo`), già al
suo posto; ciò che non si vede ancora ha opacità zero. Ogni passaggio è una sola animazione `Tappe` sul mondo: una
lista di modifiche, ognuna con la sua finestra (a, b) del tempo del passaggio. Così nessun oggetto entra o esce dalla
lista della scena (niente riordini, niente riquadri che coprono i testi fermi) e le finestre di chi esce e di chi
entra non si accavallano: prima esce il testo vecchio, poi si muovono i riquadri, poi entra il testo nuovo.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from manim import (BOLD, DOWN, LEFT, ORIGIN, RIGHT, UP, Animation, Line, Mobject, Rectangle, RoundedRectangle, VGroup,
                   linear, rate_functions, rush_from, rush_into, smooth, there_and_back)

from manim.utils.family import extract_mobject_family_members

from tools.anim.base import ScenaReel
from tools.anim.componenti import Barrato, Etichetta, Freccia, Riga, Titolo, piano, testo, tratto
from tools.anim.misure import px

# --- i testi (alla lettera dalle Note di produzione) -----------------------------------------------------------------

BOZZA = [
    "Buongiorno signora Carla, in realtà volevo\nscriverle già ieri.",
    "Purtroppo sono stati riscontrati dei problemi\nmolto seri dal nostro fornitore nella fase di\nverniciatura, e quindi "
    "dobbiamo procedere\na una riprogrammazione della consegna,\nche sostanzialmente slitta davvero di poco.",
    "So che le sedie le aspettava per\nl'inaugurazione di sabato 3 ottobre,\ne mi dispiace il doppio.",
    "Le venti sedie arriveranno venerdì 16 ottobre.",
    "Se vuole, per sabato gliene porto io dodici\ndelle nostre, in prestito.",
    "Un saluto, Giulia",
]
# dove una riga della bozza si spezza: le parole che in qualche scena si accendono da sole (scene 4 e 6, mail finale)
FUOCHI = [
    ["in realtà"],
    ["Purtroppo", "sono stati riscontrati", "molto", "seri", "procedere", "a una riprogrammazione della consegna",
     "sostanzialmente", "slitta", "davvero", "di poco"],
    ["mi dispiace il doppio"],
    [],
    ["gliene porto io dodici", "delle nostre"],
    [],
]
RIEMPITIVI = ["in realtà", "Purtroppo", "sostanzialmente", "davvero", "molto seri"]      # come li elenca C2, scritti come nella bozza
FINALE_DATA = "venerdì 16 ottobre"
FINALE = [   # la mail riscritta da noi: le prime tre frasi sono nuove, poi le frasi 3 e 5 della bozza e i saluti
    "Buongiorno signora Carla,\nle venti sedie arriveranno venerdì 16 ottobre,\ncon quasi due settimane di ritardo.",
    "Il nostro fornitore ha avuto problemi seri\nin verniciatura.",
    "Avrei dovuto scriverle già ieri.",
]
RICHIESTA_A = "Migliora questa mail."
RICHIESTA_B2 = "mantenendo il mio stile."          # B = «Migliora questa mail mantenendo il mio stile.»
RICHIESTA_C = "Non migliorare questa mail:\nelencami i problemi,\nsenza riscrivere niente."      # grande, mentre si scrive
RICHIESTA_C_STRETTA = "Non migliorare questa mail:\nelencami i problemi, senza riscrivere niente."  # le sue sagome, a 36 px
RICHIESTA_C_FUOCO = "elencami i problemi"
A8 = "mi dispiace sinceramente per il disagio"
A9 = "mi dispiace molto per il disagio"
A10_CODA = "davvero molto per il disagio"          # A10 = «mi dispiace davvero molto per il disagio»
B9_CODA = "ancora di più"                          # B9 = «mi dispiace ancora di più»
C2_RIEMPITIVI = "«Riempitivi e attenuatori a raffica»"
C2_QUARTA = "«arriva quarta»"
C2_COMMENTO = "«un modo di dire vago\ne un po' infantile»"
FRASE_4 = "Le venti sedie arriveranno\nvenerdì 16 ottobre."          # la frase 4 della bozza, nella lente su due righe
DIDASCALIA = "mail, azienda e persone inventate"
ETICHETTA_CONTA, ETICHETTA_CONTA_7 = "tornate uguali", "scritte da lei"
NOTA_PROVE, NOTA_MAX1 = "10 prove", "al massimo 1"
CUORE = "mi dispiace il doppio"

# --- impaginazione, in px della tela (origine in alto a sinistra) ------------------------------------------------------

SX, DX = 60, 960
RICH_ALTO, RICH_BASSO_A, RICH_BASSO_B, RICH_BASSO_CG, RICH_DX_STRETTA = 244, 323, 372, 496, 620
RICH_TESTO_X, RICH_RIGA1_Y, RICH_RIGA2_Y, RICH_RIGA2_Y_C, RICH_PASSO_CG, RICH_CORPO_CG = 90, 266, 317, 314, 72, 56
GIU_CG = 128                       # con la richiesta C grande (fine della 5, inizio della 6) bozza e contatore stanno più giù
NOTE_Y = 402                       # centro della riga delle note, fra richiesta e bozza
BOZ_ALTO, RIGA0, PASSO, ALT_RIGA = 453, 489, 48, 37
TESTO_X, CIFRA_X = 104, 68
SU_INIZIO = 110                    # scena 2: la bozza parte più in alto, la richiesta che cala la spinge giù
# la carta compatta (solo sagome): righe ogni 28 px, 8 px in più fra una frase e l'altra, barrette alte 14 px
C_RIGA0, C_PASSO, C_STACCO, C_ALT = BOZ_ALTO + 34, 28, 8, 14
BOZ_BASSO_C = C_RIGA0 + 13 * C_PASSO + 5 * C_STACCO + C_ALT + 28      # 933
# la lente: la fascia sotto la carta compatta, dove stanno in grande le parole di cui parla la voce
LENTE_X, LENTE_DX, LENTE_ALTO, LENTE_PASSO = 68, 940, 1000, 60
# la mail finale: le righe con un frammento a testo hanno più aria delle righe a sola sagoma
FIN_SLOT = (38, 52, 38, 38, 38, 38, 38, 38, 52, 52, 52, 38)
FIN_STACCO_DOPO, FIN_STACCO, FIN_RIGA0 = (2, 4, 5, 8, 10), 6, BOZ_ALTO + 32
K_NEUTRO, K_ACCESO, K_SPENTO = 0.42, 0.9, 0.15       # opacità di una sagoma: com'è di solito, accesa, spenta


def X(v: float) -> float:
    return (v - 540) / 120


def Y(v: float) -> float:
    return (960 - v) / 120


def riga_y(r: float) -> float:
    return RIGA0 + r * PASSO


def basso_carta(n_righe: int) -> float:
    return riga_y(n_righe - 1) + ALT_RIGA + 22


def c_centro(r: int, frase: int) -> float:
    """Il centro (px) della sagoma della riga r (0-13) nella carta compatta; `frase` è l'indice della sua frase."""
    return C_RIGA0 + r * C_PASSO + frase * C_STACCO + C_ALT / 2


def fin_slot(i: int) -> tuple[float, float]:
    """Cima e fondo (px) della riga i della mail finale."""
    y = FIN_RIGA0 + sum(FIN_SLOT[:i]) + FIN_STACCO * sum(1 for k in FIN_STACCO_DOPO if k < i)
    return y, y + FIN_SLOT[i]


def fin_centro(i: int) -> float:
    return sum(fin_slot(i)) / 2


BOZ_BASSO_FIN = fin_slot(11)[1] + 18                                   # 1045


def posa(blocco, x: float, y: float, passo: float = PASSO, da: str = "sx"):
    """Mette le righe di un blocco sulla griglia: la riga k ha la cima del puntello a y + k * passo e parte da x
    (`da="dx"`: finisce a x). La cima è quella del puntello «Hg», non degli accenti: le righe restano equidistanti."""
    for k, r in enumerate(blocco.righe):
        p = r.puntello if r.allineata else r
        dx = X(x) - (r.glifi.get_left()[0] if da == "sx" else r.glifi.get_right()[0])
        r.shift([dx, Y(y + k * passo) - p.get_top()[1], 0])
    return blocco


def scatola(x0, y0, x1, y1, colore, raggio: float = 24, spessore: float = 3) -> RoundedRectangle:
    r = RoundedRectangle(corner_radius=px(raggio), width=px(x1 - x0), height=px(y1 - y0), stroke_color=colore,
                         stroke_width=tratto(spessore), fill_opacity=0)
    return r.move_to([X((x0 + x1) / 2), Y((y0 + y1) / 2), 0])


def parole_di(blocco) -> list[VGroup]:
    """I glifi di ogni parola, in ordine di lettura (descrittori di pezzi: non entrano mai nella scena)."""
    out = []
    for r in blocco.righe:
        k = 0
        for w in r.piano.split():
            out.append(VGroup(*r.glifi.submobjects[k:k + len(w)]))
            k += len(w)
    return out


def sottolinea(glifi, riga, colore, spessore: float = 4) -> Line:
    y = riga.puntello.get_bottom()[1] - px(1)
    return Line([glifi.get_left()[0], y, 0], [glifi.get_right()[0], y, 0], stroke_color=colore, stroke_width=tratto(spessore))


class Linguetta(VGroup):
    """Il nome di una carta, a cavallo del suo bordo: un fondo color sfondo interrompe la linea dietro il testo."""

    def __init__(self, s: str, colore, sfondo, x: float, y: float, **kw):
        super().__init__(**kw)
        self.testo = testo(s, "piede", colore=colore)
        self.fondo = Rectangle(width=self.testo.width + px(24), height=px(ALT_RIGA), stroke_width=0, fill_color=sfondo, fill_opacity=1)
        self.add(self.fondo, self.testo.move_to(self.fondo))
        self.move_to([X(x) + self.width / 2, Y(y), 0])
        etichetta(self)


def etichetta(m: Mobject) -> Mobject:
    """Segna i testi di m come titoli o etichette brevi: `parole_a_schermo` li conta a parte."""
    for x in m.get_family():
        if isinstance(x, Riga):
            x._etichetta = True
    return m


# --- le sagome: un testo che smette di chiedere di essere letto -------------------------------------------------------

_OCCHIO: dict[str, tuple[float, float]] = {}
_SENZA_SPAZI = re.compile(r"\s")


def occhio(ruolo: str) -> tuple[float, float]:
    """L'occhio del carattere di un ruolo: distanza dalla cima del puntello «Hg» alla cima della «x», e altezza della
    «x» (unità). Si misura alla prima chiamata, mai al livello del modulo (il font non è ancora registrato)."""
    if ruolo not in _OCCHIO:
        r = testo("x", ruolo).righe[0]
        _OCCHIO[ruolo] = (float(r.puntello.get_top()[1] - r.glifi.get_top()[1]), float(r.glifi.height))
    return _OCCHIO[ruolo]


def centro_occhio(riga, ruolo: str) -> float:
    dy, h = occhio(ruolo)
    return float(riga.puntello.get_top()[1]) - dy - h / 2


def posa_occhio(riga, ruolo: str, x: float | None, y: float) -> None:
    """Mette una riga con il centro dell'occhio a y px (e, se x non è None, l'inizio dei glifi a x px)."""
    dx = 0.0 if x is None else X(x) - float(riga.glifi.get_left()[0])
    riga.shift([dx, Y(y) - centro_occhio(riga, ruolo), 0])


@dataclass
class RigaSagoma:
    """La sagoma di una riga: le barrette (una, o più se la riga ha dei fuochi) e per ogni fuoco la sua barretta."""
    barre: VGroup
    riga: object
    di: dict = field(default_factory=dict)


def sagome(blocco, colore, fuochi=(), ruolo: str = "piede", minimo_px: float = 16, raggio_px: float = 6) -> list[RigaSagoma]:
    """Le righe-sagoma di un testo vero già impaginato: per ogni riga una barretta piena con gli angoli arrotondati,
    alta quanto l'occhio del carattere e larga quanto la riga (si misura sui glifi, non si stima). Dove la riga
    contiene uno dei `fuochi` (parole che più avanti si accendono da sole) la barretta si spezza lì, con lo spazio fra
    le parole a fare da stacco; un pezzo più stretto di `minimo_px` (una virgola, un punto) si unisce al vicino.
    Le barrette nascono piene (opacità 1): lo stato si dà con `tinta(barre, colore, K_NEUTRO…)`.
    Candidata per la libreria (`tools/anim/componenti.py`), con `occhio()`."""
    _, h = occhio(ruolo)
    out = []
    for riga in blocco.righe:
        gl = riga.glifi.submobjects
        tagli, trovati = {0, len(gl)}, []
        for w in fuochi if riga.allineata else ():
            i = riga.piano.lower().find(w.lower())
            if i >= 0:
                fine = i + len(w)
                while fine < len(riga.piano) and not riga.piano[fine].isspace():   # la virgola o il punto restano col fuoco
                    fine += 1
                a = len(_SENZA_SPAZI.sub("", riga.piano[:i]))
                tagli |= {a, a + len(_SENZA_SPAZI.sub("", riga.piano[i:fine]))}
                trovati.append((w, a))
        lim = sorted(tagli)
        tratti = [[a, b] for a, b in zip(lim, lim[1:])]
        k = 0
        while len(tratti) > 1 and k < len(tratti):
            a, b = tratti[k]
            if gl[b - 1].get_right()[0] - gl[a].get_left()[0] < px(minimo_px):
                if k > 0:
                    tratti[k - 1][1] = b
                else:
                    tratti[1][0] = a
                tratti.pop(k)
            else:
                k += 1
        cy = centro_occhio(riga, ruolo) if riga.allineata else float(riga.get_center()[1])
        barre = VGroup()
        for a, b in tratti:
            x0, x1 = float(gl[a].get_left()[0]), float(gl[b - 1].get_right()[0])
            barra = RoundedRectangle(corner_radius=min(px(raggio_px), h / 2.2), width=max(x1 - x0, px(10)), height=h, stroke_width=0,
                                     fill_color=colore, fill_opacity=1).move_to([(x0 + x1) / 2, cy, 0])
            barra._tratto = (a, b)
            barre.add(barra)
        di = {w: next(x for x in barre if x._tratto[0] <= a < x._tratto[1]) for w, a in trovati}
        out.append(RigaSagoma(barre, riga, di))
    return out


def sotto_le_barre(barre: list, colore, spessore: float = 3, stacco_px: float = 5) -> Line:
    """Una sottolineatura sotto una o più barrette vicine della stessa riga."""
    y = min(float(x.get_bottom()[1]) for x in barre) - px(stacco_px)
    return Line([min(float(x.get_left()[0]) for x in barre), y, 0], [max(float(x.get_right()[0]) for x in barre), y, 0],
                stroke_color=colore, stroke_width=tratto(spessore))


def parole_a_schermo(scena) -> tuple[int, int, list[str]]:
    """Quante parole si leggono adesso: (contenuto, etichette, testi). Una parola conta se almeno un suo glifo ha
    opacità > 0,3; i testi segnati con `etichetta()` (titoli, pillole, note, contatore, didascalie) si contano a parte.
    Regola del presentatore: a fine beat, oltre una ventina di parole di contenuto è troppo."""
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


# --- opacità e tinte che non toccano i puntelli -------------------------------------------------------------------------

def foglie(m: Mobject) -> list:
    return m.family_members_with_points()


def segna(m: Mobject) -> Mobject:
    """Ricorda l'opacità piena di ogni foglia (i puntelli delle righe hanno 0 e restano invisibili qualunque cosa succeda)."""
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


def attenua(g: Mobject, k: float) -> None:
    """Moltiplica l'opacità che c'è adesso (una frase spenta resta più spenta di una accesa)."""
    for f in foglie(g):
        f.set_fill(opacity=f.get_fill_opacity() * k, family=False)
        f.set_stroke(opacity=f.get_stroke_opacity() * k, family=False)


# --- l'animazione a tappe ------------------------------------------------------------------------------------------------

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

    def __init__(self, radice: Mobject, tappe: list[Tappa], **kw):
        self.tappe = [t for t in tappe if t is not None]
        super().__init__(radice, rate_func=linear, **kw)

    def create_starting_mobject(self) -> Mobject:
        return Mobject()                       # la copia di partenza non serve: ogni tappa ha le sue

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
            # una tappa tocca solo ciò che cambia (punti, colori): così uno spostamento e una tinta sullo stesso
            # pezzo possono stare nella stessa finestra senza pestarsi
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
                        continue                       # non ancora partita: il pezzo resta spento
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


def t_entra(pezzo, a=0.0, b=1.0, sposta=None, scala: float = 1.0, rate=smooth, k: float = 1.0) -> Tappa:
    """Il pezzo (nascosto) parte spostato di -sposta e scalato, e arriva al suo posto acceso."""
    v = np.array(ORIGIN if sposta is None else sposta, dtype=float)
    g0 = VGroup(*foglie(pezzo))
    g0.scale(scala).shift(-v)

    def fn(g):
        g.shift(v).scale(1 / scala)
        op(g, k)
    return Tappa(pezzo, fn, a, b, rate)


def t_esce(pezzo, a=0.0, b=1.0, sposta=None, rate=smooth) -> Tappa:
    v = np.array(ORIGIN if sposta is None else sposta, dtype=float)

    def fn(g):
        g.shift(v)
        op(g, 0)
    return Tappa(pezzo, fn, a, b, rate)


def t_punti(pezzo, copia, a=0.0, b=1.0, rate=smooth, stile: bool = False) -> Tappa:
    """Il pezzo prende i punti (e, con stile, colori e opacità) di una copia fatta prima: forme e ritorni a casa."""
    sorg = foglie(copia)

    def fn(g):
        for m, s in zip(g.submobjects, sorg):
            m.points = s.points.copy()
            if stile:
                m.interpolate_color(s, s, 1)
    return Tappa(pezzo, fn, a, b, rate)


def t_traccia(pezzo, a=0.0, b=1.0, rate=smooth) -> Tappa:
    return Tappa(pezzo, lambda g: op(g, 1), a, b, rate, traccia=True)


def t_fn(pezzo, fn, a=0.0, b=1.0, rate=smooth) -> Tappa:
    return Tappa(pezzo, fn, a, b, rate)


def rimbalzo_corto(t: float, s: float = 1.0) -> float:
    """`ease_out_back` con un rientro più corto (~6 % invece del 10 %): una carta larga 900 px che rimbalza con la
    curva della libreria supererebbe il bordo dell'area contenuto di quasi 40 px."""
    t -= 1.0
    return t * t * ((s + 1.0) * t + s) + 1.0


def applica(*tappe: Tappa) -> None:
    """Le stesse modifiche, subito e senza animazione: è così che una scena parte dall'ultimo fotogramma di un'altra."""
    for t in tappe:
        if t is not None:
            t.fn(VGroup(*foglie(t.pezzo)))


# --- i tre oggetti ------------------------------------------------------------------------------------------------------

class Richiesta(VGroup):
    """La carta «richiesta»: stretta con la riga A, una riga in più per B; la C si scrive grande su tre righe (scena 5)
    e poi si stringe alle sue sagome, con a testo solo «elencami i problemi,» (scene 6 e 7)."""

    def __init__(self, col, **kw):
        super().__init__(**kw)
        self.c_attenuato = str(col.attenuato)
        self.box = scatola(SX, RICH_ALTO, RICH_DX_STRETTA, RICH_BASSO_A, col.secondario)
        self.ling = Linguetta("richiesta", col.secondario, col.sfondo, TESTO_X, RICH_ALTO)
        self.a = posa(testo(RICHIESTA_A, "etichetta"), RICH_TESTO_X, RICH_RIGA1_Y)
        self.b2 = posa(testo(RICHIESTA_B2, "etichetta", colore=col.accento), RICH_TESTO_X, RICH_RIGA2_Y)
        self.cg = posa(testo(RICHIESTA_C, "caption").scale(RICH_CORPO_CG / 48), RICH_TESTO_X, RICH_RIGA1_Y + 4, passo=RICH_PASSO_CG)
        stretta = posa(testo(RICHIESTA_C_STRETTA, "piede"), RICH_TESTO_X, RICH_RIGA1_Y + 2, passo=RICH_RIGA2_Y_C - RICH_RIGA1_Y)
        self.sag_a = sagome(self.a, self.c_attenuato, ["Migliora"], ruolo="etichetta")[0]
        self.sag_b2 = sagome(self.b2, self.c_attenuato, ruolo="etichetta")[0]
        sag_c = sagome(stretta, self.c_attenuato, [RICHIESTA_C_FUOCO])
        fuoco_c = sag_c[1].di[RICHIESTA_C_FUOCO]
        self.barre_c = VGroup(*sag_c[0].barre, *[x for x in sag_c[1].barre if x is not fuoco_c])
        self.c_fuoco = self.cg.righe[1]                       # «elencami i problemi,»: l'unica riga che resta a testo
        self._c_x = float(stretta.righe[1].glifi.get_left()[0])
        self._c_cima = float(stretta.righe[1].puntello.get_top()[1])
        self.cornice = VGroup(self.box, self.ling)
        self.add(self.box, self.ling, *self.sag_a.barre, *self.sag_b2.barre, *self.barre_c, self.a, self.b2, self.cg)
        gl = self.a.righe[0].glifi.submobjects
        self.punto_a = VGroup(gl[-1])
        self.a_senza_punto = VGroup(*gl[:-1])
        self.migliora = self.a.parola("Migliora")
        self.resto_a = VGroup(*gl[len(self.migliora):])        # «questa mail.»
        self.barre_ab = VGroup(*self.sag_a.barre, *self.sag_b2.barre)
        self.box_a = self.box.copy()
        self.box_b = scatola(SX, RICH_ALTO, RICH_DX_STRETTA, RICH_BASSO_B, col.secondario)
        self.box_cc = scatola(SX, RICH_ALTO, DX, RICH_BASSO_B, col.secondario)
        self.box_cg = scatola(SX, RICH_ALTO, DX, RICH_BASSO_CG, col.secondario)

    def stringi_fuoco(self, g) -> None:
        """«elencami i problemi,» passa da 56 a 36 px e va al suo posto nella seconda riga della carta stretta."""
        g.scale(36 / RICH_CORPO_CG)
        puntello = next(m for m in g.submobjects if isinstance(m, Line))
        g.shift([self._c_x - float(puntello.get_center()[0]), self._c_cima - float(puntello.get_top()[1]), 0])

    def t_stato(self, quale: str) -> list[Tappa]:
        """Lo stato fermo A, B, CG (la C grande) o CC (la C stretta, a sagome), per partire da lì."""
        box = {"A": self.box_a, "B": self.box_b, "CG": self.box_cg, "CC": self.box_cc}[quale]
        out = [t_punti(self.box, box), t_op(self.a, 1 if quale in ("A", "B") else 0), t_op(self.punto_a, 1 if quale == "A" else 0),
               t_op(self.b2, 1 if quale == "B" else 0), t_op(self.cg, 1 if quale == "CG" else 0),
               t_op(VGroup(self.barre_ab, self.barre_c), 0)]
        if quale == "CC":
            out += [t_fn(self.c_fuoco, self.stringi_fuoco), t_op(self.c_fuoco, 1), t_tinta(self.barre_c, self.c_attenuato, K_NEUTRO)]
        return out


def in_compatto(g, r: int, frase: int, su_px: float = 0.0) -> None:
    """Le barrette di una riga vanno al loro posto nella carta compatta e si assottigliano (l'occhio vero è ~20 px)."""
    g.stretch(px(C_ALT) / g.height, 1)
    g.shift([0, Y(c_centro(r, frase) - su_px) - g.get_center()[1], 0])


class Bozza(VGroup):
    """La carta «bozza». Il testo vero della mail (cinque frasi e i saluti, una riga ogni 48 px) si vede solo all'inizio
    della scena 2; poi ogni riga è la sua sagoma e la carta è compatta. Dentro, nascosti, i pochi testi che tornano al
    loro posto nella riga: «mi dispiace il doppio» (zoom della scena 6) e i tre frammenti della mail finale."""

    FIN_DI = {(2, 0): 6, (2, 1): 7, (2, 2): 8, (4, 0): 9, (4, 1): 10, (5, 0): 11}      # (frase, riga) → riga della mail finale

    def __init__(self, col, **kw):
        super().__init__(**kw)
        # solo stringhe: la palette del config non si può copiare (deepcopy), e i mobject si copiano a ogni passaggio
        self.c_testo, self.c_attenuato, self.c_accento = str(col.testo), str(col.attenuato), str(col.accento)
        att = self.c_attenuato
        self.box = scatola(SX, BOZ_ALTO, DX, basso_carta(14), att)
        self.box_comp = scatola(SX, BOZ_ALTO, DX, BOZ_BASSO_C, att)
        self.box_finale = scatola(SX, BOZ_ALTO, DX, BOZ_BASSO_FIN, col.terziario)
        self.ling = Linguetta("bozza", att, col.sfondo, TESTO_X, BOZ_ALTO)
        self.ling_finale = Linguetta("mail finale", col.terziario, col.sfondo, TESTO_X, BOZ_ALTO)
        self.dida = Linguetta(DIDASCALIA, att, col.sfondo, TESTO_X, basso_carta(14))
        self.dida_finale = Linguetta("riscritta da noi", att, col.sfondo, TESTO_X, BOZ_BASSO_FIN)
        self.frasi, self.prima_riga, r = [], [], 0
        for s in BOZZA:
            blocco = posa(testo(s, "piede"), TESTO_X, riga_y(r))
            self.frasi.append(blocco)
            self.prima_riga.append(r)
            r += len(blocco.righe)
        self.sag = [sagome(blocco, att, FUOCHI[k]) for k, blocco in enumerate(self.frasi)]
        self.righe = [(k, j, self.prima_riga[k] + j, rs) for k in range(6) for j, rs in enumerate(self.sag[k])]
        self.tutte_barre = VGroup(*[x for _, _, _, rs in self.righe for x in rs.barre])
        self.bande, self.bande_comp = [], []
        for k in range(5):
            n = len(self.frasi[k].righe)
            colore = col.secondario if k % 2 == 0 else col.terziario
            for lista, y0, y1 in ((self.bande, riga_y(self.prima_riga[k]) - 5, riga_y(self.prima_riga[k] + n - 1) + ALT_RIGA + 5),
                                  (self.bande_comp, c_centro(self.prima_riga[k], k) - C_ALT / 2 - 3,
                                   c_centro(self.prima_riga[k] + n - 1, k) + C_ALT / 2 + 3)):
                banda = Rectangle(width=px(DX - 12 - (TESTO_X - 8)), height=px(y1 - y0), stroke_width=0, fill_color=colore, fill_opacity=0.16)
                lista.append(banda.move_to([X((TESTO_X - 8 + DX - 12) / 2), Y((y0 + y1) / 2), 0]))
        # le cifre: nell'impaginazione vera accanto alla prima riga della frase, nella carta compatta al centro della frase
        self.cifre, self.cifre_cy = [], []
        for k in range(5):
            cifra = posa(testo(str(k + 1), "etichetta", colore=att, peso=BOLD, mono=True), CIFRA_X, riga_y(self.prima_riga[k]))
            self.cifre.append(etichetta(cifra))
            self.cifre_cy.append((c_centro(self.prima_riga[k], k) + c_centro(self.prima_riga[k] + len(self.frasi[k].righe) - 1, k)) / 2 + 3)
        # «mi dispiace il doppio» al suo posto nella carta compatta, sopra la sua barretta: si accende solo nel vuoto dello zoom
        self.f3_comp = testo(BOZZA[2], "piede", colore=col.accento)
        for j, riga in enumerate(self.f3_comp.righe):
            posa_occhio(riga, "piede", TESTO_X, c_centro(self.prima_riga[2] + j, 2))
        self.cuore36 = self.f3_comp.righe[2].parola(CUORE)
        self.cuore_seg = self.seg(2, CUORE)
        # la mail finale: tre frasi nuove (sagome nuove, a testo solo la data), poi le frasi 3 e 5 e i saluti della bozza
        self.fin, i = [testo(s, "piede") for s in FINALE], 0
        for blocco in self.fin:
            for riga in blocco.righe:
                posa_occhio(riga, "piede", TESTO_X, fin_centro(i))
                i += 1
        self.fin_sag = [rs for blocco in self.fin for rs in sagome(blocco, att, [FINALE_DATA])]
        self.fin_data = self.fin[0].righe[1].parola(FINALE_DATA + ",")
        seg_data = self.fin_sag[1].di[FINALE_DATA]
        self.fin_barre = VGroup(*[x for rs in self.fin_sag for x in rs.barre if x is not seg_data])
        self.fin_barre_data = VGroup(*[x for x in self.fin_sag[1].barre if x is not seg_data])
        self.fin_barre_altre = VGroup(*[x for n, rs in enumerate(self.fin_sag) if n != 1 for x in rs.barre])
        self.f3_fin, self.f5_fin = testo(BOZZA[2], "piede"), testo(BOZZA[4], "piede")
        for blocco, i0 in ((self.f3_fin, 6), (self.f5_fin, 9)):
            for j, riga in enumerate(blocco.righe):
                posa_occhio(riga, "piede", TESTO_X, fin_centro(i0 + j))
        self.cuore_fin = self.f3_fin.righe[2].parola(CUORE)
        self.porto_fin = VGroup(self.f5_fin.parola("gliene porto io dodici"), self.f5_fin.parola("delle nostre"))
        self.porto_seg = VGroup(self.seg(4, "gliene porto io dodici"), self.seg(4, "delle nostre"))
        self.testi_nascosti = VGroup(self.f3_comp, *self.fin, self.f3_fin, self.f5_fin)
        self.add(self.box, *self.bande, self.tutte_barre, VGroup(*[x for rs in self.fin_sag for x in rs.barre]), *self.frasi,
                 self.testi_nascosti, *self.cifre, self.ling, self.ling_finale, self.dida, self.dida_finale)

    def seg(self, k: int, w: str):
        """La barretta del fuoco w nella frase k."""
        return next(rs.di[w] for rs in self.sag[k] if w in rs.di)

    def barre(self, k: int, salvo=()) -> VGroup:
        return VGroup(*[x for rs in self.sag[k] for x in rs.barre if all(x is not s for s in salvo)])

    def t_frase(self, k: int, stato: str, a=0.0, b=1.0, salvo=(), cifra: bool = True) -> list[Tappa]:
        """Lo stato della sagoma di una frase: «neutra» (com'è di solito), «accesa» (bianca, con la cifra), «spenta»."""
        colore, kb, colore_c, kc = {"neutra": (self.c_attenuato, K_NEUTRO, self.c_attenuato, 0.8),
                                    "accesa": (self.c_testo, K_ACCESO, self.c_testo, 1.0),
                                    "spenta": (self.c_attenuato, K_SPENTO, self.c_attenuato, 0.45)}[stato]
        out = [t_tinta(self.barre(k, salvo), colore, kb, a, b)]
        if k < 5 and cifra:
            out.append(t_tinta(self.cifre[k], colore_c, kc, a, b))
        if k < 5 and stato != "accesa":
            out.append(t_op(self.bande[k], 0, a, b))
        return out

    def t_compatta(self, a=0.0, b=1.0, su_px: float = 0.0, rate=smooth) -> list[Tappa]:
        """Dall'impaginazione vera (una riga ogni 48 px) alla carta compatta. `su_px`: la carta è più in alto (scena 2)."""
        su = UP * px(su_px)
        def porta_cifra(g, y):
            puntello = next(m for m in g.submobjects if isinstance(m, Line))
            g.shift([0, Y(y - su_px) - float(puntello.get_center()[1]), 0])
        out = [t_fn(rs.barre, lambda g, r=r, k=k: in_compatto(g, r, k, su_px), a, b, rate) for k, _, r, rs in self.righe]
        out += [t_fn(cifra, lambda g, y=y: porta_cifra(g, y), a, b, rate) for cifra, y in zip(self.cifre, self.cifre_cy)]
        return out + [t_punti(self.box, self.box_comp.copy().shift(su), a, b, rate),
                      t_punti(VGroup(*self.bande), VGroup(*[x.copy().shift(su) for x in self.bande_comp]), a, b, rate),
                      t_sposta(self.dida, UP * px(basso_carta(14) - BOZ_BASSO_C), a, b, rate)]

    def t_verso_finale(self, a=0.0, b=1.0, rate=smooth) -> list[Tappa]:
        """Le sagome delle frasi 3 e 5 e dei saluti vanno al loro posto nella mail finale e riprendono l'altezza vera."""
        _, h = occhio("piede")

        def fn(g, i):
            g.stretch(h / g.height, 1)
            g.shift([0, Y(fin_centro(i)) - g.get_center()[1], 0])
        return [t_fn(rs.barre, lambda g, i=self.FIN_DI[(k, j)]: fn(g, i), a, b, rate) for k, j, _, rs in self.righe if (k, j) in self.FIN_DI]

    def t_finale(self) -> list[Tappa]:
        """Lo stato fermo della mail finale (scena 7): sagome nuove, a testo la data e le due frasi di Giulia."""
        return [t_op(VGroup(self.barre(0), self.barre(1), self.barre(3), *self.bande, *self.cifre, self.ling, self.dida), 0),
                *self.t_verso_finale(), t_punti(self.box, self.box_finale, stile=True),
                t_tinta(self.fin_barre, self.c_attenuato, K_NEUTRO), t_op(VGroup(self.fin_data, self.ling_finale, self.dida_finale), 1),
                t_op(VGroup(self.cuore_seg, self.porto_seg), 0), t_tinta(self.cuore_fin, self.c_accento), t_tinta(self.porto_fin, self.c_accento)]


class Conta(VGroup):
    """Il contatore a cavallo del bordo alto della bozza: etichetta, simbolo che cambia e « su 5»."""

    SIMBOLI = ("–", "?", "1", "2", "5")

    def __init__(self, col, **kw):
        super().__init__(**kw)
        kwv = dict(colore=col.attenuato, peso=BOLD, mono=True)
        cella = testo("0", "caption", **kwv).width
        self.coda = testo("su 5", "caption", **kwv)
        self.coda.shift([X(940) - self.coda.get_right()[0], Y(BOZ_ALTO) - self.coda.righe[0].puntello.get_center()[1], 0])
        cx = self.coda.get_left()[0] - 1.5 * cella
        self.simboli = {}
        for s in self.SIMBOLI:
            t = testo(s, "caption", **kwv)
            t.shift([cx - t.righe[0].glifi.get_center()[0], Y(BOZ_ALTO) - t.righe[0].puntello.get_center()[1], 0])
            self.simboli[s] = t
        x_et = cx - cella / 2 - px(18)

        def etich(s):
            t = testo(s, "piede", colore=col.attenuato)
            return t.shift([x_et - t.get_right()[0], Y(BOZ_ALTO) - t.righe[0].puntello.get_center()[1], 0])
        self.etich, self.etich7 = etich(ETICHETTA_CONTA), etich(ETICHETTA_CONTA_7)
        x0 = self.etich.get_left()[0] - px(14)
        self.fondo = Rectangle(width=X(952) - x0, height=px(52), stroke_width=0, fill_color=col.sfondo, fill_opacity=1)
        self.fondo.move_to([(x0 + X(952)) / 2, Y(BOZ_ALTO), 0])
        self.valore = VGroup(*self.simboli.values(), self.coda)
        # la versione grande della scommessa (scena 2), a destra della richiesta: l'etichetta sta sotto il valore
        self.etich_g = testo(ETICHETTA_CONTA, "piede", colore=col.attenuato)
        self.etich_g.shift([X(950) - self.etich_g.get_right()[0], Y(354) - self.etich_g.righe[0].puntello.get_center()[1], 0])
        self.add(self.fondo, self.etich, self.etich7, self.valore, self.etich_g)
        etichetta(self)

    def t_valore(self, s: str, colore, k=1.0, a=0.0, b=1.0, colore_coda=None) -> list[Tappa]:
        """Esce il simbolo che c'è (prima metà della finestra), entra il nuovo (seconda metà); la coda cambia tinta."""
        m = (a + b) / 2
        altri = VGroup(*[v for q, v in self.simboli.items() if q != s])
        return [t_op(altri, 0, a, m), t_tinta(self.simboli[s], colore, k, m, b), t_tinta(self.coda, colore_coda or colore, k, m, b)]


class Tavolo:
    """Tutto quello che le scene 2-7 hanno in comune, costruito acceso e poi portato allo stato d'inizio della scena."""

    K_SOLO = 64 / 44

    def __init__(self, scena: ScenaReel, compatta: bool = True):
        col = scena.cfg.palette
        self.col = col
        self.rich, self.boz, self.cont = Richiesta(col), Bozza(col), Conta(col)
        self.nota_max1 = testo(NOTA_MAX1, "piede", peso=BOLD)
        self.nota_max1.shift([X(940) - self.nota_max1.get_right()[0], Y(NOTE_Y) - self.nota_max1.righe[0].puntello.get_center()[1], 0])
        self.nota_max2 = testo("al massimo 2", "piede", peso=BOLD)
        self.nota_max2.shift([X(940) - self.nota_max2.get_right()[0], Y(NOTE_Y) - self.nota_max2.righe[0].puntello.get_center()[1], 0])
        self.nota_prove = testo(NOTA_PROVE, "piede", colore=col.attenuato)
        self.nota_prove.shift([self.nota_max1.get_left()[0] - px(30) - self.nota_prove.get_right()[0],
                               Y(NOTE_Y) - self.nota_prove.righe[0].puntello.get_center()[1], 0])
        self.note = etichetta(VGroup(self.nota_prove, self.nota_max1, self.nota_max2))
        # la lente, sotto la carta compatta. Scena 2 e inizio della 4: la frase 4 su due righe, con la sua cifra
        self.l_f4 = testo(FRASE_4, "caption").scale(1.2)
        self.l_f4.shift([X(LENTE_X + 56) - self.l_f4.get_left()[0], Y(LENTE_ALTO - 8) - self.l_f4.righe[0].puntello.get_top()[1], 0])
        self.l_cifra4 = etichetta(testo("4", "caption", peso=BOLD, mono=True))
        self.l_cifra4.shift([X(LENTE_X) - self.l_cifra4.get_left()[0],
                             self.l_f4.righe[0].puntello.get_center()[1] - self.l_cifra4.righe[0].puntello.get_center()[1], 0])
        self.lente_f4 = VGroup(self.l_cifra4, self.l_f4)
        # scena 4: «mi dispiace il doppio» nella prima riga della lente; le code di A10 e B9 prendono il posto di «il doppio»
        self.l_a10 = posa(testo("mi dispiace " + A10_CODA, "token"), LENTE_DX, LENTE_ALTO, da="dx")
        x_sx = float(self.l_a10.righe[0].glifi.get_left()[0]) * 120 + 540
        self.l_cuore = posa(testo(CUORE, "token"), x_sx, LENTE_ALTO)
        self.l_b9 = posa(testo("mi dispiace " + B9_CODA, "token"), x_sx, LENTE_ALTO)
        # quando nella lente il frammento è solo (scena 4, beat 2 e 3) cresce da 44 a 64 px attorno al suo angolo in alto a sinistra
        self.l_angolo = np.array([float(self.l_cuore.righe[0].glifi.get_left()[0]), float(self.l_cuore.righe[0].puntello.get_top()[1]), 0.0])
        self.l_b9.scale(self.K_SOLO, about_point=self.l_angolo)
        self.l_mi, self.l_doppio = self.l_cuore.parola("mi dispiace"), self.l_cuore.parola("il doppio")
        self.l_a10_coda, self.l_b9_coda = self.l_a10.parola(A10_CODA), self.l_b9.parola(B9_CODA)
        self.lente = VGroup(self.lente_f4, self.l_cuore, self.l_a10, self.l_b9)
        self.mondo = VGroup(self.rich, self.boz, self.cont, self.note, self.lente)
        self.con_la_carta = [self.boz, self.cont]            # ciò che scende e risale con la bozza (richiesta C grande)
        segna(self.mondo)
        if compatta:
            applica(*self.boz.t_compatta())

    def aggiungi(self, *mobs) -> None:
        for m in mobs:
            self.mondo.add(segna(m))

    def base(self) -> None:
        """Spegne tutto ciò che non è di ogni scena; le sagome della bozza tornano neutre, il testo vero è spento."""
        b, r = self.boz, self.rich
        op(VGroup(*b.frasi, *b.bande, *b.cifre, b.testi_nascosti, *[rs.barre for rs in b.fin_sag], b.ling_finale, b.dida_finale,
                  self.cont.etich7, self.cont.etich_g, self.note, self.lente, r.cg, r.barre_ab, r.barre_c), 0)
        tinta(b.tutte_barre, b.c_attenuato, K_NEUTRO)

    # gli stati fermi alla fine di ogni scena: la scena dopo parte da qui
    def fine_2(self) -> None:
        b, c, col = self.boz, self.cont, self.col
        self.base()
        applica(*self.rich.t_stato("A"), *c.t_valore("1", col.accento), t_op(VGroup(self.nota_prove, self.nota_max1), 1),
                *[t for k in (0, 1, 2, 4, 5) for t in b.t_frase(k, "spenta")], *b.t_frase(3, "accesa"), t_op(b.bande[3], 1),
                t_op(self.lente_f4, 1))

    def fine_4(self) -> None:
        b, c, col = self.boz, self.cont, self.col
        self.base()
        applica(*self.rich.t_stato("B"), *c.t_valore("2", col.accento), t_op(VGroup(self.nota_prove, self.nota_max2), 1),
                *[t for k in (1, 2, 4, 5) for t in b.t_frase(k, "spenta", salvo=[b.cuore_seg])],
                *[t for k in (0, 3) for t in b.t_frase(k, "accesa")], t_op(VGroup(b.bande[0], b.bande[3]), 1),
                t_tinta(b.cuore_seg, col.testo, K_ACCESO), t_fn(self.l_cuore, self.cresce_solo), t_op(self.l_mi, 1), *self.t_b9())

    def fine_5(self) -> None:
        b = self.boz
        self.base()
        applica(*self.rich.t_stato("CG"), *self.cont.t_valore("?", self.col.attenuato), t_tinta(VGroup(*b.cifre), b.c_attenuato, 0.8),
                t_sposta(VGroup(*self.con_la_carta), DOWN * px(GIU_CG)))

    def fine_6(self) -> None:
        self.base()
        applica(*self.rich.t_stato("CC"), *self.cont.t_valore("–", self.col.attenuato), *self.boz.t_finale())

    def cresce_solo(self, g) -> None:
        g.scale(self.K_SOLO, about_point=self.l_angolo)

    def t_b9(self, a=0.0, b=1.0) -> list[Tappa]:
        """Nella lente «il doppio» lascia il posto a «ancora di più» (B9): prima esce, poi entra."""
        m = (a + b) / 2
        return [t_op(self.l_doppio, 0, a, m), t_op(self.l_b9_coda, 1, m, b)]


class ScenaIA(ScenaReel):
    """Aiuti comuni: il tavolo, un passaggio a tappe, l'istante stimato di una parola della voce, il conto delle parole."""

    def prepara(self, compatta: bool = True) -> Tavolo:
        self.tv = Tavolo(self, compatta)
        return self.tv

    def fai(self, durata_s: float, *tappe, altre=()) -> None:
        piatte = [t for x in tappe for t in (x if isinstance(x, (list, tuple)) else [x])]
        self.play(Tappe(self.tv.mondo, piatte), *altre, run_time=self.arrotonda(durata_s))
        self.annota("passaggio")

    def annota(self, momento: str) -> None:
        """Con REEL_CONTA_PAROLE=file scrive una riga per passaggio: istante e parole leggibili (regola del presentatore)."""
        dove = os.environ.get("REEL_CONTA_PAROLE")
        if dove:
            n, e, testi = parole_a_schermo(self)
            with open(dove, "a", encoding="utf-8") as f:
                f.write(json.dumps({"scena": self.scena.get("n"), "t": round(self.t, 2), "momento": momento, "parole": n,
                                    "etichette": e, "testi": testi}, ensure_ascii=False) + "\n")

    def verifica(self, momento: str) -> None:
        super().verifica(momento)
        self.annota(momento)

    def alle(self, s: float) -> None:
        self.attendi_fino(s)

    def istante(self, i: int, parola: str) -> float:
        """Quando la voce arriva a `parola` nella frase i: in proporzione ai caratteri (la voce di prova ha 0,3 s di
        pausa fra le frasi e 0,5 s di coda). È una stima: gli agganci fini si riguardano con le clip vere."""
        frase = piano(self.scena["voce"][i]).lower()
        k = max(0, frase.find(parola.lower()))
        ini = self.inizi_frasi[i]
        fine = self.inizi_frasi[i + 1] - 0.3 if i + 1 < len(self.inizi_frasi) else self.durata_s - 0.5
        return ini + (fine - ini) * k / max(1, len(frase))

    def fine_beat(self, i: int) -> float:
        return (self.inizi_frasi[i + 1] if i + 1 < len(self.inizi_frasi) else self.durata_s) - self.ANTICIPO_S


# --- le scene -----------------------------------------------------------------------------------------------------------

class Scena02(ScenaIA):
    """La mail di Giulia si legge intera per un secondo, poi ogni riga diventa la sua sagoma, grande com'era il testo; la
    richiesta A cala, la scommessa «? su 5» si gioca sulle cinque sagome, e la risposta: «1 su 5» enorme (tipografia
    cinetica) mentre la carta arretra e si compatta; sotto, nella lente, la sola frase che torna, quella con la data;
    poi «1 su 5» torna piccolo sul bordo della bozza con «10 prove» e «al massimo 1»."""

    def costruisci(self):
        tv = self.prepara(compatta=False)
        b, c, r, col, a = tv.boz, tv.cont, tv.rich, tv.col, self.area.contenuto
        note = self.scena.get("testo") or [NOTA_PROVE, NOTA_MAX1]
        assert note[0] == NOTA_PROVE and note[1] == NOTA_MAX1, "le note della scena 2 sono cambiate nella sceneggiatura"
        tv.base()
        applica(*r.t_stato("A"), *c.t_valore("–", col.attenuato))
        op(VGroup(*b.frasi), 1)                              # l'unico momento del reel in cui la mail è testo
        op(VGroup(r, c, b.tutte_barre), 0)
        su = UP * px(SU_INIZIO)
        carta = VGroup(b, c)
        carta.shift(su)
        self.add(tv.mondo)                                   # fotogramma 0 pieno: si arriva da uno stacco sul filmato
        self.annota("inizio")

        # beat 0 «Questa l'ha scritta Giulia, di getto…»: le cinque frasi prendono una tinta (primo movimento a 0,13 s);
        # poi, riga per riga dall'alto, sotto il testo compare la sua sagoma e il testo si spegne: a 1,4 s non c'è più
        d0 = self.durata_beat(0)
        self.alle(0.13)
        self.fai(0.47, [t_op(b.bande[k], 1, 0.15 * k, 0.15 * k + 0.4, rush_from) for k in range(5)])
        passo = 0.045
        self.fai(0.8, [t for _, _, n, rs in b.righe for t in (t_tinta(rs.barre, b.c_attenuato, K_NEUTRO, passo * n, passo * n + 0.2),
                                                                t_op(rs.riga.glifi, 0, passo * n + 0.17, passo * n + 0.4))])
        self.alle(0.58 * d0)
        self.fai(0.5, t_entra(VGroup(c.fondo, c.etich, c.simboli["–"], c.coda), sposta=UP * px(16)))

        # beat 1 «E sopra ci scrive «migliora questa mail».»: la richiesta cala e spinge giù la bozza, poi si scrive
        self.beat(1)
        rimbalzo = rate_functions.ease_out_back
        self.fai(0.6, t_entra(r.cornice, sposta=DOWN * px(150), rate=rimbalzo), t_sposta(carta, -su, rate=rimbalzo))
        op(r.a, 0)
        for w, chiave in zip(parole_di(r.a), ("migliora", "questa", "mail")):
            self.alle(self.istante(1, chiave) - 0.08)
            self.fai(0.2, t_entra(w, sposta=UP * px(10), rate=rush_from))

        # beat 2 «Tu intanto scommetti, di cinque frasi sue quante ne tornano uguali?»: le cifre a margine, poi il «?»
        self.beat(2)
        self.alle(self.istante(2, "di cinque") - 0.15)
        self.fai(0.9, [t_entra(b.cifre[k], 0.18 * k, 0.18 * k + 0.28, sposta=RIGHT * px(14), rate=rush_from, k=0.8) for k in range(5)])
        self.alle(self.istante(2, "quante") - 0.1)
        casa_valore = c.valore.copy()
        k_g = 1.62

        def in_colonna(g):
            g.scale(k_g)
            g.shift([X(950) - g.get_right()[0], Y(290) - g.get_center()[1], 0])
        self.fai(0.7, t_op(VGroup(c.fondo, c.etich), 0, 0, 0.3), t_op(c.simboli["–"], 0, 0, 0.3),
                 t_fn(c.valore, in_colonna, 0.3, 0.85, rimbalzo), t_tinta(c.coda, col.testo, 1, 0.3, 0.85),
                 t_tinta(c.simboli["?"], col.accento, 1, 0.55, 1), t_entra(c.etich_g, 0.7, 1, sposta=UP * px(8)))
        # il vuoto della scommessa: il punto di domanda lampeggia fino alla risposta
        while self.fine_beat(2) - self.t > 0.75:
            self.fai(0.7, t_fn(c.simboli["?"], lambda g: op(g, 0.15), rate=there_and_back))

        # beat 3 «Beh, nelle nostre prove al massimo una, quella con la data.»: le sagome 1, 2, 3, 5 si spengono, la 4 resta
        self.beat(3)
        t_wow = self.istante(3, "al massimo") - 0.1
        spegni = [t for j, k in enumerate((0, 1, 2, 4, 5)) for t in b.t_frase(k, "spenta", 0.17 * j, 0.17 * j + 0.24)]
        self.fai(max(0.5, min(1.2, t_wow - self.t - 0.15)), spegni, b.t_frase(3, "accesa", 0.6, 1))
        self.alle(t_wow)
        # GRANDE (tipografia cinetica): «1 su 5» arriva enorme con la sua etichetta e le due note, e spinge indietro il resto
        fondale = VGroup(r, b)
        # le due note hanno una copia grande per il wow: al ritorno la grande si spegne dov'è mentre la piccola si accende a
        # casa (se viaggiassero attraverserebbero «1 su 5» che sale; così «al massimo 1» resta sempre leggibile)
        note_casa = VGroup(tv.nota_prove, tv.nota_max1)
        op(note_casa, 1)                                     # la copia si fa da accese: `segna` ricorda l'opacità che trova
        note_v = etichetta(note_casa.copy())
        op(note_casa, 0)
        tv.aggiungi(note_v)
        centro = a.centro + UP * px(60)
        k_v = px(700) / c.valore.width

        def grande_valore(g):
            g.scale(k_v).move_to(centro + UP * px(90))

        def grande_etichetta(g):
            g.scale(1.45).move_to(centro + DOWN * px(80))

        def indietro(g):
            g.scale(0.88, about_point=centro)
            attenua(g, 0.14)
        # mentre arretra la carta si compatta: da qui la mail è una mappa, e sotto si libera la lente. I due stati
        # d'arrivo (arretrata, e poi a casa) si preparano sugli oggetti veri e si copiano; poi tutto torna com'è adesso
        adesso = fondale.copy()
        applica(*b.t_compatta())
        salvato = fondale.copy()
        indietro(VGroup(*foglie(fondale)))
        arretrato = fondale.copy()
        applica(t_punti(fondale, adesso, stile=True))
        op(note_v, 0)
        note_v.scale(1.45).move_to(centro + DOWN * px(170))
        self.fai(0.45, t_punti(fondale, arretrato, 0, 0.7, rush_from, stile=True), c.t_valore("1", col.accento, 1, 0, 0.3),
                 t_fn(c.valore, grande_valore, 0.1, 1, rimbalzo), t_fn(c.etich_g, grande_etichetta, 0.1, 1, rimbalzo),
                 t_entra(note_v, 0.45, 1, scala=0.7, rate=rimbalzo))
        # «quella con la data»: sotto il numero, nella lente, la frase 4 parola per parola; è l'unico testo della mail che resta
        self.alle(max(self.t + 0.25, self.istante(3, "quella con la data") - 0.2))
        self.fai(0.45, t_entra(tv.l_cifra4, 0, 0.5, scala=0.6, rate=rimbalzo),
                 [t_entra(riga, 0.2 + 0.3 * j, 0.6 + 0.3 * j, sposta=UP * px(18), rate=rate_functions.ease_out_cubic)
                  for j, riga in enumerate(tv.l_f4.righe)])
        self.alle(min(self.t + 0.35, self.durata_s - 1.4))
        # ritorno: valore e note a casa (in alto), poi il resto si riaccende; l'etichetta grande esce, quella sul bordo rientra
        self.fai(0.7, t_punti(c.valore, casa_valore, 0, 0.6), t_op(note_v, 0, 0, 0.3), t_op(note_casa, 1, 0.15, 0.5), t_op(c.etich_g, 0, 0, 0.25),
                 t_punti(fondale, salvato, 0.45, 1, stile=True), t_op(VGroup(c.fondo, c.etich), 1, 0.65, 1))


class Scena04(ScenaIA):
    """«Migliora» vuol dire «riscrivi»; GRANDE (metamorfosi): nella lente «mi dispiace il doppio» diventa sul posto la
    frase di A10, sotto arrivano A8 e A9 con la stessa coda e «4 su 10»; poi la richiesta B, il «?» e «2 su 5»."""

    def costruisci(self):
        tv = self.prepara()
        b, c, r, col = tv.boz, tv.cont, tv.rich, tv.col
        t_riscrivi, t_410, t_max2 = self.scena["testo"]
        riscrivi = etichetta(Etichetta(t_riscrivi))
        riscrivi.move_to([X(950) - riscrivi.width / 2, Y((RICH_ALTO + RICH_BASSO_A) / 2), 0])
        freccia = Freccia([r.a.get_right()[0] + px(16), riscrivi.get_center()[1], 0], riscrivi.get_left(), colore=col.accento)
        # i frammenti veri di A8 e A9 sotto quello di A10, allineati a destra: «per il disagio» fa colonna
        fr8 = posa(testo(A8, "token", colore=col.attenuato), LENTE_DX, LENTE_ALTO + LENTE_PASSO, da="dx")
        fr9 = posa(testo(A9, "token", colore=col.attenuato), LENTE_DX, LENTE_ALTO + 2 * LENTE_PASSO, da="dx")
        code = [tv.l_a10.parola("per il disagio"), fr8.parola("per il disagio"), fr9.parola("per il disagio")]
        for g in code:
            g.set_color(col.accento)
        colonna = VGroup(*code)
        cornice = RoundedRectangle(corner_radius=px(14), width=colonna.width + px(24), height=colonna.height + px(22),
                                   stroke_color=col.accento, stroke_width=tratto(4), fill_opacity=0).move_to(colonna)
        pill_t = testo(t_410, "piede", colore=col.sfondo, peso=BOLD)
        pill_f = RoundedRectangle(corner_radius=px(22), width=pill_t.width + px(40), height=px(46), stroke_width=0,
                                  fill_color=col.accento, fill_opacity=1)
        pillola = etichetta(VGroup(pill_f, pill_t.move_to(pill_f)))
        pillola.move_to([cornice.get_right()[0] - pillola.width / 2, cornice.get_top()[1] + pillola.height / 2 - px(2), 0])
        assert t_max2 == "al massimo 2", "la nota della scena 4 è cambiata nella sceneggiatura"
        tv.aggiungi(riscrivi, freccia, fr8, fr9, cornice, pillola)
        tv.fine_2()
        op(VGroup(riscrivi, freccia, fr8, fr9, cornice, pillola), 0)
        self.add(tv.mondo)                                   # fotogramma 0 pieno: stacco dal filmato della scena 3
        self.annota("inizio")

        # beat 0 «Il punto è che «migliora» per lei vuol dire «riscrivi»,»
        self.fai(0.35, t_tinta(r.migliora, col.accento, a=0.25))
        self.alle(self.istante(0, "riscrivi") - 0.25)
        self.fai(0.5, t_entra(freccia, 0, 0.6, sposta=RIGHT * px(30)),
                 t_entra(riscrivi, 0.3, 1, scala=0.6, rate=rate_functions.ease_out_back))

        # beat 1 «e riscrivendo pesca fra le parole più battute, quelle di tutti.»: GRANDE (metamorfosi)
        self.beat(1)
        d1 = self.durata_beat(1)
        # la frase 4 lascia la lente e la sua sagoma si spegne; nella frase 3 si accende una barretta, e da lì esce il frammento
        self.fai(0.6, t_esce(tv.lente_f4, 0, 0.35, sposta=DOWN * px(20), rate=rush_into), b.t_frase(3, "spenta", 0, 0.35),
                 t_tinta(b.cuore_seg, col.testo, K_ACCESO, 0.38, 0.62),
                 t_entra(tv.l_cuore, 0.5, 1, sposta=DOWN * px(28), scala=0.82, rate=rate_functions.ease_out_cubic))
        self.alle(max(self.t, self.istante(1, "pesca") - 0.2))
        # «il doppio» esce, poi al suo posto entra la coda di A10, parola per parola
        nuove = parole_di(tv.l_a10)[2:]
        self.fai(min(1.1, 0.3 * d1), t_esce(tv.l_doppio, 0, 0.28, sposta=UP * px(16), rate=rush_into),
                 [t_entra(w, 0.32 + 0.13 * j, 0.32 + 0.13 * j + 0.2, sposta=DOWN * px(16), scala=1.25, rate=rate_functions.ease_out_back)
                  for j, w in enumerate(nuove)])
        applica(t_sposta(tv.l_doppio, DOWN * px(16)))        # spento: torna al suo posto per il beat 2
        self.alle(max(self.t, self.istante(1, "parole più") - 0.25))
        # nella richiesta resta a testo solo «Migliora»; da destra scivolano i frammenti di A8 e A9
        self.fai(0.8, t_op(r.resto_a, 0, 0, 0.26), t_tinta(r.sag_a.barre[1], b.c_attenuato, K_NEUTRO, 0.26, 0.5),
                 t_entra(fr8, 0.3, 0.76, sposta=LEFT * px(60), rate=rate_functions.ease_out_cubic),
                 t_entra(fr9, 0.5, 1, sposta=LEFT * px(60), rate=rate_functions.ease_out_cubic))
        self.alle(max(self.t, self.istante(1, "quelle di tutti") - 0.2))
        self.fai(0.55, t_traccia(cornice, 0, 0.7), t_entra(pillola, 0.5, 1, scala=0.5, rate=rate_functions.ease_out_back))

        # beat 2 «E se aggiungi «mantenendo il mio stile»?»: tutto com'era, poi la riga B e il «?»
        self.beat(2)
        extra = VGroup(fr8, fr9, cornice, pillola, riscrivi, freccia, tv.l_a10_coda, tv.nota_max1, r.sag_a.barre[1])
        neutre = [t for k in range(6) for t in b.t_frase(k, "neutra", 0.5, 1, salvo=[b.cuore_seg])]
        self.fai(0.7, t_op(extra, 0, 0, 0.36), t_tinta(r.migliora, col.testo, 1, 0, 0.36),
                 c.t_valore("?", col.attenuato, 1, 0, 0.9, colore_coda=col.attenuato), neutre,
                 t_fn(tv.l_cuore, tv.cresce_solo, 0.4, 0.9, rate_functions.ease_out_back), t_op(VGroup(tv.l_doppio, r.resto_a), 1, 0.5, 1))
        self.alle(max(self.t, self.istante(2, "mantenendo") - 0.3))
        op(r.b2, 0)
        self.fai(0.7, t_op(r.punto_a, 0, 0, 0.25), t_punti(r.box, r.box_b, 0.1, 0.5, rate_functions.ease_out_back),
                 [t_entra(w, 0.4 + 0.12 * j, 0.4 + 0.12 * j + 0.22, sposta=UP * px(10), rate=rush_from) for j, w in enumerate(parole_di(r.b2))])

        # beat 3 «Cambia meno, ma di frasi sue ne tornano al massimo due.»: restano accese la 1 e la 4 (B9)
        self.beat(3)
        spegni = [t for j, k in enumerate((1, 2, 4, 5)) for t in b.t_frase(k, "spenta", 0.2 * j, 0.2 * j + 0.3, salvo=[b.cuore_seg])]
        accendi = [t for k in (0, 3) for t in b.t_frase(k, "accesa", 0.55, 1)] + [t_op(VGroup(b.bande[0], b.bande[3]), 1, 0.55, 1)]
        self.fai(0.9, spegni, accendi)
        self.fai(0.7, tv.t_b9())
        self.alle(max(self.t, self.istante(3, "al massimo") - 0.1))
        self.fai(0.6, c.t_valore("2", col.accento, 1, 0, 0.5),
                 t_fn(c.valore, lambda g: g.scale(1.35, about_point=g.get_right()), 0.25, 1, there_and_back),
                 t_entra(tv.nota_max2, 0.5, 1, sposta=UP * px(10)))


class Scena05(ScenaIA):
    """La mossa: cambia la richiesta, non la bozza. La bozza è a righe-sagoma dal primo all'ultimo fotogramma e non
    cambia mai; GRANDE (carica e rimbalzo): «Migliora» si accende, una barra in accento taglia la riga, la riga
    barrata arretra e schizza via dalla carta verso l'alto, e la carta vuota cresce di colpo fino a tre righe grandi
    spingendo giù le sagome; poi la richiesta C si scrive insieme alla voce. Nessun credito, nessun punch, nessuna
    icona: l'ultimo fotogramma è `Tavolo.fine_5()`, lo stato da cui parte la scena 6."""

    SU_RICH = 6            # di quanto «sale» la carta richiesta nel beat 0: più su la linguetta uscirebbe dalla safe area
    GIU_PRIMO = 30         # quanto si stacca il tavolo nel beat 0; il resto (GIU_CG - GIU_PRIMO) lo spinge la carta che cresce
    VOLO_PX = 440          # la corsa della riga barrata che schizza via dalla carta
    RIFLESSO_PX = 408      # la corsa del riflesso sulle sagome, da sotto il bordo alto a sopra il bordo basso

    def costruisci(self):
        tv = self.prepara()
        b, c, r, col = tv.boz, tv.cont, tv.rich, tv.col
        # la riga barrata schizza via *dietro* la linguetta, non sopra: senza questo i suoi glifi passerebbero sopra
        # «richiesta» per due fotogrammi (a rest nessun testo tocca la linguetta: l'ultimo fotogramma non cambia)
        r.ling.set_z_index(1)
        barra = Barrato(r.migliora, colore=col.accento)
        # il riflesso: tre strisce sottili che fanno una banda chiara di 72 px, larga quanto la carta bozza. Parte già
        # alla quota che la carta avrà dopo la spinta (non viaggia con lei)
        riflesso = VGroup(*[Rectangle(width=px(DX - SX), height=px(24), stroke_width=0, fill_color=col.testo, fill_opacity=o)
                            for o in (0.08, 0.20, 0.08)])
        riflesso.arrange(DOWN, buff=0).move_to([X((SX + DX) / 2), Y(BOZ_ALTO + GIU_CG + 36), 0])
        tv.aggiungi(barra, riflesso)
        tv.fine_4()
        op(VGroup(barra, riflesso), 0)
        # «elencami i problemi» si scrive in accento (la virgola no) e torna del colore del testo nel beat 3
        fuoco = r.cg.righe[1].parola(RICHIESTA_C_FUOCO)
        fuoco.set_color(col.accento)
        parole = parole_di(r.cg)                             # 4 + 3 + 3 = le dieci parole della richiesta C
        self.add(tv.mondo)
        self.annota("inizio")

        # beat 0 «Quindi, se ci tieni che suoni come te, la cosa da cambiare è proprio la richiesta.»
        # escono il frammento di B9 e le note della scena 4, e «2 su 5» si attenua: il conto della richiesta B è chiuso
        self.alle(0.14)
        self.fai(0.75, t_esce(tv.lente, 0, 0.4, sposta=DOWN * px(26), rate=rush_into),
                 t_esce(tv.note, 0, 0.4, sposta=RIGHT * px(24), rate=rush_into),
                 t_tinta(VGroup(c.simboli["2"], c.coda), col.attenuato, 1, 0.45, 1))
        # su «suoni come te» le sagome tornano tutte neutre, dall'alto in basso: è di nuovo la bozza di Giulia, intatta
        self.alle(max(self.t, self.istante(0, "suoni come te") - 0.3))
        self.fai(0.95, [t for k in range(6) for t in b.t_frase(k, "neutra", 0.11 * k, 0.11 * k + 0.3)])
        # su «la richiesta» la carta prende il bordo in accento, sale di poco e il tavolo sotto si stacca da lei
        self.alle(max(self.t, self.istante(0, "la richiesta") - 0.35))
        carta_r = VGroup(r.box, r.ling, r.a, r.b2, barra)
        morbida = rate_functions.ease_out_cubic
        self.fai(0.7, t_tinta(r.box, col.accento, 1, 0, 0.55),
                 t_sposta(carta_r, UP * px(self.SU_RICH), 0.15, 0.8, morbida),
                 t_sposta(VGroup(*tv.con_la_carta), DOWN * px(self.GIU_PRIMO), 0.15, 0.8, morbida))

        # beat 1 «Cioè non le chiedi più di migliorare la mail,»: GRANDE (carica e rimbalzo)
        self.beat(1)
        self.fai(0.42, t_tinta(r.migliora, col.accento, 1, 0, 0.5), t_traccia(barra, 0.4, 1, rush_from))
        # la carica: la riga arretra di poco, poi schizza via dalla carta verso l'alto e si spegne per strada
        riga_b = VGroup(r.a, r.b2, barra)
        self.alle(max(self.t + 0.05, self.istante(1, "chiedi") - 0.25))
        # la partenza è la parte veloce della corsa (`rush_from`): la riga lascia la fascia della linguetta in un
        # fotogramma, così i suoi glifi non si leggono mai accanto a «richiesta»
        self.fai(0.6, t_sposta(riga_b, DOWN * px(18), 0, 0.28, rush_from),
                 t_sposta(riga_b, UP * px(self.VOLO_PX), 0.28, 1, rush_from), t_op(riga_b, 0, 0.42, 0.9, linear))
        # il rimbalzo: la carta vuota cresce di colpo fino a tre righe grandi e spinge giù le sagome, che non cambiano
        self.alle(max(self.t, self.istante(1, "migliorare") - 0.25))
        self.fai(0.55, t_punti(r.box, r.box_cg, 0, 1, rimbalzo_corto, stile=True),
                 t_sposta(r.ling, DOWN * px(self.SU_RICH), 0, 1, rimbalzo_corto),
                 t_sposta(VGroup(*tv.con_la_carta), DOWN * px(GIU_CG - self.GIU_PRIMO), 0, 1, rimbalzo_corto))
        # «Non migliorare questa mail:», le sole parole leggibili del beat
        t0 = max(self.t + 0.05, self.istante(1, "la mail") - 0.35)
        self.alle(t0)
        self.scrivi(parole[:4], self.fine_beat(1) - t0)

        # beat 2 «ma le fai elencare i problemi, senza riscrivere niente.»: la riga continua insieme alla voce
        self.beat(2)
        self.alle(max(self.t, self.istante(2, "elencare") - 0.25))
        self.scrivi(parole[4:7], 0.8)
        self.alle(max(self.t + 0.05, self.istante(2, "senza riscrivere") - 0.25))
        self.scrivi(parole[7:], 0.8)

        # beat 3 «In pratica lei ti fa da correttore, e chi scrive resti tu.»
        # la richiesta C si posa (il fuoco torna del colore del testo: l'ultimo fotogramma è quello da cui parte la 6)
        # e il contatore torna «? su 5» attenuato, come dopo le altre due richieste: la risposta arriva nella scena 6
        self.beat(3)
        self.fai(0.8, t_tinta(fuoco, col.testo, 1, 0, 0.4), c.t_valore("?", col.attenuato, 1, 0.3, 1))
        # su «chi scrive resti tu» un riflesso chiaro scorre una volta sulle sagome e le lascia identiche
        self.alle(max(self.t, self.istante(3, "chi scrive") - 0.15))
        self.fai(0.95, t_op(riflesso, 1, 0, 0.12), t_sposta(riflesso, DOWN * px(self.RIFLESSO_PX), 0, 1),
                 t_op(riflesso, 0, 0.88, 1))

    def scrivi(self, parole: list, durata_s: float) -> None:
        """Le parole di una riga della richiesta entrano una dopo l'altra, al passo della voce."""
        n = len(parole)
        self.fai(max(0.45, durata_s), [t_entra(w, j / n, j / n + 0.75 / n, sposta=UP * px(12), rate=rush_from)
                                       for j, w in enumerate(parole)])


class Scena06(ScenaIA):
    """La richiesta C si stringe e la bozza resta com'è, a sagome: si accendono i punti segnalati da C2 e nella lente
    si leggono, grandi, i riempitivi e la data; GRANDE (contrasto di scala): resta solo «mi dispiace il doppio» a 2×,
    con «segnalata 10 su 10» attaccata e poi il commento di C2; infine le sagome diventano quelle della mail finale."""

    def costruisci(self):
        tv = self.prepara()
        b, c, r, col = tv.boz, tv.cont, tv.rich, tv.col
        t_segnalata, t_riscritta = self.scena["testo"]
        assert t_riscritta == "riscritta da noi", "la didascalia della mail finale è cambiata nella sceneggiatura"
        # nella carta: le barrette dei riempitivi (C2 accende «molto seri»; dalla carta poi cade solo «molto»), le tre
        # sottolineature senza etichetta, il riquadro sulla frase 4
        seg = {w: b.seg(0 if w == "in realtà" else 1, w) for w in ("in realtà", "Purtroppo", "molto", "seri", "sostanzialmente", "davvero",
                                                                    "sono stati riscontrati", "procedere",
                                                                    "a una riprogrammazione della consegna", "slitta", "di poco")}
        accesi = [[seg["in realtà"]], [seg["Purtroppo"]], [seg["sostanzialmente"]], [seg["davvero"]], [seg["molto"], seg["seri"]]]
        linee = VGroup(sotto_le_barre([seg["sono stati riscontrati"]], col.secondario), sotto_le_barre([seg["procedere"]], col.secondario),
                       sotto_le_barre([seg["a una riprogrammazione della consegna"]], col.secondario),
                       sotto_le_barre([seg["slitta"], seg["davvero"], seg["di poco"]], col.secondario))
        barra4 = b.barre(3)
        y4 = c_centro(b.prima_riga[3], 3)
        riq4 = scatola(TESTO_X - 12, y4 - 14, (float(barra4.get_right()[0]) * 120 + 540) + 12, y4 + 14, col.secondario, raggio=9)
        riq4_su = scatola(TESTO_X - 12, fin_slot(1)[0] + 4, DX - 12, fin_slot(1)[1] - 4, col.secondario, raggio=12)
        # nella lente: l'etichetta di C2 e i cinque riempitivi, grandi, su due righe; sotto, «arriva quarta» e la data
        et_riemp = testo(C2_RIEMPITIVI, "piede", colore=col.accento)
        et_riemp.shift([X(LENTE_X) - et_riemp.get_left()[0], Y(962) - et_riemp.righe[0].puntello.get_top()[1], 0])
        parole, x, y = [], LENTE_X, 1010
        for n, w in enumerate(RIEMPITIVI):
            t = testo(w, "caption", colore=col.accento)
            if n == 3:
                x, y = LENTE_X, 1072
            posa(t, x, y)
            x = float(t.get_right()[0]) * 120 + 540 + 40
            parole.append(t)
        et_quarta = etichetta(testo(C2_QUARTA, "piede", colore=col.secondario))
        data_l = posa(testo(FINALE_DATA, "caption"), LENTE_X, 1138)
        et_quarta.shift([X(LENTE_X) - et_quarta.get_left()[0],
                         data_l.righe[0].puntello.get_bottom()[1] - et_quarta.righe[0].puntello.get_bottom()[1] + px(3), 0])
        data_l.shift([et_quarta.get_right()[0] + px(24) - data_l.get_left()[0], 0, 0])
        # attaccata a «mi dispiace il doppio» (sopra, a filo a sinistra); il commento di C2 sta sotto, staccato
        riga_cuore = b.f3_comp.righe[2]
        seg_t = testo(t_segnalata, "piede", colore=col.sfondo, peso=BOLD)
        seg_f = RoundedRectangle(corner_radius=px(12), width=seg_t.width + px(28), height=px(48), stroke_width=0, fill_color=col.accento, fill_opacity=1)
        segnalata = etichetta(VGroup(seg_f, seg_t.move_to(seg_f)))
        segnalata.move_to([b.cuore36.get_left()[0] + segnalata.width / 2, riga_cuore.puntello.get_top()[1] + px(8) + segnalata.height / 2, 0])
        commento = posa(testo(C2_COMMENTO, "piede"), float(b.cuore36.get_left()[0]) * 120 + 540,
                        960 - float(riga_cuore.puntello.get_bottom()[1]) * 120 + 46)
        tv.aggiungi(linee, riq4, et_riemp, *parole, et_quarta, data_l, segnalata, commento)
        tv.con_la_carta += [linee, riq4]
        tv.fine_5()
        # la scena parte da `fine_5()`: richiesta C grande alla lettera, bozza a sagome, «? su 5» attenuato. Nessun oggetto
        # della scena 5 (credito, voci) entra qui: la 5 può essere riscritta senza toccare questa scena
        op(VGroup(linee, riq4, et_riemp, *parole, et_quarta, data_l, segnalata, commento), 0)
        self.add(tv.mondo)
        self.annota("inizio")

        # beat 0 «Così la bozza resta com'è, e lei ti segnala i riempitivi, la data in fondo.»
        # la richiesta si stringe alle sue sagome (a testo resta «elencami i problemi,») e la bozza risale; «5 su 5» attenuato
        morbida = rate_functions.ease_in_out_cubic
        self.alle(0.15)
        self.fai(1.0, t_op(VGroup(r.cg.righe[0], r.cg.righe[2]), 0, 0, 0.3),
                 t_fn(r.c_fuoco, r.stringi_fuoco, 0.3, 0.7, morbida), t_punti(r.box, r.box_cc, 0.3, 0.7, morbida),
                 t_sposta(VGroup(*tv.con_la_carta), UP * px(GIU_CG), 0.3, 0.7, morbida),
                 t_tinta(r.barre_c, b.c_attenuato, K_NEUTRO, 0.7, 1), c.t_valore("5", col.attenuato, 1, 0.6, 1))   # mai in accento prima della 7
        self.alle(max(self.t, self.istante(0, "i riempitivi") - 0.35))
        rimbalzo = rate_functions.ease_out_back
        self.fai(1.2, t_entra(et_riemp, 0, 0.25, sposta=RIGHT * px(20)),
                 [t_tinta(VGroup(*gruppo), col.accento, 1, 0.1 + 0.13 * j, 0.1 + 0.13 * j + 0.2, rush_from) for j, gruppo in enumerate(accesi)],
                 [t_entra(w, 0.14 + 0.13 * j, 0.14 + 0.13 * j + 0.26, sposta=UP * px(30), scala=0.7, rate=rimbalzo) for j, w in enumerate(parole)],
                 [t_traccia(l, 0.78 + 0.05 * j, 0.78 + 0.05 * j + 0.17) for j, l in enumerate(linee)])
        self.alle(max(self.t, self.istante(0, "la data in fondo") - 0.25))
        self.fai(0.6, t_traccia(riq4, 0, 0.6), b.t_frase(3, "accesa", 0, 0.5), t_entra(et_quarta, 0.35, 0.75, sposta=RIGHT * px(16)),
                 t_entra(data_l, 0.5, 1, sposta=RIGHT * px(30), scala=0.8, rate=rimbalzo))

        # beat 1 «Attenzione però, perché ci mette anche «mi dispiace il doppio»,»: GRANDE (contrasto di scala)
        self.beat(1)
        fuoco = [*b.cuore36.submobjects, b.cuore_seg]
        resto = VGroup(*[m for m in foglie(tv.mondo) if all(m is not g for g in fuoco)])
        salvato = resto.copy()
        self.fai(0.45, t_tinta(b.cuore_seg, col.accento, 1, 0, 0.45), t_op(resto, 0, 0.2, 1))
        larga, centro = self.inquadratura(b.cuore36, 2.0)
        # nel vuoto la barretta diventa le sue parole, e la camera ci va sopra
        # (la barretta scende di 18 px mentre si spegne: sopra le parole, per un fotogramma, si leggeva come una barratura)
        def sotto_e_via(g):
            g.shift(DOWN * px(18))
            op(g, 0)

        def su_e_accesa(g):
            g.shift(UP * px(18))
            tinta(g, col.accento, 1)
        self.fai(0.8, t_fn(b.cuore_seg, sotto_e_via, 0.08, 0.4), t_tinta(b.cuore36, col.accento, 1, 0.22, 0.55),
                 altre=[self.camera.frame.animate(rate_func=morbida).set(width=larga).move_to(centro)])
        self.alle(max(self.t + 0.1, self.istante(1, "ci mette") - 0.1))
        self.fai(0.4, t_entra(segnalata, scala=0.6, sposta=UP * px(10), rate=rimbalzo))

        # beat 2 «e a quella Giulia ci teneva, quindi il consiglio non lo prende.»: il commento di C2, poi via tutti e due
        self.beat(2)
        self.fai(0.4, t_entra(commento, sposta=UP * px(12)))
        self.alle(max(self.t + 1.15, self.istante(2, "quindi il consiglio") - 0.3))
        self.fai(0.4, t_esce(VGroup(commento, segnalata), sposta=RIGHT * px(60), rate=rush_into))
        self.play(self.camera.frame.animate(rate_func=morbida).set(width=self.cfg.frame_width).move_to(ORIGIN),
                  run_time=self.arrotonda(0.6))
        # le parole tornano barretta (in accento: il consiglio non lo prende), poi tutto com'era
        self.fai(0.55, t_op(b.cuore36, 0, 0, 0.28), t_fn(b.cuore_seg, su_e_accesa, 0.12, 0.4), t_punti(resto, salvato, 0.4, 1, stile=True))

        # beat 3 «Poi la mail se la riscrive da sola.»: cadono i riempitivi, escono le sagome vecchie, entrano le nuove
        self.beat(3)
        self.alle(max(self.t, self.inizi_frasi[3] + 0.15))

        def cade(g, giu=24, giro=-0.12):
            g.shift(DOWN * px(giu)).rotate(giro)
            op(g, 0)
        molto_seri = parole[4]
        # nella lente cade prima la riga di sotto, poi quella di sopra, che scende poco: «seri» resta e nessuno lo attraversa
        cadono = [(parole[3], 24, -0.12), (molto_seri.parola("molto"), 24, -0.12), (parole[0], 12, -0.05), (parole[1], 12, -0.05),
                  (parole[2], 12, -0.05)]
        cadono_seg = [seg["davvero"], seg["molto"], seg["in realtà"], seg["Purtroppo"], seg["sostanzialmente"]]
        self.fai(0.45, [t_fn(g, lambda x, giu=giu, giro=giro: cade(x, giu, giro), 0.1 * j, 0.1 * j + 0.6, rush_into)
                        for j, (g, giu, giro) in enumerate(cadono)],
                 [t_fn(g, lambda x: cade(x, 12), 0.1 * j, 0.1 * j + 0.6, rush_into) for j, g in enumerate(cadono_seg)],
                 t_tinta(seg["seri"], b.c_attenuato, K_NEUTRO), t_tinta(molto_seri.parola("seri"), col.testo))
        # il riquadro della data non viaggia: si spegne con la frase 4 e si riaccende in testa, sulla riga nuova della data
        vecchio = VGroup(b.barre(0), b.barre(1), b.barre(3), linee, et_riemp, molto_seri, et_quarta, data_l, b.ling, b.dida, *b.cifre,
                         c.simboli["5"], riq4)
        self.fai(1.25, t_op(vecchio, 0, 0, 0.26),
                 t_punti(riq4, riq4_su, 0.27, 0.28), t_op(riq4, 1, 0.5, 0.64),
                 b.t_verso_finale(0.28, 0.62, morbida), t_punti(b.box, b.box_finale, 0.28, 0.62, stile=True),
                 t_tinta(b.fin_barre_data, b.c_attenuato, K_NEUTRO, 0.62, 0.8), t_entra(b.fin_data, 0.62, 0.8, sposta=RIGHT * px(16)),
                 t_op(riq4, 0, 0.8, 1),
                 t_tinta(b.fin_barre_altre, b.c_attenuato, K_NEUTRO, 0.74, 1), t_op(VGroup(b.ling_finale, b.dida_finale), 1, 0.74, 1),
                 t_tinta(c.simboli["–"], col.attenuato, 1, 0.74, 1),
                 t_op(VGroup(b.cuore_seg, b.porto_seg), 0, 0.72, 0.84), t_tinta(VGroup(b.cuore_fin, b.porto_fin), col.accento, 1, 0.8, 1))


class Scena07(ScenaIA):
    """Chiusura: la mail finale si riduce alle frasi 3 e 5, sopra il messaggio; l'etichetta del contatore cambia a
    vista e solo dopo «5 su 5» si accende; GRANDE (rivelazione a tratto) sotto «mi dispiace il doppio»; CTA."""

    def costruisci(self):
        tv = self.prepara()
        b, c, r, col, a = tv.boz, tv.cont, tv.rich, tv.col, self.area.contenuto
        s = self.scena["messaggio"].replace("chiedi i ", "chiedi\ni ").replace(". ==", ".\n==").replace("parole mettile", "parole==\n==mettile")
        msg = etichetta(Titolo(s, ruolo="messaggio"))
        msg.move_to([X(SX + 8) + msg.width / 2, Y(232) - msg.height / 2, 0])
        # la carta ridotta: restano le righe delle frasi 3 e 5, il contatore scende col bordo alto
        alto_nuovo, basso_nuovo = fin_slot(6)[0] - 34, fin_slot(10)[1] + 18
        giu = alto_nuovo - BOZ_ALTO
        box_piccola = scatola(SX, alto_nuovo, DX, basso_nuovo, col.terziario)
        dida_su = UP * px(BOZ_BASSO_FIN - basso_nuovo)
        cta_t = testo(self.scena["cta"].replace(" le mail", "\nle mail"), "etichetta", colore=col.sfondo, peso=BOLD)
        cta_f = RoundedRectangle(corner_radius=px(40), width=cta_t.width + px(72), height=cta_t.height + px(30), stroke_width=0,
                                 fill_color=col.accento, fill_opacity=1)
        cta = etichetta(VGroup(cta_f, cta_t.move_to(cta_f)))
        cta.move_to([X(SX) + cta.width / 2, a.y0 + cta.height / 2 + px(2), 0])
        linea = sottolinea(b.cuore_fin, b.f3_fin.righe[2], col.accento, spessore=7).shift(DOWN * px(3))
        tv.aggiungi(msg, cta, linea)
        tv.fine_6()
        applica(t_tinta(b.cuore_fin, col.testo))  # il messaggio porta l'accento del beat 0: la frase si riaccende nel beat 1
        op(VGroup(msg, cta, linea), 0)
        self.add(tv.mondo)
        self.annota("inizio")

        # beat 0 «All'IA chiedi i problemi, e le parole mettile tu.»: un passaggio (mail giù, messaggio su), poi il contatore
        via = VGroup(r, b.fin_barre, b.fin_data, b.barre(5))
        morbida = rate_functions.ease_in_out_cubic
        self.fai(1.0, t_op(via, 0, 0, 0.3), t_tinta(b.porto_fin, col.testo, 1, 0, 0.3), t_punti(b.box, box_piccola, 0.3, 0.7, morbida),
                 t_sposta(VGroup(b.ling_finale, c), DOWN * px(giu), 0.3, 0.7, morbida),
                 t_sposta(b.dida_finale, dida_su, 0.3, 0.7, morbida),
                 [t_entra(riga, 0.45 + 0.11 * j, 0.45 + 0.11 * j + 0.22, sposta=UP * px(24), rate=rate_functions.ease_out_cubic)
                  for j, riga in enumerate(msg.righe)])
        self.alle(max(self.t + 0.2, self.istante(0, "e le parole") - 0.15))
        # l'etichetta cambia a vista: la vecchia esce, la nuova entra al suo posto, e solo allora il valore si accende
        self.fai(1.0, t_esce(c.etich, 0, 0.3, sposta=LEFT * px(24), rate=rush_into), t_entra(c.etich7, 0.34, 0.62, sposta=RIGHT * px(24)),
                 c.t_valore("5", col.accento, 1, 0.5, 1))

        # beat 1 «Anche quelle che lei ti boccia.»: GRANDE (rivelazione a tratto), poi la CTA
        self.beat(1)
        self.fai(0.65, t_traccia(linea, 0, 0.85, rate_functions.ease_out_cubic), t_tinta(b.cuore_fin, col.accento, 1, 0.2, 1))
        self.fai(0.6, t_entra(cta, scala=0.85, sposta=UP * px(14), rate=rate_functions.ease_out_back))
