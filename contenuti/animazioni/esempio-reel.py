"""Animazioni dell'esempio «Generativa non vuol dire creativa» (templates/esempio-reel.md).

Una classe ScenaNN(ScenaReel) per scena. I testi a schermo vengono dalla sceneggiatura (self.scena) quando ci sono;
i numeri delle barre sono esempi dichiarati. Tempi: self.beat(i) aspetta l'inizio della frase i della VOCE,
self.fino_a(f) una frazione della scena; la scena dura esattamente quanto la clip (o la voce di prova).
"""
from manim import DOWN, LEFT, RIGHT, UP, AnimationGroup, Create, FadeIn, FadeOut, FadeTransform, LaggedStart, VGroup, VMobject

from tools.anim.base import ScenaReel, area_px
from tools.anim.componenti import (Barrato, Carta, Classifica, Contatore, CorniceSchermo, Etichetta, Evidenzia, Frase,
                                   Freccia, Lista, Messaggio, Piede, Titolo, Token, testo, tratto)
from tools.anim.misure import px


class Scena01(ScenaReel):
    """Hook: il titolo entra, «creativa» viene barrata, compare «probabile»."""

    def costruisci(self):
        a = self.area.contenuto
        titolo = Titolo(self.scena["titolo"])
        sotto = Titolo(self.scena["sottotitolo"])
        a.metti(VGroup(titolo, sotto).arrange(DOWN, aligned_edge=LEFT, buff=px(90)), "centro", "sinistra")
        self.play(titolo.per_righe(), run_time=1.0)
        self.fino_a(0.3)
        parola = titolo.parola("creativa")
        self.play(Barrato(parola).entra(), parola.animate.set_opacity(0.45), run_time=0.4)
        self.beat(1)
        self.play(sotto.per_righe(lag=0.3), run_time=0.6)


class Scena02(ScenaReel):
    """Una parola alla volta: la frase si compone, la colonna delle candidate, la prima vola in coda."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        et = Etichetta(self.scena["testo"][0], pieno=False)
        a.metti(et, "alto", "sinistra")
        frase = Frase(ancora=et.get_corner(LEFT + DOWN) + DOWN * px(70))
        self.play(et.entra(), run_time=0.4)
        for p in ("Caro", "Marco,", "oggi"):
            self.play(frase.aggiungi(p), run_time=0.35)

        self.beat(1)
        domanda = testo("prossima parola?", "caption", colore=col.attenuato)
        cl = Classifica([("si", 0.62), ("è", 0.21), ("ti", 0.09)], larghezza_px=760)
        gruppo = VGroup(domanda, cl).arrange(DOWN, aligned_edge=LEFT, buff=px(36))
        gruppo.next_to(frase.token, DOWN, buff=px(110), aligned_edge=LEFT)
        self.play(FadeIn(domanda), cl.entra(), run_time=1.4)

        self.beat(2)
        self.play(cl.scegli(0), run_time=0.4)
        self.play(frase.aggiungi(cl.token(0, colore=col.accento), da=cl.barre[0].etichetta), run_time=0.7)


class Scena03(ScenaReel):
    """La frase continua da sola con il contatore delle scelte; diventa il biglietto banale, incorniciato."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        frase = Frase(["Caro", "Marco,", "oggi", "si"], ancora=[a.x0, a.y1 - px(20), 0])
        frase.token[-1].box.set_stroke(col.accento)
        cont = Contatore(4, "parole scelte")
        a.metti(cont, "basso", "sinistra", buff_px=20)
        self.add(frase)
        self.play(cont.entra(), run_time=0.3)
        parole = "chiude un capitolo e se ne apre uno nuovo.".split()
        # contatore 0,3 s + una play per parola + respiro, tutto dentro il beat 0 (a fotogrammi interi)
        passo = self.arrotonda((self.durata_beat(0) - self.ANTICIPO_S - 0.7) / len(parole))
        for k, p in enumerate(parole, start=5):
            self.play(frase.aggiungi(p), cont.a(k), run_time=passo)

        self.beat(1)
        carta = Carta("Biglietto per Marco", ["Caro Marco, oggi si chiude un capitolo e se ne apre uno nuovo."])
        a.metti(carta, "centro", "sinistra").shift(UP * px(60))
        self.play(FadeOut(frase), FadeOut(cont), carta.entra(), run_time=0.7)

        self.beat(2)
        cornice = Evidenzia(carta.righe, buff=px(18))
        et = Etichetta(self.scena["testo"][0]).next_to(carta, DOWN, buff=px(60), aligned_edge=LEFT)
        self.play(Create(cornice), et.entra(), run_time=0.6)


class Scena04(ScenaReel):
    """I bivi: tre continuazioni, il ramo più spesso è la strada battuta; «nuovo» sì, «raro» barrato."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        radice = Token("si chiude un capitolo")
        a.metti(radice, "alto", "sinistra", buff_px=20)
        rami = [("e se ne apre uno nuovo", 16), ("ma non un'amicizia", 4), ("della nostra storia", 4)]
        figli = VGroup(*[Token(s) for s, _ in rami]).arrange(DOWN, aligned_edge=LEFT, buff=px(44))
        figli.next_to(radice, DOWN, buff=px(70)).align_to(radice, LEFT).shift(RIGHT * px(150))
        x0, y0 = radice.get_left()[0] + px(70), radice.get_bottom()[1]
        linee = VGroup(*[
            VMobject(stroke_color=col.attenuato, stroke_width=tratto(sp)).set_points_as_corners(
                [[x0, y0, 0], [x0, f.get_center()[1], 0], [f.get_left()[0] - px(6), f.get_center()[1], 0]])
            for f, (_, sp) in zip(figli, rami)])
        nota = testo("esempio", "piede", colore=col.attenuato).next_to(figli, DOWN, buff=px(40), aligned_edge=LEFT)
        self.play(FadeIn(radice, shift=UP * 0.2), run_time=0.4)
        self.play(LaggedStart(*[AnimationGroup(Create(l), FadeIn(f, shift=RIGHT * 0.2), lag_ratio=0.5)
                                for l, f in zip(linee, figli)], lag_ratio=0.35), FadeIn(nota), run_time=1.5)
        self.play(linee[0].animate.set_stroke(col.accento), figli[0].evidenzia(),
                  *[l.animate.set_stroke(opacity=0.45) for l in linee[1:]], run_time=0.5)

        self.beat(1)
        nuovo = Etichetta(self.scena["testo"][0], colore=col.terziario)
        raro = Etichetta(self.scena["testo"][1], colore=col.attenuato, pieno=False)
        a.metti(VGroup(nuovo, raro).arrange(RIGHT, buff=px(40)), "basso", "sinistra", buff_px=40)
        self.play(nuovo.entra(), run_time=0.4)

        self.beat(2)
        self.play(raro.entra(), run_time=0.3)
        self.play(Barrato(raro.testo).entra(), run_time=0.35)


class Scena05(ScenaReel):
    """La carta «contesto»: «sii originale» sposta appena le barre, la fotocopiatrice le riordina."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        carta = Carta(self.scena["testo"][0], ["Due righe per il biglietto di Marco."])
        a.metti(carta, "alto", "sinistra")
        dopo = testo("dopo «Caro Marco,»", "caption", colore=col.attenuato)
        cl = Classifica([("oggi si chiude un capitolo", 0.58), ("grazie di tutto", 0.26), ("la fotocopiatrice", 0.03)],
                        larghezza_px=620)
        a.metti(VGroup(dopo, cl).arrange(DOWN, aligned_edge=LEFT, buff=px(28)), "basso", "sinistra")
        self.play(carta.entra(), run_time=0.5)
        self.play(FadeIn(dopo), cl.entra(), run_time=1.2)
        self.fino_a(0.15)
        self.play(carta.aggiungi_riga("Sii originale."), run_time=0.6)
        self.play(cl.aggiorna([0.55, 0.28, 0.05], riordina=False), run_time=0.6)

        self.beat(1)
        self.play(carta.aggiungi_riga("Marco ha passato una vita a litigare con la fotocopiatrice."), run_time=0.7)
        self.play(cl.aggiorna([0.10, 0.12, 0.66]), run_time=1.0)

        self.beat(2)
        x = cl.barre[2].pista.get_right()[0]
        freccia = Freccia([x + px(80), carta.box.get_bottom()[1], 0], [x + px(20), cl.barre[2].get_center()[1], 0],
                          colore=col.accento)
        self.play(cl.scegli(2), freccia.entra(), run_time=0.6)


class Scena06(ScenaReel):
    """Schermo: la chat con il nuovo biglietto; l'etichetta passa da «contesto nuovo» a «l'hai messa tu»."""

    def costruisci(self):
        col, sch = self.cfg.palette, self.area.schermo
        cornice = CorniceSchermo(sch)
        alto_safe = self.cfg.frame_height / 2 - px(self.cfg.dati["safe_area"]["alto"])
        et = Etichetta(self.scena["testo"][0])
        et.move_to([sch.x0 + et.width / 2, (alto_safe + sch.y1) / 2, 0])
        # la bolla con il dettaglio vero: px nell'immagine (li stampa genera_chat.py) + dove è posata ([schermo] x, y)
        x, y = self.cfg.dati["schermo"]["x"], self.cfg.dati["schermo"]["y"]
        bolla = area_px(self.cfg, x + 256, y + 328, x + 860, y + 492).rettangolo(stroke_opacity=0, fill_opacity=0)
        self.play(cornice.entra(), et.entra(), run_time=0.6)

        self.beat(1)
        et2 = Etichetta(self.scena["testo"][1], colore=col.terziario).move_to(et, aligned_edge=LEFT)
        self.play(Create(Evidenzia(bolla, buff=px(12))), FadeTransform(et, et2), run_time=0.6)


class Scena07(ScenaReel):
    """Chiusura: messaggio, tre modi di cambiare quello che viene prima, CTA."""

    def costruisci(self):
        a = self.area.contenuto
        msg = Messaggio(self.scena["messaggio"])
        a.metti(msg, "alto", "sinistra")
        lista = Lista(["un dettaglio vero", "un vincolo", "scarta le prime idee"])
        lista.next_to(msg, DOWN, buff=px(70), aligned_edge=LEFT)
        cta = Etichetta(self.scena["cta"])
        a.metti(cta, "basso", "sinistra")
        piede = Piede(a)
        self.play(msg.entra(), run_time=1.2)

        self.beat(1)
        self.play(lista.entra_una_alla_volta(), run_time=1.5)

        self.beat(2)
        self.play(cta.entra(), *([FadeIn(piede)] if len(piede) else []), run_time=0.5)
