"""Componenti riusabili per le scene del reel (solo Text/MarkupText via Pango; colori e font dal config).

Convenzione: ogni componente è un VGroup posizionabile con i metodi Manim (next_to, move_to, align_to, oppure
`area.metti`) e ha metodi che ritornano Animation (entra, cresci, scegli, …) da passare a `self.play`.
Misure in px con `px()`; spessori dei tratti con `tratto()` (non px: vedi misure.tratto).
Le animazioni composte usano `group=self`: senza, Manim aggiunge in cima alla scena un Group nuovo con i pezzi
animati e un riquadro pieno finisce sopra il testo (la carta «contesto» che perdeva le righe).

Testo: `testo()` ritorna un `Blocco` di `Riga`. Ogni riga ha un'altezza costante (dalla cima della H al fondo
della g, qualunque lettere contenga), così righe, cartellini e barre si allineano sulla linea di base.
`blocco.parola("x")` ritorna i glifi di una parola (per barrarla, evidenziarla, colorarla).
"""
from __future__ import annotations

import html
import re

import numpy as np
from manim import (BOLD, DOWN, LEFT, ORIGIN, RIGHT, UL, UP, AnimationGroup, Arrow, Create, FadeIn, FadeOut,
                   FadeTransform, GrowArrow, GrowFromEdge, Indicate, LaggedStart, Line, MarkupText, Mobject, Rectangle,
                   RoundedRectangle, SurroundingRectangle, Text, Transform, VGroup, VMobject)
from manim import Circle, Code, SVGMobject, Succession, ValueTracker, linear, rush_from
from manim.constants import CapStyleType, LineJointType

from .config import RADICE, Config, carica
from .misure import CORPO_PX, font_size_per, px, tratto

_RE_EV = re.compile(r"==(.+?)==")
_RE_B = re.compile(r"\*\*(.+?)\*\*")
_RE_I = re.compile(r"\*(.+?)\*")
_RE_SPAZI = re.compile(r"\s")
_RE_MARCATORI = re.compile(r"==|\*\*|\*")


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


def _bilancia(righe: list[str]) -> list[str]:
    """Un ==evidenzia== o **grassetto** che attraversa un a capo viene chiuso a fine riga e riaperto nella successiva."""
    out, aperti = [], ""
    for r in righe:
        r = aperti + r
        restano = [mk for mk in ("**", "==") if r.count(mk) % 2]
        aperti = "".join(restano)
        out.append(r + "".join(reversed(restano)))
    return out


def avvolgi(s: str, larghezza_px: float, kw: dict) -> list[str]:
    """A capo greedy per parole, misurando ogni riga con Pango (testo piano, senza markup)."""
    parole = s.split()
    righe: list[str] = []
    corrente: list[str] = []
    for p in parole:
        tentativo = " ".join(corrente + [p])
        w = Text(_RE_MARCATORI.sub("", tentativo), **kw).width * _cfg().px_per_unita  # anche == spezzati a metà
        if corrente and w > larghezza_px:
            righe.append(" ".join(corrente))
            corrente = [p]
        else:
            corrente.append(p)
    if corrente:
        righe.append(" ".join(corrente))
    return _bilancia(righe) if righe else [s]


class Riga(VGroup):
    """Una riga di testo: `glifi` (MarkupText, un glifo per carattere non spazio) + un puntello invisibile alto
    quanto «Hg», che dà a tutte le righe dello stesso corpo la stessa altezza e la stessa linea di base."""

    def __init__(self, s: str, colore: str, kw: dict, **kwargs):
        super().__init__(**kwargs)
        self.piano = piano(s)
        m = MarkupText("Hg" + markup(s), color=colore, disable_ligatures=True, **kw)
        self.allineata = len(m.submobjects) == len(_RE_SPAZI.sub("", self.piano)) + 2
        if self.allineata:
            h, g = m.submobjects[0], m.submobjects[1]
            alto, basso = h.get_top()[1], g.get_bottom()[1]
            m.remove(h, g)
            x = m.get_left()[0]
            self.puntello = Line([x, alto, 0], [x, basso, 0], stroke_width=0, stroke_opacity=0)
            self.glifi = m
            self.add(self.puntello, m)
        else:  # conteggio dei glifi inatteso: niente puntello (l'altezza segue le lettere)
            self.glifi = MarkupText(markup(s), color=colore, disable_ligatures=True, **kw)
            self.add(self.glifi)

    def parola(self, w: str) -> VGroup | None:
        i = self.piano.lower().find(w.lower())
        if i < 0:
            return None
        if not self.allineata:
            return VGroup(self.glifi)
        prima = len(_RE_SPAZI.sub("", self.piano[:i]))
        n = len(_RE_SPAZI.sub("", w))
        return VGroup(*self.glifi.submobjects[prima:prima + n])


class Blocco(VGroup):
    """Testo su una o più righe: a capo automatico entro larghezza_px, «\\n» forza l'a capo."""

    def __init__(self, s: str, ruolo: str = "caption", colore: str | None = None, peso: str | None = None,
                 mono: bool = False, larghezza_px: float | None = None, allinea: str = "left", interlinea: float = 0.3, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        fkw = _font_kw(ruolo, peso, mono)
        testi: list[str] = []
        for par in str(s).split("\n"):
            testi += avvolgi(par, larghezza_px, fkw) if larghezza_px else [par]
        self.righe = VGroup(*[Riga(t, colore or cfg.palette.testo, fkw) for t in testi if t.strip()])
        bordo = {"left": LEFT, "center": ORIGIN, "right": RIGHT}[allinea]
        self.righe.arrange(DOWN, buff=px(CORPO_PX[ruolo] * interlinea), aligned_edge=bordo)
        self.add(self.righe)

    @property
    def glifi(self) -> VGroup:
        return VGroup(*[r.glifi for r in self.righe])

    def parola(self, w: str) -> VGroup:
        for r in self.righe:
            g = r.parola(w)
            if g is not None:
                return g
        raise ValueError(f"«{w}» non compare nel testo «{' '.join(r.piano for r in self.righe)}»")


def testo(s: str, ruolo: str = "caption", colore: str | None = None, peso: str | None = None, mono: bool = False,
          larghezza_px: float | None = None, allinea: str = "left", interlinea: float = 0.3) -> Blocco:
    """Testo con inline della sceneggiatura nel corpo del ruolo (misure.CORPO_PX)."""
    return Blocco(s, ruolo, colore, peso, mono, larghezza_px, allinea, interlinea)


def _limita(f: float) -> float:
    return max(0.02, min(1.0, float(f)))


def etichetta(mob: Mobject) -> Mobject:
    """Marca un testo come **etichetta di una figura** (o come parola detta): il controllo `parole-leggibili` non lo
    conta fra le frasi da leggere. I reel si guardano muti e a spiegare è la caption: il testo a schermo sta sotto le
    due parole, salvo numeri, percentuali e appunto le etichette. Si usa sui componenti della libreria che sono già
    etichette per natura e, a mano, su una didascalia di onestà che deve restare per intero."""
    for m in mob.get_family() if hasattr(mob, "get_family") else [mob]:
        m._etichetta = True
    mob._etichetta = True
    return mob


_marca = etichetta   # alias interno: in Contatore il nome `etichetta` è già un parametro


# --- componenti ------------------------------------------------------------------------------------------

class Titolo(VGroup):
    """Titolo grande (hook): maiuscolo, grassetto, ==parola== in accento; a capo entro larghezza_px."""

    def __init__(self, s: str, larghezza_px: float = 900, ruolo: str = "titolo", colore: str | None = None,
                 allinea: str = "left", maiuscolo: bool = True, **kw):
        super().__init__(**kw)
        self.testo = testo(s.upper() if maiuscolo else s, ruolo, colore=colore, peso=BOLD, larghezza_px=larghezza_px,
                           allinea=allinea, interlinea=0.14)
        self.righe = self.testo.righe
        self.add(self.testo)
        _marca(self)

    def parola(self, w: str) -> VGroup:
        return self.testo.parola(w)

    def entra(self, **kw):
        return FadeIn(self, shift=UP * 0.3, **kw)

    def per_righe(self, lag: float = 0.25, **kw):
        """Le righe compaiono una alla volta."""
        return LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in self.righe], lag_ratio=lag, group=self, **kw)


class Didascalia(VGroup):
    """Didascalia attenuata; con `area` si mette in fondo all'area (un Area di base.py). È un'etichetta: non conta
    come frase da leggere (vedi `etichetta`), ma resta soggetta al buon senso — se serve una riga intera di
    spiegazione, quella riga la dice la voce."""

    def __init__(self, s: str, area=None, larghezza_px: float = 880, colore: str | None = None, **kw):
        super().__init__(**kw)
        self.testo = testo(s, "caption", colore=colore or _cfg().palette.attenuato, larghezza_px=larghezza_px)
        self.add(self.testo)
        if area is not None:
            self.move_to([area.centro[0], area.y0 + self.height / 2 + px(20), 0])
        _marca(self)

    def entra(self, **kw):
        return FadeIn(self, **kw)


class Etichetta(VGroup):
    """Pillola con una parola chiave (TESTO:). pieno=False: solo contorno."""

    def __init__(self, s: str, colore: str | None = None, pieno: bool = True, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        col = colore or cfg.palette.accento
        self.testo = testo(s, "etichetta", colore=cfg.palette.sfondo if pieno else col, peso=BOLD)
        h = self.testo.height + px(36)
        self.box = RoundedRectangle(corner_radius=h / 2, width=self.testo.width + px(64), height=h, stroke_color=col,
                                    stroke_width=tratto(3), fill_color=col if pieno else cfg.palette.sfondo, fill_opacity=1)
        self.add(self.box, self.testo.move_to(self.box))
        _marca(self)

    def entra(self, **kw):
        return FadeIn(self, scale=0.85, **kw)


class Barrato(VGroup):
    """Riga sopra una parola (per «non vuol dire X»): passa i glifi (`blocco.parola("x")`) o un Blocco."""

    def __init__(self, parola: Mobject, colore: str | None = None, spessore_px: float = 10, **kw):
        super().__init__(**kw)
        g = getattr(parola, "glifi", parola)
        y = g.get_center()[1]
        m = px(10)
        self.riga = Line([g.get_left()[0] - m, y, 0], [g.get_right()[0] + m, y, 0],
                         stroke_color=colore or _cfg().palette.accento, stroke_width=tratto(spessore_px))
        self.add(self.riga)

    def entra(self, **kw):
        return Create(self.riga, **kw)


class Freccia(VGroup):
    """Freccia da un punto (o mobject) a un altro, con etichetta opzionale sopra."""

    def __init__(self, da, a, s: str | None = None, colore: str | None = None, spessore_px: float = 6, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        col = colore or cfg.palette.attenuato
        self.freccia = Arrow(da, a, buff=px(12), stroke_width=tratto(spessore_px), color=col, tip_length=px(34),
                             max_tip_length_to_length_ratio=0.35, max_stroke_width_to_length_ratio=20)
        self.add(self.freccia)
        self.etichetta = None
        if s:
            self.etichetta = testo(s, "etichetta", colore=col).next_to(self.freccia, UP, buff=px(8))
            self.add(self.etichetta)

    def entra(self, **kw):
        anims = [GrowArrow(self.freccia)]
        if self.etichetta is not None:
            anims.append(FadeIn(self.etichetta))
        return AnimationGroup(*anims, lag_ratio=0.5, group=self, **kw)


class Carta(VGroup):
    """Scheda con titolo e righe (per «contesto», «prompt», «biglietto»…); cresce verso il basso con aggiungi_riga."""

    def __init__(self, titolo: str, righe: list[str] | None = None, larghezza_px: float = 900, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.colore = colore or cfg.palette.secondario
        self.larghezza_px = larghezza_px
        self.pad = px(40)
        self.titolo = _marca(testo(titolo, "etichetta", colore=self.colore, peso=BOLD))   # linguetta = etichetta
        self.righe = VGroup(*[self._riga(r) for r in (righe or [])])
        self.box = self._box(self._altezza(self.righe))
        self.add(self.box, self.titolo, self.righe)
        self.titolo.move_to(self.box.get_corner(UL) + np.array([self.pad, -self.pad, 0]), aligned_edge=UL)
        prec = self.titolo
        for r in self.righe:
            r.next_to(prec, DOWN, aligned_edge=LEFT, buff=px(24))
            prec = r

    def _riga(self, s: str) -> Blocco:
        return testo(s, "caption", larghezza_px=self.larghezza_px - 2 * 40)

    def _altezza(self, righe) -> float:
        return self.titolo.height + sum(r.height + px(24) for r in righe) + 2 * self.pad

    def _box(self, altezza: float) -> RoundedRectangle:
        cfg = _cfg()
        return RoundedRectangle(corner_radius=px(28), width=px(self.larghezza_px), height=altezza, stroke_color=self.colore,
                                stroke_width=tratto(3), fill_color=cfg.palette.sfondo, fill_opacity=1)

    def aggiungi_riga(self, s: str, **kw):
        """Animazione: una nuova riga entra in fondo alla carta (la carta cresce verso il basso)."""
        r = self._riga(s)
        r.next_to(self.righe[-1] if len(self.righe) else self.titolo, DOWN, aligned_edge=LEFT, buff=px(24))
        nuovo = self._box(self.box.height + r.height + px(24)).align_to(self.box, UP).align_to(self.box, LEFT)
        self.righe.add(r)
        return AnimationGroup(Transform(self.box, nuovo), FadeIn(r, shift=UP * 0.15), lag_ratio=0.3, group=self, **kw)

    def entra(self, **kw):
        return FadeIn(self, shift=UP * 0.2, **kw)


class Barra(VGroup):
    """Etichetta + barra orizzontale proporzionale (frazione 0-1)."""

    def __init__(self, s: str, frazione: float, larghezza_px: float = 600, colore: str | None = None, altezza_px: float = 26, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.s = s
        self.colore = colore or cfg.palette.secondario
        self.frazione = _limita(frazione)
        self.larghezza_px = larghezza_px
        self.etichetta = testo(s, "token")
        self.pista = Rectangle(width=px(larghezza_px), height=px(altezza_px), stroke_width=0, fill_color=cfg.palette.attenuato,
                               fill_opacity=0.25)
        self.pista.next_to(self.etichetta, DOWN, buff=px(12), aligned_edge=LEFT)
        self.riempimento = Rectangle(width=self._larghezza(self.frazione), height=px(altezza_px), stroke_width=0,
                                     fill_color=self.colore, fill_opacity=1).move_to(self.pista, aligned_edge=LEFT)
        self.add(self.etichetta, self.pista, self.riempimento)

    def _larghezza(self, f: float) -> float:
        return px(self.larghezza_px) * _limita(f)

    def cresci(self, **kw):
        return AnimationGroup(FadeIn(self.etichetta), FadeIn(self.pista), GrowFromEdge(self.riempimento, LEFT), lag_ratio=0.2, group=self, **kw)

    def bersaglio(self, frazione: float) -> "Barra":
        """Copia della barra con la nuova lunghezza (per Transform insieme a uno spostamento)."""
        b = self.copy()
        b.riempimento.stretch_to_fit_width(self._larghezza(frazione)).align_to(b.pista, LEFT)
        b.frazione = _limita(frazione)
        return b

    def imposta(self, frazione: float, **kw):
        """Animazione: la barra cambia lunghezza."""
        nuovo = self.riempimento.copy().stretch_to_fit_width(self._larghezza(frazione)).align_to(self.pista, LEFT)
        self.frazione = _limita(frazione)
        return Transform(self.riempimento, nuovo, **kw)


class Classifica(VGroup):
    """Colonna di candidati con barre (es. «prossima parola»). Le voci si danno già in ordine.
    aggiorna() cambia le lunghezze e riordina; scegli(i) accende la voce i (indice originale)."""

    def __init__(self, voci: list[tuple[str, float]], larghezza_px: float = 600, esempio: bool = True, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.barre = VGroup(*[Barra(s, f, larghezza_px, colore=cfg.palette.secondario) for s, f in voci])
        self.barre.arrange(DOWN, aligned_edge=LEFT, buff=px(34))
        self.ordine = list(range(len(voci)))
        self.add(self.barre)
        self.nota = None
        if esempio:
            self.nota = _marca(testo("esempio: numeri inventati", "piede", colore=cfg.palette.attenuato))
            self.nota.next_to(self.barre, DOWN, aligned_edge=LEFT, buff=px(28))
            self.add(self.nota)

    def entra(self, lag: float = 0.35, **kw):
        anims = [b.cresci() for b in self.barre]
        if self.nota is not None:
            anims.append(FadeIn(self.nota))
        return LaggedStart(*anims, lag_ratio=lag, group=self, **kw)

    def aggiorna(self, frazioni: list[float], riordina: bool = True, **kw):
        """Animazione: nuove lunghezze (una per voce, nell'ordine originale); con riordina le barre si scambiano di posto."""
        posti = [self.barre[k].get_corner(UL) for k in self.ordine]
        ordine = sorted(range(len(frazioni)), key=lambda k: -frazioni[k]) if riordina else list(self.ordine)
        anims = []
        for rango, k in enumerate(ordine):
            b = self.barre[k]
            t = b.bersaglio(frazioni[k]).move_to(posti[rango], aligned_edge=UL)
            anims.append(Transform(b, t))
            b.frazione = t.frazione
        self.ordine = ordine
        return AnimationGroup(*anims, group=self, **kw)

    def scegli(self, i: int, **kw):
        """La voce i diventa color accento; le altre sbiadiscono."""
        cfg = _cfg()
        anims = []
        for k, b in enumerate(self.barre):
            if k == i:
                anims.append(b.riempimento.animate.set_fill(cfg.palette.accento))
                anims.append(b.etichetta.animate.set_color(cfg.palette.accento))
            else:
                anims.append(b.animate.fade(0.65))
        return AnimationGroup(*anims, group=self, **kw)

    def token(self, i: int, colore: str | None = None) -> "Token":
        """Un cartellino con la voce i, sovrapposto alla sua etichetta (da far volare con Frase.aggiungi)."""
        return Token(self.barre[i].s, colore=colore).move_to(self.barre[i].etichetta, aligned_edge=LEFT)


class Token(VGroup):
    """Cartellino con una parola."""

    def __init__(self, parola: str, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        col = colore or cfg.palette.attenuato
        self.parola = parola
        self.testo = testo(parola, "token")
        self.box = RoundedRectangle(corner_radius=px(16), width=self.testo.width + px(44), height=self.testo.height + px(36),
                                    stroke_color=col, stroke_width=tratto(3), fill_color=cfg.palette.sfondo, fill_opacity=1)
        self.add(self.box, self.testo.move_to(self.box))

    def entra(self, **kw):
        return FadeIn(self, shift=UP * 0.25, **kw)

    def evidenzia(self, **kw):
        return self.box.animate(**kw).set_stroke(_cfg().palette.accento, width=tratto(5))


class Frase(VGroup):
    """Riga di cartellini che va a capo entro larghezza_px, ancorata in alto a sinistra in `ancora`.
    aggiungi() anima l'ingresso di un token in coda (da un punto o con dissolvenza)."""

    def __init__(self, parole: list[str] | tuple = (), larghezza_px: float = 900, ancora=None, **kw):
        super().__init__(**kw)
        self.larghezza_px = larghezza_px
        self.ancora = np.array(ancora if ancora is not None else ORIGIN, dtype=float)
        self.token = VGroup(*[Token(p) for p in parole])
        self.add(self.token)
        self._disponi()

    def posiziona(self, ancora) -> "Frase":
        self.ancora = np.array(ancora, dtype=float)
        self._disponi()
        return self

    def _disponi(self):
        if not len(self.token):
            return
        x = y = riga_h = 0.0
        gap = px(16)
        for t in self.token:
            if x > 0 and x + t.width > px(self.larghezza_px):
                x, y = 0.0, y - riga_h - gap
            t.move_to(np.array([x + t.width / 2, y - t.height / 2, 0.0]))
            x += t.width + gap
            riga_h = max(riga_h, t.height)
        self.token.shift(self.ancora - self.token.get_corner(UL))

    def aggiungi(self, parola: "str | Token", da=None, **kw):
        """Animazione: il token entra in coda (vola da `da`, un punto o un mobject, oppure dissolvenza)."""
        if len(self.token):
            self.ancora = self.token.get_corner(UL)
        t = parola if isinstance(parola, Token) else Token(parola)
        self.token.add(t)
        self._disponi()
        if da is not None:
            dest = t.get_center().copy()
            t.move_to(da)
            return t.animate(**kw).move_to(dest)
        return FadeIn(t, shift=UP * 0.2, **kw)

    def entra_una_alla_volta(self, lag: float = 0.3, **kw):
        return LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in self.token], lag_ratio=lag, group=self, **kw)


class Lista(VGroup):
    """Elenco con trattino colorato; voci che entrano una alla volta."""

    def __init__(self, voci: list[str], larghezza_px: float = 880, ruolo: str = "token", **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.voci = VGroup()
        for k, v in enumerate(voci):
            col = cfg.palette.secondario if k % 2 == 0 else cfg.palette.accento
            t = testo(v, ruolo, larghezza_px=larghezza_px - 70)
            trattino = Rectangle(width=px(36), height=px(8), stroke_width=0, fill_color=col, fill_opacity=1)
            trattino.next_to(t, LEFT, buff=px(24)).set_y(t.righe[0].glifi.get_center()[1])
            self.voci.add(VGroup(trattino, t))
        self.voci.arrange(DOWN, aligned_edge=LEFT, buff=px(30))
        self.add(self.voci)

    def entra_una_alla_volta(self, lag: float = 0.4, **kw):
        return LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in self.voci], lag_ratio=lag, group=self, **kw)


class Contatore(VGroup):
    """Numero grande con etichetta; `a(n)` anima il cambio."""

    def __init__(self, valore: int | str, etichetta: str | None = None, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.colore = colore or cfg.palette.accento
        self.numero = testo(str(valore), "messaggio", colore=self.colore, peso=BOLD, mono=True)
        self.add(self.numero)
        if etichetta:
            self.etich = testo(etichetta, "etichetta", colore=cfg.palette.attenuato).next_to(self.numero, DOWN, buff=px(12), aligned_edge=LEFT)
            self.add(self.etich)
        _marca(self)

    def a(self, valore: int | str, **kw):
        nuovo = testo(str(valore), "messaggio", colore=self.colore, peso=BOLD, mono=True).move_to(self.numero, aligned_edge=LEFT)
        return Transform(self.numero, nuovo, **kw)

    def entra(self, **kw):
        return FadeIn(self, scale=0.8, **kw)


def Evidenzia(mob: Mobject, colore: str | None = None, buff: float = 0.15, spessore_px: float = 5) -> SurroundingRectangle:
    """Riquadro color accento attorno a un mobject (da animare con Create)."""
    return SurroundingRectangle(mob, color=colore or _cfg().palette.accento, buff=buff, corner_radius=px(16),
                                stroke_width=tratto(spessore_px))


class CorniceSchermo(VGroup):
    """Bordo arrotondato dell'area schermo (il b-roll ci viene messo sotto dal compositing)."""

    def __init__(self, area, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        r = int(cfg.dati["schermo"].get("raggio_px", 36))
        self.box = RoundedRectangle(corner_radius=px(r), width=area.larghezza, height=area.altezza,
                                    stroke_color=colore or cfg.palette.attenuato, stroke_width=tratto(4), fill_opacity=0).move_to(area.centro)
        self.add(self.box)

    def entra(self, **kw):
        return Create(self.box, **kw)


class Piede(VGroup):
    """Handle del canale in basso a sinistra, se configurato (vuoto altrimenti: controlla len() prima di animarlo)."""

    def __init__(self, area, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        h = str(cfg.canale.handle or cfg.canale.nome or "")
        if h:
            t = testo(h, "piede", colore=cfg.palette.attenuato)
            t.move_to([area.x0 + t.width / 2, area.y0 - px(50), 0])
            self.add(t)
        _marca(self)


class Messaggio(Titolo):
    """Messaggio di chiusura: maiuscolo, grassetto, con ==enfasi==; CTA a pillola opzionale sotto."""

    def __init__(self, s: str, cta: str | None = None, larghezza_px: float = 900, **kw):
        super().__init__(s, larghezza_px=larghezza_px, ruolo="messaggio", **kw)
        self.cta = None
        if cta:
            self.cta = Etichetta(cta)
            if self.cta.width > px(larghezza_px):
                self.cta.scale_to_fit_width(px(larghezza_px))
            self.cta.next_to(self.testo, DOWN, aligned_edge=LEFT, buff=px(44))
            self.add(self.cta)
        _marca(self)

    def entra(self, **kw):
        anims = [self.per_righe()]
        if self.cta is not None:
            anims.append(FadeIn(self.cta, scale=0.85))
        return LaggedStart(*anims, lag_ratio=0.6, group=self, **kw)


class Punch(VGroup):
    """La battuta a tutto schermo (il cambio grande, docs/linguaggio-reel.md §5): 1-3 parole in maiuscolo e grassetto,
    nel corpo più grande che sta nell'area (fino a CORPO_PX["punch"]), centrate. Di solito non si usa da sola:
    ScenaReel.punch() toglie la scena per il tempo della battuta e la rimette con un taglio."""

    def __init__(self, s: str, area, colore: str | None = None, maiuscolo: bool = True, **kw):
        super().__init__(**kw)
        self.testo = testo(s.upper() if maiuscolo else s, "punch", colore=colore or _cfg().palette.accento, peso=BOLD,
                           allinea="center", interlinea=0.1)
        larga, alta = area.larghezza * 0.94, area.altezza * 0.8
        if self.testo.width > larga:
            self.testo.scale_to_fit_width(larga)
        if self.testo.height > alta:
            self.testo.scale_to_fit_height(alta)
        self.add(self.testo.move_to(area.centro))
        _marca(self)

    def entra(self, **kw):
        """Entrata secca: da un po' più grande, veloce all'inizio (l'uscita è un taglio)."""
        return FadeIn(self, scale=1.25, rate_func=rush_from, **kw)


# --- icone, contatore che scorre, codice ----------------------------------------------------------------

CARTELLA_ICONE = RADICE / "assets" / "icone"


class Icona(VGroup):
    """Icona a tratto da assets/icone/<nome>.svg (set Lucide, licenza ISC) in un colore della palette.
    Altre icone: scarica l'SVG da lucide.dev nella stessa cartella."""

    def __init__(self, nome: str, altezza_px: float = 120, colore: str | None = None, **kw):
        super().__init__(**kw)
        f = CARTELLA_ICONE / f"{nome}.svg"
        if not f.exists():
            raise FileNotFoundError(f"icona «{nome}» assente in assets/icone/ (ci sono: {', '.join(Icona.disponibili())})")
        self.svg = SVGMobject(str(f), height=px(altezza_px))
        self.svg.set_fill(opacity=0).set_stroke(colore or _cfg().palette.testo, width=tratto(altezza_px * 2 / 24), opacity=1)
        for m in self.svg.family_members_with_points():
            m.cap_style = CapStyleType.ROUND
            m.joint_type = LineJointType.ROUND
        self.add(self.svg)

    @staticmethod
    def disponibili() -> list[str]:
        return sorted(p.stem for p in CARTELLA_ICONE.glob("*.svg"))

    def entra(self, **kw):
        return Create(self.svg, lag_ratio=0.15, **kw)


class ContatoreScorre(VGroup):
    """Numero grande che scorre fino a un valore (con separatore delle migliaia all'italiana).
    Dopo lo scorrimento chiama ferma(): toglie l'aggiornamento e il fotogramma finale resta statico."""

    def __init__(self, valore: float = 0, etichetta: str | None = None, decimali: int = 0, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.colore = colore or cfg.palette.accento
        self.decimali = decimali
        self.valore = ValueTracker(valore)
        self._scritto = self._formato(valore)
        self.numero = self._crea(self._scritto)
        self.add(self.numero)
        if etichetta:
            self.etich = testo(etichetta, "etichetta", colore=cfg.palette.attenuato).next_to(self.numero, DOWN, buff=px(12),
                                                                                           aligned_edge=LEFT)
            self.add(self.etich)
        self.numero.add_updater(self._aggiorna)
        _marca(self)

    def _formato(self, v: float) -> str:
        return f"{v:,.{self.decimali}f}".replace(",", " ").replace(".", ",").replace(" ", ".")

    def _crea(self, s: str) -> Blocco:
        return testo(s, "messaggio", colore=self.colore, peso=BOLD, mono=True)

    def _aggiorna(self, m) -> None:
        s = self._formato(self.valore.get_value())
        if s != self._scritto:   # Pango solo quando il numero scritto cambia
            self._scritto = s
            nuovo = self._crea(s).move_to(m, aligned_edge=LEFT)
            m.become(nuovo)
            # become allinea i punti ma lascia in piedi le Riga di prima: senza questo i controlli (e
            # `parole_a_schermo`) continuerebbero a leggere la cifra vecchia
            for vecchia, adesso in zip(m.righe, nuovo.righe, strict=False):
                vecchia.piano = adesso.piano
            _marca(m)

    def scorri(self, a: float, **kw):
        kw.setdefault("rate_func", linear)
        return self.valore.animate(**kw).set_value(a)

    def ferma(self) -> None:
        self.numero.clear_updaters()

    def entra(self, **kw):
        return FadeIn(self, scale=0.8, **kw)


def _stile_codice(cfg: Config):
    """Stile Pygments con i colori della palette (Code di Manim 0.21 prende i colori solo dallo stile)."""
    from pygments.style import Style
    from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String
    from pygments.token import Text as TestoCodice
    p = cfg.palette

    class StilePalette(Style):
        background_color = p.sfondo
        line_number_color = p.attenuato
        styles = {TestoCodice: p.testo, Name: p.testo, Keyword: f"bold {p.accento}", Name.Function: p.secondario,
                  Name.Class: p.secondario, Name.Builtin: p.secondario, String: p.terziario, Number: p.secondario,
                  Comment: f"italic {p.attenuato}", Operator: p.attenuato, Punctuation: p.attenuato}

    return StilePalette


class Codice(VGroup):
    """Blocco di codice evidenziato con i colori della palette (Pygments + Pango: niente LaTeX), corpo «token».
    Poche righe corte (~28 caratteri): se è più largo di larghezza_px solleva un errore, non rimpicciolisce."""

    def __init__(self, codice: str, linguaggio: str = "python", larghezza_px: float = 900, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        p = cfg.palette
        self.codice = Code(code_string=codice.strip("\n"), language=linguaggio, formatter_style=_stile_codice(cfg),
                           add_line_numbers=False, background="rectangle",
                           background_config={"buff": px(36), "fill_color": p.sfondo, "stroke_color": p.attenuato,
                                              "stroke_width": tratto(3), "corner_radius": px(24), "fill_opacity": 1},
                           paragraph_config={"font": cfg.font.mono, "font_size": font_size_per(CORPO_PX["token"]),
                                             "line_spacing": 0.6})
        if self.codice.width > px(larghezza_px) + 1e-6:
            raise ValueError(f"codice largo {self.codice.width * cfg.px_per_unita:.0f} px (massimo {larghezza_px:.0f}): "
                             "accorcia le righe (~28 caratteri)")
        self.add(self.codice)

    def riga(self, i: int):
        return self.codice.code_lines[i]

    def entra(self, **kw):
        return FadeIn(self, shift=UP * 0.2, **kw)

    def righe_una_alla_volta(self, lag: float = 0.3, **kw):
        return LaggedStart(FadeIn(self.codice.background), *[FadeIn(r, shift=RIGHT * 0.1) for r in self.codice.code_lines],
                           lag_ratio=lag, **kw)

    def evidenzia_riga(self, i: int, **kw):
        self.riquadro = Evidenzia(self.riga(i), buff=px(10))
        return Create(self.riquadro, **kw)


__all__ = ["testo", "markup", "piano", "avvolgi", "tratto", "etichetta", "Riga", "Blocco", "Titolo", "Didascalia",
           "Sagome", "Fila", "Spunta", "Croce", "Indice", "Lente", "PrimaDopo", "Etichetta", "Barrato",
           "Freccia", "Carta", "Barra", "Classifica", "Token", "Frase", "Lista", "Contatore", "Evidenzia", "CorniceSchermo",
           "Piede", "Messaggio", "Punch", "Icona", "ContatoreScorre", "Codice", "FadeIn", "FadeOut", "FadeTransform", "Indicate", "LaggedStart", "AnimationGroup",
           "Transform", "Create"]


# --- spiegare senza parole -------------------------------------------------------------------------------
# Dal 2026-09-20 i reel si guardano muti, con le caption che dicono il parlato: la figura deve reggere il
# concetto da sola. Questi componenti non contengono testo (o ne contengono al massimo un'etichetta).

class Sagome(VGroup):
    """Un documento (mail, pagina, elenco) reso come barrette: si capisce che è un testo, non si legge.
    `righe` sono le lunghezze relative (0-1) delle righe; `vuote` sono gli indici delle righe spente."""

    def __init__(self, righe: list[float] | int = 5, larghezza_px: float = 620, altezza_px: float = 18,
                 passo_px: float = 46, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        quote = [0.95, 0.72, 0.88, 0.6, 0.8][:righe] if isinstance(righe, int) else list(righe)
        if isinstance(righe, int) and righe > 5:
            quote = [(0.95, 0.72, 0.88, 0.6, 0.8)[i % 5] for i in range(righe)]
        self.righe = VGroup(*[
            RoundedRectangle(corner_radius=px(altezza_px / 2), width=px(larghezza_px * max(0.08, q)), height=px(altezza_px),
                             stroke_width=0, fill_color=colore or cfg.palette.attenuato, fill_opacity=0.45)
            for q in quote])
        self.righe.arrange(DOWN, buff=px(passo_px - altezza_px), aligned_edge=LEFT)
        self.add(self.righe)

    def accendi(self, i: int, colore: str | None = None, **kw):
        """Una riga si accende: è quella di cui parla la voce (senza mostrarne le parole)."""
        return self.righe[i].animate(**kw).set_fill(colore or _cfg().palette.accento, opacity=1)

    def entra(self, lag: float = 0.12, **kw):
        return LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in self.righe], lag_ratio=lag, group=self, **kw)


class Fila(VGroup):
    """Una quantità come pittogramma: `quanti` icone uguali in righe da `per_riga`, di cui `accese` in accento.
    È il modo di dire «sei su dieci» senza scrivere una frase."""

    def __init__(self, icona: str = "user", quanti: int = 10, per_riga: int = 5, accese: int = 0,
                 altezza_px: float = 96, passo_px: float = 128, colore: str | None = None, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.spento = colore or cfg.palette.attenuato
        self.figure = VGroup(*[Icona(icona, altezza_px=altezza_px, colore=self.spento) for _ in range(quanti)])
        righe = VGroup()
        for i in range(0, quanti, per_riga):
            r = VGroup(*self.figure[i:i + per_riga]).arrange(RIGHT, buff=px(passo_px - altezza_px))
            righe.add(r)
        righe.arrange(DOWN, buff=px(passo_px - altezza_px), aligned_edge=LEFT)
        self.add(righe)
        if accese:
            for f in self.figure[:accese]:
                f.svg.set_stroke(cfg.palette.accento)

    def accendi(self, quante: int, colore: str | None = None, lag: float = 0.08, **kw):
        """Le prime `quante` figure passano in accento, una dopo l'altra."""
        col = colore or _cfg().palette.accento
        return LaggedStart(*[f.svg.animate.set_stroke(col) for f in self.figure[:quante]], lag_ratio=lag, group=self, **kw)

    def entra(self, lag: float = 0.05, **kw):
        return LaggedStart(*[FadeIn(f, scale=0.8) for f in self.figure], lag_ratio=lag, group=self, **kw)


class Spunta(VGroup):
    """Il verdetto «sì» senza scriverlo: un segno di spunta disegnato a tratto."""

    def __init__(self, altezza_px: float = 96, colore: str | None = None, spessore_px: float = 12, **kw):
        super().__init__(**kw)
        h = px(altezza_px)
        self.segno = VMobject(stroke_color=colore or _cfg().palette.terziario, stroke_width=tratto(spessore_px))
        self.segno.set_points_as_corners([np.array([-h * 0.45, 0.0, 0]), np.array([-h * 0.1, -h * 0.38, 0]),
                                          np.array([h * 0.5, h * 0.42, 0])])
        self.segno.cap_style = CapStyleType.ROUND
        self.segno.joint_type = LineJointType.ROUND
        self.add(self.segno)

    def entra(self, **kw):
        return Create(self.segno, **kw)


class Croce(VGroup):
    """Il verdetto «no»: due tratti incrociati (con Spunta è la coppia giusto/sbagliato)."""

    def __init__(self, altezza_px: float = 96, colore: str | None = None, spessore_px: float = 12, **kw):
        super().__init__(**kw)
        h, col = px(altezza_px) / 2, colore or _cfg().palette.accento
        self.tratti = VGroup(
            Line([-h, -h, 0], [h, h, 0], stroke_color=col, stroke_width=tratto(spessore_px)),
            Line([-h, h, 0], [h, -h, 0], stroke_color=col, stroke_width=tratto(spessore_px)))
        for t in self.tratti:
            t.cap_style = CapStyleType.ROUND
        self.add(self.tratti)

    def entra(self, **kw):
        return AnimationGroup(*[Create(t) for t in self.tratti], lag_ratio=0.35, group=self, **kw)


class Indice(VGroup):
    """Il gesto: un puntatore che indica, tocca e trascina. Serve a dire «questo», «prendi quello e mettilo qui»
    senza una parola. Il puntatore è un triangolo pieno con la punta in alto a sinistra."""

    def __init__(self, altezza_px: float = 88, colore: str | None = None, **kw):
        super().__init__(**kw)
        h = px(altezza_px)
        col = colore or _cfg().palette.testo
        self.freccia = VMobject(stroke_width=0, fill_color=col, fill_opacity=1)
        self.freccia.set_points_as_corners([np.array([0.0, 0.0, 0]), np.array([0.0, -h, 0]),
                                            np.array([h * 0.28, -h * 0.72, 0]), np.array([h * 0.46, -h * 0.98, 0]),
                                            np.array([h * 0.60, -h * 0.88, 0]), np.array([h * 0.42, -h * 0.62, 0]),
                                            np.array([h * 0.70, -h * 0.58, 0]), np.array([0.0, 0.0, 0])])
        self.add(self.freccia)
        self.scostamento = np.array([-h * 0.12, h * 0.12, 0])   # la punta sta sopra-sinistra rispetto al bersaglio

    def vai_a(self, mob, **kw):
        """Si sposta sul bersaglio (la punta sul suo centro)."""
        return self.animate(**kw).move_to(mob.get_center() - self.scostamento + np.array([self.width / 2, -self.height / 2, 0]))

    def tocca(self, scala: float = 0.82, **kw):
        """Il «tap»: si stringe e torna."""
        return Succession(self.animate(run_time=0.12).scale(scala), self.animate(run_time=0.12).scale(1 / scala), **kw)

    def trascina(self, mob, a, **kw):
        """Porta `mob` fino ad `a` (punto o mobject) muovendo insieme puntatore e oggetto."""
        meta = a.get_center() if hasattr(a, "get_center") else np.array(a)
        salto = meta - mob.get_center()
        return AnimationGroup(self.animate.shift(salto), mob.animate.move_to(meta), group=self, **kw)

    def entra(self, **kw):
        return FadeIn(self, shift=DOWN * 0.2, **kw)


class Lente(VGroup):
    """Una lente che ingrandisce un pezzo della figura restando dentro la figura (il resto non si muove)."""

    def __init__(self, raggio_px: float = 150, colore: str | None = None, spessore_px: float = 8, **kw):
        super().__init__(**kw)
        cfg = _cfg()
        self.cerchio = Circle(radius=px(raggio_px), stroke_color=colore or cfg.palette.testo,
                              stroke_width=tratto(spessore_px), fill_opacity=0)
        self.add(self.cerchio)

    def passa_su(self, mob, **kw):
        return self.animate(**kw).move_to(mob.get_center())

    def entra(self, **kw):
        return Create(self.cerchio, **kw)


class PrimaDopo(VGroup):
    """Due stati della stessa figura, uno sopra l'altro: una tendina verticale scopre il «dopo».
    `prima` e `dopo` sono due mobject già impaginati nello stesso posto."""

    def __init__(self, prima: Mobject, dopo: Mobject, **kw):
        super().__init__(**kw)
        self.prima, self.dopo = prima, dopo
        dopo.move_to(prima)
        self.add(prima, dopo)
        self._larghezza = max(prima.width, dopo.width)
        self.dopo.set_opacity(0)

    def passa(self, durata_s: float = 0.8, **kw):
        """La tendina: il «dopo» compare da sinistra a destra mentre il «prima» sparisce."""
        kw.setdefault("run_time", durata_s)
        return AnimationGroup(FadeOut(self.prima), FadeIn(self.dopo.set_opacity(1), shift=RIGHT * 0.15),
                              lag_ratio=0.25, group=self, **kw)
