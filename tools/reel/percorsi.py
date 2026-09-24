"""Dove vanno i file di un reel: il riepilogo nel progetto, il lavoro transitorio fuori (dal 2026-09-23).

`contenuti/render/<slug>/` tiene solo quello che il presentatore guarda e che i comandi rileggono: `reel-9x16.mp4`,
`reel-prova.mp4`, `contact-sheet.png`, le copertine, `scene/NN.png`, i filmstrip di scena e `report.json`. Tutto il
resto — la cache e i video di Manim, le scene montate una per una, la voce di prova, le caption, le strisce fitte, i
provini dei filmati — si rigenera e va in `config.toml [percorsi] lavoro` (`~/Library/Caches/reel-anim/<slug>/`), che
`uv run reel pulisci` svuota. La cache dei filmati scaricati e delle immagini generate va invece in
`[percorsi] cache_broll`, che nessuno ripulisce da sé: dentro ci sono immagini Meshy pagate.
"""
from __future__ import annotations

from pathlib import Path

from ..anim.config import RADICE, Config, carica

LAVORO = "~/Library/Caches/reel-anim"
CACHE_BROLL = "~/Library/Application Support/reel-anim/cache-broll"


def riepilogo(slug: str, out: str | Path | None = None) -> Path:
    """La cartella del riepilogo di un reel (o quella data con `--out`)."""
    return Path(out) if out else RADICE / "contenuti" / "render" / slug


def radice_lavoro(cfg: Config | None = None) -> Path:
    cfg = cfg or carica()
    return cfg.percorso("percorsi", "lavoro") or Path(LAVORO).expanduser()


def lavoro(slug: str, cfg: Config | None = None) -> Path:
    """La cartella transitoria di un reel."""
    return radice_lavoro(cfg) / slug


def lavoro_per(slug: str, out: Path | None = None, cfg: Config | None = None) -> Path:
    """Con un `--out` esplicito (i test, le prove a mano) tutto resta insieme lì; altrimenti la cartella di lavoro."""
    if out is not None and Path(out).resolve() != riepilogo(slug).resolve():
        return Path(out)
    return lavoro(slug, cfg)


def cache_broll(cfg: Config | None = None) -> Path:
    cfg = cfg or carica()
    return cfg.percorso("percorsi", "cache_broll") or Path(CACHE_BROLL).expanduser()


def relativo(p: Path, base: Path = RADICE) -> str:
    """Relativo a `base` (la radice del repo) se ci sta dentro, altrimenti assoluto: `base / assoluto` resta lui."""
    try:
        return str(p.relative_to(base))
    except ValueError:
        return str(p)


def da_env(nome: str) -> str | None:
    """Una chiave dall'ambiente, poi dal `.env` della radice (gitignored): righe `NOME=valore`, anche con `export `."""
    import os
    if os.environ.get(nome):
        return os.environ[nome]
    env = RADICE / ".env"
    if not env.is_file():
        return None
    for riga in env.read_text(encoding="utf-8").splitlines():
        riga = riga.strip()
        if riga.startswith("#"):
            continue
        k, _, v = riga.removeprefix("export ").partition("=")
        if k.strip() == nome and v.strip().strip("'\""):
            return v.strip().strip("'\"")
    return None


def impronta(p: Path) -> str:
    """Sha256 corto del contenuto: dice se una sceneggiatura o un file delle animazioni è cambiato."""
    import hashlib
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def elementi_del_report(cartella: Path) -> dict[int, dict]:
    """Gli elementi per scena dell'ultimo montaggio (report.json, poi report-prova.json); {} se non ce n'è uno."""
    import json
    for nome in ("report.json", "report-prova.json"):
        try:
            elementi = json.loads((cartella / nome).read_text(encoding="utf-8")).get("elementi", [])
        except (OSError, ValueError):
            continue
        return {int(e["scena"]): {**e, "durata_s": float(e["durata_s"]), "inizi_frasi_s": list(e.get("inizi_frasi_s") or []),
                                  "caption": e.get("caption") or []}
                for e in elementi if e.get("scena") is not None and e.get("durata_s")}
    return {}
