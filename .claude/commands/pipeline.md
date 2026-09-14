---
description: Porta un reel fino alla prossima fermata (idea → sceneggiatura → revisione → animazione con anteprima)
---
Argomento: $ARGUMENTS

Sei il coordinatore della pipeline dei reel. Esegui UNA tappa e fermati alla fermata successiva: le decisioni le
prende il presentatore. Regole fisse: mai spostare file tra cartelle; mai saltare la revisione tecnica; mai animare
una sceneggiatura con ❌ aperti; le modifiche chieste a una fermata si fanno rilanciando la tappa sullo stesso file
(l'agente riscrive, niente duplicati); in ogni report finale scrivi esplicitamente «prossimo passo: …».

(Bozza funzionale della fase 2: il cruscotto, il db delle decisioni, l'ideatore e il social-strategist arrivano con
la fase 3; la registrazione e il montaggio finale con le fasi 4-5.)

Decidi la tappa dall'argomento:

**Nessun argomento** → elenca idee (`**Stato:**`) e sceneggiature (`stato:`) in `contenuti/`, con il comando per
portare avanti ciascuna.

**Un file in `contenuti/idee/` con `**Stato:** idea`** → tappa «sceneggiatura»:
1. Lancia `sceneggiatore` sull'idea (deve passare `uv run reel valida` senza errori).
2. Con Edit aggiorna l'idea: `**Stato:** sceneggiata` e aggiungi `**Sceneggiatura:** <percorso>` sotto lo stato.
3. Presenta: percorso, scene con tipo e durata stimata e durata del reel (dall'output di `valida`), il titolo
   alternativo proposto, le frasi di cui lo sceneggiatore è meno sicuro. FERMATA 2: il presentatore legge il file.
Se l'idea è già `sceneggiata`, non rifare nulla: indica la sceneggiatura collegata.

**Un file in `contenuti/sceneggiature/`** → in base a `stato:`:
- `sceneggiatura`: lancia `revisore-tecnico`. Con ❌ FERMATI e riporta claim e riformulazioni proposte (prossimo
  passo: lo sceneggiatore o il presentatore correggono, poi si rilancia). Altrimenti prosegui.
- `rivisto` (o dopo la revisione): lancia `animatore`.
- `animato`: non rilanciare nulla, ristampa il report qui sotto.
- `rivisto` o `animato` **con una richiesta di riscrittura** (il presentatore vuole cambiare VOCE, scene o brief):
  rilancia lo `sceneggiatore` sullo stesso file con la richiesta; lo stato torna a `sceneggiatura` e si riparte
  dalla revisione. Avverti che l'animatore dovrà riallineare i `beat(i)` alle righe VOCE nuove e che le clip già
  registrate (`contenuti/media/<slug>/scena-NN.*`) non valgono più: si rifà `monta --prova` e poi `reel registra`.
Report di FERMATA 3 (anteprima): percorso di `reel-9x16.mp4` e di `contact-sheet.png`, durata del reel e durate per
scena (da `report.json`), avvisi residui, ⚠️ aperte della revisione, rapporto dell'animatore (difetti della
libreria, cose che non ci stavano). Prossimo passo per il presentatore: guardare l'anteprima e annotare leggibilità,
tempi e beat; poi la registrazione in presa unica sull'anteprima (`uv run reel registra <file>`) e il montaggio con
le clip vere (`uv run reel monta <file> --anteprima`).

Se l'argomento non rientra in nessun caso (file inesistente, stato imprevisto), dillo.
