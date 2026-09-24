"""Rigenera chat-fotocopiatrice.png, il b-roll di esempio della scena 6: una chat generica (nessun marchio) grande
quanto l'area [schermo] del config. Uso: uv run python templates/esempio-reel/media/genera_chat.py
Stampa le bolle in px dell'immagine: servono ad area_px() nella scena (immagine posata in [schermo] x, y)."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from tools.anim.config import RADICE, carica

cfg = carica()
W, H = int(cfg.dati["schermo"]["larghezza"]), int(cfg.dati["schermo"]["altezza"])
F = str(RADICE / "assets" / "fonts" / "InterVariable.ttf")
f, fb = ImageFont.truetype(F, 40), ImageFont.truetype(F, 30)
im = Image.new("RGB", (W, H), "#1B1E26")
d = ImageDraw.Draw(im)
d.rectangle((0, 0, W, 96), fill="#232733")
d.text((40, 48), "Chat", font=fb, fill="#9A9DAB", anchor="lm")


def righe(testo, larg):
    out, cur = [], ""
    for p in testo.split():
        t = (cur + " " + p).strip()
        if d.textlength(t, font=f) > larg and cur:
            out.append(cur)
            cur = p
        else:
            cur = t
    return out + [cur]


def bolla(testo, y, destra, colore):
    pad, lh = 32, 54
    rr = righe(testo, W - 300)
    w = max(d.textlength(r, font=f) for r in rr) + 2 * pad
    h = len(rr) * lh + 2 * pad - 8
    x0 = W - 40 - w if destra else 40
    d.rounded_rectangle((x0, y, x0 + w, y + h), radius=34, fill=colore)
    for k, r in enumerate(rr):
        d.text((x0 + pad, y + pad + k * lh), r, font=f, fill="#F2F2F5")
    return int(x0), int(y), int(x0 + w), int(y + h)


b1 = bolla("Due righe per il biglietto di Marco. Scarta le prime tre idee.", 140, True, "#2B3A5C")
b2 = bolla("Marco ha passato una vita a litigare con la fotocopiatrice.", b1[3] + 24, True, "#2B3A5C")
b3 = bolla("Caro Marco, la fotocopiatrice ha chiesto di te. Le ho detto che da lunedì sei libero. Lei no.", b2[3] + 56, False, "#262A33")
im.save(Path(__file__).with_name("chat-fotocopiatrice.png"))
print(f"{W}x{H}  bolle: {b1} {b2} {b3}")
