"""`broll prova-inquadratura`: quale pezzo di un filmato 16:9 sopravvive al ritaglio 9:16.

In una scena di filmato non c'è grafica Manim: si vede il filmato a tutto schermo e il riquadro del
presentatore sopra, niente altro. Restano quindi due sole domande, ed entrambe si rispondono guardando:
il soggetto sta ancora dentro dopo il ritaglio, e il riquadro del presentatore non glielo copre.

Un 16:9 portato a 1920 di altezza diventa largo 3413: del filmato originale ne resta meno di un terzo.
Questo comando mostra lo stesso fotogramma ritagliato in più punti, con il riquadro al suo posto, così
l'ancoraggio si sceglie a occhio prima che lo decida un'euristica.
"""
from __future__ import annotations

from pathlib import Path

from tools.anim.config import Config, carica
from tools.reel.compositing import maschera_riquadro, posizione_riquadro
from tools.reel.contact_sheet import genera as contact
from tools.reel.ffmpeg import esegui, ffprobe, trova_ffmpeg
from tools.reel.model import Diagnostica, avviso

RADICE = Path(__file__).resolve().parents[2]

# dove ancorare il ritaglio sull'asse lungo: 0 = tutto a sinistra, 1 = tutto a destra
ANCORE = {"sinistra": 0.0, "centro": 0.5, "destra": 1.0}
IMMAGINI = (".png", ".jpg", ".jpeg", ".webp")


def render_dir(slug: str) -> Path:
    return RADICE / "contenuti" / "render" / slug


def avatar(cfg: Config) -> Path | None:
    p = RADICE / "assets" / "presentatore" / "avatar.png"
    return p if p.exists() else None


def _bande_ui(cfg: Config) -> str:
    """Scurisce le fasce che l'interfaccia della piattaforma copre, così il ritaglio si sceglie sul
    pezzo di fotogramma che si vedrà davvero.

    I quattro numeri vengono da `config.toml [safe_area]`, che oggi è tarata **su Instagram** (lo dice il
    commento del config). Su TikTok le zone coperte sono altre: finché quei valori non diventano
    per-piattaforma, qui si vede l'ingombro di Instagram e basta.
    """
    s, W, H = cfg.dati["safe_area"], cfg.larghezza, cfg.altezza
    alto, basso = int(s["alto"]), int(s["basso"])
    sx, dx = int(s.get("sinistra", 60)), int(s["destra"])
    scuro = "black@0.5"
    return "".join(
        f"drawbox=x={x}:y={y}:w={w}:h={h}:color={scuro}:t=fill," for x, y, w, h in (
            (0, 0, W, alto),                      # fascia alta
            (0, H - basso, W, basso),             # didascalia e pulsanti in basso
            (0, alto, sx, H - alto - basso),      # margine sinistro
            (W - dx, alto, dx, H - alto - basso),  # colonna dei pulsanti a destra
        ))


def _comando(filmato: Path, ancora: float, dest: Path, t: float, riquadro: str,
             cfg: Config, faccia: Path | None) -> list[str]:
    ff, _ = trova_ffmpeg()
    W, H = cfg.larghezza, cfg.altezza
    cmd = [ff, "-y", "-loglevel", "error"]
    if filmato.suffix.lower() not in IMMAGINI:
        cmd += ["-ss", f"{t:.3f}"]
    cmd += ["-i", str(filmato)]

    # lo stesso ritaglio che farà il compositing, ma con l'ancoraggio scelto invece che centrato
    filtri = [f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,"
              f"crop={W}:{H}:(in_w-out_w)*{ancora:.3f}:(in_h-out_h)/2,setsar=1,"
              f"setpts=PTS-STARTPTS,{_bande_ui(cfg)}format=rgba[v0]"]
    ultimo = "v0"
    if faccia and riquadro != "no":
        x, y, d = posizione_riquadro(cfg, riquadro)
        cmd += ["-loop", "1", "-i", str(faccia), "-loop", "1", "-i", str(maschera_riquadro(cfg))]
        filtri += [f"[1:v]scale=w='if(gte(iw/ih,1),-2,{d})':h='if(gte(iw/ih,1),{d},-2)',crop={d}:{d},"
                   "setsar=1,format=rgba[pip]",
                   "[2:v]format=gray[msk]",
                   "[pip][msk]alphamerge[pipA]",
                   f"[v0][pipA]overlay=x={x}:y={y}[v1]"]
        ultimo = "v1"
    filtri.append(f"[{ultimo}]format=rgb24[out]")
    return cmd + ["-filter_complex", ";".join(filtri), "-map", "[out]", "-frames:v", "1", str(dest)]


def prova_inquadratura(slug: str, filmato: Path, t: float = 1.0, riquadro: str = "si",
                       ancore: dict[str, float] | None = None,
                       cfg: Config | None = None) -> tuple[Path, list[Path], list[Diagnostica]]:
    """Ritaglia lo stesso fotogramma su più ancoraggi; ritorna (contact sheet, png, avvisi)."""
    cfg = cfg or carica()
    ancore = ancore or ANCORE
    diag: list[Diagnostica] = []

    info = ffprobe(filmato)
    lar, alt = info.get("larghezza"), info.get("altezza")
    if lar and alt:
        proporzione = lar / alt
        obiettivo = cfg.larghezza / cfg.altezza
        if proporzione > obiettivo:
            resta = round(obiettivo / proporzione * 100)
            diag.append(avviso(f"filmato {lar}×{alt}: del suo campo ne resta il {resta} % dopo il ritaglio 9:16"))
        if alt < cfg.altezza:
            diag.append(avviso(f"filmato alto {alt} px, meno dei {cfg.altezza} della tela: verrà ingrandito"))
    elif info.get("errore"):
        diag.append(avviso(f"non riesco a leggere {filmato.name}: {info['errore']}"))

    faccia = avatar(cfg)
    if not faccia:
        diag.append(avviso("manca assets/presentatore/avatar.png (`uv run reel setup`): "
                           "il riquadro non è disegnato e non si vede cosa copre"))

    from tools.reel.percorsi import lavoro
    dest_dir = lavoro(slug) / "broll"   # transitorio, fuori dal progetto
    dest_dir.mkdir(parents=True, exist_ok=True)
    png: list[Path] = []
    for nome, a in ancore.items():
        d = dest_dir / f"inquadratura-{nome}.png"
        esegui(_comando(filmato, a, d, t, riquadro, cfg, faccia), f"ffmpeg (inquadratura {nome})")
        png.append(d)

    diag.append(avviso("le fasce scure sono coperte dall'interfaccia: i valori di [safe_area] sono "
                       "tarati su Instagram, su TikTok le zone sono altre"))
    elementi = [{"file": str(p), "etichetta": f"{nome}  ({a:.0%})"} for p, (nome, a) in zip(png, ancore.items())]
    foglio = contact(elementi, diag, dest_dir / f"inquadratura-{filmato.stem}.png",
                     colonne=len(png), larghezza_cella=300)
    return foglio, png, diag
