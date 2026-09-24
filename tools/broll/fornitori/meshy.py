"""Meshy text-to-image: immagini generate, per le scene che su Pexels non hanno un candidato buono.

È il terzo registro (`piano.REGISTRI`): quando una scena non si può animare e un filmato che la racconti
non esiste, si generano 2-3 immagini e si montano una per frase con una dissolvenza fra l'una e l'altra
(`immagini.componi`). Non è un ripiego grafico: è materiale nuovo fatto apposta per quella scena.

Lo schema è quello già collaudato in `~/Projects/3d-models-ai/src/meshy_client.py` — POST che ritorna un
task id, polling fino a `SUCCEEDED`, download dell'immagine, failover sulla seconda chiave quando la prima
ha finito i crediti — riscritto qui perché quel progetto resta separato: nessun import fra i due.

Generare costa. Per questo la cache è la prima cosa che si guarda: `config.toml [percorsi] cache_broll` (fuori dal progetto e
da git, come i filmati scaricati), un file per prompt e indice, così rilanciare `broll genera` non ripaga
niente. La chiave non si stampa mai, nemmeno nei messaggi d'errore.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from collections.abc import Callable
from pathlib import Path

import requests

from tools.reel.percorsi import cache_broll

from ..credenziali import chiavi as chiavi_fornitore
from . import FornitoreNonConfigurato, RichiestaFallita

NOME = "meshy"
BASE = "https://api.meshy.ai/openapi/v1"
MODELLO = "nano-banana-pro"          # lo stesso di 3d-models-ai: `config.MESHY_IMAGE_MODEL`
PROPORZIONI = "9:16"                 # la tela del reel: generare quadrato e ritagliare butta metà immagine
LICENZA = "Meshy — immagine generata"
SCADENZA_S = 60
INTERVALLO_S = 5.0
ATTESA_MAX_S = 900.0

RADICE = Path(__file__).resolve().parents[3]
CACHE = cache_broll()   # fuori dal progetto e mai ripulita da sé: le immagini generate si pagano (2026-09-23)


class CreditiEsauriti(RichiestaFallita):
    """Crediti finiti sulla chiave usata (402, o un corpo che parla di crediti): si passa alla riserva."""


class TaskFallito(RichiestaFallita):
    def __init__(self, stato: str, dettaglio) -> None:
        super().__init__(f"meshy: task {stato} ({dettaglio})")
        self.stato = stato
        self.dettaglio = dettaglio


# --- chiavi e richieste ---------------------------------------------------------------------------

def chiavi() -> list[str]:
    """Le chiavi utilizzabili, principale per prima. Mai stampate: per mostrarle c'è `broll chiavi`."""
    return chiavi_fornitore(NOME)


def _intestazioni(chiave: str) -> dict:
    if not chiave:
        raise FornitoreNonConfigurato("manca MESHY_API_KEY (vedi `broll chiavi`)")
    return {"Authorization": f"Bearer {chiave}", "Content-Type": "application/json"}


def _solleva(r: requests.Response, etichetta: str) -> None:
    """L'eccezione giusta per una POST fallita: crediti finiti → failover, il resto → errore secco."""
    corpo = (r.text or "")[:200]
    if r.status_code == 402 or any(t in corpo.lower() for t in ("credit", "insufficient", "balance", "payment")):
        raise CreditiEsauriti(f"meshy {etichetta}: {r.status_code} (crediti esauriti su questa chiave)")
    if r.status_code in (401, 403):
        raise FornitoreNonConfigurato(f"meshy rifiuta la chiave ({r.status_code}): controlla MESHY_API_KEY")
    raise RichiestaFallita(f"meshy {etichetta}: {r.status_code} {corpo}")


def avvia(prompt: str, chiave: str, *, modello: str = MODELLO,
          proporzioni: str = PROPORZIONI) -> str:
    """POST text-to-image: ritorna il task id. Il task appartiene all'account di `chiave`: il polling
    va fatto con la stessa."""
    corpo = {"prompt": prompt, "ai_model": modello, "aspect_ratio": proporzioni}
    try:
        r = requests.post(f"{BASE}/text-to-image", json=corpo,
                          headers=_intestazioni(chiave), timeout=SCADENZA_S)
    except requests.RequestException as e:
        raise RichiestaFallita(f"meshy non raggiungibile: {e}") from e
    if not r.ok:
        _solleva(r, "text-to-image")
    return r.json()["result"]


def attendi(task_id: str, chiave: str, *, intervallo_s: float = INTERVALLO_S,
            attesa_max_s: float = ATTESA_MAX_S, avanzamento: Callable[[int, str], None] | None = None) -> dict:
    """Polling fino a SUCCEEDED, o all'errore. Ritorna il task, da cui si prende `image_urls`."""
    url = f"{BASE}/text-to-image/{task_id}"
    partenza = time.monotonic()
    ultimo = -1
    while True:
        try:
            r = requests.get(url, headers=_intestazioni(chiave), timeout=SCADENZA_S)
        except requests.RequestException as e:
            raise RichiestaFallita(f"meshy non raggiungibile: {e}") from e
        if not r.ok:
            _solleva(r, f"stato del task {task_id}")
        task = r.json()
        stato = str(task.get("status") or "")
        quanto = int(task.get("progress") or 0)
        if quanto != ultimo:
            (avanzamento or _avanzamento)(quanto, stato)
            ultimo = quanto
        if stato == "SUCCEEDED":
            return task
        if stato in ("FAILED", "CANCELED"):
            raise TaskFallito(stato, task.get("task_error") or "")
        if time.monotonic() - partenza > attesa_max_s:
            raise RichiestaFallita(f"meshy: nessuna risposta dopo {attesa_max_s:.0f}s (ultimo stato: {stato})")
        time.sleep(intervallo_s)


def _avanzamento(quanto: int, stato: str) -> None:
    sys.stderr.write(f"\r    meshy: {stato} {quanto}%   ")
    sys.stderr.flush()
    if stato in ("SUCCEEDED", "FAILED", "CANCELED"):
        sys.stderr.write("\n")


def url_immagine(task: dict) -> str:
    """L'URL dell'immagine dentro un task riuscito. Meshy dà una lista anche quando l'immagine è una."""
    urls = task.get("image_urls") or []
    if isinstance(urls, list) and urls:
        return str(urls[0])
    for c in ("image_url", "result_url", "thumbnail_url"):
        if task.get(c):
            return str(task[c])
    raise RichiestaFallita("meshy: task riuscito ma senza immagine (image_urls vuoto)")


def con_failover(apri: Callable[[str], str], *, elenco: list[str] | None = None) -> tuple[str, str]:
    """Avvia il task provando le chiavi in ordine, e passa alla riserva quando i crediti finiscono.

    `apri(chiave)` fa la POST e ritorna il task id. Ritorna `(task id, chiave usata)`: il polling **deve**
    usare quella chiave, perché il task vive nell'account a cui appartiene. Chi chiama non la stampa.
    """
    elenco = chiavi() if elenco is None else elenco
    if not elenco:
        raise FornitoreNonConfigurato("manca MESHY_API_KEY (vedi `broll chiavi`)")
    ultima: CreditiEsauriti | None = None
    for i, k in enumerate(elenco):
        try:
            return apri(k), k
        except CreditiEsauriti as e:
            ultima = e
            if i + 1 < len(elenco):
                print(f"    ⚠ meshy: crediti esauriti sulla chiave #{i + 1}, provo la riserva…",
                      file=sys.stderr)
    raise ultima or FornitoreNonConfigurato("nessuna chiave Meshy con crediti")


# --- cache ----------------------------------------------------------------------------------------

def impronta(prompt: str) -> str:
    return hashlib.sha1(prompt.strip().encode("utf-8")).hexdigest()


def file_cache(prompt: str, n: int = 1, cache: Path = CACHE) -> Path:
    """`meshy-<sha1 del prompt>-<n>.png`: lo stesso prompt allo stesso indice dà sempre lo stesso file."""
    return cache / f"{NOME}-{impronta(prompt)}-{n}.png"


def scarica(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=SCADENZA_S) as r:
            r.raise_for_status()
            tmp = dest.with_suffix(dest.suffix + ".tmp")
            with tmp.open("wb") as f:
                for pezzo in r.iter_content(chunk_size=1 << 16):
                    f.write(pezzo)
            tmp.replace(dest)
    except requests.RequestException as e:
        raise RichiestaFallita(f"meshy: scaricamento dell'immagine fallito: {e}") from e
    return dest


# --- generazione ----------------------------------------------------------------------------------

def genera(prompt: str, n: int = 1, *, cache: Path = CACHE, forza: bool = False,
           modello: str = MODELLO, proporzioni: str = PROPORZIONI) -> tuple[Path, dict]:
    """Un'immagine per quel prompt, dalla cache o generata adesso.

    Ritorna `(file, scheda)`: la scheda è quello che finisce nel piano e in `CREDITI.md` — prompt,
    modello, data, e `da_cache` per sapere se questa chiamata è costata.
    """
    dest = file_cache(prompt, n, cache)
    sidecar = dest.with_suffix(".json")
    if dest.exists() and not forza:
        scheda = {}
        if sidecar.exists():
            try:
                scheda = json.loads(sidecar.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                scheda = {}
        return dest, {**_scheda(prompt, n, modello, scheda.get("task", ""), scheda.get("quando", "")),
                      "da_cache": True}

    task_id, usata = con_failover(lambda k: avvia(prompt, k, modello=modello, proporzioni=proporzioni))
    task = attendi(task_id, usata)
    scarica(url_immagine(task), dest)
    scheda = _scheda(prompt, n, modello, task_id, time.strftime("%Y-%m-%d"))
    sidecar.write_text(json.dumps(scheda, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest, {**scheda, "da_cache": False}


def _scheda(prompt: str, n: int, modello: str, task: str, quando: str) -> dict:
    """Quello che finisce nel piano (e da lì in `CREDITI.md`): nessun autore, ma il prompt, che è
    l'unica cosa che rende rifacibile un'immagine che in git non c'è."""
    return {"fornitore": NOME, "generata": True, "prompt": prompt, "indice": n, "modello": modello,
            "task": task, "quando": quando, "licenza": LICENZA,
            "file": None, "candidato": f"{NOME}:{impronta(prompt)[:10]}-{n}"}
