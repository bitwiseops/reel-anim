"""Compositing ffmpeg di una scena (grafica Manim + b-roll + riquadro del presentatore + audio) e concatenazione."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

from ..anim.config import Config, carica
from .clip import ESTENSIONI as ESTENSIONI_VIDEO
from .ffmpeg import esegui, trova_ffmpeg
from .model import PIENO

from ..anim.config import RADICE
MASCHERE = RADICE / "assets" / "presentatore"


@dataclass
class Sorgenti:
    grafica: Path | None          # Manim: mp4 opaco, o mov con alpha se sotto c'è un video (b-roll o volto pieno);
                                  # None solo a volto pieno: la scena è lui e basta (l'apertura)
    durata_s: float
    riquadro: str                 # "no" | "si" | "pieno" (presentatore a tutta tela) | posizione
    video_presentatore: Path | None = None   # clip con volto (video+audio) ...
    avatar: Path | None = None               # ... oppure immagine statica (modalità prova)
    audio: Path | None = None                # audio separato (voce sintetica); se None usa quello della clip
    schermo: Path | None = None              # b-roll / screen recording sotto la grafica
    filmato: bool = False                    # scena [broll]: `grafica` è materiale esterno a tutta tela, non Manim
    caption: tuple[tuple[Path, float, float], ...] = ()   # (png, t0, t1) dei blocchi di sottotitolo, bruciati sopra tutto
    caption_xy: tuple[int, int] | None = None             # angolo in alto a sinistra della fascia (tools/reel/caption.fascia)
    # raccordo fra volto pieno e riquadro: solo a `riquadro == PIENO`. `uscita_a_riquadro` è la posizione
    # del riquadro della scena DOPO ("si" o "alto-destra"…): negli ultimi `durata_raccordo_s` il volto a tutta tela si
    # rimpicciolisce fino a coincidere con quel riquadro, prendendone la forma. `entrata_da_riquadro` è il contrario
    # nei primi secondi, col riquadro della scena PRIMA. None (vicino senza riquadro, o assente) = stacco secco.
    uscita_a_riquadro: str | None = None
    entrata_da_riquadro: str | None = None
    durata_raccordo_s: float = 0.5


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


# --- raccordo fra volto pieno e riquadro -------------------------------------------------------------------------
# Il volto a tutta tela si rimpicciolisce fino a diventare il cerchio del riquadro (e viceversa in chiusura). Il
# raccordo vive DENTRO la scena a volto pieno, così il montaggio resta un concat.
#
# Come: la finestra visibile del presentatore va dal ritaglio 9:16 a tutta tela al quadrato del riquadro, passando
# per rettangoli intermedi. Si ottiene con un solo `scale` a misura variabile (`eval=frame`, che `overlay` con
# `eval=frame` segue: `overlay_w/h` si aggiornano a ogni fotogramma) e con l'alpha disegnata da `geq` PRIMA dello
# scale, cioè a risoluzione della sorgente e a misura fissa (geq non propaga a valle i cambi di misura: applicarlo
# dopo lo scale lascia a schermo il fotogramma di prima).
# La forma è un rettangolo arrotondato il cui raggio cresce fino a metà del lato: a raccordo finito è il cerchio del
# riquadro. Fuori dalla finestra di tempo `geq` è spento (alpha opaca) e lo scale è identico a quello di sempre:
# la scena resta quella di prima, fotogramma per fotogramma.

DURATA_RACCORDO_S = 0.5


def _fasi_raccordo(src: Sorgenti, cfg: Config) -> list[tuple[str, float, float, int, int, int]]:
    """(verso, t0, span, x, y, lato) dei raccordi di questa scena; `span` è il tempo in cui il volto si muove."""
    if src.riquadro != PIENO or not (src.video_presentatore or src.avatar):
        return []
    versi = [("entrata", src.entrata_da_riquadro), ("uscita", src.uscita_a_riquadro)]
    quanti = sum(1 for _, r in versi if r)
    passo = 1.0 / cfg.fps
    if not quanti or src.durata_raccordo_s < 2 * passo:
        return []
    dur = max(passo * 2, min(src.durata_raccordo_s, src.durata_s / quanti))
    span = max(passo, dur - passo)     # l'ultimo fotogramma della scena è già il riquadro esatto
    fasi = []
    for verso, riq in versi:
        if not riq:
            continue
        x, y, d = posizione_riquadro(cfg, riq)
        fasi.append((verso, 0.0 if verso == "entrata" else src.durata_s - dur, span, x, y, d))
    return fasi


def _geometria_raccordo(fasi: list, cfg: Config, v: str) -> tuple[str, str, str, str]:
    """(larghezza, altezza, x, y) della finestra del volto, come espressioni ffmpeg nella variabile tempo `v`
    ("t" nei filtri, "T" in geq). A raccordo fermo valgono la tela intera in (0, 0)."""
    W, H = cfg.larghezza, cfg.altezza

    def una(fase) -> tuple[str, str, str, str]:
        verso, t0, span, x, y, d = fase
        p = (f"clip(({v}-{t0:.4f})/{span:.4f},0,1)" if verso == "uscita"
             else f"clip(({t0 + span:.4f}-{v})/{span:.4f},0,1)")
        e = f"(({p})*({p})*(3-2*({p})))"        # smoothstep: parte e arriva morbido
        return (f"({W}-{W - d}*{e})", f"({H}-{H - d}*{e})", f"({x}*{e})", f"({y}*{e})")

    if len(fasi) == 1:
        return una(fasi[0])
    dentro, fuori = una(fasi[0]), una(fasi[1])
    mezzo = (fasi[0][1] + fasi[0][2] + fasi[1][1]) / 2
    return tuple(f"if(lt({v},{mezzo:.4f}),{a},{b})" for a, b in zip(dentro, fuori, strict=True))


def _alpha_raccordo(fasi: list, cfg: Config) -> str:
    """L'espressione dell'alpha per `geq`: il rettangolo arrotondato, disegnato nelle coordinate della sorgente.

    W, H in geq sono le misure della sorgente; `f` è il fattore con cui lo scale la porterà a coprire la finestra,
    quindi la finestra vista dalla sorgente è (larghezza/f x altezza/f), centrata, con raggio raggio/f.

    Le variabili di `st()` sono dieci (0-9) e oltre la nona ffmpeg le sovrascrive in silenzio: qui ci stanno tutte.
    """
    ow, oh, _, _ = _geometria_raccordo(fasi, cfg, "T")
    d = int(cfg.dati["riquadro"]["dimensione_px"])
    e = f"((1-ld(0)/{cfg.larghezza})/(1-{d}/{cfg.larghezza}))"    # l'avanzamento, ricavato dalla larghezza
    corpo = ";".join([
        f"st(0,{ow})", f"st(1,{oh})",
        "st(2,max(ld(0)/W,ld(1)/H))",                       # f: quanto lo scale ingrandisce la sorgente
        "st(3,ld(0)/ld(2))", "st(4,ld(1)/ld(2))",           # finestra vista dalla sorgente
        "st(5,(W-ld(3))/2)", "st(6,(H-ld(4))/2)",           # angolo alto-sinistra della finestra
        f"st(7,{e}*min(ld(0),ld(1))/2/ld(2))",              # raggio degli angoli, nella sorgente
        "st(8,max(max(ld(5)+ld(7)-X,X-(ld(5)+ld(3)-1-ld(7))),0))",
        "st(9,max(max(ld(6)+ld(7)-Y,Y-(ld(6)+ld(4)-1-ld(7))),0))",
    ])
    bordo_x = "clip(min(X-ld(5)+1,ld(5)+ld(3)-X),0,1)"      # bordi della finestra, con un pixel di sfumatura
    bordo_y = "clip(min(Y-ld(6)+1,ld(6)+ld(4)-Y),0,1)"
    angolo = "if(lte(ld(7),0),1,clip(ld(7)+0.5-hypot(ld(8),ld(9)),0,1))"
    return f"{corpo};255*clip(min(min({bordo_x},{bordo_y}),{angolo}),0,1)"


def _filtri_raccordo(fasi: list, cfg: Config, ingresso: int, sfondo: int, uscita: str) -> list[str]:
    """I due filtri del volto che si rimpicciolisce: la sorgente mascherata e scalata, e l'overlay sullo sfondo."""
    ow, oh, ox, oy = _geometria_raccordo(fasi, cfg, "t")
    finestre = "+".join(f"between(t,{t0 - 0.05:.4f},{t0 + span + 0.05:.4f})" for _, t0, span, _, _, _ in fasi)
    return [
        f"[{ingresso}:v]fps={cfg.fps},setsar=1,format=rgba,"
        f"geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='{_alpha_raccordo(fasi, cfg)}':enable='{finestre}',"
        f"scale=w='{ow}':h='{oh}':force_original_aspect_ratio=increase:eval=frame:flags=lanczos[raccordo]",
        f"[{sfondo}:v][raccordo]overlay=x='({ox})-(overlay_w-({ow}))/2':y='({oy})-(overlay_h-({oh}))/2':"
        f"eval=frame:format=auto[{uscita}]",
    ]


def _codifica(anteprima: bool, profilo_alto: bool = False) -> list[str]:
    """H.264 + AAC stereo 48 kHz (alcuni lettori non riproducono l'audio mono), veloce in anteprima."""
    video = (["-preset", "ultrafast", "-crf", "28"] if anteprima
             else ["-preset", "medium", "-crf", "18"] + (["-profile:v", "high"] if profilo_alto else []))
    return ["-c:v", "libx264", *video, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
            "-movflags", "+faststart"]


def comando_scena(src: Sorgenti, dest: Path, cfg: Config | None = None, anteprima: bool = False) -> list[str]:
    """Costruisce il comando ffmpeg (senza eseguirlo) per una scena."""
    cfg = cfg or carica()
    ff, _ = trova_ffmpeg()
    W, H, fps = cfg.larghezza, cfg.altezza, cfg.fps
    # ogni immagine letta in loop (avatar, maschere, caption, uno SCHERMO fisso) porta la durata della scena: senza
    # `-t` è un ingresso infinito, e ffmpeg 8.1 a volte resta appeso a CPU piena invece di chiudere con gli altri
    d_img = f"{src.durata_s:.3f}"
    inputs: list[str] = []
    filtri: list[str] = []
    n = 0

    def aggiungi(*args: str) -> int:
        nonlocal n
        inputs.extend(args)
        i = n
        n += 1
        return i

    # base: il presentatore a tutta tela (apertura e chiusura), con l'eventuale grafica trasparente sopra di lui
    i_pres_base = None
    if src.riquadro == PIENO and (src.video_presentatore or src.avatar):
        i_pres_base = aggiungi("-i", str(src.video_presentatore)) if src.video_presentatore \
            else aggiungi("-loop", "1", "-t", d_img, "-i", str(src.avatar))
        fasi = _fasi_raccordo(src, cfg)
        if fasi:
            i_sfondo = aggiungi("-f", "lavfi", "-i",
                                f"color=c={cfg.palette.sfondo}:s={W}x{H}:r={fps}:d={src.durata_s:.3f}")
            filtri += _filtri_raccordo(fasi, cfg, i_pres_base, i_sfondo, "volto")
        else:
            filtri.append(f"[{i_pres_base}:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,"
                          f"crop={W}:{H},fps={fps},setsar=1[volto]")
        if src.grafica is None:
            filtri.append("[volto]null[v0]")     # l'apertura: solo lui, le caption arrivano sopra
        else:
            i_gr = aggiungi("-i", str(src.grafica))
            filtri.append(f"[{i_gr}:v]scale={W}:{H}:flags=lanczos,format=rgba[gr]")
            filtri.append("[volto][gr]overlay=0:0:format=auto[v0]")
    # base: sfondo pieno + b-roll nella cornice, oppure direttamente la grafica opaca
    elif src.schermo:
        i_base = aggiungi("-f", "lavfi", "-i", f"color=c={cfg.palette.sfondo}:s={W}x{H}:r={fps}:d={src.durata_s:.3f}")
        i_br = aggiungi("-stream_loop", "-1", "-i", str(src.schermo)) if src.schermo.suffix.lower() in ESTENSIONI_VIDEO \
            else aggiungi("-loop", "1", "-t", d_img, "-i", str(src.schermo))
        i_msk_s = aggiungi("-loop", "1", "-t", d_img, "-i", str(maschera_schermo(cfg)))
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
        i_gr = aggiungi("-i", str(src.grafica)) if src.grafica.suffix.lower() in ESTENSIONI_VIDEO \
            else aggiungi("-loop", "1", "-t", d_img, "-i", str(src.grafica))
        filtri.append(f"[{i_gr}:v]scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H},"
                      f"fps={fps},setsar=1[v0]")
    else:
        i_gr = aggiungi("-i", str(src.grafica))
        filtri.append(f"[{i_gr}:v]scale={W}:{H}:flags=lanczos,setsar=1[v0]")

    # riquadro del presentatore (non nelle scene a volto pieno: lì è già la base)
    ultimo = "v0"
    i_pres = i_pres_base
    if src.riquadro not in ("no", PIENO) and (src.video_presentatore or src.avatar):
        x, y, d = posizione_riquadro(cfg, src.riquadro)
        i_pres = aggiungi("-i", str(src.video_presentatore)) if src.video_presentatore else aggiungi("-loop", "1", "-t", d_img, "-i", str(src.avatar))
        i_msk = aggiungi("-loop", "1", "-t", d_img, "-i", str(maschera_riquadro(cfg)))
        filtri.append(f"[{i_pres}:v]scale=w='if(gte(iw/ih,1),-2,{d})':h='if(gte(iw/ih,1),{d},-2)',crop={d}:{d},setsar=1,format=rgba[pip]")
        filtri.append(f"[{i_msk}:v]format=gray[msk]")
        filtri.append("[pip][msk]alphamerge[pipA]")
        filtri.append(f"[v0][pipA]overlay=x={x}:y={y}:shortest=0[v1]")
        ultimo = "v1"
    elif src.video_presentatore and i_pres is None:
        i_pres = aggiungi("-i", str(src.video_presentatore))  # solo per l'audio

    # caption: sopra tutto il resto, una per blocco, accesa nella sua finestra. Sono PNG perché questo ffmpeg non ha
    # drawtext (vedi tools/reel/caption.py); si bruciano qui e non in Manim perché i tempi buoni sono quelli della presa.
    if src.caption:
        cx, cy = src.caption_xy or (0, 0)
        for k, (png, t0, t1) in enumerate(src.caption):
            # un fotogramma solo, che l'overlay ripete (`eof_action=repeat`): con una caption in loop per blocco una
            # scena lunga arrivava a 13 ingressi infiniti, e ffmpeg 8.1 restava in stallo a CPU zero
            i_cap = aggiungi("-i", str(png))
            filtri.append(f"[{i_cap}:v]format=rgba[cap{k}]")
            prossimo = f"c{k}"
            filtri.append(f"[{ultimo}][cap{k}]overlay=x={cx}:y={cy}:shortest=0:eof_action=repeat:"
                          f"enable='between(t,{t0:.3f},{t1:.3f})'[{prossimo}]")
            ultimo = prossimo
    filtri.append(f"[{ultimo}]format=yuv420p[v]")

    # audio
    if src.audio:
        i_a = aggiungi("-i", str(src.audio))
        filtri.append(f"[{i_a}:a]aresample=48000,apad[a]")
    elif src.video_presentatore and i_pres is not None:
        voce = catena_voce(cfg)      # pulizia per scena; il volume si fa una volta sola sul reel (normalizza_audio)
        filtri.append(f"[{i_pres}:a]aresample=48000,{voce or 'loudnorm=I=-16:TP=-1.5:LRA=11'},apad[a]")
    else:
        i_a = aggiungi("-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo")
        filtri.append(f"[{i_a}:a]anull[a]")

    cmd = [ff, "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filtri), "-map", "[v]", "-map", "[a]",
           "-t", f"{src.durata_s:.3f}", "-r", str(fps)]
    return cmd + _codifica(anteprima, profilo_alto=True) + [str(dest)]


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
    return cmd + _codifica(anteprima) + [str(dest)]


def durata_concat(scene: list[tuple[Path, float]], transizione: str, durata_trans_s: float,
                  tagli: frozenset[int] = frozenset()) -> float:
    tot = sum(d for _, d in scene)
    if transizione == "dissolvenza" and len(scene) > 1:
        tot -= durata_trans_s * (len(scene) - 1 - len([k for k in tagli if 0 < k < len(scene)]))
    return round(tot, 3)


# --- audio della voce ---------------------------------------------------------------------------------------------
# La voce si pulisce scena per scena (passa-alto, riduzione del rumore, de-esser) prima di alzarla: alzare una presa
# bassa alza anche il rumore della stanza. Il volume si porta al bersaglio una volta sola, sul reel intero, con loudnorm
# in due passaggi. La presa .wav non si tocca mai; `[audio] catena = false` torna al loudnorm per scena.

def _audio(cfg: Config | None) -> dict:
    return dict((cfg or carica()).dati.get("audio") or {})


def catena_voce(cfg: Config | None = None) -> str:
    """I filtri ffmpeg della voce registrata, prima del volume; "" se la catena è spenta."""
    a = _audio(cfg)
    if not a.get("catena", True):
        return ""
    f = []
    if a.get("passa_alto_hz"):
        f.append(f"highpass=f={int(a['passa_alto_hz'])}")
    if a.get("riduzione_rumore"):
        f.append(f"afftdn={a['riduzione_rumore']}")
    if a.get("deesser"):
        f.append(f"deesser={a['deesser']}")
    if a.get("compressore"):
        f.append(f"acompressor={a['compressore']}")
    return ",".join(f) or "anull"


def _loudnorm(a: dict) -> str:
    return (f"loudnorm=I={float(a.get('loudness_lufs', -14))}:TP={float(a.get('picco_db', -1))}"
            f":LRA={float(a.get('lra', 11))}")


def misura_loudness(video: Path, cfg: Config | None = None) -> dict:
    """Primo passaggio di loudnorm: le misure del reel, in JSON dallo stderr di ffmpeg."""
    import json
    import subprocess
    ff, _ = trova_ffmpeg()
    r = subprocess.run([ff, "-hide_banner", "-nostats", "-i", str(video), "-vn",
                        "-af", _loudnorm(_audio(cfg)) + ":print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    testo = r.stderr
    inizio = testo.rfind("{")
    if r.returncode != 0 or inizio < 0:
        raise RuntimeError(f"loudnorm, misura fallita: {testo.strip()[-300:]}")
    return json.loads(testo[inizio:testo.rfind("}") + 1])


def comando_normalizza(video: Path, dest: Path, misure: dict, cfg: Config | None = None) -> list[str]:
    ff, _ = trova_ffmpeg()
    m = misure
    filtro = (_loudnorm(_audio(cfg)) + f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
              f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    return [ff, "-y", "-loglevel", "error", "-i", str(video), "-map", "0:v", "-map", "0:a", "-c:v", "copy",
            "-af", filtro, "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", str(dest)]


def normalizza_audio(video: Path, cfg: Config | None = None) -> dict | None:
    """Secondo passaggio: il reel intero al bersaglio di `[audio]` (−14 LUFS, picco −1 dB), video copiato così com'è.
    Ritorna le misure prima e il bersaglio; None se la catena è spenta."""
    a = _audio(cfg)
    if not a.get("catena", True):
        return None
    m = misura_loudness(video, cfg)
    if not str(m.get("input_i", "")).lstrip("-").replace(".", "", 1).isdigit():   # «-inf»: nessun audio, niente da alzare
        return {"prima_lufs": None, "prima_picco_db": None, "bersaglio_lufs": None}
    tmp = video.with_name(video.stem + ".audio" + video.suffix)
    try:
        esegui(comando_normalizza(video, tmp, m, cfg), "ffmpeg (volume del reel)")
    except RuntimeError:
        tmp.unlink(missing_ok=True)
        raise
    tmp.replace(video)
    return {"prima_lufs": float(m["input_i"]), "prima_picco_db": float(m["input_tp"]),
            "bersaglio_lufs": float(a.get("loudness_lufs", -14))}


def comando_confronto(clip: Path, dest: Path, secondi: float = 12.0, cfg: Config | None = None) -> list[str]:
    """Prima/dopo per l'orecchio: lo stesso pezzo di presa, prima solo col volume e poi con la catena, allo stesso
    bersaglio di loudness (così si sente la pulizia, non il volume), separati da un secondo di silenzio."""
    ff, _ = trova_ffmpeg()
    a = _audio(cfg)
    ln = _loudnorm(a)
    voce = catena_voce(cfg) or "anull"
    grafo = (f"[0:a]aresample=48000,atrim=0:{secondi:.2f},asetpts=PTS-STARTPTS,asplit=2[x][y];"
             f"[x]{ln}[prima];[y]{voce},{ln}[dopo];"
             f"anullsrc=r=48000:cl=mono,atrim=0:1[pausa];"
             f"[prima]aresample=48000,aformat=channel_layouts=mono[p1];[dopo]aresample=48000,aformat=channel_layouts=mono[p2];"
             f"[p1][pausa][p2]concat=n=3:v=0:a=1[out]")
    return [ff, "-y", "-loglevel", "error", "-i", str(clip), "-filter_complex", grafo, "-map", "[out]",
            "-c:a", "aac", "-b:a", "192k", str(dest)]


def concatena(scene: list[tuple[Path, float]], dest: Path, transizione: str = "dissolvenza", durata_trans_s: float = 0.25,
              cfg: Config | None = None, anteprima: bool = False, tagli: frozenset[int] = frozenset()) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    esegui(comando_concat(scene, dest, transizione, durata_trans_s, cfg, anteprima, tagli), "ffmpeg (concat)")
    return dest
