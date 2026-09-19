"""Animazioni di «Generativa non vuol dire creativa» (contenuti/sceneggiature/2026-09-15-generativa-probabile.md).

La storia è una mail di candidatura ad «Acme Arredi» (annuncio inventato). Testi del modello solo dalle uscite di
contenuti/idee/uscite/generativa-probabile-2026-09-16.md: A1 (scene 1-3), B2 (scena 4), C4 (scene 5-7); frammenti A2,
A4, A6, A9 (scena 2), B1, B4, B3 (scena 4). Mai nomi, firme o email a schermo.

Il filo visivo, tre oggetti con lo stesso aspetto per tutto il reel:
- la carta «richiesta» (bordo secondario): intera con l'annuncio agganciato (hook, scene 4 e 5), compatta a pillola in
  alto a sinistra (scene 2-4), compatta con la riga del fatto in alto (scene 5-6); A → B («Sii originale.») → C (il
  fatto), parola per parola;
- la mail (bordo terziario): si ferma due volte sullo stesso gesto, cartellini e cursore (scene 1 e 5); il testo di
  un'uscita esce del tutto prima che entri quello dell'altra; da piccola diventa una sagoma senza testo leggibile;
- la colonna delle candidate (`Classifica` larga 300 px, sotto la riga in scrittura): scene 3 e 6.
Il cartellino del loop «parla di te?» sta in alto a destra (scene 2-5), poi appeso all'angolo della mail nuova.

Mosse wow (manuale §11bis), una per scena: 1 viaggio (il corpo della mail scorre veloce fino all'ultima riga);
2 punch «COLLOQUIO»; 3 metamorfosi e zoom 1,8× (la frase si riduce a gettoni vuoti, resta «per un ▌», la colonna);
4 punch «DIVANO»; 5 rivelazione a tratto (la riga «Sii originale.» parte con una carica, al suo posto si disegna la
riga vuota); 6 contrasto di scala («2.100» esce enorme dal cursore nel vuoto e ci rientra); 7 moltiplicazione (un
muro di 24 sagome dietro la prima mail).

Posizioni in px della tela (origine in alto a sinistra) con `punto()`; area contenuto 60..960 × 220..1196 px
(hook: 220..1580). Testi misurati solo dentro le funzioni (il font si registra con la scena).
"""
from __future__ import annotations

import re

import numpy as np
from manim import (BOLD, DOWN, LEFT, PI, RIGHT, UL, UP, Create, DashedLine, FadeIn, FadeOut, FadeTransform,
                   GrowFromCenter, GrowFromEdge, MoveToTarget, Rectangle, RoundedRectangle, Transform, Triangle,
                   UpdateFromAlphaFunc, VGroup, VMobject, linear, rate_functions, smooth, squish_rate_func)
from manim.utils.family import extract_mobject_family_members

from tools.anim.base import ScenaReel
from tools.anim.componenti import (Classifica, Etichetta, Evidenzia, Messaggio, Punch, Riga, Titolo, Token, piano,
                                   testo, tratto)
from tools.anim.config import carica
from tools.anim.controlli import Violazione
from tools.anim.diagrammi import Graffa
from tools.anim.misure import PX_PER_UNITA, px

CFG = carica()
P = CFG.palette
K = PX_PER_UNITA

ease_out_back = rate_functions.ease_out_back
ease_in_back = rate_functions.ease_in_back
ease_out_expo = rate_functions.ease_out_expo
ease_out_cubic = rate_functions.ease_out_cubic
rush_into = rate_functions.rush_into
there_and_back = rate_functions.there_and_back

# --- testi -------------------------------------------------------------------------------------------------------
# la richiesta (A, B = A + «Sii originale.», C = A + il fatto): contenuti/idee/uscite/generativa-probabile-2026-09-16.md
RICHIESTA = "Scrivi la mail per candidarmi a questo annuncio."
ANNUNCIO = ("«==Acme Arredi== (Padova) cerca un addetto o un'addetta marketing. Gestirai social, newsletter e promozioni "
            "nei negozi. Chiediamo due anni di esperienza e una scrittura chiara. Contratto a tempo indeterminato.»")
ETICHETTA_ANNUNCIO = "annuncio · inventato"
SII = "Sii originale."
FATTO = ("Nel mio lavoro attuale ho portato la newsletter di un negozio di biciclette da 300 a 2.100 iscritti in un "
         "anno.")
FATTO_4 = "Nel mio lavoro attuale ho portato\nla newsletter di un negozio di biciclette\nda 300 a 2.100\niscritti in un anno."
NOTA_FATTO = "esempio: candidato inventato"
# A1 (Opus): oggetto senza nome, saluto, segnaposto, ultima riga del corpo
OGGETTO_A = "**Oggetto:** Candidatura per la posizione di addetto marketing"
SALUTO_A = "Gentile responsabile della selezione,"
CHIUSA_A = ["Allego", "il", "mio", "curriculum", "e", "resto", "a", "disposizione", "per", "un", "colloquio."]
CHIUSA_A_TESTO = "Allego il mio curriculum e resto a disposizione per un colloquio."
NUMERO_A = "Ho [numero] anni di esperienza nel marketing, maturata presso [azienda/e]."
ATTIRA_A = "[… cosa vi attira di Acme Arredi …]"        # taglio nostro della riga [Facoltativo: …] (Note di produzione)
FRAMMENTI_A = ["resto a disposizione per un colloquio, anche online",           # A2
               "Sarei felice di approfondire la mia candidatura in un colloquio",  # A4
               "Resto a disposizione per un eventuale colloquio conoscitivo",    # A6
               "Resto a disposizione per un colloquio conoscitivo"]              # A9 (seguito tagliato)
# B2 (Opus): oggetto senza «– Nome Cognome», saluto, attacco, segnaposto, chiusa
OGGETTO_B = "**Oggetto:** Candidatura per il ruolo di addetto marketing"
SALUTO_B = "Gentile team di Acme Arredi,"
ATTACCO_B = "nessuno compra un divano per le sue misure."
NEGLI_B = "Negli ultimi [numero] anni ho lavorato come [ruolo] presso [azienda]."
CHIEDO_B = "…e la cosa che vi chiedo è un colloquio."
FRAMMENTI_B = ["un divano si compra in negozio",        # B1 (seguito tagliato)
               "un divano non si vende con un post"]    # B4
FRAMMENTO_B3 = "nessuno compra un divano per le sue misure"   # B3, prima frase identica a quella di B2
# C4 (Opus): oggetto (uguale a quello di A1), saluto, la riga del numero, un segnaposto, la chiusa
OGGETTO_C = OGGETTO_A
SALUTO_C = "Gentile team di Acme Arredi,"
RIGA_C = ["in", "un", "anno", "ho", "portato", "gli", "iscritti", "da", "300", "a", "2.100."]
RIGA_C_TESTO = "in un anno ho portato gli iscritti da 300 a 2.100."
ANNI_C = "…da [numero] anni."
SARE_C = "Sarei felice di approfondire la mia candidatura in un colloquio."
# colonne (esempio: numeri inventati; «colloquio» e «2.100» sono le parole vere)
CANDIDATE_3 = [("colloquio", 0.62), ("incontro", 0.18), ("confronto", 0.09)]
CANDIDATE_6 = [("2.100", 0.71), ("500", 0.09), ("1.000", 0.07)]
LOOP = "parla di te?"
TESTO_3 = ["fluente", "non gliel'hai detto"]
TESTO_6 = ["dopo il tuo numero", "l'hai messo tu"]

# --- misure (px della tela) --------------------------------------------------------------------------------------
X0, X1 = 60, 960
LARG = 900
ALTO = 232            # cima della fascia alta
Y_MAIL = 400          # cima della mail sotto la pillola (scene 2-4)
Y_CARTA = 340         # cima della carta intera al centro (scene 4-5)
Y_MAIL_C = 650        # cima della mail C4 sotto la carta col fatto (scene 5-6)
GAP = 16              # fra i cartellini
LARG_COL = 300        # barre della colonna delle candidate
ZOOM = 1.8
SCALA_TITOLO = 0.72   # il titolo dell'hook dopo 0,5 s (104 → 75 px)
PAUSA_FRASI_S = 0.3


def punto(x: float, y: float) -> np.ndarray:
    return np.array([px(x) - CFG.frame_width / 2, CFG.frame_height / 2 - px(y), 0.0])


def y_px(y: float) -> float:
    return (CFG.frame_height / 2 - y) * K


def x_px(x: float) -> float:
    return (x + CFG.frame_width / 2) * K


def alto(m) -> float:
    return y_px(m.get_top()[1])


def fondo(m) -> float:
    return y_px(m.get_bottom()[1])


def sinistra(m) -> float:
    return x_px(m.get_left()[0])


def destra(m) -> float:
    return x_px(m.get_right()[0])


def h(m) -> float:
    return m.height * K


def a_ul(m, x: float, y: float):
    return m.move_to(punto(x, y), aligned_edge=UL)


def fuori(*mobs, **kw) -> list:
    """Un FadeOut per pezzo (un FadeOut di un VGroup nuovo lascerebbe in scena i pezzi, trasparenti)."""
    return [FadeOut(m, **kw) for m in mobs]


def dentro(*mobs, **kw) -> list:
    return [FadeIn(m, **kw) for m in mobs]


def fra(a: float, b: float = 1.0, f=smooth):
    """Curva `f` compressa nella frazione [a, b] della play: più movimenti sfalsati in un solo passaggio."""
    return squish_rate_func(f, max(0.0, a), min(1.0, b))


def carica(t: float, c: float = 0.9) -> float:
    """Come `ease_in_back` ma con l'arretramento più corto (minimo ≈ −0,03 invece di −0,1): per le corse lunghe."""
    return (c + 1) * t ** 3 - c * t ** 2


def grande(scena: dict) -> str:
    for s in scena.get("animazione") or []:
        m = re.search(r"GRANDE:\s*«(.+?)»", s)
        if m:
            return m.group(1)
    raise ValueError("nessuna riga ANIMAZIONE con «GRANDE: «…»»")


def riquadro(larghezza_px: float, altezza_px: float, colore: str, z: int = -1, raggio: float = 28) -> RoundedRectangle:
    return RoundedRectangle(corner_radius=px(raggio), width=px(larghezza_px), height=px(altezza_px),
                            stroke_color=colore, stroke_width=tratto(3), fill_color=P.sfondo,
                            fill_opacity=1).set_z_index(z)


def barra(larghezza_px: float, alt: float = 18, opacita: float = 0.35) -> RoundedRectangle:
    return RoundedRectangle(corner_radius=px(alt / 2), width=px(larghezza_px), height=px(alt), stroke_width=0,
                            fill_color=P.attenuato, fill_opacity=opacita)


def barre(larghezze, alt: float = 18, gap: float = 22) -> VGroup:
    return VGroup(*[barra(w, alt) for w in larghezze]).arrange(DOWN, buff=px(gap), aligned_edge=LEFT)


def pseudo(k: int) -> float:
    """Numero fra 0 e 1, deterministico (per le sagome simili ma non uguali)."""
    return (np.sin(k * 12.9898 + 78.233) * 43758.5453) % 1.0


# --- cartellini, cursore, frecce ---------------------------------------------------------------------------------

def acceso(t: Token) -> Token:
    t.box.set_stroke(P.accento, width=tratto(5))
    t.testo.set_color(P.accento)
    return t


def cursore() -> Rectangle:
    return Rectangle(width=px(8), height=px(56), stroke_width=0, fill_color=P.accento, fill_opacity=1).set_z_index(2)


def dopo_di(c: Rectangle, m, buff_px: float = 14) -> Rectangle:
    return c.move_to([m.get_right()[0] + px(buff_px) + c.width / 2, m.get_center()[1], 0])


def lampeggio(periodo: float = 0.8):
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


def fila(parole: list[str], x: float, y: float, larghezza_px: float = 820) -> list[Token]:
    """Cartellini che vanno a capo entro larghezza_px, con l'angolo in alto a sinistra in (x, y)."""
    toks = [Token(p) for p in parole]
    cx, cy = x, y
    for t in toks:
        w = t.width * K
        if cx > x and cx + w > x + larghezza_px:
            cx, cy = x, cy + t.height * K + GAP
        a_ul(t, cx, cy)
        cx += w + GAP
    return toks


def gettone(t: Token, larghezza_px: float = 30) -> RoundedRectangle:
    """Il cartellino ridotto a gettone vuoto (la parola già scritta): stesso bordo, niente testo."""
    g = RoundedRectangle(corner_radius=px(8), width=px(larghezza_px), height=px(40), stroke_color=P.attenuato,
                         stroke_width=tratto(3), fill_color=P.sfondo, fill_opacity=1)
    return g


def freccia_gomito(punti: list[np.ndarray], colore: str | None = None, spessore_px: float = 6) -> VGroup:
    """Freccia a spezzata (punti in unità): il tratto e la punta sull'ultimo punto."""
    col = colore or P.accento
    fine, prima = punti[-1], punti[-2]
    d = (fine - prima) / np.linalg.norm(fine - prima)
    lung = px(30)
    linea = VMobject(stroke_color=col, stroke_width=tratto(spessore_px))
    linea.set_points_as_corners([*punti[:-1], fine - d * lung * 0.8])
    punta = Triangle(fill_color=col, fill_opacity=1, stroke_width=0).scale_to_fit_width(px(30))
    punta.stretch_to_fit_height(lung)
    punta.rotate(np.arctan2(d[1], d[0]) - PI / 2)
    punta.shift(fine - punta.get_vertices()[0])
    g = VGroup(linea, punta)
    g.linea, g.punta = linea, punta
    return g


class Cartellino(VGroup):
    """Etichetta piccola (corpo `piede`) a contorno: il loop «parla di te?». acceso: pieno in accento."""

    def __init__(self, s: str, acceso_: bool = False, colore: str | None = None):
        super().__init__()
        col = colore or (P.accento if acceso_ else P.attenuato)
        self.testo = testo(s, "piede", colore=P.sfondo if acceso_ else col, peso=BOLD)
        alt = self.testo.height + px(32)
        self.box = RoundedRectangle(corner_radius=alt / 2, width=self.testo.width + px(48), height=alt,
                                    stroke_color=col, stroke_width=tratto(3), fill_color=col if acceso_ else P.sfondo,
                                    fill_opacity=1)
        self.add(self.box, self.testo.move_to(self.box))
        self.set_z_index(3)


def loop_in_alto(acceso_domanda: bool = False) -> Cartellino:
    c = Cartellino(LOOP[:-1] + "==?==" if acceso_domanda else LOOP)
    return c.move_to([punto(X1, 0)[0] - c.width / 2, punto(0, ALTO)[1] - c.height / 2, 0])


def loop_sulla_mail(box, s: str = LOOP, acceso_: bool = False) -> Cartellino:
    c = Cartellino(s, acceso_=acceso_)
    return c.move_to([box.get_right()[0] - px(24) - c.width / 2, box.get_top()[1], 0])


# --- la carta «richiesta» ----------------------------------------------------------------------------------------

class Carta:
    """La carta «richiesta» a pezzi. modo: «intera» (richiesta + annuncio agganciato, riga extra opzionale),
    «pillola» (titolo e «annuncio · inventato» in due righe), «fatto» (titolo e annuncio in una riga, nota, fatto in
    quattro righe). Tutti i pezzi esistono in tutti i modi (quelli che non servono restano fuori scena)."""

    def __init__(self, modo: str, y: float = ALTO, extra: str | None = None, colore_extra: str | None = None,
                 extra_blocco=None):
        self.modo = modo
        self.titolo = testo("richiesta", "etichetta", colore=P.secondario, peso=BOLD)
        self.extra = None
        if modo == "intera":
            pad = 36
            self.riga = testo(RICHIESTA, "token", larghezza_px=LARG - 2 * pad)
            self.et_ann = testo(ETICHETTA_ANNUNCIO, "etichetta", colore=P.attenuato, peso=BOLD)
            self.annuncio = testo(ANNUNCIO, "piede", colore=P.attenuato, larghezza_px=LARG - 2 * pad - 40)
            yy = y + pad
            a_ul(self.titolo, X0 + pad, yy)
            yy += h(self.titolo) + 14
            a_ul(self.riga, X0 + pad, yy)
            yy += h(self.riga) + 14
            ys = yy
            a_ul(self.et_ann, X0 + pad + 20, yy + 18)
            a_ul(self.annuncio, X0 + pad + 20, yy + 18 + h(self.et_ann) + 8)
            yy = fondo(self.annuncio) + 18
            self.box_ann = riquadro(LARG - 2 * pad, yy - ys, P.attenuato, z=-1, raggio=20)
            a_ul(self.box_ann, X0 + pad, ys)
            self.box_ann.set_stroke(width=tratto(2))
            if extra is not None or extra_blocco is not None:
                self.extra = extra_blocco if extra_blocco is not None else testo(
                    extra, "token", colore=colore_extra, larghezza_px=LARG - 2 * pad)
                a_ul(self.extra, X0 + pad, yy + 14)
                yy = fondo(self.extra)
            self.box = a_ul(riquadro(LARG, yy + pad - y, P.secondario), X0, y)
        elif modo == "pillola":
            pad = 28
            self.et_ann = testo(ETICHETTA_ANNUNCIO, "piede", colore=P.attenuato)
            a_ul(self.titolo, X0 + pad, y + pad)
            a_ul(self.et_ann, X0 + pad, fondo(self.titolo) + 8)
            larg = max(self.titolo.width, self.et_ann.width) * K + 2 * pad
            self.box = a_ul(riquadro(larg, fondo(self.et_ann) + pad - y, P.secondario), X0, y)
        else:   # fatto
            pad = 24
            self.et_ann = testo(ETICHETTA_ANNUNCIO, "piede", colore=P.attenuato)
            a_ul(self.titolo, X0 + pad, y + pad)
            self.et_ann.move_to([punto(X0 + pad, 0)[0] + self.titolo.width + px(24) + self.et_ann.width / 2,
                                 self.titolo.get_center()[1], 0])
            self.nota = testo(NOTA_FATTO, "piede", colore=P.attenuato)
            a_ul(self.nota, X0 + pad, fondo(self.titolo) + 12)
            self.extra = testo(FATTO_4, "token", colore=P.accento)
            # gli a capo di FATTO_4 sono fissi (la scena 6 conta sulla riga «da 300 a 2.100»): a 44 px la riga della
            # newsletter è larga 867 px e a destra restavano 9 px contro i 24 di sinistra. Il corpo scende di quel che
            # basta (44 → ~43 px) perché la riga più lunga stia fra i due margini uguali; `reimpagina` porta il corpo
            larg_utile = LARG - 2 * pad
            if self.extra.width * K > larg_utile:
                self.extra.scale((larg_utile - 2) / (self.extra.width * K))
            a_ul(self.extra, X0 + pad, fondo(self.nota) + 12)
            self.box = a_ul(riquadro(LARG, fondo(self.extra) + pad - y, P.secondario), X0, y)

    def pezzi(self) -> list:
        out = [self.box, self.titolo, self.et_ann]
        if self.modo == "intera":
            out += [self.riga, self.box_ann, self.annuncio]
        if self.modo == "fatto":
            out += [self.nota]
        if self.extra is not None:
            out.append(self.extra)
        return out


def glifi(blocco) -> list:
    """I glifi di un Blocco in ordine di lettura (stesso testo con altri a capo: stessi glifi, altri posti)."""
    return [g for r in blocco.righe for g in r.glifi.submobjects]


def spento(m, scala: float = 1.0):
    """Copia trasparente di un riquadro (per farlo sparire in un posto e ricomparire in un altro senza traversate)."""
    return m.copy().set_fill(opacity=0).set_stroke(opacity=0).scale(scala)


def a_tappe(mob, stati: list, confini: list[float], curve: list | None = None) -> UpdateFromAlphaFunc:
    """`mob` passa per gli `stati` (copie con la stessa struttura e gli stessi punti), raggiunti alle frazioni `confini`
    della play; prima del primo confine resta nel primo stato, dopo l'ultimo nell'ultimo. Una sola animazione per
    oggetto anche quando il percorso ha più tratti (due animazioni sullo stesso oggetto nella stessa play non si
    sommano). Un tratto fra due stati trasparenti non si vede: è il modo di cambiare posto senza attraversare nulla."""
    curve = curve or [ease_out_cubic] * (len(stati) - 1)
    pezzi = [m.family_members_with_points() for m in (mob, *stati)]
    for p_ in pezzi[1:]:
        if len(p_) != len(pezzi[0]) or any(len(x.points) != len(y.points) for x, y in zip(pezzi[0], p_)):
            raise ValueError("a_tappe: gli stati non hanno la stessa struttura dell'oggetto")

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


def righe_dei_glifi(blocco) -> list[int]:
    return [k for k, r in enumerate(blocco.righe) for _ in r.glifi.submobjects]


def reimpagina(da, a, c0: float, c1: float, c2: float, corpo_rigido: bool = False) -> list:
    """Stesso testo, altri a capo (e, se serve, altro corpo e altro posto), senza che due parole si attraversino.
    Fra c0 e c1 ogni glifo va alla x e al corpo d'arrivo restando sulla sua riga di partenza (le righe restano
    separate); fra c1 e c2 chi sale di riga sale in verticale. Chi scende di riga: se la riga d'arrivo è nuova, scende
    in verticale e poi scorre lungo la riga; se è già occupata, si spegne dov'è e si riaccende al suo posto."""
    gs, gt = VGroup(*glifi(da)), VGroup(*glifi(a))
    gs.align_data(gt)
    s0, t = list(gs.copy()), list(gt.copy())
    rs, rt = righe_dei_glifi(da), righe_dei_glifi(a)
    passo = (a.righe[0].get_center()[1] - a.righe[1].get_center()[1]) if len(a.righe) > 1 else 0.0
    primo = {r: rs.index(r) for r in set(rs)}                      # il primo glifo di ogni riga di partenza
    d = c2 - c1
    corpo = sum(g.height for g in t) / max(sum(g.height for g in s0), 1e-9)
    gruppi: dict = {}
    for k in range(len(s0)):
        if rs[k] >= rt[k]:
            modo = "su"
        else:
            modo = "lampo" if any(rs[j] == rt[j] == rt[k] for j in range(len(s0))) else "gomito"
        gruppi.setdefault((modo, rs[k], rt[k]), []).append(k)
    anims = []
    for (modo, r_s, r_t), idx in gruppi.items():
        mob = VGroup(*[gs[k] for k in idx])
        parte = VGroup(*[s0[k] for k in idx])
        arrivo = VGroup(*[t[k] for k in idx])
        if modo == "su":
            mezzo = arrivo.copy().shift(DOWN * passo * (r_s - r_t))
            anims.append(a_tappe(mob, [parte, mezzo, arrivo], [c0, c1, c2], [ease_out_cubic, smooth]))
            continue
        k0 = primo[r_s]
        rigido = parte.copy()
        if corpo_rigido:   # anche chi scende prende il corpo d'arrivo: sennò si stacca dalla sua riga, che si stringe
            rigido.scale(corpo, about_point=s0[k0].get_center())
        rigido.shift(t[k0].get_center() - s0[k0].get_center())
        if modo == "gomito":
            giu = rigido.copy().shift(DOWN * passo * (r_t - r_s))
            anims.append(a_tappe(mob, [parte, rigido, giu, arrivo], [c0, c1, c1 + 0.4 * d, c2],
                                 [ease_out_cubic, smooth, smooth]))
        else:
            anims.append(a_tappe(mob, [parte, rigido, rigido.copy().set_fill(opacity=0),
                                       arrivo.copy().set_fill(opacity=0), arrivo],
                                 [c0, c1, c1 + 0.3 * d, c1 + 0.6 * d, c2], [ease_out_cubic, linear, linear, linear]))
    return anims


def riga_numero(carta: Carta):
    """La riga «da 300 a 2.100» della carta col fatto."""
    return carta.extra.righe[2]


# --- la mail -----------------------------------------------------------------------------------------------------

class Mail:
    """La mail a pezzi: riquadro, titolo «mail» e voci impilate [(chiave, mob, spazio_prima_px)]; i cartellini
    (chiave «fila») stanno sulla loro griglia fissa da (X0 + pad, y)."""

    def __init__(self, voci: list, y: float, x: float = X0, larghezza: float = LARG, pad: float = 36,
                 titolo: bool = True, fondo_min: float | None = None):
        self.p = {}
        self.titolo = testo("mail", "etichetta", colore=P.terziario, peso=BOLD) if titolo else None
        yy = y + pad
        if self.titolo is not None:
            a_ul(self.titolo, x + pad, yy)
            yy += h(self.titolo)
        for chiave, mob, spazio in voci:
            yy += spazio
            if isinstance(mob, list):         # cartellini già disposti a partire da (0, 0)
                for t in mob:
                    t.shift(punto(x + pad, yy) - punto(0, 0))
                yy = max(fondo(t) for t in mob)
            else:
                a_ul(mob, x + pad, yy)
                yy += h(mob)
            self.p[chiave] = mob
        yy += pad
        if fondo_min is not None:
            yy = max(yy, fondo_min)
        self.box = a_ul(riquadro(larghezza, yy - y, P.terziario), x, y)

    def testi(self) -> list:
        out = []
        for m in self.p.values():
            out += m if isinstance(m, list) else [m]
        return ([self.titolo] if self.titolo is not None else []) + out

    def pezzi(self) -> list:
        return [self.box, *self.testi()]


def fila0(parole: list[str], larghezza_px: float = 828) -> list[Token]:
    return fila(parole, 0, 0, larghezza_px)


def finestra_barre(n: int, seme: int = 0) -> VGroup:
    return barre([520 + 300 * pseudo(seme + k) for k in range(n)], gap=26)


def mail_a1(y: float, n_barre: int = 2, parole: int = 11, oggetto: bool = True) -> Mail:
    """A1 con la chiusa a cartellini (le prime `parole`)."""
    voci = []
    if oggetto:
        voci.append(("oggetto", testo(OGGETTO_A, "piede", larghezza_px=828), 16))
    voci.append(("saluto", testo(SALUTO_A, "token"), 12))
    voci.append(("finestra", finestra_barre(n_barre), 22))
    voci.append(("fila", fila0(CHIUSA_A)[:parole], 22))
    m = Mail(voci, y)
    if parole < len(CHIUSA_A):      # il riquadro ha già il posto della riga dove arriverà la parola
        m.box = a_ul(riquadro(LARG, fondo(m.p["fila"][-1]) + 36 - y, P.terziario), X0, y)
    return m


def mail_a1_corpo(y: float) -> Mail:
    """A1 al corpo (scena 3): i segnaposto e l'ultima riga, fra righe grigie."""
    return Mail([("b1", barre([640]), 22), ("numero", testo(NUMERO_A, "token", larghezza_px=828), 22),
                 ("b2", barre([560]), 22), ("attira", testo(ATTIRA_A, "token"), 22),
                 ("chiusa", testo(CHIUSA_A_TESTO, "token", colore=P.attenuato, larghezza_px=828), 22)], y)


def mail_b2(y: float, corpo: bool = False) -> Mail:
    attacco = testo(ATTACCO_B.replace("divano", "==divano==", 1), "token", larghezza_px=828)
    if not corpo:
        return Mail([("oggetto", testo(OGGETTO_B, "piede", larghezza_px=828), 16),
                     ("saluto", testo(SALUTO_B, "token"), 16), ("attacco", attacco, 16)], y)
    return Mail([("saluto", testo(SALUTO_B, "token"), 16), ("attacco", attacco, 16),
                 ("b1", barre([600]), 22), ("negli", testo(NEGLI_B, "token", larghezza_px=828), 22),
                 ("b2", barre([520]), 22), ("chiedo", testo(CHIEDO_B, "token", larghezza_px=828), 22)], y)


def mail_c4(y: float, parole: int = 10, oggetto: bool = True, acceso_: bool = False) -> Mail:
    voci = []
    if oggetto:
        voci.append(("oggetto", testo(OGGETTO_C, "piede", larghezza_px=828), 16))
    voci += [("saluto", testo(SALUTO_C, "token"), 12), ("finestra", barre([700, 560], gap=20), 20),
             ("fila", fila0(RIGA_C)[:parole], 20)]
    m = Mail(voci, y)
    if acceso_ and parole == len(RIGA_C):
        acceso(m.p["fila"][-1])
    return m


def miniatura(x: float, y: float, larghezza: float = 320, seme: int = 0, token: str | None = None,
              titolo: bool = True, n: int = 5) -> Mail:
    """La mail piccola: una sagoma con righe grigie (niente testo leggibile), col titolo e, se c'è, un cartellino."""
    voci = [("barre", barre([(larghezza - 72) * (0.55 + 0.45 * pseudo(seme + k)) for k in range(n)], gap=22), 20)]
    if token:
        voci.append(("token", [a_ul(acceso(Token(token)), 0, 0)], 24))
    return Mail(voci, y, x=x, larghezza=larghezza, titolo=titolo)


def sagoma(x: float, y: float, larghezza: float, altezza: float, seme: int) -> VGroup:
    """Una copia grigia: riquadro, una barra spessa (il saluto) e 3-4 righe di lunghezze diverse. Nessun testo."""
    box = riquadro(larghezza, altezza, P.attenuato, z=-3, raggio=16)
    a_ul(box, x, y)
    pad = 14
    w = larghezza - 2 * pad
    n = 3 + int(pseudo(seme) > 0.5)
    lunghe = [w * (0.35 + 0.2 * pseudo(seme + 1))] + [w * (0.55 + 0.45 * pseudo(seme + 2 + k)) for k in range(n)]
    righe = VGroup(*[barra(l, alt=10 if k else 14, opacita=0.45 if k else 0.6) for k, l in enumerate(lunghe)])
    righe.arrange(DOWN, buff=px((altezza - 2 * pad - 14 - 10 * n) / n), aligned_edge=LEFT)
    a_ul(righe, x + pad, y + pad)
    righe.set_z_index(-2)
    return VGroup(box, righe)


# --- impaginazioni condivise fra una scena e la successiva --------------------------------------------------------

def disposizione_01(titolo_s: str):
    """Hook. Ultimo fotogramma (la copertina): titolo ridotto in alto, pillola, mail A1 con la finestra di righe e i
    cartellini fino a «per un»."""
    tit = Titolo(titolo_s)
    tit.scale(SCALA_TITOLO)
    prova_p = Carta("pillola")
    prova_m = mail_a1(0, n_barre=5, parole=10)
    tot = h(tit) + 44 + h(prova_p.box) + 44 + h(prova_m.box)
    a_ul(tit, X0, 220 + (1360 - tot) / 2)
    pil = Carta("pillola", y=fondo(tit) + 44)
    m = mail_a1(fondo(pil.box) + 44, n_barre=5, parole=10)
    return tit, pil, m


def stato_02():
    """Ultimo fotogramma della scena 2: pillola, loop in alto, mail A1 intera con «colloquio.»."""
    pil = Carta("pillola")
    m = mail_a1(Y_MAIL)
    return pil, loop_in_alto(), m


def stato_03():
    """Ultimo fotogramma della scena 3: la mail al corpo con i tre segnaposto accesi e le due etichette sotto."""
    pil = Carta("pillola")
    m = mail_a1_corpo(Y_MAIL)
    segn = [m.p["numero"].parola("[numero]"), m.p["numero"].parola("[azienda/e]"), m.p["attira"].righe[0].glifi]
    riq = [Evidenzia(s, buff=px(8)) for s in segn]
    fl = Etichetta(TESTO_3[0], colore=P.terziario)
    nd = Etichetta(TESTO_3[1])
    VGroup(fl, nd).arrange(RIGHT, buff=px(30))
    a_ul(VGroup(fl, nd), X0, fondo(m.box) + 30)
    return pil, loop_in_alto(), m, segn, riq, fl, nd


def carta_04(extra: bool = False) -> Carta:
    return Carta("intera", y=Y_CARTA, extra=SII if extra else None, colore_extra=P.accento)


def pillola_mail() -> Mail:
    return Mail([], ALTO, larghezza=78 + 2 * 24, pad=24)


def stato_04():
    """Ultimo fotogramma della scena 4: pillola, loop, mail B2 al corpo con i segnaposto accesi e la chiusa accesa."""
    pil = Carta("pillola")
    m = mail_b2(Y_MAIL, corpo=True)
    segn = [m.p["negli"].parola("[numero]"), m.p["negli"].parola("[azienda]")]
    riq = [Evidenzia(s, buff=px(8)) for s in segn]
    nd = a_ul(Etichetta(TESTO_3[1]), X0, fondo(m.box) + 30)
    chiedo = VGroup(*glifi(m.p["chiedo"])[2:])            # «la cosa che vi chiedo è un colloquio.» (senza «…e»)
    return pil, loop_in_alto(), m, segn, riq, nd, chiedo


def stato_05():
    """Ultimo fotogramma della scena 5 (con il cursore dopo «a»)."""
    carta = Carta("fatto")
    m = mail_c4(Y_MAIL_C)
    return carta, m, loop_sulla_mail(m.box)


def graffa_06(carta: Carta, s: str) -> Graffa:
    return Graffa(riga_numero(carta), s, direzione=RIGHT, colore=P.accento)


def stato_06(testo_graffa: str):
    carta = Carta("fatto")
    m = mail_c4(Y_MAIL_C, parole=11)
    g = graffa_06(carta, testo_graffa)
    tag = loop_sulla_mail(m.box, LOOP.rstrip("?"), acceso_=True)
    return carta, m, g, tag


# --- la classe base con i tempi delle parole ---------------------------------------------------------------------

def _sillabe(w: str) -> int:
    return max(1, len(re.findall(r"[aeiouàèéìíòóù]+", w.lower())))


def _pausa(w: str) -> float:
    return 2.0 if w.endswith((".", "?", "!", ":", "…")) else 1.5 if w.endswith(",") else 0.0


class Scena(ScenaReel):
    """ScenaReel con i tempi delle singole parole (stimati a sillabe dentro la frase), la scrittura a cartellini con
    il cursore che segue e il controllo dei testi tagliati a zoom pieno."""

    def parlato(self, i: int) -> float:
        coda = 0.5 if i == len(self.inizi_frasi) - 1 else PAUSA_FRASI_S
        return max(0.3, self.durata_beat(i) - coda)

    def tempi(self, i: int) -> list[float]:
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
        n = len(self.inizi_frasi)
        return self.inizi_frasi[i + 1] - self.ANTICIPO_S if i + 1 < n else self.durata_s - 0.1

    def scrivi(self, coppie: list, cursore_: Rectangle | None = None, limite: float | None = None) -> None:
        """I cartellini entrano uno alla volta, ognuno all'istante della sua parola, in una sola play; il cursore salta
        dopo l'ultimo entrato."""
        inizio = max(self.t, coppie[0][1] - 0.08)
        fine = coppie[-1][1] + 0.3
        if limite is not None:
            fine = min(fine, limite)
        run = self.arrotonda(max(fine - inizio, 0.3))
        self.attendi_fino(inizio)
        anims, soglie = [], []
        for tok, t in coppie:
            a = min(max(t - 0.08 - inizio, 0.0) / run, 0.9)
            anims.append(FadeIn(tok, shift=UP * 0.12, rate_func=fra(a, min(1.0, a + 0.22 / run))))
            soglie.append(a + 0.11 / run)
        if cursore_ is not None:
            fermo(cursore_)
            posti = [dopo_di(cursore_.copy(), tok).get_center() for tok, _ in coppie]
            da = cursore_.get_center().copy()

            def segui(m, a):
                k = max((j for j, s in enumerate(soglie) if a >= s), default=-1)
                m.move_to(posti[k] if k >= 0 else da)

            anims.append(UpdateFromAlphaFunc(cursore_, segui, rate_func=linear))
        self.play(*anims, run_time=run)

    def scrivi_parole(self, blocco, tempi_: list[float], cursore_: Rectangle | None = None,
                      limite: float | None = None) -> None:
        """Le parole di un blocco compaiono una alla volta agli istanti dati (il blocco è già in scena con i glifi
        trasparenti); il cursore segue."""
        ws = []
        for r in blocco.righe:
            i = 0
            for w in r.piano.split():
                ws.append((VGroup(*r.glifi.submobjects[i:i + len(w)]), r))
                i += len(w)
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

    def controlla_zoom(self, momento: str) -> None:
        """A zoom pieno: ogni testo è intero o del tutto fuori campo, e quello in campo sta nell'area contenuto dello
        schermo (i controlli della libreria guardano solo la fine dei beat, quando lo zoom è già tornato)."""
        fr = self.camera.frame
        z = self.cfg.frame_width / fr.width
        c = fr.get_center()
        fx0, fx1 = c[0] - fr.width / 2, c[0] + fr.width / 2
        fy0, fy1 = c[1] - fr.height / 2, c[1] + fr.height / 2
        a = self.area.contenuto
        for m in extract_mobject_family_members(self.mobjects):
            if not isinstance(m, Riga) or not m.glifi.has_points():
                continue
            if max(g.get_fill_opacity() for g in m.glifi.family_members_with_points()) < 0.05:
                continue
            x0, y0 = m.glifi.get_left()[0], m.glifi.get_bottom()[1]
            x1, y1 = m.glifi.get_right()[0], m.glifi.get_top()[1]
            dentro_ = fx0 <= x0 and x1 <= fx1 and fy0 <= y0 and y1 <= fy1
            fuori_ = x1 < fx0 or x0 > fx1 or y1 < fy0 or y0 > fy1
            if not dentro_ and not fuori_:
                self.controlli.append(Violazione("zoom-taglio", momento, f"«{m.piano}» tagliato a zoom pieno"))
            elif dentro_:
                sx0, sx1 = (x0 - c[0]) * z, (x1 - c[0]) * z
                sy0, sy1 = (y0 - c[1]) * z, (y1 - c[1]) * z
                if sx0 < a.x0 - 1e-3 or sx1 > a.x1 + 1e-3 or sy0 < a.y0 - 1e-3 or sy1 > a.y1 + 1e-3:
                    self.controlli.append(Violazione("zoom-fuori", momento,
                                                     f"«{m.piano}» fuori dall'area contenuto a zoom pieno"))


# --- scene -------------------------------------------------------------------------------------------------------

class Scena01(Scena):
    """Hook. Fotogramma 0: titolo, carta «richiesta» con l'annuncio (inventato), testa della mail. Il titolo si riduce
    e la carta si accende sulla domanda; VIAGGIO: la carta si compatta, la mail sale e il suo corpo scorre veloce fino
    all'ultima riga; la riga si scrive a cartellini con la voce fino a «per un ▌» (la prova)."""

    def costruisci(self):
        tit_f, pil, m = disposizione_01(self.scena["titolo"])
        tit = Titolo(self.scena["titolo"])
        a_ul(tit, X0, ALTO)
        tit.target = tit_f
        dy0 = fondo(tit) - fondo(tit_f)                                  # quanto sale tutto al primo movimento
        carta = Carta("intera", y=fondo(tit) + 36)
        m0 = mail_a1(fondo(carta.box) + 36, n_barre=5, parole=10)       # la stessa mail, più in basso
        testa = [m0.box, m0.titolo, m0.p["oggetto"], m0.p["saluto"]]
        self.add(tit, *carta.pezzi(), *testa)                            # fotogramma 0 pieno: la copertina di chi scorre
        self.play(MoveToTarget(tit, rate_func=ease_out_cubic),
                  *[p.animate(rate_func=ease_out_cubic).shift(UP * px(dy0)) for p in carta.pezzi() + testa],
                  run_time=0.5)

        t0 = self.tempi(0)       # «Ti fai scrivere la candidatura dall'IA? Finisci tu la frase.»
        self.attendi_fino(t0[4] - 0.2)                                   # «candidatura»: la carta si accende
        self.play(carta.box.animate(rate_func=ease_out_expo).set_stroke(P.accento, width=tratto(6)), run_time=0.35)

        # VIAGGIO su «Finisci tu la frase»: la carta si compatta in pillola, la mail sale al suo posto, il corpo scorre
        self.attendi_fino(min(t0[6] - 0.15, self.limite(0) - 1.3))
        fin = m.p["finestra"]
        fin_top = fin.get_top()[1] - m.box.get_top()[1]
        fin_bot = fin.get_bottom()[1] - m.box.get_top()[1]
        passo = px(44)                                                   # riga di 18 px + 26 di spazio
        righe = barre([480 + 340 * pseudo(40 + k) for k in range(16)], gap=26)
        base = [fin_top - px(9) - (k - 11) * passo for k in range(16)]   # a fine corsa le righe 11-15 nella finestra
        for b in righe:
            b.set_x(fin.get_left()[0] + b.width / 2)

        def scorri(g, a):
            top = m0.box.get_top()[1]
            su = 11 * passo * (1 - a)                                    # a=0: nella finestra le righe 0-4
            lo, hi = top + fin_bot, top + fin_top
            for b, y in zip(g, base):
                yy = top + y - su
                b.set_y(yy)
                dist = min(hi - (yy + b.height / 2), (yy - b.height / 2) - lo)
                b.set_fill(opacity=0.35 * max(0.0, min(1.0, 1 + dist / px(20))))
            return g

        scorri(righe, 0.0)
        self.add(righe)
        c = cursore()
        c.move_to([m.p["fila"][0].get_left()[0] + c.width / 2, m.p["fila"][0].get_center()[1], 0])
        c.set_fill(opacity=0)
        dy = y_px(m0.box.get_top()[1]) - y_px(m.box.get_top()[1])
        mob_su = [m0.titolo, m0.p["oggetto"], m0.p["saluto"]]
        self.play(Transform(carta.box, pil.box, rate_func=fra(0, 0.55, ease_out_cubic)),
                  carta.titolo.animate(rate_func=fra(0, 0.55, ease_out_cubic)).move_to(pil.titolo),
                  Transform(carta.et_ann, pil.et_ann, rate_func=fra(0, 0.55, ease_out_cubic)),
                  *fuori(carta.riga, carta.annuncio, carta.box_ann, rate_func=fra(0, 0.3)),
                  Transform(m0.box, m.box, rate_func=fra(0.05, 0.7, ease_out_cubic)),
                  *[p.animate(rate_func=fra(0.05, 0.7, ease_out_cubic)).shift(UP * px(dy)) for p in mob_su],
                  UpdateFromAlphaFunc(righe, lambda g, a: scorri(g, ease_out_cubic(a))),
                  c.animate(rate_func=fra(0.8, 1.0)).set_fill(opacity=1),
                  run_time=self.arrotonda(min(1.2, self.limite(0) - self.t - 0.1)))
        c.move_to([m.p["fila"][0].get_left()[0] + c.width / 2, m.p["fila"][0].get_center()[1], 0])
        lampeggia(c)

        self.beat(1)             # «Allego il mio curriculum e resto a disposizione per un…»
        t1 = self.tempi(1)
        self.scrivi(list(zip(m.p["fila"], t1)), c, limite=self.limite(1))
        lampeggia(c)             # «per un ▌»: il vuoto della prova fino alla fine della scena


class Scena02(Scena):
    """PUNCH «COLLOQUIO»; al ritorno la parola è nella mail. La mail si riduce a sagoma a sinistra e a destra entrano i
    quattro frammenti, «10 su 10»; due copie grigie le scivolano accanto; la mail torna intera e sull'angolo in alto a
    destra entra «parla di te?»."""

    def costruisci(self):
        pil, _, m = stato_02()
        c_parola = acceso(m.p["fila"][-1])
        self.add(*pil.pezzi(), *m.pezzi())
        self.punch(grande(self.scena))           # il ritorno è un taglio: «colloquio.» dove c'era il cursore

        t0 = self.tempi(0)                       # «Colloquio, vero? Hai fatto un po' quello che fa lei.»
        self.attendi_fino(min(t0[6] - 0.1, self.limite(0) - 0.6))
        self.play(c_parola.animate(rate_func=there_and_back).scale(1.18), run_time=0.45)

        # beat 1 («Io gliel'ho chiesta dieci volte, e c'era in tutte e dieci.»): la mail diventa una sagoma a sinistra,
        # «colloquio.» resta leggibile; a destra i frammenti, uno alla volta
        self.beat(1)
        t1, lim = self.tempi(1), self.limite(1)
        fr = [testo(s.replace("colloquio", "==colloquio==", 1), "piede", colore=P.attenuato, larghezza_px=540)
              for s in FRAMMENTI_A]
        dieci = Etichetta(self.scena["testo"][0])
        colonna = VGroup(*fr, dieci)
        VGroup(*fr).arrange(DOWN, buff=px(24), aligned_edge=LEFT)
        dieci.next_to(VGroup(*fr), DOWN, buff=px(30), aligned_edge=LEFT)
        a_ul(colonna, 420, 400 + (796 - h(colonna)) / 2)
        mini = miniatura(X0, 0, token="colloquio.")
        dy = (y_px(colonna.get_center()[1]) - h(mini.box) / 2)
        mini = miniatura(X0, dy, token="colloquio.")
        tok = mini.p["token"][0]
        altri = [p for p in [m.p["oggetto"], m.p["saluto"], m.p["finestra"], *m.p["fila"][:-1]]]
        self.play(Transform(m.box, mini.box, rate_func=fra(0, 0.6, ease_out_cubic)),
                  m.titolo.animate(rate_func=fra(0, 0.6, ease_out_cubic)).move_to(mini.titolo),
                  *fuori(*altri, rate_func=fra(0, 0.35)),
                  FadeIn(mini.p["barre"], rate_func=fra(0.35, 0.8)),
                  c_parola.animate(rate_func=fra(0, 0.6, ease_out_cubic)).move_to(tok),
                  run_time=0.75)
        self.play(*[FadeIn(f, shift=LEFT * 0.6, rate_func=fra(0.2 * k, 0.2 * k + 0.4, ease_out_cubic))
                    for k, f in enumerate(fr)], run_time=self.arrotonda(max(0.9, min(1.5, t1[7] - 0.3 - self.t))))
        self.attendi_fino(min(t1[8] - 0.15, lim - 0.6))                  # «tutte e dieci»
        parole = [f.parola("colloquio") for f in fr]
        self.play(dieci.entra(rate_func=ease_out_back),
                  *[p.animate(rate_func=there_and_back).scale(1.25) for p in parole], run_time=0.45)

        # beat 2 («E la tua mail finisce accanto a quelle degli altri.»): i frammenti escono; la mail al centro, due
        # copie grigie (senza testo) le scivolano accanto
        self.beat(2)
        t2 = self.tempi(2)
        dx = (540 - 160) - X0
        self.play(*fuori(*fr, dieci, shift=UP * 0.5, rate_func=fra(0, 0.45, rush_into)),
                  *[p.animate(rate_func=fra(0.35, 1.0, ease_out_cubic)).shift(RIGHT * px(dx))
                    for p in [m.box, m.titolo, mini.p["barre"], c_parola]], run_time=0.7)
        copie = []
        for k, (verso, ang) in enumerate([(-1, 0.08), (1, -0.08)]):
            s_ = miniatura(X0 + dx, dy, seme=10 + 7 * k, titolo=False, n=8)
            s_.box.set_z_index(-3)
            s_.p["barre"].set_z_index(-2)
            g_ = VGroup(s_.box, s_.p["barre"])
            g_.generate_target()
            g_.target.shift(RIGHT * px(verso * 330) + DOWN * px(26)).rotate(ang)
            g_.angolo = ang
            copie.append(g_)
        self.add(*copie)
        self.attendi_fino(min(t2[5] - 0.25, self.limite(2) - 0.9))       # «accanto»
        self.play(*[MoveToTarget(g, rate_func=ease_out_back) for g in copie], run_time=0.7)

        # beat 3 («E una mail che parla di te? Si può, ma non basta chiederlo.»): le copie rientrano, la mail torna
        # intera; «parla di te?» con il «?» in accento, poi attenuato
        self.beat(3)
        t3 = self.tempi(3)
        _, loop_f, m2 = stato_02()
        loop_a = loop_in_alto(acceso_domanda=True)
        tok2 = m2.p["fila"][-1]
        acceso(tok2)
        self.play(*[g.animate(rate_func=fra(0, 0.5, rush_into)).move_to(m.box).rotate(-g.angolo).set_opacity(0)
                    for g in copie],
                  Transform(m.box, m2.box, rate_func=fra(0.2, 0.8, ease_out_cubic)),
                  m.titolo.animate(rate_func=fra(0.2, 0.8, ease_out_cubic)).move_to(m2.titolo),
                  FadeOut(mini.p["barre"], rate_func=fra(0, 0.3)),
                  c_parola.animate(rate_func=fra(0.2, 0.8, ease_out_cubic)).move_to(tok2),
                  *dentro(m2.p["oggetto"], m2.p["saluto"], m2.p["finestra"], *m2.p["fila"][:-1],
                          rate_func=fra(0.55, 1.0)),
                  run_time=0.9)
        self.remove(*copie)
        self.attendi_fino(min(t3[4] - 0.15, self.limite(3) - 1.3))       # «parla di te?»
        self.play(FadeIn(loop_a, scale=0.6, rate_func=ease_out_back), run_time=0.4)
        self.attendi_fino(min(t3[10] - 0.1, self.limite(3) - 0.5))       # «non basta chiederlo»
        self.play(loop_a.testo.parola("?").animate.set_color(P.attenuato), run_time=0.35)


class Scena03(Scena):
    """METAMORFOSI e ZOOM: la frase si riduce a gettoni vuoti, restano «per un ▌»; sotto la colonna delle candidate;
    la camera entra 1,8×, «colloquio» si accende e vola nel posto del cursore, la camera torna. Poi la mail scorre al
    corpo, «fluente», e i tre segnaposto si accendono uno per negazione; «non gliel'hai detto»."""

    def costruisci(self):
        pil, loop, m = stato_02()                # ultimo fotogramma della 2
        acceso(m.p["fila"][-1])
        self.add(*pil.pezzi(), loop, *m.pezzi())

        # beat 0 («Guarda, lei scrive una parola alla volta, e ne prende una delle più probabili.»)
        t0 = self.tempi(0)
        fila_ = m.p["fila"]
        campo_alto, campo_sx = 492, 388                                  # angolo del campo a zoom pieno (px)
        y_fila = campo_alto + 240 / ZOOM
        passati = fila_[:8]
        per, un, coll = fila_[8], fila_[9], fila_[10]
        gett = []
        xg = X0 + 40
        for t in passati:
            g = gettone(t, 30)
            a_ul(g, xg, y_fila + 20)
            gett.append(g)
            xg += 30 + 10
        per_t = per.copy()
        a_ul(per_t, xg + 8, y_fila)
        un_t = un.copy()
        a_ul(un_t, sinistra(per_t) + per_t.width * K + GAP, y_fila)
        c = dopo_di(cursore(), un_t)
        cl = Classifica(CANDIDATE_3, larghezza_px=LARG_COL)
        a_ul(cl, sinistra(per_t), fondo(un_t) + 34)
        box = a_ul(riquadro(LARG, fondo(cl) + 36 - Y_MAIL, P.terziario), X0, Y_MAIL)
        testa = barre([560, 420])
        a_ul(testa, X0 + 36, alto(m.titolo) + h(m.titolo) + 22)
        self.play(FadeOut(coll, shift=UP * 0.5, rate_func=rush_into),
                  *[FadeTransform(p, testa[k], rate_func=fra(0.1, 0.7))
                    for k, p in enumerate([m.p["oggetto"], m.p["saluto"]])],
                  FadeOut(m.p["finestra"], rate_func=fra(0, 0.4)),
                  *[Transform(t.box, g, rate_func=fra(0.1 + 0.04 * k, 0.6 + 0.04 * k, ease_out_cubic))
                    for k, (t, g) in enumerate(zip(passati, gett))],
                  *[FadeOut(t.testo, rate_func=fra(0, 0.3)) for t in passati],
                  per.animate(rate_func=fra(0.2, 0.8, ease_out_cubic)).move_to(per_t),
                  un.animate(rate_func=fra(0.25, 0.85, ease_out_cubic)).move_to(un_t),
                  Transform(m.box, box, rate_func=fra(0.1, 0.8, ease_out_cubic)),
                  FadeIn(c, rate_func=fra(0.85, 1.0)), run_time=0.9)
        self.remove(*[t.testo for t in passati])
        lampeggia(c)
        self.attendi_fino(min(t0[3] - 0.1, self.t + 0.3))                # «una parola alla volta»
        self.play(cl.entra(lag=0.3), run_time=0.8)
        # ZOOM 1,8× sulla riga «per un ▌» e sulla colonna: il bordo alto del campo cade sotto il titolo della mail
        larghezza = CFG.frame_width / ZOOM
        centro = punto(campo_sx + CFG.larghezza / (2 * ZOOM), campo_alto + CFG.altezza / (2 * ZOOM))
        self.attendi_fino(min(t0[7] - 0.2, self.limite(0) - 2.6))        # «e ne prende»
        self.play(self.camera.frame.animate(rate_func=ease_out_expo).set(width=larghezza).move_to(centro),
                  run_time=0.6)
        self.controlla_zoom("zoom scena 3")
        self.attendi_fino(min(t0[12] - 0.15, self.limite(0) - 1.75))     # «più probabili»
        self.play(cl.scegli(0), run_time=0.3)
        vola = cl.token(0, colore=P.accento)
        dest = dopo_di(vola.copy(), un_t, buff_px=GAP)
        fermo(c)
        self.play(vola.animate(path_arc=-0.8, rate_func=ease_out_back).move_to(dest),
                  FadeOut(c, rate_func=fra(0.5, 1)), run_time=0.55)
        self.play(self.torna(), run_time=self.arrotonda(max(0.3, min(0.6, self.limite(0) - self.t))))

        # beat 1 («Per questo la mail viene fluente, ma se non gliel'hai detto, non sa da quanti anni lavori,»): via la
        # colonna e la riga; la mail scorre al corpo; «fluente»; «[numero]» si accende
        self.beat(1)
        t1 = self.tempi(1)
        _, _, mc, segn, riq, fl, nd = stato_03()
        corpo = [mc.p[k] for k in ("b1", "numero", "b2", "attira", "chiusa")]
        self.play(*fuori(cl, vola, per, un, *[t.box for t in passati], shift=UP * 0.6, rate_func=fra(0, 0.45, rush_into)),
                  *fuori(*testa, rate_func=fra(0, 0.4)),
                  Transform(m.box, mc.box, rate_func=fra(0.1, 0.8, ease_out_cubic)),
                  *[FadeIn(p, shift=UP * 0.8, rate_func=fra(0.3 + 0.08 * k, 0.8 + 0.04 * k, ease_out_cubic))
                    for k, p in enumerate(corpo)], run_time=0.8)
        self.attendi_fino(min(t1[5] - 0.15, self.limite(1) - 2.2))       # «fluente»
        self.play(fl.entra(rate_func=ease_out_back), run_time=0.4)
        self.attendi_fino(min(t1[13] - 0.15, self.limite(1) - 0.7))      # «da quanti anni»
        self.play(segn[0].animate.set_color(P.accento), Create(riq[0]), run_time=0.45)

        # beat 2 («non sa dove, e non sa perché vuoi proprio loro.»): «non gliel'hai detto» (resta fino alla fine);
        # «[azienda/e]» su «dove», la riga di cosa vi attira su «perché»
        self.beat(2)
        t2 = self.tempi(2)
        self.play(nd.entra(rate_func=ease_out_back), run_time=0.35)
        self.attendi_fino(min(t2[2] - 0.15, self.limite(2) - 1.4))       # «dove»
        self.play(segn[1].animate.set_color(P.accento), Create(riq[1]), run_time=0.4)
        self.attendi_fino(min(t2[6] - 0.15, self.limite(2) - 0.6))       # «perché»
        self.play(segn[2].animate.set_color(P.accento), Create(riq[2]), run_time=0.4)


class Scena04(Scena):
    """La mail si riduce a pillola in alto e la carta scende al centro; entra «Sii originale.»; la carta torna su e la
    mail si riempie di righe grigie; PUNCH «DIVANO»: al ritorno la mail è B2, con due frammenti e «5 su 10»; il terzo
    frammento si allinea sotto l'attacco, «stessa frase»; poi il corpo di B2, i segnaposto e «non gliel'hai detto»."""

    def costruisci(self):
        pil, loop, m, segn, riq, fl, nd = stato_03()                  # ultimo fotogramma della 3
        for s in segn:
            s.set_color(P.accento)
        vecchi = [m.titolo, *[m.p[k] for k in ("b1", "numero", "b2", "attira", "chiusa")], *riq]
        self.add(*pil.pezzi(), loop, m.box, *vecchi, fl, nd)

        # beat 0 («Non sbagli a fartela scrivere, ci mancherebbe.»): le etichette escono; la mail (il testo di A1 esce
        # tutto) si riduce a pillola in alto; la carta scende al centro, intera, e si accende appena
        t0 = self.tempi(0)
        pm = pillola_mail()
        carta = carta_04()
        # Mail e richiesta si scambiano di posto nella stessa colonna: se viaggiassero tutte e due, «mail» e
        # «richiesta» si attraverserebbero. Ordine: escono i testi di A1; la mail si chiude su se stessa e si spegne;
        # la carta scende nel posto libero; la pillola «mail» spunta in alto quando la carta se n'è andata.
        pil_giu = a_ul(spento(pm.box), X0, Y_MAIL)
        self.play(*fuori(fl, nd, shift=DOWN * 0.4, rate_func=fra(0, 0.22, rush_into)),
                  *fuori(*vecchi[1:], rate_func=fra(0, 0.2)),
                  a_tappe(m.box, [m.box.copy(), pil_giu, spento(pm.box, 0.6), pm.box.copy().scale(1.08), pm.box.copy()],
                          [0.2, 0.42, 0.62, 0.8, 0.9], [ease_out_cubic, linear, ease_out_cubic, smooth]),
                  FadeOut(m.titolo, rate_func=fra(0.2, 0.36)),
                  Transform(pil.box, carta.box, rate_func=fra(0.42, 0.85, ease_out_cubic)),
                  pil.titolo.animate(rate_func=fra(0.42, 0.85, ease_out_cubic)).move_to(carta.titolo),
                  Transform(pil.et_ann, carta.et_ann, rate_func=fra(0.42, 0.85, ease_out_cubic)),
                  FadeIn(pm.titolo, scale=0.6, rate_func=fra(0.64, 0.86, ease_out_cubic)),
                  *dentro(carta.riga, carta.box_ann, carta.annuncio, rate_func=fra(0.75, 1.0)),
                  run_time=1.2)
        m.titolo = pm.titolo
        self.attendi_fino(min(t0[5] - 0.15, self.limite(0) - 0.6))       # «ci mancherebbe»
        self.play(pil.box.animate(rate_func=there_and_back).set_stroke(P.accento, width=tratto(6)), run_time=0.5)

        # beat 1 («Sbagli se pensi che basti «sii originale».»): la riga entra in accento (la carta è la richiesta B)
        self.beat(1)
        t1 = self.tempi(1)
        cb = carta_04(extra=True)
        self.attendi_fino(min(t1[5] - 0.2, self.limite(1) - 0.7))        # «sii originale»
        self.play(Transform(pil.box, cb.box, rate_func=ease_out_cubic),
                  FadeIn(cb.extra, shift=UP * 0.2, rate_func=fra(0.3, 1.0, ease_out_back)), run_time=0.5)

        # beat 2 («Io l'ho fatto, e una mail su due comincia con un divano,»): la carta torna pillola; la mail scende e
        # si riempie di righe grigie (scrive); PUNCH su «divano»: al ritorno c'è B2, con i frammenti e «5 su 10»
        self.beat(2)
        t2 = self.tempi(2)
        p2 = Carta("pillola")
        mb = mail_b2(Y_MAIL)
        vuote = [barre([700, 460]), barre([780, 820, 300])]
        a_ul(vuote[0], X0 + 36, alto(mb.p["oggetto"]))
        a_ul(vuote[1], X0 + 36, alto(mb.p["attacco"]) - 10)
        # lo scambio al contrario, con lo stesso ordine: escono i testi della carta e la pillola «mail» si spegne in
        # alto; la carta torna pillola nel posto libero; la mail si riapre sotto, dove la carta non c'è più
        self.play(*fuori(carta.riga, carta.box_ann, carta.annuncio, cb.extra, rate_func=fra(0, 0.24)),
                  FadeOut(m.titolo, rate_func=fra(0, 0.2)),
                  a_tappe(m.box, [m.box.copy(), spento(m.box, 0.6), a_ul(spento(pm.box), X0, Y_MAIL), mb.box.copy()],
                          [0.0, 0.24, 0.58, 1.0], [ease_out_cubic, linear, ease_out_cubic]),
                  Transform(pil.box, p2.box, rate_func=fra(0.24, 0.66, ease_out_cubic)),
                  pil.titolo.animate(rate_func=fra(0.24, 0.66, ease_out_cubic)).move_to(p2.titolo),
                  Transform(pil.et_ann, p2.et_ann, rate_func=fra(0.24, 0.66, ease_out_cubic)),
                  FadeIn(mb.titolo, rate_func=fra(0.7, 1.0)),
                  run_time=1.0)
        righe_v = [b for g in vuote for b in g]
        self.play(*[GrowFromEdge(b, LEFT, rate_func=fra(k / len(righe_v) * 0.8, k / len(righe_v) * 0.8 + 0.25))
                    for k, b in enumerate(righe_v)],
                  run_time=self.arrotonda(max(0.5, min(1.4, t2[11] - 0.35 - self.t))))
        fr = [testo(s.replace("divano", "==divano==", 1), "piede", colore=P.attenuato) for s in FRAMMENTI_B]
        b3 = testo(FRAMMENTO_B3.replace("divano", "==divano==", 1), "token", colore=P.attenuato, larghezza_px=828)
        a_ul(b3, X0 + 36, fondo(mb.box) + 24)
        VGroup(*fr).arrange(DOWN, buff=px(16), aligned_edge=LEFT)
        a_ul(VGroup(*fr), X0 + 36, fondo(b3) + 70)
        cinque = a_ul(Etichetta(self.scena["testo"][0], pieno=False), X0, fondo(VGroup(*fr)) + 30)
        self.attendi_fino(t2[11] - 0.12)                                 # «divano»
        self.remove(*righe_v)
        self.add(*mb.testi()[1:], *fr, cinque)
        self.punch(grande(self.scena))

        # beat 3 («e due con la stessa frase.»): il terzo frammento scivola sotto l'attacco; un riquadro le prende insieme
        self.beat(3)
        ev = Evidenzia(VGroup(mb.p["attacco"], b3), buff=px(14))
        stessa = Etichetta(self.scena["testo"][1])
        stessa.move_to([ev.get_right()[0] - stessa.width / 2 - px(20), ev.get_bottom()[1], 0]).set_z_index(3)
        self.play(FadeIn(b3, shift=LEFT * 1.2, rate_func=ease_out_expo), run_time=0.45)
        self.play(Create(ev, rate_func=ease_out_cubic), FadeIn(stessa, scale=0.6, rate_func=fra(0.4, 1, ease_out_back)),
                  run_time=0.5)
        t_ev = self.t

        # beat 4 («Cambia il vestito, ma del tuo lavoro non le hai ancora detto niente.»): via i frammenti; la mail B2
        # scorre al corpo; «[numero]» e «[azienda]» accesi, «non gliel'hai detto»; in fondo la chiusa accesa
        self.beat(4)
        t4 = self.tempi(4)
        _, _, mf, segn4, riq4, nd4, chiedo = stato_04()
        self.attendi_fino(t_ev + 1.0)                                    # il riquadro «stessa frase» resta ≥ 1 s
        corpo = [mf.p[k] for k in ("b1", "negli", "b2", "chiedo")]
        # prima escono frammenti, riquadro e oggetto; poi il riquadro della mail cresce e saluto e attacco salgono;
        # il corpo entra per ultimo, già dentro il riquadro
        self.play(*fuori(*fr, cinque, b3, ev, stessa, rate_func=fra(0, 0.28, rush_into)),
                  FadeOut(mb.p["oggetto"], rate_func=fra(0, 0.28)),
                  Transform(m.box, mf.box, rate_func=fra(0.28, 0.7, ease_out_cubic)),
                  mb.p["saluto"].animate(rate_func=fra(0.28, 0.7, ease_out_cubic)).move_to(mf.p["saluto"]),
                  mb.p["attacco"].animate(rate_func=fra(0.28, 0.7, ease_out_cubic)).move_to(mf.p["attacco"]),
                  *[FadeIn(p, shift=UP * 0.15, rate_func=fra(0.62 + 0.04 * k, 0.9 + 0.03 * k, ease_out_cubic))
                    for k, p in enumerate(corpo)], run_time=0.9)
        self.attendi_fino(min(t4[5] - 0.15, self.limite(4) - 1.6))       # «del tuo lavoro»
        self.play(*[s.animate.set_color(P.accento) for s in segn4], *[Create(r) for r in riq4],
                  nd4.entra(rate_func=ease_out_back), run_time=0.5)
        self.attendi_fino(min(t4[12] - 0.15, self.limite(4) - 0.5))      # «niente»
        self.play(chiedo.animate.set_color(P.accento), run_time=0.35)


class Scena05(Scena):
    """RIVELAZIONE A TRATTO: la carta torna intera con «Sii originale.»; la riga parte con una carica e al suo posto
    si disegna la riga vuota col cursore, «un fatto vero»; il fatto si scrive con la voce (richiesta C), la nota
    «esempio: candidato inventato»; la carta si compatta in alto e sotto la mail C4 si scrive fino a «da 300 a ▌»."""

    def costruisci(self):
        pil, loop, m, segn, riq, nd, chiedo = stato_04()              # ultimo fotogramma della 4
        for s in segn:
            s.set_color(P.accento)
        chiedo.set_color(P.accento)
        vecchi = m.pezzi()
        self.add(*pil.pezzi(), loop, *vecchi, *riq, nd)

        # beat 0 («Togli «sii originale» e dille un fatto vero che sai solo tu.»)
        t0 = self.tempi(0)
        cb = carta_04(extra=True)
        # prima esce la mail di B2 (tutta), poi la carta scende e cresce nel posto libero, poi entrano i suoi testi
        self.play(*fuori(*vecchi, *riq, nd, rate_func=fra(0, 0.3, rush_into)),
                  Transform(pil.box, cb.box, rate_func=fra(0.3, 0.8, ease_out_cubic)),
                  pil.titolo.animate(rate_func=fra(0.3, 0.8, ease_out_cubic)).move_to(cb.titolo),
                  Transform(pil.et_ann, cb.et_ann, rate_func=fra(0.3, 0.8, ease_out_cubic)),
                  *dentro(cb.riga, cb.box_ann, cb.annuncio, rate_func=fra(0.7, 1.0)),
                  FadeIn(cb.extra, rate_func=fra(0.7, 1.0)), run_time=0.75)
        riga_vuota = DashedLine(punto(X0 + 36, fondo(cb.extra) + 6), punto(X1 - 36, fondo(cb.extra) + 6),
                                dash_length=px(18), stroke_color=P.accento, stroke_width=tratto(4))
        c = cursore().move_to([punto(X0 + 36, 0)[0] + px(4), cb.extra.get_center()[1], 0])
        self.attendi_fino(min(t0[1] - 0.1, self.limite(0) - 1.6))        # «sii originale»
        # la carica arretra di ~30 px: con `ease_in_back` su 9 unità arretrava di ~110 px, oltre il bordo della tela
        self.play(cb.extra.animate(rate_func=carica).shift(RIGHT * 9).set_opacity(0), run_time=0.55)
        self.remove(cb.extra)
        self.play(Create(riga_vuota, rate_func=ease_out_cubic), FadeIn(c, rate_func=fra(0.6, 1)), run_time=0.5)
        lampeggia(c)
        fatto_et = a_ul(Etichetta(self.scena["testo"][0]), X0, ALTO)
        self.attendi_fino(min(t0[5] - 0.15, self.limite(0) - 0.45))      # «un fatto vero»
        self.play(FadeIn(fatto_et, scale=0.6, rate_func=ease_out_back), run_time=0.35)

        # beat 1 («Tipo che hai portato una newsletter a duemilacento iscritti.»): la carta si allunga e la riga del
        # fatto si scrive in accento, parola per parola, agganciata alla voce (portato, newsletter, 2.100, iscritti)
        self.beat(1)
        t1 = self.tempi(1)
        cc = Carta("intera", y=Y_CARTA, extra=FATTO, colore_extra=P.accento)
        fatto = cc.extra
        fatto.glifi.set_fill(opacity=0)
        self.add(fatto)
        nota = testo(NOTA_FATTO, "piede", colore=P.attenuato)
        a_ul(nota, X0, fondo(cc.box) + 16)
        ancore = [(0, t1[0]), (5, t1[3]), (7, t1[5]), (16, t1[7]), (17, t1[8]), (20, t1[8] + 0.5)]
        istanti = []
        for k in range(21):
            for (a, ta), (b, tb) in zip(ancore, ancore[1:]):
                if a <= k <= b:
                    istanti.append(ta + (tb - ta) * (k - a) / (b - a))
                    break
        self.play(Transform(pil.box, cc.box, rate_func=ease_out_cubic), FadeOut(riga_vuota), run_time=0.3)
        self.scrivi_parole(fatto, istanti, c, limite=self.limite(1) - 0.45)
        fermo(c)
        self.play(FadeIn(nota, shift=UP * 0.15), FadeOut(c), run_time=self.arrotonda(min(0.35, self.limite(1) - self.t)))

        # beat 2 («Ora scrive: in un anno ho portato gli iscritti da trecento a…»): la carta si compatta in alto col
        # fatto (e la nota); il loop scende sull'angolo della mail nuova (C4), che si scrive con la voce fino a «a ▌»
        self.beat(2)
        t2 = self.tempi(2)
        cf, mc, loop_m = stato_05()
        fila_ = mc.p["fila"]
        c2 = cursore().move_to([fila_[0].get_left()[0] + px(4), fila_[0].get_center()[1], 0])
        testa = [mc.box, mc.titolo, mc.p["oggetto"], mc.p["saluto"], mc.p["finestra"]]
        # Ordine del passaggio: escono i testi che non restano (riga, annuncio, nota, etichette, il loop in alto); poi
        # carta, titolo e fatto salgono insieme (il fatto resta su tre righe: nessuna riga ne attraversa un'altra);
        # arrivato in alto il fatto rifà gli a capo (`reimpagina`); nota ed etichetta dell'annuncio rientrano al loro
        # posto nuovo; la mail entra da sotto con il loop già appeso all'angolo, quando la carta ha liberato il posto.
        # Nota e loop non viaggiano più: i loro percorsi passavano sopra il fatto.
        run = self.arrotonda(min(0.95, max(0.8, t2[2] - 0.08 - self.t)))
        self.play(*fuori(cb.riga, cb.box_ann, cb.annuncio, fatto_et, nota, loop, pil.et_ann, rate_func=fra(0, 0.2)),
                  Transform(pil.box, cf.box, rate_func=fra(0.2, 0.6, ease_out_cubic)),
                  pil.titolo.animate(rate_func=fra(0.2, 0.6, ease_out_cubic)).move_to(cf.titolo),
                  *reimpagina(fatto, cf.extra, 0.2, 0.6, 0.9, corpo_rigido=True),
                  *dentro(cf.et_ann, cf.nota, rate_func=fra(0.62, 0.9)),
                  *dentro(*testa, loop_m, shift=UP * 0.5, rate_func=fra(0.5, 0.95, ease_out_cubic)),   # 0,8: sotto il cerchio
                  FadeIn(c2, rate_func=fra(0.92, 1)), run_time=run)
        lampeggia(c2)
        self.scrivi(list(zip(fila_, t2[2:12])), c2, limite=self.limite(2))
        lampeggia(c2)                            # «da 300 a ▌»: la seconda prova, lo stesso gesto della scena 1


class Scena06(Scena):
    """CONTRASTO DI SCALA: il resto si spegne e «2.100» esce enorme dal cursore, poi ci rientra. La mail si riduce a
    «da 300 a 2.100.», sotto torna la colonna; una freccia dalla riga del numero nella carta alla colonna, «dopo il tuo
    numero». Poi la mail torna intera, il loop si accende senza «?» e sulla riga del numero la graffa «l'hai messo tu»."""

    def costruisci(self):
        carta, m, loop = stato_05()                                   # ultimo fotogramma della 5
        fila_ = m.p["fila"]
        c = dopo_di(cursore(), fila_[-1])
        self.add(*carta.pezzi(), *m.pezzi(), loop, c)
        lampeggia(c)

        # beat 0 («Duemilacento, vero?»): il velo spegne la scena, il numero cresce dal cursore al centro e ci rientra
        pieno = mail_c4(Y_MAIL_C, parole=11, acceso_=True)
        numero = pieno.p["fila"][-1]
        p = Punch(grande(self.scena), self.area.contenuto)
        p.set_z_index(6)
        grande_ = p.copy()
        p.scale(numero.testo.height / p.height).move_to(numero.testo)
        velo = Rectangle(width=CFG.frame_width, height=CFG.frame_height, stroke_width=0, fill_color=P.sfondo,
                         fill_opacity=0.93).set_z_index(5)
        fermo(c)
        self.play(FadeIn(velo, rate_func=fra(0, 0.5)), FadeOut(c, rate_func=fra(0, 0.3)),
                  Transform(p, grande_, rate_func=ease_out_back), run_time=0.45)
        fine0 = self.limite(0)
        self.attendi_fino(fine0 - 0.5)
        numero.set_z_index(6)
        self.play(FadeOut(velo, rate_func=fra(0.2, 1)), FadeTransform(p, numero, rate_func=ease_out_cubic),
                  run_time=self.arrotonda(max(0.3, fine0 - self.t - 0.02)))
        numero.set_z_index(0)

        # beat 1 («È ancora una parola probabile, ma probabile dopo il tuo numero.»): la mail si riduce alla coda
        # «da 300 a 2.100.»; sotto la colonna (2.100 in testa); su «dopo il tuo numero» la freccia dalla carta
        self.beat(1)
        t1 = self.tempi(1)
        coda = fila_[7:10] + [numero]
        xs = X0 + 40
        posti = []
        for t in coda:
            posti.append(a_ul(t.copy(), xs, 630 + 24))
            xs += t.width * K + GAP
        box_c = a_ul(riquadro(xs - GAP + 40 - X0, 80 + 48, P.terziario), X0, 630)
        cl = Classifica(CANDIDATE_6, larghezza_px=LARG_COL)
        a_ul(cl, X0 + 40, fondo(box_c) + 24)
        for k, b in enumerate(cl.barre):
            if k == 0:
                b.riempimento.set_fill(P.accento)
                b.etichetta.set_color(P.accento)
            else:
                b.fade(0.65)
        via = [m.titolo, m.p["oggetto"], m.p["saluto"], m.p["finestra"], *fila_[:7]]
        numero.generate_target()
        numero.target.move_to(posti[-1])
        numero.target.box.set_stroke(P.accento, width=tratto(5))
        self.play(*fuori(*via, loop, rate_func=fra(0, 0.35)),
                  Transform(m.box, box_c, rate_func=fra(0.1, 0.7, ease_out_cubic)),
                  *[t.animate(rate_func=fra(0.1, 0.7, ease_out_cubic)).move_to(d) for t, d in zip(coda[:-1], posti)],
                  MoveToTarget(numero, rate_func=fra(0.1, 0.7, ease_out_cubic)),
                  run_time=0.7)
        self.play(cl.entra(lag=0.3), run_time=0.8)
        r3 = riga_numero(carta)
        barra0 = cl.barre[0].riempimento
        x_v = 900
        y_r = r3.get_center()[1]
        y_b = barra0.get_center()[1]
        punti = [np.array([r3.get_right()[0] + px(16), y_r, 0]), np.array([punto(x_v, 0)[0], y_r, 0]),
                 np.array([punto(x_v, 0)[0], y_b, 0]),
                 np.array([cl.barre[0].pista.get_right()[0] + px(14), y_b, 0])]
        freccia = freccia_gomito(punti)
        dopo_et = Etichetta(self.scena["testo"][0])
        dopo_et.move_to([punto(X1, 0)[0] - dopo_et.width / 2, y_b - px(90), 0])
        num_carta = r3.parola("2.100")
        self.attendi_fino(min(t1[7] - 0.3, self.limite(1) - 0.95))       # «dopo il tuo numero»
        self.play(Create(freccia.linea, rate_func=fra(0, 0.8, ease_out_cubic)), FadeIn(freccia.punta, rate_func=fra(0.7, 0.85)),
                  num_carta.animate(rate_func=there_and_back).scale(1.3),
                  FadeIn(dopo_et, scale=0.6, rate_func=fra(0.5, 1, ease_out_back)), run_time=0.8)

        # beat 2 («Ecco una mail che parla di te, e il numero ce l'hai messo tu.»): via la colonna; la mail torna intera
        # (il numero di nuovo normale); il loop si accende senza «?»; la graffa sulla riga del numero
        self.beat(2)
        t2 = self.tempi(2)
        _, mf, g, tag = stato_06(self.scena["testo"][1])
        loop_q = loop_sulla_mail(mf.box)
        numero.generate_target()
        numero.target.move_to(mf.p["fila"][-1])
        numero.target.box.set_stroke(P.attenuato, width=tratto(3))
        numero.target.testo.set_color(P.testo)
        self.play(*fuori(cl, freccia, dopo_et, shift=DOWN * 0.3, rate_func=fra(0, 0.4, rush_into)),
                  Transform(m.box, mf.box, rate_func=fra(0.1, 0.75, ease_out_cubic)),
                  *[t.animate(rate_func=fra(0.1, 0.75, ease_out_cubic)).move_to(d)
                    for t, d in zip(coda[:-1], mf.p["fila"][7:])],
                  MoveToTarget(numero, rate_func=fra(0.1, 0.75, ease_out_cubic)),
                  *dentro(mf.titolo, mf.p["oggetto"], mf.p["saluto"], mf.p["finestra"], *mf.p["fila"][:7],
                          rate_func=fra(0.45, 1.0)),
                  FadeIn(loop_q, rate_func=fra(0.6, 1.0)), run_time=0.8)
        self.attendi_fino(min(t2[4] - 0.15, self.limite(2) - 1.3))       # «parla di te»
        self.play(FadeTransform(loop_q, tag, rate_func=ease_out_cubic), run_time=0.4)
        self.attendi_fino(min(t2[9] - 0.2, self.limite(2) - 0.6))        # «il numero ce l'hai messo tu»
        self.play(g.entra(), run_time=0.5)


class Scena07(Scena):
    """Chiusura, un passaggio per frase: le due mail una accanto all'altra (A1 con «colloquio» acceso, C4 con «2.100»
    acceso e «da [numero] anni» leggibile); MOLTIPLICAZIONE: un muro di sagome grigie dietro la prima; poi il muro e la
    prima escono, la mail nuova al centro, il messaggio sopra e la CTA sotto."""

    def costruisci(self):
        carta, m, g, tag = stato_06(TESTO_6[1])                # ultimo fotogramma della 6
        vecchi = [*carta.pezzi(), *m.pezzi(), g, tag]
        self.add(*vecchi)

        # beat 0 («La prima era scritta bene.»): esce tutto; a sinistra A1, a destra C4
        pad = 30
        sx = Mail([("saluto", testo(SALUTO_A, "piede", larghezza_px=430 - 2 * pad), 14),
                   ("barre", barre([300, 340, 220]), 18),
                   ("chiusa", testo(CHIUSA_A_TESTO.replace("colloquio", "==colloquio==", 1), "piede",
                                    larghezza_px=430 - 2 * pad), 18)], 0, x=X0, larghezza=430, pad=pad)
        dx_ = Mail([("saluto", testo(SALUTO_C, "piede", larghezza_px=430 - 2 * pad), 14),
                    ("barre", barre([330]), 16),
                    ("riga", testo(RIGA_C_TESTO.replace("2.100", "==2.100==", 1), "piede", larghezza_px=430 - 2 * pad), 16),
                    ("anni", testo(ANNI_C, "piede", colore=P.attenuato), 12),
                    ("barre2", barre([280]), 16),
                    ("sare", testo(SARE_C, "piede", larghezza_px=430 - 2 * pad), 16)], 0, x=530, larghezza=430, pad=pad)
        y_dx = 232 + (964 - h(dx_.box)) / 2
        y_sx = y_dx + (h(dx_.box) - h(sx.box)) / 2
        for mm, y in ((sx, y_sx), (dx_, y_dx)):
            for p_ in mm.pezzi():
                p_.shift(DOWN * px(y))
        for p_ in sx.pezzi():
            p_.set_z_index(p_.z_index + 2 if p_ is sx.box else 3)
        # prima esce tutto (anche i testi della mail di C4), poi il riquadro cambia forma, poi entrano i testi nuovi:
        # nessun testo si vede attraverso un riquadro in movimento
        self.play(*fuori(*[v for v in vecchi if v is not m.box], rate_func=fra(0, 0.28, rush_into)),
                  Transform(m.box, dx_.box, rate_func=fra(0.3, 0.72, ease_out_cubic)),
                  *dentro(*dx_.testi(), rate_func=fra(0.7, 1.0)),
                  *dentro(*sx.pezzi(), shift=RIGHT * 0.8, rate_func=fra(0.5, 0.95, ease_out_back)),
                  run_time=1.1)

        # beat 1 («Solo che poteva firmarla chiunque.»): MOLTIPLICAZIONE. La prima mail si riduce a sagoma (il suo testo
        # esce) e prende il suo posto in un muro di 24 sagome simili, che crescono intorno a lei fino a coprire la metà
        # sinistra; nessuna copia ha testo leggibile. La mail nuova resta sola a destra.
        self.beat(1)
        celle = [(r, col) for r in range(6) for col in range(4)]
        sua = (2, 1)
        def cella(r, col):
            return X0 + col * 113, 272 + r * 148
        x_s, y_s = cella(*sua)
        mia = sagoma(x_s, y_s, 105, 140, seme=99)
        mia[0].set_stroke(P.terziario, width=tratto(4)).set_z_index(1)
        mia[1].set_z_index(2)
        muro = [sagoma(*cella(r, col), 105, 140, seme=r * 4 + col) for r, col in celle if (r, col) != sua]
        centro_s = mia.get_center()
        muro.sort(key=lambda g_: np.linalg.norm(g_.get_center() - centro_s))
        # prima escono i testi della prima mail (tutti: un testo che rimpicciolisce con il riquadro passa sopra gli
        # altri), poi il riquadro si stringe a sagoma e le sue righe grigie entrano; il muro cresce intorno
        self.play(*fuori(sx.titolo, *[sx.p[k] for k in ("saluto", "barre", "chiusa")], rate_func=fra(0, 0.17)),
                  Transform(sx.box, mia[0], rate_func=fra(0.17, 0.45, ease_out_cubic)),
                  FadeIn(mia[1], rate_func=fra(0.36, 0.48)),
                  *[GrowFromCenter(g_, rate_func=fra(0.36 + 0.018 * k, 0.36 + 0.018 * k + 0.24, ease_out_back))
                    for k, g_ in enumerate(muro)],
                  run_time=self.arrotonda(min(1.5, 0.75 * self.durata_beat(1))))
        muro.append(mia)
        self.remove(sx.box)
        self.add(mia)

        # beat 2 («Questa la puoi firmare solo tu.»): muro e prima mail escono; la mail nuova al centro, compatta sulla
        # riga del numero; il messaggio sopra, la CTA sotto
        self.beat(2)
        msg = Messaggio(self.scena["messaggio"], maiuscolo=False)
        cta = Etichetta(self.scena["cta"])
        fin = Mail([("riga", testo(RIGA_C_TESTO.replace("2.100", "==2.100==", 1), "token", larghezza_px=828), 14),
                    ("anni", testo(ANNI_C, "piede", colore=P.attenuato), 12)], 0)
        tot = h(msg) + 40 + h(fin.box) + 40 + h(cta)
        y0 = 232 + (964 - tot) / 2
        a_ul(msg, X0, y0)
        for p_ in fin.pezzi():
            p_.shift(DOWN * px(fondo(msg) + 40))
        a_ul(cta, X0, fondo(fin.box) + 40)
        # il muro esce prima che entri il messaggio; la riga del numero cambia impaginazione glifo per glifo (mai due
        # copie dello stesso testo a schermo); i testi che non restano escono prima che il riquadro si muova
        # (`reimpagina`: prima ogni riga va alla x e al corpo d'arrivo restando riga, poi «portato gli iscritti da»
        # sale in verticale accanto a «ho»: nessuna parola passa sopra un'altra). Riquadro e «…da [numero] anni.»
        # fanno le stesse due tappe: su tre righe, poi su due.
        passo = fin.p["riga"].righe[0].get_center()[1] - fin.p["riga"].righe[1].get_center()[1]
        box_3 = a_ul(riquadro(LARG, h(fin.box) + passo * K, P.terziario), X0, alto(fin.box))
        anni = dx_.p["anni"]
        c0, c1, c2 = 0.25, 0.62, 0.85
        self.play(*fuori(*muro, shift=LEFT * 1.5, rate_func=fra(0, 0.3, rush_into)),
                  *fuori(dx_.p["saluto"], dx_.p["barre"], dx_.p["barre2"], dx_.p["sare"], rate_func=fra(0, 0.25)),
                  a_tappe(m.box, [m.box.copy(), box_3, fin.box], [c0, c1, c2], [ease_out_cubic, smooth]),
                  dx_.titolo.animate(rate_func=fra(c0, c1, ease_out_cubic)).move_to(fin.titolo),
                  *reimpagina(dx_.p["riga"], fin.p["riga"], c0, c1, c2),
                  a_tappe(anni, [anni.copy(), anni.copy().move_to(fin.p["anni"]).shift(DOWN * passo),
                                 anni.copy().move_to(fin.p["anni"])], [c0, c1, c2], [ease_out_cubic, smooth]),
                  FadeIn(msg, shift=DOWN * 0.3, rate_func=fra(0.45, 0.9, ease_out_cubic)),   # il riquadro è già sceso
                  FadeIn(cta, scale=0.8, rate_func=fra(0.7, 1.0, ease_out_back)),
                  run_time=1.05)
