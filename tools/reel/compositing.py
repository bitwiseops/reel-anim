"""Compositing ffmpeg di una scena (grafica Manim + b-roll + riquadro del presentatore + audio) e concatenazione."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

from ..anim.config import Config, carica
from .ffmpeg import esegui, trova_ffmpeg

RADICE = Path(__file__).resolve().parents[2]
MASCHERE = RADICE / "assets" / "presentatore"


@dataclass
class Sorgenti:
    grafica: Path                 # Manim: mp4 opaco, o mov con alpha se c'è b-roll sotto
    durata_s: float
    riquadro: str                 # "no" | "si" | posizione
    video_presentatore: Path | None = None   # clip con volto (video+audio) ...
    avatar: Path | None = None               # ... oppure immagine statica (modalità prova)
    audio: Path | None = None                # audio separato (voce sintetica); se None usa quello della clip
    schermo: Path | None = None              # b-roll / screen recording sotto la grafica
    filmato: bool = False                    # scena [broll]: `grafica` è materiale esterno a tutta tela, non Manim
    caption: tuple[tuple[Path, float, float], ...] = ()   # (png, t0, t1) dei blocchi di sottotitolo, bruciati sopra tutto
    caption_xy: tuple[int, int] | None = None             # angolo in alto a sinistra della fascia (tools/reel/caption.fascia)


def posizione_riquadro(cfg: Config, riquadro: str) -> tuple[int, int, int]:
    """(x, y, lato) in px del riquadro del presentatore."""
    r, s = cfg.dati["riquadro"], cfg.dati["safe_area"]
    pos = r["posizione"] if riquadro == "si" else riquadro
    d, m = int(r["dimensione_px"]), int(r["margine_px"])
    x = cfg.larghezza - int(s["destra"]) - m - d if "destra" in pos else int(s.get("sinistra", 60)) + m
    y = cfg.altezza - int(s["basso"]) - d if "basso" in pos else int(s["alto"])
    return x, y, d


def maschera_riquadro(cfg: Config) -> Path:
    """PNG in scala di grigi (bianco = opaco) della forma del riquadro, generato con supersampling 4x."""
    r = cfg.dati["riquadro"]
    d, forma, raggio = int(r["dimensione_px"]), r["forma"], int(r.get("raggio_px", 48))
    dest = MASCHERE / f"_maschera-{forma}-{d}-{raggio}.png"
    if not dest.exists():
        k = 4
        im = Image.new("L", (d * k, d * k), 0)
        dr = ImageDraw.Draw(im)
        if forma == "cerchio":
            dr.ellipse((0, 0, d * k - 1, d * k - 1), fill=255)
        else:
            dr.rounded_rectangle((0, 0, d * k - 1, d * k - 1), radius=raggio * k, fill=255)
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.resize((d, d), Image.LANCZOS).save(dest)
    return dest


def maschera_schermo(cfg: Config) -> Path:
    sc = cfg.dati["schermo"]
    w, h, raggio = int(sc["larghezza"]), int(sc["altezza"]), int(sc.get("raggio_px", 36))
    dest = MASCHERE / f"_maschera-schermo-{w}x{h}-{raggio}.png"
    if not dest.exists():
        k = 4
        im = Image.new("L", (w * k, h * k), 0)
        ImageDraw.Draw(im).rounded_rectangle((0, 0, w * k - 1, h * k - 1), radius=raggio * k, fill=255)
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.resize((w, h), Image.LANCZOS).save(dest)
    return dest


def comando_scena(src: Sorgenti, dest: Path, cfg: Config | None = None, anteprima: bool = False) -> list[str]:
    """Costruisce il comando ffmpeg (senza eseguirlo) per una scena."""
    cfg = cfg or carica()
    ff, _ = trova_ffmpeg()
    W, H, fps = cfg.larghezza, cfg.altezza, cfg.fps
    inputs: list[str] = []
    filtri: list[str] = []
    n = 0

    def aggiungi(*args: str) -> int:
        nonlocal n
        inputs.extend(args)
        i = n
        n += 1
        return i

    # base: sfondo pieno + b-roll nella cornice, oppure direttamente la grafica opaca
    if src.schermo:
        i_base = aggiungi("-f", "lavfi", "-i", f"color=c={cfg.palette.sfondo}:s={W}x{H}:r={fps}:d={src.durata_s:.3f}")
        i_br = aggiungi("-stream_loop", "-1", "-i", str(src.schermo)) if src.schermo.suffix.lower() in (".mp4", ".mov", ".webm", ".m4v") \
            else aggiungi("-loop", "1", "-i", str(src.schermo))
        i_msk_s = aggiungi("-loop", "1", "-i", str(maschera_schermo(cfg)))
        sc = cfg.dati["schermo"]
        sw, sh = int(sc["larghezza"]), int(sc["altezza"])
        filtri.append(f"[{i_br}:v]scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh},setsar=1,format=rgba[br]")
        filtri.append(f"[{i_msk_s}:v]format=gray[mskS]")
        filtri.append("[br][mskS]alphamerge[brA]")
        filtri.append(f"[{i_base}:v][brA]overlay=x={int(sc['x'])}:y={int(sc['y'])}:shortest=1[base]")
        i_gr = aggiungi("-i", str(src.grafica))
        filtri.append(f"[{i_gr}:v]scale={W}:{H}:flags=lanczos,format=rgba[gr]")
        filtri.append("[base][gr]overlay=0:0:format=auto[v0]")
    elif src.filmato:
        # `broll rendi` consegna già 1080×1920 a fps giusti; un file messo a mano no, e stirarlo lo deformerebbe:
        # si riempie la tela e si ritaglia al centro. Niente ripetizione: se è corto lo dice `monta`.
        i_gr = aggiungi("-i", str(src.grafica)) if src.grafica.suffix.lower() in (".mp4", ".mov", ".webm", ".m4v") \
            else aggiungi("-loop", "1", "-i", str(src.grafica))
        filtri.append(f"[{i_gr}:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
                      f"fps={fps},setsar=1[v0]")
    else:
        i_gr = aggiungi("-i", str(src.grafica))
        filtri.append(f"[{i_gr}:v]scale={W}:{H}:flags=lanczos,setsar=1[v0]")

    # riquadro del presentatore
    ultimo = "v0"
    i_pres = None
    if src.riquadro != "no" and (src.video_presentatore or src.avatar):
        x, y, d = posizione_riquadro(cfg, src.riquadro)
        i_pres = aggiungi("-i", str(src.video_presentatore)) if src.video_presentatore else aggiungi("-loop", "1", "-i", str(src.avatar))
        i_msk = aggiungi("-loop", "1", "-i", str(maschera_riquadro(cfg)))
        filtri.append(f"[{i_pres}:v]scale=w='if(gte(iw/ih,1),-2,{d})':h='if(gte(iw/ih,1),{d},-2)',crop={d}:{d},setsar=1,format=rgba[pip]")
        filtri.append(f"[{i_msk}:v]format=gray[msk]")
        filtri.append("[pip][msk]alphamerge[pipA]")
        filtri.append(f"[v0][pipA]overlay=x={x}:y={y}:shortest=0[v1]")
        ultimo = "v1"
    elif src.video_presentatore:
        i_pres = aggiungi("-i", str(src.video_presentatore))  # solo per l'audio

    # caption: sopra tutto il resto, una per blocco, accesa nella sua finestra. Sono PNG perché questo ffmpeg non ha
    # drawtext (vedi tools/reel/caption.py); si bruciano qui e non in Manim perché i tempi buoni sono quelli della presa.
    if src.caption:
        cx, cy = src.caption_xy or (0, 0)
        for k, (png, t0, t1) in enumerate(src.caption):
            i_cap = aggiungi("-loop", "1", "-i", str(png))
            filtri.append(f"[{i_cap}:v]format=rgba,setpts=PTS-STARTPTS[cap{k}]")
            prossimo = f"c{k}"
            filtri.append(f"[{ultimo}][cap{k}]overlay=x={cx}:y={cy}:shortest=0:"
                          f"enable='between(t,{t0:.3f},{t1:.3f})'[{prossimo}]")
            ultimo = prossimo
    filtri.append(f"[{ultimo}]format=yuv420p[v]")

    # audio
    if src.audio:
        i_a = aggiungi("-i", str(src.audio))
        filtri.append(f"[{i_a}:a]aresample=48000,apad[a]")
    elif src.video_presentatore and i_pres is not None:
        filtri.append(f"[{i_pres}:a]aresample=48000,loudnorm=I=-16:TP=-1.5:LRA=11,apad[a]")
    else:
        i_a = aggiungi("-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo")
        filtri.append(f"[{i_a}:a]anull[a]")

    cmd = [ff, "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filtri), "-map", "[v]", "-map", "[a]",
           "-t", f"{src.durata_s:.3f}", "-r", str(fps)]
    if anteprima:
        cmd += ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "28"]
    else:
        cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "18", "-profile:v", "high"]
    # audio sempre stereo: la voce sintetica e molte clip sono mono, e alcuni lettori non riproducono l'audio mono
    cmd += ["-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
            str(dest)]
    return cmd


def componi_scena(src: Sorgenti, dest: Path, cfg: Config | None = None, anteprima: bool = False) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    esegui(comando_scena(src, dest, cfg, anteprima), f"ffmpeg (scena {dest.stem})")
    return dest


def comando_concat(scene: list[tuple[Path, float]], dest: Path, transizione: str = "dissolvenza", durata_trans_s: float = 0.25,
                   cfg: Config | None = None, anteprima: bool = False, tagli: frozenset[int] = frozenset()) -> list[str]:
    """Concatena le scene: dissolvenza incrociata (xfade + acrossfade) oppure taglio netto.

    `tagli` sono le giunzioni che restano un taglio anche quando il reel va in dissolvenza: `k` è la giunzione
    fra la scena `k-1` e la `k` (indici di `scene`). Servono agli stacchi fra animazione e filmato: grafica
    scura e filmato chiaro, sciolti uno nell'altro, lasciano per qualche fotogramma il fantasma dei testi
    sopra l'immagine. Senza `tagli` il comando è quello di sempre.
    """
    cfg = cfg or carica()
    ff, _ = trova_ffmpeg()
    inputs: list[str] = []
    for p, _ in scene:
        inputs += ["-i", str(p)]
    filtri: list[str] = []
    if transizione == "dissolvenza" and len(scene) > 1:
        d = durata_trans_s
        v_prec, a_prec = "0:v", "0:a"
        if tagli:
            # concat e xfade nella stessa catena: concat esce con una base dei tempi sua, e xfade rifiuta due
            # ingressi con basi diverse. Si portano tutti alla stessa prima di cominciare.
            for k in range(len(scene)):
                filtri.append(f"[{k}:v]settb=AVTB,fps={cfg.fps}[n{k}]")
            v_prec = "n0"
        offset = 0.0
        for k in range(1, len(scene)):
            v_k = f"n{k}" if tagli else f"{k}:v"
            if k in tagli:
                offset += scene[k - 1][1]
                filtri.append(f"[{v_prec}][{a_prec}][{v_k}][{k}:a]concat=n=2:v=1:a=1[c{k}][a{k}]")
                filtri.append(f"[c{k}]settb=AVTB,fps={cfg.fps}[v{k}]")
            else:
                offset += scene[k - 1][1] - d
                filtri.append(f"[{v_prec}][{v_k}]xfade=transition=fade:duration={d}:offset={offset:.3f}[v{k}]")
                filtri.append(f"[{a_prec}][{k}:a]acrossfade=d={d}[a{k}]")
            v_prec, a_prec = f"v{k}", f"a{k}"
        mappa = ["-map", f"[{v_prec}]", "-map", f"[{a_prec}]"]
    else:
        seg = "".join(f"[{k}:v][{k}:a]" for k in range(len(scene)))
        filtri.append(f"{seg}concat=n={len(scene)}:v=1:a=1[v][a]")
        mappa = ["-map", "[v]", "-map", "[a]"]
    cmd = [ff, "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filtri), *mappa, "-r", str(cfg.fps)]
    cmd += ["-c:v", "libx264", "-preset", "ultrafast" if anteprima else "medium", "-crf", "28" if anteprima else "18",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart",
            str(dest)]
    return cmd


def durata_concat(scene: list[tuple[Path, float]], transizione: str, durata_trans_s: float,
                  tagli: frozenset[int] = frozenset()) -> float:
    tot = sum(d for _, d in scene)
    if transizione == "dissolvenza" and len(scene) > 1:
        tot -= durata_trans_s * (len(scene) - 1 - len([k for k in tagli if 0 < k < len(scene)]))
    return round(tot, 3)


def concatena(scene: list[tuple[Path, float]], dest: Path, transizione: str = "dissolvenza", durata_trans_s: float = 0.25,
              cfg: Config | None = None, anteprima: bool = False, tagli: frozenset[int] = frozenset()) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    esegui(comando_concat(scene, dest, transizione, durata_trans_s, cfg, anteprima, tagli), "ffmpeg (concat)")
    return dest
