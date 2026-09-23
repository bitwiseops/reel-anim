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

Fra un'immagine e l'altra c'è una **dissolvenza** (`xfade`), lunga quanto `config.toml [transizioni]
durata_s`: fra due immagini generate lo stacco secco somiglia a un errore di montaggio, mentre il reel ha
già la dissolvenza fra le scene e questa è la stessa grammatica. La dissolvenza comincia **sull'inizio
frase**, come faceva lo stacco, così il cambio resta ancorato a quello che il presentatore sta dicendo.

Con `xfade` le durate si sovrappongono — l'uscita dura `offset + durata del secondo ingresso` — quindi le
lunghezze degli ingressi si ricalcolano (`montaggio`) perché il totale resti esattamente `durata_s`.
"""
from __future__ import annotations

from pathlib import Path

from tools.anim.config import Config, carica
from tools.reel.ffmpeg import esegui, trova_ffmpeg

RADICE = Path(__file__).resolve().parents[2]

SOVRAMISURA = 1.18      # quanto l'immagine è più grande del fotogramma: è lo spazio per la carrellata
DURATA_MIN_S = 0.6      # sotto, il cambio è uno sfarfallio invece che uno stacco
DISSOLVENZA_S = 0.25    # ripiego se config.toml non ha [transizioni] durata_s
TENUTA_MIN_S = 0.3      # quanto ogni immagine resta ferma e sola: sotto, si vedono solo dissolvenze
MARGINE_S = 0.04        # un fotogramma d'aria sugli ingressi intermedi: xfade taglia il resto da sé


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


def dissolvenza_s(tenute: list[tuple[float, float]], cfg: Config | None = None) -> float:
    """Quanto dura la dissolvenza fra un'immagine e l'altra.

    Quella di `config.toml [transizioni] durata_s`, accorciata se la tenuta più breve non le lascia
    spazio: sotto `TENUTA_MIN_S` di immagine ferma e sola non si vedrebbe più l'immagine, solo il
    passaggio. Con una sola immagine non c'è niente da dissolvere.
    """
    if len(tenute) < 2:
        return 0.0
    cfg = cfg or carica()
    voluta = float((cfg.dati.get("transizioni") or {}).get("durata_s", DISSOLVENZA_S))
    piu_corta = min(d for _, d in tenute)
    return round(max(0.0, min(voluta, piu_corta - TENUTA_MIN_S)), 3)


def montaggio(tenute: list[tuple[float, float]], dissolvenza: float) -> tuple[list[float], list[float]]:
    """Le lunghezze degli ingressi e gli offset delle dissolvenze, perché il totale resti esatto.

    `xfade` non somma: l'uscita dura `offset + lunghezza del secondo ingresso`, e del primo butta tutto
    quello che sta oltre `offset + dissolvenza`. Quindi la dissolvenza comincia sull'inizio frase
    (`offset` = inizio della tenuta), ogni immagine in mezzo dura la sua tenuta **più** la dissolvenza —
    il tempo in cui sfuma nella successiva — e l'ultima dura la sua tenuta e basta: così l'uscita finale
    vale `inizio dell'ultima tenuta + la sua durata`, cioè la durata della scena.
    """
    ultimo = len(tenute) - 1
    offset = [inizio for inizio, _ in tenute]
    lunghezze = [d if (i == ultimo or dissolvenza <= 0) else d + dissolvenza + MARGINE_S
                 for i, (_, d) in enumerate(tenute)]
    return lunghezze, offset


def _ramo(indice: int, entrata: int, larghezza: int, altezza: int, durata: float, fps: int) -> str:
    """Una carrellata lenta sull'immagine: verso alternato, così i cambi non sembrano un metronomo."""
    w, h = int(larghezza * SOVRAMISURA), int(altezza * SOVRAMISURA)
    avanti = indice % 2 == 0
    frazione = f"min(t/{max(durata, 0.1):.3f},1)"
    x = f"(in_w-out_w)*({frazione})" if avanti else f"(in_w-out_w)*(1-({frazione}))"
    return (f"[{entrata}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
            f"crop={larghezza}:{altezza}:x='{x}':y='(in_h-out_h)/2',"
            f"fps={fps},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[v{indice}]")


def comando(immagini: list[Path], tenute: list[tuple[float, float]], dest: Path, cfg: Config,
            dissolvenza: float | None = None) -> list[str]:
    ff, _ = trova_ffmpeg()
    W, H, fps = cfg.larghezza, cfg.altezza, cfg.fps
    t = dissolvenza_s(tenute, cfg) if dissolvenza is None else dissolvenza
    lunghezze, offset = montaggio(tenute, t)
    ingressi: list[str] = []
    filtri: list[str] = []
    for i, lunghezza in enumerate(lunghezze):
        img = immagini[i % len(immagini)]          # meno immagini che beat: si riusano in giro
        ingressi += ["-loop", "1", "-t", f"{lunghezza:.3f}", "-i", str(img)]
        filtri.append(_ramo(i, i, W, H, lunghezza, fps))
    if t > 0 and len(lunghezze) > 1:
        dentro = "v0"
        for i in range(1, len(lunghezze)):
            fuori = "out" if i == len(lunghezze) - 1 else f"x{i}"
            filtri.append(f"[{dentro}][v{i}]xfade=transition=fade:duration={t:.3f}:"
                          f"offset={offset[i]:.3f}[{fuori}]")
            dentro = fuori
    else:
        filtri.append("".join(f"[v{i}]" for i in range(len(lunghezze))) +
                      f"concat=n={len(lunghezze)}:v=1:a=0[out]")
    totale = sum(d for _, d in tenute)
    # la lunghezza si chiude in **fotogrammi**, come in `rendi.py`: `-t` taglia sui secondi e a 30 fps
    # una scena di 6,01 s perderebbe (o guadagnerebbe) il fotogramma che il montaggio pretende
    filtri.append(f"[out]trim=end_frame={round(totale * fps)},setpts=PTS-STARTPTS[fin]")
    return [ff, "-y", "-loglevel", "error", *ingressi, "-filter_complex", ";".join(filtri),
            "-map", "[fin]", "-r", str(fps),
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
