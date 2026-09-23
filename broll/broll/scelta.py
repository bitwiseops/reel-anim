"""`broll scegli`: fissa nel piano quale candidato va in una scena, da che punto e con che ritaglio.

La scelta è la parte soggettiva e si fa guardando i provini; qui la si scrive in `piano.json` in modo che
le tappe a valle leggano il piano e non rigiudichino. Nella scelta si copia tutto il candidato (autore,
licenza, url): un `broll cerca` successivo rifà la lista dei candidati, e i crediti di un filmato già
scelto non devono dipendere da quella.

Una scena può avere più tagli (`--aggiungi`): gli stacchi fra l'uno e l'altro non si inventano, cadono
sugli inizi frase più vicini alla divisione in parti uguali, come nel registro a immagini.
"""
from __future__ import annotations

from tools.reel.model import Diagnostica, avviso, errore

from .inquadratura import ANCORE
from .piano import ScenaBroll

TAGLIO_MIN_S = 1.5      # sotto, più che uno stacco è un lampo: due tagli in una scena di tre secondi


class SceltaNonValida(ValueError):
    pass


def ancora(valore: str) -> float:
    """`sinistra | centro | destra` oppure un numero fra 0 e 1 (0 = tutto a sinistra)."""
    if valore in ANCORE:
        return ANCORE[valore]
    try:
        a = float(valore.replace(",", "."))
    except ValueError:
        raise SceltaNonValida(f"ancora «{valore}»: {' | '.join(ANCORE)} oppure un numero fra 0 e 1") from None
    if not 0.0 <= a <= 1.0:
        raise SceltaNonValida(f"ancora {a}: deve stare fra 0 e 1")
    return a


def scegli(s: ScenaBroll, chiave: str, da_s: float = 0.0, ancora_x: float = 0.5,
           aggiungi: bool = False) -> dict:
    """Mette il candidato fra i tagli della scena (al posto di quelli che c'erano, o in coda)."""
    if s.registro != "filmato":
        raise SceltaNonValida(f"la scena {s.n} è a «{s.registro}», non a filmato")
    c = next((c for c in s.candidati if f"{c['fornitore']}:{c['id']}" == chiave), None)
    if c is None:
        noti = ", ".join(f"{c['fornitore']}:{c['id']}" for c in s.candidati) or "nessuno: prima `broll cerca`"
        raise SceltaNonValida(f"{chiave} non è fra i candidati della scena {s.n} ({noti})")
    if da_s < 0:
        raise SceltaNonValida(f"--da {da_s}: non può essere negativo")
    taglio = {**c, "candidato": chiave, "da_s": round(da_s, 3), "ancora": round(ancora_x, 3)}
    s.scelti = (s.scelti if aggiungi else []) + [taglio]
    s.stato = "scelto"
    return taglio


def confini(quanti: int, inizi_frasi_s: list[float], durata_s: float) -> list[tuple[float, float]]:
    """Le finestre (inizio, durata) di `quanti` tagli dentro la scena.

    Ogni stacco va sull'inizio frase più vicino alla divisione in parti uguali; se lì vicino non c'è un
    beat utilizzabile (nessun beat, o uno che lascerebbe un taglio più corto di `TAGLIO_MIN_S`), resta
    la divisione in parti uguali.
    """
    if quanti <= 1:
        return [(0.0, durata_s)]
    stacchi: list[float] = []
    for i in range(1, quanti):
        ideale = durata_s * i / quanti
        prima = stacchi[-1] if stacchi else 0.0
        buoni = [t for t in inizi_frasi_s
                 if t - prima >= TAGLIO_MIN_S and durata_s - t >= TAGLIO_MIN_S * (quanti - i)]
        stacchi.append(min(buoni, key=lambda t: abs(t - ideale)) if buoni else max(ideale, prima))
    bordi = [0.0, *stacchi, durata_s]
    return [(a, b - a) for a, b in zip(bordi, bordi[1:])]


def controlla_immagini(s: ScenaBroll) -> list[Diagnostica]:
    """Le immagini generate ci sono ancora? La cache sta fuori da git: si rigenerano, non si recuperano."""
    from .rendi import file_immagini

    if not s.scelti:
        return [errore(f"nessuna immagine generata: `broll genera <slug> --scena {s.n}`", scena=s.n)]
    mancanti = [f.name for f in file_immagini(s) if not f.exists()]
    if mancanti:
        return [errore(f"{len(mancanti)} immagini non sono più nella cache ({', '.join(mancanti)}): "
                       f"`broll genera <slug> --scena {s.n}` le rifà", scena=s.n)]
    return []


def controlla_scelta(s: ScenaBroll) -> list[Diagnostica]:
    """I tagli scelti reggono la scena? Un filmato che finisce prima lascerebbe un fermo immagine."""
    d: list[Diagnostica] = []
    if s.registro == "immagini":
        return controlla_immagini(s)
    if not s.scelti:
        return [errore("nessun filmato scelto: `broll scegli`", scena=s.n)]
    for taglio, (_, durata) in zip(s.scelti, confini(len(s.scelti), s.inizi_frasi_s, s.durata_s)):
        resta = float(taglio.get("durata_s") or 0) - float(taglio.get("da_s") or 0)
        if resta < durata:
            d.append(errore(f"{taglio['candidato']} da {taglio.get('da_s', 0):.1f}s ne ha ancora {resta:.1f}, "
                            f"il taglio ne chiede {durata:.1f}: parti prima (--da) o aggiungi un taglio", scena=s.n))
        if float(taglio.get("resta_ritaglio") or 1) < 0.5:
            d.append(avviso(f"{taglio['candidato']} è orizzontale: dopo il ritaglio ne resta il "
                            f"{float(taglio['resta_ritaglio']):.0%}, guarda `broll prova-inquadratura`", scena=s.n))
    return d
