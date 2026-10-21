<div align="center">

# 🎬 reel-anim

**Can an explainer Reel be written like code, from script to final cut?**
Vertical 9:16 Reels where Manim animations drive the explanation and the presenter sits in a picture-in-picture frame, all generated from a Markdown screenplay.

![Python](https://img.shields.io/badge/python-3.12-blue)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
![Manim](https://img.shields.io/badge/graphics-Manim%20Community-1f6f8b)
![ffmpeg](https://img.shields.io/badge/montage-ffmpeg-007808)
![uv](https://img.shields.io/badge/deps-uv-de5fe9)

</div>

---

## Table of contents

- [Overview](#overview)
- [Highlights](#highlights)
- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [The screenplay](#the-screenplay)
- [Commands](#commands)
- [Project structure](#project-structure)
- [Limitations](#limitations)
- [License and credits](#license-and-credits)

## Overview

Reels are watched muted, so the animation has to carry the explanation and the captions have to carry the voice. reel-anim produces **Instagram Reels (1080×1920 at 30 fps)** in which the animations lead and the presenter (face and voice, one clip per scene) appears in a frame, with full-screen opening and closing. Everything is generated from a Markdown screenplay.

> **Brand-free.** The pipeline carries no identity of its own: palette, fonts, handle, frame and test voice live in [`config.toml`](config.toml), with a git-ignored `config.local.toml` for overrides.

## Highlights

- 🎞️ **Manim component library:** diagrams, patterns, beat-synced highlights, punches and zooms, with readability minimums enforced.
- 🧾 **Markdown screenplay:** one `VOCE:` line is one animation beat, validated before rendering.
- 🎙️ **Guided recording:** `reel registra` walks you through the presenter clips scene by scene.
- 🔊 **Audio chain** normalised to −14 LUFS, **captions** burned into the video.
- 🧪 **Preview mode:** a synthetic voice and a placeholder avatar give a complete preview before you record anything (not publishable).
- 🎥 **B-roll scenes:** stock footage from Pexels or Pixabay, or animated Meshy images.
- 🤖 **Claude Code agents:** ideation, screenplay, technical review and animation sub-agents under [`.claude/`](.claude/).

## Quick start

Requires Python 3.12, [uv](https://docs.astral.sh/uv/) and ffmpeg.

```bash
git clone https://github.com/bitwiseops/reel-anim.git
cd reel-anim
uv sync
uv run reel setup        # checks ffmpeg, manim and fonts; creates a placeholder avatar

# full preview of the example reel, no presenter needed
uv run reel monta templates/esempio-reel/esempio-reel.md --prova --anteprima

uv run pytest -q         # tests marked "slow" use Manim and ffmpeg
```

## How it works

```
idea → script → screenplay.md → validate → animate (Manim) → montage (ffmpeg) → Reel + contact sheet + report
```

1. **Script:** the spoken text is drafted from an idea by an external model.
2. **Validate:** the screenplay is checked against the limits in `tools/reel/validate.py`.
3. **Animate:** each scene is a Manim class whose beats start on the first words of each sentence.
4. **Montage:** ffmpeg composites the animation with the presenter frame, handles the full-screen to frame transition, mixes audio and burns in captions.
5. **Report:** a contact sheet and a `report.json` with per-scene timing, where timing warnings should be driven to zero.

## The screenplay

The grammar keywords are in Italian:

```markdown
## Scena 2 [spiegazione, durata=8s]
VOCE: Ogni riga di voce è un beat dell'animazione.
ANIMAZIONE: Il diagramma si costruisce a ritmo del parlato.
CAPTION: Ogni riga = un beat
```

Scene types are `hook`, `spiegazione`, `schermo`, `broll` and `chiusura`. Full grammar in [`docs/sceneggiatura.md`](docs/sceneggiatura.md) and [`templates/reel.md`](templates/reel.md).

## Commands

| Command | Purpose |
|---|---|
| `reel setup` | check the environment |
| `reel valida <file>` | validate a screenplay |
| `reel copione <idea>` | draft the spoken script |
| `reel anima <file> [--scena N]` | render the Manim scenes |
| `reel monta <file> [--prova] [--anteprima]` | assemble the Reel |
| `reel registra <file>` | guided recording of the presenter |
| `reel clip`, `parlato`, `gobbo`, `audio`, `pulisci` | clips, spoken text, teleprompter, audio, cleanup |
| `broll piano / cerca / genera / rendi` | stock and generated footage scenes |

## Project structure

```
├── config.toml            # sizes, palette, fonts, audio, paths
├── tools/
│   ├── anim/              # Manim library: base scene, components, diagrams, patterns
│   ├── reel/              # CLI: parser, validate, voice, compositing, captions, montage
│   └── broll/             # B-roll scenes
├── templates/             # grammar, script prompt, two worked example reels
├── contenuti/             # one folder per stage: ideas → scripts → screenplays → animations
├── docs/                  # editorial rules, screenplay grammar, animation manual
├── assets/                # fonts, placeholder avatar, Lucide icons
└── .claude/               # agents, /pipeline command, workflow, hooks
```

## Limitations

Preview output (`--prova`) uses a synthetic voice and a placeholder avatar and is **not publishable**. A real Reel needs recorded presenter clips. The screenplay grammar, the CLI and the docs are in Italian. B-roll needs API keys (`PEXELS_API_KEY` or `PIXABAY_API_KEY` for stock footage, `MESHY_API_KEY` for generated footage).

## License and credits

[MIT](LICENSE) © 2026 Flavio Cordari. Bundled fonts (Inter, JetBrains Mono: OFL) and Lucide icons (ISC) keep their own licenses.
