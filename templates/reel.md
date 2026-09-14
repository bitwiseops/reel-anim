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
  Tipi: hook (Scena 1, obbligatoria) | spiegazione (default) | schermo (b-roll / screen recording) | chiusura (ultima, obbligatoria)

  VOCE: frase             ripetibile: ogni riga è una frase detta a camera dal presentatore (= un beat dell'animazione)
  ANIMAZIONE: prosa       ripetibile: cosa si vede; una riga sola, oppure una per frase della VOCE (beat i ↔ frase i)
  TESTO: etichetta        ripetibile (max 4, ≤ 4 parole): parole chiave che compaiono a schermo
  TITOLO: / SOTTOTITOLO:  solo hook (titolo ≤ 10 parole: regge da solo)
  MESSAGGIO: / CTA:       solo chiusura (messaggio ≤ 25 parole, CTA una riga)
  SCHERMO: file.mp4       scena schermo (o spiegazione): file in contenuti/media/<slug>/ mostrato nella cornice
  RIQUADRO: no|si|posizione   riquadro del presentatore (default: no nell'hook, si altrove); posizioni: basso-destra basso-sinistra alto-destra alto-sinistra

Inline: ==evidenzia== (una per scena: la parola che conta, in colore accento), **grassetto**.
Limiti: 6-8 scene (min 5, max 9); VOCE ≤ 35 parole per scena (hook ≤ 15), max 4 righe VOCE per scena;
  ogni scena 2,5-14 s stimati; reel 30-60 s. La VOCE è parlato: frasi corte, una cosa per frase.
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
TESTO: 

## Scena 3 [spiegazione]
VOCE: 
ANIMAZIONE: 

## Scena 4 [schermo]
SCHERMO: 
VOCE: 
ANIMAZIONE: 

## Scena 5 [spiegazione]
VOCE: 
ANIMAZIONE: 

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
