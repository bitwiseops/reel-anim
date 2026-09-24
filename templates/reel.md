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
GRAMMATICA (una riga = un elemento; dentro una Scena non è ammesso altro): docs/sceneggiatura.md.
Verifica sempre con:  uv run reel valida <questo file>   (limiti in tools/reel/validate.py::LIMITI; stampa la durata
  stimata di ogni scena e del reel). Regole del presentatore: docs/regole-editoriali.md.

  ## Scena N [tipo, durata=Ns, transizione=taglio|dissolvenza]   N consecutivo da 1; il primo flag è il tipo
  Tipi: hook (Scena 1, obbligatoria) | spiegazione (default) | schermo (materiale nella finestra, con la grafica intorno) | chiusura (ultima, obbligatoria)
        broll (filmato a tutto schermo col riquadro sopra, senza grafica e senza TESTO: non si scrive a mano, lo mette `broll scrivi`)

  VOCE: parlato           ripetibile: ogni riga è un pezzo di parlato detto a camera (= un beat dell'animazione), non per forza una frase chiusa
  ANIMAZIONE: prosa       ripetibile: cosa si vede; una riga sola, oppure una per riga della VOCE (beat i ↔ riga i)
  FIGURA: una riga        obbligatoria nelle scene animate: cosa si capisce GUARDANDO, senza leggere niente a schermo
  TESTO: etichetta        ripetibile, pochissime parole: numeri, percentuali, una parola chiave. È un extra, non la spiegazione
  CAPTION: no|alto|basso  dove stanno i sottotitoli in questa scena (default: basso; alto = deroga dichiarata)
  TITOLO: / SOTTOTITOLO:  solo hook: il titolo della copertina, regge da solo
  MESSAGGIO: / CTA:       solo chiusura: il testo della caption del post (CTA una riga)
  SCHERMO: file.mp4       scena schermo: file in contenuti/media/<slug>/ mostrato nella cornice; in una scena broll è tutta la tela
  RIQUADRO: pieno|no|si|posizione   riquadro del presentatore; default: pieno in hook e chiusura (lui a tutta tela, con le
                              sole caption), si altrove; posizioni: basso-destra basso-sinistra alto-destra alto-sinistra
                              (default del config: alto-destra, perché il fondo è della fascia delle caption)

IL REEL SI GUARDA MUTO (docs/regole-editoriali.md §1): l'animazione non contiene testo necessario a capire, il concetto
  lo porta la figura (riga FIGURA:). Hook e chiusura sono il presentatore a tutta tela: niente ANIMAZIONE né FIGURA.
Inline: ==evidenzia== (una per scena: la parola che conta, in colore accento; vale anche nella caption), **grassetto**.
La VOCE viene dal copione (uv run reel copione <idea>), spezzata in beat alla lettera (docs/sceneggiatura.md §5).
Le durate reali le decidono le clip registrate (contenuti/media/<slug>/scena-NN.mov): uv run reel registra <file>
-->

## Scena 1 [hook]
TITOLO: 
SOTTOTITOLO: 
VOCE: 

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
