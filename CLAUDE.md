# reel-anim — Reel esplicativi con Manim

## Cos'è
Pipeline per produrre Reel Instagram 9:16 (30-90 s) in cui **le animazioni guidano la spiegazione** di un concetto
e **il presentatore compare in un riquadro** in sovraimpressione (volto + voce, una clip registrata per scena).
Motore: **Manim Community** (grafica), **ffmpeg** (compositing e montaggio), Python 3.12 con `uv`. Tutto generato
da script a partire da una sceneggiatura markdown; niente tool esterni. **Senza brand**: identità (palette, font,
handle, riquadro, voce sintetica) in `config.toml` (+ `config.local.toml` gitignored per gli override).
Nato da `~/Projects/io-e-lia` (renderer HTML di caroselli, che resta inalterato): da lì sono stati copiati o
adattati parser, validazione, ffprobe/filmstrip, contact sheet; cruscotto e `pubblica` arrivano nella fase 3.
Piano completo: `~/.claude/plans/dobbiamo-revisionare-il-modello-lovely-piglet.md`.

## Struttura
- `config.toml` — identità e misure (video 1080×1920 @30, safe area, riquadro, schermo, palette, font, voce di prova)
  e `[stile]` (corpus di reelkit, guida del parlato, `pattern` = `~/Projects/reelkit/pattern.md` con i pattern
  narrativi che ideatore e sceneggiatore leggono direttamente)
- `tools/anim/` — libreria Manim: `config` (TOML + font Pango + opzioni `tempconfig`), `misure` (px ↔ unità,
  minimi di leggibilità, `FATTORE_FONT_SIZE` misurato con `calibra.py`), `base` (`ScenaReel` con `durata_s`,
  `beat(i)` sugli inizi delle frasi, `durata_beat`, `arrotonda`, `fino_a`, `chiudi`, aree contenuto/riquadro/schermo, `debug` con guide; cambi grandi `punch(s)` e `zoom_su(mob)`/`torna()`), `componenti` (Titolo,
  Caption, Etichetta, Barrato, Freccia, Carta, Barra, Classifica, Token, Frase, Lista, Contatore, Evidenzia,
  CorniceSchermo, Piede, Messaggio, Punch, Icona, ContatoreScorre, Codice), `diagrammi` (Nodo, Flusso, Ciclo, Confronto,
  Corrispondenza, Graffa, Tabella), `controlli` (controlli automatici a fine beat), `vetrina` (una scena di prova per
  componente: `uv run python -m tools.anim.vetrina`), `prova` (scena di prova della fase 0)
- `tools/reel/` — grammatica e montaggio: `model`, `parser`, `validate` (`LIMITI`, fonte unica), `stima`, `gobbo`,
  `clip`, `voce` (`say`), `manim_render`, `compositing` (filtergraph ffmpeg: b-roll, riquadro con maschera, audio,
  concat con xfade), `fotogrammi`, `contact_sheet`, `monta`, `stile` (guida del parlato rispetto al corpus),
  `__main__` (CLI `uv run reel`)
- `broll/` — sottosistema del materiale esterno (filmati che si alternano alle animazioni): **progetto `uv`
  a sé**, con proprio `pyproject.toml`, `uv.lock` e `.venv`, così le sue dipendenze non entrano mai in quelle
  della radice. `uv run --project broll broll piano|stato|prova-inquadratura` (`broll/README.md`)
- `contenuti/` — `spunti/` (link, righe o tema: il punto di partenza, `stato: spunto → ideato`), `idee/`,
  `sceneggiature/`, `bozze/ in-produzione/ pubblicati/ db/`, `archivio/<slug>/` (reel chiusi o abbandonati: si
  leggono, non girano), `animazioni/<slug>.py` (una classe
  `ScenaNN(ScenaReel)` per scena), `media/<slug>/scena-NN.mov` (clip del presentatore, gitignored),
  `render/<slug>/` (output, gitignored)
- `templates/reel.md` — grammatica della sceneggiatura (blocco-commento) · `templates/esempio-reel.md` — esempio
  completo (7 scene, tutti i tipi e tutti i componenti) con `contenuti/animazioni/esempio-reel.py` e il b-roll versionato
  in `contenuti/media/esempio-reel/`: `uv run reel monta templates/esempio-reel.md --prova --anteprima` (~20 s)
- `docs/` — `sceneggiatura.md` (grammatica, limiti, come si scrive la VOCE), `animazioni.md` (manuale
  dell'animatore: regole, tempi, componenti, controlli, trappole, fonti), `registrazione.md` (clip del presentatore),
  `linguaggio-reel.md` (hook, payoff, CTA), `stile-parlato.md` (come parla il presentatore: la scrive lo `stilista`)
- `assets/fonts/` (Inter Variable, JetBrains Mono) · `assets/presentatore/avatar.png` (segnaposto da `reel setup`) ·
  `assets/icone/` (SVG Lucide, licenza ISC)
- `.claude/agents/` — `ideatore` (spunto → idea, anche da un link con WebFetch; sceglie uno schema da `pattern.md`
  e lo scrive in `## Struttura narrativa`), `stilista` (corpus di reelkit →
  `docs/stile-parlato.md`), `sceneggiatore` (idea → sceneggiatura, `reel valida`), `revisore-tecnico` (claim anche
  nelle animazioni e contro la fonte, `stato: rivisto`), `animatore` (`.py` + `anima --json` + fotogrammi +
  `monta --prova --anteprima`, `stato: animato`; non tocca `tools/`) · `.claude/commands/pipeline.md` —
  `/pipeline <file> [--tutto]`: fino alla prossima fermata, o con `--tutto` fino all'anteprima da registrare; la
  tappa T0b genera le uscite vere dei testi del modello (`claude -p`, Opus e Sonnet) in `contenuti/idee/uscite/` ·
  `.claude/workflows/reel.js` — la stessa corsa come Workflow deterministico (`args` = percorso di partenza)

## Stato
Fasi 0 e 1 chiuse (2026-09-13, in `main`). Fase 2 in corso (branch `fase-2-primo-reel`): il primo reel vero
«Generativa non vuol dire creativa» (slug `generativa-non-creativa`) ha fatto da banco di prova per libreria, agenti e
`reel registra`; **il 2026-09-15 i contenuti sono stati azzerati** e i suoi testi archiviati in
`contenuti/archivio/generativa-non-creativa/` (clip, prese e render cancellati). Nuovi: `ideatore` e spunti,
`stilista` e `reel stile` (corpus in `~/Projects/reelkit/export.md`), `/pipeline --tutto`
e il workflow `reel`. Le revisioni del presentatore hanno l'ultima parola. Prima corsa `--tutto` il 2026-09-15
(`generativa-probabile`, biglietto per Marco, commit 3ae4d09). Il 2026-09-16: pattern narrativi di reelkit agli
agenti (`[stile] pattern`, `reel stile`, tappa T0b) e lo spunto riscritto con la mail di risposta a un annuncio di
lavoro, stesso slug, render cancellato; la corsa `--tutto` è arrivata all'anteprima (74 s, azienda «Acme Arredi»)
con le mosse wow (`docs/animazioni.md` §11bis). **Prossimo passo**: l'animatore corregge i testi sovrapposti nei
passaggi delle scene 4, 5 e 7, poi il presentatore guarda l'anteprima (dettagli nella memoria `stato-avanzamento`).

## Comandi
`uv run reel setup` · `stile` · `valida <file>` · `gobbo <file> [--scrivi]` · `clip <file>` · `voce <file>` ·
`registra <file> [--da-scena N] [--dispositivi] [--video N --audio N] [--spezza presa-NN]` ·
`anima <file> [--scena N] [--qualita l|m|h] [--debug] [--json]` · `monta <file> [--prova] [--anteprima] [--scena N]` ·
`uv run pytest -q` (i test `slow` usano Manim e ffmpeg). `--prova` = voce sintetica + avatar segnaposto: anteprima
completa senza il presentatore, **non pubblicabile**.

## Grammatica (vedi templates/reel.md)
`## Scena N [hook|spiegazione|schermo|chiusura, durata=Ns, transizione=…]` con righe `VOCE:` (una riga =
un beat = un pezzo di parlato), `ANIMAZIONE:` (brief per l'animatore), `TESTO:`, `TITOLO:/SOTTOTITOLO:` (hook), `MESSAGGIO:/CTA:`
(chiusura), `SCHERMO: file`, `RIQUADRO: no|si|posizione`; inline `==evidenzia==`, `**grassetto**`.
Limiti in `tools/reel/validate.py::LIMITI`: 6-8 scene (5-9), VOCE ≤ 50 parole/scena (hook ≤ 20, chiusura ≤ 18), scena 2,5-19 s,
reel 30-90 s (dal 2026-09-15: la VOCE è parlato vero, «prima il monologo, poi i beat», `docs/sceneggiatura.md` §5;
`valida` avvisa su frasi da titolo in fila, «X, sì. Y, no.», due punti come snodo). La durata reale di ogni scena la
decide la clip registrata; senza clip vale la stima (2,8 parole/s).
I beat partono sugli inizi delle frasi VOCE: esatti con la voce di prova (una frase alla volta, `pausa_frasi_s`),
esatti anche con le clip di `reel registra` (sidecar `scena-NN.json`, `origine_tempi: presa`), stimati a parole con
clip esterne. `anima` usa gli stessi tempi di `monta --prova`; `report.json` ha per
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

## Pipeline (`.claude/commands/pipeline.md`; completa in fase 3)
spunto → idea (ideatore, **fermata 1**) → sceneggiatura (**fermata 2**) → revisione tecnica (con ❌ ci si ferma) →
animazione (animatore: `.py` + anteprima `--prova`) → **fermata 3: il presentatore guarda l'anteprima** →
registrazione (`reel registra`) → montaggio → social → approvazione → pubblica (container REELS). Con `--tutto` (o
il workflow `reel`) si salta dalla partenza alla fermata 3, fermandosi solo su ❌, errori o agenti bloccati. Spunti:
`stato: spunto → ideato`; idee: `**Stato:** idea → sceneggiata`; sceneggiature: `stato: sceneggiatura → rivisto →
animato → …`. Mai spostare file tra cartelle: lo fa il presentatore. Fase 3: cruscotto, db delle decisioni,
social-strategist.

## Registrazione guidata (fase 5, fatta il 2026-09-14; decisione: B con «riprendi da questa scena»)
`uv run reel registra <file>` (`docs/registrazione.md` §6): app Tkinter con tre pannelli (webcam con il cerchio, il
reel `--prova` con il volto live nel riquadro, testo karaoke sui tempi della voce di prova; inquadratura spostabile e
zoomabile prima della presa, salvata in `inquadratura.json` e applicata come ritaglio al taglio). **Presa unica** da
una scena a scelta con pre-roll e conto alla rovescia; un ffmpeg avfoundation scrive il video `_prese/presa-NN.mov`
(h264 videotoolbox) e la pipe di anteprima, così l'indice del fotogramma letto dà l'istante nella presa; **l'audio lo
registra Python con PortAudio (`sounddevice`) in `presa-NN.wav`**, perché avfoundation perde il 10-15 % dei pacchetti
audio (verificato il 2026-09-14). A fine presa le scene coperte per intero diventano `scena-NN.mov` + `scena-NN.json`
(inizi delle frasi, che `monta` usa: `origine_tempi: presa`, niente ASR). Moduli: `tools/reel/registra.py` (logica
pura, `Timeline`, `karaoke`, comandi, `Presa`, `spezza`, inquadratura), `cattura.py` (processi + thread + `Microfono`,
testabile con lavfi), `registra_app.py` (Tk, importato solo dal comando; menu per fotocamera e microfono, scelta
salvata per nome in `contenuti/media/dispositivi.json`). Config `[registrazione]`. L'evento `clip` nel
db arriva con la fase 3 (oggi il registro è `_prese/prese.json`).

## Prossimi passi della libreria
- Fatto (2026-09-13): esplorazione della community (fonti in `docs/animazioni.md` §13, nessun plugin da installare);
  componenti per diagrammi, icone, codice, contatore che scorre; controlli automatici a fine beat, controllo statico
  del file, `anima --json`.
- Da fare: ASR solo se servirà per clip esterne (con `registra` i tempi sono già esatti); controlli sui pixel dei fotogrammi chiave
  (b-roll e immagini, che i controlli sugli ingombri non vedono).
