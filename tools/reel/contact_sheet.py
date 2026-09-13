"""Contact sheet con Pillow: miniature in griglia, etichette, diagnostiche in fondo (copiato da io-e-lia)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .model import Diagnostica

FONT = Path(__file__).resolve().parents[2] / "assets" / "fonts" / "InterVariable.ttf"


def _font(size: int):
    try:
        return ImageFont.truetype(str(FONT), size)
    except OSError:
        return ImageFont.load_default()


def genera(elementi: list[dict], diagnostiche: list[Diagnostica], dest: Path, colonne: int = 3,
           larghezza_cella: int = 360) -> Path:
    """elementi: [{file, etichetta, animata: bool, problema: bool, ratio: float}]"""
    margine, gap, testa = 30, 24, 90
    h_cella = int(larghezza_cella * 1.25)
    righe = (len(elementi) + colonne - 1) // colonne
    h_diag = 40 + 34 * max(1, len(diagnostiche))
    W = margine * 2 + colonne * larghezza_cella + (colonne - 1) * gap
    H = margine * 2 + righe * (h_cella + testa + gap) + h_diag
    img = Image.new("RGB", (W, H), (246, 243, 238))
    d = ImageDraw.Draw(img)
    f_et, f_diag = _font(26), _font(24)
    for k, e in enumerate(elementi):
        r, c = divmod(k, colonne)
        x = margine + c * (larghezza_cella + gap)
        y = margine + r * (h_cella + testa + gap)
        try:
            mini = Image.open(e["file"]).convert("RGB")
            ratio = mini.height / mini.width
            mw = larghezza_cella if ratio >= 1.25 else larghezza_cella
            mh = int(mw * ratio)
            if mh > h_cella:
                mh = h_cella
                mw = int(mh / ratio)
            mini = mini.resize((mw, mh), Image.LANCZOS)
            img.paste(mini, (x + (larghezza_cella - mw) // 2, y))
        except (OSError, FileNotFoundError):
            d.rectangle((x, y, x + larghezza_cella, y + h_cella), fill=(220, 214, 204))
        bordo = (220, 60, 60) if e.get("problema") else (200, 195, 188)
        d.rectangle((x - 2, y - 2, x + larghezza_cella + 2, y + h_cella + 2), outline=bordo, width=4 if e.get("problema") else 2)
        if e.get("animata"):
            cx, cy = x + larghezza_cella - 36, y + 36
            d.ellipse((cx - 26, cy - 26, cx + 26, cy + 26), fill=(30, 27, 34))
            d.polygon([(cx - 9, cy - 14), (cx - 9, cy + 14), (cx + 15, cy)], fill=(255, 255, 255))
        d.text((x, y + h_cella + 14), e["etichetta"], font=f_et, fill=(30, 27, 34))
    y = margine + righe * (h_cella + testa + gap) + 10
    if not diagnostiche:
        d.text((margine, y), "Nessun avviso.", font=f_diag, fill=(60, 140, 80))
    for k, diag in enumerate(diagnostiche):
        col = (200, 40, 40) if diag.livello == "errore" else (170, 110, 20)
        d.text((margine, y + k * 34), str(diag)[:150], font=f_diag, fill=col)
    dest.parent.mkdir(parents=True, exist_ok=True)
    img.save(dest)
    return dest
