"""Catalogo dei pattern Manim: una scena di prova per ogni pattern di `docs/pattern-manim.md`.

Gemello di `vetrina.py` (che prova i *componenti*): qui stanno i **modi di fare** che tornano in ogni reel e che
nessun componente incapsula — passaggi a finestre, rimbalzo che non esce dall'area, corpo più grande che tiene una
riga sola, riflesso che scorre, zoom verificato. Il codice qui è il pattern: si legge, si copia, si adatta.

Regola del catalogo: **un pattern senza scena di prova non entra**. Così non si riempie di roba non verificata.
Quando un aiuto locale compare per la terza volta in `contenuti/animazioni/*.py`, diventa un pattern (o un
componente): è la «regola del tre» di `docs/pattern-manim.md`.

Uso: uv run python -m tools.anim.pattern [--solo nome] [--qualita l|m|h] [--out cartella]
Esce con 1 se una scena ha avvisi di tempo o violazioni dei controlli.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from manim import DOWN, LEFT, RIGHT, UP, FadeIn, FadeOut, Rectangle, Succession, VGroup, rate_functions

from .base import ScenaReel
from .componenti import Fila, Icona, Sagome, testo
from .config import RADICE, carica
from .misure import CORPO_PX, px, tratto

DURATA_S = 6.0
SCENA = {"voce": ["uno due tre", "quattro cinque sei", "sette otto nove"], "riquadro": "si"}


# --- pattern 1: finestre (un solo oggetto alla volta, senza accavallamenti) --------------------------------

def finestre(scena: ScenaReel, tappe: list, durata_s: float) -> None:
    """Ogni tappa ha la sua finestra di tempo: entra, resta, esce **prima** che entri la successiva.
    È il rimedio ai «testi sovrapposti per 0,3 s» che si vedono solo a 8 fps: due animazioni che si
    accavallano di un fotogramma lasciano due cose leggibili insieme."""
    quanto = scena.arrotonda(durata_s / max(1, len(tappe)))
    for i, mob in enumerate(tappe):
        scena.play(FadeIn(mob), run_time=scena.arrotonda(quanto * 0.35))
        scena.wait(max(0.0, quanto * 0.3))
        if i < len(tappe) - 1:
            scena.play(FadeOut(mob), run_time=scena.arrotonda(quanto * 0.35))


class PatternFinestre(ScenaReel):
    def costruisci(self):
        a = self.area.contenuto
        pezzi = [Icona(n, altezza_px=200) for n in ("brain", "cpu", "sparkles")]
        for m in pezzi:
            a.metti(m, "centro", "centro")
        finestre(self, pezzi, self.durata_s * 0.9)


# --- pattern 2: rimbalzo che non esce dall'area ------------------------------------------------------------

def rimbalzo(oltre: float = 0.06):
    """`ease_out_back` di Manim arretra del 10 %: su un oggetto largo 900 px sono 90 px fuori dall'area.
    Questa versione lascia scegliere di quanto sfora (6 % = una ventina di px, due fotogrammi)."""
    def f(t: float) -> float:
        s = 1.70158 * (oltre / 0.10)
        t -= 1
        return t * t * ((s + 1) * t + s) + 1
    return f


class PatternRimbalzo(ScenaReel):
    def costruisci(self):
        a = self.area.contenuto
        carta = Rectangle(width=px(560), height=px(160), stroke_color=self.cfg.palette.secondario,
                          stroke_width=tratto(3), fill_color=self.cfg.palette.sfondo, fill_opacity=1)
        a.metti(carta, "centro", "centro")
        self.add(carta)
        self.beat(1)
        grande = Rectangle(width=px(860), height=px(260), stroke_color=self.cfg.palette.accento,
                           stroke_width=tratto(3), fill_color=self.cfg.palette.sfondo, fill_opacity=1)
        a.metti(grande, "centro", "centro")
        self.play(carta.animate.become(grande), run_time=0.6, rate_func=rimbalzo(0.06))


# --- pattern 3: il corpo più grande che tiene una riga sola -------------------------------------------------

def grande(s: str, larghezza_px: float, ruoli: tuple[str, ...] = ("punch", "titolo", "messaggio")) -> VGroup:
    """`MarkupText` va a capo da solo (Pango riceve una larghezza fissa) e non si può spegnere: una parola larga
    diventa due righe senza che il codice lo chieda. Si provano i corpi dal più grande al più piccolo e si tiene il
    primo che sta in una riga sola dentro `larghezza_px`."""
    for ruolo in ruoli:
        blocco = testo(s, ruolo, peso="BOLD")
        if len(blocco.righe) == 1 and blocco.width * 120 <= larghezza_px:
            return blocco
    return testo(s, ruoli[-1], peso="BOLD", larghezza_px=larghezza_px)


class PatternGrande(ScenaReel):
    def costruisci(self):
        a = self.area.contenuto
        for i, parola in enumerate(("SUBIRLA", "SAPERLA USARE")):
            m = grande(parola, a.larghezza * 120)
            a.metti(m, "centro", "centro")
            if i:
                self.beat(1)
            self.play(FadeIn(m), run_time=0.4)
            if not i:
                self.play(FadeOut(m), run_time=0.3)   # esce del tutto prima che entri l'altra (pattern 1)


# --- pattern 4: riflesso che scorre su una figura -----------------------------------------------------------

def riflesso(scena: ScenaReel, sopra, durata_s: float = 0.8):
    """Una banda chiara che scende una volta sopra una figura, senza cambiarla: dice «guarda qui» su un oggetto
    che deve restare identico (se cambiasse, la figura affermerebbe qualcosa che non è successo)."""
    banda = Rectangle(width=sopra.width * 1.05, height=px(26), stroke_width=0,
                      fill_color=scena.cfg.palette.testo, fill_opacity=0.18)
    banda.move_to(sopra.get_top() + UP * px(20))
    scena.add(banda)
    scena.play(banda.animate.move_to(sopra.get_bottom() + DOWN * px(20)), run_time=durata_s)
    scena.remove(banda)


class PatternRiflesso(ScenaReel):
    def costruisci(self):
        s = Sagome(5, larghezza_px=560)
        self.area.contenuto.metti(s, "centro", "sinistra", buff_px=20)
        self.play(s.entra(), run_time=0.6)
        self.beat(1)
        riflesso(self, s, 0.9)


# --- pattern 5: zoom verificato ------------------------------------------------------------------------------

def controlla_zoom(scena: ScenaReel, dentro: list, fattore: float) -> None:
    """Con la camera ingrandita, quello che sta fuori dalla cornice sparisce: prima di zoomare si controlla che gli
    oggetti che devono restare leggibili ci stiano davvero."""
    larghezza = scena.cfg.frame_width / fattore
    altezza = scena.cfg.frame_height / fattore
    for m in dentro:
        if m.width > larghezza or m.height > altezza:
            scena.avvisi.append(f"zoom {fattore}×: «{type(m).__name__}» non ci sta ({m.width:.1f} > {larghezza:.1f})")


class PatternZoom(ScenaReel):
    def costruisci(self):
        f = Fila("user", quanti=10, per_riga=5, altezza_px=80)
        self.area.contenuto.metti(f, "centro", "centro")
        self.play(f.entra(), run_time=0.6)
        self.beat(1)
        controlla_zoom(self, [f.figure[0]], 2.2)
        self.play(self.zoom_su(f.figure[0], 2.2), run_time=0.6)
        self.beat(2)
        self.play(self.torna(), run_time=0.5)


# --- pattern 6: stato di fine vincolante ---------------------------------------------------------------------

def fine_scena(mobs: list) -> dict:
    """L'ultimo fotogramma di una scena è il primo della successiva (quando non c'è uno stacco): si dichiara qui,
    e la scena dopo ricostruisce esattamente questo. Ritorna posizioni e scale, da confrontare nei test."""
    return {type(m).__name__: (float(m.get_center()[0]), float(m.get_center()[1]), float(m.width)) for m in mobs}


class PatternFineScena(ScenaReel):
    def costruisci(self):
        f = Fila("user", quanti=10, per_riga=5, altezza_px=80)
        self.area.contenuto.metti(f, "alto", "centro")
        self.play(f.entra(), run_time=0.5)
        self.beat(1)
        self.play(f.accendi(6), run_time=0.6)
        self.stato_finale = fine_scena([f])


SCENE = [PatternFinestre, PatternRimbalzo, PatternGrande, PatternRiflesso, PatternZoom, PatternFineScena]


def main(argv: list[str] | None = None) -> int:
    from ..reel.contact_sheet import genera as contact
    from ..reel.fotogrammi import filmstrip_scena, fotogramma_chiave
    from ..reel.manim_render import renderizza
    ap = argparse.ArgumentParser(prog="pattern", description="scene di prova dei pattern di docs/pattern-manim.md")
    ap.add_argument("--solo", help="solo i pattern il cui nome contiene questo testo")
    ap.add_argument("--qualita", choices="lmh", default="l")
    ap.add_argument("--out", default=str(RADICE / "contenuti" / "render" / "_pattern"))
    a = ap.parse_args(argv)
    cfg = carica()
    out = Path(a.out)
    celle, problemi = [], 0
    for k, cls in enumerate(SCENE, 1):
        nome = cls.__name__.removeprefix("Pattern")
        if a.solo and a.solo.lower() not in nome.lower():
            continue
        base = f"{k:02d}-{nome.lower()}"
        res = renderizza(cls, DURATA_S, dict(SCENA), out / "_manim", base, a.qualita, cfg=cfg)
        png = fotogramma_chiave(res.video, DURATA_S, out / f"{base}.png", frazione=0.97)
        filmstrip_scena(res.video, DURATA_S, out / f"{base}-filmstrip.png")
        guai = res.avvisi + res.controlli
        problemi += len(guai)
        print(f"{nome}: {png}" + ("" if guai else "  ok"))
        for g in guai:
            print(f"   ✗ {g}")
        celle.append({"file": png, "etichetta": nome, "animata": True, "problema": bool(guai)})
    if celle:
        contact(celle, [], out / "contact-sheet.png")
        print(f"-> {out / 'contact-sheet.png'}")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
