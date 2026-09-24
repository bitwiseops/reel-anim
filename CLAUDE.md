# reel-anim — Reel esplicativi con Manim

## Cos'è
Pipeline per produrre Reel Instagram 9:16 in cui **le animazioni guidano la spiegazione** di un concetto e **il
presentatore compare in un riquadro** (volto + voce, una clip per scena); apertura e chiusura sono lui a volto pieno.
I reel si guardano muti: le caption col parlato si bruciano nel montaggio. Motore: **Manim Community** (grafica),
**ffmpeg** (compositing e montaggio), Python 3.12 con `uv`; tutto generato da script a partire da una sceneggiatura
markdown. **Senza brand**: identità (palette, font, handle, riquadro, voce di prova) in `config.toml`
(+ `config.local.toml` gitignored per gli override).

## Struttura
- `config.toml` — misure (1080×1920 @30, aree, riquadro), palette, font, voce di prova, `[audio]`, `[copione]`
  (catena dei modelli esterni), `[percorsi]`, `[stile]` (`pattern` di reelkit per l'ideatore; `indice` e
  `trascrizioni` = reel veri trascritti, sei nel prompt del copione)
- `tools/anim/` — libreria Manim: `config`, `misure` (px ↔ unità, minimi di leggibilità), `base` (`ScenaReel`: beat
  sugli inizi delle frasi, aree, `punch`, `zoom_su`), `componenti`, `diagrammi`, `pattern`, `controlli` (a fine
  beat), `vetrina` (`uv run python -m tools.anim.vetrina`). Manuale: `docs/animazioni.md`
- `tools/reel/` — CLI `uv run reel`: `model`, `parser`, `validate` (`LIMITI`, fonte unica dei limiti), `stima`,
  `copione` (il parlato da un modello esterno: Poe, poi `claude -p`), `uscite`, `voce`, `manim_render`,
  `compositing` (filtergraph ffmpeg, raccordo volto pieno ↔ riquadro, catena audio a −14 LUFS), `caption`, `monta`,
  `fotogrammi`, `contact_sheet`, `registra`/`cattura`/`registra_app` (registrazione guidata, `docs/registrazione.md`),
  `parlato`, `gobbo`, `clip`, `percorsi`
- `tools/broll/` — le scene a filmato: `uv run broll piano|stato|cerca|provini|genera|scegli|rendi|scrivi|chiavi|prova-inquadratura`
  (Pexels/Pixabay e immagini Meshy animate → `contenuti/media/<slug>/broll-scena-NN.mp4`; `docs/broll.md`)
- `contenuti/` — `spunti/` → `idee/` → `copioni/` → `sceneggiature/`; `animazioni/<slug>.py` (una classe
  `ScenaNN(ScenaReel)` per scena); `media/<slug>/` (clip del presentatore e filmati, gitignored); `render/<slug>/`
  (il riepilogo: reel, contact sheet, `scene/`, filmstrip, `report.json`; gitignored); `archivio/<slug>/` (reel
  chiusi: si leggono, non girano). Il transitorio sta in `~/Library/Caches/reel-anim/<slug>/` (`reel pulisci`), la
  cache dei filmati in `~/Library/Application Support/reel-anim/cache-broll`
- `templates/` — `reel.md` (grammatica), `copione.md` (prompt del copione), `esempio-reel.md` (esempio completo, con
  `contenuti/animazioni/esempio-reel.py`: `uv run reel monta templates/esempio-reel.md --prova --anteprima`)
- `docs/` — `regole-editoriali.md` (**fonte unica** delle regole del presentatore), `sceneggiatura.md` (grammatica),
  `animazioni.md` (manuale dell'animatore), `pattern-manim.md`, `registrazione.md`, `linguaggio-reel.md`, `broll.md`
- `assets/` — font (Inter, JetBrains Mono), avatar segnaposto, icone Lucide (ISC)
- `.claude/agents/` — sul modello della sessione `ideatore`, `sceneggiatore`, `revisore-tecnico`, `animatore`; su
  `sonnet` `broll`, `immagini`, `controllore-fotogrammi`, `verificatore-fonte`. Ognuno ha le «Regole in vigore» per
  tema; la cronaca sta in `storico/<agente>.md`, che gli agenti non caricano. `.claude/commands/pipeline.md`
  (`/pipeline <file> [--tutto]`) e `.claude/workflows/reel.js` (la stessa corsa come Workflow);
  `.claude/hooks/caffeina.sh` tiene sveglio il Mac durante agenti e workflow

## Comandi
`uv run reel setup` · `valida <file>` · `copione <idea> [--prova-a-secco] [--nota "…"] [--modello X] [--forza]` ·
`uscite <idea>` · `voce <file>` · `anima <file> [--scena N] [--qualita l|m|h] [--debug] [--json]` ·
`monta <file> [--prova] [--anteprima] [--scena N]` · `strisce <file> [--scena N]` · `registra <file> [--da-scena N]` ·
`parlato <file> [--applica]` · `clip <file>` · `gobbo <file>` · `audio <file>` · `pulisci [<slug>]` ·
`uv run pytest -q` (i test `slow` usano Manim e ffmpeg). `--prova` = voce sintetica + avatar segnaposto: anteprima
completa senza il presentatore, **non pubblicabile**.

## Grammatica (`templates/reel.md`, `docs/sceneggiatura.md`)
`## Scena N [hook|spiegazione|schermo|broll|chiusura, durata=Ns, transizione=…]` con righe `VOCE:` (una riga = un
beat), `ANIMAZIONE:`, `FIGURA:`, `TESTO:`, `CAPTION:`, `TITOLO:/SOTTOTITOLO:` (hook), `MESSAGGIO:/CTA:` (chiusura,
solo per il post), `SCHERMO:`, `RIQUADRO:`; inline `==evidenzia==`, `**grassetto**`. Limiti: `validate.LIMITI`.
La durata di una scena la decide la clip registrata (senza clip, la stima). I beat partono sugli inizi delle frasi
VOCE (esatti con la voce di prova e con `reel registra`); `report.json` ha per scena `inizi_frasi_s`,
`origine_tempi`, `avvisi_tempi` (da portare a zero).

## Convenzioni
- Tutto in italiano, anche i nomi nel codice. Nessun riferimento a un brand nel codice.
- **Prima di animare leggere `docs/animazioni.md`.** Si consegna con zero avvisi di tempo (`⚠`) e zero controlli (`✗`).
- Claude Code non vede i video: guarda `scene/NN.png`, `fotogrammi/NN-filmstrip.png`, `contact-sheet.png`,
  `report.json` in `contenuti/render/<slug>/` e le strisce fitte (il comando stampa il percorso).
- **Claude non guarda mai il volto del presentatore**: dopo la registrazione solo le immagini coperte
  (`fotogrammi.copri_volto`), mai `copertina*.png`, video montati o fotogrammi estratti a mano.
- La pubblicazione la lancia il presentatore. Mai spostare file fra le cartelle dei contenuti: lo fa lui.
- Aggiornare la memoria (`~/.claude/projects/-Users-bitwise-Projects-reel-anim/memory/`) a ogni milestone.
- **Gli agenti imparano**: ogni lezione **modifica la regola in vigore** nel tema giusto dell'agente giusto, senza
  date; una regola superata **si toglie, non si marca**; la cronaca (chi, quale reel, quando, perché) va in
  `.claude/agents/storico/<agente>.md`. Una lezione sulla libreria va in `docs/animazioni.md` o
  `docs/sceneggiatura.md`, una regola del presentatore in `docs/regole-editoriali.md`: negli agenti resta il rimando.
- Commenti e documenti dicono cosa vale e perché, non come ci si è arrivati (quello sta in git).

## Pipeline (`.claude/commands/pipeline.md`)
spunto → idea (ideatore, **fermata 1**) → copione (`reel copione`) → sceneggiatura (**fermata 2**) → revisione
tecnica (con ❌ ci si ferma) → filmati (`broll`, `immagini`) ∥ animazione → montaggio `--prova` e controllori →
**fermata 3: il presentatore guarda l'anteprima** → registrazione → montaggio → pacchetto social → pubblicazione.
Con `--tutto` (o il workflow `reel`) si va dalla partenza alla fermata 3, fermandosi solo su ❌, errori o agenti
bloccati. Stati: spunti `spunto → ideato`; idee `idea → sceneggiata`; sceneggiature `sceneggiatura → rivisto →
animato → …`.

## Da fare
Controlli sui pixel dei fotogrammi chiave (filmati e immagini, che i controlli sugli ingombri non vedono); ASR solo
se serviranno clip esterne.
