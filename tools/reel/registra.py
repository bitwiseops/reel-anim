"""Registrazione guidata (logica pura, senza Tk): la timeline dell'anteprima, il karaoke, i comandi ffmpeg di
cattura/riproduzione/taglio, le prese e la spezzatura in clip per scena.

Modalità: presa unica. L'app riproduce l'anteprima di `monta --prova` (muta) mentre un processo ffmpeg registra la
webcam in `_prese/presa-NN.mov` e manda gli stessi fotogrammi, ridotti, su una pipe: l'indice k del fotogramma letto
dalla pipe è il tempo k/fps nel file. L'audio lo registra Python (PortAudio via `sounddevice`) in `_prese/presa-NN.wav`:
avfoundation perde il 10-15 % dei pacchetti audio su questa macchina, PortAudio no. Quando parte la riproduzione si
annotano k0 (fotogrammi letti) e n0 (campioni registrati): da lì ogni istante del reel ha il suo istante nel video e
nell'audio della presa. A fine presa ogni scena coperta per intero diventa `scena-NN.mov` (video ritagliato
sull'inquadratura scelta + audio) con accanto `scena-NN.json` (gli inizi delle frasi seguiti nella presa, che il
montaggio usa al posto della stima a parole).
"""
from __future__ import annotations

import json
import math
import re
import subprocess
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime
from pathlib import Path

from ..anim.config import Config
from . import clip as clipmod
from .compositing import posizione_riquadro
from .ffmpeg import esegui, trova_ffmpeg
from .model import PIENO, Diagnostica, Reel, avviso, testo_piano
from .percorsi import impronta
from .voce import CODA_VOCE_S

from ..anim.config import RADICE
PRESE = "_prese"

REGISTRAZIONE_DEFAULT = {
    "video": 0, "audio": None,              # fotocamera (avfoundation) e microfono (PortAudio; None = predefinito): indice o parte del nome
    "risoluzione": "1920x1080", "fps": 30, "pixel_format": "nv12", "frequenza_audio": 48000,
    "preroll_s": 2.0,                       # il reel parte questi secondi prima della scena scelta
    "conto_alla_rovescia_s": 3,
    "latenza_s": 0.10,                      # sensore + fps + pipe: quanto il fotogramma letto è più vecchio dell'istante di lettura
    "coda_presa_s": 0.5,                    # a fine reel si continua a registrare questi secondi
    "codec": "h264_videotoolbox", "bitrate": "8M",
    "altezza_pannelli_px": None,            # None = quanta ne lascia lo schermo sopra i comandi
    "fps_pannelli": 30,
    "timeout_apertura_s": 20.0,             # macOS può chiedere il permesso per la fotocamera: si aspetta
}


def opzioni(cfg: Config, video: int | str | None = None, audio: int | str | None = None) -> dict:
    """Default ⊕ [registrazione] del config ⊕ dispositivi scelti nella finestra l'ultima volta ⊕ riga di comando."""
    o = {**REGISTRAZIONE_DEFAULT, **cfg.dati.get("registrazione", {}), **dispositivi_scelti()}
    if video is not None:
        o["video"] = video
    if audio is not None:
        o["audio"] = audio
    return o


DISPOSITIVI_SCELTI = RADICE / "contenuti" / "media" / "dispositivi.json"   # per macchina, non per reel (gitignored)


def dispositivi_scelti(percorso: Path | None = None) -> dict:
    """{"video": nome, "audio": nome} scelti nella finestra: per nome, perché gli indici cambiano con i dispositivi collegati."""
    percorso = percorso or DISPOSITIVI_SCELTI
    if not percorso.exists():
        return {}
    try:
        d = json.loads(percorso.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return {k: d[k] for k in ("video", "audio") if isinstance(d.get(k), str) and d[k]}


def salva_dispositivi_scelti(scelti: dict, percorso: Path | None = None) -> Path:
    percorso = percorso or DISPOSITIVI_SCELTI
    percorso.parent.mkdir(parents=True, exist_ok=True)
    percorso.write_text(json.dumps({**dispositivi_scelti(percorso), **scelti}, ensure_ascii=False), encoding="utf-8")
    return percorso


# --- timeline dell'anteprima ------------------------------------------------------------------------

@dataclass(frozen=True)
class Frase:
    testo: str
    parole: tuple[str, ...]
    t_inizio_s: float      # assoluti nel reel
    t_fine_s: float
    grezzo: str = ""       # la riga con i segni (==evidenzia==): va nel sidecar, le caption si fanno da qui


@dataclass(frozen=True)
class ScenaTL:
    n: int
    tipo: str
    t_inizio_s: float
    durata_s: float
    riquadro: str
    frasi: tuple[Frase, ...]

    @property
    def t_fine_s(self) -> float:
        return self.t_inizio_s + self.durata_s


@dataclass(frozen=True)
class Timeline:
    scene: tuple[ScenaTL, ...]
    durata_s: float
    fps: int
    reel: Path
    hash_md: str
    sovrapposizione_s: float   # le scene si sovrappongono di questo (la dissolvenza del montaggio)

    def scena_a(self, t: float) -> ScenaTL | None:
        """La scena in corso a t; nella sovrapposizione fra due scene vince quella che comincia."""
        for s in reversed(self.scene):
            if s.t_inizio_s <= t < s.t_fine_s:
                return s
        return None

    def scena_n(self, n: int) -> ScenaTL:
        return self.scene[self.indice(n)]

    def indice(self, n: int) -> int:
        for i, s in enumerate(self.scene):
            if s.n == n:
                return i
        raise KeyError(f"scena {n} assente dalla timeline")

    @property
    def frasi(self) -> list[Frase]:
        return [f for s in self.scene for f in s.frasi]


class ReportNonPronto(RuntimeError):
    pass


def _frase(riga: str, t_inizio: float, t_fine: float) -> Frase:
    piano = testo_piano(riga)
    return Frase(piano, tuple(piano.split()), t_inizio, t_fine, riga)


def con_voce(tl: Timeline, n: int, righe: list[str]) -> Timeline:
    """La timeline con il testo della scena n cambiato (la correzione fatta nella finestra): i tempi restano."""
    s = tl.scena_n(n)
    if len(righe) != len(s.frasi):
        raise ValueError(f"scena {n}: {len(righe)} righe per {len(s.frasi)} frasi")
    frasi = tuple(_frase(v, f.t_inizio_s, f.t_fine_s) for v, f in zip(righe, s.frasi))
    return replace(tl, scene=tuple(replace(x, frasi=frasi) if x.n == n else x for x in tl.scene))


def timeline_da_report(report: dict, r: Reel, cfg: Config, parlato: dict[int, list[str]] | None = None) -> Timeline:
    """Timeline dal report.json di `monta --prova`; ReportNonPronto se l'anteprima non c'è o non corrisponde alla sceneggiatura.
    `parlato` = le righe corrette in registrazione (clip.carica_parlato), al posto della VOCE: i tempi restano del report."""
    if not report.get("prova"):
        raise ReportNonPronto("il report non è di un'anteprima --prova")
    reel = report.get("reel") or {}
    if not reel.get("file"):
        raise ReportNonPronto("il report non ha il reel concatenato (montaggio parziale o con errori)")
    elementi = report.get("elementi") or []
    if [e.get("scena") for e in elementi] != [s.n for s in r.scene]:
        raise ReportNonPronto("le scene del report non coincidono con quelle della sceneggiatura")
    pausa = float(cfg.dati["voce_sintetica"].get("pausa_frasi_s", 0.3))
    tr = cfg.dati.get("transizioni", {})
    sovr = float(tr.get("durata_s", 0.25)) if tr.get("tipo", "dissolvenza") == "dissolvenza" else 0.0
    scene = []
    for e, s in zip(elementi, r.scene):
        if "t_inizio_s" not in e:
            raise ReportNonPronto(f"scena {s.n}: tempi assoluti assenti dal report")
        t0, d = float(e["t_inizio_s"]), float(e["durata_s"])
        inizi = [float(x) for x in e.get("inizi_frasi_s") or []]
        if len(inizi) != len(s.voce):
            raise ReportNonPronto(f"scena {s.n}: {len(inizi)} tempi nel report per {len(s.voce)} frasi: rifai monta --prova")
        righe = (parlato or {}).get(s.n)
        if righe is None or len(righe) != len(s.voce):   # una correzione vecchia con un altro numero di frasi non vale
            righe = s.voce
        frasi = []
        for j, (v, i) in enumerate(zip(righe, inizi)):
            fine = (inizi[j + 1] - pausa) if j + 1 < len(inizi) else d - CODA_VOCE_S
            fine = max(fine, i + 0.2)
            frasi.append(_frase(v, round(t0 + i, 3), round(t0 + fine, 3)))
        scene.append(ScenaTL(s.n, s.tipo, t0, d, str(e.get("riquadro") or s.riquadro_effettivo()), tuple(frasi)))
    return Timeline(tuple(scene), float(reel.get("durata_s") or scene[-1].t_fine_s), int(reel.get("fps") or cfg.fps),
                    Path(report["cartella"]) / reel["file"], str(report.get("hash_md") or ""), sovr)


def carica_timeline(r: Reel, out: Path, cfg: Config) -> tuple[Timeline, list[Diagnostica]]:
    """Legge la copia stabile dell'anteprima (report-prova.json, che il montaggio con le clip vere non tocca) o,
    se manca, report.json; avvisa se l'anteprima è di una versione precedente della sceneggiatura."""
    p = out / "report-prova.json"
    if not p.exists():
        p = out / "report.json"
    if not p.exists():
        raise ReportNonPronto(f"manca {p}")
    tl = timeline_da_report(json.loads(p.read_text(encoding="utf-8")), r, cfg, clipmod.carica_parlato(r.slug))
    if not tl.reel.exists():
        raise ReportNonPronto(f"manca il video dell'anteprima {tl.reel}")
    diag: list[Diagnostica] = []
    if r.sorgente and tl.hash_md and impronta(r.sorgente) != tl.hash_md:
        diag.append(avviso("l'anteprima è di una versione precedente della sceneggiatura: rifai `monta --prova --anteprima`"))
    return tl, diag


# --- karaoke ------------------------------------------------------------------------------------------

@dataclass(frozen=True)
class Karaoke:
    scena: ScenaTL | None
    frase: Frase | None        # in corso
    accese: int                # parole già dette della frase in corso
    frazione_scena: float
    precedente: Frase | None   # l'ultima finita
    prossima: Frase | None     # la prima che deve ancora cominciare
    attesa_s: float            # quanto manca alla prossima (0 se una frase è in corso o non ce ne sono più)


def parole_accese(f: Frase, t: float) -> int:
    """Quante parole della frase sono già dette a t: in proporzione ai caratteri (spazi inclusi)."""
    if t >= f.t_fine_s:
        return len(f.parole)
    if t <= f.t_inizio_s or not f.parole:
        return 0
    frazione = (t - f.t_inizio_s) / (f.t_fine_s - f.t_inizio_s)
    totale = len(f.testo)
    fine, n = 0, 0
    for p in f.parole:
        fine += len(p) + 1
        if fine - 1 <= frazione * totale:
            n += 1
    return n


def karaoke(tl: Timeline, t: float) -> Karaoke:
    scena = tl.scena_a(t)
    corrente = precedente = prossima = None
    for f in tl.frasi:
        if f.t_inizio_s <= t < f.t_fine_s and (scena is None or f in scena.frasi):
            corrente = f
        elif f.t_fine_s <= t:
            precedente = f
        elif f.t_inizio_s > t and prossima is None:
            prossima = f
    frazione = min(1.0, max(0.0, (t - scena.t_inizio_s) / scena.durata_s)) if scena and scena.durata_s > 0 else 0.0
    attesa = (prossima.t_inizio_s - t) if (prossima and corrente is None) else 0.0
    return Karaoke(scena, corrente, parole_accese(corrente, t) if corrente else 0, frazione, precedente, prossima, round(attesa, 2))


# --- comandi ffmpeg -----------------------------------------------------------------------------------

# --- livello del microfono (vu-meter) ------------------------------------------------------------------

# Il 23/09 le prese di ia-e-lavoro erano a −37 LUFS: il montaggio le alzava di 20 dB, e con la voce il rumore della
# stanza. Il bersaglio sono picchi del parlato fra −18 e −3 dBFS (le soglie dicono il primo giudizio che vale).
SOGLIE_LIVELLO = ((-1.0, "satura"), (-3.0, "alto"), (-18.0, "buono"), (-30.0, "basso"))
SILENZIO_DB = -90.0


def dbfs(picco_campione: int, fondo_scala: int = 32768) -> float:
    """Il picco di un blocco PCM 16 bit in dBFS (0 = fondo scala)."""
    import math
    return max(SILENZIO_DB, 20 * math.log10(max(abs(picco_campione), 1) / fondo_scala))


def giudizio_livello(picco_db: float) -> str:
    for soglia, nome in SOGLIE_LIVELLO:
        if picco_db >= soglia:
            return nome
    return "troppo basso"


def dimensioni_pipe(risoluzione: str, larghezza: int) -> tuple[int, int]:
    """Dimensioni (pari) dell'anteprima ridotta di un flusso WxH portato a `larghezza` px."""
    w, h = (int(x) for x in risoluzione.lower().split("x"))
    hh = round(h * larghezza / w)
    return larghezza - larghezza % 2, hh - hh % 2


def snap_fotogramma(t: float, fps: int) -> float:
    return max(0.0, math.floor(t * fps + 1e-9) / fps)


def comando_cattura(opz: dict, file: Path | None, dim_pipe: tuple[int, int], sorgente: list[str] | None = None) -> list[str]:
    """ffmpeg che legge la webcam (solo video: l'audio lo registra `cattura.Microfono`) e scrive (a) la presa su
    `file` e (b) i fotogrammi ridotti rgb24 su stdout. Con file=None è la sola anteprima fra una presa e l'altra.
    `sorgente` sostituisce l'input avfoundation (test con lavfi)."""
    ff, _ = trova_ffmpeg()
    fps, w, h = int(opz["fps"]), *dim_pipe
    if sorgente is None:
        sorgente = ["-f", "avfoundation", "-framerate", str(fps), "-video_size", str(opz["risoluzione"]),
                    "-pixel_format", str(opz["pixel_format"]), "-thread_queue_size", "1024", "-i", str(opz["video"])]
    cmd = [ff, "-hide_banner", "-loglevel", "warning", "-nostats", "-y", *sorgente]
    pipe = f"scale={w}:{h}[vp]"
    if file is None:
        cmd += ["-filter_complex", f"[0:v]fps={fps},{pipe}"]
    else:
        cmd += ["-filter_complex", f"[0:v]fps={fps},split=2[vf][vp0];[vp0]{pipe}",
                "-map", "[vf]", "-an", *_codifica_video(opz, realtime=True), "-fps_mode", "passthrough", "-f", "mov", str(file)]
    cmd += ["-map", "[vp]", "-pix_fmt", "rgb24", "-fps_mode", "passthrough", "-f", "rawvideo", "pipe:1"]
    return cmd


# --- inquadratura: il quadrato della webcam che finisce nel riquadro ------------------------------------

def inquadratura_default(risoluzione: str) -> dict:
    """Il quadrato centrale più grande: è ciò che farebbe il montaggio da solo."""
    w, h = (int(x) for x in risoluzione.lower().split("x"))
    lato = min(w, h)
    return {"x": (w - lato) // 2, "y": (h - lato) // 2, "lato": lato}


def limita_inquadratura(inq: dict, risoluzione: str, minimo: int) -> dict:
    """Tiene il quadrato dentro il fotogramma e non più piccolo del riquadro (mai ingrandire i pixel)."""
    w, h = (int(x) for x in risoluzione.lower().split("x"))
    lato = int(max(min(int(inq.get("lato", min(w, h))), min(w, h)), min(minimo, min(w, h))))
    x = int(min(max(int(inq.get("x", 0)), 0), w - lato))
    y = int(min(max(int(inq.get("y", 0)), 0), h - lato))
    return {"x": x, "y": y, "lato": lato}


def carica_inquadratura(cartella: Path, risoluzione: str, minimo: int) -> dict:
    p = cartella / "inquadratura.json"
    if p.exists():
        try:
            return limita_inquadratura(json.loads(p.read_text(encoding="utf-8")), risoluzione, minimo)
        except (json.JSONDecodeError, ValueError, TypeError):
            pass
    return inquadratura_default(risoluzione)


def salva_inquadratura(cartella: Path, inq: dict) -> Path:
    p = cartella / "inquadratura.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(inq), encoding="utf-8")
    return p


def _codifica_video(opz: dict, realtime: bool = False) -> list[str]:
    codec = str(opz["codec"])
    c = ["-c:v", codec]
    if codec == "h264_videotoolbox":
        c += (["-realtime", "1", "-prio_speed", "1"] if realtime else []) + ["-profile:v", "high"]
    elif codec == "libx264":
        c += ["-preset", "ultrafast" if realtime else "fast"]
    return c + ["-b:v", str(opz["bitrate"]), "-g", str(opz["fps"]), "-pix_fmt", "nv12" if codec == "h264_videotoolbox" else "yuv420p"]


def _codifica_audio() -> list[str]:
    # PCM: nessuna generazione lossy in più (il montaggio ricodifica, normalizza e forza lo stereo)
    return ["-c:a", "pcm_s16le", "-ar", "48000", "-ac", "1"]


def comando_riproduzione(reel: Path, t0_s: float, dim: tuple[int, int]) -> list[str]:
    """ffmpeg che decodifica il reel dall'istante t0_s (già allineato con snap_fotogramma) in rgb24 ridotto su stdout,
    muto: il presentatore legge il karaoke e il microfono registra. Il ritmo lo dà chi legge la pipe, non -re."""
    ff, _ = trova_ffmpeg()
    w, h = dim
    return [ff, "-hide_banner", "-loglevel", "error", "-nostats", "-ss", f"{t0_s:.3f}", "-i", str(reel), "-an",
            "-vf", f"scale={w}:{h}", "-pix_fmt", "rgb24", "-f", "rawvideo", "pipe:1"]


def riquadro_in_scala(cfg: Config, riquadro: str, scala: float) -> tuple[int, int, int]:
    """(x, y, lato) del riquadro del presentatore nell'anteprima ridotta."""
    x, y, d = posizione_riquadro(cfg, riquadro)
    return round(x * scala), round(y * scala), round(d * scala)


# --- prese e spezzatura -------------------------------------------------------------------------------

@dataclass
class Presa:
    nome: str                 # presa-02
    file: str                 # relativo a contenuti/media/<slug>/: _prese/presa-02.mov (solo video)
    da_scena: int
    t_reel0_s: float          # istante del reel a cui è partita la riproduzione (può essere < 0: pre-roll della scena 1)
    k0: int                   # fotogrammi della presa già letti dalla pipe in quell'istante
    inizio_video_s: float     # start_time del video nel file (ffprobe)
    latenza_s: float          # quanto il fotogramma letto è più vecchio dell'istante di lettura
    fps: int
    t_reel_stop_s: float      # istante del reel a cui la presa si è fermata
    quando: str
    hash_md: str
    scene: list[int] = field(default_factory=list)   # scene tagliate da questa presa
    audio: str = ""           # _prese/presa-02.wav (vuoto: audio dentro il file video, prese vecchie)
    n0: int = 0               # campioni audio già registrati quando è partita la riproduzione
    frequenza_audio: int = 48000
    latenza_audio_s: float = 0.0   # latenza d'ingresso riferita da PortAudio
    inquadratura: dict | None = None   # {x, y, lato} in pixel della cattura: il quadrato che va nel riquadro

    def t_file(self, t_reel: float) -> float:
        """L'istante nel video della presa che corrisponde a t_reel."""
        return self.inizio_video_s + self.k0 / self.fps + self.latenza_s + (t_reel - self.t_reel0_s)

    def t_audio(self, t_reel: float) -> float:
        """L'istante nel wav della presa che corrisponde a t_reel: i campioni contati a T0 erano stati captati
        latenza_audio_s prima, quindi l'istante T0 nel wav è n0/f + latenza."""
        return self.n0 / self.frequenza_audio + self.latenza_audio_s + (t_reel - self.t_reel0_s)


def scene_coperte(tl: Timeline, p: Presa) -> list[ScenaTL]:
    """Le scene registrate per intero dalla presa: dalla scena di partenza in poi, finite prima dello stop."""
    return [s for s in tl.scene if s.n >= p.da_scena and s.t_inizio_s >= p.t_reel0_s and s.t_fine_s <= p.t_reel_stop_s + 1e-6]


def comando_taglio(p: Presa, s: ScenaTL, presa: Path, dest: Path, opz: dict, audio: Path | None = None) -> list[str]:
    """Taglia dalla presa la clip della scena: seek preciso (ri-codifica) sul video e sul wav, durata a fotogrammi
    interi, ritaglio sull'inquadratura scelta (un quadrato: il montaggio poi lo porta a 360 px senza tagliare altro),
    tranne nelle scene a volto pieno, che tengono il fotogramma intero.
    Niente loudnorm: lo fa il montaggio."""
    ff, _ = trova_ffmpeg()
    fps = int(opz["fps"])
    durata = round(s.durata_s * fps) / fps
    cmd = [ff, "-hide_banner", "-loglevel", "error", "-y", "-ss", f"{p.t_file(s.t_inizio_s):.3f}", "-i", str(presa)]
    if audio is not None:
        cmd += ["-ss", f"{p.t_audio(s.t_inizio_s):.3f}", "-i", str(audio)]
    cmd += ["-t", f"{durata:.3f}", "-map", "0:v"]
    cmd += ["-map", "1:a"] if audio is not None else (["-map", "0:a"] if not p.audio else ["-an"])
    # a volto pieno (apertura e chiusura, dal 2026-09-21) la tela è lui: si tiene il fotogramma intero, e il
    # montaggio lo porta a 1080×1920. Il quadrato dell'inquadratura serve solo alle scene col riquadro.
    if p.inquadratura and s.riquadro != PIENO:
        q = p.inquadratura
        cmd += ["-vf", f"crop={q['lato']}:{q['lato']}:{q['x']}:{q['y']}"]
    cmd += [*_codifica_video(opz), *_codifica_audio(), "-fps_mode", "cfr", "-r", str(fps), "-f", "mov", str(dest)]
    return cmd


def scrivi_sidecar(clip: Path, s: ScenaTL, p: Presa) -> Path:
    dati = {"inizi_frasi_s": [round(f.t_inizio_s - s.t_inizio_s, 3) for f in s.frasi], "origine_tempi": "presa",
            "presa": p.file, "t_reel_s": s.t_inizio_s, "t_presa_s": round(p.t_file(s.t_inizio_s), 3),
            "durata_s": s.durata_s, "hash_md": p.hash_md, "quando": p.quando,
            "voce": [f.grezzo or f.testo for f in s.frasi]}   # il testo recitato: le caption si fanno da qui
    dest = clipmod.sidecar(clip)
    dest.write_text(json.dumps(dati, ensure_ascii=False, indent=1), encoding="utf-8")
    return dest


def registro(cartella: Path) -> list[dict]:
    p = cartella / PRESE / "prese.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def salva_registro(cartella: Path, prese: list[dict]) -> Path:
    p = cartella / PRESE / "prese.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(prese, ensure_ascii=False, indent=1), encoding="utf-8")
    return p


def aggiorna_registro(cartella: Path, p: Presa) -> None:
    prese = [x for x in registro(cartella) if x.get("nome") != p.nome]
    prese.append(asdict(p))
    salva_registro(cartella, prese)


def presa_dal_registro(cartella: Path, nome: str) -> Presa:
    for x in registro(cartella):
        if x.get("nome") == nome or x.get("file") == nome:
            return Presa(**x)
    raise KeyError(f"presa {nome} assente da {cartella / PRESE / 'prese.json'}")


def prossima_presa(cartella: Path) -> str:
    """Il nome della prossima presa: presa-NN con NN dopo l'ultimo fra file e registro."""
    usati = [int(m.group(1)) for x in registro(cartella) if (m := re.fullmatch(r"presa-(\d+)", str(x.get("nome", ""))))]
    usati += [int(m.group(1)) for f in (cartella / PRESE).glob("presa-*.mov") if (m := re.fullmatch(r"presa-(\d+)", f.stem))]
    return f"presa-{max(usati, default=0) + 1:02d}"


def spezza(tl: Timeline, p: Presa, cartella: Path, opz: dict, avanzamento=None) -> list[Path]:
    """Taglia le scene coperte dalla presa in scena-NN.mov (+ sidecar) e aggiorna il registro. `avanzamento(i, n, scena)`
    viene chiamato prima di ogni taglio."""
    scene = scene_coperte(tl, p)
    fatte: list[Path] = []
    presa = cartella / p.file
    audio = (cartella / p.audio) if p.audio else None
    p.scene = []
    for i, s in enumerate(scene):
        if avanzamento:
            avanzamento(i, len(scene), s)
        dest = cartella / clipmod.nome_atteso(s.n)
        esegui(comando_taglio(p, s, presa, dest, opz, audio), f"ffmpeg (taglio scena {s.n})")
        scrivi_sidecar(dest, s, p)
        p.scene.append(s.n)
        fatte.append(dest)
        aggiorna_registro(cartella, p)
    if not scene:
        aggiorna_registro(cartella, p)
    return fatte


def nuova_presa(nome: str, da_scena: int, t_reel0_s: float, k0: int, inizio_video_s: float, opz: dict, t_reel_stop_s: float,
                hash_md: str, n0: int = 0, latenza_audio_s: float = 0.0, inquadratura: dict | None = None,
                con_audio: bool = True) -> Presa:
    return Presa(nome, f"{PRESE}/{nome}.mov", da_scena, round(t_reel0_s, 3), k0, inizio_video_s, float(opz["latenza_s"]),
                 int(opz["fps"]), round(t_reel_stop_s, 3), datetime.now().isoformat(timespec="seconds"), hash_md,
                 audio=f"{PRESE}/{nome}.wav" if con_audio else "", n0=n0, frequenza_audio=int(opz["frequenza_audio"]),
                 latenza_audio_s=round(latenza_audio_s, 4), inquadratura=dict(inquadratura) if inquadratura else None)


# --- dispositivi --------------------------------------------------------------------------------------

def dispositivi(stderr: str) -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    """Parser dell'elenco di `ffmpeg -f avfoundation -list_devices true`: (video, audio) come (indice, nome)."""
    video: list[tuple[int, str]] = []
    audio: list[tuple[int, str]] = []
    corrente = None
    for riga in stderr.splitlines():
        if "video devices" in riga:
            corrente = video
        elif "audio devices" in riga:
            corrente = audio
        elif corrente is not None and (m := re.search(r"\[(\d+)\] (.+?)\s*$", riga)):
            corrente.append((int(m.group(1)), m.group(2)))
    return video, audio


def dispositivi_audio() -> list[tuple[int, str]]:
    """I microfoni visti da PortAudio (indice globale di sounddevice, nome)."""
    import sounddevice as sd
    return [(i, str(d["name"])) for i, d in enumerate(sd.query_devices()) if int(d.get("max_input_channels", 0)) > 0]


def elenca_dispositivi() -> tuple[list[tuple[int, str]], list[tuple[int, str]]]:
    """(fotocamere avfoundation, microfoni PortAudio)."""
    ff, _ = trova_ffmpeg()
    # l'elenco va su stderr e ffmpeg esce con un codice diverso da 0: è normale
    r = subprocess.run([ff, "-hide_banner", "-f", "avfoundation", "-list_devices", "true", "-i", ""], capture_output=True, text=True)
    return dispositivi(r.stderr)[0], dispositivi_audio()


def indice_dispositivo(spec: int | str, lista: list[tuple[int, str]]) -> int:
    """Un indice, oppure una parte del nome (i nomi sono localizzati: «MacBook» basta); prima il nome intero."""
    if isinstance(spec, int) or str(spec).isdigit():
        return int(spec)
    for i, nome in lista:
        if str(spec).lower() == nome.lower():
            return i
    for i, nome in lista:
        if str(spec).lower() in nome.lower():
            return i
    raise ValueError(f"dispositivo «{spec}» non trovato fra: " + ", ".join(f"[{i}] {n}" for i, n in lista))
