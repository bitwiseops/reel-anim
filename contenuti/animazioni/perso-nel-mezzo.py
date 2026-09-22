"""Animazioni di «Quello che metti in mezzo, l'IA lo legge peggio»
(contenuti/sceneggiature/2026-09-21-perso-nel-mezzo.md).

Regime «il reel si guarda muto» (docs/animazioni.md §0): nessuna frase a schermo. A schermo solo figure, quattro
numeri (76, 54, 63, 56) e tre etichette (`TESTO:` della sceneggiatura): «Stanford, 2023», «% giuste», «0 paragrafi».

Struttura: scena 1 e 8 a volto pieno, scene 2, 4, 6 `[broll]`: **nessuna classe**. Animate 3, 5, 7: la 5 parte
dall'ultimo fotogramma della 3 e la 7 dall'ultimo della 5 (dopo il filmato si entra con un taglio su uno stato che
chi guarda riconosce), ricostruiti con `Quadro.fine_3()` e `Quadro.fine_5()`.

Il filo visivo (sempre stesso aspetto e stesso posto):
- la **colonna** di venti righe-sagoma (`Sagome`), il documento letto dall'alto in basso, a sinistra;
- la **riga accesa** (accento), il paragrafo con la risposta: si sposta nella 3, sta al decimo posto nella 5, vola
  in cima nella 7;
- la **carta «?»** sotto la colonna, la domanda: sempre nello stesso punto, in fondo;
- le **barre** accanto alle righe 1, 10 e 20 (e la barra «0 paragrafi» accanto alla carta), tutte sulla stessa scala:
  la pista vuota è il 100 %.

Mosse wow (manuale §11bis): 3 rivelazione a tratto (la U coricata), 5 contrasto di scala (zoom 5× breve sulla punta
del 54 e la linea del 56), 7 carica e rimbalzo (la riga accesa che vola in cima).

Posizioni in px della tela (origine in alto a sinistra) con `punto()`; l'area contenuto è 60..960 × 604..1356 px.
"""
from __future__ import annotations

import numpy as np
from manim import (BOLD, DOWN, LEFT, RIGHT, UP, Create, DashedLine, FadeIn, FadeOut, GrowFromEdge, Line, Rectangle,
                   RoundedRectangle, UpdateFromAlphaFunc, VGroup, VMobject, linear, rate_functions, smooth,
                   squish_rate_func, there_and_back)

from tools.anim.base import ScenaReel
from tools.anim.componenti import Didascalia, Indice, Lente, Sagome, Spunta, etichetta, testo
from tools.anim.config import carica
from tools.anim.misure import PX_PER_UNITA, px, tratto
from tools.anim.pattern import rimbalzo

CFG = carica()
P = CFG.palette
ease_out_cubic = rate_functions.ease_out_cubic
ease_out_sine = rate_functions.ease_out_sine
rush_into = rate_functions.rush_into

# --- testi a schermo (TESTO: della sceneggiatura; la 5 e la 7 li ereditano dalla 3) ---------------------------
FONTE = "Stanford, 2023"
GIUSTE = "% giuste"
ZERO = "0 paragrafi"

# --- misure condivise (px della tela) ------------------------------------------------------------------------
X_COL, W_COL, H_RIGA, PASSO, Y_SLOT0 = 84, 300, 12, 25, 690   # la colonna: 20 righe, slot k al centro y_slot(k)
N_RIGHE = 20
# lunghezze delle righe (frazioni di W_COL): simili, non uguali; la prima è la riga accesa
QUOTE = [0.9, 0.72, 0.95, 0.6, 0.84, 0.68, 0.92, 0.57, 0.8, 0.88,
         0.64, 0.93, 0.7, 0.62, 0.9, 0.75, 0.66, 0.94, 0.58, 0.82]
CARTA_X, CARTA_Y, CARTA_W, CARTA_H = 84, 1196, 150, 100       # la carta «?», sotto la colonna
X_BAR, L_BAR, H_BAR = 420, 480, 48                            # pista = 100 %
SLOT_BARRE = (0, 9, 19)
VALORI = (76, 54, 63)                                         # GPT-3.5-Turbo, 20 paragrafi, Tab. 6
VALORE_0 = 56                                                 # stesso modello senza paragrafi, Tab. 1
Y_BARRA_0 = CARTA_Y + CARTA_H / 2
NUM_BUFF = 22                                                 # dalla punta al numero
Y_GIUSTE = 610                                                # bordo alto di «% giuste»
# scena 7: il blocco di cinque righe, ingrandito 2×, sopra la carta
SCALA_BLOCCO, P_TOP = 2.0, 810
NASTRO = 1060                                                 # corsa del nastro: il blocco dopo arriva da fuori tela
X_LENTE = 250
RIGA_TROVATA = 3                                              # nel terzo blocco, la quarta riga si accende


def punto(x: float, y: float) -> np.ndarray:
    return np.array([px(x) - CFG.frame_width / 2, CFG.frame_height / 2 - px(y), 0.0])


def y_px(y: float) -> float:
    return (CFG.frame_height / 2 - y) * PX_PER_UNITA


def w_px(m) -> float:
    return m.width * PX_PER_UNITA


def y_slot(k: int) -> float:
    return Y_SLOT0 + PASSO * k


def fra(a: float, b: float = 1.0, f=smooth):
    """Curva `f` compressa nella frazione [a, b] della play (movimenti sfalsati in un solo passaggio)."""
    return squish_rate_func(f, max(0.0, a), min(1.0, b))


def carica_rimbalzo(indietro: float = 0.06, oltre: float = 0.08, quota: float = 0.22):
    """Arretra di `indietro` (frazione della corsa) nel primo `quota` del tempo, poi parte, supera l'arrivo di
    `oltre` e ci torna (rimbalzo di tools.anim.pattern, che non esce dall'area)."""
    r = rimbalzo(oltre)

    def f(t: float) -> float:
        if t < quota:
            return -indietro * np.sin(np.pi / 2 * t / quota)
        s = (t - quota) / (1 - quota)
        return -indietro + (1 + indietro) * r(s)
    return f


def a_tappe(mob, stati: list, confini: list[float], curve: list | None = None) -> UpdateFromAlphaFunc:
    """`mob` passa per gli `stati` (copie con la stessa struttura), raggiunti alle frazioni `confini` della play:
    una sola animazione per oggetto anche quando il percorso ha più tratti (due `.animate` non si sommano).
    Aiuto locale (da contenuti/archivio/generativa-probabile/animazioni.py)."""
    curve = curve or [smooth] * (len(stati) - 1)
    pezzi = [m.family_members_with_points() for m in (mob, *stati)]

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


def glifi(blocco):
    """I glifi di un testo di una riga (mai il puntello: cambiarne il colore fa scattare il controllo `colore`)."""
    return blocco.righe[0].glifi


def punta_su(indice: Indice, p: np.ndarray) -> Indice:
    """Mette l'indice con la punta sul punto p (come Indice.vai_a, ma senza animazione)."""
    return indice.move_to(p - indice.scostamento + np.array([indice.width / 2, -indice.height / 2, 0]))


# --- i pezzi del quadro ------------------------------------------------------------------------------------

class BarraPos(VGroup):
    """Una barra del grafico: la pista vuota (100 %), il pieno e il numero accanto alla punta."""

    def __init__(self, y: float, valore: int, colore: str | None = None, **kw):
        super().__init__(**kw)
        self.y, self.valore = y, valore
        self.colore = colore or P.secondario
        self.pista = Rectangle(width=px(L_BAR), height=px(H_BAR), stroke_color=P.attenuato, stroke_width=tratto(2),
                               fill_opacity=0).move_to(punto(X_BAR + L_BAR / 2, y))
        self.pieno = Rectangle(width=px(L_BAR * valore / 100), height=px(H_BAR), stroke_width=0,
                               fill_color=self.colore, fill_opacity=1).move_to(punto(X_BAR + L_BAR * valore / 200, y))
        self.numero = testo(str(valore), "etichetta", colore=P.testo, peso=BOLD)
        self.numero.move_to(punto(self.punta_x + NUM_BUFF, y), aligned_edge=LEFT)
        self.add(self.pista, self.pieno, self.numero)

    @property
    def punta_x(self) -> float:
        return X_BAR + L_BAR * self.valore / 100

    def punta(self) -> np.ndarray:
        return punto(self.punta_x, self.y)

    def spenta(self) -> None:
        self.pieno.set_fill(P.attenuato, opacity=0.35)
        glifi(self.numero).set_color(P.attenuato)

    def attenua(self, rate_func=smooth) -> list:
        return [self.pieno.animate(rate_func=rate_func).set_fill(P.attenuato, opacity=0.35),
                glifi(self.numero).animate(rate_func=rate_func).set_color(P.attenuato)]

    def riaccendi(self, rate_func=smooth, numero: bool = True) -> list:
        a = [self.pieno.animate(rate_func=rate_func).set_fill(self.colore, opacity=1)]
        if numero:
            a.append(glifi(self.numero).animate(rate_func=rate_func).set_color(P.testo))
        return a


def carta_domanda() -> VGroup:
    box = RoundedRectangle(corner_radius=px(22), width=px(CARTA_W), height=px(CARTA_H), stroke_color=P.secondario,
                           stroke_width=tratto(3), fill_color=P.sfondo, fill_opacity=1)
    box.move_to(punto(CARTA_X + CARTA_W / 2, CARTA_Y + CARTA_H / 2))
    q = etichetta(testo("?", "messaggio", colore=P.testo, peso=BOLD))
    q.shift(box.get_center() - glifi(q).get_center())
    g = VGroup(box, q)
    g.set_z_index(3)   # le righe che cadono passano dietro
    return g


class Quadro:
    """Tutti gli oggetti del filo visivo, nelle loro posizioni. Gli stati di fine delle scene stanno qui, così la
    scena dopo il filmato riparte esattamente da dove era rimasta la scena animata prima."""

    def __init__(self):
        self.sag = Sagome(QUOTE, larghezza_px=W_COL, altezza_px=H_RIGA, passo_px=PASSO)
        self.righe = list(self.sag.righe)
        self.colonna = VGroup(*self.righe)
        self.chiave = self.righe[0]
        self.chiave.set_z_index(1)
        self.ordine = list(self.righe)          # slot → riga
        self.disponi()
        self.carta = carta_domanda()
        self.giuste = etichetta(testo(GIUSTE, "etichetta", colore=P.attenuato))
        self.giuste.move_to(punto(X_BAR + w_px(self.giuste) / 2, Y_GIUSTE + self.giuste.height * PX_PER_UNITA / 2))
        self.fonte = Didascalia(FONTE)
        self.fonte.move_to(punto(950 - w_px(self.fonte) / 2, 1352 - self.fonte.height * PX_PER_UNITA / 2))
        self.barre = [BarraPos(y_slot(k), v) for k, v in zip(SLOT_BARRE, VALORI)]
        self.barra0 = BarraPos(Y_BARRA_0, VALORE_0, colore=P.attenuato)
        self.zero = etichetta(testo(ZERO, "etichetta", colore=P.attenuato))
        self.zero.move_to(punto(X_COL + w_px(self.zero) / 2, CARTA_Y + CARTA_H + 12
                                + self.zero.height * PX_PER_UNITA / 2))
        x0 = self.barra0.punta_x
        self.linea = DashedLine(punto(x0, Y_BARRA_0 - H_BAR / 2), punto(x0, 640), dash_length=px(14),
                                dashed_ratio=0.55, stroke_color=P.testo, stroke_width=tratto(3))
        self.curva = VMobject(stroke_color=P.accento, stroke_width=tratto(6))
        self.curva.set_points_smoothly([b.punta() for b in self.barre])
        self.curva.set_z_index(2)

    # --- la colonna ---
    def posto(self, r, slot: int) -> np.ndarray:
        return punto(X_COL + w_px(r) / 2, y_slot(slot))

    def disponi(self) -> None:
        for k, r in enumerate(self.ordine):
            r.move_to(self.posto(r, k))

    def con_chiave_a(self, k: int) -> list:
        nuovo = [r for r in self.ordine if r is not self.chiave]
        nuovo.insert(k, self.chiave)
        return nuovo

    def sposta(self, k: int, a: float = 0.0, b: float = 1.0, curva=smooth, arco_px: float = 34,
               segue=None, curva_altre=smooth) -> list:
        """Animazioni: la riga accesa va allo slot k facendo un piccolo arco verso destra, le altre si scostano di
        un posto. `segue`: un oggetto che viaggia attaccato alla riga (l'indice)."""
        nuovo = self.con_chiave_a(k)
        anims = []
        for slot, r in enumerate(nuovo):
            if r is self.chiave:
                continue
            meta = self.posto(r, slot)
            if np.linalg.norm(r.get_center() - meta) > 1e-6:
                anims.append(r.animate(rate_func=fra(a, b, curva_altre)).move_to(meta))
        p0 = self.chiave.get_center().copy()
        p1 = self.posto(self.chiave, k)
        scarto = (segue.get_center() - self.chiave.get_center()) if segue is not None else None
        tempo = fra(a, b, linear)

        def f(m, t):
            u = curva(tempo(t))
            m.move_to(p0 + (p1 - p0) * u + RIGHT * px(arco_px) * np.sin(np.pi * min(1.0, max(0.0, u))))
            if segue is not None:
                segue.move_to(m.get_center() + scarto)

        anims.append(UpdateFromAlphaFunc(self.chiave, f, rate_func=linear))
        self.ordine = nuovo
        return anims

    # --- stati di fine ---
    def fine_3(self, sc: ScenaReel) -> None:
        """L'ultimo fotogramma della scena 3: riga accesa in fondo, tre barre piene con i numeri, la curva."""
        self.ordine = self.con_chiave_a(19)
        self.disponi()
        self.chiave.set_fill(P.accento, opacity=1)
        sc.add(self.colonna, self.carta, self.fonte, *[b.pista for b in self.barre], self.giuste)
        for b in self.barre:
            sc.add(b.pieno, b.numero)
        sc.add(self.curva)

    def fine_5(self, sc: ScenaReel) -> None:
        """L'ultimo fotogramma della scena 5: riga accesa al decimo posto, 76 e 63 attenuate, 54 piena, la barra
        grigia 56 con la linea tratteggiata; la curva non c'è più."""
        self.ordine = self.con_chiave_a(9)
        self.disponi()
        self.chiave.set_fill(P.accento, opacity=1)
        self.barre[0].spenta()
        self.barre[2].spenta()
        sc.add(self.colonna, self.carta, self.fonte, *[b.pista for b in self.barre], self.giuste)
        for b in self.barre:
            sc.add(b.pieno, b.numero)
        sc.add(self.barra0.pista, self.barra0.pieno, self.barra0.numero, self.zero, self.linea)


# --- scene ---------------------------------------------------------------------------------------------------

class Scena03(ScenaReel):
    """Il paragrafo con la risposta cambia posto nella colonna; le barre dicono quante risposte giuste, e la curva
    che ne unisce le punte è la U coricata."""

    def costruisci(self):
        testi = self.scena.get("testo") or [FONTE, GIUSTE]
        assert testi[0] == FONTE and testi[1] == GIUSTE, "TESTO: della scena 3 cambiato: aggiorna FONTE e GIUSTE"
        q = Quadro()
        self.add(q.colonna, q.carta)                       # fotogramma 0 già pieno (dopo il filmato)

        # beat 0 · «A Stanford danno all'IA venti paragrafi, e l'unico con la risposta lo spostano.»
        self.play(q.chiave.animate(rate_func=fra(0, 0.6)).set_fill(P.accento, opacity=1),
                  FadeIn(q.fonte, rate_func=fra(0.4, 1)), run_time=0.8)
        self.attendi_fino(1.3)
        self.play(*q.sposta(9), run_time=0.9)                # a metà
        self.attendi_fino(2.4)
        self.play(*q.sposta(19), run_time=0.9)               # in fondo
        self.attendi_fino(3.5)
        self.play(*q.sposta(0), run_time=1.1)                # e di nuovo in cima

        # beat 1 · «Tu dove dici che lo trova meglio?» — le piste vuote, poi il vuoto della scommessa
        self.beat(1)
        self.play(*[Create(b.pista) for b in q.barre], FadeIn(q.giuste, rate_func=fra(0.3, 1)), run_time=0.6)

        # beat 2 · «In cima uno dei modelli risponde giusto tre volte su quattro,»
        self.beat(2)
        b1, b10, b20 = q.barre
        self.play(GrowFromEdge(b1.pieno, LEFT, rate_func=fra(0, 0.75, ease_out_cubic)),
                  FadeIn(b1.numero, rate_func=fra(0.75, 1)), run_time=1.0)

        # beat 3 · «in mezzo poco più di una su due,»
        self.beat(3)
        self.play(*q.sposta(9, 0, 0.45), *b1.attenua(fra(0, 0.4)),
                  GrowFromEdge(b10.pieno, LEFT, rate_func=fra(0.45, 0.85, ease_out_cubic)),
                  FadeIn(b10.numero, rate_func=fra(0.85, 1)), run_time=1.2)

        # beat 4 · «e in fondo risale.» — GRANDE: la curva si disegna dalle punte, le barre si riaccendono al passaggio
        self.beat(4)
        self.play(*q.sposta(19, 0, 0.4),
                  GrowFromEdge(b20.pieno, LEFT, rate_func=fra(0.1, 0.5, ease_out_cubic)),
                  FadeIn(b20.numero, rate_func=fra(0.5, 0.62)),
                  Create(q.curva, rate_func=fra(0.28, 1.0, smooth)),
                  *b1.riaccendi(fra(0.28, 0.42)), run_time=1.15)


class Scena05(ScenaReel):
    """Senza nessun paragrafo lo stesso modello arriva a 56: più in là del 54 col paragrafo giusto in mezzo."""

    def costruisci(self):
        testi = self.scena.get("testo") or [ZERO]
        assert testi[0] == ZERO, "TESTO: della scena 5 cambiato: aggiorna ZERO"
        q = Quadro()
        q.fine_3(self)                                      # fotogramma 0 = ultimo della scena 3
        b1, b10, b20 = q.barre
        b0 = q.barra0

        # beat 0 · «E la cosa che mi ha colpito è che quello stesso modello, senza nessun paragrafo,»
        self.play(*b1.attenua(), *b10.attenua(), *b20.attenua(), FadeOut(q.curva), run_time=0.6)
        self.attendi_fino(2.1)
        # le venti righe cadono, dal fondo in su, e spariscono (dietro la carta)
        dur, passo = 0.35, 0.65 / (N_RIGHE - 1)
        cadute = []
        for i, r in enumerate(reversed(q.ordine)):
            cadute.append(r.animate(rate_func=fra(i * passo, i * passo + dur, rush_into))
                          .shift(DOWN * px(70)).set_fill(opacity=0))
        self.play(*cadute, run_time=1.0)
        self.play(Create(b0.pista, rate_func=fra(0, 0.3)),
                  GrowFromEdge(b0.pieno, LEFT, rate_func=fra(0.15, 0.75, ease_out_cubic)),
                  FadeIn(b0.numero, rate_func=fra(0.75, 1)), FadeIn(q.zero, rate_func=fra(0.5, 1)), run_time=0.8)
        self.play(Create(q.linea), run_time=0.5)            # dalla punta del 56 in su

        # beat 1 · «ci azzecca più spesso che col paragrafo giusto messo in mezzo.»
        self.beat(1)
        q.ordine = q.con_chiave_a(9)
        for k, r in enumerate(q.ordine):                     # invisibili: le rimetto sopra il loro posto
            r.move_to(q.posto(r, k) + UP * px(70))
        q.chiave.set_fill(P.accento, opacity=0)
        rientri = []
        dur, passo = 0.3, 0.45 / (N_RIGHE - 1)
        for i, r in enumerate(q.ordine):
            op = 1.0 if r is q.chiave else 0.45
            rientri.append(r.animate(rate_func=fra(i * passo, i * passo + dur, ease_out_cubic))
                           .shift(DOWN * px(70)).set_fill(opacity=op))
        self.play(*rientri, *b10.riaccendi(fra(0.5, 1)), run_time=0.8)
        # sosta a scala intera (condizione del revisore): 54 e 56 intere sulla stessa scala prima dello zoom
        self.wait(0.55)
        # GRANDE (contrasto di scala): zoom breve sulla punta del 54 e sulla linea del 56
        fuoco = Rectangle(width=px(40), height=px(40)).move_to(punto((b10.punta_x + b0.punta_x) / 2, b10.y))
        lontani = [d for d in q.linea.submobjects if abs(y_px(d.get_center()[1]) - b10.y) > 70]
        # testi e barre vicine escono mentre la camera si avvicina: a zoom pieno nessun testo tagliato ai bordi, e
        # niente che passi sotto il riquadro del presentatore o nella fascia delle caption
        altri = [glifi(m) for m in (b1.numero, b20.numero, b0.numero, q.zero, q.giuste, q.fonte.testo, q.carta[1])]
        self.play(self.zoom_su(fuoco, 5), *[d.animate.set_stroke(opacity=0) for d in lontani],
                  *[g.animate(rate_func=fra(0, 0.35)).set_fill(opacity=0) for g in altri],
                  *[b.pista.animate(rate_func=fra(0, 0.35)).set_stroke(opacity=0) for b in (b1, b20, b0)],
                  *[b.pieno.animate(rate_func=fra(0, 0.35)).set_fill(opacity=0) for b in (b1, b20, b0)],
                  run_time=0.55)
        lampo = Rectangle(width=px(16), height=px(H_BAR), stroke_width=0, fill_color=P.accento, fill_opacity=0)
        lampo.move_to(punto(b10.punta_x - 8, b10.y))
        self.add(lampo)
        self.play(lampo.animate(rate_func=there_and_back).set_fill(opacity=1), run_time=0.5)
        self.remove(lampo)
        self.wait(0.1)
        self.play(self.torna(), *[d.animate.set_stroke(opacity=1) for d in lontani],
                  *[g.animate(rate_func=fra(0.65, 1)).set_fill(opacity=1) for g in altri],
                  *[b.pista.animate(rate_func=fra(0.65, 1)).set_stroke(opacity=1) for b in (b1, b20, b0)],
                  *[b.pieno.animate(rate_func=fra(0.65, 1)).set_fill(opacity=op)
                    for b, op in ((b1, 0.35), (b20, 0.35), (b0, 1.0))], run_time=0.55)

        # beat 2 · «E il perché preciso non è ancora chiaro.» — la riga c'è, la barra non si muove
        self.beat(2)
        alone = RoundedRectangle(corner_radius=px(14), width=q.chiave.width + px(28), height=px(H_RIGA + 22),
                                 stroke_width=0, fill_color=P.accento, fill_opacity=0).move_to(q.chiave)
        alone.set_z_index(0)
        self.add(alone)
        self.play(alone.animate(rate_func=there_and_back).set_fill(opacity=0.35),
                  q.chiave.animate(rate_func=there_and_back).scale(1.15), run_time=0.7)
        self.remove(alone)


class Scena07(ScenaReel):
    """La mossa: il pezzo che conta in cima, la domanda in fondo; se non sai dov'è, un blocco alla volta; la spunta
    solo dopo che la lente l'ha ritrovato nel documento."""

    def costruisci(self):
        q = Quadro()
        q.fine_5(self)                                      # fotogramma 0 = ultimo della scena 5
        b1, b10, b20 = q.barre
        b0 = q.barra0

        # beat 0 · «Quindi il pezzo che conta prendilo e mettilo in ==cima==,»
        togli = [b.numero for b in q.barre] + [b0.pista, b0.pieno, b0.numero, q.zero, q.linea, q.giuste, q.fonte]
        indice = Indice()
        indice.set_z_index(5)
        punta_su(indice, q.chiave.get_right() + RIGHT * px(14))
        self.play(*[FadeOut(m, rate_func=fra(0, 0.6)) for m in togli], *b10.attenua(fra(0, 0.6)),
                  FadeIn(indice, shift=DOWN * px(30), rate_func=fra(0.35, 1)), run_time=0.7)
        self.play(indice.tocca(), run_time=0.24)
        # GRANDE (carica e rimbalzo): la riga arretra, vola in cima con l'indice, supera e si assesta
        self.play(*q.sposta(0, 0, 1, curva=carica_rimbalzo(), segue=indice, curva_altre=fra(0.2, 0.75)),
                  *b1.riaccendi(fra(0.75, 1), numero=False), run_time=1.2)

        # beat 1 · «e la domanda scrivila in fondo.»
        self.beat(1)
        punta = punto(CARTA_X + CARTA_W * 0.8, CARTA_Y + 18)
        meta = punta - indice.scostamento + np.array([indice.width / 2, -indice.height / 2, 0])
        self.play(indice.animate(rate_func=ease_out_cubic).move_to(meta), run_time=0.5)
        self.play(indice.tocca(), run_time=0.24)
        self.play(q.carta.animate(rate_func=there_and_back).scale(1.12),
                  *[FadeOut(m) for b in q.barre for m in (b.pista, b.pieno)], run_time=0.6)

        # beat 2 · «E se non sai dov'è, dagliene un pezzo alla volta.»
        self.beat(2)
        blocchi = [q.ordine[5 * b:5 * b + 5] for b in range(4)]

        def in_p(r, j: int, dx: float = 0.0):
            t = r.copy().scale(SCALA_BLOCCO)
            t.move_to(punto(X_COL + w_px(t) / 2 + dx, P_TOP + H_RIGA * SCALA_BLOCCO / 2 + j * PASSO * SCALA_BLOCCO))
            return t

        anims = [FadeOut(indice, rate_func=fra(0, 0.25))]
        for b, blocco in enumerate(blocchi):
            for j, r in enumerate(blocco):
                s0 = r.copy()
                s1 = r.copy().set_fill(P.attenuato, opacity=0.45) if r is q.chiave else r.copy()
                s2 = s1.copy().shift(UP * px((3 - b) * 22))
                if b == 0:
                    s3 = in_p(s2, j)
                    anims.append(a_tappe(r, [s0, s1, s2, s3], [0.0, 0.22, 0.6, 1.0],
                                         [smooth, smooth, ease_out_cubic]))
                else:
                    s3 = s2.copy().shift(RIGHT * px(1000))
                    anims.append(a_tappe(r, [s0, s1, s2, s3], [0.0, 0.2, 0.4, 0.54 + 0.02 * b],
                                         [smooth, smooth, rush_into]))
        self.play(*anims, run_time=1.3)
        q.chiave.set_z_index(0)
        # i blocchi dopo aspettano fuori tela, già grandi, sulla riga del blocco visibile
        for b in (1, 2):
            for j, r in enumerate(blocchi[b]):
                r.become(in_p(r, j, NASTRO))
        self.remove(*blocchi[3])
        self.attendi_fino(self.t + 0.15)
        # il nastro: esce il primo blocco, entra il secondo
        self.play(*[r.animate.shift(LEFT * px(NASTRO)) for r in blocchi[0] + blocchi[1]], run_time=0.85)
        self.remove(*blocchi[0])

        # beat 3 · «Poi chiedile la frase esatta da cui l'ha presa, e cercala nel documento.»
        self.beat(3)
        trovata = blocchi[2][RIGA_TROVATA]
        anims = [r.animate(rate_func=smooth).shift(LEFT * px(NASTRO)) for r in blocchi[1]]
        for r in blocchi[2]:
            if r is trovata:
                s1 = r.copy().shift(LEFT * px(NASTRO))
                s2 = s1.copy().set_fill(P.accento, opacity=1)
                anims.append(a_tappe(r, [r.copy(), s1, s2], [0.0, 0.78, 1.0]))
            else:
                anims.append(r.animate(rate_func=fra(0, 0.78)).shift(LEFT * px(NASTRO)))
        self.play(*anims, run_time=1.1)
        self.remove(*blocchi[1])
        # la lente scende sul blocco, scorre le righe e si ferma sulla riga accesa
        lente = Lente(raggio_px=62)
        c = lente.cerchio
        manico = Line(c.get_center() + np.array([1, -1, 0]) * c.width / 2 / np.sqrt(2),
                      c.get_center() + np.array([1, -1, 0]) * (c.width / 2 / np.sqrt(2) + px(46)),
                      stroke_color=P.testo, stroke_width=tratto(12))
        vetro = VGroup(lente, manico).set_z_index(4)
        y_prima = y_px(blocchi[2][0].get_center()[1])
        vetro.shift(punto(X_LENTE, y_prima) - c.get_center())
        self.play(FadeIn(vetro, shift=DOWN * px(60)), run_time=0.45)
        self.play(vetro.animate(rate_func=ease_out_sine).shift(trovata.get_center()[1] * UP
                                                                 - c.get_center()[1] * UP), run_time=1.1)
        self.wait(0.2)
        spunta = Spunta(altezza_px=96)
        spunta.move_to(punto(X_COL + w_px(trovata) + 90, y_px(trovata.get_center()[1])))
        self.play(spunta.entra(), run_time=0.6)
