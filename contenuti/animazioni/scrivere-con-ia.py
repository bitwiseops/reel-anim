"""Animazioni di «All'IA chiedi i problemi, non le parole»
(contenuti/sceneggiature/2026-09-21-scrivere-con-ia.md).

Regime «il reel si guarda muto» (docs/animazioni.md §0): le caption col parlato si bruciano in fondo, quindi qui
**non c'è nessuna frase da leggere**. A schermo: figure, numeri e quattro etichette corte.

Struttura a 9 scene (2026-09-21): la 1 è il presentatore a tutto schermo e **non ha classe**; la 3, la 5 e la 7 sono
a filmato (`[broll]`) e non hanno classe. Animate: 2, 4, 6, 8, e la 9 che disegna **solo** il messaggio e la CTA, in
coda, su fondo trasparente sopra la faccia (docs/animazioni.md §5).
Fra ogni coppia di scene animate c'è un filmato: il primo fotogramma di 4, 6 e 8 è **lo stato di fine** della scena
animata prima (`fine_2`, `fine_4`, `fine_6`: stesse funzioni, stessa area con riquadro e caption), e il primo
cambiamento parte subito. La 2 arriva da uno stacco sulla faccia, la 8 finisce su uno stacco verso la faccia.

La convenzione, imparata nella scena 2 e mai tradita (Note di produzione della sceneggiatura):
- **la mail è una carta di cinque blocchi di righe-sagoma**, uno per frase, con le proporzioni vere delle cinque
  frasi della bozza (9/30/17/7/12 parole → 2/4/3/1/2 righe: il quarto è il più corto, il secondo il più alto);
- **acceso in accento = frase tua**, **grigio = frase sua**; contare le frasi tue è contare i blocchi accesi;
- il **contatore** ripete lo stesso conto come numero, con un metro solo: 5 → ? → 1 → 5 → 2 → 5, e l'ultimo 5, in
  accento pieno, arriva alla fine della scena 8;
- la **richiesta è una pastiglia con un'icona** (mai una riga di testo): `sparkles` → `sparkles` + `user` → lente.
  Pastiglia, lente e segni sono in `secondario`: tutto ciò che è dell'IA ha quel colore (così non si confonde con
  l'accento, che vuol dire «tua»). La Croce della scena 8 è in accento: è la tua decisione.
"""
from __future__ import annotations

import random

import numpy as np
from manim import (BOLD, DOWN, LEFT, RIGHT, UP, AnimationGroup, Circle, Create, Ellipse, FadeIn, FadeOut,
                   FadeTransform, GrowFromCenter, GrowFromEdge, Line, RoundedRectangle, ShowPassingFlash, Transform,
                   VGroup, VMobject, Wiggle, rate_functions, smooth, squish_rate_func, there_and_back)
from manim.constants import CapStyleType

from tools.anim.base import ScenaReel
from tools.anim.componenti import Croce, Etichetta, Icona, Lente, Messaggio, etichetta, testo
from tools.anim.misure import px, tratto
from tools.anim.pattern import rimbalzo

# i due TESTO della scena 2: le scene 4, 6 e 8 li rimettono in scena come li avevamo lasciati
NOTA = "esempio inventato"
PROVE = "10 prove"

# --- misure condivise fra le scene (px della tela; l'area contenuto delle scene 2-8 è 900 × 752) -----------
RIGA_W = 520          # larghezza di una riga piena
RIGA_H = 13
PASSO = 30            # riga a riga dentro un blocco
GAP = 20              # aria in più fra un blocco e l'altro
PAD_X, PAD_Y = 40, 32
N_RIGHE = (2, 4, 3, 1, 2)     # le proporzioni vere delle cinque frasi: 9/30/17/7/12 parole

CARTA_GIU = 198       # bordo alto della carta, px sotto il bordo alto dell'area (sotto il contatore)
CONT_GIU = 6          # bordo alto del contatore, in alto a sinistra
NOTA_GIU = 698        # la nota «esempio inventato», sotto la carta
PAST_R = 70           # raggio della pastiglia della richiesta
PAST_DX = 215         # la pastiglia si appoggia sulla metà destra del bordo alto
LENTE_R = 280         # la lente al massimo: l'oggetto più grande dello schermo (4× la pastiglia)
LENTE_R_SCAN = 150    # la lente che scorre sulla carta

ACCESO_OP = 0.95      # opacità di un blocco acceso
SPENTO_OP = 0.5

# le cinque frasi come lunghezze di riga (0-1). Il blocco 3 (indice 3, la data) è **sempre** identico quando torna
# identico davvero; la scheggia (le ultime due righe del blocco 2) resta identica anche nella mail che ti riscrivi tu.
BOZZA = [[0.95, 0.25], [0.97, 0.99, 0.92, 0.92], [0.98, 0.94, 0.28], [0.90], [0.99, 0.51]]
RISCRITTA_A = [[0.99, 0.46], [0.93, 0.99, 0.96, 0.61], [0.99, 0.87, 0.40], [0.90], [0.96, 0.67]]
RISCRITTA_A2 = [[0.97, 0.38], [0.99, 0.94, 0.99, 0.48], [0.95, 0.92, 0.52], [0.90], [0.99, 0.55]]
RISCRITTA_B = [[0.95, 0.25], [0.96, 0.98, 0.90, 0.72], [0.99, 0.91, 0.33], [0.90], [0.98, 0.58]]
RICOMPOSTA = [[0.84, 0.30], [0.86, 0.82, 0.85, 0.50], [0.80, 0.94, 0.28], [0.78], [0.86, 0.44]]

SCHEGGIA = (2, (1, 2))   # la frase a cui teneva: le ultime due righe del terzo blocco


# --- aiuti locali -------------------------------------------------------------------------------------------


def giu(a, m, giu_px: float, dx_px: float = 0.0):
    """Mette `m` con il bordo alto a `giu_px` px sotto il bordo alto dell'area, spostato di `dx_px` dal centro."""
    m.move_to([a.centro[0] + px(dx_px), a.y1 - px(giu_px) - m.height / 2, 0])
    return m


def angolo(a, m, giu_px: float, sx_px: float = 0.0):
    """Mette `m` col bordo alto-sinistra a `giu_px` sotto il bordo alto e `sx_px` dal bordo sinistro dell'area."""
    m.move_to([a.x0 + px(sx_px) + m.width / 2, a.y1 - px(giu_px) - m.height / 2, 0])
    return m


def y_giu(a, giu_px: float) -> float:
    return a.y1 - px(giu_px)


def dx(a, dx_px: float) -> float:
    return a.centro[0] + px(dx_px)


def attenua(m, fattore: float):
    """Abbassa l'intensità **senza toccare i colori**: `set_opacity` su un'icona SVG accende un riempimento fuori
    palette e il controllo `colore` lo segnala (docs/animazioni.md §10)."""
    for x in m.family_members_with_points():
        so, fo = x.get_stroke_opacity(), x.get_fill_opacity()
        if so > 0:
            x.set_stroke(opacity=so * fattore)
        if fo > 0:
            x.set_fill(opacity=fo * fattore)
    return m


def nota(sc, a):
    """«esempio inventato», la didascalia di onestà della scena 2: resta sotto la carta finché resta la carta."""
    n = etichetta(testo(NOTA, "piede", colore=sc.cfg.palette.attenuato))
    return giu(a, n, NOTA_GIU, dx_px=190)


# --- la carta della mail ------------------------------------------------------------------------------------

def _altezza_blocchi() -> float:
    dentro = sum(n * RIGA_H + (n - 1) * (PASSO - RIGA_H) for n in N_RIGHE)
    return dentro + (len(N_RIGHE) - 1) * (PASSO - RIGA_H + GAP)


CARTA_W = RIGA_W + 2 * PAD_X
CARTA_H = _altezza_blocchi() + 2 * PAD_Y
SALTO_BLOCCO = RIGA_H + PASSO - RIGA_H + GAP     # quanto scende un blocco quando il quarto (una riga) gli va sopra


class Foglio(VGroup):
    """La carta della mail: un riquadro e cinque blocchi di righe-sagoma, uno per frase. Acceso in accento =
    frase tua, grigio = frase sua. Non tiene riferimenti alla scena (solo stringhe di colore), così `copy()` e
    `generate_target()` funzionano (docs/animazioni.md §10, RecursionError di `cfg.palette`)."""

    def __init__(self, quote, accesi, acceso: str, spento: str, bordo: str, sfondo: str, **kw):
        super().__init__(**kw)
        self.acceso, self.spento = acceso, spento
        self.box = RoundedRectangle(corner_radius=px(22), width=px(CARTA_W), height=px(CARTA_H),
                                    stroke_color=bordo, stroke_width=tratto(3), fill_color=sfondo, fill_opacity=1)
        self.blk = self._blocchi(quote, accesi)
        self._al_posto(self.blk)
        self.add(self.box, self.blk)

    def _al_posto(self, b):
        b.align_to(self.box, UP).shift(DOWN * px(PAD_Y))
        b.align_to(self.box, LEFT).shift(RIGHT * px(PAD_X))

    def _blocchi(self, quote, accesi) -> VGroup:
        blocchi = VGroup()
        for i, q in enumerate(quote):
            on = i in accesi
            righe = VGroup(*[RoundedRectangle(corner_radius=px(RIGA_H / 2), width=px(RIGA_W * x), height=px(RIGA_H),
                                              stroke_width=0, fill_color=self.acceso if on else self.spento,
                                              fill_opacity=ACCESO_OP if on else SPENTO_OP) for x in q])
            righe.arrange(DOWN, buff=px(PASSO - RIGA_H), aligned_edge=LEFT)
            blocchi.add(righe)
        blocchi.arrange(DOWN, buff=px(PASSO - RIGA_H + GAP), aligned_edge=LEFT)
        return blocchi

    def blocchi_come(self, quote, accesi) -> VGroup:
        """Gli stessi cinque blocchi con altre lunghezze di riga, già al loro posto sulla carta (e nella scala
        attuale della carta)."""
        b = self._blocchi(quote, accesi)
        b.scale(self.box.width / px(CARTA_W), about_point=b.get_corner(UP + LEFT))
        self._al_posto_scalato(b)
        return b

    def _al_posto_scalato(self, b):
        k = self.box.width / px(CARTA_W)
        b.align_to(self.box, UP).shift(DOWN * px(PAD_Y) * k)
        b.align_to(self.box, LEFT).shift(RIGHT * px(PAD_X) * k)

    def scheggia(self) -> VGroup:
        i, righe = SCHEGGIA
        return VGroup(*[self.blk[i][k] for k in righe])

    def sostituisci(self, sc, nuovi, quali):
        """Dopo un'animazione che ha fatto entrare `nuovi[i]` al posto di `blk[i]`: aggiorna la struttura e rimette
        la carta intera **dove stava nella lista della scena**. Il `FadeOut` di un blocco spezza la carta in pezzi
        e i blocchi nuovi entrano in cima: un `sc.add(self)` la riporterebbe sopra a tutto (sopra la pastiglia)."""
        for i in quali:
            self.blk.submobjects[i] = nuovi[i]
        fam = {id(m) for m in self.get_family()}
        pos = next((k for k, m in enumerate(sc.mobjects) if id(m) in fam), len(sc.mobjects))
        sc.mobjects = [m for m in sc.mobjects if id(m) not in fam]
        sc.mobjects.insert(pos, self)


def foglio(sc, quote=BOZZA, accesi=(0, 1, 2, 3, 4), area=None, giu_px: float = CARTA_GIU) -> Foglio:
    col = sc.cfg.palette
    f = Foglio(quote, set(accesi), col.accento, col.attenuato, col.attenuato, col.sfondo)
    giu(area or sc.area.contenuto, f, giu_px)
    return f


def riscrivi(f: Foglio, nuovi: VGroup, quali, passo: float = 0.13, largo: float = 0.16) -> list:
    """«Riscrivi»: un blocco alla volta, dall'alto, le righe vecchie si ritirano e le nuove si ridisegnano da
    sinistra a destra. Le finestre di un blocco non si accavallano (prima esce il vecchio, poi entra il nuovo)."""
    anims = []
    for k, i in enumerate(quali):
        p = passo * k
        anims.append(FadeOut(f.blk[i], shift=RIGHT * 0.08, rate_func=squish_rate_func(smooth, p, p + largo)))
        for j, r in enumerate(nuovi[i]):
            q = p + largo + 0.02 + 0.03 * j
            anims.append(GrowFromEdge(r, LEFT, rate_func=squish_rate_func(rate_functions.ease_out_cubic,
                                                                          min(q, 0.97), min(q + largo, 1.0))))
    return anims


# --- il contatore «frasi tue» -------------------------------------------------------------------------------

class Conta(VGroup):
    """Il metro del reel, uno solo dall'inizio alla fine: quante delle cinque frasi hanno ancora le tue parole.
    Numero grande + «su 5» + etichetta; `memoria` è il valore del giro prima, piccolo e spento accanto;
    `prove` è l'etichetta di provenienza, agganciata al numero (solo quando il numero è l'esito di una prova)."""

    def __init__(self, valore, colore: str, spento: str, memoria=None, prove: str | None = None, **kw):
        super().__init__(**kw)
        self.colore = colore
        self.numero = testo(str(valore), "messaggio", colore=colore, peso=BOLD, mono=True)
        riga = VGroup(self.numero)
        self.resto = testo("su 5", "token", colore=spento, mono=True)
        self.resto.next_to(self.numero, RIGHT, buff=px(14)).align_to(self.numero, DOWN)
        riga.add(self.resto)
        self.mem = None
        if memoria is not None:
            self.mem = testo(str(memoria), "token", colore=spento, mono=True)
            self.mem.next_to(self.resto, RIGHT, buff=px(40)).align_to(self.numero, DOWN)
            attenua(self.mem, 0.45)
            riga.add(self.mem)
        self.nome = testo("frasi tue", "etichetta", colore=spento)
        voci = VGroup(riga, self.nome)
        self.prove = None
        if prove:
            self.prove = testo(prove, "piede", colore=spento)
            voci.add(self.prove)
        voci.arrange(DOWN, buff=px(10), aligned_edge=LEFT)
        self.voci = voci
        self.add(voci)
        etichetta(self)

    def a(self, valore, colore: str | None = None, **kw):
        """Il numero cambia restando ancorato a sinistra (la colonna non si sposta)."""
        nuovo = testo(str(valore), "messaggio", colore=colore or self.colore, peso=BOLD,
                      mono=True).move_to(self.numero, aligned_edge=LEFT)
        etichetta(nuovo)
        return Transform(self.numero, nuovo, **kw)


def conta(sc, valore, acceso: bool = False, memoria=None, prove: str | None = None, area=None) -> Conta:
    col = sc.cfg.palette
    c = Conta(valore, col.accento if acceso else col.attenuato, col.attenuato, memoria=memoria, prove=prove)
    angolo(area or sc.area.contenuto, c, CONT_GIU, 0)
    return c


# --- la richiesta: una pastiglia con un'icona ---------------------------------------------------------------

def pastiglia(sc, icona: str = "sparkles", raggio_px: float = PAST_R) -> VGroup:
    """La richiesta al modello: mai una riga di testo, sempre una pastiglia tonda con dentro un'icona."""
    col = sc.cfg.palette
    disco = Circle(radius=px(raggio_px), stroke_width=0, fill_color=col.secondario, fill_opacity=1)
    ico = Icona(icona, altezza_px=raggio_px * 1.05, colore=col.sfondo).move_to(disco)
    return VGroup(disco, ico)


def posa_pastiglia(sc, a) -> VGroup:
    p = pastiglia(sc)
    return giu(a, p, CARTA_GIU - 2 * PAST_R, dx_px=PAST_DX)


def toppa(sc, past, raggio_px: float = 34) -> VGroup:
    """La toppa «mantenendo il mio stile»: una piccola icona `user` nell'accento dei blocchi «frasi tue»."""
    col = sc.cfg.palette
    disco = Circle(radius=px(raggio_px), stroke_color=col.accento, stroke_width=tratto(4),
                   fill_color=col.sfondo, fill_opacity=1)
    ico = Icona("user", altezza_px=raggio_px * 1.1, colore=col.accento).move_to(disco)
    return VGroup(disco, ico).move_to(past.get_center() + np.array([px(66), -px(30), 0]))


def lente(sc, raggio_px: float = LENTE_R) -> VGroup:
    """La richiesta che cambia mossa: la lente (componente `Lente`) con un manico, nel colore dell'IA."""
    col = sc.cfg.palette
    le = Lente(raggio_px=raggio_px, colore=col.secondario, spessore_px=max(6, raggio_px / 22))
    d = np.array([0.7071, -0.7071, 0.0])      # manico in basso a destra, come una lente in mano
    c = le.cerchio.get_center()
    manico = Line(c + d * px(raggio_px), c + d * px(raggio_px * 1.42), stroke_color=col.secondario,
                  stroke_width=tratto(raggio_px / 10))
    manico.cap_style = CapStyleType.ROUND
    le.add(manico)
    return le


# --- i segni che la lente lascia --------------------------------------------------------------------------

def segno(sc, largo_px: float = 86, alto_px: float = 30, meta: bool = False, opacita: float = 1.0,
          spessore_px: float = 4) -> VGroup:
    """Un segno del correttore: un anellino attorno a un pezzo di riga. Non cambia la riga (la tesi della scena 6
    è che la carta non cambia), e non è un conto: alcuni escono dal quadro, uno è tagliato, l'ultimo sfuma."""
    col = sc.cfg.palette
    e = Ellipse(width=px(largo_px), height=px(alto_px), stroke_color=col.secondario,
                stroke_width=tratto(spessore_px), fill_opacity=0)
    if meta:
        mezzo = VMobject(stroke_color=col.secondario, stroke_width=tratto(spessore_px))
        mezzo.pointwise_become_partial(e, 0.0, 0.5)       # la metà di sopra: il resto è oltre il bordo
        e = mezzo
    if opacita != 1.0:
        e.set_stroke(opacity=opacita)
    return VGroup(e)


CHIAVE = 3   # nella lista dei segni, quello sulla scheggia: la scena 8 gli attacca l'etichetta


def posa_segni(sc, f: Foglio) -> list[VGroup]:
    """I segni della scena 6, posati su righe diverse dei primi tre blocchi. Due sporgono dal bordo destro della
    carta, uno è tagliato a metà sul bordo basso, l'ultimo sfuma: la quantità non si può contare. Il quarto
    (`CHIAVE`) sta sulla scheggia: è quello a cui la scena 8 attacca «segnalata 10 su 10»."""
    def su_riga(blocco, riga, da_sinistra_px, **kw):
        s = segno(sc, **kw)
        r = f.blk[blocco][riga]
        s.move_to([r.get_left()[0] + px(da_sinistra_px), r.get_center()[1], 0])
        return s

    segni = [su_riga(0, 0, 170),
             su_riga(1, 1, 560, largo_px=96),          # sporge dal bordo destro
             su_riga(1, 3, 70, largo_px=104),
             su_riga(2, 1, 330, largo_px=120),         # CHIAVE: sulla scheggia
             su_riga(2, 0, 566, largo_px=92),          # sporge dal bordo destro
             su_riga(0, 1, 64, opacita=0.3)]           # sfuma: la fila continua
    tagliato = segno(sc, largo_px=92, meta=True)
    tagliato.move_to([f.box.get_left()[0] + px(220), f.box.get_bottom()[1] + tagliato.height / 2 - px(2), 0])
    segni.append(tagliato)
    return segni


def anello(sc, mob, buff_px: float = 16) -> RoundedRectangle:
    """Il cerchio sottile attorno al quarto blocco («la notizia arriva per quarta»)."""
    return RoundedRectangle(corner_radius=px(18), width=mob.width + px(2 * buff_px),
                            height=mob.height + px(2 * buff_px), stroke_color=sc.cfg.palette.secondario,
                            stroke_width=tratto(3), fill_opacity=0).move_to(mob)


# --- la folla di mail-sagoma della scena 4 ------------------------------------------------------------------

def mail_sagoma(sc, r: random.Random, larghezza_px: float = 156) -> VGroup:
    """Una mail qualunque: un riquadro opaco con quattro-sei righe di lunghezze **visibilmente diverse**. Simili
    e mai identiche, perché le dieci uscite vere sono diverse fra loro."""
    col = sc.cfg.palette
    h, passo = 7, 17
    quote = [round(r.uniform(0.35, 1.0), 2) for _ in range(r.randint(4, 6))]
    righe = VGroup(*[RoundedRectangle(corner_radius=px(h / 2), width=px((larghezza_px - 30) * q), height=px(h),
                                      stroke_width=0, fill_color=col.attenuato, fill_opacity=0.8) for q in quote])
    righe.arrange(DOWN, buff=px(passo - h), aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=px(10), width=px(larghezza_px), height=righe.height + px(30),
                           stroke_color=col.attenuato, stroke_width=tratto(2), fill_color=col.sfondo, fill_opacity=1)
    righe.move_to(box)
    return VGroup(box, righe)


def folla(sc, quante: int = 46, seme: int = 7) -> VGroup:
    """La folla: sagome sovrapposte e sfalsate, **mai in griglia e mai contabili**, che continuano oltre i bordi.
    A destra e a sinistra escono dalla tela; in alto, a sinistra del riquadro del presentatore, salgono oltre il
    bordo dell'area; in basso c'è la fascia delle caption, che non si tocca: lì le ultime sfumano, come se la folla
    continuasse sotto."""
    a = sc.area.contenuto
    r = random.Random(seme)
    g = VGroup()
    for _ in range(quante):
        m = mail_sagoma(sc, r, larghezza_px=r.uniform(140, 190))
        m.rotate(r.uniform(-10, 10) * np.pi / 180)
        x = r.uniform(-560, 560)
        alto = -70 if x < 20 else 20          # sopra l'area solo lontano dal riquadro (in alto a destra)
        y = r.uniform(alto, 700)
        m.move_to([dx(a, x), y_giu(a, y), 0])
        if m.get_bottom()[1] < a.y0 + px(4):  # mai nella fascia delle caption
            m.shift(UP * (a.y0 + px(4) - m.get_bottom()[1]))
        if m.get_bottom()[1] < a.y0 + px(70):
            attenua(m, 0.35)                   # in fondo sfumano: la folla continua sotto
        g.add(m)
    g.set_z_index(-3)
    return g


# ============================================================================================================
def fine_2(sc):
    """L'ultimo fotogramma della scena 2, ricostruito: la scena 4 parte da lì (dopo il filmato della 3)."""
    a = sc.area.contenuto
    f = foglio(sc, RISCRITTA_A, accesi={3})
    c = conta(sc, 1, prove=PROVE)
    past = posa_pastiglia(sc, a)
    return f, c, past, nota(sc, a)


class Scena02(ScenaReel):
    """La bozza, la richiesta «migliora questa mail», il vuoto della scommessa e il conto.
    GRANDE (tipografia cinetica) sul beat 3: dal «?» arriva un 1 alto un quarto di schermo."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        self.f = foglio(self, BOZZA, accesi=())         # stacco dalla faccia: al fotogramma 0 la carta c'è già, grigia
        self.nota = etichetta(testo(self.scena["testo"][0], "piede", colore=col.attenuato))
        giu(a, self.nota, NOTA_GIU, dx_px=190)
        self.add(self.f, self.nota)

        # beat 0 — «cinque frasi»: i cinque blocchi si accendono uno dopo l'altro, poi entra il contatore
        accesa = self.f.blocchi_come(BOZZA, accesi=range(5))
        self.play(AnimationGroup(*[Transform(self.f.blk[i], accesa[i]) for i in range(5)], lag_ratio=0.35),
                  run_time=self.arrotonda(2.2))
        self.cont = conta(self, 5)
        self.play(FadeIn(self.cont, shift=RIGHT * 0.2), run_time=0.7)

        # beat 1 — la richiesta scende e si appoggia sul bordo alto della carta, che si abbassa sotto il peso
        self.beat(1)
        self.past = posa_pastiglia(self, a)
        posa = self.past.get_center().copy()
        self.past.shift(UP * px(104))
        self.play(FadeIn(self.past, shift=DOWN * 0.2), run_time=0.35)
        self.play(self.past.animate.move_to(posa), run_time=0.45, rate_func=rate_functions.ease_in_quad)
        self.play(self.f.animate(rate_func=there_and_back).shift(DOWN * px(12)), run_time=0.45)

        # beat 2 — il contatore scivola al centro e il valore diventa un «?»: un secondo di vuoto vero
        self.beat(2)
        self.play(self.cont.animate.shift(RIGHT * (a.centro[0] - self.cont.get_center()[0])), run_time=0.6)
        self.play(self.cont.a("?", colore=col.accento), run_time=0.35)
        self.play(self.cont.numero.animate(rate_func=there_and_back).scale(1.22), run_time=1.1)

        # beat 3 — GRANDE (tipografia cinetica): la carta si rifà un blocco alla volta (il quarto resta acceso
        # identico) e dal «?» arriva un 1 enorme che spinge indietro la carta; poi torna piccolo in alto a sinistra
        self.beat(3)
        self.play(self.past.animate(rate_func=there_and_back).scale(1.2), run_time=0.3)
        nuovi = self.f.blocchi_come(RISCRITTA_A, accesi={3})
        self.play(*riscrivi(self.f, nuovi, (0, 1, 2, 4), passo=0.12, largo=0.2), run_time=self.arrotonda(1.25))
        self.f.sostituisci(self, nuovi, (0, 1, 2, 4))

        indietro = self.f.copy().scale(0.8)
        giu(a, indietro, CARTA_GIU + 50)
        attenua(indietro, 0.35)
        uno = testo("1", "punch", colore=col.accento, peso=BOLD, mono=True)
        etichetta(uno)
        uno.scale_to_fit_height(px(400)).move_to([a.centro[0], y_giu(a, 400), 0])
        seme = uno.copy().scale_to_fit_height(self.cont.numero.height).move_to(self.cont.numero)
        grande, uno = uno, seme
        self.remove(self.cont.numero)
        self.add(uno)
        self.play(Transform(self.f, indietro),
                  FadeOut(VGroup(self.cont.resto, self.cont.nome), scale=0.6),
                  Transform(uno, grande, rate_func=rimbalzo(0.08)),
                  run_time=self.arrotonda(0.95))
        self.remove(self.cont)
        self.wait(0.3)                      # l'1 enorme resta un attimo: è la risposta alla scommessa
        self.cont = conta(self, 1, prove=self.scena["testo"][1])
        avanti = foglio(self, RISCRITTA_A, accesi={3})
        self.play(Transform(uno, self.cont.numero.copy()), Transform(self.f, avanti),
                  run_time=self.arrotonda(0.6), rate_func=rate_functions.ease_in_out_sine)
        self.remove(uno)
        self.add(self.cont)
        self.remove(self.cont.resto, self.cont.nome, self.cont.prove)
        self.play(FadeIn(self.cont.resto), FadeIn(self.cont.nome), FadeIn(self.cont.prove), run_time=0.35)


# ============================================================================================================
def fine_4(sc):
    """L'ultimo fotogramma della scena 4, ricostruito: la scena 6 parte da lì (dopo il filmato della 5)."""
    a = sc.area.contenuto
    f = foglio(sc, RISCRITTA_B, accesi={0, 3})
    c = conta(sc, 2, memoria=1)
    past = posa_pastiglia(sc, a)
    return f, c, past, toppa(sc, past), nota(sc, a)


class Scena04(ScenaReel):
    """«Migliora» vuol dire «riscrivi», e riscrivendo pesca fra le parole di tutti.
    GRANDE (moltiplicazione) sul beat 1: la nostra mail sparisce dentro una folla di mail simili."""

    def costruisci(self):
        a = self.area.contenuto
        self.f, self.cont, self.past, self.nota = fine_2(self)     # dopo il filmato: la carta come l'avevamo lasciata
        self.add(self.f, self.cont, self.past, self.nota)

        # beat 0 — la richiesta si stacca, sale al centro e cresce; sotto di lei le righe si ridisegnano veloci
        salita = pastiglia(self).scale(1.5)
        giu(a, salita, 16)
        self.play(Transform(self.past, salita), run_time=0.7, rate_func=rate_functions.ease_out_cubic)
        nuovi = self.f.blocchi_come(RISCRITTA_A2, accesi={3})
        self.play(*riscrivi(self.f, nuovi, (0, 1, 2, 4), passo=0.16, largo=0.2), run_time=self.arrotonda(1.5))
        self.f.sostituisci(self, nuovi, (0, 1, 2, 4))

        # beat 1 — GRANDE (moltiplicazione): via ogni numero, la carta si rimpicciolisce in un angolo e dietro
        # sciama la folla; poi la nostra diventa una sagoma come le altre e non si distingue più
        self.beat(1)
        self.play(FadeOut(self.cont, shift=LEFT * 0.2), FadeOut(self.nota), FadeOut(self.past, scale=0.5),
                  run_time=0.4)
        posto = np.array([dx(a, -150), y_giu(a, 360), 0])
        piccola = self.f.copy().scale(0.27).move_to(posto)
        self.f.set_z_index(-1)
        self.play(Transform(self.f, piccola), run_time=0.7, rate_func=rate_functions.ease_in_out_sine)
        self.sciame = folla(self)
        ordine = sorted(self.sciame, key=lambda m: np.linalg.norm(m.get_center() - posto))   # dal centro ai bordi
        self.play(AnimationGroup(*[GrowFromCenter(m) for m in ordine], lag_ratio=0.03),
                  run_time=self.arrotonda(1.6))
        nostra = mail_sagoma(self, random.Random(101), larghezza_px=168).move_to(posto).rotate(4 * np.pi / 180)
        nostra.set_z_index(-3)
        self.play(FadeTransform(self.f, nostra), run_time=0.5)
        self.remove(self.f)
        self.nostra = nostra

        # beat 2 — la folla si sfila via di lato, torna la bozza con tutti e cinque i blocchi accesi, il
        # contatore torna a 5 (accanto, l'1 del giro prima) e alla pastiglia si attacca la toppa «user»
        self.beat(2)
        via = []
        for i, m in enumerate(list(self.sciame) + [self.nostra]):
            verso = LEFT if m.get_center()[0] < a.centro[0] else RIGHT
            via.append(FadeOut(m, shift=verso * 2.4, rate_func=squish_rate_func(rate_functions.rush_into,
                                                                               min(0.45, 0.01 * i), 1.0)))
        self.f = foglio(self, BOZZA, accesi=range(5))
        self.cont = conta(self, 5, memoria=1)
        self.nota = nota(self, a)
        dentro = squish_rate_func(smooth, 0.55, 1.0)
        self.play(*via, FadeIn(self.f, shift=UP * 0.25, rate_func=dentro),
                  FadeIn(self.cont, shift=RIGHT * 0.2, rate_func=dentro), FadeIn(self.nota, rate_func=dentro),
                  run_time=self.arrotonda(1.3))
        self.remove(self.sciame)
        self.past = posa_pastiglia(self, a)
        self.play(FadeIn(self.past, shift=DOWN * 0.3), run_time=0.45, rate_func=rate_functions.ease_out_cubic)
        self.toppa = toppa(self, self.past)
        self.play(FadeIn(self.toppa, scale=0.6, rate_func=rimbalzo(0.1)), run_time=0.45)

        # beat 3 — la richiesta tocca di nuovo la carta: tre blocchi si spengono, due restano accesi,
        # il contatore scende da 5 a 2. Ultimo fotogramma: due accesi su cinque, tre riscritti.
        self.beat(3)
        self.play(VGroup(self.past, self.toppa).animate(rate_func=there_and_back).shift(DOWN * px(26)),
                  run_time=0.5)
        nuovi = self.f.blocchi_come(RISCRITTA_B, accesi={0, 3})
        self.play(*riscrivi(self.f, nuovi, (1, 2, 4), passo=0.2, largo=0.22), self.cont.a(2),
                  run_time=self.arrotonda(1.6))
        self.f.sostituisci(self, nuovi, (1, 2, 4))


# ============================================================================================================
class Scena06(ScenaReel):
    """La richiesta cambia mossa: non «migliorala» ma «elencami i problemi».
    GRANDE (contrasto di scala) sul beat 1: la pastiglia schizza via e al suo posto scende una lente enorme."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        self.f, self.cont, self.past, self.toppa, self.nota = fine_4(self)
        # dopo il filmato la mail riscritta rientra da sotto, com'era (tre grigi, due accesi)
        self.f.shift(DOWN * px(30))
        self.add(self.f, self.cont, self.past, self.toppa)

        # beat 0 — rientra, poi scende fuori dal basso; al suo posto torna la bozza intatta, il contatore torna a 5
        # e sopra resta sola la pastiglia, che si accende e trema
        self.play(self.f.animate.shift(UP * px(30)), FadeIn(self.nota, rate_func=squish_rate_func(smooth, 0.6, 1.0)),
                  run_time=0.25, rate_func=rate_functions.ease_out_cubic)
        bozza = foglio(self, BOZZA, accesi=range(5))
        cinque = conta(self, 5)
        self.play(FadeOut(self.f, shift=DOWN * 0.8, rate_func=squish_rate_func(rate_functions.rush_into, 0.0, 0.45)),
                  FadeOut(self.toppa, scale=0.5, rate_func=squish_rate_func(smooth, 0.0, 0.35)),
                  FadeIn(bozza, shift=DOWN * 0.3, rate_func=squish_rate_func(smooth, 0.38, 1.0)),
                  FadeOut(self.cont, rate_func=squish_rate_func(smooth, 0.0, 0.4)),
                  FadeIn(cinque, rate_func=squish_rate_func(smooth, 0.5, 1.0)),
                  run_time=self.arrotonda(0.7))
        self.f, self.cont = bozza, cinque
        self.remove(self.past)
        self.add(self.past)                 # la pastiglia sopra la carta nuova
        alone = Circle(radius=px(PAST_R), stroke_color=col.secondario, stroke_width=tratto(5),
                       fill_opacity=0).move_to(self.past)
        self.play(Wiggle(self.past, scale_value=1.12, rotation_angle=0.05 * np.pi, n_wiggles=5),
                  alone.animate(rate_func=rate_functions.ease_out_cubic).scale(1.6).set_stroke(opacity=0),
                  run_time=self.arrotonda(0.6))
        self.remove(alone)

        # beat 1 — GRANDE (contrasto di scala): la pastiglia arretra e schizza via dall'alto; al suo posto
        # scende la lente, che cresce fino a diventare l'oggetto più grande dello schermo. La carta non si muove.
        self.beat(1)
        self.play(self.past.animate.shift(DOWN * px(22)), run_time=0.25, rate_func=rate_functions.ease_out_quad)
        self.play(FadeOut(self.past, shift=UP * 3.2, rate_func=rate_functions.rush_into), run_time=0.4)
        centro = self.f.get_center()
        self.lente = lente(self, LENTE_R)
        self.lente.shift(centro + np.array([-px(40), px(40), 0]) - self.lente.cerchio.get_center())
        seme = lente(self, LENTE_R).scale(0.28).move_to([dx(a, PAST_DX), y_giu(a, CARTA_GIU - PAST_R), 0])
        grande = self.lente
        self.lente = seme
        self.play(FadeIn(self.lente, shift=DOWN * 0.3), run_time=0.3)
        self.play(Transform(self.lente, grande), run_time=self.arrotonda(1.1), rate_func=rimbalzo(0.05))

        # beat 2 — la lente si avvicina alla carta (si stringe) e scorre dall'alto in basso, lenta; la carta non
        # cambia di una riga
        self.beat(2)
        c0 = self.f.blk[0].get_center()
        vicina = lente(self, LENTE_R_SCAN)
        vicina.shift(np.array([self.f.get_center()[0] - px(20), c0[1], 0]) - vicina.cerchio.get_center())
        self.play(Transform(self.lente, vicina), run_time=0.5, rate_func=rate_functions.ease_in_out_sine)
        self.play(self.lente.animate.shift(DOWN * (c0[1] - self.f.blk[1].get_center()[1])),
                  run_time=self.arrotonda(max(0.6, self.durata_beat(2) - 0.75)), rate_func=rate_functions.linear)

        # beat 3 — la lente continua a scendere e dietro di lei restano i segni (non contabili, non tutti) e un
        # anello attorno al quarto blocco; poi esce di scena. Il contatore tiene 5 su 5
        self.beat(3)
        self.segni = posa_segni(self, self.f)
        self.anello = anello(self, self.f.blk[3])
        dur = self.arrotonda(min(2.6, 0.7 * self.durata_beat(3)))
        passaggio = self.f.blk[3].get_center()[1] - self.lente.get_center()[1]
        tempi = [0.02, 0.1, 0.22, 0.34, 0.4, 0.12, 0.9]      # quando la lente passa sulla riga di ciascun segno
        self.play(self.lente.animate(rate_func=rate_functions.ease_in_out_sine).shift(UP * passaggio),
                  *[Create(s, rate_func=squish_rate_func(smooth, t, min(1.0, t + 0.12)))
                    for s, t in zip(self.segni, tempi)],
                  Create(self.anello, rate_func=squish_rate_func(smooth, 0.8, 1.0)),
                  run_time=dur)
        self.play(FadeOut(self.lente, shift=RIGHT * 2.2 + DOWN * 0.4, rate_func=rate_functions.rush_into),
                  run_time=0.5)


# ============================================================================================================
def fine_6(sc):
    """L'ultimo fotogramma della scena 6, ricostruito: la scena 8 parte da lì (dopo il filmato della 7). La
    lente è già uscita: nella 8 non rientra più."""
    a = sc.area.contenuto
    f = foglio(sc, BOZZA, accesi=range(5))
    return f, conta(sc, 5), posa_segni(sc, f), anello(sc, f.blk[3]), nota(sc, a)


class Scena08(ScenaReel):
    """Il consiglio che non prendi, e la mail che ti riscrivi tu.
    GRANDE (metamorfosi) sul beat 1: i cinque blocchi si ricompongono da soli, senza nessun oggetto dell'IA.
    È l'ultima figura del reel: dopo c'è lo stacco sulla faccia."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        self.f, self.cont, self.segni, self.anello, self.nota = fine_6(self)
        self.add(self.f, self.anello, *self.segni, self.cont, self.nota)
        chiave = self.segni[CHIAVE]
        altri = [s for k, s in enumerate(self.segni) if k != CHIAVE]
        sch_idx = SCHEGGIA[1]

        # beat 0 — via il contatore (in questo beat nessun contatore è visibile) e la nota; zoom sul terzo blocco:
        # la carta cresce, il resto si spegne e la scheggia resta accesa, viva. Attaccata al segno sulla scheggia
        # entra l'etichetta del conto: parola e numero sulla stessa pastiglia, insieme.
        self.mondo = VGroup(self.f, self.anello, *self.segni)
        k = 1.45
        perno = self.f.blk[2].get_center()
        bersaglio = self.mondo.copy().scale(k, about_point=perno)
        sposta = np.array([a.centro[0] - bersaglio[0].get_center()[0], a.y1 - px(10) - bersaglio[0].get_top()[1], 0])
        bersaglio.shift(sposta)
        # nel bersaglio: le righe fuori dalla scheggia e i segni che non sono quello si spengono
        bf = bersaglio[0]
        for i, blocco in enumerate(bf.blk):
            for j, r in enumerate(blocco):
                if not (i == SCHEGGIA[0] and j in sch_idx):
                    r.set_fill(opacity=0.25)
        for kk, s in enumerate(bersaglio[2:]):
            if kk != CHIAVE:
                attenua(s, 0.3)
        attenua(bersaglio[1], 0.3)
        self.play(FadeOut(self.cont, shift=LEFT * 0.2, rate_func=squish_rate_func(smooth, 0.0, 0.4)),
                  FadeOut(self.nota, rate_func=squish_rate_func(smooth, 0.0, 0.4)),
                  Transform(self.mondo, bersaglio, rate_func=rate_functions.ease_in_out_cubic),
                  run_time=self.arrotonda(0.6))
        self.eti = Etichetta(self.scena["testo"][0], colore=col.secondario)
        self.eti.next_to(chiave, DOWN, buff=px(40)).align_to(chiave, LEFT).shift(LEFT * px(40))
        gancio = Line(chiave.get_bottom(), self.eti.get_top(), stroke_color=col.secondario, stroke_width=tratto(4))
        self.eti.set_z_index(2)
        self.play(FadeIn(self.eti, scale=0.85), Create(gancio), run_time=self.arrotonda(0.3))
        fermo_da = self.t

        # beat 1 — la Croce cade sul segno quando l'etichetta è rimasta ferma e leggibile almeno 1,5 s (se il beat 0
        # non la regge, in testa a questo beat); segno, etichetta e croce escono insieme, senza separarsi, lo zoom
        # torna sulla carta intera. Poi GRANDE (metamorfosi): prima cadono fuori tutti i segni, e solo quando sono
        # fuori — nessun oggetto dell'IA in scena — i cinque blocchi si ricompongono, tutti accesi; torna il 5
        self.beat(1)
        self.attendi_fino(fermo_da + 1.5)
        cr = Croce(altezza_px=86).move_to(chiave)
        cr.set_z_index(3)
        self.play(cr.entra(), run_time=self.arrotonda(0.3))
        marca = VGroup(chiave, self.eti, gancio, cr)
        self.mondo.remove(chiave)               # il segno scartato esce con la marca, non torna con la carta
        f0, _, segni0, anello0, _ = fine_6(self)   # la carta intera com'era, coi segni che restano
        piena = VGroup(f0, anello0, *[s for kk, s in enumerate(segni0) if kk != CHIAVE])
        self.play(FadeOut(marca, shift=RIGHT * 3.0, rate_func=squish_rate_func(rate_functions.rush_into, 0.0, 0.45)),
                  Transform(self.mondo, piena, rate_func=squish_rate_func(rate_functions.ease_in_out_cubic, 0.4, 1.0)),
                  run_time=self.arrotonda(0.8))
        via = [self.anello] + altri
        self.play(AnimationGroup(*[FadeOut(s, shift=DOWN * 1.6 + RIGHT * 0.3) for s in via], lag_ratio=0.1),
                  run_time=self.arrotonda(0.55), rate_func=rate_functions.ease_in_quad)
        for s in via:
            self.remove(s)
        self.mondo = None
        nuovi = self.f.blocchi_come(RICOMPOSTA, accesi=range(5))
        for i, blocco in enumerate(nuovi):   # la scheggia non la tocchi: resta identica, e più viva delle altre
            for j, r in enumerate(blocco):
                r.set_fill(opacity=1.0 if (i == SCHEGGIA[0] and j in sch_idx) else 0.8)
        self.cont = conta(self, 5)
        self.nota = nota(self, a)
        self.play(AnimationGroup(*[Transform(self.f.blk[i], nuovi[i]) for i in range(5)], lag_ratio=0.12,
                                 rate_func=rate_functions.ease_in_out_sine),
                  FadeIn(self.cont, shift=RIGHT * 0.2, rate_func=squish_rate_func(smooth, 0.55, 1.0)),
                  FadeIn(self.nota, rate_func=squish_rate_func(smooth, 0.55, 1.0)),
                  run_time=self.arrotonda(0.9))

        # beat 2 — il quarto blocco, il corto, sale al primo posto e gli altri scivolano giù di una posizione
        # (il corto si spegne dov'è e si riaccende in testa: due blocchi che si scambiano di posto nella stessa
        # colonna si attraverserebbero, docs/animazioni.md §10); sotto la scheggia corre la sottolineatura e il
        # contatore si accende in accento pieno: il loop si chiude qui
        self.beat(2)
        salto = px(SALTO_BLOCCO)
        testa = self.f.blk[3].copy()
        testa.align_to(self.f.blk[0], UP).align_to(self.f.blk[0], LEFT)
        self.play(FadeOut(self.f.blk[3], rate_func=squish_rate_func(smooth, 0.0, 0.3)),
                  *[self.f.blk[i].animate(rate_func=squish_rate_func(rate_functions.ease_in_out_sine, 0.32, 0.8))
                    .shift(DOWN * salto) for i in (0, 1, 2)],
                  FadeIn(testa, shift=DOWN * 0.15, rate_func=squish_rate_func(smooth, 0.82, 1.0)),
                  run_time=self.arrotonda(0.9))
        self.f.sostituisci(self, [None, None, None, testa], (3,))
        sch = self.f.scheggia()
        y = float(sch.get_bottom()[1]) - px(11)
        linea = Line([sch.get_left()[0] - px(4), y, 0], [sch.get_right()[0] + px(4), y, 0],
                     stroke_color=col.accento, stroke_width=tratto(6))
        linea.cap_style = CapStyleType.ROUND
        acceso = conta(self, 5, acceso=True)
        self.play(Create(linea, rate_func=rate_functions.ease_out_cubic),
                  Transform(self.cont, acceso, rate_func=squish_rate_func(smooth, 0.3, 1.0)),
                  run_time=self.arrotonda(0.6))


# ============================================================================================================
# Scena 1 e Scena 9: il presentatore a tutto schermo con le sole caption (2026-09-21), nessuna classe.
