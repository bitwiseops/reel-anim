"""ffmpeg/ffprobe di sistema: ricerca, probe dei file, filmstrip con Pillow (adattato da io-e-lia/tools/render/video.py)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections.abc import Callable
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from ..anim.config import RADICE


class FfmpegMancante(RuntimeError):
    pass


def trova_ffmpeg() -> tuple[str, str]:
    """Ritorna (ffmpeg, ffprobe). Ordine: REEL_FFMPEG, poi il PATH (Homebrew)."""
    env = os.environ.get("REEL_FFMPEG")
    if env and Path(env).exists():
        probe = Path(env).with_name("ffprobe")
        return env, str(probe) if probe.exists() else "ffprobe"
    ff = shutil.which("ffmpeg")
    if ff:
        return ff, shutil.which("ffprobe") or "ffprobe"
    raise FfmpegMancante("ffmpeg non trovato: `brew install ffmpeg`")


def esegui(cmd: list[str], descrizione: str = "ffmpeg") -> None:
    """Esegue ffmpeg/ffprobe con loglevel error; solleva RuntimeError con la coda dello stderr se fallisce."""
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{descrizione} ha fallito ({r.returncode}): {r.stderr.strip()[-800:]}")


def ffprobe(path: Path) -> dict:
    """Dimensioni, codec, pix_fmt, rotazione, audio e durata del file; {'errore': ...} se non leggibile."""
    _, probe = trova_ffmpeg()
    try:
        out = subprocess.run([probe, "-v", "error", "-show_entries",
                              "stream=index,codec_type,codec_name,width,height,pix_fmt,sample_rate,channels,start_time,nb_frames:stream_side_data=rotation:format=duration",
                              "-of", "json", str(path)], capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return {"errore": str(e)}
    j = json.loads(out)
    video = next((s for s in j.get("streams", []) if s.get("codec_type") == "video"), {})
    audio = next((s for s in j.get("streams", []) if s.get("codec_type") == "audio"), None)
    rot = 0
    for sd in video.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    w, h = video.get("width"), video.get("height")
    if rot in (90, -90, 270, -270) and w and h:
        w, h = h, w
    return {"larghezza": w, "altezza": h, "codec": video.get("codec_name"), "pix_fmt": video.get("pix_fmt"),
            "rotazione": rot, "audio": audio.get("codec_name") if audio else None,
            "audio_hz": int(audio["sample_rate"]) if audio and audio.get("sample_rate") else None,
            "audio_canali": int(audio["channels"]) if audio and audio.get("channels") else None,
            "durata_s": round(float(j.get("format", {}).get("duration", 0) or 0), 2),
            # il muxer mov può far partire il video dopo lo 0 se il primo pacchetto audio lo precede: serve a `registra`
            "inizio_video_s": float(video.get("start_time") or 0),
            "fotogrammi": int(video["nb_frames"]) if str(video.get("nb_frames", "")).isdigit() else None}


def font_etichette(size: int):
    try:
        return ImageFont.truetype(str(RADICE / "assets" / "fonts" / "InterVariable.ttf"), size)
    except OSError:
        return ImageFont.load_default()


def estrai_fotogramma(video: Path, t_s: float, dest: Path, copri: Callable | None = None) -> Path:
    """Un PNG del video all'istante t_s. `copri(immagine, t_s) -> immagine` lo passa prima di lasciarlo su disco
    (il volto del presentatore nelle immagini di controllo: `fotogrammi.copri_volto`)."""
    ff, _ = trova_ffmpeg()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for t in (t_s, t_s - 0.1, t_s - 0.5):   # a fine file ffmpeg può non trovare fotogrammi: arretra un po'
        esegui([ff, "-y", "-loglevel", "error", "-ss", f"{max(0.0, t):.3f}", "-i", str(video), "-frames:v", "1", str(dest)], "ffmpeg (fotogramma)")
        if dest.exists():
            if copri is not None:
                copri(Image.open(dest).convert("RGB"), t_s).save(dest)
            return dest
    raise RuntimeError(f"nessun fotogramma estraibile da {video} a {t_s:.2f} s")


def filmstrip(video: Path, tempi_s: list[float], dest: Path, larghezza: int = 300, per_riga: int | None = None,
              decimali: int = 1, copri: Callable | None = None) -> Path:
    """Striscia di fotogrammi del video agli istanti dati, con l'etichetta del tempo sopra ciascuno.
    Con `per_riga` va a capo su più righe (le strisce fitte: tante miniature in un'immagine che resti leggibile)."""
    imgs = []
    tmp = dest.parent / f"_{dest.stem}"
    tmp.mkdir(parents=True, exist_ok=True)
    for k, t in enumerate(tempi_s):
        p = estrai_fotogramma(video, t, tmp / f"{k:02d}.png", copri)
        im = Image.open(p).convert("RGB")
        # ridotta subito: una striscia fitta ha decine di fotogrammi, a piena risoluzione sono centinaia di MB
        imgs.append(im.resize((larghezza, int(larghezza * im.height / im.width)), Image.LANCZOS))
    if not imgs:
        return dest
    h = imgs[0].height
    gap, testa = 12, 34
    colonne = min(len(imgs), per_riga or len(imgs))
    righe = -(-len(imgs) // colonne)
    W = colonne * larghezza + (colonne - 1) * gap
    out = Image.new("RGB", (W, righe * (h + testa) + (righe - 1) * gap), (246, 243, 238))
    d = ImageDraw.Draw(out)
    f = font_etichette(22)
    for k, (im, t) in enumerate(zip(imgs, tempi_s)):
        x, y = (k % colonne) * (larghezza + gap), (k // colonne) * (h + testa + gap)
        out.paste(im, (x, y + testa))
        d.text((x, y + 4), f"{t:.{decimali}f} s", font=f, fill=(30, 27, 34))
    out.save(dest)
    shutil.rmtree(tmp, ignore_errors=True)
    return dest


def tempi_campione(durata_s: float, quanti: int = 6) -> list[float]:
    if quanti <= 1 or durata_s <= 0:
        return [0.0]
    fine = max(0.0, durata_s - 0.05)
    return [round(k * fine / (quanti - 1), 3) for k in range(quanti)]
