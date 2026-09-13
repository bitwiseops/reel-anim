"""Animazioni di «Generativa non vuol dire creativa» (contenuti/sceneggiature/2026-09-13-generativa-non-creativa.md).

Il filo visivo: tre oggetti per tutto il reel, sempre con lo stesso aspetto.
- La carta «richiesta» (bordo secondario) è «quello che viene prima»: intera nella scena 2, compatta (solo il
  titolo) in alto nelle scene 3-4 e 6, di nuovo intera e più lunga nella 5, con la sola riga del dettaglio alla fine
  della 6; nella 7 entra, stretta, nel buco della linea fra l'IA e Marco.
- Il biglietto: cartellini su righe fisse; dentro la carta «biglietto» (bordo terziario) quando è intero (scene 2,
  4 dal beat 1, 6), cartellini senza carta mentre si guarda come si scrive (scene 3-4). Il biglietto nuovo della 6
  cresce con la voce (2 righe, poi 4) e torna per un attimo nella 7 con «Lei no.» acceso.
- La colonna delle candidate: `Classifica` con la nota «esempio: numeri inventati» (scene 3 e 5; nella 6 «la»
  parte dalla sua testa).

Cambi grandi: la battuta a tutto schermo (`punch`) nella 6 («LEI NO.») e nella 7 («TU SÌ»); lo zoom di camera
nella 2 (sul cursore, il momento della prova), dentro un solo beat.

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
from manim import (BOLD, DOWN, DR, LEFT, RIGHT, UL, UP, AnimationGroup, Create, CubicBezier, DashedLine, FadeIn, FadeOut,
                   LaggedStart, Line, Rectangle, RoundedRectangle, Transform, VGroup)

from tools.anim.base import ScenaReel, aree
from tools.anim.componenti import (Barrato, Carta, Classifica, Etichetta, Evidenzia, Freccia, Icona, Messaggio, Titolo,
                                   Token, testo, tratto)
from tools.anim.config import carica
from tools.anim.diagrammi import Graffa
from tools.anim.misure import PX_PER_UNITA, px

CFG = carica()
P = CFG.palette

# --- testi che ritornano fra le scene (dalla sceneggiatura: scene 1, 2, 5 e 6) ---------------------------------
RICHIESTA = "Un biglietto originale per la pensione di Marco. Lo firma tutto l'ufficio."
SII = "Sii originale."
DETTAGLIO = "Marco ha passato una vita a litigare con la fotocopiatrice."
# righe fisse: «e se ne apre uno nuovo.» ha una riga sua (il riquadro «probabile» la incornicia intera)
BIGLIETTO = [["Caro", "Marco,", "oggi", "si", "chiude"], ["un", "capitolo"],
             ["e", "se", "ne", "apre", "uno", "nuovo."], ["Goditi", "il", "meritato", "riposo!"]]
BIGLIETTO_NUOVO = [["Caro", "Marco,", "la", "fotocopiatrice"], ["ha", "chiesto", "di", "te."],
                   ["Le", "ho", "detto", "che", "da", "lunedì"], ["sei", "libero.", "Lei", "no."]]
LEI_NO = (16, 17)   # indici di «Lei» e «no.» fra i cartellini del biglietto nuovo
# TESTO/TITOLO delle scene precedenti, per ricostruirne l'ultimo fotogramma (nella scena stessa si usa self.scena)
TITOLO_1, SOTTO_1 = "Generativa non vuol dire creativa", "Vuol dire ==probabile=="
TESTO_2, TESTO_3, TESTO_4, TESTO_6 = "probabile", "una tra le prime", ["scritto da lei", "fluente", "originale"], "l'hai messa tu"

# --- candidate (esempi dichiarati dalla Classifica) ------------------------------------------------------------
CANDIDATE_3 = [("e", 0.46), ("ma", 0.22), ("della", 0.12)]          # dopo «capitolo»
CANDIDATE_5 = [("oggi", 0.48), ("ti", 0.22), ("la", 0.08)]          # dopo «Caro Marco,»
DOPO_SII = [0.45, 0.25, 0.10]                                       # «Sii originale.»: si muovono appena
DOPO_DETTAGLIO = [0.12, 0.09, 0.58]                                 # la fotocopiatrice: «la» in testa

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


def cresce(box, nuovo_box, riga):
    """La carta si allunga e la riga nuova entra quando c'è posto (come Carta.aggiungi_riga, ma a pezzi).
    group=box: senza, Manim accoda alla scena un Group (box, riga) e il riquadro pieno, ora «in movimento», viene
    disegnato sopra il titolo fermo (durante questa play e in ogni play dopo che anima qualcosa che sta prima)."""
    return LaggedStart(Transform(box, nuovo_box), FadeIn(riga, shift=UP * 0.15), lag_ratio=0.35, group=box)


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
    """Un cartellino acceso: bordo e parola in accento (è «Lei no.» nelle scene 6 e 7)."""
    t.box.set_stroke(P.accento, width=tratto(5))
    t.testo.set_color(P.accento)
    return t


class Scena(ScenaReel):
    """ScenaReel con due aiuti locali per i cambi grandi (vedi il rapporto: sono candidati per la libreria)."""

    def punch_fino(self, s: str, k: int, tenuta_max: float = 0.9) -> None:
        """self.punch(s) con la tenuta tagliata per finire all'inizio del beat k: con la voce di prova «Lei no.» e
        «Tu sì.» durano 0,7 s, meno dell'entrata + tenuta predefinite (1,05 s), e il beat dopo partirebbe tardi."""
        entrata = self.arrotonda(0.15)
        fine = self.inizi_frasi[k] - self.ANTICIPO_S
        tenuta = self.arrotonda(max(0.3, min(tenuta_max, fine - self.t - entrata)))
        self.punch(s, tenuta_s=tenuta, entrata_s=entrata)

    def zoom_area(self, mob, fattore: float):
        """Come self.zoom_su, ma porta mob al centro dell'area contenuto e non al centro della tela: con il riquadro in
        basso l'area è più alta del centro della tela (708 contro 960 px) e con zoom_su l'oggetto ingrandito scende
        verso il riquadro."""
        centro = mob.get_center() - self.area.contenuto.centro / fattore
        return self.camera.frame.animate.set(width=self.cfg.frame_width / fattore).move_to(centro)


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
    """Il riquadro accento sulla riga «e se ne apre uno nuovo.» e l'etichetta appesa al suo angolo in alto a destra."""
    cornice = Evidenzia(VGroup(*b.righe[2]), buff=px(12))
    tag = Etichetta(s).next_to(cornice, UP, buff=0).align_to(cornice, RIGHT)
    return cornice, tag


def disposizione_03():
    """Scene 3-4: pillola in alto, cartellini senza carta, intestazione e candidate sotto."""
    pil = pillola()
    bs = Biglietto(BIGLIETTO).allinea_righe(ALTO + pil.altezza_px + 40)
    testa = testo("dopo «capitolo»", "etichetta", colore=P.attenuato)
    cl = Classifica(CANDIDATE_3, larghezza_px=460)
    fondo_c = y_px(bs.righe[2][0].get_bottom()[1])
    VGroup(testa, cl).arrange(DOWN, aligned_edge=LEFT, buff=px(28)).move_to(punto(X0, fondo_c + 50), aligned_edge=UL)
    return pil, bs, testa, cl


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


ZOOM_2 = 2.0   # scena 2: la camera su «capitolo» e il cursore (a 1,6 la richiesta restava a metà in alto)
Y_BIGLIETTO_6 = 640                                # cima del biglietto nuovo alla fine della 6 (e nella 7)


def y_scrive_06() -> float:
    """Cima del biglietto nuovo mentre si scrive, sotto la pillola (una funzione: i testi si misurano solo dopo che
    ScenaReel ha registrato il font)."""
    return ALTO + pillola().altezza_px + 40


def biglietto_06(y: float, righe: int = 4) -> Biglietto:
    """Il biglietto nuovo con le prime `righe` righe; con tutte e 4, «Lei no.» acceso."""
    b = Biglietto(BIGLIETTO_NUOVO[:righe], y_px=y)
    if righe == 4:
        for i in LEI_NO:
            acceso(b.token()[i])
    return b


def extra_06(r: Scheda, bersaglio: Token, s: str):
    """Graffa accento sotto la riga del dettaglio (appena fuori dalla carta) e freccia verso «fotocopiatrice»."""
    g = Graffa(r.righe[0], s, direzione=DOWN, colore=P.accento)
    g.shift(DOWN * (g.graffa.get_top()[1] - r.box.get_bottom()[1] + px(10)))
    f = Freccia(g.etichetta.get_right() + RIGHT * px(16), bersaglio.get_top() + UP * px(4), colore=P.accento)
    return g, f


def stato_finale_06(s: str):
    """Ultimo fotogramma della 6: la richiesta con la riga del dettaglio, graffa e freccia, il biglietto sotto."""
    r6 = Scheda([DETTAGLIO])
    b6 = biglietto_06(Y_BIGLIETTO_6)
    g, f = extra_06(r6, b6.token()[3], s)
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
    """La richiesta di un biglietto originale; il biglietto si scrive fino a «capitolo», pausa col cursore (la camera
    si avvicina: il momento della prova), poi il resto mentre la camera torna (probabile)."""

    def costruisci(self):
        titolo, sotto = disposizione_01(TITOLO_1, SOTTO_1)   # ultimo fotogramma dell'hook
        barra, parola = barra_01(titolo)
        parola.set_opacity(0.45)
        self.add(titolo, barra, sotto)
        r, b = disposizione_02(self.area.contenuto)
        tok = b.token()
        primi, resto = tok[:7], tok[7:]                   # fino a «capitolo» / «e se ne apre…»
        self.play(*fuori(titolo, barra, sotto, shift=UP * 0.3), *dentro(*r.pezzi(), shift=UP * 0.2), run_time=0.5)

        self.beat(1)
        t1, d1 = self.t, self.durata_beat(1)
        self.play(*dentro(b.box, b.titolo, shift=UP * 0.2), run_time=0.4)
        self.attendi_fino(t1 + 0.25 * d1)                 # «Comincia così:», poi un cartellino per parola, lento
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in primi], lag_ratio=1.0),
                  run_time=self.arrotonda(0.55 * d1))
        cursore = cursore_dopo(primi[-1])
        cursore.add_updater(lampeggio())
        self.add(cursore)

        self.beat(2)
        t2, d2 = self.t, self.durata_beat(2)
        # il cambio grande: la camera si avvicina a «capitolo» e al cursore che lampeggia ancora (chi guarda la
        # finisce da solo); poi torna indietro mentre arriva il resto. Tutto dentro il beat: i controlli di fine
        # beat vedono la tela intera (con lo zoom la richiesta esce dallo schermo e sarebbe «testo-fuori»).
        self.play(self.zoom_area(VGroup(primi[-1], cursore), ZOOM_2), run_time=0.45)
        self.attendi_fino(t2 + 0.22 * d2)
        cursore.clear_updaters()
        self.remove(cursore)
        self.play(self.torna(), LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in resto], lag_ratio=0.6),
                  run_time=self.arrotonda(0.4 * d2))
        cornice, tag = extra_02(b, self.scena["testo"][0])
        self.play(Create(cornice), FadeIn(tag, scale=0.85), run_time=0.45)


class Scena03(Scena):
    """Una parola per volta: la frase si ricompone, le candidate dopo «capitolo», «e» (una tra le prime) va in coda."""

    def costruisci(self):
        r, b = disposizione_02(self.area.contenuto)       # ultimo fotogramma della scena 2
        cornice, tag = extra_02(b, TESTO_2)
        self.add(*r.pezzi(), b.box, b.titolo, *b.token(), cornice, tag)
        pil, bs, testa, cl = disposizione_03()
        primi = bs.token()[:7]
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
        e = cl.token(0, colore=P.accento)
        self.play(e.animate.move_to(bs.righe[2][0]), run_time=0.5)


class Scena04(Scena):
    """Il bivio dopo «capitolo»: la frase corre sul ramo spesso di «e»; torna un biglietto intero, scritto da lei (non
    pescato da un archivio); fluente sì, originale no."""

    def costruisci(self):
        pil, bs, testa, cl = disposizione_03()            # ultimo fotogramma della scena 3
        scelta(cl, 0)
        g = graffa_03(cl, TESTO_3)
        e = Token("e", colore=P.accento).move_to(bs.righe[2][0])
        primi = bs.token()[:7]
        self.add(*pil.pezzi(), *primi, testa, cl, g, e)

        # beat 0: tre rami da «capitolo», con la sola prima parola all'attacco
        cap = bs.righe[1][1]
        y_figli = y_px(cap.get_bottom()[1]) + 250
        fila = VGroup(*[Token(p) for p in BIGLIETTO[2]]).arrange(RIGHT, buff=px(GAP))
        fila.move_to(punto(X0 + PAD, y_figli), aligned_edge=UL)   # «e se ne apre uno nuovo.» sul ramo di «e»
        cont = list(fila[1:])
        ma = Token("ma").move_to([punto(520, 0)[0], fila.get_center()[1], 0])
        della = Token("della").move_to([punto(800, 0)[0], fila.get_center()[1], 0])
        origine = cap.get_bottom() + DOWN * px(8)

        def ramo(figlio, spessore):
            fine = figlio.get_top() + UP * px(8)
            h = origine[1] - fine[1]
            return CubicBezier(origine, origine + DOWN * h * 0.5, fine + UP * h * 0.5, fine,
                               stroke_color=P.attenuato, stroke_width=tratto(spessore))

        rami = [ramo(fila[0], 16), ramo(ma, 6), ramo(della, 3)]
        nota = testo("esempio: numeri inventati", "piede", colore=P.attenuato)
        nota.next_to(fila, DOWN, buff=px(40)).align_to(fila, LEFT)
        d0 = self.durata_beat(0)
        self.play(*fuori(testa, cl, g), run_time=0.25)   # prima esce la classifica, poi crescono i rami
        self.play(e.animate.move_to(fila[0]), *[Create(x) for x in rami], *dentro(ma, della, nota), run_time=0.6)
        self.attendi_fino(0.26 * d0)
        acceso = rami[0].copy().set_stroke(P.accento)     # la frase prende la strada più battuta
        self.play(Create(acceso), rami[1].animate.set_stroke(opacity=0.3), rami[2].animate.set_stroke(opacity=0.3),
                  run_time=0.35)
        self.play(*fuori(ma, della, rami[1], rami[2]), run_time=0.2)
        self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in cont], lag_ratio=0.8),
                  run_time=self.arrotonda(min(1.0, 0.25 * d0)))

        # beat 1: i rami spariscono, torna il biglietto intero; il database barrato diventa «scritto da lei»
        self.beat(1)
        t1, d1 = self.t, self.durata_beat(1)
        b4 = carta_04(pil)
        vecchi = primi + [e] + cont
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


class Scena05(Scena):
    """La richiesta torna intera: «Sii originale.» sposta appena le barre, il dettaglio vero le riordina («la» in
    testa)."""

    def costruisci(self):
        pil = pillola()                                   # ultimo fotogramma della scena 4
        b4 = carta_04(pil)
        lei, fl, orig, barra_orig = etichette_04(pil, b4, TESTO_4)
        self.add(*pil.pezzi(), b4.box, b4.titolo, *b4.token(), lei, fl, orig, barra_orig)
        r1, r2, r3 = carte_05()
        cl, testa = candidate_05()

        self.play(*fuori(b4.box, b4.titolo, *b4.token(), lei, fl, orig, barra_orig), run_time=0.3)
        self.play(cresce(pil.box, r1.box, r1.righe[0]), cl.entra(), FadeIn(testa), run_time=0.6)
        self.play(cresce(pil.box, r2.box, r2.righe[1]), run_time=0.4)
        self.play(cl.aggiorna(DOPO_SII, riordina=False), run_time=0.4)

        self.beat(1)
        t1, d1 = self.t, self.durata_beat(1)
        self.play(cresce(pil.box, r3.box, r3.righe[2]), run_time=0.5)
        self.attendi_fino(t1 + 0.28 * d1)                 # «…Marco litigava con la fotocopiatrice»
        self.play(cl.aggiorna(DOPO_DETTAGLIO), run_time=0.9)
        self.play(cl.scegli(2), run_time=0.4)
        # niente zoom qui (proposta delle note di produzione, provata): la carta larga 900 px sopra le barre resta
        # tagliata in alto e a destra a ogni ingrandimento, e il riordino si legge già a tela intera


class Scena06(Scena):
    """«la» parte dalla testa della colonna e vola nel biglietto nuovo, che si scrive e cresce con la voce; «LEI NO.» a
    tutto schermo; il biglietto scende, la richiesta torna con la riga del dettaglio: «l'hai messa tu»."""

    def costruisci(self):
        r3 = carte_05()[-1]                               # ultimo fotogramma della scena 5
        cl, testa = candidate_05(finale=True)
        self.add(*r3.pezzi(), testa, cl)
        pil = pillola()
        corto = biglietto_06(y_scrive_06(), righe=2)         # il biglietto mentre si scrive la prima frase
        b6 = biglietto_06(y_scrive_06())                     # intero (le posizioni dei cartellini sono le stesse)
        tok = b6.token()
        box = corto.box

        # beat 0: la richiesta si compatta in alto (resta il contesto); il biglietto si scrive con la voce; «la» parte
        # dalla testa della colonna e solo quando è arrivato la colonna esce (revisione T4)
        t0, d0 = self.t, self.durata_beat(0)
        self.play(Transform(r3.box, pil.box), *fuori(*r3.righe), run_time=0.4)
        self.attendi_fino(t0 + 0.15 * d0)                 # «Ora scrive:»
        self.play(*dentro(box, b6.titolo, shift=UP * 0.2), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tok[:2]], lag_ratio=0.6), run_time=0.4)
        la = Token("la", colore=P.accento).move_to(cl.barre[0].etichetta, aligned_edge=LEFT).set_z_index(1)
        self.attendi_fino(t0 + 0.34 * d0)                 # «la»
        self.play(FadeIn(la, scale=1.2), run_time=0.2)
        self.play(la.animate.move_to(tok[2]), run_time=0.45)
        self.play(*fuori(cl, testa, shift=DOWN * 0.2), FadeIn(tok[3], shift=UP * 0.15), run_time=0.35)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tok[4:8]], lag_ratio=0.6),
                  run_time=self.arrotonda(0.7))

        # beat 1: il biglietto cresce di due righe e si scrive con la voce
        self.beat(1)
        d1 = self.durata_beat(1)
        self.play(Transform(box, b6.box), la.box.animate.set_stroke(P.attenuato, width=tratto(3)), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tok[8:16]], lag_ratio=0.5),
                  run_time=self.arrotonda(min(1.3, 0.62 * d1)))

        # beat 2: il cambio grande; al ritorno il biglietto è intero, con «Lei no.» acceso
        self.beat(2)
        self.add(*[tok[i] for i in LEI_NO])               # entrano durante il taglio: al ritorno ci sono già
        self.punch_fino(grande(self.scena), 3)

        # beat 3: il biglietto scende; la richiesta torna con la riga del dettaglio; graffa e freccia
        self.beat(3)
        t3, d3 = self.t, self.durata_beat(3)
        self.attendi_fino(t3 + 0.3)                       # un attimo per vedere «Lei no.» nel biglietto
        r6 = Scheda([DETTAGLIO])
        giu = DOWN * px(Y_BIGLIETTO_6 - y_scrive_06())
        pezzi_b = [box, b6.titolo, tok[0], tok[1], la, *tok[3:]]
        self.play(cresce(r3.box, r6.box, r6.righe[0]), *[m.animate.shift(giu) for m in pezzi_b], run_time=0.6)
        g, f = extra_06(r6, tok[3], self.scena["testo"][0])
        self.attendi_fino(t3 + 0.52 * d3)                 # «…l'hai messa tu»
        self.play(g.entra(), run_time=0.45)
        self.play(f.entra(), run_time=0.4)


class Scena07(Scena):
    """Chiusura: l'IA e Marco con la linea interrotta; «TU SÌ»; la richiesta entra nel buco della linea e ci scivola la
    riga della fotocopiatrice; torna il biglietto con «Lei no.»; restano messaggio e CTA."""

    def costruisci(self):
        r6, b6, g, f = stato_finale_06(TESTO_6)           # ultimo fotogramma della scena 6
        self.add(*r6.pezzi(), b6.box, b6.titolo, *b6.token(), g, f)

        a = self.area.contenuto
        msg = Messaggio(self.scena["messaggio"].replace(". ", ".\n", 1), maiuscolo=False)   # «Tu sì.» su una riga sua
        msg.move_to(punto(X0, ALTO), aligned_edge=UL)
        righe = msg.righe
        fondo_msg = y_px(msg.get_bottom()[1])
        y_c = (fondo_msg + 40 + y_px(a.y0)) / 2           # centro del diagramma nello spazio sotto il messaggio
        bot, ia, user, marco, seg_sx, seg_dx, cx, w_carta = diagramma_07(a, y_c)
        vuota = carta_07(cx, y_c, w_carta)
        piena = carta_07(cx, y_c, w_carta, [DETTAGLIO])
        riga = piena.righe[0].set_color(P.accento)

        # beat 0: esce tutto; il messaggio si scrive con la voce; l'IA e Marco, fra loro la linea interrotta
        t0, d0 = self.t, self.durata_beat(0)
        self.play(*fuori(*r6.pezzi(), b6.box, b6.titolo, *b6.token(), g, f, shift=DOWN * 0.2), run_time=0.3)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in righe[:2]], lag_ratio=0.3), bot.entra(), FadeIn(ia),
                  run_time=0.5)
        self.play(user.entra(), FadeIn(marco), Create(seg_sx), Create(seg_dx), run_time=0.45)

        # beat 1: il cambio grande; al ritorno il messaggio ha anche «Tu sì.»
        self.beat(1)
        self.add(righe[2])
        self.punch_fino(grande(self.scena), 2)

        # beat 2: una linea accento dal presentatore a Marco; la richiesta entra nel buco della linea e ci scivola,
        # da Marco, la riga della fotocopiatrice: l'IA arriva a Marco solo da quello che scrivi (revisione T13)
        self.beat(2)
        t2, d2 = self.t, self.durata_beat(2)
        riq = self.area.riquadro
        fine = marco.get_bottom() + DOWN * px(14)
        verso = (fine - riq.centro) / np.linalg.norm(fine - riq.centro)
        inizio = riq.centro + verso * (riq.larghezza / 2 + px(18))
        linea = Line(inizio, fine, stroke_color=P.accento, stroke_width=tratto(6))
        self.play(Create(linea), run_time=0.35)
        self.attendi_fino(t2 + 0.2 * d2)                  # «nella richiesta»
        self.play(FadeIn(vuota.box, scale=0.9), FadeIn(vuota.titolo), run_time=0.3)
        self.attendi_fino(t2 + 0.38 * d2)                 # «quello che sai solo tu»
        self.play(LaggedStart(AnimationGroup(Transform(vuota.box, piena.box), Transform(vuota.titolo, piena.titolo)),
                              FadeIn(riga, shift=LEFT * 0.4), lag_ratio=0.35, group=vuota.box), run_time=0.55)

        # beat 3: torna per un attimo il biglietto con «Lei no.» acceso; poi restano messaggio e CTA, centrati
        self.beat(3)
        t3, d3 = self.t, self.durata_beat(3)
        bb = biglietto_06(Y_BIGLIETTO_6)
        diagramma = [bot, ia, user, marco, seg_sx, seg_dx, linea, vuota.box, vuota.titolo, riga]
        self.play(*fuori(*diagramma, shift=DOWN * 0.2), *dentro(bb.box, bb.titolo, *bb.token(), shift=UP * 0.2),
                  run_time=0.4)
        cta = Etichetta(self.scena["cta"])
        h = msg.height + px(50) + cta.height
        dy = (a.centro[1] + h / 2) - msg.get_top()[1]     # sposta il messaggio: messaggio + CTA centrati nell'area
        cta.move_to(punto(X0, 0), aligned_edge=LEFT).set_y(msg.get_bottom()[1] + dy - px(50) - cta.height / 2)
        self.attendi_fino(t3 + 0.5 * d3)                  # «…la fotocopiatrice»
        self.play(*fuori(bb.box, bb.titolo, *bb.token(), shift=DOWN * 0.2), *[r.animate.shift(UP * dy) for r in righe],
                  FadeIn(cta, shift=UP * 0.2), run_time=0.5)
