# reel-anim

**Explainer Reels as code.** Generates vertical 9:16 Instagram Reels where *animations drive the explanation* and the presenter appears in a picture-in-picture frame (one clip per scene), opening and closing full-screen. Everything, from the script to the burned-in captions, is produced from a Markdown screenplay.

- **Graphics:** [Manim Community](https://www.manim.community/) with a custom component library (diagrams, patterns, beat-synced highlights and zooms)
- **Assembly:** ffmpeg compositing, presenter ↔ full-frame transitions, audio chain normalised to −14 LUFS, captions
- **Script:** Python 3.12 with [uv](https://docs.astral.sh/uv/); brand identity (palette, fonts, handle, layout) lives in [`config.toml`](config.toml), so the pipeline itself is brand-free

## From idea to Reel

```
idea → script (LLM) → screenplay.md → validate → animate (Manim) → mount (ffmpeg) → Reel + contact sheet + report
```

A scene is a few lines of Markdown (the grammar keywords are in Italian):

```markdown
## Scena 2 [spiegazione, durata=8s]
VOCE: Ogni riga di voce è un beat dell'animazione.
ANIMAZIONE: Il diagramma si costruisce a ritmo del parlato.
CAPTION: Ogni riga = un beat
```

The animation timeline is synced to the beginnings of the spoken sentences, and a `report.json` flags any timing warnings. Preview with a synthetic voice and a placeholder avatar before recording anything.

## Quick start

```bash
uv sync
uv run reel setup
uv run reel monta templates/esempio-reel/esempio-reel.md --prova --anteprima   # full preview, no presenter needed
uv run pytest -q
```

Main commands: `reel valida`, `reel copione`, `reel anima`, `reel monta`, `reel registra` (guided recording), `reel clip`, plus `broll` for stock-footage scenes (Pexels / Pixabay or animated Meshy images). Docs are in [`docs/`](docs/) (screenplay grammar, animation manual, recording workflow); the repository's working language is Italian.

## Stack

Python 3.12 · Manim · ffmpeg · uv · Pillow · pytest · Claude Code sub-agents and workflow (`.claude/`)

## License

MIT, see [LICENSE](LICENSE). Bundled fonts (Inter, JetBrains Mono: OFL) and Lucide icons (ISC) keep their own licenses.
