"""Caption: i sottotitoli che seguono la voce, disegnati con Pillow e bruciati nel montaggio.

I reel si guardano senza audio (regole editoriali §1), quindi il parlato deve comparire scritto.
Le caption **non** stanno dentro Manim: la grafica si renderizza prima della registrazione, con i tempi della voce
sintetica, mentre i tempi buoni sono quelli della presa. Si bruciano quindi nel compositing (`compositing.Sorgenti`),
dopo che la clip del presentatore esiste; così valgono anche per le scene `[broll]`, che da Manim non passano.

Un blocco = 6-8 parole (`[caption] parole_blocco`), che è un respiro di lettura. L'inizio di ogni **frase** è esatto
(`inizi_frasi_s`); dentro la frase i blocchi si dividono in proporzione ai caratteri, come fa il karaoke di
`registra.parole_accese`: l'errore resta di due-tre decimi e su un blocco intero non si vede.

Perché Pillow e non `drawtext`/`ass`: l'ffmpeg di questa macchina è compilato senza libfreetype e senza libass
(`tools/reel/fotogrammi.py` lo dice già per il titolo di copertina). Pillow usa lo stesso font e la stessa palette
del resto del reel, misura l'a capo e disegna la piastra arrotondata.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

from ..anim.config import Config, carica
from .fotogrammi import font_pesato
from .model import RE_EVIDENZA, testo_piano

_RE_MARK = re.compile(r"\*\*|\*")


@dataclass(frozen=True)
class Blocco:
    """Un blocco di caption: il testo (con ==evidenzia== ancora dentro) e la finestra in cui sta a schermo."""
    testo: str
    t0: float
    t1: float
    frase: int   # indice della frase VOCE da cui viene

    @property
    def piano(self) -> str:
        return testo_piano(self.testo)


def attiva(cfg: Config, caption: str | bool | None = None) -> str | None:
    """Dove sta la fascia in questa scena: "basso" | "alto" | None (scena senza caption: chiusura, punch)."""
    c = cfg.dati.get("caption") or {}
    if not c:
        return None
    if caption is None or caption is True or caption in ("si", "sì"):
        return str(c.get("posizione", "basso"))
    if caption is False or caption in ("no", "nessuna"):
        return None
    return str(caption)


def fascia(cfg: Config, dove: str = "basso") -> tuple[int, int, int, int]:
    """(x, y, larghezza, altezza) in px della fascia delle caption, dentro la safe area."""
    c, s = cfg.dati["caption"], cfg.dati["safe_area"]
    h = int(c.get("altezza_px", 200))
    x = int(s.get("sinistra", 60))
    w = cfg.larghezza - x - int(s.get("destra", 120))
    y = cfg.altezza - int(s["basso"]) - h if dove == "basso" else int(s["alto"])
    return x, y, w, h


def _spezza(frase: str, parole_max: int, caratteri_max: int) -> list[str]:
    """Una frase in blocchi **di lunghezza simile**: si decide prima in quanti pezzi sta (al massimo `parole_max`
    parole e `caratteri_max` caratteri l'uno) e poi si taglia vicino alla misura giusta, preferendo la punteggiatura.
    Blocchi uguali si leggono meglio di un blocco pieno seguito da due parole."""
    parole = frase.split()
    if not parole:
        return []
    n = max(1, -(-len(parole) // parole_max), -(-len(frase) // caratteri_max))
    while True:
        tagli, presi = [], 0
        for k in range(1, n):
            ideale = round(len(parole) * k / n)
            scelto = ideale
            for d in (0, 1, -1, 2, -2):            # la pausa più vicina alla misura giusta
                j = ideale + d
                if presi < j < len(parole) and parole[j - 1].endswith((",", ";", ":", ".", "?", "!", "…")):
                    scelto = j
                    break
            scelto = max(presi + 1, min(scelto, len(parole) - (n - k)))
            tagli.append(scelto)
            presi = scelto
        pezzi = [" ".join(parole[a:b]) for a, b in zip([0] + tagli, tagli + [len(parole)], strict=True)]
        if all(len(x) <= caratteri_max and len(x.split()) <= parole_max for x in pezzi) or n >= len(parole):
            return pezzi
        n += 1


def blocchi(voce: list[str], inizi_s: list[float], durata_s: float, cfg: Config | None = None) -> list[Blocco]:
    """I blocchi di una scena, con i loro tempi. `inizi_s` sono gli inizi delle frasi (esatti con la presa o con la
    voce sintetica); dentro la frase i blocchi si dividono in proporzione ai caratteri."""
    cfg = cfg or carica()
    c = cfg.dati.get("caption") or {}
    parole_max = int(c.get("parole_blocco", 7))
    caratteri_max = int(c.get("caratteri_riga_max", 42)) * int(c.get("righe_max", 2))
    minimo = float(c.get("durata_min_s", 0.7))
    out: list[Blocco] = []
    for i, frase in enumerate(voce):
        da = float(inizi_s[i]) if i < len(inizi_s) else 0.0
        a = float(inizi_s[i + 1]) if i + 1 < len(inizi_s) else float(durata_s)
        pezzi = _spezza(frase, parole_max, caratteri_max)
        if not pezzi or a <= da:
            continue
        # sotto la durata minima si legge meno di quanto si insegue: si torna indietro a blocchi più lunghi
        while len(pezzi) > 1 and (a - da) / len(pezzi) < minimo:
            pezzi = _spezza(frase, parole_max * 2, caratteri_max * 2) if len(pezzi) > 2 else [frase]
            if len(pezzi) == 1:
                break
        pesi = [max(1, len(testo_piano(p))) for p in pezzi]
        tot = sum(pesi)
        della_frase: list[Blocco] = []
        t = da
        for p, peso in zip(pezzi, pesi, strict=True):
            fine = t + (a - da) * peso / tot
            della_frase.append(Blocco(p, round(t, 3), round(min(fine, a), 3), i))
            t = fine
        out += _unisci_corti(della_frase, minimo)
    return out


def _unisci_corti(blocchi_frase: list[Blocco], minimo: float) -> list[Blocco]:
    """Un blocco che resterebbe a schermo meno di `minimo` si legge come un lampo: si fonde con il vicino."""
    fusi = list(blocchi_frase)
    cambiato = True
    while cambiato and len(fusi) > 1:
        cambiato = False
        for k, b in enumerate(fusi):
            if b.t1 - b.t0 >= minimo:
                continue
            j = k - 1 if k > 0 else k + 1          # di norma si attacca al blocco prima
            a, z = (fusi[j], b) if j < k else (b, fusi[j])
            fusi[min(j, k)] = Blocco(f"{a.testo} {z.testo}", a.t0, z.t1, a.frase)
            fusi.pop(max(j, k))
            cambiato = True
            break
    return fusi


def _parole_accento(s: str) -> list[tuple[str, bool]]:
    """Le parole del blocco, ognuna con «è in accento?». La punteggiatura resta attaccata alla parola: «==sei==,»
    è una parola sola, non «sei» più una virgola che va a spasso."""
    resto = _RE_MARK.sub("", s)
    marcati: list[tuple[str, bool]] = []
    i = 0
    for m in RE_EVIDENZA.finditer(resto):
        marcati += [(c, False) for c in resto[i:m.start()]]
        marcati += [(c, True) for c in m.group(1)]
        i = m.end()
    marcati += [(c, False) for c in resto[i:]]
    parole: list[tuple[str, bool]] = []
    corrente, acc = "", False
    for c, a in marcati:
        if c.isspace():
            if corrente:
                parole.append((corrente, acc))
            corrente, acc = "", False
        else:
            corrente += c
            acc = acc or a
    if corrente:
        parole.append((corrente, acc))
    return parole


def _righe_segmentate(d: ImageDraw.ImageDraw, s: str, font, larghezza: int, righe_max: int) -> list[list[tuple[str, bool]]]:
    """A capo misurato, tenendosi dietro quali parole sono in accento. Su due righe le bilancia: una riga piena e
    una con l'ultima parola sola si legge peggio di due righe uguali."""
    parole = _parole_accento(s)
    if not parole:
        return [[]]
    misura = lambda ps: d.textlength(" ".join(w for w, _ in ps), font=font)   # noqa: E731
    if misura(parole) <= larghezza:
        return [parole]
    if righe_max >= 2:
        migliore, costo = None, None
        for k in range(1, len(parole)):
            a, b = misura(parole[:k]), misura(parole[k:])
            if max(a, b) <= larghezza and (costo is None or max(a, b) < costo):
                migliore, costo = k, max(a, b)
        if migliore:
            return [parole[:migliore], parole[migliore:]]
    righe: list[list[tuple[str, bool]]] = [[]]
    for w, acc in parole:
        if righe[-1] and misura(righe[-1] + [(w, acc)]) > larghezza:
            righe.append([(w, acc)])
        else:
            righe[-1].append((w, acc))
    return righe[:righe_max] if righe_max else righe


def disegna(b: Blocco, cartella: Path, cfg: Config | None = None, dove: str = "basso") -> Path:
    """Il PNG (RGBA) di un blocco, grande quanto la fascia. In cache per contenuto: lo stesso testo con lo stesso
    stile non si ridisegna."""
    cfg = cfg or carica()
    c, p = cfg.dati["caption"], cfg.palette
    x, y, w, h = fascia(cfg, dove)
    corpo = int(c.get("corpo_px", 56))
    chiave = hashlib.sha1(f"{b.testo}|{corpo}|{w}x{h}|{p.testo}|{p.accento}|{c.get('piastra_opacita')}|"
                          f"{c.get('raggio_px')}|{c.get('righe_max')}".encode()).hexdigest()[:16]
    dest = cartella / f"cap-{chiave}.png"
    if dest.exists():
        return dest
    cartella.mkdir(parents=True, exist_ok=True)
    k = 2   # supersampling: i glifi a 56 px si vedono, l'aliasing pure
    im = Image.new("RGBA", (w * k, h * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    font = font_pesato(cfg, corpo * k, peso=700)
    righe_max = int(c.get("righe_max", 2))
    margine = int(28 * k)
    righe = _righe_segmentate(d, b.testo, font, w * k - 2 * margine, righe_max)
    interlinea = int(corpo * k * 1.18)
    alt_testo = interlinea * len(righe)
    # piastra: serve sulle scene a filmato, dove sotto c'è un'immagine chiara
    larga = max(d.textlength(" ".join(p for p, _ in r), font=font) for r in righe) + 2 * margine
    piastra = (int((w * k - larga) / 2), int((h * k - alt_testo) / 2 - margine * 0.6),
               int((w * k + larga) / 2), int((h * k + alt_testo) / 2 + margine * 0.6))
    colore = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ImageDraw.Draw(colore).rounded_rectangle(piastra, radius=int(c.get("raggio_px", 16)) * k,
                                             fill=(*_rgb(p.sfondo), int(255 * float(c.get("piastra_opacita", 0.75)))))
    im = Image.alpha_composite(im, colore)
    d = ImageDraw.Draw(im)
    ty = (h * k - alt_testo) / 2
    for riga in righe:
        larghezza_riga = d.textlength(" ".join(w_ for w_, _ in riga), font=font)
        tx = (w * k - larghezza_riga) / 2
        for j, (parola, acc) in enumerate(riga):
            s = parola if j == len(riga) - 1 else parola + " "
            d.text((tx, ty), s, font=font, fill=p.accento if acc else p.testo)
            tx += d.textlength(s, font=font)
        ty += interlinea
    im.resize((w, h), Image.LANCZOS).save(dest)
    return dest


def _rgb(hex_colore: str) -> tuple[int, int, int]:
    s = hex_colore.lstrip("#")
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))   # type: ignore[return-value]


def prepara(voce: list[str], inizi_s: list[float], durata_s: float, cartella: Path, cfg: Config | None = None,
            dove: str | None = "basso") -> list[tuple[Path, Blocco]]:
    """I PNG pronti per il filtergraph: (file, blocco). `dove=None` = scena senza caption."""
    if dove is None:
        return []
    cfg = cfg or carica()
    return [(disegna(b, cartella, cfg, dove), b) for b in blocchi(voce, inizi_s, durata_s, cfg)]


__all__ = ["Blocco", "attiva", "blocchi", "disegna", "fascia", "prepara"]
