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
  FERMATA 1 dopo l'idea, FERMATA 2 dopo la sceneggiatura, FERMATA 2b sui provini dei filmati (solo se il piano
  propone scene a filmato), FERMATA 3 dopo l'anteprima. Revisione e animazione corrono in
  fila, senza fermata in mezzo; filmati e animazione corrono **insieme**.
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
- **`contenuti/sceneggiature/…`**: `sceneggiatura` → T2; `rivisto` → T2b (se le scene a filmato sono già
  marcate `[broll]`, dritto al secondo tempo ∥ T3); `animato` → ristampa il report (T4).
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

**T0b · uscite vere** (un comando, senza agenti). Si fa se le «Note per il reel» dell'idea elencano richieste da
generare e l'idea non ha ancora la riga `**Uscite:**`: `uv run reel uscite <idea>` (prima `--prova-a-secco` per vedere
le richieste che ha trovato). Lancia in parallelo 5 uscite con Opus e 5 con Sonnet per richiesta, da una cartella
neutra (`claude -p … --tools "" --no-session-persistence`), anonimizza nome ed email dell'account (più i termini di
`config.local.toml [uscite] anonimizza`), scrive `contenuti/idee/uscite/<slug>-<data>.md` con le sigle (A1…A10, B1…;
1-5 Opus, 6-10 Sonnet) e aggiunge `**Uscite:**` all'idea. Se fallisce, fermati: senza uscite vere lo sceneggiatore
non scrive i testi del modello. **Da ricontrollare a mano**, perché lo strumento li segnala ma non li decide: le
uscite marcate «da ricontrollare» (`--tools ""` non spegne i connettori dell'account: «Drive», «Gmail», commenti su
città o ateneo) — sostituisci le inferenze personali, dichiara l'artefatto in testa al file e ricordalo al revisore:
la caption dovrà dire che lo strumento passava nome, email e connettori. Se il nome di un'azienda sta dentro le
richieste, l'omonimia si controlla **prima** di generare.

**T1 · sceneggiatura.** Prima lancia `uv run reel stile`: se il verdetto è `da rifare` o `manca`, dillo nel report
(lo `stilista` si lancia a parte, non blocca); riporta anche la riga `pattern:` (se manca, lo schema dell'idea non ha
una fonte da rileggere). Poi lancia `sceneggiatore` sull'idea: deve passare `uv run reel valida`
senza errori (rilancialo con gli errori al massimo due volte). Con Edit aggiorna l'idea: `**Stato:** sceneggiata` e
`**Sceneggiatura:** <percorso>` sotto la riga dello stato.
A fermate → FERMATA 2: percorso, scene con tipo e durata stimata, durata del reel (dall'output di `valida`), il titolo
alternativo, le frasi di cui lo sceneggiatore è meno sicuro. Prossimo passo: il presentatore legge la VOCE ad alta
voce (`uv run reel gobbo <file>`), corregge, poi `/pipeline <sceneggiatura>`.

**T2 · revisione.** Due tempi, il secondo in parallelo.
1. Raccogli l'elenco **fonte → claim**: dalla sezione `## Fonte` e dai «claim per il revisore» dell'idea, più i numeri
   e i fatti della sceneggiatura (VOCE, numeri a schermo, `FIGURA:`) con la fonte indicata nelle Note di produzione.
2. Lancia **un `verificatore-fonte` per fonte, tutti insieme** (un solo messaggio, più Agent): ognuno scarica la pagina
   e riporta la scheda alla lettera. Nessuna fonte esterna (reel senza numeri): salta questo passo.
3. Lancia `revisore-tecnico` passandogli le schede: il verdetto ✅/⚠️/❌ resta suo, e riapre lui le fonti dubbie.
Con un ❌ fermati in entrambe le modalità: riporta i claim e le riformulazioni proposte (prossimo passo: il
presentatore sceglie, lo sceneggiatore corregge, poi si rilancia; alla seconda passata bastano il revisore e i soli
verificatori delle fonti nuove). Altrimenti prosegui.

**T2b · filmati, primo tempo** (agente `broll`, modalità `marca`; in serie, è veloce). Va deciso **prima di animare**,
perché una scena a filmato non ha una classe Manim e la scena dopo parte da uno stacco. L'agente lancia `broll piano`,
controlla l'**equilibrio** (circa metà delle scene in mezzo, ± una, mai due di fila; apertura e chiusura non contano:
sono il presentatore a tutto schermo), corregge i falsi positivi dell'euristica in `piano.json`, riscrive le query in
inglese e marca le scene con `broll scrivi --presto`. Se chiude BLOCKED (la sceneggiatura non divide i registri, o un
brief non descrive un'immagine) si rimanda allo sceneggiatore con il suo elenco, e si riparte da T2. Se `scrivi --presto` non ha convertito una scena scritta per
il filmato (ha un `TESTO:`), **non far partire l'animatore**: la vedrebbe come scena sua. A fermate lo decide il
presentatore; con `--tutto` fermati e riportalo. Zero scene a filmato: scrivilo nel report e prosegui.

**T2b secondo tempo ∥ T2c ∥ T3: in parallelo** (un solo messaggio, tre Agent).
- `broll` in modalità `scegli`: `cerca`, `provini`, guarda i contact sheet. A fermate → **FERMATA 2b**: per ogni scena i
  due candidati consigliati e perché, con i comandi `broll scegli` pronti; il presentatore sceglie **mentre l'animatore
  lavora**, poi `/pipeline <file>` riparte da `rendi`. Con `--tutto` l'agente sceglie da sé: la scelta è **provvisoria**
  e va in testa ai punti «da confermare» del report. Poi `rendi`, `prova-inquadratura`, `scrivi`, `valida`.
  Cambiare un filmato dopo costa poco: `broll scegli`, `broll rendi --forza`, `uv run reel monta`, senza rianimare.
- **T2c · la clip generata** (agente `immagini`, `sonnet`). Ogni reel ne ha **almeno una** (regole editoriali §3,
  2026-09-22): 2-3 immagini generate con Meshy montate sui beat, con la dissolvenza. Si lancia insieme a `broll`
  `scegli`: se la scena non è già decisa, glielo dice `broll` nel suo rapporto (scena senza candidati buoni, o quella
  dove l'immagine generata aggiunge di più). Costa chiamate a Meshy: una scena per reel, e si rigenera solo se
  l'immagine è inservibile. Alla fermata 3 il provino e i prompt vanno fra i punti da confermare.
- **T3 · animazione.** `animatore`: `.py`, `anima --json` a zero ⚠ e zero ✗, fotogrammi, `stato: animato`. Se i filmati
  non sono ancora resi il suo `monta --prova --anteprima` fallisce sulle scene `[broll]`: non è un suo errore, il
  montaggio lo rifai tu in T4 quando `broll` ha finito.

**T3b · controllo dei fotogrammi, in parallelo.** Quando ci sono i `_scene/NN.mp4` montati, lancia **un
`controllore-fotogrammi` per scena animata, tutti insieme**: ognuno fa `uv run reel strisce <file> --scena N`, guarda i
passaggi a 8 fps e riferisce i difetti con l'istante. I difetti **gravi** tornano all'animatore in un solo rimando con
l'elenco per scena (al massimo **due** rimandi; dopo, i difetti rimasti vanno nel report); i «dubbi» li guardi tu sulla
striscia indicata prima di rimandarli. Tu guardi comunque `contact-sheet.png`: le scene devono distinguersi a colpo
d'occhio. Un testo tagliato o un beat vuoto si rimanda all'animatore, non al presentatore.

**T4 · anteprima e report.** Se `contenuti/render/<slug>/report.json` manca o è più vecchio della sceneggiatura,
rilancia `uv run reel monta <file> --prova --anteprima`; rilancialo anche dopo `broll rendi` e dopo ogni rimando
all'animatore. Poi `broll piano` + `broll rendi` se le durate della prima anteprima hanno riportato una scena a
`scelto` (solo ffmpeg). Poi il report qui sotto: è la FERMATA 3, e con `--tutto` è
il report unico.

## Report della FERMATA 3 (e fine di `--tutto`)
1. **File**: spunto, idea, sceneggiatura, `contenuti/animazioni/<slug>.py`, `contenuti/render/<slug>/reel-prova.mp4`,
   `contact-sheet.png`, `scene/NN.png`, `fotogrammi/NN-filmstrip.png`.
2. **La VOCE per scena**, testuale, come la leggerà nel karaoke: è quello che il presentatore deve rileggere prima di
   registrare.
3. **Durate**: per scena da `report.json` (con `origine_tempi`), il totale, e il confronto con la stima di `valida`.
3bis. **Filmati**: quali scene sono a filmato, il candidato scelto per ciascuna (con `--tutto` la scelta è provvisoria:
   dillo per primo), i provini da riguardare, cosa copre il riquadro, i crediti per la didascalia.
4. **Avvisi**: residui di `valida`, ⚠️ del revisore (una riga ciascuno), rapporto dell'animatore (difetti della
   libreria, cose che non ci stavano), difetti dei `controllore-fotogrammi` rimasti dopo i rimandi (scena, istante), frasi di cui lo sceneggiatore è meno sicuro, stato della guida di stile.
5. **Da confermare**: i fatti presi dalla fonte (idee da un link), i testi attribuiti a un modello (con la sigla
   dell'uscita), lo schema narrativo e come è stato distribuito sulle scene.
6. **Prossimo passo**: guardare l'anteprima e annotare leggibilità, tempi e beat; poi la registrazione in presa unica
   sull'anteprima (`uv run reel registra <file>`), dove il presentatore **corregge la VOCE** fuori dalla presa (tasto `E`),
   e il montaggio con le clip vere (`uv run reel monta <file> --anteprima`).

## Dopo la registrazione (regole editoriali §8-9)
- `uv run reel monta <file> --anteprima`: le caption si fanno dal testo recitato; la riga «testo cambiato in
  registrazione» e `report.json` (`voce_recitata`, `voce_cambiata`) dicono dove. `uv run reel parlato <file>` mostra le
  differenze; con il sì del presentatore `--applica` le riporta nel .md (frasi con numeri o fatti nuovi → revisore).
- **Il volto lo guarda solo lui**: dopo un montaggio con le clip vere si leggono solo le immagini coperte che `monta` e
  `strisce` scrivono da sé (avatar nel riquadro, cartello a volto pieno), mai `copertina*.png`, i video o fotogrammi
  estratti a mano. Si controllano durate, `origine_tempi` e caption nel report.

## Chi gira su che modello
`ideatore`, `sceneggiatore`, `revisore-tecnico`, `animatore`, `stilista`: il modello della sessione (il più forte: è
lì che nasce la qualità). `broll`, `controllore-fotogrammi`, `verificatore-fonte`: `sonnet` (nel loro frontmatter).
T0b: nessun modello, è un comando. Gli agenti non lanciano altri agenti: il lavoro in parallelo lo apri tu, con più
Agent nello stesso messaggio (T2 verificatori, T2b ∥ T3, T3b controllori; due reel insieme vanno benissimo).

Prima di chiudere: le lezioni della corsa (rimandi del revisore, difetti trovati nei fotogrammi, note del presentatore)
**modificano la regola in vigore** nel tema giusto dell'agente giusto, con la data fra parentesi; una regola superata
si toglie, non si marca. La cronaca (chi, su quale reel, perché) va in `.claude/agents/storico/<agente>.md`. Una regola
del presentatore che vale per tutti si scrive in `docs/regole-editoriali.md`, e negli agenti solo «cosa cambia per te».
