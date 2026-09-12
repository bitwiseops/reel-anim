"""Voce sintetica per l'anteprima senza clip (macOS `say`, configurabile in config.toml [voce_sintetica])."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from ..anim.config import Config, carica
from .ffmpeg import ffprobe, trova_ffmpeg
from .model import testo_piano


class VoceNonDisponibile(RuntimeError):
    pass


def sintetizza(testo: str, dest: Path, cfg: Config | None = None) -> Path:
    """Genera dest (.aiff via `say`, poi convertito in .m4a 48 kHz con ffmpeg). Ritorna il file audio finale."""
    cfg = cfg or carica()
    vs = cfg.dati["voce_sintetica"]
    cmd = vs.get("comando", "say")
    if not shutil.which(cmd):
        raise VoceNonDisponibile(f"comando '{cmd}' non trovato: la voce sintetica di prova richiede macOS `say`")
    dest.parent.mkdir(parents=True, exist_ok=True)
    aiff = dest.with_suffix(".aiff")
    r = subprocess.run([cmd, "-v", str(vs.get("voce", "Alice")), "-r", str(vs.get("velocita_wpm", 170)),
                        "-o", str(aiff), testo_piano(testo)], capture_output=True, text=True)
    if r.returncode != 0 or not aiff.exists():
        raise VoceNonDisponibile(f"{cmd} ha fallito: {r.stderr.strip()[-300:]}")
    ff, _ = trova_ffmpeg()
    out = dest.with_suffix(".m4a")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(aiff), "-af", "aresample=48000", "-c:a", "aac", "-b:a", "128k", str(out)], check=True)
    aiff.unlink(missing_ok=True)
    return out


def durata_s(audio: Path) -> float:
    return float(ffprobe(audio).get("durata_s") or 0.0)
