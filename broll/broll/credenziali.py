"""Le chiavi dei servizi esterni, lette senza mai stamparle.

Ordine: variabili d'ambiente, poi `.env` nella radice del repo, poi `config.local.toml` sezione
`[broll]`. Tutti e tre sono fuori da git (`.gitignore`: `.env`, `config.local.toml`).

I nomi sono quelli **già in uso** in `~/Projects/3d-models-ai` (`MESHY_API_KEY`, con la fallback che
quel progetto usa quando la principale esaurisce i crediti): così la stessa chiave serve entrambi i
progetti invece di esistere in due posti con due nomi diversi.
"""
from __future__ import annotations

import os
from pathlib import Path

from tools.anim.config import Config, carica

RADICE = Path(__file__).resolve().parents[2]

# fornitore -> (chiave principale, chiavi di riserva…)
FORNITORI: dict[str, tuple[str, ...]] = {
    "meshy": ("MESHY_API_KEY", "MESHY_API_KEY_FALLBACK"),
    "pexels": ("PEXELS_API_KEY",),
    "pixabay": ("PIXABAY_API_KEY",),
}

# A cosa serve ciascuno. Nessuna chiave è obbligatoria di per sé: serve **almeno un fornitore di
# ricerca**, e la generazione è in più. Pixabay è un secondo banco di filmati, non un requisito.
RUOLI: dict[str, str] = {"pexels": "ricerca", "pixabay": "ricerca", "meshy": "generazione"}


def configurati(ruolo: str, cfg: Config | None = None) -> list[str]:
    """I fornitori di quel ruolo che hanno almeno una chiave."""
    return [f for f, r in RUOLI.items() if r == ruolo and chiavi(f, cfg)]


def _da_env_file(nome: str) -> str | None:
    """Legge una riga `NOME=valore` dal `.env` della radice. Nessuna dipendenza: il formato che serve
    qui è una riga per chiave, come in `3d-models-ai/.env`."""
    f = RADICE / ".env"
    if not f.exists():
        return None
    try:
        righe = f.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    for riga in righe:
        riga = riga.strip()
        if riga.startswith(f"{nome}=") and not riga.startswith("#"):
            v = riga.split("=", 1)[1].strip().strip("'\"")
            return v or None
    return None


def chiave(nome: str, cfg: Config | None = None) -> str | None:
    """Il valore di una chiave, o None. Non stamparlo: per mostrarlo usa `mascherata`."""
    v = os.environ.get(nome)
    if v:
        return v
    v = _da_env_file(nome)
    if v:
        return v
    cfg = cfg or carica()
    return (cfg.dati.get("broll", {}) or {}).get(nome.lower()) or None


def chiavi(fornitore: str, cfg: Config | None = None) -> list[str]:
    """Tutte le chiavi utilizzabili per un fornitore, principale per prima (come `meshy_api_keys()`
    in 3d-models-ai: la riserva entra in gioco quando la prima esaurisce i crediti)."""
    return [v for n in FORNITORI.get(fornitore, ()) if (v := chiave(n, cfg))]


def mascherata(v: str | None) -> str:
    """Quanto basta a riconoscerla, non abbastanza da usarla."""
    if not v:
        return "—"
    return f"{v[:4]}… ({len(v)} caratteri)"


def dove(nome: str) -> str:
    if os.environ.get(nome):
        return "ambiente"
    if _da_env_file(nome):
        return ".env"
    return "config.local.toml" if chiave(nome) else "—"


def stato(cfg: Config | None = None) -> list[dict]:
    return [{"fornitore": f, "ruolo": RUOLI.get(f, ""), "nome": n, "valore": chiave(n, cfg),
             "dove": dove(n)}
            for f, nomi in FORNITORI.items() for n in nomi]
