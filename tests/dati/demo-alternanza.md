---
titolo: Demo dell'alternanza
slug: demo-alternanza
data_creazione: 2026-09-19
stato: sceneggiatura
formato: reel
tipo: pillola
pilastro: come funziona
messaggio_centrale: Sceneggiatura di prova del sottosistema broll, con due scene d'attenzione che vanno a filmato.
idea:
---

# Demo dell'alternanza

<!--
Non è un reel da pubblicare: è il banco di prova di `broll piano → cerca → provini → scegli → rendi`.
Sui reel veri il piano dà — correttamente — zero scene a filmato, perché ogni scena ha qualcosa da
disegnare. Qui le scene 2 e 4 non nominano meccanismi, quantità né figure della libreria: sono scene
d'attenzione, e il piano le propone a filmato.
  uv run broll piano tests/dati/demo-alternanza.md

Il file è versionato **dopo** `broll scrivi`: le scene 2 e 4 sono già [broll] con la loro riga SCHERMO:, che è lo
stato da cui parte l'animatore. I filmati non sono in git (contenuti/media/ è ignorata): su una copia nuova
`uv run broll rendi demo-alternanza` li riscarica e li rifà da contenuti/broll/demo-alternanza/piano.json.
Per rifare il giro da capo: riporta le due scene a [spiegazione], togli le righe SCHERMO: e lancia `broll piano --da-capo`.
-->

## Scena 1 [hook]
TITOLO: Chiedi una mail all'IA
SOTTOTITOLO: E ti arriva ==quella di tutti==
VOCE: Hai chiesto una mail all'IA?
VOCE: Ti è arrivata quella che arriva a tutti.
ANIMAZIONE: Il titolo è già in scena al primo fotogramma e sale appena.
ANIMAZIONE: Sotto compare «quella di tutti» in accento.
RIQUADRO: no

## Scena 2 [broll]
SCHERMO: broll-scena-02.mp4
VOCE: Pensa a chi la riceve, quella mail.
VOCE: È lunedì mattina, ha la casella piena e un caffè che si fredda.
VOCE: Apre la tua e ha già capito come va a finire.
ANIMAZIONE: Una persona alla scrivania davanti al portatile, di mattina, legge la posta con una tazza di caffè accanto.

## Scena 3 [spiegazione]
VOCE: Perché l'IA va avanti una parola alla volta.
VOCE: E a ogni passo prende una tra le più ==probabili==.
ANIMAZIONE: La frase si compone un token alla volta, con la classifica delle candidate e le barre (esempio).
TESTO: la più probabile

## Scena 4 [broll]
SCHERMO: broll-scena-04.mp4
VOCE: Il risultato è una mail educata, ordinata, giusta.
VOCE: Che però potrebbe averla scritta chiunque.
VOCE: E chi legge, di quelle, ne ha già viste una pila.
ANIMAZIONE: Una pila di fogli e lettere tutte uguali su una scrivania, una mano le sfoglia in fretta.

## Scena 5 [spiegazione]
VOCE: Allora non chiederle di essere originale.
VOCE: Dalle quello che sai solo tu, un numero, un nome, un dettaglio.
ANIMAZIONE: Confronto a due colonne: a sinistra il prompt «Sii originale.», a destra il prompt con il dettaglio vero.
TESTO: cambia la richiesta

## Scena 6 [chiusura]
MESSAGGIO: L'IA non ti conosce. ==Tu sì.==
CTA: Provaci con la prossima mail
ANIMAZIONE: Il messaggio entra una riga alla volta, «Tu sì.» in accento; sotto la CTA.
VOCE: L'IA non ti conosce.
VOCE: Tu sì.
