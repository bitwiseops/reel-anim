"""Componenti per diagrammi esplicativi: passi in colonna, cicli, confronti, corrispondenze, graffe, tabelle.

Stesse convenzioni di componenti.py: VGroup posizionabili, metodi che ritornano animazioni, misure con px(), spessori
con tratto(), testo con testo(). `group=self` solo nelle animazioni di un componente già tutto in scena: per far
entrare una parte sola di un componente (Flusso.entra_passo, Confronto.mostra_prima) il gruppo non si passa, sennò
Manim aggiunge in scena anche le parti non ancora entrate.
"""
from __future__ import annotations

import math

from manim import (BOLD, DOWN, LEFT, ORIGIN, PI, RIGHT, TAU, UP, AnimationGroup, Arc, Brace, Create, DashedLine, Dot,
                   FadeIn, GrowFromCenter, LaggedStart, Line, MoveAlongPath, RoundedRectangle, VectorizedPoint, VGroup)

from .componenti import Barrato, Carta, Etichetta, Evidenzia, Freccia, Token, _cfg, testo
from .misure import px, tratto


class Nodo(VGroup):
    """Un passo: riquadro con testo centrato. accendi() = passo attivo (accento), spegni() = passo fatto (attenuato)."""

    def __init__(self, s: str, larghezza_px: float = 760, **kw):
        super().__init__(**kw)
        p = _cfg().palette
        self.testo = testo(s, "token", larghezza_px=larghezza_px - 80, allinea="center")
        self.box = RoundedRectangle(corner_radius=px(24), width=px(larghezza_px), height=self.testo.height + px(56),
                                    stroke_color=p.attenuato, stroke_width=tratto(3), fill_color=p.sfondo, fill_opacity=1)
        self.add(self.box, self.testo.move_to(self.box))

    def entra(self, **kw):
        return FadeIn(self, shift=UP * 0.2, **kw)

    def accendi(self, **kw):
        p = _cfg().palette
        return AnimationGroup(self.box.animate.set_stroke(p.accento, width=tratto(5)).set_fill(p.accento, opacity=0.14),
                              self.testo.animate.set_color(p.testo), group=self, **kw)

    def spegni(self, **kw):
        p = _cfg().palette
        return AnimationGroup(self.box.animate.set_stroke(p.attenuato, width=tratto(3)).set_fill(p.sfondo, opacity=1),
                              self.testo.animate.set_color(p.attenuato), group=self, **kw)


class Flusso(VGroup):
    """Passi in colonna uniti da frecce. Tipico: un passo per beat (entra_passo), il passo attivo in accento (attiva)."""

    def __init__(self, passi: list[str], larghezza_px: float = 760, buff_px: float = 84, **kw):
        super().__init__(**kw)
        self.nodi = VGroup(*[Nodo(s, larghezza_px) for s in passi]).arrange(DOWN, buff=px(buff_px))
        self.frecce = VGroup(*[Freccia(a.get_bottom(), b.get_top()) for a, b in zip(self.nodi[:-1], self.nodi[1:])])
        self.add(self.frecce, self.nodi)
        self.attivo: int | None = None

    def entra_passo(self, i: int, **kw):
        """Entra il passo i (con la freccia che ci arriva)."""
        anims = ([self.frecce[i - 1].entra()] if i > 0 else []) + [self.nodi[i].entra()]
        return AnimationGroup(*anims, lag_ratio=0.5, **kw)

    def entra(self, lag: float = 0.3, **kw):
        """Tutti i passi, uno dopo l'altro, in una sola animazione."""
        return LaggedStart(*[self.entra_passo(i) for i in range(len(self.nodi))], lag_ratio=lag, **kw)

    def attiva(self, i: int, **kw):
        """Il passo i si accende; quello acceso prima si spegne."""
        anims = [self.nodi[i].accendi()]
        if self.attivo is not None and self.attivo != i:
            anims.append(self.nodi[self.attivo].spegni())
        self.attivo = i
        return AnimationGroup(*anims, **kw)


class Ciclo(VGroup):
    """Stati su un cerchio (il primo in alto, poi in senso orario) uniti da archi con la punta. Un punto accento
    viaggia da uno stato al successivo (vai) e lo stato raggiunto si accende (accendi)."""

    def __init__(self, stati: list[str], raggio_px: float = 300, **kw):
        super().__init__(**kw)
        p = _cfg().palette
        self.n = len(stati)
        self.raggio = px(raggio_px)
        self.angoli = [PI / 2 - TAU * k / self.n for k in range(self.n)]
        self.stati = VGroup(*[Etichetta(s, colore=p.attenuato, pieno=False) for s in stati])
        for e, a in zip(self.stati, self.angoli):
            e.move_to([self.raggio * math.cos(a), self.raggio * math.sin(a), 0])
        self._m = [self._margine(e, a) for e, a in zip(self.stati, self.angoli)]
        self.archi = VGroup()
        for k in range(self.n):
            j = (k + 1) % self.n
            arco = Arc(radius=self.raggio, start_angle=self.angoli[k] - self._m[k], angle=-(TAU / self.n - self._m[k] - self._m[j]),
                       arc_center=ORIGIN, stroke_color=p.attenuato, stroke_width=tratto(5))
            self.archi.add(arco.add_tip(tip_length=px(26), tip_width=px(26)))
        self._centro = VectorizedPoint(ORIGIN)
        self.corrente = 0
        self.punto = Dot(radius=px(14), color=p.accento).move_to(self._sul_cerchio(self.angoli[0] + self._m[0]))
        self.add(self._centro, self.archi, self.stati, self.punto)

    def _sul_cerchio(self, angolo: float):
        c = self._centro.get_center()
        return c + self.raggio * math.cos(angolo) * RIGHT + self.raggio * math.sin(angolo) * UP

    def _margine(self, e, a: float) -> float:
        """Angolo (rad) di cui l'arco si stacca dallo stato per non toccarlo."""
        cx, cy = float(e.get_center()[0]), float(e.get_center()[1])
        w, h = e.width / 2 + px(18), e.height / 2 + px(18)
        d = 0.0
        while d < PI / self.n:
            x, y = self.raggio * math.cos(a - d), self.raggio * math.sin(a - d)
            if abs(x - cx) > w or abs(y - cy) > h:
                return d
            d += 0.005
        return 0.8 * PI / self.n

    def entra(self, lag: float = 0.15, **kw):
        anims = [FadeIn(e, scale=0.85) for e in self.stati] + [Create(a) for a in self.archi] + [FadeIn(self.punto)]
        return LaggedStart(*anims, lag_ratio=lag, group=self, **kw)

    def vai(self, **kw):
        """Il punto va dallo stato corrente al successivo lungo il cerchio."""
        k = self.corrente
        j = (k + 1) % self.n
        percorso = Arc(radius=self.raggio, start_angle=self.angoli[k] + self._m[k], angle=-TAU / self.n + self._m[j] - self._m[k],
                       arc_center=self._centro.get_center())
        self.corrente = j
        return MoveAlongPath(self.punto, percorso, **kw)

    def accendi(self, k: int, **kw):
        """Lo stato k in accento pieno, gli altri spenti."""
        p = _cfg().palette
        anims = []
        for i, e in enumerate(self.stati):
            if i == k:
                anims += [e.box.animate.set_fill(p.accento, opacity=1).set_stroke(p.accento), e.testo.animate.set_color(p.sfondo)]
            else:
                anims += [e.box.animate.set_fill(p.sfondo, opacity=1).set_stroke(p.attenuato), e.testo.animate.set_color(p.attenuato)]
        return AnimationGroup(*anims, group=self, **kw)


class Confronto(VGroup):
    """Prima e dopo in colonna: la carta «prima» viene bocciata (barrata e attenuata), la freccia porta al «dopo».
    Tipico su tre beat: mostra_prima(), boccia(), mostra_dopo()."""

    def __init__(self, prima: str, dopo: str, titolo_prima: str = "prima", titolo_dopo: str = "dopo",
                 larghezza_px: float = 900, **kw):
        super().__init__(**kw)
        p = _cfg().palette
        self.prima = Carta(titolo_prima, [prima], larghezza_px, colore=p.attenuato)
        self.dopo = Carta(titolo_dopo, [dopo], larghezza_px, colore=p.accento)
        VGroup(self.prima, self.dopo).arrange(DOWN, buff=px(130))
        self.freccia = Freccia(self.prima.get_bottom(), self.dopo.get_top(), colore=p.accento)
        self.barre = VGroup()
        self.add(self.prima, self.freccia, self.dopo, self.barre)

    def mostra_prima(self, **kw):
        return self.prima.entra(**kw)

    def boccia(self, **kw):
        """Ogni riga della carta «prima» viene barrata e la carta si attenua."""
        p = _cfg().palette
        for blocco in self.prima.righe:
            for riga in blocco.righe:
                self.barre.add(Barrato(riga, colore=p.accento, spessore_px=6))
        return AnimationGroup(self.prima.animate.fade(0.5), *[b.entra() for b in self.barre], lag_ratio=0.15, **kw)

    def mostra_dopo(self, **kw):
        return AnimationGroup(self.freccia.entra(), self.dopo.entra(), lag_ratio=0.5, **kw)


class Corrispondenza(VGroup):
    """Due colonne di cartellini; collega(i, j) le unisce: linea piena se l'abbinamento è giusto, tratteggiata e
    attenuata se è sbagliato."""

    def __init__(self, sinistra: list[str], destra: list[str], distanza_px: float = 240, **kw):
        super().__init__(**kw)
        self.sinistra = VGroup(*[Token(s) for s in sinistra]).arrange(DOWN, buff=px(36), aligned_edge=RIGHT)
        self.destra = VGroup(*[Token(s) for s in destra]).arrange(DOWN, buff=px(36), aligned_edge=LEFT)
        self.destra.next_to(self.sinistra, RIGHT, buff=px(distanza_px)).align_to(self.sinistra, UP)
        self.linee = VGroup()
        self.add(self.sinistra, self.destra, self.linee)

    def entra(self, lag: float = 0.12, **kw):
        return LaggedStart(*[t.entra() for t in [*self.sinistra, *self.destra]], lag_ratio=lag, group=self, **kw)

    def collega(self, i: int, j: int, giusto: bool = True, **kw):
        p = _cfg().palette
        a = self.sinistra[i].get_right() + RIGHT * px(10)
        b = self.destra[j].get_left() + LEFT * px(10)
        if giusto:
            linea = Line(a, b, stroke_color=p.terziario, stroke_width=tratto(5))
        else:
            linea = DashedLine(a, b, dash_length=px(18), stroke_color=p.attenuato, stroke_width=tratto(4))
        self.linee.add(linea)
        return Create(linea, **kw)


class Graffa(VGroup):
    """Graffa accanto a un gruppo con un'etichetta sulla punta (Brace + testo: niente LaTeX di Brace.get_text)."""

    def __init__(self, mob, s: str, direzione=RIGHT, colore: str | None = None, **kw):
        super().__init__(**kw)
        col = colore or _cfg().palette.attenuato
        self.graffa = Brace(mob, direction=direzione, buff=px(16), color=col)
        self.etichetta = testo(s, "etichetta", colore=col)
        self.graffa.put_at_tip(self.etichetta, buff=px(16))
        self.add(self.graffa, self.etichetta)

    def entra(self, **kw):
        return AnimationGroup(GrowFromCenter(self.graffa), FadeIn(self.etichetta), lag_ratio=0.4, group=self, **kw)


class Tabella(VGroup):
    """Tabella semplice senza LaTeX: intestazione in grassetto attenuato, righe di testo, linea sotto l'intestazione.
    Celle vuote come «–». cella(r, c), riga(r); evidenzia(r, c=None) incornicia una riga o una cella."""

    def __init__(self, righe: list[list[str]], intestazione: bool = True, larghezze_px: list[float] | None = None, **kw):
        super().__init__(**kw)
        p = _cfg().palette
        self.n_righe, self.n_col = len(righe), max(len(r) for r in righe)
        celle = []
        for i, r in enumerate(righe):
            testa = intestazione and i == 0
            for j in range(self.n_col):
                s = (r[j] if j < len(r) else "") or "–"
                celle.append(testo(s, "etichetta" if testa else "token", colore=p.attenuato if testa else p.testo,
                                   peso=BOLD if testa else None, larghezza_px=larghezze_px[j] if larghezze_px else None))
        self.celle = VGroup(*celle).arrange_in_grid(rows=self.n_righe, cols=self.n_col, buff=(px(56), px(30)),
                                                     col_alignments="l" * self.n_col)
        self.add(self.celle)
        self.linea = None
        if intestazione and self.n_righe > 1:
            y = (self.riga(0).get_bottom()[1] + self.riga(1).get_top()[1]) / 2
            self.linea = Line([self.celle.get_left()[0], y, 0], [self.celle.get_right()[0], y, 0], stroke_color=p.attenuato,
                              stroke_width=tratto(2))
            self.add(self.linea)

    def cella(self, r: int, c: int):
        return self.celle[r * self.n_col + c]

    def riga(self, r: int) -> VGroup:
        return VGroup(*self.celle[r * self.n_col:(r + 1) * self.n_col])

    def entra(self, lag: float = 0.25, **kw):
        parti = [FadeIn(self.riga(r), shift=UP * 0.1) for r in range(self.n_righe)]
        if self.linea is not None:
            parti.insert(1, Create(self.linea))
        return LaggedStart(*parti, lag_ratio=lag, group=self, **kw)

    def evidenzia(self, r: int, c: int | None = None, **kw):
        self.riquadro = Evidenzia(self.riga(r) if c is None else self.cella(r, c), buff=px(16))
        return Create(self.riquadro, **kw)


__all__ = ["Nodo", "Flusso", "Ciclo", "Confronto", "Corrispondenza", "Graffa", "Tabella"]
