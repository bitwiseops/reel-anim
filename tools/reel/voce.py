"""Voce sintetica per l'anteprima senza clip (macOS `say`, configurabile in config.toml [voce_sintetica]).

Si sintetizza una frase della VOCE alla volta: ogni frase diventa un WAV in cache, poi le frasi si uniscono con una
pausa fissa (`pausa_frasi_s`). Così l'istante in cui comincia ogni frase è noto al campione e `ScenaReel.beat(i)`
cade proprio sulla frase i.
"""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import wave
from pathlib import Path
from typing import NamedTuple

from ..anim.config import Config, carica
from .ffmpeg import ffprobe, trova_ffmpeg
from .model import testo_piano

FREQUENZA = 48000
CODA_VOCE_S = 0.5   # silenzio che il montaggio lascia dopo l'ultima frase di una scena con voce sintetica


class VoceNonDisponibile(RuntimeError):
    pass


class VoceFrasi(NamedTuple):
    audio: Path            # m4a AAC 48 kHz
    inizi_s: list[float]   # istante d'inizio di ogni frase nell'audio
    durata_s: float        # durata dell'audio (senza la coda aggiunta dal montaggio)


def _say(cfg: Config) -> tuple[str, str, str]:
    vs = cfg.dati["voce_sintetica"]
    cmd = str(vs.get("comando", "say"))
    if not shutil.which(cmd):
        raise VoceNonDisponibile(f"comando '{cmd}' non trovato: la voce sintetica di prova richiede macOS `say`")
    return cmd, str(vs.get("voce", "Alice")), str(vs.get("velocita_wpm", 170))


def sintetizza_frase(frase: str, cartella: Path, cfg: Config | None = None) -> Path:
    """Una frase → WAV 48 kHz mono 16 bit, in cache per (comando, voce, velocità, testo): `say` gira una volta sola."""
    cfg = cfg or carica()
    cmd, voce, wpm = _say(cfg)
    testo = testo_piano(frase).strip()
    chiave = hashlib.sha256(f"v1|{cmd}|{voce}|{wpm}|{testo}".encode("utf-8")).hexdigest()[:16]
    dest = cartella / f"{chiave}.wav"
    if dest.exists():
        return dest
    cartella.mkdir(parents=True, exist_ok=True)
    aiff = dest.with_suffix(".aiff")
    r = subprocess.run([cmd, "-v", voce, "-r", wpm, "-o", str(aiff), testo], capture_output=True, text=True)
    if r.returncode != 0 or not aiff.exists():
        raise VoceNonDisponibile(f"{cmd} ha fallito: {r.stderr.strip()[-300:]}")
    ff, _ = trova_ffmpeg()
    tmp = dest.with_name(f"{chiave}.tmp.wav")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(aiff), "-ar", str(FREQUENZA), "-ac", "1", "-c:a", "pcm_s16le",
                    str(tmp)], check=True)
    tmp.replace(dest)   # un file a metà non finisce mai in cache
    aiff.unlink(missing_ok=True)
    return dest


def unisci_wav(pezzi: list[Path], pausa_s: float, dest: Path) -> tuple[list[float], float]:
    """Concatena WAV dello stesso formato con `pausa_s` di silenzio tra un pezzo e l'altro.
    Ritorna (inizi_s, durata_s), calcolati sul numero di campioni (esatti, arrotondati al millisecondo)."""
    if not pezzi:
        raise ValueError("nessuna frase da unire")
    dest.parent.mkdir(parents=True, exist_ok=True)
    inizi: list[float] = []
    campioni = 0
    formato: tuple[int, int, int] | None = None
    with wave.open(str(dest), "wb") as out:
        for k, p in enumerate(pezzi):
            with wave.open(str(p), "rb") as w:
                f = (w.getnchannels(), w.getsampwidth(), w.getframerate())
                if formato is None:
                    formato = f
                    out.setnchannels(f[0])
                    out.setsampwidth(f[1])
                    out.setframerate(f[2])
                elif f != formato:
                    raise ValueError(f"{p.name}: formato (canali, byte, Hz) {f} diverso da {formato}")
                if k:
                    silenzio = round(pausa_s * f[2])
                    out.writeframes(b"\x00" * silenzio * f[0] * f[1])
                    campioni += silenzio
                inizi.append(round(campioni / f[2], 3))
                n = w.getnframes()
                out.writeframes(w.readframes(n))
                campioni += n
    assert formato is not None
    return inizi, round(campioni / formato[2], 3)


def sintetizza_frasi(frasi: list[str], dest: Path, cfg: Config | None = None) -> VoceFrasi:
    """Voce di una scena: una frase alla volta (in cache), unite con la pausa del config, codificate in `dest` (.m4a)."""
    cfg = cfg or carica()
    if not frasi:
        raise ValueError("nessuna frase da sintetizzare")
    pezzi = [sintetizza_frase(f, dest.parent / "frasi", cfg) for f in frasi]
    pausa = float(cfg.dati["voce_sintetica"].get("pausa_frasi_s", 0.3))
    wav = dest.with_suffix(".wav")
    inizi, durata = unisci_wav(pezzi, pausa, wav)
    ff, _ = trova_ffmpeg()
    audio = dest.with_suffix(".m4a")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(wav), "-af", f"aresample={FREQUENZA}", "-c:a", "aac",
                    "-b:a", "128k", str(audio)], check=True)
    wav.unlink(missing_ok=True)
    return VoceFrasi(audio, inizi, durata)


def durata_s(audio: Path) -> float:
    return float(ffprobe(audio).get("durata_s") or 0.0)
