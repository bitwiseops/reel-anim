"""`broll genera`: le immagini di una scena, fatte con Meshy quando su Pexels non c'è niente di buono.

Decisione del presentatore del 2026-09-22: **quando un candidato buono non esiste, la clip della scena si
fa unendo 2-3 immagini generate**, con una dissolvenza fra l'una e l'altra. Non è un ripiego grafico ed è
l'opposto del testo di riserva: è materiale nuovo, fatto apposta per quella scena, che entra nel reel come
un filmato qualunque — un file per scena, 1080×1920, muto, lungo quanto la scena.

Il piano resta l'unico stato durevole: qui la scena passa a `registro: "immagini"`, stato `scelto`, con la
lista dei file e **i prompt usati**, che sono l'unica cosa che rende ripetibile un'immagine che in git non
c'è. I byte stanno nella cache, fuori da git, e rilanciare il comando non ripaga la generazione.

I prompt buoni li scrive l'agente, che ha davanti la scena: si passano con `--prompt`, uno per immagine.
Quello che si ricava dal brief `ANIMAZIONE:` è il ripiego, ed è fatto come le query di `query.py` — parole
piene, senza il gergo del montaggio — più un passaggio in inglese, perché Meshy lavora in inglese.
"""
from __future__ import annotations

from pathlib import Path

from tools.reel.model import Diagnostica, avviso
from tools.reel.percorsi import relativo

from .fornitori import meshy
from .piano import ScenaBroll
from .query import _parole

QUANTE_PREDEFINITE = 3
PAROLE_PER_PROMPT = 8

# La coda fissa di ogni prompt ricavato dal brief. «no text» non è un vezzo: dal 2026-09-20 i reel si
# guardano muti e le parole a schermo sono le caption, quindi un'immagine con scritte dentro è inservibile.
STILE = ("cinematic still, vertical 9:16, single clear subject, dark background, soft rim light, "
         "shallow depth of field, no text, no words, no letters, no logos, no watermark")
# Quando le immagini sono più dei soggetti che il brief offre, si cambia inquadratura invece di ripetere.
INQUADRATURE = ("wide shot", "close-up", "high angle", "low angle")

# Il brief è italiano, Meshy lavora in inglese. Non serve un traduttore: le parole che restano dopo il
# filtro di `query.py` sono poche e concrete, e quelle che il glossario non conosce passano com'erano —
# un nome proprio o un termine tecnico («token», «server») in inglese ci sta già.
GLOSSARIO = {
    "acqua": "water", "aereo": "airplane", "albero": "tree", "anziano": "elderly person",
    "aula": "classroom", "auto": "car", "azienda": "company office", "bambino": "child",
    "banco": "desk", "bicchiere": "glass", "biblioteca": "library", "bosco": "forest",
    "bussola": "compass", "cabina": "booth", "calcolatore": "computer", "camera": "room",
    "campo": "field", "cantiere": "construction site", "capannone": "warehouse", "carta": "paper",
    "cassetta": "box", "catena": "chain", "cavi": "cables", "cavo": "cable", "cervello": "brain",
    "chiave": "key", "città": "city", "computer": "computer", "corda": "rope", "costo": "cost",
    "cucina": "kitchen", "denaro": "money", "deserto": "desert", "dito": "finger", "donna": "woman",
    "energia": "energy", "fabbrica": "factory", "faro": "lighthouse", "ferro": "iron",
    "fila": "queue of people", "finestra": "window", "foglio": "sheet of paper", "folla": "crowd",
    "fumo": "smoke", "gente": "people", "ghiaccio": "ice", "giardino": "garden", "impronta": "footprint",
    "ingranaggi": "gears", "ingranaggio": "gear", "labirinto": "maze", "laboratorio": "laboratory",
    "lampada": "lamp", "libro": "book", "luce": "light", "macchina": "machine", "mano": "hand",
    "mappa": "map", "mare": "sea", "mattone": "brick", "medico": "doctor", "memoria": "memory",
    "montagna": "mountain", "motore": "engine", "mucchio": "pile", "muro": "wall", "nave": "ship",
    "nebbia": "fog", "notte": "night", "nuvola": "cloud", "occhio": "eye", "officina": "workshop",
    "ombra": "shadow", "onda": "wave", "operaio": "worker", "orologio": "clock", "ostacolo": "obstacle",
    "penna": "pen", "persona": "person", "persone": "people", "pila": "stack", "pioggia": "rain",
    "ponte": "bridge", "porta": "door", "quaderno": "notebook", "ragazza": "young woman",
    "ragazzo": "young man", "rete": "network", "ricerca": "search", "riunione": "meeting",
    "sabbia": "sand", "sala": "hall", "sasso": "stone", "scaffale": "shelf", "scala": "staircase",
    "scatola": "box", "scrivania": "desk", "semaforo": "traffic light", "sentiero": "path",
    "serra": "greenhouse", "server": "server rack", "sguardo": "gaze", "soldi": "money",
    "specchio": "mirror", "stanza": "room", "strada": "road", "studente": "student", "tavolo": "table",
    "telefono": "smartphone", "tempo": "time", "terra": "earth", "tetto": "roof", "traffico": "traffic",
    "treno": "train", "ufficio": "office", "uomo": "man", "valigia": "suitcase", "vento": "wind",
    "vetro": "glass", "viaggio": "journey", "zaino": "backpack",
    # qualità e azioni che nei brief descrivono davvero l'immagine
    "affollato": "crowded", "antico": "old", "buio": "dark", "caldo": "warm", "chiuso": "closed",
    "freddo": "cold", "grigio": "grey", "lento": "slow", "luminoso": "bright", "nuovo": "new",
    "pieno": "full", "rotto": "broken", "stanco": "tired", "veloce": "fast", "vecchio": "old",
    "vuoto": "empty", "aperto": "open", "solo": "alone", "insieme": "together",
    "cade": "falling", "corre": "running", "cresce": "growing", "guarda": "looking",
    "lavora": "working", "scrive": "writing", "sale": "rising", "scende": "descending",
    "aspetta": "waiting", "cerca": "searching", "costruisce": "building",
}


class PromptMancante(ValueError):
    pass


def _inglese(parole: list[str]) -> list[str]:
    """Le parole del brief in inglese, quando il glossario le conosce; le altre restano com'erano."""
    fuori: list[str] = []
    for w in parole:
        v = GLOSSARIO.get(w, w)
        if v not in fuori:
            fuori.append(v)
    return fuori


def soggetto(riga: str) -> str:
    """Il soggetto di una riga di brief: parole piene, senza il gergo del montaggio, in inglese."""
    return " ".join(_inglese(_parole(riga))[:PAROLE_PER_PROMPT])


def prompt_da_brief(s: ScenaBroll, quante: int = QUANTE_PREDEFINITE) -> list[str]:
    """`quante` prompt ricavati dal brief `ANIMAZIONE:` della scena (dalla VOCE solo se il brief manca).

    È il ripiego: i prompt buoni li scrive l'agente e si passano con `--prompt`. Qui si fa quel che fa
    `query.py` per le ricerche — una riga di brief, un soggetto — e quando le immagini sono più dei
    soggetti si cambia inquadratura invece di chiedere due volte la stessa cosa.
    """
    basi = [b for riga in s.brief if (b := soggetto(riga))]
    if not basi:
        basi = [b for riga in s.voce if (b := soggetto(riga))][:1]
    if not basi:
        raise PromptMancante(f"la scena {s.n} non ha né brief ANIMAZIONE: né VOCE: da cui ricavare un "
                             "prompt: passalo a mano con --prompt")
    fuori: list[str] = []
    for i in range(max(1, quante)):
        pezzi = [basi[i % len(basi)]]
        if quante > len(basi):
            pezzi.append(INQUADRATURE[i % len(INQUADRATURE)])
        pezzi.append(STILE)
        fuori.append(", ".join(pezzi))
    return fuori



def genera_scena(s: ScenaBroll, prompt: list[str] | None = None, *, quante: int = QUANTE_PREDEFINITE,
                 forza: bool = False, genera=None) -> tuple[list[dict], list[Diagnostica]]:
    """Genera (o ripesca dalla cache) le immagini della scena e le mette nel piano.

    Aggiorna `s`: registro `immagini`, stato `scelto`, `scelti` = una scheda per immagine (file, prompt,
    modello, data) e `file` = il nome che `broll rendi` scriverà. Ritorna `(schede, diagnostica)`.
    """
    genera = genera or meshy.genera          # risolto tardi, così i test lo sostituiscono con un finto
    prompts = [p.strip() for p in (prompt or []) if p.strip()] or prompt_da_brief(s, quante)
    diag: list[Diagnostica] = []
    schede: list[dict] = []
    for i, p in enumerate(prompts, start=1):
        f, scheda = genera(p, i, forza=forza)
        schede.append({**scheda, "file": relativo(Path(f))})
    s.registro = "immagini"
    s.scelti = schede
    s.stato = "scelto"
    s.file = s.nome_file()
    s.note = f"immagini generate: {len(schede)}"

    tenute = len(s.inizi_frasi_s) or 1
    if len(schede) < tenute:
        diag.append(avviso(f"{tenute} frasi e {len(schede)} immagini: qualcuna si ripeterà "
                           f"(`--quante {tenute}`)", scena=s.n))
    if not s.inizi_frasi_s:
        diag.append(avviso("il piano non ha gli inizi frase: le immagini non cadranno sui beat "
                           "(prima `uv run reel monta … --prova`, poi `broll piano`)", scena=s.n))
    return schede, diag
