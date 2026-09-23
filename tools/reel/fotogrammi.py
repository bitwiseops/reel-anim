"""Fotogrammi chiave, filmstrip e cover: ciò che Claude Code (che non vede il video) guarda al posto del video."""
from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from ..anim.config import Config, carica
from .ffmpeg import estrai_fotogramma, filmstrip, tempi_campione
from .model import PIENO, testo_piano


def ritaglio_4x5(cfg: Config) -> tuple[int, int, int, int]:
    """Banda centrale 4:5 della tela 9:16 (1080x1350 su 1080x1920)."""
    h = int(cfg.larghezza * 5 / 4)
    y = (cfg.altezza - h) // 2
    return (0, y, cfg.larghezza, y + h)


def fotogramma_chiave(video: Path, durata_s: float, dest: Path, frazione: float = 0.6, copri: Callable | None = None) -> Path:
    return estrai_fotogramma(video, durata_s * frazione, dest, copri)


def filmstrip_scena(video: Path, durata_s: float, dest: Path, quanti: int = 6, copri: Callable | None = None) -> Path:
    return filmstrip(video, tempi_campione(durata_s, quanti), dest, 300, copri=copri)


# --- il volto del presentatore nelle immagini di controllo ------------------------------------------------------
# Regola del presentatore (2026-09-22): il suo volto lo guarda solo lui. Con le clip vere i fotogrammi che legge
# Claude (scene/NN.png, filmstrip, strisce, contact sheet) si scrivono già coperti: nel riquadro torna l'avatar
# segnaposto del `--prova`, e una scena a volto pieno diventa un cartello con le caption di quell'istante.

def copri_volto(cfg: Config, riquadro: str, avatar: Path, caption: list[dict] | None = None) -> Callable | None:
    """La funzione `copri(immagine, t) -> immagine` per una scena montata con la clip vera; None se non c'è niente
    da coprire (scena senza riquadro). `caption` = i blocchi del report ({testo, t0, t1}), per le scene a volto pieno."""
    if riquadro == "no":
        return None
    from .compositing import maschera_riquadro, posizione_riquadro
    pal = cfg.palette
    faccia = Image.open(avatar).convert("RGB") if avatar.exists() else None

    def copri(im: Image.Image, t: float) -> Image.Image:
        k = im.width / cfg.larghezza
        if riquadro == PIENO:
            out = Image.new("RGB", im.size, pal.sfondo)
            if faccia is not None:
                lato = int(im.width * 0.5)
                out.paste(faccia.resize((lato, lato)), ((im.width - lato) // 2, int(im.height * 0.22)))
            d = ImageDraw.Draw(out)
            d.text((int(40 * k), int(40 * k)), "volto pieno (coperto)", font=font_pesato(cfg, max(12, int(44 * k)), 700), fill=pal.attenuato)
            attiva = next((c["testo"] for c in caption or [] if c["t0"] <= t < c["t1"]), "")
            if attiva:
                f = font_pesato(cfg, max(12, int(52 * k)), 700)
                y = int(im.height * 0.62)
                for riga in a_capo(d, attiva, f, int(im.width * 0.84)):
                    d.text((int(im.width * 0.08), y), riga, font=f, fill=pal.testo)
                    y += int(66 * k)
            return out
        x, y, lato = (round(v * k) for v in posizione_riquadro(cfg, riquadro))
        maschera = Image.open(maschera_riquadro(cfg)).convert("L").resize((lato, lato))
        riempi = faccia.resize((lato, lato)) if faccia is not None else Image.new("RGB", (lato, lato), pal.secondario)
        im.paste(riempi, (x, y), maschera)
        return im
    return copri


def cartello(dest: Path, testo: str, cfg: Config | None = None) -> Path:
    """Un'immagine 4:5 con una scritta: al posto di ciò che Claude non deve guardare (la copertina con il volto)."""
    cfg = cfg or carica()
    im = Image.new("RGB", (1080, 1350), cfg.palette.sfondo)
    d = ImageDraw.Draw(im)
    d.multiline_text((80, 560), testo, font=font_pesato(cfg, 64, 700), fill=cfg.palette.attenuato, spacing=20)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im.save(dest)
    return dest


def copri_reel(cfg: Config, elementi: list[dict], avatar: Path) -> Callable | None:
    """`copri` per il reel intero: sceglie la scena dall'istante (t_inizio_s/t_fine_s degli elementi del report)."""
    per_scena = [(e["t_inizio_s"], e["t_fine_s"], copri_volto(cfg, e.get("riquadro", "no"), avatar, e.get("caption")))
                 for e in elementi if e.get("clip_vera")]
    if not per_scena:
        return None

    def copri(im: Image.Image, t: float) -> Image.Image:
        for t0, t1, f in per_scena:
            if t0 <= t < t1 and f is not None:
                return f(im, t - t0)
        return im
    return copri


ANTICIPO_FITTI_S = 0.2   # la finestra parte poco prima della frase: `beat(i)` anticipa, e lì esce il beat di prima
FPS_SCENA_FITTA = 4


def _campiona(t0: float, t1: float, fps: float) -> list[float]:
    return [round(t0 + k / fps, 3) for k in range(int((t1 - t0) * fps + 1e-6) + 1)]


def tempi_fitti(inizi_frasi_s: list[float], durata_s: float, fps: float = 8, finestra_s: float = 1.3) -> list[list[float]]:
    """Gli istanti da guardare attorno a ogni passaggio: per ogni inizio di beat una finestra di `finestra_s` secondi che
    parte ANTICIPO_FITTI_S prima, tagliata a [0, durata] e campionata a `fps`. Una lista per beat (vuota se cade fuori)."""
    fine = max(0.0, durata_s - 0.05)    # come `tempi_campione`: sull'ultimo istante ffmpeg può non trovare fotogrammi
    out = []
    for b in inizi_frasi_s:
        t0 = max(0.0, b - ANTICIPO_FITTI_S)
        out.append(_campiona(t0, min(fine, t0 + finestra_s), fps) if t0 <= fine and fps > 0 else [])
    return out


def strisce_fitte(video: Path, durata_s: float, inizi_frasi_s: list[float], cartella: Path, n: int, fps: float = 8,
                  finestra_s: float = 1.3, sorgente: str = "scene", copri: Callable | None = None) -> list[Path]:
    """Le strisce di fotogrammi fitti della scena n: `NN-fitti-b<i>.png` per il passaggio di ogni beat (i come in
    `beat(i)`) e `NN-fitti-scena.png` con tutta la scena a 4 fps. Il filmstrip a 6 istanti e i controlli a fine beat
    non vedono un testo che ne attraversa un altro o lampeggia *durante* un'animazione: qui sì, con l'istante scritto
    sopra ogni miniatura (due decimali: a 8 fps il passo è 0,125 s). Con la sorgente `anima` i nomi sono
    `NN-fitti-anima-…`, così non sovrascrivono quelli della scena montata (che legge il `controllore-fotogrammi`)."""
    base = f"{n:02d}-fitti-" + ("" if sorgente == "scene" else f"{sorgente}-")
    out = []
    for i, tempi in enumerate(tempi_fitti(inizi_frasi_s, durata_s, fps, finestra_s)):
        if tempi:
            out.append(filmstrip(video, tempi, cartella / f"{base}b{i}.png", 270, per_riga=6, decimali=2, copri=copri))
    intera = _campiona(0.0, max(0.0, durata_s - 0.05), FPS_SCENA_FITTA)
    return out + [filmstrip(video, intera, cartella / f"{base}scena.png", 180, per_riga=10, decimali=2, copri=copri)]


def video_scena(out: Path, n: int, sorgente: str = "scene") -> Path | None:
    """Il video della scena n nella cartella di lavoro (`percorsi.lavoro`): `scene` = la scena montata (riquadro e caption compresi),
    `anima` = la sola grafica di `reel anima` (Manim la lascia in _anima/videos/<risoluzione>/: vale la più recente)."""
    if sorgente == "scene":
        p = out / "_scene" / f"{n:02d}.mp4"
        return p if p.exists() else None
    trovati = sorted((out / "_anima" / "videos").glob(f"*/scena-{n:02d}.mp4"), key=lambda p: p.stat().st_mtime)
    return trovati[-1] if trovati else None


def tempi_dal_report(out: Path) -> dict[int, dict]:
    """Per scena `durata_s` e `inizi_frasi_s` dell'ultimo montaggio (report.json, poi report-prova.json): sono gli
    stessi tempi che usa `anima`. Vuoto se non c'è nessun report leggibile."""
    for nome in ("report.json", "report-prova.json"):
        try:
            elementi = json.loads((out / nome).read_text(encoding="utf-8")).get("elementi", [])
        except (OSError, ValueError):
            continue
        return {int(e["scena"]): {"durata_s": float(e["durata_s"]), "inizi_frasi_s": list(e.get("inizi_frasi_s") or []),
                                  "clip_vera": e.get("clip_vera"), "caption": e.get("caption") or []}
                for e in elementi if e.get("scena") is not None and e.get("durata_s")}
    return {}


VELO = 0.58             # quanto si scurisce il fotogramma sotto il titolo: deve leggersi in una griglia di miniature
CORPO_TITOLO_PX, CORPO_SOTTOTITOLO_PX = 104, 76


def font_pesato(cfg: Config, corpo: int, peso: int = 800) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Il font del canale a un corpo e un peso dati (Pillow): lo usano il titolo di copertina e le caption."""
    try:
        font = ImageFont.truetype(str(cfg.font_file()[0]), corpo)
    except OSError:
        return ImageFont.load_default()
    try:
        # Inter Variable ha più assi (opsz, wght): si tocca solo il peso, gli altri restano al loro default
        assi = font.get_variation_axes()
        nome = lambda a: (a["name"].decode() if isinstance(a["name"], bytes) else str(a["name"])).lower()  # noqa: E731
        font.set_variation_by_axes([min(peso, a["maximum"]) if nome(a) in ("weight", "wght") else a["default"] for a in assi])
    except (OSError, AttributeError, ValueError):
        pass
    return font


def a_capo(d: ImageDraw.ImageDraw, testo: str, font, larghezza: int) -> list[str]:
    """A capo greedy misurato con Pillow (come `componenti.avvolgi` fa con Pango)."""
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
    blocchi = [(testo_piano(titolo).upper(), font_pesato(cfg, CORPO_TITOLO_PX), p.testo)]
    if sottotitolo:
        blocchi.append((testo_piano(sottotitolo).upper(), font_pesato(cfg, CORPO_SOTTOTITOLO_PX), p.accento))
    righe = [(r, font, colore) for testo, font, colore in blocchi for r in a_capo(d, testo, font, larghezza)]
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
