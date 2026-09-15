"""Animazioni di «Generativa non vuol dire creativa» (contenuti/sceneggiature/2026-09-13-generativa-non-creativa.md).

Il filo visivo: tre oggetti per tutto il reel, sempre con lo stesso aspetto.
- La carta «richiesta» (bordo secondario) è «quello che viene prima»: intera nella scena 2, compatta (solo il
  titolo) in alto nelle scene 3-4 e 6, di nuovo intera e più lunga nella 5, con la sola riga del dettaglio alla fine
  della 6; nella 7 entra, stretta, nel buco della linea fra l'IA e Marco.
- Il biglietto: cartellini su righe fisse; dentro la carta «biglietto» (bordo terziario) quando è intero (scene 2,
  4 dal beat 1, 6), cartellini senza carta mentre si guarda come si scrive (scene 3-4). I due biglietti sono uscite
  vere di Claude Opus 5 (tagli nelle note di produzione). Il biglietto nuovo della 6 cresce con la voce (2 righe, poi
  5); dal 2026-09-14 non torna più nella 7.
- La colonna delle candidate: `Classifica` con la nota «esempio: numeri inventati» (scene 3 e 5; nella 6 «sono»
  parte dalla sua testa).

Cambi grandi: la battuta a tutto schermo (`punch`) nella 6 («PER DISPETTO.») e nella 7 («TU SÌ»), dopo
`oltre_inizio` (difetto di `punch` nella libreria). Lo zoom di camera nella 2 (sul cursore) è stato tolto dopo
l'anteprima del 2026-09-13: a 2× tagliava le parole della richiesta ai bordi. Chiusura calma (2026-09-14): un solo
passaggio per frase, con i movimenti sfalsati dentro la stessa play (`dopo`, `finestre`).

Ogni scena parte dall'ultimo fotogramma della precedente, ricostruito con le stesse funzioni di impaginazione
(`disposizione_NN`, `stato_finale_NN`): la dissolvenza fra le scene non si vede e gli oggetti non saltano.
Le carte si tengono a pezzi (riquadro, titolo, righe) e non si aggiungono mai come gruppo: così si compattano e
crescono con dei Transform senza che Manim ridisegni pezzi già usciti. I riquadri stanno sotto a tutto
(z_index -1): un biglietto che torna attorno a cartellini già in scena non li copre.
Posizioni in px della tela (origine in alto a sinistra) con `punto()`; area contenuto 60..960 × 220..1196 px
(hook: 220..1580).
"""
from __future__ import annotations

import re

import numpy as np
from manim import (BOLD, DOWN, DR, LEFT, RIGHT, UL, UP, Create, CubicBezier, DashedLine, FadeIn, FadeOut, LaggedStart,
                   Line, ManimColor, MoveToTarget, Rectangle, RoundedRectangle, Transform, UpdateFromAlphaFunc, VGroup,
                   interpolate_color, linear, smooth, squish_rate_func)

from tools.anim.base import ScenaReel, aree
from tools.anim.componenti import (Barrato, Carta, Classifica, Etichetta, Evidenzia, Freccia, Icona, Messaggio, Titolo,
                                   Token, testo, tratto)
from tools.anim.config import carica
from tools.anim.diagrammi import Graffa
from tools.anim.misure import PX_PER_UNITA, px

CFG = carica()
P = CFG.palette

# --- testi che ritornano fra le scene (dalla sceneggiatura: scene 1, 2, 5 e 6) ---------------------------------
RICHIESTA = "Un biglietto per la pensione di Marco. Lo firma tutto l'ufficio."
SII = "Sii originale."
DETTAGLIO = "Marco ha passato una vita a litigare con la fotocopiatrice."
# il biglietto banale (uscita vera di Claude Opus 5, tagli nelle note di produzione, «berlo sul divano» è un ritocco del
# presentatore), su righe fisse: la voce si ferma dopo «sveglia», a metà della seconda riga, e «la decidi tu,» arriva lì
# (il riquadro «probabile» incornicia quei tre)
BIGLIETTO = [["Caro", "Marco,", "da", "domani"], ["la", "sveglia", "la", "decidi", "tu,"],
             ["e", "il", "caffè", "potrai"], ["berlo", "sul", "divano."]]
N_SVEGLIA = 6          # cartellini fino a «sveglia» compreso
DOPO_SVEGLIA = (1, 2)  # riga e posto del secondo «la» (la parola scelta nelle scene 3-4)
# il biglietto nuovo (uscita vera di Claude Opus 5, `B-opus-1`: attacco e P.S., tagli nelle note), 5 righe fisse: beat
# 0 le prime due, beat 1 fino a «perfezione.», beat 2 «Per dispetto.» (acceso, poi di nuovo normale: revisione V12)
BIGLIETTO_NUOVO = [["Caro", "Marco,", "sono", "io."], ["Quella", "in", "fondo", "al", "corridoio."],
                   ["Da", "quando", "esci", "da", "quella"], ["porta", "prometto", "di", "funzionare"],
                   ["alla", "perfezione.", "Per", "dispetto."]]
SONO, IO = 2, 3            # indici fra i cartellini del biglietto nuovo
PER_DISPETTO = (20, 21)
# il bugiardino della 5: estratto vero di Claude Opus 5 (`C-opus-1`, richiesta con «Sii originale.»; tagli nelle note)
BUGIARDINO = ("PENSIONE®", "Principio attivo: tempo libero al 100%.",
              "Eccipienti: sveglia spenta, caffè bevuto seduto.")
LUCI_5 = ("sveglia", "caffè")   # le parole del biglietto della scena 2 che restano dentro la forma nuova
# TESTO/TITOLO delle scene precedenti, per ricostruirne l'ultimo fotogramma (nella scena stessa si usa self.scena)
TITOLO_1, SOTTO_1 = "Generativa non vuol dire creativa", "Vuol dire ==probabile=="
TESTO_2, TESTO_3, TESTO_4, TESTO_6 = "probabile", "una tra le prime", ["scritto da lei", "fluente", "originale"], "l'hai messa tu"

# --- candidate (esempi dichiarati dalla Classifica) ------------------------------------------------------------
CANDIDATE_3 = [("la", 0.46), ("non", 0.22), ("è", 0.12)]           # dopo «sveglia» (parole vere, numeri no)
CANDIDATE_5 = [("da", 0.48), ("oggi", 0.22), ("sono", 0.08)]       # dopo «Caro Marco,» (parole vere, numeri no)
DOPO_DETTAGLIO = [0.12, 0.09, 0.58]                                 # la fotocopiatrice: «sono» in testa

# --- misure (px) -------------------------------------------------------------------------------------------------
X0 = 60            # bordo sinistro dell'area contenuto
X1 = 960           # bordo destro
LARGHEZZA = 900    # carte a tutta larghezza
PAD = 40           # margine interno delle carte (come Carta)
GAP = 16           # spazio fra i cartellini (come Frase)
ALTO = 232         # cima della carta «richiesta» nelle scene 3-6
COLONNA_DX = 580   # colonna a destra delle barre per l'intestazione «dopo «…»»


def punto(x_px: float, y_px: float) -> np.ndarray:
    """Un punto della tela in px (origine in alto a sinistra) in unità Manim."""
    return np.array([px(x_px) - CFG.frame_width / 2, CFG.frame_height / 2 - px(y_px), 0.0])


def y_px(y: float) -> float:
    """Da una y in unità Manim alla y in px della tela."""
    return (CFG.frame_height / 2 - y) * PX_PER_UNITA


def fuori(*mobs, **kw) -> list:
    """Un FadeOut per pezzo (un FadeOut di un VGroup nuovo lascerebbe in scena i pezzi, trasparenti)."""
    return [FadeOut(m, **kw) for m in mobs]


def dentro(*mobs, **kw) -> list:
    return [FadeIn(m, **kw) for m in mobs]


def citazione(s: str) -> str:
    """Il primo testo fra «» di una riga ANIMAZIONE."""
    m = re.search(r"«(.+?)»", s)
    if not m:
        raise ValueError(f"nessuna citazione «…» in: {s}")
    return m.group(1)


def grande(scena: dict) -> str:
    """Il testo del cambio grande: «…» dopo «GRANDE:» in una riga ANIMAZIONE."""
    for s in scena.get("animazione") or []:
        m = re.search(r"GRANDE:\s*«(.+?)»", s)
        if m:
            return m.group(1)
    raise ValueError("nessuna riga ANIMAZIONE con «GRANDE: «…»»")


def acceso(t: Token) -> Token:
    """Un cartellino acceso: bordo e parola in accento («Per dispetto.» al ritorno dal punch, «io.» alla fine della 6)."""
    t.box.set_stroke(P.accento, width=tratto(5))
    t.testo.set_color(P.accento)
    return t


class Scena(ScenaReel):
    """ScenaReel con un aiuto locale per i cambi grandi (`punch` accorcia da solo la tenuta, ma vedi oltre_inizio)."""

    def oltre_inizio(self, i: int) -> None:
        """Da chiamare dopo beat(i) e prima di un punch (e prima di aggiungere ciò che deve comparire al ritorno).
        Difetto della libreria (da segnalare, tools/ non si tocca): beat(i) si ferma fino a un fotogramma prima del suo
        obiettivo (attese arrotondate per difetto), e allora punch prende l'inizio del beat in corso per «il beat dopo»
        e porta la tenuta al minimo di 0,3 s (nella 7 «TU SÌ» durava 0,33 s su 0,65, poi 0,3 s di scena ferma). Un
        fotogramma di attesa lo evita."""
        if self.t < self.inizi_frasi[i] - self.ANTICIPO_S + 1e-6:
            self.wait(self._fotogramma)


def riquadro(larghezza_px: float, altezza: float, colore: str) -> RoundedRectangle:
    """Il riquadro di una carta, con lo stile di Carta, sotto a tutto."""
    return RoundedRectangle(corner_radius=px(28), width=px(larghezza_px), height=altezza, stroke_color=colore,
                            stroke_width=tratto(3), fill_color=P.sfondo, fill_opacity=1).set_z_index(-1)


class CartaR(Carta):
    """Carta della libreria con il corpo delle righe a scelta (la scena 7 usa «token») e il riquadro sotto a tutto."""

    def __init__(self, titolo: str, righe=None, ruolo: str = "caption", **kw):
        self.ruolo = ruolo
        super().__init__(titolo, righe, **kw)
        self.box.set_z_index(-1)

    def _riga(self, s: str):
        return testo(s, self.ruolo, larghezza_px=self.larghezza_px - 2 * PAD)


class Scheda:
    """La carta «richiesta» a pezzi (riquadro, titolo, righe), con l'angolo in alto a sinistra in (x_px, y_px)."""

    def __init__(self, righe=(), y_px: float = ALTO, ruolo: str = "caption", larghezza_px: float = LARGHEZZA,
                 x_px: float = X0):
        c = CartaR("richiesta", list(righe), ruolo=ruolo, larghezza_px=larghezza_px)
        c.move_to(punto(x_px, y_px), aligned_edge=UL)
        self.box, self.titolo, self.righe = c.box, c.titolo, list(c.righe)

    def pezzi(self) -> list:
        return [self.box, self.titolo, *self.righe]

    @property
    def altezza_px(self) -> float:
        return self.box.height * PX_PER_UNITA


def pillola() -> Scheda:
    """La carta «richiesta» compatta: solo il titolo (scene 3-4)."""
    w = testo("richiesta", "etichetta", peso=BOLD).width * PX_PER_UNITA + 2 * PAD
    return Scheda([], larghezza_px=w)


class Biglietto:
    """Il biglietto: cartellini su righe fisse dentro una carta «biglietto». I pezzi restano separati: nelle scene 3-4
    in scena vanno solo i cartellini, riquadro e titolo tornano quando il biglietto è intero."""

    def __init__(self, righe: list[list[str]], y_px: float = 0, x_px: float = X0):
        self.titolo = testo("biglietto", "etichetta", colore=P.terziario, peso=BOLD)
        self.righe = [[Token(p) for p in r] for r in righe]
        file = VGroup(*[VGroup(*r).arrange(RIGHT, buff=px(GAP)) for r in self.righe])
        file.arrange(DOWN, buff=px(GAP), aligned_edge=LEFT)
        alt = self.titolo.height + px(24) + file.height + 2 * px(PAD)
        self.box = riquadro(LARGHEZZA, alt, P.terziario).move_to(punto(x_px, y_px), aligned_edge=UL)
        self.titolo.move_to(self.box.get_corner(UL) + np.array([px(PAD), -px(PAD), 0]), aligned_edge=UL)
        file.next_to(self.titolo, DOWN, buff=px(24), aligned_edge=LEFT)

    def token(self) -> list[Token]:
        return [t for r in self.righe for t in r]

    def allinea_righe(self, y: float) -> "Biglietto":
        """Sposta tutto in modo che la prima riga di cartellini abbia la cima a y px."""
        d = punto(0, y)[1] - self.righe[0][0].get_top()[1]
        for m in [self.box, self.titolo, *self.token()]:
            m.shift(UP * d)
        return self

    @property
    def altezza_px(self) -> float:
        return self.box.height * PX_PER_UNITA


def scelta(cl: Classifica, i: int) -> None:
    """Lo stato di cl.scegli(i), senza animazione (per ricostruire l'ultimo fotogramma di una scena)."""
    for k, b in enumerate(cl.barre):
        if k == i:
            b.riempimento.set_fill(P.accento)
            b.etichetta.set_color(P.accento)
        else:
            b.fade(0.65)


def cursore_dopo(t) -> Rectangle:
    return Rectangle(width=px(8), height=px(56), stroke_width=0, fill_color=P.accento, fill_opacity=1).next_to(
        t, RIGHT, buff=px(14))


def lampeggio(periodo: float = 0.8):
    """Updater (con dt) che accende e spegne un oggetto: gira anche durante le attese, finché non si toglie."""
    stato = {"t": 0.0}

    def aggiorna(m, dt):
        stato["t"] += dt
        m.set_fill(opacity=1.0 if (stato["t"] % periodo) < 0.55 * periodo else 0.0)

    return aggiorna


# --- impaginazioni condivise fra una scena e la successiva -----------------------------------------------------

def disposizione_01(titolo_s: str, sotto_s: str) -> tuple[Titolo, Titolo]:
    """Hook: «Generativa / non vuol dire / creativa» e sotto «vuol dire probabile», il gruppo centrato nell'area
    dell'hook (senza riquadro). Il fondo del sottotitolo resta a sinistra del cerchio del presentatore, così
    l'ultimo fotogramma può essere anche il primo della scena 2, dove il riquadro c'è."""
    p = titolo_s.split()
    titolo = Titolo("\n".join([p[0], " ".join(p[1:-1]), p[-1]]))
    sotto = Titolo(sotto_s)
    aree(CFG, None).contenuto.metti(VGroup(titolo, sotto).arrange(DOWN, aligned_edge=LEFT, buff=px(90)),
                                    "centro", "sinistra")
    return titolo, sotto


def barra_01(titolo: Titolo) -> tuple[Barrato, VGroup]:
    parola = titolo.parola("creativa")
    return Barrato(parola), parola


def disposizione_02(area) -> tuple[Scheda, Biglietto]:
    """Scena 2: richiesta intera e biglietto sotto, il gruppo centrato in verticale nell'area."""
    alto, basso = y_px(area.y1), y_px(area.y0)
    r0 = Scheda([RICHIESTA])
    b0 = Biglietto(BIGLIETTO)
    tot = r0.altezza_px + 40 + b0.altezza_px
    y = alto + (basso - alto - tot) / 2
    return Scheda([RICHIESTA], y_px=y), Biglietto(BIGLIETTO, y_px=y + r0.altezza_px + 40)


def extra_02(b: Biglietto, s: str):
    """Il riquadro accento su «la decidi tu,» (metà della seconda riga) e l'etichetta appesa sotto il suo angolo destro.
    Sopra c'è la prima riga del biglietto: l'etichetta sta nella fascia della terza riga, a destra di «potrai»."""
    r, k = DOPO_SVEGLIA
    cornice = Evidenzia(VGroup(*b.righe[r][k:]), buff=px(12))
    tag = Etichetta(s).next_to(cornice, DOWN, buff=0)
    sinistra = max(b.righe[r + 1][-1].get_right()[0] + px(GAP), cornice.get_right()[0] - tag.width)
    tag.set_x(sinistra + tag.width / 2)
    return cornice, tag


def disposizione_03():
    """Scene 3-4: pillola in alto, cartellini senza carta, intestazione e candidate sotto la riga di «sveglia»."""
    pil = pillola()
    bs = Biglietto(BIGLIETTO).allinea_righe(ALTO + pil.altezza_px + 40)
    testa = testo("dopo «sveglia»", "etichetta", colore=P.attenuato)
    cl = Classifica(CANDIDATE_3, larghezza_px=460)
    fondo_c = y_px(bs.righe[DOPO_SVEGLIA[0]][0].get_bottom()[1])
    VGroup(testa, cl).arrange(DOWN, aligned_edge=LEFT, buff=px(28)).move_to(punto(X0, fondo_c + 50), aligned_edge=UL)
    return pil, bs, testa, cl


def posto_scelta(bs: Biglietto) -> Token:
    """Il posto del secondo «la» nel biglietto: dove vola la candidata scelta (scena 3) e da dove riparte (scena 4)."""
    r, k = DOPO_SVEGLIA
    return bs.righe[r][k]


def graffa_03(cl: Classifica, s: str) -> Graffa:
    return Graffa(VGroup(cl.barre[0], cl.barre[1]), s, direzione=RIGHT, colore=P.testo)


def carta_04(pil: Scheda) -> Biglietto:
    """Scena 4 dal beat 1: il biglietto intero sotto la pillola."""
    return Biglietto(BIGLIETTO, y_px=ALTO + pil.altezza_px + 50)


def etichette_04(pil: Scheda, b: Biglietto, testi: list[str]):
    """«scritto da lei» a destra della pillola; «fluente» e «originale» (con la barra) sotto il biglietto."""
    lei = Etichetta(testi[0], colore=P.testo, pieno=False)
    lei.move_to([0, pil.box.get_center()[1], 0]).align_to(b.box, RIGHT)
    fl = Etichetta(testi[1], colore=P.terziario)
    orig = Etichetta(testi[2], colore=P.accento, pieno=False)
    VGroup(fl, orig).arrange(RIGHT, buff=px(40)).next_to(b.box, DOWN, buff=px(40), aligned_edge=LEFT)
    return lei, fl, orig, Barrato(orig.testo, colore=P.testo)


def carte_05() -> list[Scheda]:
    """Scena 5: la richiesta con 1, 2 e 3 righe (cresce verso il basso, stessa cima)."""
    return [Scheda([RICHIESTA]), Scheda([RICHIESTA, SII]), Scheda([RICHIESTA, SII, DETTAGLIO])]


def candidate_05(finale: bool = False):
    """Le candidate dopo «Caro Marco,» sotto la carta lunga, con l'intestazione nella colonna di destra.
    finale=True: l'ultimo fotogramma (riordinate, «la» in testa e accesa)."""
    lunga = carte_05()[-1]
    if finale:
        voci = sorted(zip([s for s, _ in CANDIDATE_5], DOPO_DETTAGLIO), key=lambda v: -v[1])
        cl = Classifica(voci, larghezza_px=480)
        scelta(cl, 0)
    else:
        cl = Classifica(CANDIDATE_5, larghezza_px=480)
    cl.move_to(punto(X0, ALTO + lunga.altezza_px + 40), aligned_edge=UL)
    testa = testo("dopo\n«Caro Marco,»", "etichetta", colore=P.attenuato)
    testa.move_to([punto(COLONNA_DX, 0)[0], cl.get_top()[1], 0], aligned_edge=UL)
    return cl, testa


Y_BIGLIETTO_6 = 575    # cima del biglietto nuovo alla fine della 6 (e all'inizio della 7): 5 righe, 612 px, fondo a 1187


def y_scrive_06() -> float:
    """Cima del biglietto nuovo mentre si scrive, sotto la pillola (una funzione: i testi si misurano solo dopo che
    ScenaReel ha registrato il font)."""
    return ALTO + pillola().altezza_px + 40


def biglietto_06(y: float, righe: int = 5) -> Biglietto:
    """Il biglietto nuovo con le prime `righe` righe, cartellini normali (gli accenti li decide la scena)."""
    return Biglietto(BIGLIETTO_NUOVO[:righe], y_px=y)


def extra_06(r: Scheda, bersaglio, s: str):
    """Graffa accento sotto la riga del dettaglio e freccia dalla parola «fotocopiatrice» a «sono io.» (nota del
    presentatore: la parola del dettaglio punta la risposta). La graffa sta nel margine basso della carta e l'etichetta
    appena sotto il bordo: tutta fuori dalla carta finirebbe a 591 px, e il biglietto di 5 righe (612 px) deve partire
    da 575 per stare nell'area. La freccia parte da sotto la graffa, in corrispondenza della parola."""
    g = Graffa(r.righe[0], s, direzione=DOWN, colore=P.accento)
    g.shift(DOWN * (g.graffa.get_top()[1] - r.righe[0].get_bottom()[1] + px(4)))
    parola = r.righe[0].parola("fotocopiatrice")
    inizio = np.array([parola.get_center()[0], g.graffa.get_bottom()[1] - px(6), 0])
    f = Freccia(inizio, bersaglio.get_top() + UP * px(4), colore=P.accento)
    return g, f


def stato_finale_06(s: str):
    """Ultimo fotogramma della 6: la richiesta con la riga del dettaglio, graffa e freccia, il biglietto sotto con «sono
    io.» acceso e «Per dispetto.» normale (revisione V12: l'accento è sulla freccia e su «sono io.», non sulla battuta)."""
    r6 = Scheda([DETTAGLIO])
    b6 = biglietto_06(Y_BIGLIETTO_6)
    sono_io = VGroup(acceso(b6.token()[SONO]), acceso(b6.token()[IO]))
    g, f = extra_06(r6, sono_io, s)
    return r6, b6, g, f


def diagramma_07(area, y_c: float, s_marco: str = "Marco"):
    """Scena 7: a sinistra l'IA (icona «bot»), a destra Marco (icona «user»), all'altezza y_c px; fra le due una
    linea tratteggiata con un buco al centro, sotto a tutto (z -2): la carta che entra nel buco la copre."""
    bot = Icona("bot", altezza_px=130, colore=P.testo)
    user = Icona("user", altezza_px=130, colore=P.testo)
    ia = testo("IA", "token", colore=P.attenuato)
    marco = testo(s_marco, "token")
    sx = VGroup(bot, ia).arrange(DOWN, buff=px(18))
    dx = VGroup(user, marco).arrange(DOWN, buff=px(18))
    y = punto(0, y_c)[1]
    sx.move_to([punto(X0, 0)[0] + sx.width / 2, y - (bot.get_center()[1] - sx.get_center()[1]), 0])
    dx.move_to([punto(X1 - 10, 0)[0] - dx.width / 2, y - (user.get_center()[1] - dx.get_center()[1]), 0])
    a, b = bot.get_right() + RIGHT * px(22), user.get_left() + LEFT * px(22)
    cx = (a[0] + b[0]) / 2
    buco = px(170)
    stile = dict(dash_length=px(18), stroke_color=P.attenuato, stroke_width=tratto(4))
    seg_sx = DashedLine(a, [cx - buco / 2, y, 0], **stile).set_z_index(-2)
    seg_dx = DashedLine(b, [cx + buco / 2, y, 0], **stile).set_z_index(-2)   # da Marco verso il buco
    larghezza_carta = (b[0] - a[0]) * PX_PER_UNITA - 2 * 64
    return bot, ia, user, marco, seg_sx, seg_dx, cx, larghezza_carta


def carta_07(cx: float, y_c: float, larghezza_px: float, righe=()) -> Scheda:
    """La carta «richiesta» centrata in (cx unità, y_c px), stretta per stare nel buco della linea."""
    prova = Scheda(list(righe), ruolo="token", larghezza_px=larghezza_px)
    x_px = cx * PX_PER_UNITA + CFG.frame_width / 2 * PX_PER_UNITA - larghezza_px / 2
    return Scheda(list(righe), y_px=y_c - prova.altezza_px / 2, ruolo="token", larghezza_px=larghezza_px, x_px=x_px)


# --- scene -----------------------------------------------------------------------------------------------------

class Scena01(Scena):
    """Hook: il titolo intero è già la copertina al primo fotogramma e si assesta riga per riga; «creativa» barrata
    appena detta; sotto «vuol dire probabile»."""

    def costruisci(self):
        titolo, sotto = disposizione_01(self.scena["titolo"], self.scena["sottotitolo"])
        for r in titolo.righe:                            # un po' più in basso: salgono al loro posto entro 0,5 s
            r.shift(DOWN * px(40))
        self.add(titolo)                                  # primo fotogramma pieno: il titolo intero
        self.play(LaggedStart(*[r.animate.shift(UP * px(40)) for r in titolo.righe], lag_ratio=0.25, group=titolo),
                  run_time=0.5)

        self.beat(1)                                      # «Generativa non vuol dire creativa.»
        barra, parola = barra_01(titolo)
        self.attendi_fino(self.inizi_frasi[2] - self.ANTICIPO_S - 0.45)   # appena detta «creativa»
        self.play(barra.entra(), parola.animate.set_opacity(0.45), run_time=0.35)

        self.beat(2)                                      # «Vuol dire probabile.»
        self.play(sotto.per_righe(lag=0.3), run_time=0.5)


class Scena02(Scena):
    """La richiesta di un biglietto originale; il biglietto si scrive fino a «sveglia», pausa col cursore (il momento
    della prova), poi «la decidi tu,» dove lampeggiava il cursore, il resto, e il riquadro «probabile»."""

    def costruisci(self):
        titolo, sotto = disposizione_01(TITOLO_1, SOTTO_1)   # ultimo fotogramma dell'hook
        barra, parola = barra_01(titolo)
        parola.set_opacity(0.45)
        self.add(titolo, barra, sotto)
        r, b = disposizione_02(self.area.contenuto)
        tok = b.token()
        n = N_SVEGLIA
        primi, attesa, resto = tok[:n], tok[n:n + 3], tok[n + 3:]   # fino a «sveglia» / «la decidi tu,» / «e il caffè…»
        self.play(*fuori(titolo, barra, sotto, shift=UP * 0.3), *dentro(*r.pezzi(), shift=UP * 0.2), run_time=0.5)

        self.beat(1)
        t1, d1 = self.t, self.durata_beat(1)
        self.play(*dentro(b.box, b.titolo, shift=UP * 0.2), run_time=0.4)
        self.attendi_fino(t1 + 0.27 * d1)                 # «Comincia così:», poi un cartellino per parola, lento
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in primi], lag_ratio=1.0),
                  run_time=self.arrotonda(0.6 * d1))
        cursore = cursore_dopo(primi[-1])                 # a metà della seconda riga, subito dopo «sveglia»
        cursore.add_updater(lampeggio())
        self.add(cursore)

        self.beat(2)
        t2, d2 = self.t, self.durata_beat(2)
        # il cursore lampeggia ancora per un attimo: chi guarda la finisce da solo; poi arriva il resto, lento. Niente
        # zoom (anteprima del 2026-09-13): a 2× la riga della richiesta restava tagliata ai bordi.
        self.attendi_fino(t2 + 0.22 * d2)
        cursore.clear_updaters()
        self.remove(cursore)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in attesa], lag_ratio=0.6), run_time=self.arrotonda(0.5))
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in resto], lag_ratio=0.5), run_time=self.arrotonda(0.7))
        cornice, tag = extra_02(b, self.scena["testo"][0])
        self.play(Create(cornice), FadeIn(tag, scale=0.85), run_time=0.45)


class Scena03(Scena):
    """Una parola per volta: la frase si ricompone fino a «sveglia», le candidate la / non / è, «la» (una tra le prime)
    va in coda."""

    def costruisci(self):
        r, b = disposizione_02(self.area.contenuto)       # ultimo fotogramma della scena 2
        cornice, tag = extra_02(b, TESTO_2)
        self.add(*r.pezzi(), b.box, b.titolo, *b.token(), cornice, tag)
        pil, bs, testa, cl = disposizione_03()
        primi = bs.token()[:N_SVEGLIA]
        d0 = self.durata_beat(0)
        self.play(Transform(r.box, pil.box), Transform(r.titolo, pil.titolo), FadeOut(r.righe[0]),
                  *fuori(b.box, b.titolo, *b.token(), cornice, tag, shift=DOWN * 0.2), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in primi], lag_ratio=0.8),
                  run_time=self.arrotonda(min(1.1, 0.5 * d0)))

        self.beat(1)
        self.play(FadeIn(testa), cl.entra(), run_time=min(1.2, 0.45 * self.durata_beat(1)))

        self.beat(2)
        g = graffa_03(cl, self.scena["testo"][0])
        self.play(g.entra(), cl.scegli(0), run_time=0.4)
        la = cl.token(0, colore=P.accento)
        self.play(la.animate.move_to(posto_scelta(bs)), run_time=0.5)


class Scena04(Scena):
    """Il bivio dopo «sveglia»: la frase corre sul ramo spesso di «la» e scrive «decidi tu,»; torna un biglietto intero,
    scritto da lei (non pescato da un archivio); fluente sì, originale no."""

    def costruisci(self):
        pil, bs, testa, cl = disposizione_03()            # ultimo fotogramma della scena 3
        scelta(cl, 0)
        g = graffa_03(cl, TESTO_3)
        la = Token("la", colore=P.accento).move_to(posto_scelta(bs))
        primi = bs.token()[:N_SVEGLIA]
        self.add(*pil.pezzi(), *primi, testa, cl, g, la)

        # beat 0: tre rami da «sveglia», con la sola prima parola all'attacco (le candidate della scena 3)
        r, k = DOPO_SVEGLIA
        sv = bs.righe[r][k - 1]
        y_figli = y_px(sv.get_bottom()[1]) + 250
        fila = VGroup(*[Token(p) for p in BIGLIETTO[r][k:]]).arrange(RIGHT, buff=px(GAP))
        fila.move_to(punto(X0 + PAD, y_figli), aligned_edge=UL)   # «la decidi tu,» sul ramo di «la»
        cont = list(fila[1:])
        non = Token("non").move_to([punto(560, 0)[0], fila.get_center()[1], 0])
        e = Token("è").move_to([punto(820, 0)[0], fila.get_center()[1], 0])
        origine = sv.get_bottom() + DOWN * px(8)

        def ramo(figlio, spessore):
            fine = figlio.get_top() + UP * px(8)
            h = origine[1] - fine[1]
            return CubicBezier(origine, origine + DOWN * h * 0.5, fine + UP * h * 0.5, fine,
                               stroke_color=P.attenuato, stroke_width=tratto(spessore))

        rami = [ramo(fila[0], 16), ramo(non, 6), ramo(e, 3)]
        nota = testo("esempio: numeri inventati", "piede", colore=P.attenuato)
        nota.next_to(fila, DOWN, buff=px(40)).align_to(fila, LEFT)
        d0 = self.durata_beat(0)
        self.play(*fuori(testa, cl, g), run_time=0.25)   # prima esce la classifica, poi crescono i rami
        self.play(la.animate.move_to(fila[0]), *[Create(x) for x in rami], *dentro(non, e, nota), run_time=0.6)
        self.attendi_fino(0.26 * d0)
        acceso = rami[0].copy().set_stroke(P.accento)     # la frase prende la strada più battuta
        self.play(Create(acceso), rami[1].animate.set_stroke(opacity=0.3), rami[2].animate.set_stroke(opacity=0.3),
                  run_time=0.35)
        self.play(*fuori(non, e, rami[1], rami[2]), run_time=0.2)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in cont], lag_ratio=0.8),
                  run_time=self.arrotonda(min(0.7, 0.2 * d0)))

        # beat 1: i rami spariscono, torna il biglietto intero; il database barrato diventa «scritto da lei»
        self.beat(1)
        t1, d1 = self.t, self.durata_beat(1)
        b4 = carta_04(pil)
        vecchi = primi + [la] + cont
        nuovi = b4.token()
        self.play(*fuori(acceso, rami[0], nota), *[Transform(v, n) for v, n in zip(vecchi, nuovi)],
                  *dentro(b4.box, b4.titolo, *nuovi[len(vecchi):]), run_time=0.5)
        lei, fl, orig, barra_orig = etichette_04(pil, b4, self.scena["testo"])
        db = Icona("database", altezza_px=110, colore=P.testo).move_to(lei)
        m = px(12)
        barra_db = Line(db.get_corner(UL) + (LEFT + UP) * m, db.get_corner(DR) + (RIGHT + DOWN) * m,
                        stroke_color=P.accento, stroke_width=tratto(10))
        self.attendi_fino(t1 + 0.2 * d1)
        self.play(db.entra(), run_time=0.35)
        self.play(Create(barra_db), run_time=0.25)
        self.attendi_fino(t1 + 0.45 * d1)
        self.play(FadeOut(db.svg, scale=0.8), FadeOut(barra_db, scale=0.8), FadeIn(lei, scale=0.85), run_time=0.4)

        self.beat(2)
        self.play(FadeIn(fl, scale=0.85), run_time=0.35)

        self.beat(3)
        self.play(FadeIn(orig, scale=0.85), run_time=0.3)
        self.play(barra_orig.entra(), run_time=0.3)


class Bugiardino:
    """La carta «biglietto» piccola della 5, a pezzi (bordo terziario, come il biglietto): l'estratto vero di Opus 5 con
    il titolo «PENSIONE®» grande, che si legge per primo, e due righe. Nessuna etichetta «nuova» né «originale»
    (revisione X5: due bugiardini su cinque hanno lo stesso titolo e righe identiche)."""

    def __init__(self, y_px: float, larghezza_px: float = 760, x_px: float = X0):
        nome, *righe = BUGIARDINO
        self.titolo = testo("biglietto", "etichetta", colore=P.terziario, peso=BOLD)
        self.nome = testo(nome, "messaggio", peso=BOLD)
        self.righe = [testo(r, "caption", larghezza_px=larghezza_px - 2 * PAD) for r in righe]
        corpo = VGroup(self.titolo, self.nome, *self.righe).arrange(DOWN, buff=px(24), aligned_edge=LEFT)
        self.box = riquadro(larghezza_px, corpo.height + 2 * px(PAD), P.terziario).move_to(punto(x_px, y_px),
                                                                                           aligned_edge=UL)
        corpo.move_to(self.box.get_corner(UL) + np.array([px(PAD), -px(PAD), 0]), aligned_edge=UL)

    def pezzi(self) -> list:
        return [self.box, self.titolo, self.nome, *self.righe]


class Scena05(Scena):
    """«Sii originale.» cambia la forma (il bugiardino «PENSIONE®», estratto vero di Opus 5), ma dentro la sveglia
    resta; il dettaglio vero riordina le candidate dopo «Caro Marco,»: «sono» in testa."""

    def costruisci(self):
        pil = pillola()                                   # ultimo fotogramma della scena 4
        b4 = carta_04(pil)
        lei, fl, orig, barra_orig = etichette_04(pil, b4, TESTO_4)
        vecchi = [b4.box, b4.titolo, *b4.token(), lei, fl, orig, barra_orig]
        self.add(*pil.pezzi(), *vecchi)
        _, r2, r3 = carte_05()
        bug = Bugiardino(ALTO + r2.altezza_px + 40)
        cl, testa = candidate_05()                        # già al posto finale: non si sposta quando la carta cresce
        su = UP * 0.15

        # beat 0 («Aggiungere «sii originale» cambia la forma.»): esce la 4 e la richiesta torna intera con «Sii
        # originale.» (0,9 s); poi, accanto (sotto: l'asse del 9:16), il bugiardino, prima il titolo (0,9 s)
        self.play(*fuori(*vecchi, shift=DOWN * 0.2, rate_func=dopo(0, 0.4)),
                  Transform(pil.box, r2.box, rate_func=dopo(0.15, 0.7)),
                  FadeIn(r2.righe[0], shift=su, rate_func=dopo(0.35, 0.8)),
                  FadeIn(r2.righe[1], shift=su, rate_func=dopo(0.6, 1.0)), run_time=0.9)
        self.play(FadeIn(bug.box, shift=UP * 0.2, rate_func=dopo(0, 0.35)),
                  FadeIn(bug.titolo, shift=UP * 0.2, rate_func=dopo(0, 0.35)),
                  FadeIn(bug.nome, scale=1.1, rate_func=dopo(0.15, 0.5)),
                  FadeIn(bug.righe[0], shift=su, rate_func=dopo(0.45, 0.75)),
                  FadeIn(bug.righe[1], shift=su, rate_func=dopo(0.65, 1.0)), run_time=0.9)

        # beat 1 («Dentro, la sveglia resta.»): nel bugiardino si accendono «sveglia» e «caffè», come nella scena 2
        self.beat(1)
        t1, d1 = self.t, self.durata_beat(1)
        luci = [bug.righe[1].parola(p) for p in LUCI_5]
        self.attendi_fino(t1 + 0.35 * d1)                 # «…la sveglia»
        self.play(*[p.animate.set_color(P.accento) for p in luci], run_time=0.4)

        # beat 2 («Serve un dettaglio vero: Marco litigava con la fotocopiatrice.»): esce il bugiardino, entra la colonna
        # con «da» in testa; ~0,4 s dopo la riga del dettaglio (revisione X7), poi il riordino e «sono» in accento
        self.beat(2)
        self.play(*fuori(*bug.pezzi(), shift=DOWN * 0.2, rate_func=dopo(0, 0.45)),
                  cl.entra(rate_func=dopo(0.3, 1.0)), FadeIn(testa, rate_func=dopo(0.3, 0.8)), run_time=0.8)
        self.wait(0.4)                                    # «da» in testa, fermo, prima del dettaglio
        self.play(Transform(pil.box, r3.box, rate_func=dopo(0, 0.6)),
                  FadeIn(r3.righe[2], shift=su, rate_func=dopo(0.3, 1.0)), run_time=0.6)
        self.play(cl.aggiorna(DOPO_DETTAGLIO), run_time=0.9)
        self.play(cl.scegli(2), run_time=0.4)
        # niente zoom (provato nel primo reel): la carta larga 900 px sopra le barre resta tagliata ai bordi


def _tra(a: float, x0: float, x1: float) -> float:
    """Dove sta a fra x0 e x1, da 0 a 1."""
    return min(1.0, max(0.0, (a - x0) / (x1 - x0)))


def finestre(n: int, a: float = 0.0, b: float = 1.0, durata: float = 1.6) -> list:
    """Le curve di n cartellini che entrano uno dopo l'altro fra le frazioni a e b della play (ognuno dura `durata`
    passi): la scrittura a cartellini dentro un solo passaggio, senza LaggedStart."""
    w = (b - a) / (n - 1 + durata)
    return [dopo(a + k * w, a + k * w + durata * w) for k in range(n)]


def vola(t: Token, dove, comparsa=(0.0, 0.2), moto=(0.35, 1.0)) -> UpdateFromAlphaFunc:
    """Il cartellino si accende dove sta (dissolvenza, finestra `comparsa`) e poi vola in `dove` (finestra `moto`), in
    una sola animazione: FadeIn e .animate sullo stesso oggetto nella stessa play non si sommano (vale l'ultima)."""
    da, a_ = t.get_center().copy(), np.array(dove, dtype=float)
    # l'opacità solo su riquadro e glifi: set_opacity sul cartellino intero accenderebbe anche il puntello invisibile
    # delle righe (una Line bianca larga zero), e il controllo «colore» la vede
    t.box.set_opacity(0)
    t.testo.glifi.set_opacity(0)

    def f(m, a):
        o = _tra(a, *comparsa)
        m.box.set_opacity(o)
        m.testo.glifi.set_opacity(o)
        m.move_to(da + (a_ - da) * smooth(_tra(a, *moto)))

    return UpdateFromAlphaFunc(t, f, rate_func=linear)


def scende_e_si_accende(t: Token, spostamento, moto=(0.0, 0.4), luce=(0.75, 1.0)) -> UpdateFromAlphaFunc:
    """Il cartellino si sposta con il biglietto (finestra `moto`) e poi si accende come acceso() (finestra `luce`), in
    una sola animazione (MoveToTarget farebbe le due cose insieme)."""
    da = t.get_center().copy()
    bordo, parola, acc = ManimColor(P.attenuato), ManimColor(P.testo), ManimColor(P.accento)

    def f(m, a):
        m.move_to(da + spostamento * smooth(_tra(a, *moto)))
        s = smooth(_tra(a, *luce))
        m.box.set_stroke(interpolate_color(bordo, acc, s), width=tratto(3 + 2 * s))
        m.testo.set_color(interpolate_color(parola, acc, s))

    return UpdateFromAlphaFunc(t, f, rate_func=linear)


class Scena06(Scena):
    """«sono» parte dalla testa della colonna e vola nel biglietto nuovo, che si scrive e cresce con la voce; «PER
    DISPETTO.» a tutto schermo; il biglietto scende, la richiesta torna con la riga del dettaglio, «Per dispetto.» torna
    normale e l'accento passa alla graffa «l'hai messa tu», alla freccia e a «io.» (revisione V12)."""

    def costruisci(self):
        r3 = carte_05()[-1]                               # ultimo fotogramma della scena 5
        cl, testa = candidate_05(finale=True)
        self.add(*r3.pezzi(), testa, cl)
        pil = pillola()
        y0 = y_scrive_06()
        corto = biglietto_06(y0, righe=2)                 # il biglietto mentre si scrive la prima frase
        b6 = biglietto_06(y0)                             # intero (i cartellini stanno negli stessi posti)
        tok = b6.token()
        box = corto.box
        su = UP * 0.15

        # beat 0 («Ora scrive: caro Marco, sono io. Quella in fondo al corridoio.»): tre passaggi, come chiedono le note
        # di produzione (la pillola con l'ingresso del biglietto; «sono» che vola; la colonna che esce dopo, T4); la
        # scrittura a cartellini sta dentro i passaggi, con la voce
        t0, d0 = self.t, self.durata_beat(0)
        # passaggio 1 (0,7 s, «Ora scrive:»): la richiesta si compatta nella pillola e resta come contesto (T6); entra il
        # biglietto, alto due righe
        self.play(Transform(r3.box, pil.box, rate_func=dopo(0, 0.6)), *fuori(*r3.righe, rate_func=dopo(0, 0.4)),
                  FadeIn(box, shift=UP * 0.2, rate_func=dopo(0.3, 1.0)),
                  FadeIn(b6.titolo, shift=UP * 0.2, rate_func=dopo(0.3, 1.0)), run_time=0.7)
        # passaggio 2 (1,3 s, «caro Marco, sono»): «Caro», «Marco,»; «sono» si accende sulla testa della colonna (sopra
        # l'etichetta già accesa della scena 5) e vola al suo posto
        sono = Token("sono", colore=P.accento).move_to(cl.barre[0].etichetta, aligned_edge=LEFT).set_z_index(1)
        self.attendi_fino(t0 + 0.2 * d0)                  # «caro»
        self.play(FadeIn(tok[0], shift=su, rate_func=dopo(0, 0.3)), FadeIn(tok[1], shift=su, rate_func=dopo(0.2, 0.5)),
                  vola(sono, tok[SONO].get_center(), comparsa=(0.3, 0.5), moto=(0.55, 1.0)), run_time=1.3)
        # passaggio 3 (1,5 s, «io. Quella in fondo al corridoio.»): solo ora, con «sono» arrivato, la colonna esce
        # (revisione T4); «io.» e la seconda riga si scrivono con la voce
        riga2 = tok[IO + 1:IO + 6]
        self.play(*fuori(cl, testa, shift=DOWN * 0.2, rate_func=dopo(0, 0.4)),
                  FadeIn(tok[IO], shift=su, rate_func=dopo(0, 0.25)),
                  *[FadeIn(t, shift=su, rate_func=r) for t, r in zip(riga2, finestre(len(riga2), 0.25, 0.9))],
                  run_time=1.5)

        # beat 1, un passaggio: il biglietto cresce a cinque righe e la seconda frase si scrive con la voce, fino a
        # «perfezione.»; «sono» torna al bordo normale (un accento per beat)
        self.beat(1)
        d1 = self.durata_beat(1)
        nuove = tok[IO + 6:PER_DISPETTO[0]]
        self.play(Transform(box, b6.box, rate_func=dopo(0, 0.15)),
                  sono.box.animate(rate_func=dopo(0, 0.15)).set_stroke(P.attenuato, width=tratto(3)),
                  sono.testo.animate(rate_func=dopo(0, 0.15)).set_color(P.testo),
                  *[FadeIn(t, shift=su, rate_func=r) for t, r in zip(nuove, finestre(len(nuove), 0.05, 1.0, durata=1.5))],
                  run_time=self.arrotonda(min(3.6, 0.9 * d1)))

        # beat 2, il cambio grande; al ritorno il biglietto è intero, con «Per dispetto.» acceso (entra durante il
        # taglio). oltre_inizio prima di aggiungerlo: così il punch tiene ~1 s e non 0,3 (difetto della libreria)
        self.beat(2)
        self.oltre_inizio(2)
        for i in PER_DISPETTO:
            acceso(tok[i])
        self.add(*[tok[i] for i in PER_DISPETTO])
        self.punch(grande(self.scena))

        # beat 3, un passaggio (2,4 s): il biglietto scende e «Per dispetto.» torna normale mentre la richiesta torna con
        # la riga del dettaglio; poi la graffa «l'hai messa tu» e la freccia dalla parola «fotocopiatrice», e «sono io.»
        # si accende quando la freccia arriva (nota del presentatore; V12: la battuta non resta accesa accanto a «l'hai
        # messa tu»)
        self.beat(3)
        t3 = self.t
        r6 = Scheda([DETTAGLIO])
        fine = biglietto_06(Y_BIGLIETTO_6)
        g, f = extra_06(r6, VGroup(fine.token()[SONO], fine.token()[IO]), self.scena["testo"][0])
        giu = DOWN * px(Y_BIGLIETTO_6 - y0)
        battuta = [tok[i] for i in PER_DISPETTO]
        for t in battuta:
            t.generate_target()
            t.target.shift(giu)
            t.target.box.set_stroke(P.attenuato, width=tratto(3))
            t.target.testo.set_color(P.testo)
        altri = [box, b6.titolo] + [t for k, t in enumerate(tok) if k not in (SONO, IO, *PER_DISPETTO)]
        self.attendi_fino(t3 + 0.35)                      # un attimo per vedere il biglietto intero con la battuta accesa
        self.play(*[m.animate(rate_func=dopo(0, 0.4)).shift(giu) for m in altri],
                  *[MoveToTarget(t, rate_func=dopo(0, 0.4)) for t in battuta],
                  scende_e_si_accende(sono, giu, luce=(0.84, 1.0)), scende_e_si_accende(tok[IO], giu, luce=(0.84, 1.0)),
                  Transform(r3.box, r6.box, rate_func=dopo(0.05, 0.4)),
                  FadeIn(r6.righe[0], shift=su, rate_func=dopo(0.2, 0.45)),
                  g.entra(rate_func=dopo(0.45, 0.68)), f.entra(rate_func=dopo(0.62, 0.88)), run_time=2.4)


def pezzi_finale_06() -> list:
    """I pezzi dell'ultimo fotogramma della 6, uno per uno (la 7 li fa uscire tutti, qualunque cosa ci sia)."""
    pezzi = []
    for x in stato_finale_06(TESTO_6):
        if isinstance(x, Scheda):
            pezzi += x.pezzi()
        elif isinstance(x, Biglietto):
            pezzi += [x.box, x.titolo, *x.token()]
        else:
            pezzi.append(x)
    return pezzi


def dopo(a: float, b: float = 1.0):
    """Curva smooth compressa nella frazione [a, b] della play: più movimenti in un solo passaggio, sfalsati, senza
    LaggedStart (che accoderebbe un gruppo nuovo in cima alla scena)."""
    return squish_rate_func(smooth, a, b)


class Scena07(Scena):
    """Chiusura, un passaggio per frase: l'IA e Marco con la linea interrotta e il messaggio; «TU SÌ»; la richiesta
    entra nel buco della linea con la riga della fotocopiatrice; il diagramma esce con calma e restano messaggio e
    CTA (il biglietto non torna più: nota del presentatore del 2026-09-14)."""

    def costruisci(self):
        vecchi = pezzi_finale_06()                        # ultimo fotogramma della scena 6
        self.add(*vecchi)

        a = self.area.contenuto
        msg = Messaggio(self.scena["messaggio"].replace(". ", ".\n", 1), maiuscolo=False)   # «Tu sì.» su una riga sua
        msg.move_to(punto(X0, ALTO), aligned_edge=UL)
        righe = msg.righe
        fondo_msg = y_px(msg.get_bottom()[1])
        y_c = (fondo_msg + 40 + y_px(a.y0)) / 2           # centro del diagramma nello spazio sotto il messaggio
        bot, ia, user, marco, seg_sx, seg_dx, cx, w_carta = diagramma_07(a, y_c)
        piena = carta_07(cx, y_c, w_carta, [DETTAGLIO])
        riga = piena.righe[0].set_color(P.accento)

        # Chiusura calma (nota del presentatore del 2026-09-14): un solo passaggio per frase, ognuno ≥ 0,6 s; i movimenti
        # di un passaggio sono sfalsati dentro la stessa play con dopo(a, b), non con play in fila.

        # beat 0, un passaggio (1,0 s): esce tutto; entrano il messaggio, l'IA e Marco, fra loro la linea interrotta
        self.play(*fuori(*vecchi, shift=DOWN * 0.2, rate_func=dopo(0, 0.45)),
                  FadeIn(righe[0], shift=UP * 0.2, rate_func=dopo(0.3, 0.75)),
                  FadeIn(righe[1], shift=UP * 0.2, rate_func=dopo(0.42, 0.87)),
                  # le icone in dissolvenza: Create a progresso 0 disegna un punto per tratto (estremità tonde), e con la
                  # curva sfalsata i punti resterebbero a schermo per un terzo del passaggio
                  FadeIn(bot, scale=0.9, rate_func=dopo(0.35, 0.9)), FadeIn(ia, rate_func=dopo(0.45, 0.9)),
                  FadeIn(user, scale=0.9, rate_func=dopo(0.45, 1.0)), FadeIn(marco, rate_func=dopo(0.55, 1.0)),
                  Create(seg_sx, rate_func=dopo(0.5, 1.0)), Create(seg_dx, rate_func=dopo(0.5, 1.0)), run_time=1.0)

        # beat 1, il cambio grande; al ritorno il messaggio ha anche «Tu sì.»
        self.beat(1)
        self.oltre_inizio(1)                              # prima di aggiungere «Tu sì.», che compare solo al ritorno
        self.add(righe[2])
        self.punch(grande(self.scena))                    # la tenuta si accorcia da sola fino al beat dopo

        # beat 2, un passaggio (0,8 s): una linea accento dal presentatore a Marco; la richiesta entra nel buco della
        # linea e ci scivola, da Marco, la riga della fotocopiatrice: l'IA arriva a Marco solo da quello che scrivi
        # (revisione T13). Agganciato all'inizio del beat, non alle parole: la frase è di tre parole («Scrivilo nella
        # richiesta.») e la riga, che scioglie il «lo», deve restare intera ≥ 1 s prima che il diagramma esca (U4).
        self.beat(2)
        riq = self.area.riquadro
        fine = marco.get_bottom() + DOWN * px(14)
        verso = (fine - riq.centro) / np.linalg.norm(fine - riq.centro)
        inizio = riq.centro + verso * (riq.larghezza / 2 + px(18))
        linea = Line(inizio, fine, stroke_color=P.accento, stroke_width=tratto(6))
        self.play(Create(linea, rate_func=dopo(0, 0.5)), FadeIn(piena.box, scale=0.9, rate_func=dopo(0.1, 0.55)),
                  FadeIn(piena.titolo, rate_func=dopo(0.15, 0.6)), FadeIn(riga, shift=LEFT * 0.4, rate_func=dopo(0.4, 1.0)),
                  run_time=0.8)
        riga_intera = self.t

        # beat 3, un passaggio (1,0 s): il diagramma esce con calma mentre il messaggio scende al centro e sotto entra
        # la CTA; poi l'ultimo fotogramma pulito (solo messaggio e CTA) fino alla fine
        self.beat(3)
        t3 = self.t
        diagramma = [bot, ia, user, marco, seg_sx, seg_dx, linea, piena.box, piena.titolo, riga]
        cta = Etichetta(self.scena["cta"])
        h = msg.height + px(50) + cta.height
        dy = (a.centro[1] + h / 2) - msg.get_top()[1]     # sposta il messaggio: messaggio + CTA centrati nell'area
        cta.move_to(punto(X0, 0), aligned_edge=LEFT).set_y(msg.get_bottom()[1] + dy - px(50) - cta.height / 2)
        self.attendi_fino(max(t3 + 0.1, riga_intera + 1.05))   # U4: la riga intera ≥ 1 s, anche con un beat 2 corto
        self.play(*fuori(*diagramma, shift=DOWN * 0.2, rate_func=dopo(0, 0.6)),
                  *[r.animate(rate_func=dopo(0.1, 0.9)).shift(UP * dy) for r in righe],
                  FadeIn(cta, shift=UP * 0.2, rate_func=dopo(0.4, 1.0)), run_time=1.0)
