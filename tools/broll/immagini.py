"""Scene fatte di immagini ferme, montate sui beat.

Il terzo registro: quando per una scena non esiste né una clip filmata né una animata, si compongono
immagini — trovate fuori o generate — una per frase, così quello che si vede richiama quello che il
presentatore sta dicendo **in quel momento**.

I tempi non si inventano: `inizi_frasi_s` arriva da `report.json` ed è esatto con la voce di prova e con
le prese di `reel registra` (`origine_tempi: presa`). Ogni immagine tiene il campo da un inizio frase al
successivo, l'ultima fino alla fine della scena.

Un fermo immagine per otto secondi è il «fermo morto» che `docs/animazioni.md` vieta: ogni immagine si
muove, e la mossa cambia a ogni immagine (`MOSSE`: spinta dentro, carrellata, allargamento, diagonale),
così il movimento non sembra un metronomo. Dal 2026-09-23 metà delle clip del reel sono immagini Meshy, e
devono reggere il confronto con un filmato: per questo lo zoom (`zoompan` su un'immagine raddoppiata, che
toglie lo scatto dei pixel interi) e non più la sola carrellata.

Fra un'immagine e l'altra c'è una **transizione** (`xfade`) presa in giro da `config.toml [transizioni]
immagini` (zoomin, circleopen…: le «wow» chieste dal presentatore), lunga `immagini_s`; senza la chiave
resta la dissolvenza del reel. Comincia **sull'inizio frase**, così il cambio resta ancorato a quello che il
presentatore sta dicendo.

Con `xfade` le durate si sovrappongono — l'uscita dura `offset + durata del secondo ingresso` — quindi le
lunghezze degli ingressi si ricalcolano (`montaggio`) perché il totale resti esattamente `durata_s`.
"""
from __future__ import annotations

from pathlib import Path

from tools.anim.config import Config, carica
from tools.reel.ffmpeg import esegui, trova_ffmpeg


SOVRAMISURA = 1.18      # lo zoom delle carrellate: è lo spazio in cui l'inquadratura scorre
ZOOM = 0.22             # quanto entra (o esce) la spinta: 1 → 1,22
MOSSE = ("spinta", "carrellata", "allarga", "diagonale")
TRANSIZIONI = ("fade",) # ripiego se config.toml non ha [transizioni] immagini
DURATA_MIN_S = 0.6      # sotto, il cambio è uno sfarfallio invece che uno stacco
TENUTA_DIVISA_MIN_S = 1.5   # una tenuta si divide per far vedere un'immagine in più solo se ognuna resta almeno così
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


def dividi_per_immagini(tenute: list[tuple[float, float]], n_immagini: int) -> list[tuple[float, float]]:
    """Più immagini che frasi: si divide a metà la tenuta più lunga finché ogni immagine ha la sua, purché le metà
    restino di almeno `TENUTA_DIVISA_MIN_S`. Le immagini generate si pagano: una generata e mai vista è sprecata
    (2026-09-23, ia-e-lavoro: 2 frasi e 3 gesti). Il cambio in più cade a metà frase, non su un inizio."""
    out = list(tenute)
    while len(out) < n_immagini:
        k = max(range(len(out)), key=lambda i: out[i][1])
        inizio, d = out[k]
        if d / 2 < TENUTA_DIVISA_MIN_S:
            break
        out[k:k + 1] = [(inizio, round(d / 2, 3)), (round(inizio + d / 2, 3), round(d - d / 2, 3))]
    return out


def dissolvenza_s(tenute: list[tuple[float, float]], cfg: Config | None = None) -> float:
    """Quanto dura la dissolvenza fra un'immagine e l'altra.

    Quella di `config.toml [transizioni] durata_s`, accorciata se la tenuta più breve non le lascia
    spazio: sotto `TENUTA_MIN_S` di immagine ferma e sola non si vedrebbe più l'immagine, solo il
    passaggio. Con una sola immagine non c'è niente da dissolvere.
    """
    if len(tenute) < 2:
        return 0.0
    cfg = cfg or carica()
    tr = cfg.dati.get("transizioni") or {}
    voluta = float(tr.get("immagini_s", tr.get("durata_s", DISSOLVENZA_S)))
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


def mossa(indice: int) -> str:
    return MOSSE[indice % len(MOSSE)]


def _zoompan(nome: str, n: int) -> tuple[str, str, str]:
    """(z, x, y) di `zoompan` per la mossa; `on` è il fotogramma, `n` quanti ne dura l'immagine."""
    p = f"(on/{max(n - 1, 1)})"
    centro_x, centro_y = "(iw-iw/zoom)/2", "(ih-ih/zoom)/2"
    if nome == "spinta":
        return f"1+{ZOOM}*{p}", centro_x, centro_y
    if nome == "allarga":
        return f"{1 + ZOOM}-{ZOOM}*{p}", centro_x, centro_y
    if nome == "carrellata":
        return f"{SOVRAMISURA}", f"(iw-iw/zoom)*{p}", centro_y
    return f"{SOVRAMISURA}+0.06*{p}", f"(iw-iw/zoom)*{p}", f"(ih-ih/zoom)*{p}"   # diagonale


def _ramo(indice: int, entrata: int, larghezza: int, altezza: int, durata: float, fps: int) -> str:
    """L'immagine raddoppiata, poi la mossa con `zoompan` al fotogramma: un fotogramma in ingresso, uno in uscita."""
    n = max(1, round(durata * fps))
    z, x, y = _zoompan(mossa(indice), n)
    return (f"[{entrata}:v]scale={2 * larghezza}:{2 * altezza}:force_original_aspect_ratio=increase,"
            f"crop={2 * larghezza}:{2 * altezza},"
            f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s={larghezza}x{altezza}:fps={fps},"
            f"setpts=PTS-STARTPTS,setsar=1,format=yuv420p[v{indice}]")


def transizioni(cfg: Config) -> tuple[str, ...]:
    """I nomi `xfade` delle transizioni fra un'immagine e l'altra, in giro."""
    nomi = (cfg.dati.get("transizioni") or {}).get("immagini")
    return tuple(nomi) if nomi else TRANSIZIONI


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
        ingressi += ["-loop", "1", "-framerate", str(fps), "-t", f"{lunghezza:.3f}", "-i", str(img)]
        filtri.append(_ramo(i, i, W, H, lunghezza, fps))
    if t > 0 and len(lunghezze) > 1:
        dentro, nomi = "v0", transizioni(cfg)
        for i in range(1, len(lunghezze)):
            fuori = "out" if i == len(lunghezze) - 1 else f"x{i}"
            filtri.append(f"[{dentro}][v{i}]xfade=transition={nomi[(i - 1) % len(nomi)]}:duration={t:.3f}:"
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
    tenute = dividi_per_immagini(finestre(inizi_frasi_s, durata_s), len(immagini))
    dest.parent.mkdir(parents=True, exist_ok=True)
    esegui(comando(immagini, tenute, dest, cfg), f"ffmpeg (immagini scena {dest.stem})")
    return dest, tenute
