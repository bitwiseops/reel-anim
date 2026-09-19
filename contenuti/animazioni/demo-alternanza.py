"""Animazioni di «Demo dell'alternanza» (broll/esempi/demo-alternanza.md): banco di prova delle scene [broll].

Le scene 2 e 4 sono [broll] (filmato a tutto schermo col riquadro sopra): non hanno una classe. Le scene 3 e 5
arrivano da uno stacco su un filmato, quindi il loro fotogramma 0 è già pieno (self.add prima di ogni animazione) e
non continua nulla da una scena precedente; l'ultimo fotogramma delle scene 1 e 3 è completo e fermo.
I numeri delle barre sono esempi dichiarati (nota «esempio: numeri inventati» della Classifica).
"""
from manim import DOWN, LEFT, PI, UP, FadeIn, FadeOut, LaggedStart, VGroup, rate_functions

from tools.anim.base import ScenaReel
from tools.anim.componenti import Classifica, Etichetta, Frase, Messaggio, Titolo, testo
from tools.anim.diagrammi import Confronto
from tools.anim.misure import px

ARCO = PI / 2   # il cartellino scelto vola in coda alla frase girando a destra di «prossima parola?», non sopra


class Scena01(ScenaReel):
    """Hook: il titolo è già in scena al primo fotogramma e sale appena; sotto compare «quella di tutti»."""

    def costruisci(self):
        a = self.area.contenuto
        titolo = Titolo(self.scena["titolo"])
        sotto = Titolo(self.scena["sottotitolo"])
        a.metti(VGroup(titolo, sotto).arrange(DOWN, aligned_edge=LEFT, buff=px(90)), "centro", "sinistra")
        titolo.shift(DOWN * px(30))
        self.add(titolo)                                  # la copertina di chi scorre: mai un primo fotogramma vuoto
        self.play(titolo.animate.shift(UP * px(30)), run_time=0.5)

        self.beat(1)                                      # «Ti è arrivata quella che arriva a tutti.»
        self.play(sotto.per_righe(lag=0.3), run_time=min(0.8, 0.4 * self.durata_beat(1)))


class Scena03(ScenaReel):
    """Una parola alla volta: la frase e la classifica sono già in scena allo stacco; «in» viene scelta e vola in
    coda, la classifica si rifà per la parola dopo, e sulla seconda frase vince «merito»: la più probabile."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        frase = Frase(["Buongiorno,", "le", "scrivo"], ancora=[a.x0, a.y1, 0])
        domanda = testo("prossima parola?", "caption", colore=col.attenuato)
        cl = Classifica([("in", 0.64), ("per", 0.21), ("perché", 0.06)], larghezza_px=620)
        cl2 = Classifica([("merito", 0.58), ("risposta", 0.27), ("quanto", 0.07)], larghezza_px=620, esempio=False)
        et = Etichetta(self.scena["testo"][0])
        colonna = VGroup(domanda, cl).arrange(DOWN, aligned_edge=LEFT, buff=px(36))
        # l'impaginazione si misura sulla frase finita (due parole in più, su una riga sola), così niente si sposta
        piena = Frase(["Buongiorno,", "le", "scrivo", "in", "merito"])
        blocco = VGroup(piena, colonna, et).arrange(DOWN, aligned_edge=LEFT, buff=px(80))
        a.metti(blocco, "centro", "sinistra")
        frase.posiziona(piena.token.get_corner(UP + LEFT))
        cl2.barre.move_to(cl.barre, aligned_edge=UP + LEFT)
        self.add(frase, domanda, cl)                      # fotogramma 0 pieno: si arriva da uno stacco sul filmato

        d0 = self.durata_beat(0)                          # «Perché l'IA va avanti una parola alla volta.»
        self.wait(self.arrotonda(0.12 * d0))
        self.play(cl.scegli(0), run_time=self.arrotonda(min(0.4, 0.15 * d0)))
        self.play(frase.aggiungi(cl.token(0, colore=col.accento), da=cl.barre[0].etichetta, path_arc=ARCO),
                  run_time=self.arrotonda(min(0.6, 0.22 * d0)), rate_func=rate_functions.ease_out_cubic)
        # la classifica si rifà per la parola dopo: prima escono le voci vecchie, poi entrano le nuove (mai incrociate)
        self.play(*[FadeOut(b) for b in cl.barre], frase.token[-1].box.animate.set_stroke(col.attenuato),
                  run_time=self.arrotonda(min(0.3, 0.1 * d0)))
        self.play(LaggedStart(*[b.cresci() for b in cl2.barre], lag_ratio=0.25),
                  run_time=self.arrotonda(min(0.8, 0.28 * d0)))

        self.beat(1)                                      # «E a ogni passo prende una tra le più probabili.»
        d1 = self.durata_beat(1)
        self.wait(self.arrotonda(0.2 * d1))
        self.play(cl2.scegli(0), et.entra(), run_time=self.arrotonda(min(0.5, 0.18 * d1)))
        self.play(frase.aggiungi(cl2.token(0, colore=col.accento), da=cl2.barre[0].etichetta, path_arc=ARCO),
                  run_time=self.arrotonda(min(0.7, 0.25 * d1)), rate_func=rate_functions.ease_out_cubic)


class Scena05(ScenaReel):
    """Confronto in colonna: allo stacco ci sono già la richiesta «Sii originale.» e, sotto, la carta vuota della tua
    richiesta; la prima viene bocciata, la seconda si riempie con il dettaglio vero (nome e numero in accento)."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        et = Etichetta(self.scena["testo"][0], pieno=False)
        cf = Confronto("Scrivimi la mail di candidatura.\nSii originale.",
                       "Scrivimi la mail di candidatura.\nDa Acme Arredi gestivo 40 ordini al giorno.",
                       titolo_prima="la richiesta di tutti", titolo_dopo="la tua richiesta")
        a.metti(VGroup(et, cf).arrange(DOWN, aligned_edge=LEFT, buff=px(60)), "centro", "sinistra")
        dopo = cf.dopo
        dopo.box.set_stroke(opacity=0.4)
        self.add(et, cf.prima, dopo.box, dopo.titolo)     # fotogramma 0 pieno: si arriva da uno stacco sul filmato

        d0 = self.durata_beat(0)                          # «Allora non chiederle di essere originale.»
        self.wait(self.arrotonda(0.35 * d0))
        self.play(cf.boccia(), run_time=self.arrotonda(min(0.9, 0.35 * d0)))

        self.beat(1)                                      # «Dalle quello che sai solo tu, un numero, un nome, un dettaglio.»
        t1, d1 = self.inizi_frasi[1], self.durata_beat(1)
        self.play(cf.freccia.entra(), dopo.box.animate.set_stroke(opacity=1),  FadeIn(dopo.righe, shift=UP * 0.15), run_time=self.arrotonda(min(1.0, 0.3 * d1)))
        riga = dopo.righe[0]
        self.attendi_fino(t1 + 0.48 * d1)                 # «…un numero,»
        self.play(riga.parola("40 ordini").animate.set_color(col.accento), run_time=0.3)
        self.attendi_fino(t1 + 0.66 * d1)                 # «…un nome,»
        self.play(riga.parola("Acme Arredi").animate.set_color(col.accento), run_time=0.3)


class Scena06(ScenaReel):
    """Chiusura: il messaggio entra una riga alla volta, «Tu sì.» in accento sulla sua frase, poi la CTA."""

    def costruisci(self):
        a = self.area.contenuto
        msg = Messaggio(self.scena["messaggio"], cta=self.scena["cta"])
        a.metti(msg, "centro", "sinistra")
        tu = msg.parola("Tu sì.")
        resto = [g for r in msg.righe for g in r.glifi if g not in tu.submobjects]
        self.play(FadeIn(VGroup(*resto), shift=UP * 0.2), run_time=self.arrotonda(min(0.7, 0.5 * self.durata_beat(0))))

        # «Tu sì.»: con la voce di prova restano ~0,85 s fino alla fine della scena. Un solo passaggio, agganciato
        # all'inizio del beat: la battuta e, mezzo tempo dopo, la CTA; il resto è l'ultimo fotogramma fermo.
        self.beat(1)
        self.play(LaggedStart(FadeIn(tu, shift=UP * 0.2), FadeIn(msg.cta, scale=0.85), lag_ratio=0.4),
                  run_time=self.arrotonda(min(0.6, 0.7 * self.durata_beat(1))))
