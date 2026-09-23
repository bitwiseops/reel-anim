"""`broll rendi`: dai tagli scelti al file della scena, `contenuti/media/<slug>/broll-scena-NN.mp4`.

Verso il montaggio il contratto è uno solo, uguale per i tre registri: **un file per scena**, già
1080×1920, già lungo quanto la scena, muto. Qui si scarica il filmato scelto (una volta: la cache è
`contenuti/media/_cache-broll/`, fuori da git e ricostruibile dal piano), lo si ritaglia a 9:16
sull'ancora scelta e si concatenano i tagli con gli stacchi sui beat.

La lunghezza si conta in **fotogrammi**, non in secondi: ogni taglio è chiuso da `trim=end_frame`, così
la somma è esatta anche quando il filmato d'origine è a 25 o a 60 fps e `-t` arrotonderebbe per conto suo.
"""
from __future__ import annotations

import hashlib
from collections.abc import Callable
from pathlib import Path

from tools.anim.config import Config, carica
from tools.reel.clip import cartella as cartella_media
from tools.reel.ffmpeg import esegui, ffprobe, trova_ffmpeg
from tools.reel.model import Diagnostica, avviso

from .fornitori import Candidato, pexels
from .immagini import ImmaginiMancanti, componi
from .piano import ScenaBroll
from .scelta import confini

RADICE = Path(__file__).resolve().parents[2]
CACHE = RADICE / "contenuti" / "media" / "_cache-broll"
FORNITORI = {pexels.NOME: pexels}
MARGINE_S = 0.5         # si legge un po' oltre il taglio: a chiuderlo al fotogramma ci pensa `trim`


class ResaFallita(RuntimeError):
    pass


def sha256(f: Path) -> str:
    h = hashlib.sha256()
    with f.open("rb") as fh:
        for pezzo in iter(lambda: fh.read(1 << 20), b""):
            h.update(pezzo)
    return h.hexdigest()


def procura(taglio: dict, cache: Path = CACHE) -> Path:
    """Il filmato del taglio, dalla cache o scaricato adesso."""
    fornitore = FORNITORI.get(taglio["fornitore"])
    if fornitore is None:
        raise ResaFallita(f"fornitore «{taglio['fornitore']}» sconosciuto")
    dest = cache / f"{taglio['fornitore']}-{taglio['id']}.mp4"
    return fornitore.scarica(Candidato.da_dict(taglio), dest)


def fotogrammi(finestre: list[tuple[float, float]], fps: int) -> list[int]:
    """Quanti fotogrammi per taglio. Si arrotondano i bordi e non le durate, così la somma torna."""
    bordi = [round(finestre[0][0] * fps)] + [round((t + d) * fps) for t, d in finestre]
    return [b - a for a, b in zip(bordi, bordi[1:])]


def comando(sorgenti: list[Path], tagli: list[dict], finestre: list[tuple[float, float]],
            dest: Path, cfg: Config) -> list[str]:
    ff, _ = trova_ffmpeg()
    W, H, fps = cfg.larghezza, cfg.altezza, cfg.fps
    ingressi: list[str] = []
    filtri: list[str] = []
    for i, (f, taglio, (_, durata), n) in enumerate(zip(sorgenti, tagli, finestre, fotogrammi(finestre, fps))):
        ingressi += ["-ss", f"{float(taglio.get('da_s') or 0):.3f}", "-t", f"{durata + MARGINE_S:.3f}", "-i", str(f)]
        # `-ss` prima di `-i` lascia i PTS d'origine: senza setpts il concat non li mette in fila
        filtri.append(f"[{i}:v]setpts=PTS-STARTPTS,scale={W}:{H}:force_original_aspect_ratio=increase,"
                      f"crop={W}:{H}:(in_w-out_w)*{float(taglio.get('ancora', 0.5)):.3f}:(in_h-out_h)/2,"
                      f"fps={fps},trim=end_frame={n},setpts=PTS-STARTPTS,setsar=1,format=yuv420p[v{i}]")
    filtri.append("".join(f"[v{i}]" for i in range(len(tagli))) + f"concat=n={len(tagli)}:v=1:a=0[out]")
    return [ff, "-y", "-loglevel", "error", *ingressi, "-filter_complex", ";".join(filtri),
            "-map", "[out]", "-an", "-r", str(fps),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", str(dest)]


def file_immagini(s: ScenaBroll) -> list[Path]:
    """Le immagini generate della scena, nell'ordine del piano. I percorsi sono relativi alla radice."""
    fuori: list[Path] = []
    for t in s.scelti:
        f = Path(t.get("file") or "")
        fuori.append(f if f.is_absolute() else RADICE / f)
    return fuori


def rendi_scena(slug: str, s: ScenaBroll, cfg: Config | None = None, *, dest: Path | None = None,
                procura: Callable[[dict], Path] = procura) -> tuple[Path, list[Diagnostica]]:
    """Rende la scena e controlla che il file rispetti il contratto. Aggiorna `s` (sha256, stato).

    Due registri, un solo contratto verso il montaggio: un file per scena, 1080×1920, muto, lungo quanto
    la scena al fotogramma. Le scene a `immagini` non scaricano niente — le immagini le ha già generate
    `broll genera` — e si compongono con la dissolvenza sugli inizi frase.
    """
    if s.registro == "immagini":
        return _rendi_immagini(slug, s, cfg or carica(), dest=dest)

    cfg = cfg or carica()
    diag: list[Diagnostica] = []
    dest = dest or cartella_media(slug) / (s.file or f"broll-scena-{s.n:02d}.mp4")
    finestre = confini(len(s.scelti), s.inizi_frasi_s, s.durata_s)

    sorgenti: list[Path] = []
    for taglio in s.scelti:
        f = procura(taglio)
        impronta = sha256(f)
        if taglio.get("sha256") and taglio["sha256"] != impronta:
            diag.append(avviso(f"{taglio['candidato']}: il file scaricato non è più quello del piano "
                               "(sha256 diverso): riguardalo prima di fidarti", scena=s.n))
        taglio["sha256"] = impronta
        sorgenti.append(f)

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.stem + ".tmp" + dest.suffix)
    try:
        esegui(comando(sorgenti, s.scelti, finestre, tmp, cfg), f"ffmpeg (resa scena {s.n})")
        _verifica(tmp, round(s.durata_s * cfg.fps), cfg)
    except RuntimeError:
        tmp.unlink(missing_ok=True)
        raise
    tmp.replace(dest)
    s.file, s.stato = dest.name, "reso"
    return dest, diag


def _rendi_immagini(slug: str, s: ScenaBroll, cfg: Config, *,
                    dest: Path | None = None) -> tuple[Path, list[Diagnostica]]:
    """Le immagini generate della scena, montate sugli inizi frase con la dissolvenza fra l'una e l'altra."""
    diag: list[Diagnostica] = []
    dest = dest or cartella_media(slug) / (s.file or f"broll-scena-{s.n:02d}.mp4")
    sorgenti = file_immagini(s)
    if not sorgenti:
        raise ResaFallita(f"scena {s.n}: nessuna immagine nel piano (prima `broll genera {slug} --scena {s.n}`)")
    if not s.inizi_frasi_s:
        diag.append(avviso("nessun inizio frase nel piano: un'immagine sola per tutta la scena "
                           "(prima `uv run reel monta … --prova`, poi `broll piano`)", scena=s.n))

    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.stem + ".tmp" + dest.suffix)
    try:
        _, tenute = componi(sorgenti, s.inizi_frasi_s, s.durata_s, tmp, cfg)
        _verifica(tmp, round(s.durata_s * cfg.fps), cfg)
    except ImmaginiMancanti as e:
        tmp.unlink(missing_ok=True)
        raise ResaFallita(str(e)) from e
    except RuntimeError:
        tmp.unlink(missing_ok=True)
        raise
    tmp.replace(dest)
    if len(sorgenti) < len(tenute):
        diag.append(avviso(f"{len(tenute)} frasi e {len(sorgenti)} immagini: le immagini si ripetono "
                           f"(`broll genera {slug} --scena {s.n} --quante {len(tenute)}`)", scena=s.n))
    elif len(sorgenti) > len(tenute):
        diag.append(avviso(f"{len(tenute)} frasi e {len(sorgenti)} immagini: le ultime "
                           f"{len(sorgenti) - len(tenute)} non si vedono (una immagine per frase)",
                           scena=s.n))
    s.file, s.stato = dest.name, "reso"
    return dest, diag


def _verifica(f: Path, attesi: int, cfg: Config) -> None:
    """Il contratto col montaggio: tela piena, muto, lungo quanto la scena al fotogramma."""
    info = ffprobe(f)
    if info.get("errore"):
        raise ResaFallita(f"non riesco a rileggere {f.name}: {info['errore']}")
    if (info["larghezza"], info["altezza"]) != (cfg.larghezza, cfg.altezza):
        raise ResaFallita(f"{f.name} è {info['larghezza']}×{info['altezza']}, non {cfg.larghezza}×{cfg.altezza}")
    if info["audio"]:
        raise ResaFallita(f"{f.name} ha una traccia audio: il b-roll è muto")
    if info["fotogrammi"] != attesi:
        raise ResaFallita(f"{f.name} ha {info['fotogrammi']} fotogrammi, la scena ne chiede {attesi}: "
                          "il filmato d'origine finisce prima del taglio")
