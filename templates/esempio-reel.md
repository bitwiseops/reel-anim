---
titolo: Generativa non vuol dire creativa
slug: esempio-reel
data_creazione: 2026-09-13
stato: animato
formato: reel
tipo: pillola
pilastro: come funziona
messaggio_centrale: L'IA sceglie a ogni passo una delle parole più probabili; per avere una frase nuova non chiedere originalità, cambia quello che viene prima.
idea:
---

# Generativa non vuol dire creativa

<!--
Esempio completo della grammatica (vedi templates/reel.md): 7 scene, una per tipo, e i componenti della libreria
usati in contenuti/animazioni/esempio-reel.py (una classe ScenaNN per scena).
Prova senza presentatore:  uv run reel monta templates/esempio-reel.md --prova --anteprima
Il b-roll della scena 6 è un'immagine versionata in contenuti/media/esempio-reel/.

Il reel si guarda muto (docs/regole-editoriali.md §1): l'animazione non contiene frasi da leggere, a schermo restano
numeri, etichette di una parola e figure. La scena 6 è l'esempio della **deroga** (`CAPTION: alto`). Per mostrare i
componenti `Titolo` e `Messaggio`, qui l'hook è animato (`RIQUADRO: no`) e la chiusura ha grafica sopra il volto
pieno: nei reel veri apertura e chiusura sono solo il presentatore con le caption (docs/regole-editoriali.md §4).
-->

## Scena 1 [hook]
TITOLO: Generativa non vuol dire creativa
SOTTOTITOLO: Vuol dire ==probabile==
VOCE: L'IA scrive quello che ti aspetti?
VOCE: Guarda che generativa non vuol dire creativa.
VOCE: Vuol dire che sceglie il probabile.
ANIMAZIONE: Il titolo è già in scena al primo fotogramma (è quello che vede chi scorre) e sale appena.
ANIMAZIONE: «Creativa» viene barrata appena detta.
ANIMAZIONE: Sotto compare «probabile» in accento.
RIQUADRO: no

## Scena 2 [spiegazione]
VOCE: Quando l'IA scrive, va avanti una parola alla volta.
VOCE: A ogni passo si mette in fila le parole che potrebbero venire dopo.
VOCE: E ne prende una tra le più ==probabili==.
ANIMAZIONE: In alto una riga cresce una tessera alla volta: tre tessere uguali, senza parole dentro, e uno spazio vuoto che aspetta.
ANIMAZIONE: Sotto lo spazio vuoto scendono tre barre di lunghezza diversa, una per candidata, con l'etichetta di una parola ciascuna (esempio dichiarato).
ANIMAZIONE: La barra più lunga si accende e la sua tessera vola nello spazio vuoto della riga.
FIGURA: una riga che cresce una tessera alla volta, e ogni volta vince la barra più lunga.
TESTO: esempio

## Scena 3 [spiegazione]
VOCE: Poi rifà la stessa scelta, parola dopo parola.
VOCE: E il biglietto per Marco viene fuori così.
VOCE: Se l'hai finito in testa prima di lei, era semplicemente il più probabile.
ANIMAZIONE: La riga continua da sola, veloce: le tessere si aggiungono a raffica e un contatore sale con loro.
ANIMAZIONE: La riga finita diventa il blocco di un biglietto, righe piene senza parole leggibili.
ANIMAZIONE: Un riquadro accento incornicia il blocco e il contatore si ferma.
FIGURA: la stessa scelta ripetuta molte volte produce un testo intero.
TESTO: 14

## Scena 4 [spiegazione]
VOCE: A ogni bivio prende quasi sempre la strada più battuta.
VOCE: Quindi il testo è nuovo, nel senso che nessuno l'ha scritto così.
VOCE: Ma ==raro== no, non lo è.
ANIMAZIONE: Dal blocco parte un bivio a tre rami, uno spesso e due sottili (esempio); un punto in accento percorre il ramo spesso.
ANIMAZIONE: Sotto il ramo spesso entra l'etichetta «nuovo».
ANIMAZIONE: Accanto entra «raro» e una barra lo taglia.
FIGURA: tre strade di spessore diverso, e il punto prende sempre la più larga.
TESTO: nuovo
TESTO: raro

## Scena 5 [spiegazione]
VOCE: Se le chiedi di essere originale, cambia poco o niente.
VOCE: Se invece le dai un dettaglio vero, tipo Marco che litigava con la fotocopiatrice, cambia tutto.
VOCE: E adesso la frase più probabile è un'altra.
ANIMAZIONE: Torna la colonna delle tre barre; sopra, una carta vuota con la sola linguetta «richiesta». Una tessera «originale» entra nella carta e le barre si muovono appena.
ANIMAZIONE: Un puntatore prende una tessera «fotocopiatrice» e la trascina dentro la carta: le barre si riordinano.
ANIMAZIONE: La barra che ora è in testa si accende.
FIGURA: la stessa colonna di barre cambia ordine solo quando entra il dettaglio vero.
TESTO: richiesta

## Scena 6 [schermo]
SCHERMO: chat-fotocopiatrice.png
CAPTION: alto
VOCE: Ecco il biglietto che scrive adesso.
VOCE: Però la parte nuova non l'ha inventata lei, l'hai messa tu, prima.
ANIMAZIONE: Nella cornice la chat con la richiesta e il biglietto nuovo; sopra, l'etichetta «adesso».
ANIMAZIONE: Un riquadro accento sulla richiesta, dove sta il dettaglio vero.
FIGURA: la richiesta che contiene il dettaglio e il biglietto che ne esce.
TESTO: adesso
RIQUADRO: alto-destra

## Scena 7 [chiusura]
MESSAGGIO: Non chiederle di essere originale: ==cambia quello che viene prima==.
CTA: Salva per il prossimo biglietto
VOCE: Non chiederle di essere originale.
VOCE: Cambia quello che viene prima.
ANIMAZIONE: Il messaggio entra in alto e sotto restano tre tessere, una per ogni cosa da dare: un dettaglio, un vincolo, uno scarto.
ANIMAZIONE: In fondo la CTA a pillola; l'ultimo fotogramma resta pulito.
FIGURA: tre tessere da mettere nella richiesta, e il messaggio sopra.

## Note di produzione
<!-- Scelte di regia, b-roll da girare, dubbi. Non renderizzate. -->
- **Il reel si guarda muto**: nessuna frase a schermo. Le parole dentro le tessere e le etichette delle barre sono
  di una parola sola; i numeri (il contatore, le lunghezze delle barre) non contano come testo.
- Nessun numero reale: tutte le barre sono esempi dichiarati (l'etichetta «esempio» sotto la colonna).
- **Deroga alla fascia delle caption: una sola scena, la 6** (`CAPTION: alto`). Lì il contenuto *è* il testo della
  chat: la fascia va in cima e il fondo resta all'immagine. Il limite è due scene per reel.
- La scena 6 in produzione vera è uno screen recording della chat; qui è un'immagine statica di esempio.

## Revisione tecnica
<!-- Compilata dal revisore-tecnico. -->
- «Una delle più probabili» e non «la più probabile»: il modello campiona (temperatura), non prende sempre la prima.
  A schermo le barre lo dicono: la più lunga vince, ma le altre restano in campo.
- Il modello lavora a token, non a parole: semplificazione accettabile per il pubblico.
- «Sii originale» sposta poco la distribuzione, non zero: la voce dice «poco o niente» e le barre si muovono appena.
- Le tre barre e i tre rami sono **esempi dichiarati**, non misure: l'etichetta «esempio» resta a schermo finché
  restano loro.

## Note di animazione
<!-- Compilate dall'animatore: beat scelti, tempi Manim, cose che non stanno. -->
- Componenti usati: `Titolo`, `Barrato`, `Etichetta`, `Classifica` (barre con etichetta di una parola), `Sagome`
  (il biglietto che si vede ma non si legge), `ContatoreScorre`, `Indice` (il gesto che trascina), `Carta` con la
  sola linguetta, `CorniceSchermo`, `Messaggio`, `Didascalia`.
- La scena 7 è a volto pieno (default della chiusura), con le caption: la grafica va sopra, su fondo trasparente.

## Pacchetto social
**Caption Reel:**
**Hashtag:**
**Alt text cover:**
**Variante LinkedIn (post testuale):**
