"""Il copione: il parlato del reel scritto da un modello esterno, prima della sceneggiatura (`uv run reel copione`).

Dal 2026-09-23 la VOCE non la scrive più lo sceneggiatore: nella prova alla cieca sul reel GPU il presentatore ha messo
gpt-5.4 davanti a deepseek-v4-pro, gemini-3.1-pro e Claude. Il comando legge dall'idea tema, messaggio e
`## Tappe del parlato`, compone il prompt da `templates/copione.md` con sei trascrizioni di reelkit per l'orecchio, e lo
manda al primo modello della catena (`config.toml [copione] modelli`); si scende al successivo solo se il precedente
fallisce: errore, punti Poe che non bastano, cifre o un reel oltre i 120 s anche dopo una correzione (le lunghezze
oltre i limiti, come in `valida`, restano avvisi). Lo sceneggiatore poi spezza
il copione in beat e ci costruisce attorno le animazioni.

La logica è pura; le chiamate stanno in `Poe` e `chiama_claude`, che i test sostituiscono.
"""
from __future__ import annotations

import hashlib
import os
import re
import tempfile
from pathlib import Path
from typing import Callable, NamedTuple

import yaml

from .model import conta_parole
from .validate import LIMITI, due_punti_snodo, frasi_di, frasi_titolo, schema_si_no

RADICE = Path(__file__).resolve().parents[2]
CARTELLA = RADICE / "contenuti" / "copioni"
TEMPLATE = RADICE / "templates" / "copione.md"
POE = "https://api.poe.com"
CLAUDE = "claude"               # l'anello della catena che non passa da Poe: `claude -p`, modello `opus`
TIMEOUT_S = 600.0
USD_PER_PUNTO = 0.30 / 10_000   # ricarica giornaliera di Poe: 10.000 punti ≈ 0,30 $ (letto il 2026-09-23)
CARATTERI_PER_TOKEN = 3.2       # italiano, stima prudente: serve solo a decidere se i punti bastano


class ErroreCopione(RuntimeError):
    pass


class ErroreChiamata(RuntimeError):
    """Un anello della catena che non risponde (rete, 402, 5xx, risposta vuota): si passa al successivo."""


class Tappa(NamedTuple):
    n: int
    testo: str      # la riga intera dell'idea, con il registro fra parentesi


class Idea(NamedTuple):
    tema: str
    messaggio: str
    tappe: list[Tappa]


class Esame(NamedTuple):
    errori: list[str]        # il copione non si usa: si passa al modello dopo
    correggibili: list[str]  # lunghezze e cifre: una correzione allo stesso modello
    avvisi: list[str]        # stile: vanno nel file, non fanno cambiare modello
    duri: list[str] = []     # i correggibili che restano un motivo di scarto anche dopo la correzione


class Esito(NamedTuple):
    modello: str
    scene: dict[int, str]
    esame: Esame
    tentativi: list[str]     # una riga per anello: «gpt-5.4: accorciato (310 → 241 parole)», «deepseek…: saltato (…)»


# --- l'idea ------------------------------------------------------------------------------------------------

def _sezione(testo: str, titolo: str) -> str | None:
    m = re.search(rf"^## {re.escape(titolo)}\s*$", testo, re.M)
    if not m:
        return None
    fine = re.search(r"^## ", testo[m.end():], re.M)
    return (testo[m.end():m.end() + fine.start()] if fine else testo[m.end():]).strip()


def leggi_idea(testo: str) -> Idea:
    """Tema (il titolo `# …`), `## Messaggio centrale` e `## Tappe del parlato`: una riga numerata per scena
    (`N. (apertura | filmato: … | animazione | chiusura) i fatti`), anche su più righe."""
    tema = re.search(r"^# (.+)$", testo, re.M)
    messaggio = _sezione(testo, "Messaggio centrale")
    blocco = _sezione(testo, "Tappe del parlato")
    if blocco is None:
        raise ErroreCopione("l'idea non ha «## Tappe del parlato»: la scrive l'ideatore, una riga numerata per scena")
    tappe: list[Tappa] = []
    for riga in blocco.splitlines():
        m = re.match(r"^(\d+)\.\s+(.+)$", riga.strip())
        if m:
            tappe.append(Tappa(int(m.group(1)), m.group(2).strip()))
        elif tappe and riga.strip() and not riga.lstrip().startswith(("<!--", "#")):
            tappe[-1] = tappe[-1]._replace(testo=f"{tappe[-1].testo} {riga.strip()}")
    if not tappe:
        raise ErroreCopione("«## Tappe del parlato» non ha righe «N. (registro) fatti»")
    if [t.n for t in tappe] != list(range(1, len(tappe) + 1)):
        raise ErroreCopione(f"tappe numerate male: {' '.join(str(t.n) for t in tappe)} (attese 1, 2, 3…)")
    n_min, n_max = LIMITI["scene_min"], LIMITI["scene_max"]
    if not n_min <= len(tappe) <= n_max:
        raise ErroreCopione(f"{len(tappe)} tappe: il reel ne vuole {n_min}-{n_max}")
    if not messaggio:
        raise ErroreCopione("l'idea non ha «## Messaggio centrale»")
    return Idea(tema.group(1).strip() if tema else "", " ".join(messaggio.split()), tappe)


def riga_copione(testo_idea: str, percorso: str) -> str:
    """L'idea con `**Copione:** <percorso>` sotto `**Stato:**` (aggiornata se c'è già) e lo stato `idea` → `copione`."""
    riga = f"**Copione:** {percorso}"
    if re.search(r"^\*\*Copione:\*\*.*$", testo_idea, re.M):
        testo_idea = re.sub(r"^\*\*Copione:\*\*.*$", lambda _: riga, testo_idea, count=1, flags=re.M)
    elif re.search(r"^\*\*Stato:\*\*.*$", testo_idea, re.M):
        testo_idea = re.sub(r"^(\*\*Stato:\*\*.*)$", lambda m: f"{m.group(1)}\n{riga}", testo_idea, count=1, flags=re.M)
    else:
        raise ErroreCopione("l'idea non ha la riga «**Stato:**» sotto cui scrivere «**Copione:**»")
    return re.sub(r"^\*\*Stato:\*\*\s*idea\s*$", "**Stato:** copione", testo_idea, count=1, flags=re.M)


# --- il prompt ---------------------------------------------------------------------------------------------

def scegli_trascrizioni(voci: list[dict], seme: str, quante: int = 6, secondi: float = 85) -> list[dict]:
    """Sei reel di durata vicina alla nostra, uno per account finché ce ne sono (così il passo non è di uno solo),
    sempre gli stessi per lo stesso reel. Fuori quelli troppo corti o lenti: sono musica con due parole sopra."""
    buone = [v for v in voci if 45 <= v["durata_s"] <= 160 and (v.get("parole_al_s") or 0) >= 2]
    chiave = lambda v: (abs(v["durata_s"] - secondi) // 15, hashlib.sha1(f"{seme}:{v['id']}".encode()).hexdigest())
    buone.sort(key=chiave)
    scelte, account = [], set()
    for v in buone:
        if len(scelte) < quante and v["account"] not in account:
            scelte.append(v)
            account.add(v["account"])
    for v in buone:
        if len(scelte) < quante and v not in scelte:
            scelte.append(v)
    return scelte


def secondi_per(parole: int, parole_al_s: float = 2.8) -> int:
    return int(round(parole / parole_al_s / 5) * 5)


def componi_prompt(template: str, idea: Idea, trascrizioni: list[tuple[str, str]], parole: int, nota: str = "",
                   parole_al_s: float = 2.8) -> str:
    corpo = re.sub(r"^<!--.*?-->\s*", "", template, flags=re.S)
    valori = {
        "trascrizioni": "\n\n".join(f"--- trascrizione {i} ---\n{t.strip()}" for i, t in trascrizioni),
        "secondi": str(secondi_per(parole, parole_al_s)),
        "scene": str(len(idea.tappe)),
        "parole": str(parole),
        "tema": idea.tema,
        "messaggio": idea.messaggio,
        "tappe": "\n".join(f"{t.n}. {t.testo}" for t in idea.tappe),
        "hook_max": str(LIMITI["parole_voce_hook_max"]),
        "chiusura_max": str(LIMITI["parole_voce_chiusura_max"]),
        "scena_max": str(LIMITI["parole_voce_max"]),
        "nota": f"\nRichiesta del presentatore per questa versione: {' '.join(nota.split())}\n" if nota.strip() else "",
    }
    out = re.sub(r"\{\{(\w+)\}\}", lambda m: valori[m.group(1)], corpo)
    return out.strip() + "\n"


def prompt_correzione(scene: dict[int, str], problemi: list[str], parole: int) -> str:
    """La seconda chiamata allo stesso modello: il suo testo e cosa sistemare, senza trascrizioni (costa poco)."""
    testo = "\n".join(f"## Scena {n}\n{t}" for n, t in sorted(scene.items()))
    return ("Questo è il parlato di un reel che hai scritto tu. Va sistemato così, senza cambiare il tono, "
            "tenendo le frasi che funzionano e senza aggiungere fatti:\n"
            + "\n".join(f"- {p}" for p in problemi)
            + f"\n- In tutto al massimo {parole} parole; i numeri in lettere come si dicono.\n\n"
            + testo + "\n\nRispondi solo con il testo corretto, nello stesso formato (## Scena N).\n")


# --- l'uscita ----------------------------------------------------------------------------------------------

def leggi_uscita(testo: str) -> dict[int, str]:
    """`## Scena N` → il parlato, su una riga. Si ignora quello che c'è prima (qualche modello saluta)."""
    parti = re.split(r"^\s*#{1,3}\s*Scena\s+(\d+)\b[^\n]*$", testo, flags=re.M | re.I)
    scene: dict[int, str] = {}
    for i in range(1, len(parti), 2):
        corpo = re.sub(r"^\s*(<parlato>|</parlato>)\s*$", "", parti[i + 1], flags=re.M)
        corpo = " ".join(corpo.replace("**", "").split())
        scene[int(parti[i])] = corpo.strip("\"“” ")
    return scene


def parole_totali(scene: dict[int, str]) -> int:
    return sum(conta_parole(t) for t in scene.values())


def esamina(scene: dict[int, str], n_tappe: int, parole: int, tetto: int | None = None) -> Esame:
    """Come `valida`: i limiti di parole sono una richiesta (una correzione, poi avvisi), mentre le cifre e un reel
    oltre `tetto` parole (l'errore di `valida`, 120 s) scartano il copione. Nella prova gpt-5.4 era il preferito anche
    a 310 parole: una regola più severa di `valida` lo scartava (2026-09-23)."""
    errori, corr, avvisi, duri = [], [], [], []
    if sorted(scene) != list(range(1, n_tappe + 1)):
        errori.append(f"scene {', '.join(map(str, sorted(scene))) or 'nessuna'} invece di 1-{n_tappe}")
        return Esame(errori, corr, avvisi)
    vuote = [n for n, t in scene.items() if not t]
    if vuote:
        errori.append(f"scene vuote: {', '.join(map(str, vuote))}")
    for n, t in sorted(scene.items()):
        k = conta_parole(t)
        massimo, nome = ((LIMITI["parole_voce_hook_max"], "apertura") if n == 1 else
                         (LIMITI["parole_voce_chiusura_max"], "chiusura") if n == n_tappe else
                         (LIMITI["parole_voce_max"], f"scena {n}"))
        if k > massimo:
            corr.append(f"la {nome} ha {k} parole: al massimo {massimo}")
        if re.search(r"\d", t):
            cifre = ", ".join(sorted(set(re.findall(r"\d[\d.,]*", t))))
            duri.append(f"scena {n}: numeri in cifre ({cifre}): vanno scritti in lettere come si dicono")
    tot = parole_totali(scene)
    if tetto is not None and tot > tetto:
        duri.append(f"in tutto {tot} parole: oltre {tetto} il reel supera il limite di `valida`")
    elif tot > parole * 1.1:
        corr.append(f"in tutto {tot} parole: al massimo {parole}")
    corr += duri
    frasi = [f for n, t in sorted(scene.items()) if n != n_tappe for f in frasi_di([t])]
    titoli = frasi_titolo(frasi)
    if len(titoli) > LIMITI["frasi_titolo_reel_max"]:
        avvisi.append(f"{len(titoli)} frasi da titolo fuori dalla chiusura: {' / '.join(titoli)}")
    for n, t in sorted(scene.items()):
        if any(schema_si_no(f) for f in frasi_di([t])):
            avvisi.append(f"scena {n}: schema «X, sì. Y, no.»")
        if due_punti_snodo(t):
            avvisi.append(f"scena {n}: due punti come snodo")
    return Esame(errori, corr, avvisi, duri)


# --- la catena ---------------------------------------------------------------------------------------------

def catena(prompt: str, modelli: list[str], n_tappe: int, parole: int,
           chiama: Callable[[str, str], str], salta: Callable[[str, str], str | None] = lambda m, p: None,
           avanzamento: Callable[[str], None] | None = None, tetto: int | None = None) -> Esito:
    """Il primo modello che consegna un copione senza errori. `salta(modello, prompt)` dice perché non chiamarlo
    (punti che non bastano); `chiama(modello, prompt)` risponde o solleva ErroreChiamata. Un copione solo lungo o con
    cifre riceve **una** correzione dallo stesso modello: nella prova gpt-5.4 era il preferito, ma a 310 parole."""
    tentativi: list[str] = []
    dillo = avanzamento or (lambda s: None)
    for m in modelli:
        perche = salta(m, prompt)
        if perche:
            tentativi.append(f"{m}: saltato ({perche})")
            dillo(tentativi[-1])
            continue
        try:
            scene = leggi_uscita(chiama(m, prompt))
            esame = esamina(scene, n_tappe, parole, tetto)
            nota = "ok"
            if not esame.errori and esame.correggibili:
                prima = parole_totali(scene)
                dillo(f"{m}: da sistemare ({'; '.join(esame.correggibili)}), una correzione")
                p2 = prompt_correzione(scene, esame.correggibili, parole)
                perche = salta(m, p2)
                if perche:
                    raise ErroreChiamata(f"correzione saltata ({perche})")
                corrette = leggi_uscita(chiama(m, p2))
                esame = esamina(corrette, n_tappe, parole, tetto)
                scene, nota = corrette, f"corretto ({prima} → {parole_totali(corrette)} parole)"
        except ErroreChiamata as e:
            tentativi.append(f"{m}: fallito ({e})")
            dillo(tentativi[-1])
            continue
        if esame.errori or esame.duri:
            tentativi.append(f"{m}: scartato ({'; '.join(esame.errori + esame.duri)})")
            dillo(tentativi[-1])
            continue
        if esame.correggibili:      # lunghezze rimaste dopo la correzione: come in `valida`, avvisi
            esame = Esame([], [], esame.correggibili + esame.avvisi)
        tentativi.append(f"{m}: {nota}")
        dillo(tentativi[-1])
        return Esito(m, scene, esame, tentativi)
    raise ErroreCopione("nessun modello della catena ha consegnato un copione:\n   " + "\n   ".join(tentativi))


# --- il file -----------------------------------------------------------------------------------------------

def componi_file(idea_rel: str, idea: Idea, esito: Esito, data: str, punti: int | None, nota: str = "") -> str:
    testa = {"idea": idea_rel, "modello": esito.modello, "data": data, "parole": parole_totali(esito.scene),
             "punti_poe": punti, "catena": esito.tentativi}
    if nota.strip():
        testa["nota"] = " ".join(nota.split())
    if esito.esame.avvisi:
        testa["avvisi"] = esito.esame.avvisi
    corpo = "\n\n".join(f"## Scena {n}\n{t}" for n, t in sorted(esito.scene.items()))
    return (f"---\n{yaml.safe_dump(testa, allow_unicode=True, sort_keys=False, width=1000)}---\n\n"
            f"# Copione · {idea.tema}\n\n"
            "<!-- Il parlato del reel, scritto dal modello indicato sopra. Lo sceneggiatore lo prende alla lettera e lo\n"
            "spezza in righe VOCE; si corregge qui a mano, o si rigenera con `uv run reel copione <idea> --nota \"…\"`. -->\n\n"
            f"{corpo}\n")


def leggi_copione(testo: str) -> dict[int, str]:
    """Le scene di un file copione (per lo sceneggiatore e per i test)."""
    return leggi_uscita(re.sub(r"^---\n.*?\n---\n", "", testo, count=1, flags=re.S))


# --- chiamate ----------------------------------------------------------------------------------------------

def chiave_poe() -> str | None:
    """`POE_API_KEY` dall'ambiente, poi da `.env` nella radice (gitignored), una riga `NOME=valore`."""
    if os.environ.get("POE_API_KEY"):
        return os.environ["POE_API_KEY"]
    env = RADICE / ".env"
    if env.is_file():
        for riga in env.read_text(encoding="utf-8").splitlines():
            nome, _, valore = riga.strip().removeprefix("export ").partition("=")
            if nome.strip() == "POE_API_KEY" and valore.strip():
                return valore.strip().strip("\"'")
    return None


class Poe:
    """L'API di Poe, compatibile OpenAI: saldo, prezzi, una chiamata."""

    def __init__(self, chiave: str, token_uscita: int = 6000, punti_minimi: int = 1500):
        import requests
        self._s = requests.Session()
        self._s.headers["Authorization"] = f"Bearer {chiave}"
        self.token_uscita, self.punti_minimi = token_uscita, punti_minimi
        self._prezzi: dict[str, dict] | None = None

    def saldo(self) -> int:
        r = self._s.get(f"{POE}/usage/current_balance", timeout=30)
        r.raise_for_status()
        return int(r.json()["current_point_balance"])

    def prezzi(self) -> dict[str, dict]:
        if self._prezzi is None:
            r = self._s.get(f"{POE}/v1/models", timeout=30)
            r.raise_for_status()
            self._prezzi = {m["id"]: (m.get("pricing") or {}) for m in r.json().get("data", [])}
        return self._prezzi

    def stima_punti(self, modello: str, prompt: str) -> int | None:
        """Il costo massimo di una chiamata, in punti; None se Poe non dà il prezzo (alcuni modelli rispondono
        senza essere in elenco)."""
        p = self.prezzi().get(modello)
        if not p:
            return None
        if p.get("request"):
            usd = float(p["request"])
        else:
            usd = (len(prompt) / CARATTERI_PER_TOKEN * float(p.get("prompt") or 0)
                   + self.token_uscita * float(p.get("completion") or 0))
        return int(usd / USD_PER_PUNTO) + 1

    def salta(self, modello: str, prompt: str) -> str | None:
        try:
            saldo = self.saldo()
            stima = self.stima_punti(modello, prompt)
        except Exception as e:  # rete, JSON: senza saldo non si rischia la chiamata
            return f"saldo non leggibile: {e}"
        if saldo < self.punti_minimi:
            return f"saldo {saldo} punti, sotto i {self.punti_minimi} minimi"
        if stima is not None and stima > saldo:
            return f"stima {stima} punti, saldo {saldo}"
        return None

    def chiama(self, modello: str, prompt: str) -> str:
        import requests
        try:
            r = self._s.post(f"{POE}/v1/chat/completions", timeout=TIMEOUT_S,
                             json={"model": modello, "messages": [{"role": "user", "content": prompt}]})
        except requests.RequestException as e:
            raise ErroreChiamata(str(e)) from e
        if r.status_code != 200:
            raise ErroreChiamata(f"HTTP {r.status_code}: {r.text[:200]}")
        try:
            testo = r.json()["choices"][0]["message"]["content"]
        except (ValueError, KeyError, IndexError, TypeError) as e:
            raise ErroreChiamata(f"risposta senza testo: {r.text[:200]}") from e
        if not str(testo or "").strip():
            raise ErroreChiamata("risposta vuota")
        return str(testo)


def chiama_claude(prompt: str, modello: str = "opus", timeout_s: float = TIMEOUT_S) -> str:
    """L'ultimo anello: `claude -p` da una cartella vuota, come le uscite della tappa T0b."""
    from . import uscite
    cmd = uscite.comando(uscite.Richiesta("-", "copione", prompt), modello)
    try:
        with tempfile.TemporaryDirectory(prefix="copione-") as tmp:
            return uscite.estrai_result(uscite.lancia(cmd, Path(tmp), timeout_s))
    except uscite.ErroreUscite as e:
        raise ErroreChiamata(str(e)) from e
