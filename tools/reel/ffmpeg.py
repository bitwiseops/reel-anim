"""ffmpeg/ffprobe di sistema: ricerca, probe dei file, filmstrip con Pillow (adattato da io-e-lia/tools/render/video.py)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RADICE = Path(__file__).resolve().parents[2]


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
                              "stream=index,codec_type,codec_name,width,height,pix_fmt,sample_rate,channels:stream_side_data=rotation:format=duration",
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
            "durata_s": round(float(j.get("format", {}).get("duration", 0) or 0), 2)}


def _font(size: int):
    try:
        return ImageFont.truetype(str(RADICE / "assets" / "fonts" / "InterVariable.ttf"), size)
    except OSError:
        return ImageFont.load_default()


def estrai_fotogramma(video: Path, t_s: float, dest: Path) -> Path:
    """Un PNG del video all'istante t_s."""
    ff, _ = trova_ffmpeg()
    dest.parent.mkdir(parents=True, exist_ok=True)
    for t in (t_s, t_s - 0.1, t_s - 0.5):   # a fine file ffmpeg può non trovare fotogrammi: arretra un po'
        esegui([ff, "-y", "-loglevel", "error", "-ss", f"{max(0.0, t):.3f}", "-i", str(video), "-frames:v", "1", str(dest)], "ffmpeg (fotogramma)")
        if dest.exists():
            return dest
    raise RuntimeError(f"nessun fotogramma estraibile da {video} a {t_s:.2f} s")


def filmstrip(video: Path, tempi_s: list[float], dest: Path, larghezza: int = 300) -> Path:
    """Striscia di fotogrammi del video agli istanti dati, con l'etichetta del tempo sopra ciascuno."""
    imgs = []
    tmp = dest.parent / f"_{dest.stem}"
    tmp.mkdir(parents=True, exist_ok=True)
    for k, t in enumerate(tempi_s):
        p = estrai_fotogramma(video, t, tmp / f"{k:02d}.png")
        imgs.append(Image.open(p).convert("RGB"))
    if not imgs:
        return dest
    ratio = imgs[0].height / imgs[0].width
    h = int(larghezza * ratio)
    gap, testa = 12, 34
    W = len(imgs) * larghezza + (len(imgs) - 1) * gap
    out = Image.new("RGB", (W, h + testa), (246, 243, 238))
    d = ImageDraw.Draw(out)
    f = _font(22)
    for k, (im, t) in enumerate(zip(imgs, tempi_s)):
        x = k * (larghezza + gap)
        out.paste(im.resize((larghezza, h), Image.LANCZOS), (x, testa))
        d.text((x, 4), f"{t:.1f} s", font=f, fill=(30, 27, 34))
    out.save(dest)
    shutil.rmtree(tmp, ignore_errors=True)
    return dest


def tempi_campione(durata_s: float, quanti: int = 6) -> list[float]:
    if quanti <= 1 or durata_s <= 0:
        return [0.0]
    fine = max(0.0, durata_s - 0.05)
    return [round(k * fine / (quanti - 1), 3) for k in range(quanti)]
