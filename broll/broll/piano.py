"""Il piano visivo di un reel: per ogni scena, materiale esterno o animazione, e con quale filmato.

Il piano è l'unico stato durevole del sottosistema. Sta in `contenuti/broll/<slug>/piano.json` e va in
git: è la decisione, non il pixel. I byte dei filmati no (vivono sotto `contenuti/media/`, ignorata),
perché il piano porta url e sha256 e si riscaricano.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from tools.anim.config import Config, carica
from tools.reel.model import Diagnostica, Scena, avviso
from tools.reel.parser import parse
from tools.reel.stima import durata_stimata_s

RADICE = Path(__file__).resolve().parents[2]
VERSIONE = 1

# Tre registri. L'animazione spiega, il filmato tiene l'attenzione; le immagini composte sono il
# ripiego quando per quella scena non esiste né una clip filmata né una animata: si montano sui beat,
# una per frase, per richiamare quello che il presentatore sta dicendo in quel momento.
REGISTRI = ("animazione", "filmato", "immagini")
STATI_SCENA = ("da-scegliere", "scelto", "reso")
# i tipi di scena che possono andare a filmato. La chiusura è la CTA, e una scena [schermo] ha già il suo
# materiale nella finestra 900x980. L'hook sì, ed è il primo candidato: i primi 5-10 secondi devono
# catturare l'attenzione, quindi il presentatore pone il problema nel riquadro e dietro c'è una clip che
# lo richiama; il TITOLO non va a schermo, vive in copertina (decisione di Flavio, 2026-09-19). Resta
# animato l'hook il cui brief parla del titolo: lì c'è una tipografia da disegnare, non un'immagine.
AMMESSE = ("hook", "spiegazione")

# Quello che si spiega disegnando: meccanismi, quantità, e le figure della libreria. Se una scena nomina
# una di queste cose, il filmato non la può raccontare e la scena resta animata.
# Un marcatore che finisce con "-" è un prefisso (probabil- → probabile, probabilità); gli altri sono
# parole intere. I confini di parola non sono un dettaglio: senza, «accento» (che i brief dicono a ogni
# riga) conteneva «cento» e «barrata» conteneva «barra», e ogni scena risultava tecnica.
TECNICI = (
    "flusso", "ciclo", "confronto", "tabella", "grafico", "barra", "barre", "classifica", "diagramma",
    "schema", "contatore", "corrispondenza", "graffa", "codice", "lista", "passo", "passi", "colonna",
    "percentual-", "probabil-", "token", "modello", "algoritmo", "parametr-", "funziona", "calcol-",
    "passaggio", "formula", "curva", "prompt", "dataset", "statistic-", "distribuzione",
)
# Nella VOCE i numeri si scrivono a lettere, perché è parlato: «su cento righe, novanta sono uguali».
# Le centinaia sono elencate invece che prese per prefisso, altrimenti «accento» rientra dalla finestra.
CENTINAIA = ("cento", "duecento", "trecento", "quattrocento", "cinquecento", "seicento", "settecento",
             "ottocento", "novecento")
NUMERI = CENTINAIA + ("mila", "milione", "milioni", "miliardo", "miliardi", "per cento", "percento",
                      "metà", "doppio", "triplo")
_COMPOSTI = (r"\b\w+mila\b",)          # diecimila, ventimila

# I brief sono pieni di tempi («entro 0,5 s», «~1 s, appena…»): sono regia, non quantità da mostrare.
RE_TEMPI = re.compile(r"\d+(?:[.,]\d+)?\s*(?:ms|s|secondi?)\b")


def _pattern(marcatori: tuple[str, ...]) -> list[str]:
    return [rf"\b{re.escape(m[:-1])}" if m.endswith("-") else rf"\b{re.escape(m)}\b" for m in marcatori]


RE_TECNICA = re.compile("|".join(_pattern(TECNICI) + _pattern(NUMERI) + list(_COMPOSTI)))


class PianoMancante(RuntimeError):
    pass


@dataclass
class ScenaBroll:
    n: int
    tipo: str
    durata_s: float
    origine_durata: str                 # "report" | "stima"
    inizi_frasi_s: list[float] = field(default_factory=list)
    origine_tempi: str = ""             # voce-sintetica | presa | parole-clip | stima
    registro: str = "animazione"        # animazione | filmato | immagini
    voce: list[str] = field(default_factory=list)
    brief: list[str] = field(default_factory=list)
    query: list[str] = field(default_factory=list)
    stato: str = "da-scegliere"
    candidati: list[dict] = field(default_factory=list)
    scelti: list[dict] = field(default_factory=list)
    file: str | None = None
    note: str = ""

    def to_dict(self) -> dict:
        return {"n": self.n, "tipo": self.tipo, "durata_s": self.durata_s, "origine_durata": self.origine_durata,
                "inizi_frasi_s": self.inizi_frasi_s, "origine_tempi": self.origine_tempi,
                "registro": self.registro, "voce": self.voce, "brief": self.brief, "query": self.query,
                "stato": self.stato, "candidati": self.candidati, "scelti": self.scelti, "file": self.file,
                "note": self.note}

    @classmethod
    def da_dict(cls, d: dict) -> ScenaBroll:
        noti = {c: d[c] for c in cls.__dataclass_fields__ if c in d}
        return cls(**noti)


@dataclass
class Piano:
    slug: str
    sorgente: str
    hash_md: str
    scene: list[ScenaBroll]
    quando: str = ""
    cornice: dict = field(default_factory=dict)
    versione: int = VERSIONE

    @property
    def filmati(self) -> list[ScenaBroll]:
        return [s for s in self.scene if s.registro == "filmato"]

    def scena(self, n: int) -> ScenaBroll | None:
        return next((s for s in self.scene if s.n == n), None)

    def to_dict(self) -> dict:
        return {"versione": self.versione, "slug": self.slug, "sorgente": self.sorgente, "hash_md": self.hash_md,
                "quando": self.quando, "cornice": self.cornice, "scene": [s.to_dict() for s in self.scene]}

    @classmethod
    def da_dict(cls, d: dict) -> Piano:
        return cls(slug=d["slug"], sorgente=d.get("sorgente", ""), hash_md=d.get("hash_md", ""),
                   scene=[ScenaBroll.da_dict(s) for s in d.get("scene", [])], quando=d.get("quando", ""),
                   cornice=d.get("cornice", {}), versione=d.get("versione", VERSIONE))


# --- percorsi -------------------------------------------------------------------------------------

def cartella(slug: str) -> Path:
    return RADICE / "contenuti" / "broll" / slug


def file_piano(slug: str) -> Path:
    return cartella(slug) / "piano.json"


def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(RADICE))
    except ValueError:
        return str(p)


def hash_sceneggiatura(md: Path) -> str:
    """Lo stesso calcolo di monta.py, così i due hash si confrontano."""
    return hashlib.sha256(md.read_bytes()).hexdigest()[:16]


# --- lettura e scrittura --------------------------------------------------------------------------

def carica_piano(slug: str) -> Piano:
    p = file_piano(slug)
    if not p.exists():
        raise PianoMancante(f"manca {p.relative_to(RADICE)}: prima `broll piano <sceneggiatura.md>`")
    return Piano.da_dict(json.loads(p.read_text(encoding="utf-8")))


def salva(p: Piano) -> Path:
    """Scrittura atomica, come fa il resto del repo."""
    dest = file_piano(p.slug)
    dest.parent.mkdir(parents=True, exist_ok=True)
    p.quando = datetime.now().isoformat(timespec="seconds")
    tmp = dest.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(p.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(dest)
    return dest


# --- durate ---------------------------------------------------------------------------------------

def _durate_dal_report(slug: str) -> dict[int, dict]:
    """Durate e **inizi delle frasi** dall'ultimo montaggio, se c'è: report.json o report-prova.json.

    Gli inizi frase servono al registro `immagini`: un'immagine per beat, così il montaggio segue quello
    che il presentatore sta dicendo. Sono esatti con la voce di prova e con le prese di `reel registra`.
    """
    out = RADICE / "contenuti" / "render" / slug
    for nome in ("report.json", "report-prova.json"):
        f = out / nome
        if not f.exists():
            continue
        try:
            dati = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        return {int(e["scena"]): {"durata_s": float(e["durata_s"]),
                                  "inizi_frasi_s": list(e.get("inizi_frasi_s") or []),
                                  "origine_tempi": e.get("origine_tempi") or ""}
                for e in dati.get("elementi", []) if e.get("scena")}
    return {}


# --- costruzione ----------------------------------------------------------------------------------

def _tecnica(s: Scena) -> bool:
    """La scena ha qualcosa da spiegare, cioè da disegnare?

    Il criterio del presentatore: **Manim spiega, la clip tiene l'attenzione**. Una scena che nomina un
    meccanismo, una quantità o una figura della libreria va animata; una che non ha niente da mostrare
    è una scena d'attenzione, e lì il filmato lavora meglio di una carta che scorre.
    """
    return bool(_marcatori(s))


def _marcatori(s: Scena) -> list[str]:
    """Cosa, nella scena, dice che c'è da disegnare. Vuoto = scena d'attenzione."""
    testo = " ".join(s.animazione + s.voce + s.testo).lower()
    trovati = sorted(set(RE_TECNICA.findall(testo)))
    if any(c.isdigit() for c in RE_TEMPI.sub(" ", testo)):
        trovati.append("una quantità")
    return trovati


RE_TIPOGRAFIA = re.compile(r"\b(sotto)?titolo\b")


def _hook_filmabile(s: Scena) -> bool:
    """Il brief dell'hook descrive un'immagine da cercare, o un titolo da animare?

    Senza brief non c'è niente da cercare; con un brief che parla del titolo c'è una tipografia da
    disegnare. In tutti e due i casi l'hook resta a Manim, che è la scelta sicura.
    """
    brief = " ".join(s.animazione).lower()
    return bool(brief) and not RE_TIPOGRAFIA.search(brief)


def _proponi(scene: list[Scena]) -> set[int]:
    """Quali scene proporre a filmato: quelle senza niente da spiegare, alternate, non più di metà.

    È l'euristica della M1 e serve a far partire il piano. Dalla M5 la proposta la fa l'agente, che legge
    la scena invece di cercarci dentro delle parole; questa resta il ripiego quando l'agente non c'è.
    """
    ammesse = [s.n for s in scene if s.tipo in AMMESSE and not _tecnica(s)
               and (s.tipo != "hook" or _hook_filmabile(s))]
    tetto = len(scene) // 2
    scelte: list[int] = []
    for n in ammesse:
        if len(scelte) >= tetto:
            break
        if scelte and n == scelte[-1] + 1:      # mai due scene di filmato attaccate
            continue
        scelte.append(n)
    return set(scelte)


def da_sceneggiatura(md: Path, cfg: Config | None = None) -> tuple[Piano, list[Diagnostica]]:
    """Legge la sceneggiatura e propone un piano. Non scrive niente: lo fa il chiamante con `salva`."""
    cfg = cfg or carica()
    from .query import query_scena

    r, diag = parse(md)
    durate = _durate_dal_report(r.slug)
    proposte = _proponi(r.scene)

    scene: list[ScenaBroll] = []
    for s in r.scene:
        d = durate.get(s.n)
        sb = ScenaBroll(n=s.n, tipo=s.tipo,
                        durata_s=round(d["durata_s"] if d else durata_stimata_s(s, cfg), 2),
                        origine_durata="report" if d else "stima",
                        inizi_frasi_s=d["inizi_frasi_s"] if d else [],
                        origine_tempi=d["origine_tempi"] if d else "",
                        voce=list(s.voce), brief=list(s.animazione))
        # una scena già [broll] nel .md è una decisione presa: si rispetta
        if s.tipo == "broll" or s.n in proposte:
            sb.registro = "filmato"
            sb.query = query_scena(s, cfg)
            sb.file = f"broll-scena-{s.n:02d}.mp4"
        elif s.tipo in AMMESSE:
            sb.note = "animata: " + ", ".join(_marcatori(s)) if _marcatori(s) else "animata: alternanza"
        scene.append(sb)

    sc = cfg.dati["schermo"]
    p = Piano(slug=r.slug, sorgente=_rel(md), hash_md=hash_sceneggiatura(md), scene=scene,
              cornice={"pieno": [cfg.larghezza, cfg.altezza],
                       "finestra": [int(sc["larghezza"]), int(sc["altezza"])]})
    return p, diag + controlla(p)


def eredita(nuovo: Piano, vecchio: Piano, fps: int = 30) -> list[int]:
    """Rifare il piano non deve disfare le decisioni: porta nel nuovo candidati e scelte del vecchio.

    Una scena eredita se è ancora a filmato e dice ancora le stesse frasi (la VOCE è congelata da prima
    della tappa: se è cambiata, il filmato scelto rispondeva a un'altra scena). Se nel frattempo è cambiata
    la durata — è arrivata la presa vera al posto della stima — la scelta resta ma la resa no: si torna a
    `scelto`, e `broll rendi` la rifà lunga giusta. Ritorna le scene che hanno ereditato.
    """
    ereditate: list[int] = []
    for s in nuovo.scene:
        v = vecchio.scena(s.n)
        if v is None or s.registro != "filmato" or v.registro != "filmato" or v.voce != s.voce:
            continue
        s.query = v.query or s.query
        s.candidati, s.scelti, s.file = v.candidati, v.scelti, v.file or s.file
        s.stato = v.stato
        if v.stato == "reso" and abs(v.durata_s - s.durata_s) > 1 / fps:
            s.stato = "scelto"
            s.note = f"durata cambiata da {v.durata_s:.2f} a {s.durata_s:.2f} s: da rendere di nuovo"
        if s.candidati or s.scelti:
            ereditate.append(s.n)
    return ereditate


# --- controlli ------------------------------------------------------------------------------------

def controlla(p: Piano) -> list[Diagnostica]:
    """L'alternanza regge? Gli stessi limiti editoriali del resto del repo, nello stesso formato."""
    d: list[Diagnostica] = []
    filmati = [s.n for s in p.filmati]
    if not filmati:
        d.append(avviso("nessuna scena a filmato: il piano non cambia niente rispetto a oggi"))
    if len(filmati) > len(p.scene) // 2:
        d.append(avviso(f"{len(filmati)} scene su {len(p.scene)} a filmato: più della metà del reel è materiale "
                        "esterno, è uno stock video e non un reel spiegato"))
    for a, b in zip(filmati, filmati[1:]):
        if b == a + 1:
            d.append(avviso(f"scene {a} e {b} entrambe a filmato: l'alternanza si vede solo se si alterna", scena=b))
    for s in p.scene:
        if s.registro == "filmato" and s.tipo not in AMMESSE and s.tipo != "broll":
            d.append(avviso(f"scena [{s.tipo}] proposta a filmato: ammesse solo {' | '.join(AMMESSE)}", scena=s.n))
        if s.registro == "filmato" and not s.query:
            d.append(avviso("scena a filmato senza query di ricerca", scena=s.n))
    return d


def esito(p: Piano, diag: list[Diagnostica]) -> dict:
    """Lo schema ESITO di .claude/workflows/reel.js, per la tappa della pipeline."""
    errori = [str(x) for x in diag if x.livello == "errore"]
    return {"stato": "DONE" if not errori else "BLOCKED",
            "file": str(file_piano(p.slug).relative_to(RADICE)),
            "errori": errori,
            "avvisi": [str(x) for x in diag if x.livello != "errore"],
            "bloccato": bool(errori),
            "motivo": errori[0] if errori else ""}
