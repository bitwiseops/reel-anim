"""Tappa T0b: le uscite vere dei testi che il reel attribuisce a un modello (`claude -p`, più modelli, più uscite l'uno).

Dall'idea si leggono le richieste («Testi del modello: richieste da generare»), si lanciano da una cartella vuota, si
tolgono i dati dell'account che la CLI passa al modello e si scrive `contenuti/idee/uscite/<slug>-<data>.md`, il file
che sceneggiatore e revisore leggono. La logica è pura; i processi stanno in `lancia`, `versione_claude`, `account_git`.
"""
from __future__ import annotations

import json
import re
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Callable, NamedTuple

from ..anim.config import Config
from .parser import riga_sotto_stato, sezione

from ..anim.config import RADICE
CARTELLA = RADICE / "contenuti" / "idee" / "uscite"
PROMPT_DI_SISTEMA = "Sei un assistente che scrive testi su richiesta."
IN_PARALLELO = 6
TIMEOUT_S = 300.0
NOME_FINTO, EMAIL_FINTA = "Nome Cognome", "nome.cognome@email.it"


class ErroreUscite(RuntimeError):
    pass


class Richiesta(NamedTuple):
    sigla: str      # A, B, C…
    nome: str       # «base («migliora»)»
    testo: str      # il testo esatto passato a `claude -p`


class Uscita(NamedTuple):
    sigla: str      # A1…A10: prima i modelli nell'ordine dato, `per_modello` uscite l'uno
    modello: str
    testo: str


# --- richieste dell'idea -----------------------------------------------------------------------------

_INTESTAZIONE = re.compile(r"\*\*Testi del modello: richieste da generare")
_RICHIESTA = re.compile(r"^- \*\*([A-Z]) · (.+?):\*\*\s*(`+)(.+?)\3", re.M | re.S)


def richieste(testo_idea: str) -> list[Richiesta]:
    """Le richieste da generare: in `## Note per il reel`, dopo «Testi del modello: richieste da generare», i bullet
    ``- **A · nome:** `testo esatto` ``. Un a capo dentro i backtick è l'a capo del markdown, cioè uno spazio."""
    note = sezione(testo_idea, "Note per il reel") or ""
    m = _INTESTAZIONE.search(note)
    if not m:
        raise ErroreUscite("l'idea non elenca richieste: manca «**Testi del modello: richieste da generare**» nelle Note per il reel")
    blocco = note[m.end():]
    out = [Richiesta(sigla, nome.strip(), re.sub(r"\s*\n\s*", " ", t).strip()) for sigla, nome, _, t in _RICHIESTA.findall(blocco)]
    if not out:
        raise ErroreUscite("nessuna richiesta nella forma «- **A · nome:** `testo`» dopo «Testi del modello: richieste da generare»")
    lettere = [r.sigla for r in out]
    if lettere != [chr(ord("A") + k) for k in range(len(out))]:
        raise ErroreUscite(f"sigle delle richieste fuori ordine o ripetute: {' '.join(lettere)} (attese A, B, C…)")
    return out


def slug_e_data(idea: Path) -> tuple[str, str | None]:
    """`2026-09-19-scrivere-con-ia.md` → («scrivere-con-ia», «2026-09-19»): lo slug è il nome del file senza la data."""
    m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)$", idea.stem)
    return (m.group(2), m.group(1)) if m else (idea.stem, None)


def sigle(richiesta: Richiesta, modelli: list[str], per_modello: int) -> list[tuple[str, str]]:
    """(sigla, modello) delle uscite di una richiesta: A1-A5 col primo modello, A6-A10 col secondo."""
    return [(f"{richiesta.sigla}{k * per_modello + i + 1}", m) for k, m in enumerate(modelli) for i in range(per_modello)]


# --- claude -p -------------------------------------------------------------------------------------------

def comando(richiesta: Richiesta, modello: str) -> list[str]:
    return ["claude", "-p", richiesta.testo, "--model", modello, "--system-prompt", PROMPT_DI_SISTEMA, "--tools", "",
            "--no-session-persistence", "--output-format", "json"]


def estrai_result(stdout: str) -> str:
    """Il testo dell'evento `type == "result"`: l'output JSON è quell'oggetto, o la lista di tutti gli eventi."""
    try:
        j = json.loads(stdout)
    except ValueError as e:
        raise ErroreUscite(f"l'output di claude -p non è JSON: {stdout.strip()[:200]!r}") from e
    eventi = j if isinstance(j, list) else [j]
    r = next((e for e in reversed(eventi) if isinstance(e, dict) and e.get("type") == "result"), None)
    if r is None:
        raise ErroreUscite("nell'output di claude -p manca l'evento «result»")
    if r.get("is_error") or not str(r.get("result") or "").strip():
        raise ErroreUscite(f"claude -p ha risposto con un errore o a vuoto: {str(r.get('result') or r.get('subtype'))[:200]}")
    return str(r["result"]).strip()


def lancia(cmd: list[str], cwd: Path, timeout_s: float = TIMEOUT_S) -> str:
    """Un `claude -p` da una cartella neutra; ritorna lo stdout. I test la sostituiscono."""
    try:
        r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout_s)
    except FileNotFoundError as e:
        raise ErroreUscite("`claude` non è nel PATH") from e
    except subprocess.TimeoutExpired as e:
        raise ErroreUscite(f"claude -p oltre {timeout_s:.0f} s") from e
    if r.returncode != 0:
        raise ErroreUscite(f"claude -p ha fallito ({r.returncode}): {(r.stderr or r.stdout).strip()[-400:]}")
    return r.stdout


def genera(rr: list[Richiesta], modelli: list[str], per_modello: int = 5, timeout_s: float = TIMEOUT_S,
           avanzamento: Callable[[str, int, int], None] | None = None) -> list[Uscita]:
    """Tutte le uscite, IN_PARALLELO alla volta, nell'ordine delle sigle. Al primo fallimento si annulla ciò che non
    è partito e si solleva ErroreUscite: senza tutte le uscite vere il file non si scrive."""
    lavori = [(r, s, m) for r in rr for s, m in sigle(r, modelli, per_modello)]
    with tempfile.TemporaryDirectory(prefix="uscite-") as tmp:      # vuota: il modello non deve leggere CLAUDE.md
        ex = ThreadPoolExecutor(max_workers=IN_PARALLELO)
        futuri = {ex.submit(lambda r=r, m=m: estrai_result(lancia(comando(r, m), Path(tmp), timeout_s))): k
                  for k, (r, _, m) in enumerate(lavori)}
        testi: dict[int, str] = {}
        try:
            for f in as_completed(futuri):
                _, s, m = lavori[futuri[f]]
                try:
                    testi[futuri[f]] = f.result()
                except ErroreUscite as e:
                    raise ErroreUscite(f"{s} ({m}): {e}") from e
                if avanzamento:
                    avanzamento(s, len(testi), len(lavori))
        finally:
            ex.shutdown(wait=True, cancel_futures=True)
    return [Uscita(s, m, testi[k]) for k, (_, s, m) in enumerate(lavori)]


def versione_claude() -> str:
    try:
        return subprocess.run(["claude", "--version"], capture_output=True, text=True, timeout=30).stdout.strip() or "versione ignota"
    except (OSError, subprocess.TimeoutExpired):
        return "versione ignota"


# --- anonimizzazione ---------------------------------------------------------------------------------------

def account_git() -> tuple[str, str]:
    """Nome ed email dell'account come li conosce git: sono gli stessi che `claude -p` passa al modello."""
    def leggi(chiave: str) -> str:
        try:
            return subprocess.run(["git", "config", chiave], cwd=RADICE, capture_output=True, text=True, timeout=10).stdout.strip()
        except (OSError, subprocess.TimeoutExpired):
            return ""
    return leggi("user.name"), leggi("user.email")


def termini_account(nome: str, email: str, cfg: Config | None = None) -> list[tuple[str, str]]:
    """Coppie (vero, finto) nell'ordine in cui si applicano: l'email intera prima del nome che contiene, il nome completo
    prima di nome e cognome da soli; in coda i termini di `[uscite] anonimizza` (config.local.toml: dominio, città…)."""
    out = [(email, EMAIL_FINTA)] if email else []
    if nome:
        out.append((nome, NOME_FINTO))
        parole = nome.split()
        if len(parole) == 2:
            out += list(zip(parole, NOME_FINTO.split()))
    extra = cfg.dati.get("uscite", {}).get("anonimizza", []) if cfg else []
    return out + [(str(vero), str(finto)) for vero, finto in extra]


def anonimizza(testo: str, termini: list[tuple[str, str]]) -> tuple[str, int]:
    """Sostituisce ogni termine vero col suo finto: a parola intera, senza distinzione di maiuscole. Ritorna il testo e
    quante sostituzioni ha fatto."""
    n = 0
    for vero, finto in termini:
        if not vero.strip():
            continue
        testo, k = re.subn(rf"(?<!\w){re.escape(vero)}(?!\w)", lambda _: finto, testo, flags=re.I)
        n += k
    return testo, n


# i capoluoghi più grandi: un'inferenza sulla città dell'account viene dall'indirizzo o dai connettori, non dalla richiesta
_CITTA = ("Roma", "Milano", "Napoli", "Torino", "Palermo", "Genova", "Bologna", "Firenze", "Bari", "Catania", "Venezia",
          "Verona", "Messina", "Padova", "Trieste", "Brescia", "Parma", "Taranto", "Prato", "Modena", "Reggio Calabria",
          "Reggio Emilia", "Perugia", "Livorno", "Ravenna", "Cagliari", "Foggia", "Rimini", "Salerno", "Ferrara", "Sassari",
          "Latina", "Monza", "Siracusa", "Pescara", "Bergamo", "Trento", "Vicenza", "Bolzano", "Ancona", "Pisa", "Lecce", "Udine")
_SPIE = [(re.compile(rf"(?<!\w){p}(?!\w)"), None) for p in ("Drive", "Gmail", "Google", *_CITTA)] + \
        [(re.compile(r"(?<!\w)(universit\w+|ateneo)(?!\w)", re.I), "università")]


def segnalazioni(testo: str, richiesta: str = "") -> list[str]:
    """Le spie dell'artefatto dei connettori e delle inferenze personali («Drive», «Gmail», «Google», una città,
    l'università): non si sostituiscono, si ricontrollano a mano. Ciò che nomina già la richiesta non è una spia."""
    out = []
    for rx, etichetta in _SPIE:
        m = rx.search(testo)
        if m and not rx.search(richiesta) and (etichetta or m.group(0)) not in out:
            out.append(etichetta or m.group(0))
    return out


# --- file delle uscite e riga nell'idea ------------------------------------------------------------------

def _etichetta(modello: str) -> str:
    return modello[:1].upper() + modello[1:]


def componi(slug: str, data: str, versione: str, rr: list[Richiesta], uscite: list[Uscita], modelli: list[str], per_modello: int,
            ritoccate: list[str], n_sostituzioni: int, segnalate: dict[str, list[str]]) -> str:
    """Il markdown di `contenuti/idee/uscite/<slug>-<data>.md`, nel formato che sceneggiatore e revisore già leggono."""
    fasce = ", ".join(f"{k * per_modello + 1}-{(k + 1) * per_modello} {_etichetta(m)}" for k, m in enumerate(modelli))
    if ritoccate:
        ritocco = (f"dove il modello li ha usati sono sostituiti da «{NOME_FINTO}» e «{EMAIL_FINTA}» ({len(ritoccate)} uscite su "
                   f"{len(uscite)}, {n_sostituzioni} sostituzioni: {' '.join(ritoccate)})")
    else:
        ritocco = f"qui non compaiono (0 uscite su {len(uscite)}, 0 sostituzioni)"
    if segnalate:
        spie = "da ricontrollare a mano, e da sostituire se è un'inferenza personale: " + \
               ", ".join(f"{s} ({', '.join(v)})" for s, v in segnalate.items())
    else:
        spie = "nessuna uscita nomina Drive, Gmail, Google, una città o l'università"
    testa = [
        f"# Uscite vere · {slug} · {data}", "",
        f"Generate il {data} dalla tappa T0b di `/pipeline` (`uv run reel uscite`) con `claude -p` ({versione}), da una cartella neutra:",
        f"`--model {'|'.join(modelli)} --system-prompt \"{PROMPT_DI_SISTEMA}\" --tools \"\" --no-session-persistence`.",
        f"Sigle: {fasce}. Testi riportati così come sono usciti, con un solo ritocco: `claude -p` passa al modello nome ed",
        f"email dell'account anche da una cartella neutra; {ritocco}.",
        "A schermo non vanno mai i dati veri.",
        "**Artefatto dei connettori:** `--tools \"\"` non spegne i connettori dell'account (Drive, Gmail) e il modello può inferire",
        f"città o ateneo dall'indirizzo; {spie}.",
        "La caption deve dire che lo strumento passava nome, email e connettori.", "",
    ]
    corpo = []
    for r in rr:
        corpo += [f"## {r.sigla} · {r.nome}", "", "**Richiesta:**", "", f"> {r.testo}", ""]
        for s, m in sigle(r, modelli, per_modello):
            u = next(u for u in uscite if u.sigla == s)
            corpo += [f"### {s} · {_etichetta(m)} ({m})", "", u.testo.strip(), ""]
    return "\n".join(testa + corpo)


def scrivi_file(dest: Path, slug: str, data: str, versione: str, rr: list[Richiesta], uscite: list[Uscita], modelli: list[str],
                per_modello: int, termini_veri: list[tuple[str, str]], forza: bool = False) -> dict:
    """Anonimizza, segnala e scrive il file; non sovrascrive senza `forza`. Ritorna i conti da mostrare a video."""
    if dest.exists() and not forza:
        raise ErroreUscite(f"{dest} esiste già: le uscite vere non si rigenerano per caso (--forza per sovrascrivere)")
    per_sigla = {s: r for r in rr for s, _ in sigle(r, modelli, per_modello)}
    pulite, ritoccate, n_sostituzioni, segnalate = [], [], 0, {}
    for u in uscite:
        testo, n = anonimizza(u.testo, termini_veri)
        if n:
            ritoccate.append(u.sigla)
            n_sostituzioni += n
        spie = segnalazioni(testo, per_sigla[u.sigla].testo)
        if spie:
            segnalate[u.sigla] = spie
        pulite.append(u._replace(testo=testo))
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(componi(slug, data, versione, rr, pulite, modelli, per_modello, ritoccate, n_sostituzioni, segnalate),
                    encoding="utf-8")
    return {"file": dest, "uscite": len(uscite), "ritoccate": ritoccate, "sostituzioni": n_sostituzioni, "segnalate": segnalate}


def riga_uscite(testo_idea: str, percorso: str) -> str:
    """L'idea con `**Uscite:** <percorso>` sotto `**Stato:**` (aggiornata, non duplicata)."""
    return riga_sotto_stato(testo_idea, "Uscite", percorso, ErroreUscite)
