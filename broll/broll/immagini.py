"""Scene fatte di immagini ferme, montate sui beat.

Il terzo registro: quando per una scena non esiste né una clip filmata né una animata, si compongono
immagini — trovate fuori o generate — una per frase, così quello che si vede richiama quello che il
presentatore sta dicendo **in quel momento**.

I tempi non si inventano: `inizi_frasi_s` arriva da `report.json` ed è esatto con la voce di prova e con
le prese di `reel registra` (`origine_tempi: presa`). Ogni immagine tiene il campo da un inizio frase al
successivo, l'ultima fino alla fine della scena.

Un fermo immagine per otto secondi è il «fermo morto» che `docs/animazioni.md` vieta: ogni immagine si
muove piano, con una carrellata che cambia verso a ogni cambio, in modo che il movimento non sembri un
metronomo.
"""
from __future__ import annotations

from pathlib import Path

from tools.anim.config import Config, carica
from tools.reel.ffmpeg import esegui, trova_ffmpeg

RADICE = Path(__file__).resolve().parents[2]

SOVRAMISURA = 1.18      # quanto l'immagine è più grande del fotogramma: è lo spazio per la carrellata
DURATA_MIN_S = 0.6      # sotto, il cambio è uno sfarfallio invece che uno stacco


class ImmaginiMancanti(RuntimeError):
    pass


def finestre(inizi_frasi_s: list[float], durata_s: float) -> list[tuple[float, float]]:
    """Da inizi a intervalli (inizio, durata). Gli inizi troppo ravvicinati si fondono col precedente."""
    if not inizi_frasi_s:
        return [(0.0, durata_s)]
    inizi = [t for t in sorted(inizi_frasi_s) if t < durata_s]
    if not inizi or inizi[0] > 0:
        inizi = [0.0] + inizi
    tenute: list[tuple[float, float]] = []
    for i, t in enumerate(inizi):
        fine = inizi[i + 1] if i + 1 < len(inizi) else durata_s
        if tenute and fine - t < DURATA_MIN_S:
            inizio, _ = tenute[-1]
            tenute[-1] = (inizio, fine - inizio)      # troppo corta: la si dà alla precedente
        else:
            tenute.append((t, fine - t))
    return tenute


def _ramo(indice: int, entrata: int, larghezza: int, altezza: int, durata: float, fps: int) -> str:
    """Una carrellata lenta sull'immagine: verso alternato, così i cambi non sembrano un metronomo."""
    w, h = int(larghezza * SOVRAMISURA), int(altezza * SOVRAMISURA)
    avanti = indice % 2 == 0
    frazione = f"min(t/{max(durata, 0.1):.3f},1)"
    x = f"(in_w-out_w)*({frazione})" if avanti else f"(in_w-out_w)*(1-({frazione}))"
    return (f"[{entrata}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
            f"crop={larghezza}:{altezza}:x='{x}':y='(in_h-out_h)/2',"
            f"fps={fps},setsar=1,format=yuv420p[v{indice}]")


def comando(immagini: list[Path], tenute: list[tuple[float, float]], dest: Path, cfg: Config) -> list[str]:
    ff, _ = trova_ffmpeg()
    W, H, fps = cfg.larghezza, cfg.altezza, cfg.fps
    ingressi: list[str] = []
    filtri: list[str] = []
    for i, (_, durata) in enumerate(tenute):
        img = immagini[i % len(immagini)]          # meno immagini che beat: si riusano in giro
        ingressi += ["-loop", "1", "-t", f"{durata:.3f}", "-i", str(img)]
        filtri.append(_ramo(i, i, W, H, durata, fps))
    filtri.append("".join(f"[v{i}]" for i in range(len(tenute))) +
                  f"concat=n={len(tenute)}:v=1:a=0[out]")
    totale = sum(d for _, d in tenute)
    return [ff, "-y", "-loglevel", "error", *ingressi, "-filter_complex", ";".join(filtri),
            "-map", "[out]", "-t", f"{totale:.3f}", "-r", str(fps),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(dest)]


def componi(immagini: list[Path], inizi_frasi_s: list[float], durata_s: float, dest: Path,
            cfg: Config | None = None) -> tuple[Path, list[tuple[float, float]]]:
    """Monta le immagini sui beat e scrive un mp4 muto lungo esattamente `durata_s`."""
    cfg = cfg or carica()
    if not immagini:
        raise ImmaginiMancanti("nessuna immagine da comporre")
    mancanti = [p for p in immagini if not p.exists()]
    if mancanti:
        raise ImmaginiMancanti(f"immagini assenti: {', '.join(p.name for p in mancanti)}")
    tenute = finestre(inizi_frasi_s, durata_s)
    dest.parent.mkdir(parents=True, exist_ok=True)
    esegui(comando(immagini, tenute, dest, cfg), f"ffmpeg (immagini scena {dest.stem})")
    return dest, tenute
