"""Modello dati di un reel: quello che il parser produce e tutto il resto consuma (adattato da io-e-lia)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# [broll]: il filmato (o le immagini composte) a tutto schermo col riquadro sopra, senza grafica Manim.
# [schermo] resta il materiale nella finestra, con la grafica intorno.
TIPI_SCENA = ("hook", "spiegazione", "schermo", "broll", "chiusura")
CON_FILE = ("schermo", "broll")         # i tipi che senza SCHERMO: <file> non hanno niente da mostrare
TRANSIZIONI = ("taglio", "dissolvenza")
POSIZIONI_RIQUADRO = ("basso-destra", "basso-sinistra", "alto-destra", "alto-sinistra")
# RIQUADRO: pieno = il presentatore a tutta tela, con la grafica Manim (trasparente) sopra di lui. Dal 2026-09-21 è
# il default di [hook] e [chiusura]: lui che parla guardando in camera, con le caption e nient'altro (il MESSAGGIO
# della chiusura non va a schermo: è il testo per la caption del post).
PIENO = "pieno"
# CAPTION: i sottotitoli seguono la voce e si bruciano nel montaggio (tools/reel/caption.py). "no" li sospende
# dove la parola detta è già grande a schermo (punch, MESSAGGIO); "alto" sposta la fascia in cima, per la deroga
# delle scene in cui il testo *è* il contenuto.
CAPTION = ("si", "no", "alto", "basso")
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
    figura: str | None = None                            # cosa si capisce guardando, senza leggere niente a schermo
    testo: list[str] = field(default_factory=list)       # etichette a schermo (extra: numeri, una-due parole)
    titolo: str | None = None                            # hook
    sottotitolo: str | None = None                       # hook
    messaggio: str | None = None                         # chiusura
    cta: str | None = None                               # chiusura
    schermo: str | None = None                           # file b-roll (relativo a contenuti/media/<slug>/)
                                                         # in [schermo] sta nella finestra, in [broll] è tutta la tela
    riquadro: str | None = None                          # None = default per tipo; "no" | "si" | "pieno" | posizione
    caption: str | None = None                           # None = dal config; "no" | "alto" | "basso"
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

    @property
    def a_filmato(self) -> bool:
        """La scena è materiale esterno a tutta tela, senza grafica: una [broll], o un hook con `SCHERMO:`.

        L'hook a filmato è l'apertura parlata: il presentatore nel riquadro pone il problema, dietro c'è una clip
        che lo richiama, e il `TITOLO:` non va a schermo — vive solo in copertina.
        """
        return self.tipo == "broll" or (self.tipo == "hook" and bool(self.schermo))

    def riquadro_effettivo(self) -> str:
        """Dove sta il presentatore. Dal 2026-09-21 **i due estremi del reel sono suoi, a tutta tela**: l'apertura
        (pone il problema guardando in camera) e la chiusura (dice la conclusione). In mezzo sta nel riquadro, e
        sopra un filmato `[broll]` pure. `RIQUADRO: si` riporta una di quelle due al riquadro di prima, `no` lo
        toglie del tutto."""
        if self.riquadro is not None:
            return self.riquadro
        if self.tipo == "chiusura":
            return PIENO
        if self.tipo == "hook":
            return "si" if self.a_filmato else PIENO      # con SCHERMO: resta l'hook a filmato, col riquadro sopra
        return "si"

    @property
    def a_volto_pieno(self) -> bool:
        """Il presentatore riempie la tela: la grafica Manim gli va sopra, trasparente."""
        return self.riquadro_effettivo() == PIENO

    def caption_effettiva(self) -> str:
        """Dove stanno i sottotitoli in questa scena. Nella [chiusura] **a volto pieno** ci sono: c'è solo una faccia
        che parla, e senza sottotitoli chi guarda muto non legge la conclusione. In una chiusura riportata al riquadro
        (`RIQUADRO: si`) non ci sono: lì il MESSAGGIO è la frase detta scritta grande, e una caption sotto direbbe le
        stesse parole una seconda volta."""
        if self.caption is not None:
            return self.caption
        if self.tipo == "chiusura":
            return "si" if self.a_volto_pieno else "no"
        return "si"

    def to_dict(self) -> dict:
        return {"n": self.n, "tipo": self.tipo, "voce": self.voce, "animazione": self.animazione, "figura": self.figura,
                "testo": self.testo, "titolo": self.titolo, "sottotitolo": self.sottotitolo, "messaggio": self.messaggio,
                "cta": self.cta, "schermo": self.schermo, "riquadro": self.riquadro_effettivo(),
                "caption": self.caption_effettiva(), "durata_min_s": self.durata_min_s, "transizione": self.transizione}


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
