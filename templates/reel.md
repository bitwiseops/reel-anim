---
titolo: 
slug: 
data_creazione: 
stato: sceneggiatura   # sceneggiatura | rivisto | animato | montato | approvato | pubblicato
formato: reel
tipo: pillola          # pillola | docenza (o quello che il canale prevede)
pilastro: 
messaggio_centrale:    # UNA frase: cosa deve portarsi a casa chi guarda
idea:                  # path del file idea di partenza (opzionale)
---

# {titolo}

<!--
GRAMMATICA (una riga = un elemento; dentro una Scena non è ammesso altro).
Verifica sempre con:  uv run reel valida <questo file>   (stampa la durata stimata di ogni scena e del reel)

  ## Scena N [tipo, durata=Ns, transizione=taglio|dissolvenza]   N consecutivo da 1; il primo flag è il tipo
  Tipi: hook (Scena 1, obbligatoria) | spiegazione (default) | schermo (materiale nella finestra, con la grafica intorno) | chiusura (ultima, obbligatoria)
        broll (filmato a tutto schermo col riquadro sopra, senza grafica e senza TESTO: non si scrive a mano, lo mette `broll scrivi`)

  VOCE: parlato           ripetibile: ogni riga è un pezzo di parlato detto a camera (= un beat dell'animazione), non per forza una frase chiusa
  ANIMAZIONE: prosa       ripetibile: cosa si vede; una riga sola, oppure una per riga della VOCE (beat i ↔ riga i)
  FIGURA: una riga        obbligatoria nelle scene animate: cosa si capisce GUARDANDO, senza leggere niente a schermo
  TESTO: etichetta        ripetibile (max 2, ≤ 2 parole): numeri, percentuali, una parola chiave. È un extra, non la spiegazione
  CAPTION: no|alto|basso  dove stanno i sottotitoli in questa scena (default: basso; nella chiusura: no)
  TITOLO: / SOTTOTITOLO:  solo hook (titolo ≤ 10 parole: regge da solo)
  MESSAGGIO: / CTA:       solo chiusura (messaggio ≤ 12 parole consigliate, 25 al massimo; CTA una riga)
  SCHERMO: file.mp4       scena schermo (o spiegazione): file in contenuti/media/<slug>/ mostrato nella cornice; in una scena broll è tutta la tela
                          nell'hook = apertura a filmato: clip a tutto schermo, presentatore nel riquadro, TITOLO solo in copertina (la mette `broll scrivi`)
  RIQUADRO: no|si|posizione   riquadro del presentatore (default: no nell'hook, si altrove); posizioni: basso-destra basso-sinistra alto-destra alto-sinistra
                              default del config: alto-destra, perché il fondo è della fascia delle caption

IL REEL SI GUARDA MUTO. Nel video ci sono le caption: il parlato scritto, sincronizzato, bruciato nel montaggio dopo
  la registrazione. Chi guarda non può leggere le caption e un testo nell'animazione insieme, quindi **l'animazione
  non contiene testo necessario a capire**: vanno bene numeri, percentuali e parole singole (due solo se sono
  un'espressione sola, come «Fondo Monetario»); non vanno bene le frasi. Il concetto lo porta la figura: quantità,
  gesti, prima/dopo, confronti di forma. Lo dice la riga FIGURA: di ogni scena.

Inline: ==evidenzia== (una per scena: la parola che conta, in colore accento; vale anche nella caption), **grassetto**.
Limiti: 6-8 scene (min 5, max 9); VOCE ≤ 50 parole per scena (hook ≤ 20, chiusura ≤ 18), max 5 righe VOCE per scena;
  TESTO al massimo 2 per scena e ≤ 2 parole (numeri e percentuali non contano);
  ogni scena 2,5-19 s stimati; reel 30-90 s. La VOCE è parlato vero: prima si scrive il monologo come lo si direbbe
  (verbi, connettivi, io/tu), poi lo si spezza in righe; niente titoli in fila, niente «X, sì. Y, no.», niente due
  punti come snodo (docs/sceneggiatura.md §5).
Le durate reali le decidono le clip registrate (contenuti/media/<slug>/scena-NN.mov): uv run reel registra <file>
Ogni beat dell'animazione parte con la sua frase VOCE: istanti esatti nell'anteprima con voce sintetica (una frase
  alla volta) e con le clip di `reel registra`; stimati in proporzione alle parole con clip esterne.
-->

## Scena 1 [hook]
TITOLO: 
SOTTOTITOLO: 
VOCE: 
ANIMAZIONE: 
RIQUADRO: no

## Scena 2 [spiegazione]
VOCE: 
VOCE: 
ANIMAZIONE: 
ANIMAZIONE: 
FIGURA: 
TESTO: 

## Scena 3 [spiegazione]
VOCE: 
ANIMAZIONE: 
FIGURA: 

## Scena 4 [schermo]
SCHERMO: 
VOCE: 
ANIMAZIONE: 
FIGURA: 

## Scena 5 [spiegazione]
VOCE: 
ANIMAZIONE: 
FIGURA: 

## Scena 6 [chiusura]
MESSAGGIO: 
CTA: 
VOCE: 
ANIMAZIONE: 

## Note di produzione
<!-- Scelte di regia, b-roll da girare, dubbi. Non renderizzate. -->

## Revisione tecnica
<!-- Compilata dal revisore-tecnico. -->

## Note di animazione
<!-- Compilate dall'animatore: beat scelti, tempi Manim, cose che non stanno. -->

## Pacchetto social
**Caption Reel:**
**Hashtag:**
**Alt text cover:**
**Variante LinkedIn (post testuale):**
