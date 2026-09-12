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
  `beat(i)`, `fino_a`, `chiudi`, aree contenuto/riquadro/schermo, `debug` con guide), `componenti` (Titolo,
  Caption, Etichetta, Barrato, Freccia, Carta, Barra, Classifica, Token, Frase, Lista, Contatore, Evidenzia,
  CorniceSchermo, Piede, Messaggio), `prova` (scena di prova della fase 0)
- `tools/reel/` — grammatica e montaggio: `model`, `parser`, `validate` (`LIMITI`, fonte unica), `stima`, `gobbo`,
  `clip`, `voce` (`say`), `manim_render`, `compositing` (filtergraph ffmpeg: b-roll, riquadro con maschera, audio,
  concat con xfade), `fotogrammi`, `contact_sheet`, `monta`, `__main__` (CLI `uv run reel`)
- `contenuti/` — `bozze/ idee/ sceneggiature/ in-produzione/ pubblicati/ db/`, `animazioni/<slug>.py` (una classe
  `ScenaNN(ScenaReel)` per scena), `media/<slug>/scena-NN.mov` (clip del presentatore, gitignored),
  `render/<slug>/` (output, gitignored)
- `templates/reel.md` — grammatica della sceneggiatura (blocco-commento) · `templates/esempio-reel.md` (da scrivere)
- `assets/fonts/` (Inter Variable, JetBrains Mono) · `assets/presentatore/avatar.png` (segnaposto da `reel setup`)

## Comandi
`uv run reel setup` · `valida <file>` · `gobbo <file> [--scrivi]` · `clip <file>` · `voce <file>` ·
`anima <file> [--scena N] [--qualita l|m|h] [--debug]` · `monta <file> [--prova] [--anteprima] [--scena N]` ·
`uv run pytest -q` (i test `slow` usano Manim e ffmpeg). `--prova` = voce sintetica + avatar segnaposto: anteprima
completa senza il presentatore, **non pubblicabile**.

## Grammatica (vedi templates/reel.md)
`## Scena N [hook|spiegazione|schermo|chiusura, durata=Ns, transizione=…]` con righe `VOCE:` (una frase = un
beat), `ANIMAZIONE:` (brief per l'animatore), `TESTO:`, `TITOLO:/SOTTOTITOLO:` (hook), `MESSAGGIO:/CTA:`
(chiusura), `SCHERMO: file`, `RIQUADRO: no|si|posizione`; inline `==evidenzia==`, `**grassetto**`.
Limiti in `tools/reel/validate.py::LIMITI`: 6-8 scene (5-9), VOCE ≤ 35 parole/scena (hook ≤ 15), scena 2,5-14 s,
reel 30-60 s. La durata reale di ogni scena la decide la clip registrata; senza clip vale la stima (2,8 parole/s).

## Convenzioni
- Tutto in italiano (codice: nomi italiani come in io-e-lia). Nessun riferimento a un brand nel codice.
- Animazioni: solo `Text`/`MarkupText` (Pango, niente LaTeX), font e colori dal config, testo mai sotto 36 px,
  contenuto dentro `self.area.contenuto` (lascia libero il riquadro), nessun gradiente. Manim è deterministico.
- Claude Code non vede i video: guarda `scene/NN.png`, `fotogrammi/NN-filmstrip.png`, `contact-sheet.png`,
  `report.json` in `contenuti/render/<slug>/`.
- Mai pubblicare senza `--pubblica`; la pubblicazione la lancia il presentatore.
- Aggiornare la memoria (`~/.claude/projects/-Users-bitwise-Projects-reel-anim/memory/`) a ogni milestone.

## Pipeline prevista (fase 3, da fare)
idea → sceneggiatura → revisione tecnica → animazione (animatore: `.py` + anteprima `--prova`) → fermata: il
presentatore guarda → registrazione (gobbo, clip) → montaggio → social → approvazione → pubblica (container REELS).

## Registrazione guidata (fase 5, da fare prima della registrazione vera)
`uv run reel registra <file>`: **app desktop nativa in Python** (Tkinter + ffmpeg avfoundation) in cui il
presentatore vede se stesso e il testo da recitare, registra con un tasto e la clip si salva da sola in
`contenuti/media/<slug>/scena-NN.*` (evento `clip` nel db, ffprobe con durata vs stima). Decisione aperta: (A) una
clip per scena con gobbo, oppure (B) una presa unica con l'anteprima del reel e il testo sincronizzato sui beat, poi
spezzata per scene dai tempi noti. Dettagli e pro/contro nel piano.

## Da esplorare
- Best practice Manim: cercare un MCP server o un sito di riferimento con gli snippet più usati (docs.manim.community
  «examples», manim-community/awesome-manim, plugin) e distillarli in `docs/animazioni.md` per l'agente animatore.
