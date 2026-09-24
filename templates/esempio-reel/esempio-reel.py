"""Animazioni dell'esempio (esempio-reel.md qui accanto): una classe ScenaNN per scena.

Rifatto il 2026-09-20 per la regola «il reel si guarda muto» (docs/sceneggiatura.md §0): sul video vengono bruciate
le caption con il parlato, quindi qui **non ci sono frasi da leggere**. A schermo restano figure, numeri ed etichette
di una parola; il biglietto è un blocco di righe che si vede ma non si legge (`Sagome`). L'unica deroga è la scena 6,
dove il contenuto *è* la chat: lì la sceneggiatura dichiara `CAPTION: alto` e la fascia va in cima.

Vale come esempio d'uso della libreria: Titolo/Barrato, Classifica, Sagome, ContatoreScorre, Indice, Carta con la
sola linguetta, CorniceSchermo, Messaggio, Didascalia, Etichetta.
"""
from __future__ import annotations

from manim import DOWN, LEFT, RIGHT, UP, Create, FadeIn, FadeOut, Line, VGroup

from tools.anim.base import ScenaReel
from tools.anim.componenti import (Barrato, Carta, Classifica, ContatoreScorre, Didascalia, Etichetta, Evidenzia,
                                   CorniceSchermo, Indice, Messaggio, Sagome, Titolo, Token, testo)
from tools.anim.misure import px, tratto

CANDIDATE = [("si", 0.48), ("è", 0.22), ("ti", 0.08)]


def tessera(scena, s: str = "", larghezza_px: float = 150) -> VGroup:
    """Una tessera della riga: un rettangolo con dentro al massimo una parola (o niente)."""
    from manim import RoundedRectangle
    cfg = scena.cfg
    box = RoundedRectangle(corner_radius=px(12), width=px(larghezza_px), height=px(72), stroke_width=tratto(3),
                           stroke_color=cfg.palette.attenuato, fill_color=cfg.palette.sfondo, fill_opacity=1)
    g = VGroup(box)
    if s:
        g.add(testo(s, "token", colore=cfg.palette.testo).move_to(box))
    return g


class Scena01(ScenaReel):
    """Hook: il titolo è già in scena al primo fotogramma, «creativa» viene barrata, entra «probabile»."""

    def costruisci(self):
        a = self.area.contenuto
        t = Titolo("Generativa non vuol dire creativa", larghezza_px=880)
        a.metti(t, "alto", "sinistra", buff_px=20)
        self.add(t)
        self.play(t.animate.shift(UP * px(16)), run_time=0.5)
        self.beat(1)
        barra = Barrato(t.parola("creativa"))
        self.play(barra.entra(), run_time=0.5)
        self.beat(2)
        sub = Titolo("Vuol dire probabile", larghezza_px=760, ruolo="messaggio", colore=self.cfg.palette.accento)
        sub.next_to(t, DOWN, buff=px(56), aligned_edge=LEFT)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.6)


class Scena02(ScenaReel):
    """La riga cresce una tessera alla volta; sotto, tre barre: vince la più lunga."""

    def costruisci(self):
        a = self.area.contenuto
        self.riga = VGroup(*[tessera(self) for _ in range(3)]).arrange(RIGHT, buff=px(16))
        a.metti(self.riga, "alto", "sinistra", buff_px=20)
        self.play(FadeIn(self.riga[0]), run_time=0.3)
        self.play(FadeIn(self.riga[1]), run_time=0.3)
        self.beat(1)
        vuota = tessera(self)
        vuota.next_to(self.riga, RIGHT, buff=px(16))
        vuota[0].set_stroke(self.cfg.palette.accento)
        self.play(FadeIn(self.riga[2]), Create(vuota[0]), run_time=0.5)
        self.cl = Classifica(CANDIDATE, larghezza_px=560)
        self.cl.next_to(self.riga, DOWN, buff=px(90), aligned_edge=LEFT)
        self.play(self.cl.entra(), run_time=1.0)
        self.beat(2)
        self.play(self.cl.scegli(0), run_time=0.4)
        vincente = tessera(self, "si")
        vincente.move_to(self.cl.barre[0].etichetta, aligned_edge=LEFT)
        self.play(FadeIn(vincente), run_time=0.2)
        self.play(vincente.animate.move_to(vuota), run_time=0.6)
        self.remove(vuota)


class Scena03(ScenaReel):
    """La riga continua da sola e il contatore sale; il testo finito è un blocco che non si legge."""

    def costruisci(self):
        a = self.area.contenuto
        riga = VGroup(*[tessera(self, s) for s in ("", "si", "")]).arrange(RIGHT, buff=px(16))
        a.metti(riga, "alto", "sinistra", buff_px=20)
        cont = ContatoreScorre(3, "parole scelte")
        cont.next_to(riga, DOWN, buff=px(70), aligned_edge=LEFT)
        self.add(riga, cont)
        self.beat(1)
        blocco = Sagome([0.95, 0.8, 0.88, 0.55], larghezza_px=640)
        blocco.next_to(cont, DOWN, buff=px(70), aligned_edge=LEFT)
        self.play(blocco.entra(), cont.scorri(14), run_time=1.2)
        cont.ferma()
        self.beat(2)
        cornice = Evidenzia(blocco, buff=px(24))
        eti = Etichetta("probabile")
        eti.next_to(cornice, DOWN, buff=px(28)).align_to(blocco, LEFT)
        self.play(Create(cornice), run_time=0.5)
        self.play(eti.entra(), run_time=0.4)


class Scena04(ScenaReel):
    """Il bivio: tre rami di spessore diverso, il punto prende il più largo."""

    def costruisci(self):
        a = self.area.contenuto
        blocco = Sagome([0.9, 0.7], larghezza_px=420)
        a.metti(blocco, "alto", "sinistra", buff_px=20)
        self.add(blocco)
        partenza = blocco.get_bottom() + DOWN * px(20)
        rami, spessori = [], (16, 6, 4)
        for i, sp in enumerate(spessori):
            fine = partenza + RIGHT * px(230 * i) + DOWN * px(230)
            rami.append(Line(partenza, fine, stroke_color=self.cfg.palette.attenuato, stroke_width=tratto(sp)))
        self.play(*[Create(r) for r in rami], run_time=0.8)
        self.beat(1)
        grosso = rami[0]   # il primo è il più spesso: è la strada più battuta
        self.play(grosso.animate.set_stroke(self.cfg.palette.accento), run_time=0.4)
        nuovo = Etichetta("nuovo")
        nuovo.next_to(grosso.get_end(), DOWN, buff=px(24)).align_to(blocco, LEFT)
        self.play(nuovo.entra(), run_time=0.4)
        self.beat(2)
        raro = Etichetta("raro", pieno=False)
        raro.next_to(nuovo, RIGHT, buff=px(60))
        self.play(raro.entra(), run_time=0.35)
        self.play(Barrato(raro.testo).entra(), run_time=0.4)


class Scena05(ScenaReel):
    """Le barre si muovono appena con «originale», si riordinano con il dettaglio vero."""

    def costruisci(self):
        a = self.area.contenuto
        from manim import RoundedRectangle
        box = RoundedRectangle(corner_radius=px(24), width=px(620), height=px(150), stroke_width=tratto(3),
                               stroke_color=self.cfg.palette.attenuato, fill_color=self.cfg.palette.sfondo, fill_opacity=1)
        linguetta = Etichetta("richiesta", pieno=False)
        carta = VGroup(box, linguetta.next_to(box, UP, buff=px(14)).align_to(box, LEFT))
        a.metti(carta, "alto", "sinistra", buff_px=20)
        cl = Classifica(CANDIDATE, larghezza_px=560)
        cl.next_to(carta, DOWN, buff=px(60), aligned_edge=LEFT)
        self.add(carta, cl)
        self.beat(0)
        t1 = Token("originale")
        t1.next_to(carta, RIGHT, buff=px(40))
        self.play(FadeIn(t1), run_time=0.3)
        self.play(t1.animate.move_to(box.get_left() + RIGHT * (t1.width / 2 + px(28))), run_time=0.5)
        self.play(cl.aggiorna([0.46, 0.24, 0.08], riordina=False), run_time=0.6)
        self.beat(1)
        t2 = Token("fotocopiatrice", colore=self.cfg.palette.accento)
        t2.next_to(cl, RIGHT, buff=px(30))
        mano = Indice()
        mano.next_to(t2, DOWN, buff=px(6))
        self.play(FadeIn(t2), mano.entra(), run_time=0.4)
        self.play(mano.trascina(t2, box.get_right() + LEFT * (t2.width / 2 + px(28))), run_time=0.8)
        self.play(FadeOut(mano, shift=DOWN * 0.2), run_time=0.25)
        self.play(cl.aggiorna([0.12, 0.20, 0.62]), run_time=0.8)
        self.beat(2)
        self.play(cl.scegli(2), run_time=0.4)


class Scena06(ScenaReel):
    """Deroga (CAPTION: alto): nella cornice c'è la chat, e lì il testo è il contenuto."""

    def costruisci(self):
        cornice = CorniceSchermo(self.area.schermo)
        eti = Etichetta("adesso")
        eti.next_to(cornice, DOWN, buff=px(24)).align_to(cornice, LEFT)
        self.add(cornice)
        self.play(eti.entra(), run_time=0.4)
        self.beat(1)
        quadro = self.area.schermo
        alto = quadro.y1 - quadro.altezza * 0.22
        riquadro = VGroup(Line([quadro.x0 + px(40), alto, 0], [quadro.x1 - px(40), alto, 0],
                               stroke_color=self.cfg.palette.accento, stroke_width=tratto(6)))
        self.play(Create(riquadro), run_time=0.5)


class Scena07(ScenaReel):
    """Chiusura: il messaggio e le tre tessere da mettere nella richiesta."""

    def costruisci(self):
        a = self.area.contenuto
        m = Messaggio("Non chiederle di essere originale: ==cambia quello che viene prima==", larghezza_px=860)
        a.metti(m, "alto", "sinistra", buff_px=20)
        self.play(m.per_righe(), run_time=1.0)
        self.beat(1)
        tessere = VGroup(*[tessera(self, s, 300) for s in ("dettaglio", "vincolo", "scarto")]).arrange(DOWN, buff=px(18))
        tessere.next_to(m, DOWN, buff=px(44)).align_to(m, LEFT)
        self.play(FadeIn(tessere, shift=UP * 0.15), run_time=0.7)
        cta = Etichetta("Salva per il prossimo biglietto")
        a.metti(cta, "basso", "sinistra", buff_px=10)
        self.play(cta.entra(), run_time=0.4)
