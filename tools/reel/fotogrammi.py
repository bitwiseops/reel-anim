"""Fotogrammi chiave, filmstrip e cover: ciò che Claude Code (che non vede il video) guarda al posto del video."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from ..anim.config import Config, carica
from .ffmpeg import estrai_fotogramma, filmstrip, tempi_campione
from .model import testo_piano


def ritaglio_4x5(cfg: Config) -> tuple[int, int, int, int]:
    """Banda centrale 4:5 della tela 9:16 (1080x1350 su 1080x1920)."""
    h = int(cfg.larghezza * 5 / 4)
    y = (cfg.altezza - h) // 2
    return (0, y, cfg.larghezza, y + h)


def fotogramma_chiave(video: Path, durata_s: float, dest: Path, frazione: float = 0.6) -> Path:
    return estrai_fotogramma(video, durata_s * frazione, dest)


def filmstrip_scena(video: Path, durata_s: float, dest: Path, quanti: int = 6) -> Path:
    return filmstrip(video, tempi_campione(durata_s, quanti), dest, 300)


VELO = 0.58             # quanto si scurisce il fotogramma sotto il titolo: deve leggersi in una griglia di miniature
CORPO_TITOLO_PX, CORPO_SOTTOTITOLO_PX = 104, 76


def _font_titolo(cfg: Config, corpo: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    try:
        font = ImageFont.truetype(str(cfg.font_file()[0]), corpo)
    except OSError:
        return ImageFont.load_default()
    try:
        # Inter Variable ha più assi (opsz, wght): si tocca solo il peso, gli altri restano al loro default
        assi = font.get_variation_axes()
        nome = lambda a: (a["name"].decode() if isinstance(a["name"], bytes) else str(a["name"])).lower()  # noqa: E731
        font.set_variation_by_axes([min(800, a["maximum"]) if nome(a) in ("weight", "wght") else a["default"] for a in assi])
    except (OSError, AttributeError, ValueError):
        pass
    return font


def _a_capo(d: ImageDraw.ImageDraw, testo: str, font, larghezza: int) -> list[str]:
    righe, riga = [], ""
    for parola in testo.split():
        prova = f"{riga} {parola}".strip()
        if riga and d.textlength(prova, font=font) > larghezza:
            righe.append(riga)
            riga = parola
        else:
            riga = prova
    return righe + [riga] if riga else righe


def titola(immagine: Path, titolo: str, sottotitolo: str | None, cfg: Config) -> Path:
    """Scrive TITOLO e SOTTOTITOLO sopra un fotogramma, dentro la banda 4:5 (quella che si vede nella griglia).

    Serve all'hook a filmato: a schermo lì non c'è nessun titolo, quindi la copertina non può più essere un
    fotogramma dell'hook e basta. È l'unico punto in cui un testo sta sopra il filmato, ed è un'immagine ferma.
    Con Pillow, come le altre scritte del repo (questo ffmpeg non ha `drawtext`).
    """
    p, s = cfg.palette, cfg.dati["safe_area"]
    im = Image.open(immagine).convert("RGB")
    im = Image.blend(im, Image.new("RGB", im.size, p.sfondo), VELO)
    d = ImageDraw.Draw(im)
    x = int(s.get("sinistra", 60)) + 24
    larghezza = cfg.larghezza - x - int(s.get("sinistra", 60)) - 24
    _, alto, _, basso = ritaglio_4x5(cfg)
    blocchi = [(testo_piano(titolo).upper(), _font_titolo(cfg, CORPO_TITOLO_PX), p.testo)]
    if sottotitolo:
        blocchi.append((testo_piano(sottotitolo).upper(), _font_titolo(cfg, CORPO_SOTTOTITOLO_PX), p.accento))
    righe = [(r, font, colore) for testo, font, colore in blocchi for r in _a_capo(d, testo, font, larghezza)]
    interlinea = 1.12
    altezza = sum(int(font.size * interlinea) for _, font, _ in righe) + (40 if sottotitolo else 0)
    y = alto + max(60, (basso - alto - altezza) // 3)       # un terzo dall'alto: sotto resta il volto nel riquadro
    ultimo = righe[0][1]
    for r, font, colore in righe:
        if font is not ultimo:
            y += 40
            ultimo = font
        d.text((x, y), r, font=font, fill=colore)
        y += int(font.size * interlinea)
    im.save(immagine)
    return immagine


def cover(video_hook: Path, durata_s: float, out: Path, cfg: Config | None = None, frazione: float = 0.97,
          titolo: str | None = None, sottotitolo: str | None = None) -> tuple[Path, Path]:
    """Copertina: l'ultimo fotogramma dell'hook, quando titolo e sottotitolo sono tutti in scena (al 70 % cadeva
    sull'ingresso del sottotitolo). Con `titolo` (hook a filmato: a schermo il titolo non c'è) si prende un
    fotogramma a metà della clip e il titolo ce lo si scrive sopra."""
    cfg = cfg or carica()
    intera = estrai_fotogramma(video_hook, durata_s * (0.5 if titolo else frazione), out / "copertina.png")
    if titolo:
        titola(intera, titolo, sottotitolo, cfg)
    ritagliata = out / "copertina-4x5.png"
    Image.open(intera).crop(ritaglio_4x5(cfg)).save(ritagliata)
    return intera, ritagliata
