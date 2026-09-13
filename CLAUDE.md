# reel-anim — Reel esplicativi con Manim

## Cos'è
Pipeline per produrre Reel Instagram 9:16 (30-60 s) in cui **le animazioni guidano la spiegazione** di un concetto
e **il presentatore compare in un riquadro** in sovraimpressione (volto + voce, una clip registrata per scena).
Motore: **Manim Community** (grafica), **ffmpeg** (compositing e montaggio), Python 3.12 con `uv`. Tutto generato
da script a partire da una sceneggiatura markdown; niente tool esterni. **Senza brand**: identità (palette, font,
handle, riquadro, voce sintetica) in `config.toml` (+ `config.local.toml` gitignored per gli override).
Nato da `~/Projects/io-e-lia` (renderer HTML di caroselli, che resta inalterato): da lì sono stati copiati o
adattati parser, validazione, ffprobe/filmstrip, contact sheet; cruscotto e `pubblica` arrivano nella fase 3.
Piano completo: `~/.claude/plans/dobbiamo-revisionare-il-modello-lovely-piglet.md`.

## Struttura
- `config.toml` — identità e misure (video 1080×1920 @30, safe area, riquadro, schermo, palette, font, voce di prova)
- `tools/anim/` — libreria Manim: `config` (TOML + font Pango + opzioni `tempconfig`), `misure` (px ↔ unità,
  minimi di leggibilità, `FATTORE_FONT_SIZE` misurato con `calibra.py`), `base` (`ScenaReel` con `durata_s`,
  `beat(i)` sugli inizi delle frasi, `durata_beat`, `arrotonda`, `fino_a`, `chiudi`, aree contenuto/riquadro/schermo, `debug` con guide), `componenti` (Titolo,
  Caption, Etichetta, Barrato, Freccia, Carta, Barra, Classifica, Token, Frase, Lista, Contatore, Evidenzia,
  CorniceSchermo, Piede, Messaggio, Icona, ContatoreScorre, Codice), `diagrammi` (Nodo, Flusso, Ciclo, Confronto,
  Corrispondenza, Graffa, Tabella), `controlli` (controlli automatici a fine beat), `vetrina` (una scena di prova per
  componente: `uv run python -m tools.anim.vetrina`), `prova` (scena di prova della fase 0)
- `tools/reel/` — grammatica e montaggio: `model`, `parser`, `validate` (`LIMITI`, fonte unica), `stima`, `gobbo`,
  `clip`, `voce` (`say`), `manim_render`, `compositing` (filtergraph ffmpeg: b-roll, riquadro con maschera, audio,
  concat con xfade), `fotogrammi`, `contact_sheet`, `monta`, `__main__` (CLI `uv run reel`)
- `contenuti/` — `bozze/ idee/ sceneggiature/ in-produzione/ pubblicati/ db/`, `animazioni/<slug>.py` (una classe
  `ScenaNN(ScenaReel)` per scena), `media/<slug>/scena-NN.mov` (clip del presentatore, gitignored),
  `render/<slug>/` (output, gitignored)
- `templates/reel.md` — grammatica della sceneggiatura (blocco-commento) · `templates/esempio-reel.md` — esempio
  completo (7 scene, tutti i tipi e tutti i componenti) con `contenuti/animazioni/esempio-reel.py` e il b-roll versionato
  in `contenuti/media/esempio-reel/`: `uv run reel monta templates/esempio-reel.md --prova --anteprima` (~20 s)
- `docs/` — `sceneggiatura.md` (grammatica, limiti, come si scrive la VOCE), `animazioni.md` (manuale
  dell'animatore: regole, tempi, componenti, controlli, trappole, fonti), `registrazione.md` (clip del presentatore)
- `assets/fonts/` (Inter Variable, JetBrains Mono) · `assets/presentatore/avatar.png` (segnaposto da `reel setup`) ·
  `assets/icone/` (SVG Lucide, licenza ISC)
- `.claude/agents/` — `sceneggiatore` (idea → sceneggiatura, `reel valida`), `revisore-tecnico` (claim anche nelle
  animazioni, `stato: rivisto`), `animatore` (`.py` + `anima --json` + fotogrammi + `monta --prova --anteprima`,
  `stato: animato`; non tocca `tools/`) · `.claude/commands/pipeline.md` — `/pipeline <file>`: una tappa, poi fermata

## Stato
Fasi 0 e 1 chiuse (2026-09-13, in `main`). Fase 2 in corso (branch `fase-2-primo-reel`): primo reel vero
«Generativa non vuol dire creativa» (`contenuti/idee/2026-09-10-llm-perche-generativa.md`, slug
`generativa-non-creativa`) portato dagli agenti fino a `animato`; fermata: il presentatore guarda l'anteprima.

## Comandi
`uv run reel setup` · `valida <file>` · `gobbo <file> [--scrivi]` · `clip <file>` · `voce <file>` ·
`anima <file> [--scena N] [--qualita l|m|h] [--debug] [--json]` · `monta <file> [--prova] [--anteprima] [--scena N]` ·
`uv run pytest -q` (i test `slow` usano Manim e ffmpeg). `--prova` = voce sintetica + avatar segnaposto: anteprima
completa senza il presentatore, **non pubblicabile**.

## Grammatica (vedi templates/reel.md)
`## Scena N [hook|spiegazione|schermo|chiusura, durata=Ns, transizione=…]` con righe `VOCE:` (una frase = un
beat), `ANIMAZIONE:` (brief per l'animatore), `TESTO:`, `TITOLO:/SOTTOTITOLO:` (hook), `MESSAGGIO:/CTA:`
(chiusura), `SCHERMO: file`, `RIQUADRO: no|si|posizione`; inline `==evidenzia==`, `**grassetto**`.
Limiti in `tools/reel/validate.py::LIMITI`: 6-8 scene (5-9), VOCE ≤ 35 parole/scena (hook ≤ 15), scena 2,5-14 s,
reel 30-60 s. La durata reale di ogni scena la decide la clip registrata; senza clip vale la stima (2,8 parole/s).
I beat partono sugli inizi delle frasi VOCE: esatti con la voce di prova (una frase alla volta, `pausa_frasi_s`),
stimati a parole con le clip (ASR in fase 5). `anima` usa gli stessi tempi di `monta --prova`; `report.json` ha per
scena `inizi_frasi_s`, `origine_tempi`, `avvisi_tempi` (beat in ritardo, scena che sfora: da portare a zero).

## Convenzioni
- Tutto in italiano (codice: nomi italiani come in io-e-lia). Nessun riferimento a un brand nel codice.
- **Prima di animare leggere `docs/animazioni.md`.** Si consegna con zero avvisi di tempo (`⚠`) e zero controlli (`✗`).
- Animazioni: solo `Text`/`MarkupText` (Pango, niente LaTeX), font e colori dal config, testo mai sotto 36 px,
  contenuto dentro `self.area.contenuto` (lascia libero il riquadro), nessun gradiente. Manim è deterministico.
  Testo con `testo()` (righe ad altezza costante; `.parola("x")` dà i glifi di una parola); posizioni con
  `area.metti(mob, v, h)` e `px()`; spessori dei tratti con `tratto(px)` e mai `px()` (linee invisibili); le
  animazioni composte dei componenti passano `group=self`, altrimenti un riquadro pieno finisce sopra il testo.
- Claude Code non vede i video: guarda `scene/NN.png`, `fotogrammi/NN-filmstrip.png`, `contact-sheet.png`,
  `report.json` in `contenuti/render/<slug>/`.
- Mai pubblicare senza `--pubblica`; la pubblicazione la lancia il presentatore.
- Aggiornare la memoria (`~/.claude/projects/-Users-bitwise-Projects-reel-anim/memory/`) a ogni milestone.
- **Gli agenti imparano**: ogni lezione di una sessione, tecnica (trappole, controlli mancanti) o di stile (note del
  presentatore sui reel), va nella sezione «Lezioni dalle sessioni» dell'agente giusto in `.claude/agents/`, con la
  data; se riguarda la libreria anche in `docs/animazioni.md` o `docs/sceneggiatura.md`.

## Pipeline (bozza funzionale in fase 2; completa in fase 3)
idea → sceneggiatura (**fermata 2**) → revisione tecnica (con ❌ ci si ferma) → animazione (animatore: `.py` +
anteprima `--prova`) → **fermata 3: il presentatore guarda l'anteprima** → registrazione (gobbo, clip) → montaggio →
social → approvazione → pubblica (container REELS). Idee: `**Stato:** idea → sceneggiata`; sceneggiature:
`stato: sceneggiatura → rivisto → animato → …`. Mai spostare file tra cartelle: lo fa il presentatore. Fase 3:
cruscotto, db delle decisioni, ideatore, social-strategist.

## Registrazione guidata (fase 5, da fare prima della registrazione vera)
`uv run reel registra <file>`: **app desktop nativa in Python** (Tkinter + ffmpeg avfoundation) in cui il
presentatore vede se stesso e il testo da recitare, registra con un tasto e la clip si salva da sola in
`contenuti/media/<slug>/scena-NN.*` (evento `clip` nel db, ffprobe con durata vs stima). Decisione aperta: (A) una
clip per scena con gobbo, oppure (B) una presa unica con l'anteprima del reel e il testo sincronizzato sui beat, poi
spezzata per scene dai tempi noti. Dettagli e pro/contro nel piano.

## Prossimi passi della libreria
- Fatto (2026-09-13): esplorazione della community (fonti in `docs/animazioni.md` §13, nessun plugin da installare);
  componenti per diagrammi, icone, codice, contatore che scorre; controlli automatici a fine beat, controllo statico
  del file, `anima --json`.
- Da fare: allineamento ASR delle frasi per le clip vere (fase 5); controlli sui pixel dei fotogrammi chiave
  (b-roll e immagini, che i controlli sugli ingombri non vedono).
