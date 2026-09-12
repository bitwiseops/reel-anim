import subprocess
from pathlib import Path

import pytest

from tools.reel.ffmpeg import ffprobe, filmstrip, tempi_campione, trova_ffmpeg


@pytest.fixture(scope="module")
def clip(tmp_path_factory) -> Path:
    ff, _ = trova_ffmpeg()
    dest = tmp_path_factory.mktemp("clip") / "c.mp4"
    subprocess.run([ff, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=red:s=270x480:r=30:d=2",
                    "-f", "lavfi", "-i", "sine=frequency=440:duration=2", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-shortest", str(dest)], check=True)
    return dest


def test_ffprobe(clip):
    p = ffprobe(clip)
    assert (p["larghezza"], p["altezza"], p["codec"], p["pix_fmt"], p["audio"]) == (270, 480, "h264", "yuv420p", "aac")
    assert abs(p["durata_s"] - 2.0) < 0.1 and p["rotazione"] == 0
    assert "errore" in ffprobe(clip.with_name("nope.mp4"))


def test_filmstrip_e_tempi(clip, tmp_path):
    t = tempi_campione(2.0, 4)
    assert t[0] == 0 and t[-1] < 2.0 and len(t) == 4
    out = filmstrip(clip, t, tmp_path / "f.png", 100)
    from PIL import Image
    im = Image.open(out)
    assert im.width == 4 * 100 + 3 * 12 and im.height > 100
