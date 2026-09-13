"""Vetrina dei componenti di diagrammi.py e dei più recenti di componenti.py: una scena di prova per ognuno, senza
sceneggiatura, per vedere come stanno e per passarli dai controlli automatici. È anche un esempio d'uso.

Uso: uv run python -m tools.anim.vetrina [--solo nome] [--qualita l|m|h] [--out cartella]
Output (default contenuti/render/_vetrina/): NN-nome.png (fotogramma finale), NN-nome-filmstrip.png, contact-sheet.png.
Esce con 1 se una scena ha avvisi di tempo o violazioni dei controlli.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from manim import DOWN, AnimationGroup, FadeIn, LaggedStart, VGroup

from .base import ScenaReel
from .componenti import Caption, Codice, ContatoreScorre, Icona, Lista, testo
from .config import RADICE, carica
from .diagrammi import Ciclo, Confronto, Corrispondenza, Flusso, Graffa, Tabella
from .misure import px

DURATA_S = 6.0
SCENA = {"voce": ["uno due tre", "quattro cinque sei", "sette otto nove"], "riquadro": "si"}


class VetrinaFlusso(ScenaReel):
    def costruisci(self):
        f = Flusso(["La domanda entra nel modello", "Il modello sceglie una parola", "La parola si aggiunge al testo"])
        self.area.contenuto.metti(f, "alto", "centro", buff_px=20)
        for i in range(3):
            self.beat(i)
            self.play(f.entra_passo(i), run_time=0.6)
            self.play(f.attiva(i), run_time=0.3)


class VetrinaCiclo(ScenaReel):
    def costruisci(self):
        c = Ciclo(["pensa", "agisci", "osserva"])
        self.area.contenuto.metti(c, "centro", "centro")
        self.play(c.entra(), run_time=1.0)
        self.play(c.accendi(0), run_time=0.3)
        for i in (1, 2):
            self.beat(i)
            self.play(c.vai(), run_time=0.7)
            self.play(c.accendi(c.corrente), run_time=0.3)


class VetrinaConfronto(ScenaReel):
    def costruisci(self):
        c = Confronto("Scrivi un biglietto originale per Marco.",
                      "Marco ha litigato una vita con la fotocopiatrice: due righe su questo.")
        self.area.contenuto.metti(c, "alto", "sinistra")
        self.play(c.mostra_prima(), run_time=0.5)
        self.beat(1)
        self.play(c.boccia(), run_time=0.6)
        self.beat(2)
        self.play(c.mostra_dopo(), run_time=0.8)


class VetrinaCorrispondenza(ScenaReel):
    def costruisci(self):
        c = Corrispondenza(["gatto", "cane", "automobile"], ["animale", "veicolo"])
        self.area.contenuto.metti(c, "centro", "centro")
        self.play(c.entra(), run_time=0.8)
        self.beat(1)
        self.play(c.collega(0, 0), run_time=0.4)
        self.play(c.collega(1, 0), run_time=0.4)
        self.beat(2)
        self.play(c.collega(2, 0, giusto=False), run_time=0.4)
        self.play(c.collega(2, 1), run_time=0.4)


class VetrinaGraffa(ScenaReel):
    def costruisci(self):
        lista = Lista(["un dettaglio vero", "un vincolo", "scarta le prime idee"], larghezza_px=560)
        self.area.contenuto.metti(lista, "centro", "sinistra", buff_px=20)
        g = Graffa(lista, "contesto")
        self.play(lista.entra_una_alla_volta(), run_time=1.0)
        self.beat(1)
        self.play(g.entra(), run_time=0.6)


class VetrinaTabella(ScenaReel):
    def costruisci(self):
        t = Tabella([["modello", "parametri"], ["piccolo", "1 miliardo"], ["medio", "8 miliardi"], ["grande", "70 miliardi"]])
        self.area.contenuto.metti(t, "centro", "sinistra", buff_px=20)
        self.play(t.entra(), run_time=1.0)
        self.beat(1)
        self.play(t.evidenzia(3), run_time=0.5)
        self.beat(2)
        nota = Caption("esempio: numeri indicativi", area=self.area.contenuto)
        self.play(nota.entra(), run_time=0.4)


class VetrinaCodice(ScenaReel):
    def costruisci(self):
        cod = Codice('risposta = modello.genera(\n    "Due righe per Marco",\n    temperatura=0.7,\n)')
        self.area.contenuto.metti(cod, "centro", "sinistra")
        self.play(cod.righe_una_alla_volta(), run_time=1.2)
        self.beat(1)
        self.play(cod.evidenzia_riga(2), run_time=0.5)


class VetrinaIcone(ScenaReel):
    def costruisci(self):
        att = self.cfg.palette.attenuato
        celle = VGroup(*[VGroup(Icona(n, 100), testo(n, "piede", colore=att)).arrange(DOWN, buff=px(14))
                         for n in Icona.disponibili()])
        celle.arrange_in_grid(cols=3, buff=(px(40), px(36)))
        self.area.contenuto.metti(celle, "centro", "centro")
        self.play(LaggedStart(*[AnimationGroup(c[0].entra(), FadeIn(c[1])) for c in celle], lag_ratio=0.1), run_time=1.5)


class VetrinaContatore(ScenaReel):
    def costruisci(self):
        c = ContatoreScorre(0, "parametri del modello (esempio)")
        self.area.contenuto.metti(c, "centro", "sinistra", buff_px=20)
        self.play(c.entra(), run_time=0.4)
        self.beat(1)
        self.play(c.scorri(70_000_000_000), run_time=1.4)
        c.ferma()


SCENE = [VetrinaFlusso, VetrinaCiclo, VetrinaConfronto, VetrinaCorrispondenza, VetrinaGraffa, VetrinaTabella, VetrinaCodice,
         VetrinaIcone, VetrinaContatore]


def main(argv: list[str] | None = None) -> int:
    from ..reel.contact_sheet import genera as contact
    from ..reel.fotogrammi import filmstrip_scena, fotogramma_chiave
    from ..reel.manim_render import renderizza
    ap = argparse.ArgumentParser(prog="vetrina", description="scene di prova dei componenti, con i controlli automatici")
    ap.add_argument("--solo", help="solo i componenti il cui nome contiene questo testo")
    ap.add_argument("--qualita", choices="lmh", default="l")
    ap.add_argument("--out", default=str(RADICE / "contenuti" / "render" / "_vetrina"))
    a = ap.parse_args(argv)
    cfg = carica()
    out = Path(a.out)
    celle, problemi = [], 0
    for k, cls in enumerate(SCENE, 1):
        nome = cls.__name__.removeprefix("Vetrina")
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
