"""Componenti riusabili per le scene del reel (solo Text/MarkupText via Pango; colori e font dal config).

Convenzione: ogni componente è un VGroup posizionabile con i metodi Manim (next_to, move_to, align_to) e ha metodi
che ritornano Animation (entra, cresci, scegli, …) da passare a `self.play`. Le misure sono in px tramite `px()`.
"""
from __future__ import annotations

import html
import re

import numpy as np
from manim import (BOLD, DOWN, LEFT, ORIGIN, RIGHT, UP, AnimationGroup, Arrow, Create, FadeIn, FadeOut,
                   GrowFromEdge, Indicate, LaggedStart, Line, MarkupText, Mobject, Rectangle, RoundedRectangle,
                   SurroundingRectangle, Text, Transform, VGroup, VMobject)

from .config import Config, carica
from .misure import CORPO_PX, font_size_per, px

_RE_EV = re.compile(r"==(.+?)==")
_RE_B = re.compile(r"\*\*(.+?)\*\*")
_RE_I = re.compile(r"\*(.+?)\*")


def _cfg() -> Config:
    return carica()


def markup(testo: str, accento: str | None = None) -> str:
    """Da inline della sceneggiatura (==evidenzia==, **grassetto**, *corsivo*) a Pango markup."""
    acc = accento or _cfg().palette.accento
    s = html.escape(testo, quote=False)
    s = _RE_EV.sub(lambda m: f'<span foreground="{acc}">{m.group(1)}</span>', s)
    s = _RE_B.sub(r"<b>\1</b>", s)
    s = _RE_I.sub(r"<i>\1</i>", s)
    return s


def piano(testo: str) -> str:
    return _RE_I.sub(r"\1", _RE_B.sub(r"\1", _RE_EV.sub(r"\1", testo)))


def _font_kw(ruolo: str, peso: str | None = None, mono: bool = False) -> dict:
    cfg = _cfg()
    return {"font": cfg.font.mono if mono else cfg.font.famiglia, "font_size": font_size_per(CORPO_PX[ruolo]),
            "weight": peso or "NORMAL"}


def testo(s: str, ruolo: str = "caption", colore: str | None = None, peso: str | None = None, mono: bool = False,
          larghezza_px: float | None = None, allinea: str = "left", line_spacing: float = 0.9) -> MarkupText:
    """Testo con inline della sceneggiatura, a capo automatico entro larghezza_px (misurato con Pango)."""
    cfg = _cfg()
    kw = _font_kw(ruolo, peso, mono)
    colore = colore or cfg.palette.testo
    righe = [s]
    if larghezza_px:
        righe = avvolgi(s, larghezza_px, kw)
    m = MarkupText("\n".join(markup(r) for r in righe), color=colore, line_spacing=line_spacing, justify=False,
                   disable_ligatures=True, **kw)
    if allinea == "center":
        pass  # MarkupText centra le righe di default
    return m


def avvolgi(s: str, larghezza_px: float, kw: dict) -> list[str]:
    """A capo greedy per parole, misurando ogni riga con Pango (testo piano, senza markup)."""
    parole = s.split()
    righe: list[str] = []
    corrente: list[str] = []
    for p in parole:
        tentativo = " ".join(corrente + [p])
        w = Text(piano(tentativo), **kw).width * _cfg().px_per_unita
        if corrente and w > larghezza_px:
            righe.append(" ".join(corrente))
            corrente = [p]
        else:
            corrente.append(p)
    if corrente:
        righe.append(" ".join(corrente))
    return righe or [s]


# --- componenti ------------------------------------------------------------------------------------------

class Titolo(VGroup):
    """Titolo grande (hook): maiuscolo, grassetto, ==parola== in accento; a capo entro larghezza_px."""

    def __init__(self, s: str, larghezza_px: float = 900, ruolo: str = "titolo", **kw):
        super().__init__(**kw)
        self.testo = testo(s.upper() if ruolo == "titolo" else s, ruolo, peso=BOLD, larghezza_px=larghezza_px)
        self.add(self.testo)

    def entra(self, **kw):
        return FadeIn(self, shift=UP * 0.3, **kw)

    def per_righe(self, lag: float = 0.25):
        """Le righe compaiono una alla volta (per i titoli su più righe)."""
        return LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in self.testo.submobjects] if len(self.testo.submobjects) > 1 else [FadeIn(self)], lag_ratio=lag)


class Caption(VGroup):
    """Didascalia in basso nell'area contenuto (attenuata). `area` è un Area di base.py."""

    def __init__(self, s: str, area=None, larghezza_px: float = 880, colore: str | None = None, **kw):
        super().__init__(**kw)
        self.testo = testo(s, "caption", colore=colore or _cfg().palette.attenuato, larghezza_px=larghezza_px)
        self.add(self.testo)
        if area is not None:
            self.move_to([area.centro[0], area.y0 + self.height / 2 + px(20), 0])

    def entra(self, **kw):
        return FadeIn(self, **kw)


class Etichetta(VGroup):
    """Pillola con una parola chiave (TESTO:)."""

    def __init__(self, s: str, colore: str | None = None, pieno: bool = True, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        col = colore or cfg.palette.accento
        t = testo(s, "etichetta", colore=cfg.palette.sfondo if pieno else col, peso=BOLD)
        box = RoundedRectangle(corner_radius=px(28), width=t.width + px(56), height=t.height + px(36),
                               stroke_color=col, stroke_width=3, fill_color=col, fill_opacity=1 if pieno else 0)
        self.add(box, t.move_to(box))

    def entra(self, **kw):
        return FadeIn(self, scale=0.85, **kw)


class Barrato(VGroup):
    """Parola con una riga sopra (per «non vuol dire X»)."""

    def __init__(self, parola: Mobject, colore: str | None = None, **kw):
        super().__init__(**kw)
        col = colore or _cfg().palette.accento
        self.riga = Line(parola.get_left(), parola.get_right(), stroke_color=col, stroke_width=px(10)).move_to(parola.get_center())
        self.add(self.riga)

    def entra(self, **kw):
        return Create(self.riga, **kw)


class Freccia(VGroup):
    def __init__(self, da, a, s: str | None = None, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        col = colore or cfg.palette.attenuato
        self.freccia = Arrow(da, a, buff=px(12), stroke_width=px(6), color=col, max_tip_length_to_length_ratio=0.15)
        self.add(self.freccia)
        if s:
            self.etichetta = testo(s, "etichetta", colore=col).next_to(self.freccia, UP, buff=px(8))
            self.add(self.etichetta)

    def entra(self, **kw):
        anims = [GrowFromEdge(self.freccia, self.freccia.get_start(), **kw)]
        if len(self) > 1:
            anims.append(FadeIn(self[1]))
        return AnimationGroup(*anims, lag_ratio=0.5)


class Carta(VGroup):
    """Scheda con titolo e righe (per «contesto», «prompt», …)."""

    def __init__(self, titolo: str, righe: list[str] | None = None, larghezza_px: float = 880, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        col = colore or cfg.palette.secondario
        self.titolo = testo(titolo, "etichetta", colore=col, peso=BOLD)
        self.righe = VGroup(*[testo(r, "caption", larghezza_px=larghezza_px - px(80)) for r in (righe or [])])
        corpo = VGroup(self.titolo, *self.righe).arrange(DOWN, aligned_edge=LEFT, buff=px(20))
        self.box = RoundedRectangle(corner_radius=px(28), width=larghezza_px / cfg.px_per_unita,
                                    height=corpo.height + px(64), stroke_color=col, stroke_width=3, fill_color=cfg.palette.sfondo, fill_opacity=1)
        corpo.move_to(self.box).align_to(self.box, LEFT).shift(RIGHT * px(40))
        self.add(self.box, corpo)

    def aggiungi_riga(self, s: str, larghezza_px: float = 880):
        """Animazione: una nuova riga entra in fondo alla carta (la carta cresce)."""
        r = testo(s, "caption", larghezza_px=larghezza_px - px(80))
        ultimo = self.righe[-1] if len(self.righe) else self.titolo
        r.next_to(ultimo, DOWN, aligned_edge=LEFT, buff=px(20))
        self.righe.add(r)
        nuovo = self.box.copy().stretch_to_fit_height(self.box.height + r.height + px(20)).align_to(self.box, UP)
        return AnimationGroup(Transform(self.box, nuovo), FadeIn(r, shift=UP * 0.15), lag_ratio=0.3)

    def entra(self, **kw):
        return FadeIn(self, shift=UP * 0.2, **kw)


class Barra(VGroup):
    """Etichetta + barra orizzontale proporzionale (frazione 0-1)."""

    def __init__(self, s: str, frazione: float, larghezza_px: float = 600, colore: str | None = None, altezza_px: float = 26, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.colore = colore or cfg.palette.secondario
        self.frazione = max(0.02, min(1.0, frazione))
        self.larghezza_px = larghezza_px
        self.etichetta = testo(s, "token", colore=cfg.palette.testo)
        self.pista = Rectangle(width=px(larghezza_px), height=px(altezza_px), stroke_width=0, fill_color=cfg.palette.attenuato, fill_opacity=0.25)
        self.riempimento = Rectangle(width=px(larghezza_px * self.frazione), height=px(altezza_px), stroke_width=0,
                                     fill_color=self.colore, fill_opacity=1).align_to(self.pista, LEFT)
        pista = VGroup(self.pista, self.riempimento)
        self.add(VGroup(self.etichetta, pista).arrange(DOWN, aligned_edge=LEFT, buff=px(10)))

    def cresci(self, **kw):
        return AnimationGroup(FadeIn(self.etichetta), FadeIn(self.pista), GrowFromEdge(self.riempimento, LEFT), lag_ratio=0.2, **kw)

    def imposta(self, frazione: float):
        """Animazione: la barra cambia lunghezza."""
        nuovo = Rectangle(width=px(self.larghezza_px * max(0.02, min(1.0, frazione))), height=self.riempimento.height, stroke_width=0,
                          fill_color=self.colore, fill_opacity=1).align_to(self.pista, LEFT).align_to(self.pista, UP)
        self.frazione = frazione
        return Transform(self.riempimento, nuovo)


class Classifica(VGroup):
    """Colonna di candidati con barre (es. «prossima parola»), il primo evidenziato con scegli()."""

    def __init__(self, voci: list[tuple[str, float]], larghezza_px: float = 600, esempio: bool = True, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.barre = VGroup(*[Barra(s, f, larghezza_px, colore=cfg.palette.secondario) for s, f in voci])
        self.barre.arrange(DOWN, aligned_edge=LEFT, buff=px(34))
        self.add(self.barre)
        if esempio:
            self.nota = testo("esempio: numeri inventati", "piede", colore=cfg.palette.attenuato)
            self.nota.next_to(self.barre, DOWN, aligned_edge=LEFT, buff=px(20))
            self.add(self.nota)

    def entra(self, lag: float = 0.35, **kw):
        anims = [b.cresci() for b in self.barre]
        if len(self) > 1:
            anims.append(FadeIn(self[1]))
        return LaggedStart(*anims, lag_ratio=lag, **kw)

    def scegli(self, i: int, **kw):
        """La voce i diventa color accento e pulsa; le altre sbiadiscono."""
        cfg = _cfg()
        anims = []
        for k, b in enumerate(self.barre):
            if k == i:
                anims.append(b.riempimento.animate.set_fill(cfg.palette.accento))
                anims.append(b.etichetta.animate.set_color(cfg.palette.accento))
            else:
                anims.append(b.animate.set_opacity(0.3))
        return AnimationGroup(*anims, **kw)

    def token(self, i: int) -> "Token":
        return Token(piano(self.barre[i].etichetta.original_text if hasattr(self.barre[i].etichetta, "original_text") else "")).move_to(self.barre[i].etichetta)

    def riordina(self, voci: list[tuple[str, float]], **kw):
        """Animazione: nuove voci al posto delle vecchie (stessa posizione)."""
        nuova = Classifica(voci, self.barre[0].larghezza_px, esempio=len(self) > 1).move_to(self).align_to(self, LEFT).align_to(self, UP)
        return Transform(self, nuova, **kw)


class Token(VGroup):
    """Cartellino con una parola."""

    def __init__(self, parola: str, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        col = colore or cfg.palette.attenuato
        self.parola = parola
        t = testo(parola, "token")
        self.box = RoundedRectangle(corner_radius=px(16), width=t.width + px(44), height=t.height + px(36),
                                    stroke_color=col, stroke_width=3, fill_color=cfg.palette.sfondo, fill_opacity=1)
        self.add(self.box, t.move_to(self.box))

    def entra(self, **kw):
        return FadeIn(self, shift=UP * 0.25, **kw)

    def evidenzia(self, **kw):
        return self.box.animate.set_stroke(_cfg().palette.accento, width=5)


class Frase(VGroup):
    """Riga di cartellini che va a capo entro larghezza_px; aggiungi() anima l'ingresso di un token in coda."""

    def __init__(self, parole: list[str], larghezza_px: float = 900, **kw):
        super().__init__(**kw)
        self.larghezza_px = larghezza_px
        self.token = VGroup()
        for p in parole:
            self.token.add(Token(p))
        self._disponi()
        self.add(self.token)

    def _disponi(self):
        x = 0.0
        y = 0.0
        gap = px(16)
        riga_h = 0.0
        pos = []
        for t in self.token:
            if x > 0 and x + t.width > px(self.larghezza_px):
                x, y = 0.0, y - riga_h - gap
            pos.append((x + t.width / 2, y - t.height / 2))
            x += t.width + gap
            riga_h = max(riga_h, t.height)
        for t, (cx, cy) in zip(self.token, pos):
            t.move_to(np.array([cx, cy, 0.0]))
        # ancora in alto a sinistra: la frase cresce verso il basso
        if len(self.token):
            self.token.shift(-self.token.get_corner(UP + LEFT))

    def aggiungi(self, parola: str | Token, da=None):
        """Animazione: il token entra in coda (da un punto `da` o con fade)."""
        origine = self.token.get_corner(UP + LEFT) if len(self.token) else ORIGIN
        t = parola if isinstance(parola, Token) else Token(parola)
        self.token.add(t)
        self._disponi()
        self.token.shift(origine - self.token.get_corner(UP + LEFT))
        if da is not None:
            dest = t.get_center().copy()
            t.move_to(da)
            return t.animate.move_to(dest)
        return FadeIn(t, shift=UP * 0.2)

    def entra_una_alla_volta(self, lag: float = 0.3, **kw):
        return LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in self.token], lag_ratio=lag, **kw)


class Lista(VGroup):
    """Elenco con trattino colorato; voci che entrano una alla volta."""

    def __init__(self, voci: list[str], larghezza_px: float = 880, ruolo: str = "token", **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.voci = VGroup()
        for k, v in enumerate(voci):
            col = cfg.palette.secondario if k % 2 == 0 else cfg.palette.accento
            tratto = Rectangle(width=px(36), height=px(6), stroke_width=0, fill_color=col, fill_opacity=1)
            t = testo(v, ruolo, larghezza_px=larghezza_px - px(70))
            riga = VGroup(tratto, t).arrange(RIGHT, buff=px(24), aligned_edge=UP)
            tratto.shift(DOWN * (t.height * 0.5 - px(3)))
            self.voci.add(riga)
        self.voci.arrange(DOWN, aligned_edge=LEFT, buff=px(30))
        self.add(self.voci)

    def entra_una_alla_volta(self, lag: float = 0.4, **kw):
        return LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in self.voci], lag_ratio=lag, **kw)


class Contatore(VGroup):
    """Numero grande con etichetta; `a(n)` anima il cambio."""

    def __init__(self, valore: int | str, etichetta: str | None = None, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.colore = colore or cfg.palette.accento
        self.numero = testo(str(valore), "messaggio", colore=self.colore, peso=BOLD, mono=True)
        self.add(self.numero)
        if etichetta:
            self.etich = testo(etichetta, "etichetta", colore=cfg.palette.attenuato).next_to(self.numero, DOWN, buff=px(8))
            self.add(self.etich)

    def a(self, valore: int | str, **kw):
        nuovo = testo(str(valore), "messaggio", colore=self.colore, peso=BOLD, mono=True).move_to(self.numero)
        return Transform(self.numero, nuovo, **kw)

    def entra(self, **kw):
        return FadeIn(self, scale=0.8, **kw)


def Evidenzia(mob: Mobject, colore: str | None = None, buff: float = 0.12) -> SurroundingRectangle:
    return SurroundingRectangle(mob, color=colore or _cfg().palette.accento, buff=buff, corner_radius=px(12), stroke_width=px(5))


class CorniceSchermo(VGroup):
    """Bordo arrotondato dell'area schermo (il b-roll ci viene messo sotto dal compositing)."""

    def __init__(self, area, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        r = int(cfg.dati["schermo"].get("raggio_px", 36))
        self.box = RoundedRectangle(corner_radius=px(r), width=area.larghezza, height=area.altezza,
                                    stroke_color=colore or cfg.palette.attenuato, stroke_width=4, fill_opacity=0).move_to(area.centro)
        self.add(self.box)

    def entra(self, **kw):
        return Create(self.box, **kw)


class Piede(VGroup):
    """Handle del canale in basso a sinistra, se configurato."""

    def __init__(self, area, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        h = str(cfg.canale.handle or cfg.canale.nome or "")
        if h:
            t = testo(h, "piede", colore=cfg.palette.attenuato)
            t.move_to([area.x0 + t.width / 2, area.y0 - px(50), 0])
            self.add(t)


class Messaggio(VGroup):
    """Messaggio di chiusura: maiuscolo, grassetto, con ==enfasi==; più CTA a pillola."""

    def __init__(self, s: str, cta: str | None = None, larghezza_px: float = 900, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.testo = testo(s.upper(), "messaggio", peso=BOLD, larghezza_px=larghezza_px)
        self.add(self.testo)
        if cta:
            self.cta = Etichetta(cta, colore=cfg.palette.accento)
            if self.cta.width > px(larghezza_px):
                self.cta.scale_to_fit_width(px(larghezza_px))
            self.cta.next_to(self.testo, DOWN, aligned_edge=LEFT, buff=px(44))
            self.add(self.cta)

    def entra(self, **kw):
        anims = [FadeIn(self.testo, shift=UP * 0.2)]
        if len(self) > 1:
            anims.append(FadeIn(self[1], scale=0.85))
        return LaggedStart(*anims, lag_ratio=0.6, **kw)


__all__ = ["testo", "markup", "piano", "avvolgi", "Titolo", "Caption", "Etichetta", "Barrato", "Freccia", "Carta", "Barra",
           "Classifica", "Token", "Frase", "Lista", "Contatore", "Evidenzia", "CorniceSchermo", "Piede", "Messaggio",
           "FadeIn", "FadeOut", "Indicate", "LaggedStart", "AnimationGroup", "Transform", "Create"]
