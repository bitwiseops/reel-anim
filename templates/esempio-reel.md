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
Esempio completo della grammatica (vedi templates/reel.md): 7 scene, una per tipo, e tutti i componenti della
libreria usati in contenuti/animazioni/esempio-reel.py (una classe ScenaNN per scena).
Prova senza presentatore:  uv run reel monta templates/esempio-reel.md --prova --anteprima
Il b-roll della scena 6 è un'immagine versionata in contenuti/media/esempio-reel/.
-->

## Scena 1 [hook]
TITOLO: Generativa non vuol dire creativa
SOTTOTITOLO: Vuol dire ==probabile==
VOCE: L'IA scrive quello che ti aspetti?
VOCE: Generativa non vuol dire creativa.
VOCE: Vuol dire probabile.
ANIMAZIONE: Il titolo è già in scena al primo fotogramma (è quello che vede chi scorre) e sale appena.
ANIMAZIONE: «Creativa» viene barrata appena detta.
ANIMAZIONE: Sotto compare «probabile» in accento.
RIQUADRO: no

## Scena 2 [spiegazione]
VOCE: Quando l'IA scrive, sceglie una parola alla volta.
VOCE: A ogni passo mette in fila le parole possibili.
VOCE: E prende una delle più ==probabili==.
ANIMAZIONE: In alto la frase del biglietto si compone un cartellino alla volta: «Caro», «Marco,», «oggi».
ANIMAZIONE: Sotto compare la colonna delle candidate con le barre (esempio): «si», «è», «ti».
ANIMAZIONE: La prima si accende e vola in coda alla frase.
TESTO: una parola alla volta

## Scena 3 [spiegazione]
VOCE: Poi rifà la scelta, parola dopo parola.
VOCE: E il biglietto per Marco esce così.
VOCE: Se l'hai finito in testa prima di lei, era il più probabile.
ANIMAZIONE: La frase continua da sola, veloce, e un contatore conta le scelte.
ANIMAZIONE: Arriva la frase intera: «oggi si chiude un capitolo e se ne apre uno nuovo».
ANIMAZIONE: Un riquadro accento la incornicia, con l'etichetta «la più probabile».
TESTO: la più probabile

## Scena 4 [spiegazione]
VOCE: A ogni bivio prende la strada più battuta.
VOCE: Il testo è nuovo: nessuno l'ha scritto così.
VOCE: Ma ==raro==, no.
ANIMAZIONE: Da «si chiude un capitolo» partono tre rami (esempio): «e se ne apre uno nuovo» spesso, «ma non un'amicizia» e «della nostra storia» sottili; il ramo spesso si accende.
ANIMAZIONE: In basso compare l'etichetta «nuovo».
ANIMAZIONE: Accanto, «raro» viene barrato.
TESTO: nuovo
TESTO: raro

## Scena 5 [spiegazione]
VOCE: Chiederle di essere originale non cambia quasi niente.
VOCE: Un dettaglio vero invece sì: Marco litigava con la fotocopiatrice.
VOCE: Adesso la più probabile è un'altra frase.
ANIMAZIONE: Una carta «contesto» con la richiesta del biglietto e, sotto, le candidate con le barre (esempio); entra la riga «Sii originale.» e le barre si muovono appena.
ANIMAZIONE: Entra la riga sulla fotocopiatrice e le barre si riordinano.
ANIMAZIONE: In testa ora c'è «la fotocopiatrice», in accento.
TESTO: contesto

## Scena 6 [schermo]
SCHERMO: chat-fotocopiatrice.png
VOCE: Ecco il biglietto che scrive adesso.
VOCE: La parte nuova non l'ha inventata lei: l'hai messa tu, prima.
ANIMAZIONE: Nella cornice la chat con la richiesta e il nuovo biglietto; sopra, l'etichetta «contesto nuovo».
ANIMAZIONE: Un riquadro accento sulla richiesta con il dettaglio vero; l'etichetta diventa «l'hai messa tu».
TESTO: contesto nuovo
TESTO: l'hai messa tu
RIQUADRO: alto-destra

## Scena 7 [chiusura]
MESSAGGIO: Non chiederle di essere originale: ==cambia quello che viene prima==.
CTA: Salva per il prossimo biglietto
VOCE: Non chiederle di essere originale.
VOCE: Dalle un dettaglio vero, un vincolo, uno scarto.
VOCE: Cambia quello che viene prima.
ANIMAZIONE: Il messaggio entra in alto.
ANIMAZIONE: Sotto, tre voci una alla volta: «un dettaglio vero», «un vincolo», «scarta le prime idee».
ANIMAZIONE: In fondo la CTA a pillola.

## Note di produzione
<!-- Scelte di regia, b-roll da girare, dubbi. Non renderizzate. -->
- Nessun numero reale: tutte le barre sono esempi dichiarati (etichetta «esempio: numeri inventati» sotto la colonna).
- La scena 6 in produzione vera è uno screen recording della chat; qui è un'immagine statica di esempio.

## Revisione tecnica
<!-- Compilata dal revisore-tecnico. -->
- «Una delle più probabili» e non «la più probabile»: il modello campiona (temperatura), non prende sempre la prima.
- Il modello lavora a token, non a parole: semplificazione accettabile per il pubblico.
- «Sii originale» sposta poco la distribuzione, non zero: la voce dice «quasi niente» e le barre si muovono appena.

## Note di animazione
<!-- Compilate dall'animatore: beat scelti, tempi Manim, cose che non stanno. -->

## Pacchetto social
**Caption Reel:**
**Hashtag:**
**Alt text cover:**
**Variante LinkedIn (post testuale):**
