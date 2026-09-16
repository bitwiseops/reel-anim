"""Animazioni di «Generativa non vuol dire creativa» (contenuti/sceneggiature/2026-09-15-generativa-probabile.md).

Il filo visivo: pochi oggetti per tutto il reel, sempre con lo stesso aspetto.
- La carta «richiesta» (bordo secondario) è «quello che viene prima»: intera nell'hook (A2), compatta a pillola in
  alto a sinistra nelle scene 2-3, al centro con «Sii originale.» nella 4 (C2), al centro con la riga della
  fotocopiatrice nella 5 (D2), con la sola riga del dettaglio nella 6, stretta nel buco della linea fra l'IA e Marco
  nella 7 (revisione ⚠️ 31).
- Il biglietto (bordo terziario, cartellini su righe fisse): «Caro Marco, / finalmente potrai / spegnere la sveglia /
  senza sensi di colpa!» (A2-opus-5) nelle scene 1-3; nella 4 lo stesso riquadro con il vestito da verbale
  (C2-opus-3, senza le righe A2: ⚠️ 18); nella 5-6 il biglietto pulito con righe grigie e il P.S. in fondo
  (D2-opus-5, ⚠️ 23). Due volte si ferma sullo stesso gesto, con il cursore: «spegnere la ▌» e «Poi si è ▌».
- La colonna delle candidate (`Classifica`, larga 400 px, sotto la riga in scrittura): scena 3 e scena 6.
- L'etichetta «solo per Marco?» (il loop): in alto a destra dalla 2 alla 6, poi scende sul biglietto senza «?».

Cambi grandi: `punch` «SVEGLIA» (2), «INCEPPATA» (6), «TU SÌ» (7); zoom 1,6× nella 3 (colonna) e nella 4 (verbale).
Lo zoom non usa `zoom_su`: l'inquadratura è scelta a mano (`inquadra`) perché a zoom pieno ogni testo nel campo sia
intero o del tutto fuori (lezione del 2026-09-14): il bordo alto cade sopra la prima riga del biglietto (scena 3) o
sopra il suo titolo (scena 4), e le righe sono a capo entro la larghezza del campo.

Ogni scena parte dall'ultimo fotogramma della precedente, ricostruito con le stesse funzioni di impaginazione; le carte
si tengono a pezzi (riquadro, titolo, righe) con i riquadri sotto (z -1). Posizioni in px della tela (origine in alto
a sinistra) con `punto()`; area contenuto 60..960 × 220..1196 px (hook: 220..1580). Testi misurati solo dentro le
funzioni (il font si registra con la scena).
"""
from __future__ import annotations

import re

import numpy as np
from manim import (BOLD, DOWN, LEFT, RIGHT, UL, UP, Create, DashedLine, FadeIn, FadeOut, FadeTransform, Line,
                   MoveToTarget, Rectangle, RoundedRectangle, Transform, UpdateFromAlphaFunc, VGroup, linear, smooth,
                   squish_rate_func)

from tools.anim.base import ScenaReel, aree
from tools.anim.componenti import Classifica, Etichetta, Freccia, Icona, Messaggio, Titolo, Token, piano, testo, tratto
from tools.anim.config import carica
from tools.anim.diagrammi import Graffa
from tools.anim.misure import PX_PER_UNITA, px

CFG = carica()
P = CFG.palette

# --- testi del modello (Claude Opus 5, contenuti/media/generativa-probabile/biglietti-claude-2026-09-14.md) --------
RICHIESTA = "Un biglietto per la pensione di Marco. Lo firma tutto l'ufficio."          # A2
SII = "Sii originale."                                                                # C2 = A2 + questa riga
DETTAGLIO = "Marco ha passato una vita a litigare con la fotocopiatrice."             # D2 = A2 + questa riga
BIGLIETTO = [["Caro", "Marco,"], ["finalmente", "potrai"], ["spegnere", "la", "sveglia"],
             ["senza", "sensi", "di", "colpa!"]]                                      # A2-opus-5, «Versione spiritosa»
FRAMMENTI = [("«la sveglia spenta il lunedì mattina»", "sveglia"),                    # A2-opus-2
             ("«Adesso la sveglia la puoi spegnere.»", "sveglia"),                    # A2-opus-3
             ("«le mattine senza sveglia»", "sveglia"),                               # A2-opus-4
             ("«niente sveglie»", "sveglie")]                                         # A2-opus-1
VERBALE_TESTA = "VERBALE DELLA RIUNIONE STRAORDINARIA DELL'UFFICIO"                  # C2-opus-3 (e -1, -4)
VERBALE_RIGHE = ["– punta la sveglia solo quando vuole lui;",                          # C2-opus-3, Punto 3
                 "– non partecipa più alle riunioni che \"potevano essere una mail\"."]
PS = [["P.S.", "La", "fotocopiatrice", "ci"], ["ha", "chiesto", "di", "salutarti."],
      ["Poi", "si", "è", "inceppata."]]                                              # D2-opus-5, in fondo all'interno
DETTAGLIO_7 = "Marco ha passato\nuna vita a\nlitigare con la\nfotocopiatrice."        # a capo per il buco della linea
CANDIDATE_3 = [("sveglia", 0.58), ("luce", 0.21), ("televisione", 0.08)]              # dopo «spegnere la» (esempio)
CANDIDATE_6 = [("inceppata", 0.52), ("bloccata", 0.27), ("spenta", 0.09)]             # dopo «si è» (esempio)
# TITOLO/TESTO delle scene precedenti, per ricostruirne l'ultimo fotogramma (nella scena stessa: self.scena)
TITOLO_1 = "Generativa non vuol dire creativa"
TESTO_2 = ["5 su 5", "solo per Marco?"]
TESTO_3 = ["fluente", "di tutti"]
TESTO_4 = ["3 su 5"]
TESTO_6 = ["dopo la fotocopiatrice", "l'hai data tu"]

# --- misure (px della tela) --------------------------------------------------------------------------------------
X0, X1 = 60, 960       # bordi dell'area contenuto
LARGHEZZA = 900        # carte a tutta larghezza
PAD = 40               # margine interno delle carte (come Carta)
GAP = 16               # spazio fra i cartellini (come Frase)
ALTO = 232             # cima della pillola «richiesta» (e della fascia in alto)
Y_BIG = 390            # cima del biglietto nelle scene 2-5
Y_CENTRO = 542         # cima della carta al centro (scene 4-5)
Y_DET_6 = 370          # cima della carta col dettaglio mentre torna la colonna (scena 6)
Y_PS_6 = 590           # cima del biglietto P.S. alla fine della 6
SCALA_TITOLO = 0.6     # il titolo dell'hook dopo 0,5 s (104 px → 62 px: resta leggibile nella copertina)
LARG_VERBALE = 560     # a capo del verbale: sta intero nel campo dello zoom (675 px)
ZOOM = 1.6
PAUSA_FRASI_S = 0.3    # la voce di prova lascia 0,3 s fra le frasi e 0,5 s dopo l'ultima


def punto(x: float, y: float) -> np.ndarray:
    """Un punto della tela in px (origine in alto a sinistra) in unità Manim."""
    return np.array([px(x) - CFG.frame_width / 2, CFG.frame_height / 2 - px(y), 0.0])


def y_px(y: float) -> float:
    return (CFG.frame_height / 2 - y) * PX_PER_UNITA


def x_px(x: float) -> float:
    return (x + CFG.frame_width / 2) * PX_PER_UNITA


def alto_px(m) -> float:
    return y_px(m.get_top()[1])


def fondo_px(m) -> float:
    return y_px(m.get_bottom()[1])


def fuori(*mobs, **kw) -> list:
    """Un FadeOut per pezzo (un FadeOut di un VGroup nuovo lascerebbe in scena i pezzi, trasparenti)."""
    return [FadeOut(m, **kw) for m in mobs]


def dentro(*mobs, **kw) -> list:
    return [FadeIn(m, **kw) for m in mobs]


def dopo(a: float, b: float = 1.0):
    """Curva smooth compressa nella frazione [a, b] della play: più movimenti sfalsati in un solo passaggio."""
    return squish_rate_func(smooth, max(0.0, a), min(1.0, b))


def grande(scena: dict) -> str:
    """Il testo del cambio grande: «…» subito dopo «GRANDE:» in una riga ANIMAZIONE."""
    for s in scena.get("animazione") or []:
        m = re.search(r"GRANDE:\s*«(.+?)»", s)
        if m:
            return m.group(1)
    raise ValueError("nessuna riga ANIMAZIONE con «GRANDE: «…»»")


def riquadro(larghezza_px: float, altezza: float, colore: str, z: int = -1) -> RoundedRectangle:
    """Il riquadro di una carta, con lo stile di Carta, sotto ai testi."""
    return RoundedRectangle(corner_radius=px(28), width=px(larghezza_px), height=altezza, stroke_color=colore,
                            stroke_width=tratto(3), fill_color=P.sfondo, fill_opacity=1).set_z_index(z)


def inquadra(fattore: float, sinistra_px: float, alto: float) -> tuple[float, np.ndarray]:
    """Larghezza e centro della camera ingrandita `fattore` volte con l'angolo in alto a sinistra del campo in
    (sinistra_px, alto) px della tela: il bordo alto si sceglie fra due righe, così nessun testo resta tagliato."""
    return CFG.frame_width / fattore, punto(sinistra_px + CFG.larghezza / (2 * fattore),
                                            alto + CFG.altezza / (2 * fattore))


# --- cartellini e cursore ----------------------------------------------------------------------------------------

def acceso(t: Token) -> Token:
    t.box.set_stroke(P.accento, width=tratto(5))
    t.testo.set_color(P.accento)
    return t


def spento(t: Token) -> Token:
    t.box.set_stroke(P.attenuato, width=tratto(3))
    t.testo.set_color(P.testo)
    return t


def cursore() -> Rectangle:
    return Rectangle(width=px(8), height=px(56), stroke_width=0, fill_color=P.accento, fill_opacity=1)


def dopo_di(c: Rectangle, m, buff_px: float = 14) -> Rectangle:
    """Il cursore subito a destra di m, centrato in altezza su m."""
    return c.move_to([m.get_right()[0] + px(buff_px) + c.width / 2, m.get_center()[1], 0])


def prima_di(c: Rectangle, m, buff_px: float = 6) -> Rectangle:
    """Il cursore dove comincia m (una riga vuota): a sinistra del suo primo glifo."""
    return c.move_to([m.get_left()[0] - px(buff_px) + c.width / 2, m.get_center()[1], 0])


def lampeggio(periodo: float = 0.8):
    """Updater (con dt) che accende e spegne un oggetto: gira anche durante le attese, finché non si toglie."""
    stato = {"t": 0.0}

    def aggiorna(m, dt):
        stato["t"] += dt
        m.set_fill(opacity=1.0 if (stato["t"] % periodo) < 0.55 * periodo else 0.0)

    return aggiorna


def lampeggia(c: Rectangle) -> None:
    c.clear_updaters()
    c.set_fill(opacity=1)
    c.add_updater(lampeggio())


def fermo(c: Rectangle) -> None:
    c.clear_updaters()
    c.set_fill(opacity=1)


def parole(blocco) -> list[tuple[VGroup, object]]:
    """I glifi di ogni parola di un Blocco, in ordine, con la riga che li contiene (per il cursore)."""
    out = []
    for r in blocco.righe:
        i = 0
        for w in r.piano.split():
            out.append((VGroup(*r.glifi.submobjects[i:i + len(w)]), r))
            i += len(w)
    return out


# --- la carta «richiesta» e il biglietto, a pezzi ----------------------------------------------------------------

class Scheda:
    """La carta «richiesta» a pezzi (riquadro, titolo, righe) con l'angolo in alto a sinistra in (x_px, y_px). Le righe
    sono stringhe (corpo `ruolo`, colore da `colori`) o Blocchi già fatti."""

    def __init__(self, righe=(), y_px: float = ALTO, x_px: float = X0, larghezza_px: float = LARGHEZZA,
                 ruolo: str = "caption", colori=None):
        colori = list(colori or [None] * len(righe))
        self.titolo = testo("richiesta", "etichetta", colore=P.secondario, peso=BOLD)
        self.righe = [testo(r, ruolo, colore=c, larghezza_px=larghezza_px - 2 * PAD) if isinstance(r, str) else r
                      for r, c in zip(righe, colori)]
        corpo = VGroup(self.titolo, *self.righe).arrange(DOWN, buff=px(24), aligned_edge=LEFT)
        self.box = riquadro(larghezza_px, corpo.height + 2 * px(PAD), P.secondario)
        self.box.move_to(punto(x_px, y_px), aligned_edge=UL)
        corpo.move_to(self.box.get_corner(UL) + np.array([px(PAD), -px(PAD), 0]), aligned_edge=UL)

    def pezzi(self) -> list:
        return [self.box, self.titolo, *self.righe]

    @property
    def altezza_px(self) -> float:
        return self.box.height * PX_PER_UNITA


def pillola() -> Scheda:
    """La carta «richiesta» compatta: solo il titolo, in alto a sinistra."""
    return Scheda([], larghezza_px=testo("richiesta", "etichetta", peso=BOLD).width * PX_PER_UNITA + 2 * PAD)


def etichetta_loop(s: str, acceso_: bool = False) -> Etichetta:
    """«solo per Marco?» attenuata in alto a destra, centrata sulla pillola (acceso_: il «?» in accento)."""
    e = Etichetta(s[:-1] + "==?==" if acceso_ else s, colore=P.attenuato, pieno=False)
    pil = pillola()
    return e.move_to([punto(X1, 0)[0] - e.width / 2, pil.box.get_center()[1], 0])


class Biglietto:
    """Il biglietto A2: cartellini su righe fisse sotto il titolo «biglietto»; `box_per(k)` è il riquadro alto k
    righe (il biglietto cresce con la voce). I cartellini stanno negli stessi posti qualunque sia il riquadro."""

    def __init__(self, righe: list[list[str]], y_px: float, x_px: float = X0):
        self.y, self.x = y_px, x_px
        self.titolo = testo("biglietto", "etichetta", colore=P.terziario, peso=BOLD)
        self.titolo.move_to(punto(x_px + PAD, y_px + PAD), aligned_edge=UL)
        self.righe = [[Token(p) for p in r] for r in righe]
        self.file = [VGroup(*r).arrange(RIGHT, buff=px(GAP)) for r in self.righe]
        VGroup(*self.file).arrange(DOWN, buff=px(GAP), aligned_edge=LEFT).next_to(self.titolo, DOWN, buff=px(24),
                                                                                  aligned_edge=LEFT)
        self.box = self.box_per(len(righe))

    def box_per(self, k: int) -> RoundedRectangle:
        fondo = self.file[k - 1].get_bottom()[1] - px(PAD)
        return riquadro(LARGHEZZA, punto(0, self.y)[1] - fondo, P.terziario).move_to(punto(self.x, self.y),
                                                                                      aligned_edge=UL)

    def token(self, k: int | None = None) -> list[Token]:
        return [t for r in self.righe[:k] for t in r]


class BigliettoPS:
    """Il biglietto pulito (D2-opus-5): tre righe grigie senza parole (l'interno, che non mostriamo) e in fondo il P.S.
    a cartellini (revisione ⚠️ 23: «in fondo» si vede, e non sembra che il biglietto sia tutto lì)."""

    def __init__(self, y_px: float):
        self.titolo = testo("biglietto", "etichetta", colore=P.terziario, peso=BOLD)
        self.titolo.move_to(punto(X0 + PAD, y_px + PAD), aligned_edge=UL)
        self.barre = [RoundedRectangle(corner_radius=px(9), width=px(w), height=px(18), stroke_width=0,
                                       fill_color=P.attenuato, fill_opacity=0.35) for w in (800, 720, 560)]
        VGroup(*self.barre).arrange(DOWN, buff=px(40), aligned_edge=LEFT).next_to(self.titolo, DOWN, buff=px(30),
                                                                                  aligned_edge=LEFT)
        self.righe = [[Token(p) for p in r] for r in PS]
        self.file = [VGroup(*r).arrange(RIGHT, buff=px(GAP)) for r in self.righe]
        VGroup(*self.file).arrange(DOWN, buff=px(GAP), aligned_edge=LEFT).next_to(self.barre[-1], DOWN, buff=px(40),
                                                                                  aligned_edge=LEFT)
        fondo = self.file[-1].get_bottom()[1] - px(PAD)
        self.box = riquadro(LARGHEZZA, punto(0, y_px)[1] - fondo, P.terziario).move_to(punto(X0, y_px),
                                                                                       aligned_edge=UL)

    def token(self, k: int | None = None) -> list[Token]:
        return [t for r in self.righe[:k] for t in r]

    def pezzi(self) -> list:
        return [self.box, self.titolo, *self.barre, *self.token()]


class Verbale:
    """Il biglietto col vestito da verbale (C2-opus-3): lo stesso riquadro e lo stesso titolo del biglietto, dentro solo
    parole di C2-opus-3 (revisione ⚠️ 18). Le copie (C2-opus-1 e -4) hanno solo l'intestazione, rientrate e più in alto,
    dietro al verbale: si vede la loro intestazione, identica."""

    def __init__(self, y_px: float, righe: bool = False, copia: int = 0):
        self.copia = copia
        rientro = 30 * copia
        pezzi = []
        self.titolo = None
        if not copia:
            self.titolo = testo("biglietto", "etichetta", colore=P.terziario, peso=BOLD)
            pezzi.append(self.titolo)
        self.testa = testo(VERBALE_TESTA, "etichetta", peso=BOLD, larghezza_px=LARG_VERBALE)
        self.righe = [testo(r, "token", larghezza_px=LARG_VERBALE) for r in VERBALE_RIGHE] if righe else []
        corpo = VGroup(*pezzi, self.testa, *self.righe).arrange(DOWN, buff=px(24), aligned_edge=LEFT)
        z = -1 - 2 * copia
        self.box = riquadro(LARGHEZZA - 2 * rientro, corpo.height + 2 * px(PAD), P.terziario, z=z)
        self.box.move_to(punto(X0 + rientro, y_px), aligned_edge=UL)
        corpo.move_to(self.box.get_corner(UL) + np.array([px(PAD), -px(PAD), 0]), aligned_edge=UL)
        if copia:
            self.testa.set_z_index(z + 1)

    def pezzi(self) -> list:
        return [self.box, *([self.titolo] if self.titolo else []), self.testa, *self.righe]


def pezzi_biglietto(b: Biglietto, k: int) -> list:
    return [b.box_per(k), b.titolo, *b.token(k)]


# --- impaginazioni condivise fra una scena e la successiva --------------------------------------------------------

def disposizione_01(titolo_s: str):
    """Hook: il gruppo centrato nell'area dell'hook, sia al fotogramma 0 (titolo grande, biglietto di una riga) sia alla
    fine (titolo ridotto, biglietto di tre righe), così la copertina (ritaglio 4:5 dell'ultimo fotogramma) è intera.
    Ritorna il titolo, la carta e il biglietto nelle posizioni finali, la cima del titolo al fotogramma 0 e gli
    spostamenti (px) di carta e biglietto fra il fotogramma 0 e la fine."""
    area = aree(CFG, None).contenuto
    alto, basso = y_px(area.y1), y_px(area.y0)
    tit = Titolo(titolo_s)
    h_t = tit.height * PX_PER_UNITA
    r = Scheda([RICHIESTA])
    prova = Biglietto(BIGLIETTO, 0)
    h1, h3 = (prova.box_per(k).height * PX_PER_UNITA for k in (1, 3))
    y_f = alto + (basso - alto - (SCALA_TITOLO * h_t + 36 + r.altezza_px + 36 + h3)) / 2
    y_0 = alto + (basso - alto - (h_t + 40 + r.altezza_px + 40 + h1)) / 2
    tit.scale(SCALA_TITOLO).move_to(punto(X0, y_f), aligned_edge=UL)
    yc = y_f + SCALA_TITOLO * h_t + 36
    r = Scheda([RICHIESTA], y_px=yc)
    yb = yc + r.altezza_px + 36
    b = Biglietto(BIGLIETTO, yb)
    yc0 = y_0 + h_t + 40
    return tit, r, b, y_0, yc0 - yc, yc0 + r.altezza_px + 40 - yb


def frammenti_02(b: Biglietto):
    """I quattro frammenti delle altre risposte, attenuati con la sola «sveglia» in accento, sotto il biglietto; «5 su 5»
    accanto all'ultimo (il più corto)."""
    blocchi = []
    for s, w in FRAMMENTI:
        bl = testo(s, "token", colore=P.attenuato)
        bl.parola(w).set_color(P.accento)
        blocchi.append(bl)
    VGroup(*blocchi).arrange(DOWN, buff=px(18), aligned_edge=LEFT).move_to(
        punto(X0, fondo_px(b.box_per(4)) + 30), aligned_edge=UL)
    return blocchi


def etichette_03(b: Biglietto, testi: list[str]):
    fl = Etichetta(testi[0], colore=P.terziario)
    dt = Etichetta(testi[1])
    VGroup(fl, dt).arrange(RIGHT, buff=px(30)).move_to(punto(X0, fondo_px(b.box_per(4)) + 30), aligned_edge=UL)
    return fl, dt


def verbale_04():
    """Scena 4, beat 1: il verbale in basso e le due copie che spuntano dietro, più in alto; «3 su 5» sotto."""
    prova = Verbale(0)
    passo = prova.testa.height * PX_PER_UNITA + 2 * 24 + 8     # la striscia che spunta: tutta l'intestazione
    copie = [Verbale(Y_BIG + passo * (1 - k), copia=k + 1) for k in range(2)]   # copia 1 più vicina, copia 2 in cima
    fronte = Verbale(Y_BIG + 2 * passo)
    tre = Etichetta(TESTO_4[0], pieno=False).move_to(punto(X0, fondo_px(fronte.box) + 30), aligned_edge=UL)
    return copie, fronte, tre


def verbale_finale_04():
    """Ultimo fotogramma della 4: il verbale intero in alto, «sveglia» e «una mail» accese, «3 su 5» sotto."""
    v = Verbale(Y_BIG, righe=True)
    tre = Etichetta(TESTO_4[0], pieno=False).move_to(punto(X0, fondo_px(v.box) + 30), aligned_edge=UL)
    return v, tre


def sveglia_mail(v: Verbale):
    return v.righe[0].parola("sveglia"), v.righe[1].parola("una mail")


def carta_05(righe, colori=None) -> Scheda:
    return Scheda(righe, y_px=Y_CENTRO, colori=colori)


def graffa_06(r: Scheda, s: str) -> Graffa:
    """Graffa accento sotto la riga del dettaglio, nel margine basso della carta; l'etichetta appena sotto il bordo."""
    g = Graffa(r.righe[0], s, direzione=DOWN, colore=P.accento)
    g.shift(DOWN * (g.graffa.get_top()[1] - r.righe[0].get_bottom()[1] + px(4)))
    return g


def tag_06(s: str, colore: str, ps: BigliettoPS) -> Etichetta:
    """«solo per Marco» come un cartellino appeso all'angolo in alto a destra del biglietto."""
    e = Etichetta(s, colore=colore)
    return e.move_to([punto(X1 - 30, 0)[0] - e.width / 2, ps.box.get_top()[1], 0]).set_z_index(1)


def stato_finale_06():
    r = Scheda([DETTAGLIO])
    ps = BigliettoPS(Y_PS_6)
    g = graffa_06(r, TESTO_6[1])
    tag = tag_06(TESTO_2[1].rstrip("?"), P.terziario, ps)
    return r, ps, g, tag


# --- la classe base con i tempi delle parole ---------------------------------------------------------------------

def _sillabe(w: str) -> int:
    return max(1, len(re.findall(r"[aeiouàèéìíòóù]+", w.lower())))


def _pausa(w: str) -> float:
    return 2.0 if w.endswith((".", "?", "!", ":")) else 1.5 if w.endswith(",") else 0.0


class Scena(ScenaReel):
    """ScenaReel con i tempi delle singole parole (stimati a sillabe dentro la frase) e la scrittura a cartellini con
    il cursore che segue."""

    def parlato(self, i: int) -> float:
        coda = 0.5 if i == len(self.inizi_frasi) - 1 else PAUSA_FRASI_S
        return max(0.3, self.durata_beat(i) - coda)

    def tempi(self, i: int) -> list[float]:
        """Inizio stimato di ogni parola della frase i: la durata parlata divisa a sillabe, con una pausa dopo virgole e
        punti (con la voce di prova l'errore è di ~0,1 s)."""
        ps = piano(self.scena["voce"][i]).split()
        pesi = [_sillabe(p) + _pausa(p) for p in ps]
        tot = sum(pesi) - _pausa(ps[-1])
        t0, d = self.inizi_frasi[i], self.parlato(i)
        out, acc = [], 0.0
        for w in pesi:
            out.append(t0 + d * acc / tot)
            acc += w
        return out

    def limite(self, i: int) -> float:
        """Fin dove può arrivare un'animazione del beat i (l'inizio del beat dopo, o la fine della scena)."""
        n = len(self.inizi_frasi)
        return self.inizi_frasi[i + 1] - self.ANTICIPO_S if i + 1 < n else self.durata_s - 0.1

    def scrivi(self, coppie: list, cursore_: Rectangle | None = None, limite: float | None = None,
               extra: list | None = None) -> None:
        """I cartellini entrano uno alla volta, ognuno all'istante della sua parola (coppie = [(token, t)]), in una sola
        play; il cursore salta dopo l'ultimo entrato."""
        inizio = max(self.t, coppie[0][1] - 0.08)
        fine = coppie[-1][1] + 0.3
        if limite is not None:
            fine = min(fine, limite)
        run = self.arrotonda(max(fine - inizio, 0.3))
        self.attendi_fino(inizio)
        anims, soglie = [], []
        for tok, t in coppie:
            a = min(max(t - 0.08 - inizio, 0.0) / run, 0.9)
            anims.append(FadeIn(tok, shift=UP * 0.12, rate_func=dopo(a, min(1.0, a + 0.22 / run))))
            soglie.append(a + 0.11 / run)            # il cursore salta quando il cartellino è a metà
        if cursore_ is not None:
            fermo(cursore_)
            posti = [dopo_di(cursore_.copy(), tok).get_center() for tok, _ in coppie]
            da = cursore_.get_center().copy()

            def segui(m, a):
                k = max((j for j, s in enumerate(soglie) if a >= s), default=-1)
                m.move_to(posti[k] if k >= 0 else da)

            anims.append(UpdateFromAlphaFunc(cursore_, segui, rate_func=linear))
        self.play(*anims, *(extra or []), run_time=run)

    def scrivi_parole(self, blocco, tempi_: list[float], cursore_: Rectangle | None = None,
                      limite: float | None = None) -> None:
        """Le parole di una riga di carta compaiono una alla volta, agli istanti dati; il blocco è già in scena con i
        glifi trasparenti; il cursore segue."""
        ws = parole(blocco)
        inizio = max(self.t, tempi_[0] - 0.08)
        fine = tempi_[-1] + 0.3
        if limite is not None:
            fine = min(fine, limite)
        run = self.arrotonda(max(fine - inizio, 0.3))
        self.attendi_fino(inizio)
        finestre = [(min(max(t - 0.08 - inizio, 0.0) / run, 0.9), 0.18 / run) for t in tempi_]

        def f(m, a):
            for (g, _), (s, w) in zip(ws, finestre):
                g.set_fill(opacity=min(1.0, max(0.0, (a - s) / w)))

        anims = [UpdateFromAlphaFunc(blocco, f, rate_func=linear)]
        if cursore_ is not None:
            fermo(cursore_)
            posti = [np.array([g.get_right()[0] + px(10) + cursore_.width / 2, r.get_center()[1], 0]) for g, r in ws]
            da = cursore_.get_center().copy()

            def segui(m, a):
                k = max((j for j, (s, w) in enumerate(finestre) if a >= s + w / 2), default=-1)
                m.move_to(posti[k] if k >= 0 else da)

            anims.append(UpdateFromAlphaFunc(cursore_, segui, rate_func=linear))
        self.play(*anims, run_time=run)


# --- scene -------------------------------------------------------------------------------------------------------

class Scena01(Scena):
    """Hook: titolo, carta «richiesta» e biglietto con «Caro Marco, ▌» già al fotogramma 0; il titolo si riduce e la
    carta si accende mentre la voce la dice; il biglietto si scrive con la voce fino a «spegnere la ▌», e il cursore
    lampeggia fino alla fine (la prova)."""

    def costruisci(self):
        tit, r, b, y0, dc, db = disposizione_01(self.scena["titolo"])
        grande_ = Titolo(self.scena["titolo"]).move_to(punto(X0, y0), aligned_edge=UL)
        grande_.target = tit
        box = b.box_per(1)
        c = dopo_di(cursore(), b.righe[0][-1])
        pezzi_c, pezzi_b = r.pezzi(), [box, b.titolo, *b.righe[0], c]
        for m in pezzi_c:
            m.shift(DOWN * px(dc))
        for m in pezzi_b:
            m.shift(DOWN * px(db))
        self.add(grande_, *pezzi_c, *pezzi_b)            # fotogramma 0 pieno: la copertina di chi scorre
        self.play(MoveToTarget(grande_), *[m.animate.shift(UP * px(dc)) for m in pezzi_c],
                  *[m.animate.shift(UP * px(db)) for m in pezzi_b], run_time=0.5)
        lampeggia(c)
        t0 = self.tempi(0)                                # «Ho chiesto all'IA un biglietto per la pensione di Marco.»
        self.attendi_fino(t0[3] - 0.15)                   # «un biglietto…»: la carta si accende mentre la voce la dice
        self.play(r.box.animate.set_stroke(P.accento, width=tratto(5)), run_time=0.4)

        self.beat(1)                                      # «Finisci tu. Caro Marco, finalmente potrai spegnere la…»
        self.play(r.box.animate.set_stroke(P.secondario, width=tratto(3)), Transform(box, b.box_per(3)), run_time=0.4)
        lampeggia(c)
        t1 = self.tempi(1)
        toks = [*b.righe[1], *b.righe[2][:2]]             # finalmente, potrai, spegnere, la
        self.scrivi(list(zip(toks, t1[4:8])), c, limite=self.limite(1))
        lampeggia(c)                                      # «la ▌»: il vuoto della prova fino alla fine della scena


class Scena02(Scena):
    """«SVEGLIA» a tutto schermo; al ritorno la parola è nel biglietto e la riga si completa; i quattro frammenti delle
    altre risposte, «5 su 5»; poi «solo per Marco?» in alto a destra (il loop)."""

    def costruisci(self):
        tit, r, b, *_ = disposizione_01(TITOLO_1)          # ultimo fotogramma dell'hook, con «sveglia» già al suo posto
        box = b.box_per(3)
        # lo stesso gruppo, alzato fino alla fascia in alto: nell'hook arriva a ~1380 px, e qui c'è il presentatore (il
        # cerchio coprirebbe «sveglia» proprio al ritorno). Lo spostamento lo nasconde il taglio del punch
        alza = alto_px(tit) - ALTO
        for m in [tit, *r.pezzi(), box, b.titolo, *b.token()]:
            m.shift(UP * px(alza))
        sv = acceso(b.righe[2][2])
        self.add(tit, *r.pezzi(), box, b.titolo, *b.token(3))
        self.punch(grande(self.scena))                    # il ritorno è un taglio: «sveglia» compare dove c'era il cursore

        # dopo il punch (con «L'hai finita tu, proprio come lei.»): via il titolo, la carta si compatta in alto a
        # sinistra, il biglietto sale al suo posto delle scene 2-5 e la riga si completa
        pil = pillola()
        b2 = Biglietto(BIGLIETTO, Y_BIG)
        su = UP * px(b.y - alza - Y_BIG)
        r4 = b2.righe[3]
        self.play(FadeOut(tit, shift=UP * 0.3, rate_func=dopo(0, 0.45)),
                  Transform(r.box, pil.box, rate_func=dopo(0.1, 0.7)), Transform(r.titolo, pil.titolo, rate_func=dopo(0.1, 0.7)),
                  FadeOut(r.righe[0], rate_func=dopo(0, 0.35)),
                  Transform(box, b2.box_per(4), rate_func=dopo(0.1, 0.7)),
                  *[m.animate(rate_func=dopo(0.1, 0.7)).shift(su) for m in [b.titolo, *b.token(3)]],
                  *[FadeIn(t, shift=UP * 0.12, rate_func=dopo(0.55 + 0.1 * k, 0.8 + 0.1 * k)) for k, t in enumerate(r4)],
                  run_time=1.0)

        # beat 1: i frammenti, uno alla volta; «5 su 5» su «tutte e cinque»
        self.beat(1)
        t1, lim = self.tempi(1), self.limite(1)
        fr = frammenti_02(b2)
        cinque = Etichetta(self.scena["testo"][0], pieno=False)
        cinque.next_to(fr[-1], RIGHT, buff=px(40))
        self.play(*[FadeIn(f, shift=LEFT * 0.3, rate_func=dopo(0.25 * k, 0.25 * k + 0.3)) for k, f in enumerate(fr)],
                  run_time=self.arrotonda(min(2.0, 0.55 * self.durata_beat(1))))
        self.attendi_fino(min(t1[8] - 0.15, lim - 0.4))   # «tutte e cinque»
        self.play(cinque.entra(), run_time=0.3)

        # beat 2: i frammenti escono, «sveglia» torna normale; «solo per Marco?» con il «?» in accento, poi attenuato
        self.beat(2)
        t2 = self.tempi(2)
        loop = etichetta_loop(self.scena["testo"][1], acceso_=True)
        self.play(*fuori(*fr, cinque, shift=DOWN * 0.2), sv.box.animate.set_stroke(P.attenuato, width=tratto(3)),
                  sv.testo.animate.set_color(P.testo), run_time=0.4)
        self.attendi_fino(t2[7] - 0.2)                    # «solo per Marco?»
        self.play(loop.entra(), run_time=0.4)
        self.attendi_fino(min(t2[11], self.limite(2) - 0.5))   # «ma non basta chiederglielo»
        self.play(loop.testo.parola("?").animate.set_color(P.attenuato), run_time=0.4)


class Scena03(Scena):
    """Una parola alla volta: il biglietto si svuota e si ricompone fino a «spegnere la ▌»; sotto la colonna delle
    candidate; zoom sulla colonna, «sveglia» vola nel posto del cursore; il biglietto intero, «fluente», «di tutti»."""

    def costruisci(self):
        pil = pillola()                                    # ultimo fotogramma della 2
        loop = etichetta_loop(TESTO_2[1])
        b = Biglietto(BIGLIETTO, Y_BIG)
        box = b.box_per(4)
        self.add(*pil.pezzi(), loop, box, b.titolo, *b.token())

        # beat 0: il biglietto si svuota; la frase si ricompone con la voce, un cartellino alla volta, e il cursore la segue
        b2 = Biglietto(BIGLIETTO, Y_BIG)
        c = prima_di(cursore(), b2.righe[0][0].testo)
        self.play(*fuori(box, b.titolo, *b.token(), shift=DOWN * 0.1), FadeIn(c, rate_func=dopo(0.6, 1)), run_time=0.4)
        t0 = self.tempi(0)                                 # «Guarda, quando genera, scrive una parola alla volta,»
        toks = [*b2.righe[0], *b2.righe[1], *b2.righe[2][:2]]
        self.scrivi(list(zip(toks, t0[1:7])), c, limite=self.limite(0))
        lampeggia(c)

        # beat 1: la colonna sotto il cursore; zoom (GRANDE) sulla colonna; «sveglia» si accende e vola nel posto del
        # cursore; la camera torna prima del beat dopo
        self.beat(1)
        cl = Classifica(CANDIDATE_3, larghezza_px=400)
        cl.move_to(punto(X0 + PAD, fondo_px(b2.file[2]) + 36), aligned_edge=UL)
        self.play(cl.entra(), run_time=0.7)
        larghezza, centro = inquadra(ZOOM, 56, 445)       # campo 675 × 1200 px: da «Caro Marco,» alla nota, testi interi;
        # «finalmente potrai» e il cursore sotto i 220 px dell'interfaccia, la nota sopra il presentatore
        self.play(self.camera.frame.animate.set(width=larghezza).move_to(centro), run_time=0.5)
        fine = self.limite(1)
        self.attendi_fino(fine - 1.15)
        self.play(cl.scegli(0), run_time=0.3)
        sv = cl.token(0, colore=P.accento)
        fermo(c)
        self.play(sv.animate.move_to(b2.righe[2][2]), FadeOut(c, rate_func=dopo(0.6, 1)), run_time=0.45)
        self.play(self.torna(), run_time=self.arrotonda(max(0.2, fine - self.t)))

        # beat 2: il biglietto intero; «fluente» e poi «di tutti»
        self.beat(2)
        t2 = self.tempi(2)                                 # «Per questo il testo viene fluente, e per questo è il biglietto di tutti.»
        fl, dt = etichette_03(b2, self.scena["testo"])
        self.play(FadeOut(cl, rate_func=dopo(0, 0.5)), FadeIn(b2.box_per(4), rate_func=dopo(0.2, 0.8)),
                  FadeIn(b2.titolo, rate_func=dopo(0.2, 0.8)),
                  *[FadeIn(t, shift=UP * 0.12, rate_func=dopo(0.4 + 0.1 * k, 0.7 + 0.1 * k)) for k, t in enumerate(b2.righe[3])],
                  sv.box.animate(rate_func=dopo(0.3, 0.8)).set_stroke(P.attenuato, width=tratto(3)), run_time=0.8)
        self.attendi_fino(t2[5] - 0.2)                     # «fluente»
        self.play(fl.entra(), run_time=0.35)
        self.attendi_fino(min(t2[12] - 0.2, self.limite(2) - 0.5))   # «di tutti»
        self.play(dt.entra(), run_time=0.35)


class Scena04(Scena):
    """«Sii originale.»: la carta scende al centro e riceve la riga (C2); il biglietto torna col vestito da verbale,
    tre intestazioni identiche, «3 su 5»; zoom sul verbale: dentro ci sono ancora «sveglia» e «una mail»."""

    def costruisci(self):
        pil = pillola()                                    # ultimo fotogramma della 3
        loop = etichetta_loop(TESTO_2[1])
        b = Biglietto(BIGLIETTO, Y_BIG)
        fl, dt = etichette_03(b, TESTO_3)
        vecchi = [b.box_per(4), b.titolo, *b.token(), fl, dt]
        self.add(*pil.pezzi(), loop, *vecchi)

        # beat 0 («E se aggiungi «sii originale»?»): il biglietto esce, la carta scende al centro intera (A2); su «sii
        # originale» la carta cresce e ci entra la riga, in accento (C2)
        a2 = carta_05([RICHIESTA])
        c2 = carta_05([RICHIESTA, SII], colori=[None, P.accento])
        self.play(*fuori(*vecchi, shift=DOWN * 0.2, rate_func=dopo(0, 0.45)),
                  Transform(pil.box, a2.box, rate_func=dopo(0.1, 0.7)), Transform(pil.titolo, a2.titolo, rate_func=dopo(0.1, 0.7)),
                  FadeIn(a2.righe[0], shift=UP * 0.15, rate_func=dopo(0.4, 1.0)), run_time=0.8)
        t0 = self.tempi(0)
        self.attendi_fino(min(t0[3] - 0.1, self.limite(0) - 0.45))   # «sii originale»
        self.play(Transform(pil.box, c2.box), FadeIn(c2.righe[1], shift=UP * 0.15, rate_func=dopo(0.3, 1.0)), run_time=0.45)

        # beat 1 («Tre volte su cinque mi ha fatto un verbale.»): la carta torna compatta; il biglietto torna col vestito da
        # verbale (le righe A2 sono già uscite: sotto l'intestazione solo parole di C2-opus-3); dietro scivolano due copie
        # con la stessa intestazione; «3 su 5»
        self.beat(1)
        pil2 = pillola()
        copie, fronte, tre = verbale_04()
        self.play(Transform(pil.box, pil2.box, rate_func=dopo(0, 0.6)), Transform(pil.titolo, pil2.titolo, rate_func=dopo(0, 0.6)),
                  *fuori(a2.righe[0], c2.righe[1], rate_func=dopo(0, 0.4)),
                  *dentro(*fronte.pezzi(), shift=UP * 0.2, rate_func=dopo(0.35, 1.0)), run_time=0.7)
        # le copie partono nascoste dietro il verbale (più basse e più strette) e scivolano su senza dissolvenza: in
        # dissolvenza l'intestazione di una si vedeva attraverso il riquadro semitrasparente dell'altra
        salite = [UP * (v.box.get_top()[1] - fronte.box.get_top()[1]) for v in copie]
        for v, d in zip(copie, salite):
            for m in v.pezzi():
                m.shift(-d)
        self.add(*[m for v in copie for m in v.pezzi()])
        self.play(*[m.animate.shift(d) for v, d in zip(copie, salite) for m in v.pezzi()], run_time=0.6)
        self.play(tre.entra(), run_time=0.3)

        # beat 2 («Ma dentro ci sono ancora la sveglia e le riunioni che potevano essere una mail.»): le copie escono, il
        # verbale sale e riceve le due righe del Punto 3; zoom (GRANDE): si accende «sveglia», poi «una mail»; torna
        self.beat(2)
        t2, fine = self.tempi(2), self.durata_s - 0.1
        v, tre2 = verbale_finale_04()
        self.play(*fuori(*[m for c in copie for m in c.pezzi()], shift=UP * 0.2, rate_func=dopo(0, 0.4)),
                  Transform(fronte.box, v.box, rate_func=dopo(0.05, 0.6)),
                  fronte.titolo.animate(rate_func=dopo(0.05, 0.6)).move_to(v.titolo),
                  fronte.testa.animate(rate_func=dopo(0.05, 0.6)).move_to(v.testa),
                  tre.animate(rate_func=dopo(0.05, 0.6)).move_to(tre2),
                  *[FadeIn(rg, shift=UP * 0.12, rate_func=dopo(0.5 + 0.15 * k, 0.85 + 0.15 * k)) for k, rg in enumerate(v.righe)],
                  run_time=0.7)
        larghezza, centro = inquadra(ZOOM, 56, 356)       # campo 675 × 1200 px: dal titolo del verbale a «3 su 5»; la
        # fascia in alto (pillola ed etichetta) resta fuori, l'intestazione sotto i 220 px dell'interfaccia
        self.play(self.camera.frame.animate.set(width=larghezza).move_to(centro), run_time=0.5)
        sveglia, mail = sveglia_mail(v)
        self.attendi_fino(min(t2[6] - 0.15, fine - 2.2))  # «la sveglia»
        self.play(sveglia.animate.set_color(P.accento), run_time=0.3)
        self.attendi_fino(min(t2[13] - 0.15, fine - 1.0))  # «una mail»
        self.play(mail.animate.set_color(P.accento), run_time=0.3)
        self.attendi_fino(max(self.t, min(t2[13] + 0.3, fine - 0.55)))
        self.play(self.torna(), run_time=self.arrotonda(max(0.3, min(0.5, fine - self.t))))


class Scena05(Scena):
    """«Sii originale.» scivola fuori dalla carta (senza barratura) e resta una riga vuota col cursore; la riga della
    fotocopiatrice si scrive con la voce (D2); sotto il biglietto pulito, il P.S. in fondo si scrive con la voce, fino
    a «Poi si è ▌» (la seconda prova)."""

    def costruisci(self):
        pil = pillola()                                    # ultimo fotogramma della 4
        loop = etichetta_loop(TESTO_2[1])
        v, tre = verbale_finale_04()
        for p in sveglia_mail(v):
            p.set_color(P.accento)
        self.add(*pil.pezzi(), loop, *v.pezzi(), tre)

        # beat 0 («Quello che le manca è una cosa che sai solo tu.»): la carta torna al centro con «Sii originale.»; la
        # riga scivola fuori e al suo posto resta una riga vuota col cursore; «che sai solo tu»
        c2 = carta_05([RICHIESTA, SII])
        d2 = carta_05([RICHIESTA, DETTAGLIO], colori=[None, P.accento])
        det = d2.righe[1]
        det.glifi.set_fill(opacity=0)
        c = prima_di(cursore(), det.righe[0].glifi)
        solo = Etichetta(self.scena["testo"][0]).move_to(punto(X0, fondo_px(d2.box) + 30), aligned_edge=UL)
        self.play(*fuori(*v.pezzi(), tre, shift=DOWN * 0.2, rate_func=dopo(0, 0.45)),
                  Transform(pil.box, c2.box, rate_func=dopo(0.1, 0.7)), Transform(pil.titolo, c2.titolo, rate_func=dopo(0.1, 0.7)),
                  FadeIn(c2.righe[0], shift=UP * 0.15, rate_func=dopo(0.35, 0.8)),
                  FadeIn(c2.righe[1], shift=UP * 0.15, rate_func=dopo(0.45, 0.9)), run_time=0.8)
        self.play(FadeOut(c2.righe[1], shift=RIGHT * 0.8, rate_func=dopo(0, 0.6)),
                  Transform(pil.box, d2.box, rate_func=dopo(0.35, 1.0)), FadeIn(c, rate_func=dopo(0.7, 1.0)), run_time=0.6)
        self.add(det)
        lampeggia(c)
        t0 = self.tempi(0)
        self.attendi_fino(min(t0[9] - 0.15, self.limite(0) - 0.4))   # «solo tu» (parola 9 di «Quello che le manca è…»)
        self.play(solo.entra(), run_time=0.35)

        # beat 1 («Tipo che Marco ha passato una vita a litigare con la fotocopiatrice.»): la riga si scrive con la voce
        self.beat(1)
        t1 = self.tempi(1)
        solo2 = Etichetta(self.scena["testo"][0], colore=P.attenuato, pieno=False).move_to(solo)
        self.play(Transform(solo, solo2), run_time=0.3)
        self.scrivi_parole(det, t1[2:], c, limite=self.limite(1))
        fermo(c)

        # beat 2 («E in fondo al biglietto scrive: la fotocopiatrice ci ha chiesto di salutarti.»): la carta si compatta
        # in alto; sotto il biglietto pulito, e il P.S. in fondo si scrive con la voce
        self.beat(2)
        t2 = self.tempi(2)
        pil2 = pillola()
        ps = BigliettoPS(Y_BIG)
        c_ps = prima_di(cursore(), ps.righe[0][0].testo)
        self.play(Transform(pil.box, pil2.box, rate_func=dopo(0, 0.6)), Transform(pil.titolo, pil2.titolo, rate_func=dopo(0, 0.6)),
                  *fuori(c2.righe[0], det, solo, c, rate_func=dopo(0, 0.4)),
                  *dentro(ps.box, ps.titolo, *ps.barre, shift=UP * 0.2, rate_func=dopo(0.35, 1.0)),
                  FadeIn(c_ps, rate_func=dopo(0.7, 1.0)), run_time=0.8)
        c = c_ps
        lampeggia(c)
        toks = ps.token(2)                                 # P.S., La, fotocopiatrice, ci / ha, chiesto, di, salutarti.
        istanti = [t2[6] - 0.25] + t2[6:13]
        self.scrivi(list(zip(toks, istanti)), c, limite=self.limite(2))

        # beat 3 («Poi si è…»): «Poi», «si», «è»; il cursore lampeggia fino alla fine
        self.beat(3)
        t3 = self.tempi(3)
        self.scrivi(list(zip(ps.righe[2][:3], t3[:3])), c, limite=self.limite(3))
        lampeggia(c)


class Scena06(Scena):
    """«INCEPPATA» a tutto schermo; al ritorno la parola è nel biglietto. La carta mostra la riga del dettaglio, torna
    la colonna delle candidate dopo «si è» e la freccia da «fotocopiatrice»; poi il biglietto intero, «solo per
    Marco» senza «?» sul biglietto e la graffa «l'hai data tu» (con «inceppata» già normale: ⚠️ 28)."""

    def costruisci(self):
        pil = pillola()                                    # ultimo fotogramma della 5, con «inceppata.» al posto del cursore
        loop = etichetta_loop(TESTO_2[1])
        ps = BigliettoPS(Y_BIG)
        inc = acceso(ps.righe[2][3])
        self.add(*pil.pezzi(), loop, *ps.pezzi())
        self.punch(grande(self.scena))

        # beat 1 («È ancora una parola probabile, ma probabile dopo la fotocopiatrice.»): del biglietto resta la riga
        # «Poi si è inceppata.» (di nuovo normale); la carta scende e mostra la riga del dettaglio; sotto la riga torna la
        # colonna; su «dopo la fotocopiatrice» la freccia dalla parola nella carta all'intestazione della colonna
        self.beat(1)
        t1 = self.tempi(1)
        det = Scheda([DETTAGLIO], y_px=Y_DET_6)
        riga3 = ps.righe[2]
        y_riga = Y_DET_6 + det.altezza_px + 30
        su = UP * px(alto_px(ps.file[2]) - y_riga)
        inc.generate_target()
        spento(inc.target).shift(su)
        self.play(*fuori(ps.box, ps.titolo, *ps.barre, *ps.token(2), rate_func=dopo(0, 0.4)),
                  *[t.animate(rate_func=dopo(0.15, 0.75)).shift(su) for t in riga3[:3]],
                  MoveToTarget(inc, rate_func=dopo(0.15, 0.75)),
                  Transform(pil.box, det.box, rate_func=dopo(0.3, 0.85)), Transform(pil.titolo, det.titolo, rate_func=dopo(0.3, 0.85)),
                  FadeIn(det.righe[0], shift=UP * 0.15, rate_func=dopo(0.5, 1.0)), run_time=0.9)
        cl = Classifica(CANDIDATE_6, larghezza_px=400)
        cl.move_to(punto(X0 + PAD, y_riga + 80 + 40), aligned_edge=UL)
        self.play(cl.entra(), run_time=0.8)
        parola = det.righe[0].parola("fotocopiatrice")
        fine_riga = x_px(inc.get_right()[0])
        x_f = min(x_px(parola.get_right()[0]) - 16, max(x_px(parola.get_left()[0]) + 30, fine_riga + 50))
        testa = testo(self.scena["testo"][0].replace(" la ", " la\n", 1), "etichetta", colore=P.accento, peso=BOLD)
        testa.move_to(punto(x_f - 60, alto_px(cl)), aligned_edge=UL)
        freccia = Freccia([punto(x_f, 0)[0], parola.get_bottom()[1] - px(10), 0],
                          [punto(x_f, 0)[0], testa.get_top()[1] + px(4), 0], colore=P.accento)
        self.attendi_fino(min(t1[7] - 0.25, self.limite(1) - 0.7))   # «dopo la fotocopiatrice»
        self.play(freccia.entra(), FadeIn(testa, rate_func=dopo(0.4, 1.0)), run_time=0.6)

        # beat 2 («Ecco una frase che vale solo per Marco, e la riga gliel'hai data tu.»): la colonna esce; la carta
        # torna in alto, il biglietto intero sotto, e l'etichetta del loop scende sul suo angolo; su «solo per Marco»
        # perde il «?» e si accende; su «gliel'hai data tu» la graffa (l'accento passa lì, l'etichetta diventa terziaria)
        self.beat(2)
        t2 = self.tempi(2)
        r6, ps6, g, tag_fin = stato_finale_06()
        tag = tag_06(TESTO_2[1].rstrip("?"), P.accento, ps6)
        giu = DOWN * px(alto_px(ps6.file[2]) - y_riga)
        su_carta = UP * px(Y_DET_6 - ALTO)
        loop.generate_target()
        loop.target.move_to([punto(X1 - 30, 0)[0] - loop.width / 2, ps6.box.get_top()[1], 0])
        loop.set_z_index(1)
        self.play(*fuori(cl, testa, freccia, rate_func=dopo(0, 0.4)),
                  *[m.animate(rate_func=dopo(0.2, 0.8)).shift(su_carta) for m in (pil.box, pil.titolo, det.righe[0])],
                  *[t.animate(rate_func=dopo(0.2, 0.8)).shift(giu) for t in riga3],
                  *dentro(ps6.box, ps6.titolo, *ps6.barre, *ps6.token(2), rate_func=dopo(0.45, 1.0)),
                  MoveToTarget(loop, rate_func=dopo(0.25, 0.85)), run_time=0.9)
        self.attendi_fino(min(t2[5] - 0.2, self.limite(2) - 1.8))   # «solo per Marco»
        self.play(FadeTransform(loop, tag), run_time=0.5)
        self.attendi_fino(min(t2[11] - 0.25, self.limite(2) - 0.7))  # «gliel'hai data tu»
        self.play(g.entra(), tag.box.animate.set_fill(P.terziario).set_stroke(P.terziario), run_time=0.6)


class Scena07(Scena):
    """Chiusura, un passaggio per frase: l'IA e Marco con la linea interrotta e il messaggio; «TU SÌ»; la linea dal
    presentatore a Marco e la carta «richiesta» nel buco della linea, con la riga della fotocopiatrice (⚠️ 31); il
    diagramma esce con calma, messaggio e CTA al centro, sotto il biglietto «Caro Marco, ▌» dell'hook (per il replay)."""

    def costruisci(self):
        r6, ps6, g6, tag6 = stato_finale_06()               # ultimo fotogramma della 6
        vecchi = [*r6.pezzi(), *ps6.pezzi(), g6, tag6]
        self.add(*vecchi)

        a = self.area.contenuto
        msg = Messaggio(self.scena["messaggio"].replace(". ", ".\n", 1), maiuscolo=False)   # «Tu sì.» su una riga sua
        msg.move_to(punto(X0, ALTO), aligned_edge=UL)
        righe = msg.righe
        y_c = (fondo_px(msg) + 40 + y_px(a.y0)) / 2        # centro del diagramma, sotto il messaggio
        bot = Icona("bot", altezza_px=110, colore=P.testo)
        user = Icona("user", altezza_px=110, colore=P.testo)
        ia = testo("IA", "token", colore=P.attenuato)
        marco = testo("Marco", "token")
        sx = VGroup(bot, ia).arrange(DOWN, buff=px(18))
        dx = VGroup(user, marco).arrange(DOWN, buff=px(18))
        y = punto(0, y_c)[1]
        sx.move_to([punto(X0, 0)[0] + sx.width / 2, y - (bot.get_center()[1] - sx.get_center()[1]), 0])
        dx.move_to([punto(X1, 0)[0] - dx.width / 2, y - (user.get_center()[1] - dx.get_center()[1]), 0])
        pa, pb = bot.get_right() + RIGHT * px(22), user.get_left() + LEFT * px(22)
        cx = (pa[0] + pb[0]) / 2
        riga = testo(DETTAGLIO_7, "token", colore=P.accento)
        carta = Scheda([riga], y_px=0, ruolo="token", larghezza_px=riga.width * PX_PER_UNITA + 2 * PAD)
        spostamento = np.array([cx, y, 0]) - carta.box.get_center()
        for m in carta.pezzi():
            m.shift(spostamento)
        buco = carta.box.width / 2
        stile = dict(dash_length=px(18), stroke_color=P.attenuato, stroke_width=tratto(4))
        seg_sx = DashedLine(pa, [cx - buco, y, 0], **stile).set_z_index(-2)
        seg_dx = DashedLine(pb, [cx + buco, y, 0], **stile).set_z_index(-2)

        # beat 0 («L'IA non ha mai conosciuto Marco.»), un passaggio: esce tutto; il messaggio, l'IA e Marco, fra loro la
        # linea tratteggiata interrotta (le icone in dissolvenza: Create con curva sfalsata le disegna a puntini)
        self.play(*fuori(*vecchi, shift=DOWN * 0.2, rate_func=dopo(0, 0.45)),
                  FadeIn(righe[0], shift=UP * 0.2, rate_func=dopo(0.3, 0.75)),
                  FadeIn(righe[1], shift=UP * 0.2, rate_func=dopo(0.42, 0.87)),
                  FadeIn(bot, scale=0.9, rate_func=dopo(0.35, 0.9)), FadeIn(ia, rate_func=dopo(0.45, 0.9)),
                  FadeIn(user, scale=0.9, rate_func=dopo(0.45, 1.0)), FadeIn(marco, rate_func=dopo(0.55, 1.0)),
                  Create(seg_sx, rate_func=dopo(0.5, 1.0)), Create(seg_dx, rate_func=dopo(0.5, 1.0)), run_time=1.0)

        # beat 1, il cambio grande; al ritorno il messaggio ha anche «Tu sì.»
        self.beat(1)
        self.add(righe[2])
        self.punch(grande(self.scena))

        # beat 2 («Quindi diglielo tu, nella richiesta.»), un passaggio: la linea accento dal presentatore a Marco; la carta
        # «richiesta» entra nel buco della linea e ci scivola, da Marco, la riga della fotocopiatrice (l'IA arriva a Marco
        # solo da quello che scrivi). Agganciato all'inizio del beat: la riga deve restare intera ≥ 1 s (U4)
        self.beat(2)
        riq = self.area.riquadro
        fine = marco.get_bottom() + DOWN * px(14)
        verso = (fine - riq.centro) / np.linalg.norm(fine - riq.centro)
        linea = Line(riq.centro + verso * (riq.larghezza / 2 + px(18)), fine, stroke_color=P.accento,
                     stroke_width=tratto(6))
        self.play(Create(linea, rate_func=dopo(0, 0.5)), FadeIn(carta.box, scale=0.9, rate_func=dopo(0.1, 0.55)),
                  FadeIn(carta.titolo, rate_func=dopo(0.15, 0.6)), FadeIn(riga, shift=LEFT * 0.4, rate_func=dopo(0.4, 1.0)),
                  run_time=0.8)
        riga_intera = self.t

        # beat 3 («E salutami la fotocopiatrice.»), un passaggio: il diagramma esce, messaggio e CTA al centro, sotto il
        # biglietto dell'hook con «Caro Marco, ▌»; poi l'ultimo fotogramma fermo (il cursore lampeggia) fino alla fine
        self.beat(3)
        t3 = self.t
        diagramma = [bot, ia, user, marco, seg_sx, seg_dx, linea, carta.box, carta.titolo, riga]
        cta = Etichetta(self.scena["cta"])
        prova = Biglietto(BIGLIETTO, 0)
        h_b = prova.box_per(1).height * PX_PER_UNITA
        tot = msg.height * PX_PER_UNITA + 44 + cta.height * PX_PER_UNITA + 60 + h_b
        y_m = y_px(a.y1) + (a.altezza * PX_PER_UNITA - tot) / 2
        dy = px(y_m - ALTO)
        cta.move_to(punto(X0, y_m + msg.height * PX_PER_UNITA + 44), aligned_edge=UL)
        b = Biglietto(BIGLIETTO, fondo_px(cta) + 60)
        c = dopo_di(cursore(), b.righe[0][-1])
        self.attendi_fino(max(t3 + 0.1, riga_intera + 1.05))   # U4: la riga intera ≥ 1 s, anche con un beat 2 corto
        self.play(*fuori(*diagramma, shift=DOWN * 0.2, rate_func=dopo(0, 0.55)),
                  *[rg.animate(rate_func=dopo(0.1, 0.8)).shift(DOWN * dy) for rg in righe],
                  FadeIn(cta, shift=UP * 0.2, rate_func=dopo(0.4, 0.9)),
                  *dentro(b.box_per(1), b.titolo, *b.righe[0], c, shift=UP * 0.2, rate_func=dopo(0.5, 1.0)), run_time=1.1)
        lampeggia(c)
