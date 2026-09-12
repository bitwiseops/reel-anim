"""Modello dati di un reel: quello che il parser produce e tutto il resto consuma (adattato da io-e-lia)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

TIPI_SCENA = ("hook", "spiegazione", "schermo", "chiusura")
TRANSIZIONI = ("taglio", "dissolvenza")
POSIZIONI_RIQUADRO = ("basso-destra", "basso-sinistra", "alto-destra", "alto-sinistra")
STATI = ("sceneggiatura", "rivisto", "animato", "montato", "approvato", "pubblicato")


@dataclass
class Diagnostica:
    livello: str  # "errore" | "avviso"
    msg: str
    riga: int | None = None
    scena: int | None = None

    def __str__(self) -> str:
        dove = []
        if self.scena is not None:
            dove.append(f"scena {self.scena}")
        if self.riga is not None:
            dove.append(f"riga {self.riga}")
        prefisso = f"[{self.livello.upper()}]"
        return f"{prefisso:9s} {' · '.join(dove) + ': ' if dove else ''}{self.msg}"

    def to_dict(self) -> dict:
        return {"livello": self.livello, "msg": self.msg, "riga": self.riga, "scena": self.scena}


def errore(msg: str, riga: int | None = None, scena: int | None = None) -> Diagnostica:
    return Diagnostica("errore", msg, riga, scena)


def avviso(msg: str, riga: int | None = None, scena: int | None = None) -> Diagnostica:
    return Diagnostica("avviso", msg, riga, scena)


@dataclass
class Scena:
    n: int
    tipo: str = "spiegazione"
    riga: int = 0
    voce: list[str] = field(default_factory=list)        # frasi dette a camera: ogni riga è un beat
    animazione: list[str] = field(default_factory=list)  # brief per l'animatore
    testo: list[str] = field(default_factory=list)       # etichette a schermo
    titolo: str | None = None                            # hook
    sottotitolo: str | None = None                       # hook
    messaggio: str | None = None                         # chiusura
    cta: str | None = None                               # chiusura
    schermo: str | None = None                           # file b-roll (relativo a contenuti/media/<slug>/)
    riquadro: str | None = None                          # None = default per tipo; "no" | "si" | posizione
    durata_min_s: float | None = None
    transizione: str | None = None

    @property
    def voce_piena(self) -> str:
        return " ".join(self.voce)

    @property
    def parole_voce(self) -> int:
        return conta_parole(self.voce_piena)

    @property
    def testi(self) -> list[str]:
        """Tutto ciò che compare a schermo o si dice (per emoji, evidenzia, claim)."""
        return [t for t in (self.titolo, self.sottotitolo, self.messaggio, self.cta) if t] + self.testo + self.voce

    def riquadro_effettivo(self) -> str:
        if self.riquadro is not None:
            return self.riquadro
        return "no" if self.tipo == "hook" else "si"

    def to_dict(self) -> dict:
        return {"n": self.n, "tipo": self.tipo, "voce": self.voce, "animazione": self.animazione, "testo": self.testo,
                "titolo": self.titolo, "sottotitolo": self.sottotitolo, "messaggio": self.messaggio, "cta": self.cta,
                "schermo": self.schermo, "riquadro": self.riquadro_effettivo(), "durata_min_s": self.durata_min_s,
                "transizione": self.transizione}


@dataclass
class Reel:
    meta: dict
    scene: list[Scena]
    sorgente: Path | None = None

    @property
    def slug(self) -> str:
        return str(self.meta.get("slug") or (self.sorgente.stem if self.sorgente else "reel"))

    @property
    def formato(self) -> str:
        return str(self.meta.get("formato") or "").strip().lower()

    @property
    def stato(self) -> str:
        return str(self.meta.get("stato") or "").strip().lower()

    @property
    def hook(self) -> Scena | None:
        return next((s for s in self.scene if s.tipo == "hook"), None)

    @property
    def chiusura(self) -> Scena | None:
        return next((s for s in self.scene if s.tipo == "chiusura"), None)

    @property
    def parole_voce(self) -> int:
        return sum(s.parole_voce for s in self.scene)

    def scena(self, n: int) -> Scena | None:
        return next((s for s in self.scene if s.n == n), None)


_INLINE = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|==(.+?)==")


def testo_piano(testo: str) -> str:
    """Rimuove la formattazione inline (*corsivo*, **grassetto**, ==evidenzia==)."""
    return _INLINE.sub(lambda m: m.group(1) or m.group(2) or m.group(3), testo)


def conta_parole(testo: str) -> int:
    return len(testo_piano(testo).split())


def evidenziate(testo: str) -> list[str]:
    return re.findall(r"==(.+?)==", testo)


_EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F1E6-\U0001F1FF]")


def conta_emoji(testo: str) -> int:
    return len(_EMOJI.findall(testo))
