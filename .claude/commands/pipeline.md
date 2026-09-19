---
description: Porta un reel fino alla prossima fermata, o con --tutto dallo spunto fino all'anteprima da registrare
argument-hint: <file> [--tutto]
---
Argomenti: $ARGUMENTS (il primo è il file; `--tutto` è facoltativo)

Sei il coordinatore della pipeline dei reel: lanci gli agenti, controlli quello che consegnano e riferisci al
presentatore. Le decisioni le prende lui, alle fermate.

## Regole fisse
- Mai spostare file tra cartelle (lo fa il presentatore). Mai saltare la revisione tecnica. Mai animare una
  sceneggiatura con ❌ aperti.
- Le modifiche chieste a una fermata si fanno rilanciando l'agente sullo stesso file: l'agente riscrive, niente
  duplicati. Le revisioni del presentatore hanno l'ultima parola.
- Gli agenti non toccano `tools/`: un difetto della libreria va nel rapporto.
- Ogni report finisce con «prossimo passo: …».

## Due modalità
- **A fermate** (default). La pipeline si ferma dove serve una decisione del presentatore, non dopo ogni agente:
  FERMATA 1 dopo l'idea, FERMATA 2 dopo la sceneggiatura, FERMATA 3 dopo l'anteprima. Revisione e animazione corrono in
  fila, senza fermata in mezzo.
- **`--tutto`**: nessuna fermata intermedia, dalla partenza fino all'anteprima `--prova` e al report unico. Ci si
  ferma solo se: il revisore lascia un ❌; `uv run reel valida` ha ancora errori dopo due rilanci dello sceneggiatore;
  un agente chiude BLOCKED o NEEDS_CONTEXT; un agente non esiste in questa sessione (gli agenti creati nella sessione
  corrente non sono lanciabili: dillo e proponi di riaprire la sessione). In ogni caso riporta dove ti sei fermato e
  perché.
- La stessa corsa esiste come Workflow deterministico: `.claude/workflows/reel.js` (`args` = il percorso di partenza).

## Da dove si parte
- **Nessun argomento** → elenca spunti (`stato:` in `contenuti/spunti/`), idee (`**Stato:**` in `contenuti/idee/`) e
  sceneggiature (`stato:` in `contenuti/sceneggiature/`), con il comando per portare avanti ciascuno. L'archivio
  (`contenuti/archivio/`) non si elenca. Ricorda come si scrive uno spunto (`contenuti/spunti/README.md`).
- **`contenuti/spunti/…`**: `stato: spunto` → T0. `stato: ideato` → non rifare nulla: indica l'idea (`idea:`).
- **`contenuti/idee/…`**: `**Stato:** idea` → T1. `sceneggiata` → indica la sceneggiatura collegata.
- **`contenuti/sceneggiature/…`**: `sceneggiatura` → T2; `rivisto` → T3; `animato` → ristampa il report (T4).
  `rivisto` o `animato` **con una richiesta di riscrittura** (il presentatore vuole cambiare VOCE, scene o brief) →
  T1 sullo stesso file con la richiesta; lo stato torna a `sceneggiatura`. Avverti che l'animatore dovrà riallineare i
  `beat(i)` alle righe VOCE nuove e che le clip già registrate (`contenuti/media/<slug>/scena-NN.*`) non valgono più.
- Altro (file inesistente, stato imprevisto): dillo e fermati.

## Le tappe
**T0 · idea.** Lancia `ideatore` sullo spunto: scrive l'idea in `contenuti/idee/` e porta lo spunto a `stato: ideato`.
Se chiude NEEDS_CONTEXT, riporta le sue domande e fermati (anche con `--tutto`).
A fermate → FERMATA 1: percorso dell'idea, angolo scelto e scartati, schema narrativo scelto (reel di reelkit e
tecniche), messaggio centrale, hook candidato, richieste da generare, fatti presi dalla fonte da confermare. Prossimo
passo: il presentatore legge e corregge l'idea, poi `/pipeline <idea>`. A fermate T0b si fa all'inizio di T1.

**T0b · uscite vere** (la fai tu, senza agenti). Si fa se le «Note per il reel» dell'idea elencano richieste da
generare e l'idea non ha ancora la riga `**Uscite:**`. Per ogni richiesta, 5 uscite con Opus e 5 con Sonnet, da una
cartella neutra (lo scratchpad, non il repo, così il modello non legge `CLAUDE.md`):
`claude -p "<richiesta>" --model opus|sonnet --system-prompt "Sei un assistente che scrive testi su richiesta." --tools "" --no-session-persistence --output-format json`;
dall'output prendi l'evento `type == "result"`. Salva tutto in `contenuti/idee/uscite/<slug>-<data>.md`: per ogni
richiesta il testo esatto, poi le uscite con una sigla (A1…A10 per la prima richiesta, B1… per la seconda; 1-5 Opus,
6-10 Sonnet) e il modello. Poi con Edit aggiungi all'idea `**Uscite:** <percorso>` sotto la riga dello stato. Se
`claude -p` fallisce, fermati: senza uscite vere lo sceneggiatore non scrive i testi del modello.
`claude -p` passa al modello nome ed email dell'account anche da una cartella neutra (`--bare` vale solo con chiave
API): prima di salvare sostituisci i dati veri con «Nome Cognome» e «nome.cognome@email.it» e dichiaralo in testa al
file (2026-09-16: nome in 28 uscite su 30).

**T1 · sceneggiatura.** Prima lancia `uv run reel stile`: se il verdetto è `da rifare` o `manca`, dillo nel report
(lo `stilista` si lancia a parte, non blocca); riporta anche la riga `pattern:` (se manca, lo schema dell'idea non ha
una fonte da rileggere). Poi lancia `sceneggiatore` sull'idea: deve passare `uv run reel valida`
senza errori (rilancialo con gli errori al massimo due volte). Con Edit aggiorna l'idea: `**Stato:** sceneggiata` e
`**Sceneggiatura:** <percorso>` sotto la riga dello stato.
A fermate → FERMATA 2: percorso, scene con tipo e durata stimata, durata del reel (dall'output di `valida`), il titolo
alternativo, le frasi di cui lo sceneggiatore è meno sicuro. Prossimo passo: il presentatore legge la VOCE ad alta
voce (`uv run reel gobbo <file>`), corregge, poi `/pipeline <sceneggiatura>`.

**T2 · revisione.** Lancia `revisore-tecnico`. Con un ❌ fermati in entrambe le modalità: riporta i claim e le
riformulazioni proposte (prossimo passo: il presentatore sceglie, lo sceneggiatore corregge, poi si rilancia).
Altrimenti prosegui con T3.

**T3 · animazione.** Lancia `animatore`: `.py`, `anima --json`, fotogrammi, `monta --prova --anteprima`,
`stato: animato`. Prima di consegnare guarda tu `contact-sheet.png` e i fotogrammi fitti di ogni scena: un testo
tagliato o un beat vuoto si rimanda all'animatore, non al presentatore. I cambi di stato si guardano a 8 fps (a 2 fps i testi
sovrapposti per 0,3 s non si vedono).

**T4 · anteprima e report.** Se `contenuti/render/<slug>/report.json` manca o è più vecchio della sceneggiatura,
rilancia `uv run reel monta <file> --prova --anteprima`. Poi il report qui sotto: è la FERMATA 3, e con `--tutto` è
il report unico.

## Report della FERMATA 3 (e fine di `--tutto`)
1. **File**: spunto, idea, sceneggiatura, `contenuti/animazioni/<slug>.py`, `contenuti/render/<slug>/reel-prova.mp4`,
   `contact-sheet.png`, `scene/NN.png`, `fotogrammi/NN-filmstrip.png`.
2. **La VOCE per scena**, testuale, come la leggerà nel karaoke: è quello che il presentatore deve rileggere prima di
   registrare.
3. **Durate**: per scena da `report.json` (con `origine_tempi`), il totale, e il confronto con la stima di `valida`.
4. **Avvisi**: residui di `valida`, ⚠️ del revisore (una riga ciascuno), rapporto dell'animatore (difetti della
   libreria, cose che non ci stavano), frasi di cui lo sceneggiatore è meno sicuro, stato della guida di stile.
5. **Da confermare**: i fatti presi dalla fonte (idee da un link), i testi attribuiti a un modello (con la sigla
   dell'uscita), lo schema narrativo e come è stato distribuito sulle scene.
6. **Prossimo passo**: guardare l'anteprima e annotare leggibilità, tempi e beat; poi la registrazione in presa unica
   sull'anteprima (`uv run reel registra <file>`) e il montaggio con le clip vere (`uv run reel monta <file>
   --anteprima`).

Prima di chiudere: le lezioni della corsa (rimandi del revisore, difetti trovati nei fotogrammi, note del presentatore)
vanno nella sezione «Lezioni dalle sessioni» dell'agente giusto, con la data.
