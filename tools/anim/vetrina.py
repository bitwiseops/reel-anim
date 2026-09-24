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

from manim import DOWN, LEFT, RIGHT, AnimationGroup, FadeIn, FadeOut, LaggedStart, VGroup

from .base import ScenaReel
from .componenti import (Classifica, Codice, ContatoreScorre, Croce, Didascalia, Fila, Icona, Indice, Lente,
                         Lista, PrimaDopo, Sagome, Spunta, testo)
from .config import RADICE, carica
from .diagrammi import Ciclo, Confronto, Corrispondenza, Flusso, Graffa, Tabella
from .misure import px

DURATA_S = 6.0
SCENA = {"voce": ["uno due tre", "quattro cinque sei", "sette otto nove"], "riquadro": "si"}


class VetrinaFlusso(ScenaReel):
    def costruisci(self):
        f = Flusso(["domanda", "modello", "parola"])
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
        c = Confronto("originale", "vero")
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
        lista = Lista(["dettaglio", "vincolo", "scarto"], larghezza_px=560)
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
        nota = Didascalia("esempio: numeri indicativi", area=self.area.contenuto)
        self.play(nota.entra(), run_time=0.4)


class VetrinaCodice(ScenaReel):
    def costruisci(self):
        cod = Codice('risposta = modello.genera(\n    "Due righe per Marco",\n    temperatura=0.7,\n)')
        self.area.contenuto.metti(cod, "centro", "sinistra")
        self.play(cod.righe_una_alla_volta(), run_time=1.2)
        self.beat(1)
        self.play(cod.evidenzia_riga(2), run_time=0.5)


class VetrinaIcone(ScenaReel):
    PER_PAGINA = 12     # 4 × 3: con più icone la griglia usciva dall'area; si sfogliano a pagine

    def costruisci(self):
        att = self.cfg.palette.attenuato
        nomi = Icona.disponibili()
        pagine = [nomi[k:k + self.PER_PAGINA] for k in range(0, len(nomi), self.PER_PAGINA)]
        for n_pag, pagina in enumerate(pagine):
            # i nomi composti vanno a capo, sennò escono di lato
            celle = VGroup(*[VGroup(Icona(n, 84), testo(n.replace("-", "-\n"), "piede", colore=att)).arrange(DOWN, buff=px(12))
                             for n in pagina])
            celle.arrange_in_grid(cols=4, buff=(px(20), px(24)))
            self.area.contenuto.metti(celle, "centro", "centro")
            self.play(LaggedStart(*[AnimationGroup(c[0].entra(), FadeIn(c[1])) for c in celle], lag_ratio=0.1), run_time=1.2)
            if n_pag < len(pagine) - 1:
                self.wait(0.6)
                self.play(FadeOut(celle), run_time=0.3)


class VetrinaContatore(ScenaReel):
    def costruisci(self):
        c = ContatoreScorre(0, "parametri del modello (esempio)")
        self.area.contenuto.metti(c, "centro", "sinistra", buff_px=20)
        self.play(c.entra(), run_time=0.4)
        self.beat(1)
        self.play(c.scorri(70_000_000_000), run_time=1.4)
        c.ferma()


class VetrinaPunch(ScenaReel):
    def costruisci(self):
        lista = Lista(["dettaglio", "vincolo"], larghezza_px=560)
        self.area.contenuto.metti(lista, "centro", "sinistra", buff_px=20)
        self.play(lista.entra_una_alla_volta(), run_time=0.8)
        self.beat(1)
        self.punch("tu sì")                                 # taglio alla battuta e ritorno alla scena
        self.beat(2)
        self.play(lista.voci[0].animate.set_color(self.cfg.palette.accento), run_time=0.3)


class VetrinaZoom(ScenaReel):
    def costruisci(self):
        cl = Classifica([("oggi", 0.48), ("ti", 0.22), ("la", 0.08)], larghezza_px=620)
        self.area.contenuto.metti(cl, "alto", "sinistra", buff_px=20)
        self.play(cl.entra(), run_time=0.8)
        self.beat(1)
        self.play(self.zoom_su(cl.barre[2], 1.3), run_time=0.6)   # il cambio grande senza disegni nuovi
        self.beat(2)
        self.play(self.torna(), run_time=0.5)


class VetrinaFila(ScenaReel):
    """Una quantità senza scriverla: sei figure su dieci si accendono."""

    def costruisci(self):
        f = Fila("user", quanti=10, per_riga=5, altezza_px=96)
        self.area.contenuto.metti(f, "alto", "centro", buff_px=20)
        self.play(f.entra(), run_time=0.8)
        self.beat(1)
        self.play(f.accendi(6), run_time=0.9)


class VetrinaSagome(ScenaReel):
    """Un documento che si vede ma non si legge: la riga di cui parla la voce si accende."""

    def costruisci(self):
        s = Sagome(6, larghezza_px=620)
        self.area.contenuto.metti(s, "centro", "sinistra", buff_px=20)
        self.play(s.entra(), run_time=0.8)
        self.beat(1)
        self.play(s.accendi(2), run_time=0.4)
        self.beat(2)
        self.play(s.accendi(4), run_time=0.4)


class VetrinaGesto(ScenaReel):
    """Il gesto: il puntatore indica una riga, la tocca e la trascina."""

    def costruisci(self):
        s = Sagome(5, larghezza_px=560)
        self.area.contenuto.metti(s, "alto", "sinistra", buff_px=20)
        ind = Indice()
        ind.next_to(s, DOWN, buff=px(40))
        self.play(FadeIn(s), ind.entra(), run_time=0.6)
        self.beat(1)
        self.play(ind.vai_a(s.righe[1]), run_time=0.5)
        self.play(ind.tocca(), run_time=0.3)
        self.beat(2)
        self.play(ind.trascina(s.righe[1], s.get_bottom() + DOWN * px(120)), run_time=0.8)


class VetrinaVerdetto(ScenaReel):
    """Sì e no senza parole, e la lente che guarda un pezzo."""

    def costruisci(self):
        s = Sagome(4, larghezza_px=520)
        self.area.contenuto.metti(s, "alto", "sinistra", buff_px=20)
        sp, cr = Spunta(), Croce()
        sp.next_to(s, DOWN, buff=px(60)).align_to(s, LEFT)
        cr.next_to(sp, RIGHT, buff=px(140))
        le = Lente(raggio_px=120).move_to(s.righe[0])
        self.play(FadeIn(s), run_time=0.4)
        self.beat(1)
        self.play(sp.entra(), run_time=0.5)
        self.play(cr.entra(), run_time=0.5)
        self.beat(2)
        self.play(le.entra(), run_time=0.4)
        self.play(le.passa_su(s.righe[2]), run_time=0.6)


class VetrinaPrimaDopo(ScenaReel):
    """Lo stesso oggetto prima e dopo, con la tendina."""

    def costruisci(self):
        prima = Sagome([0.9, 0.85, 0.7, 0.6], larghezza_px=560)
        dopo = Sagome([0.5, 0.45], larghezza_px=560, colore=self.cfg.palette.terziario)
        pd = PrimaDopo(prima, dopo)
        self.area.contenuto.metti(pd, "centro", "centro")
        self.play(FadeIn(prima), run_time=0.5)
        self.beat(1)
        self.play(pd.passa(), run_time=0.9)


SCENE = [VetrinaFila, VetrinaSagome, VetrinaGesto, VetrinaVerdetto, VetrinaPrimaDopo, VetrinaFlusso, VetrinaCiclo, VetrinaConfronto, VetrinaCorrispondenza, VetrinaGraffa, VetrinaTabella, VetrinaCodice,
         VetrinaIcone, VetrinaContatore, VetrinaPunch, VetrinaZoom]


def mostra(scene: list, prefisso: str, descrizione: str, cartella: str, argv: list[str] | None = None) -> int:
    """Rende ogni scena di prova, stampa i controlli falliti e fa il contact sheet; 1 se qualcosa non passa.
    La usano questa vetrina e quella dei pattern (`tools/anim/pattern.py`)."""
    from ..reel.contact_sheet import genera as contact
    from ..reel.fotogrammi import filmstrip_scena, fotogramma_chiave
    from ..reel.manim_render import renderizza
    ap = argparse.ArgumentParser(prog=prefisso.lower(), description=descrizione)
    ap.add_argument("--solo", help="solo le scene il cui nome contiene questo testo")
    ap.add_argument("--qualita", choices="lmh", default="l")
    ap.add_argument("--out", default=str(RADICE / "contenuti" / "render" / cartella))
    a = ap.parse_args(argv)
    cfg = carica()
    out = Path(a.out)
    celle, problemi = [], 0
    for k, cls in enumerate(scene, 1):
        nome = cls.__name__.removeprefix(prefisso)
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


def main(argv: list[str] | None = None) -> int:
    return mostra(SCENE, "Vetrina", "scene di prova dei componenti, con i controlli automatici", "_vetrina", argv)

if __name__ == "__main__":
    sys.exit(main())
