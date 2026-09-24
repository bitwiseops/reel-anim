"""Parser della sceneggiatura reel (markdown a grammatica rigida) -> Reel (adattato da io-e-lia)."""
from __future__ import annotations

import difflib
import re
from pathlib import Path

import yaml

from .model import (CAPTION, CON_FILE, PIENO, POSIZIONI_RIQUADRO, TIPI_SCENA, TRANSIZIONI, Diagnostica, Reel, Scena,
                    avviso, errore)


class ErroreParse(Exception):
    def __init__(self, diagnostiche: list[Diagnostica]):
        super().__init__("\n".join(str(d) for d in diagnostiche))
        self.diagnostiche = diagnostiche


RE_H2_SCENA = re.compile(r"^##\s+scena\s+(\d+)\s*(?:\[(.*)\])?\s*$", re.I)
RE_H2 = re.compile(r"^##\s")
RE_H1 = re.compile(r"^#\s")
RE_CAMPO = re.compile(r"^(voce|animazione|figura|testo|titolo|sottotitolo|messaggio|cta|schermo|riquadro|caption)"
                      r"\s*:\s*(.*)$", re.I)
RE_COMMENTO = re.compile(r"<!--.*?-->", re.S)
RE_DURATA = re.compile(r"^(\d+(?:[.,]\d+)?)\s*(ms|s)?$", re.I)

PREFISSI = ["VOCE", "ANIMAZIONE", "FIGURA", "TESTO", "TITOLO", "SOTTOTITOLO", "MESSAGGIO", "CTA", "SCHERMO",
            "RIQUADRO", "CAPTION"]
RIPETIBILI = {"VOCE": "voce", "ANIMAZIONE": "animazione", "TESTO": "testo"}
SINGOLI = {"TITOLO": "titolo", "SOTTOTITOLO": "sottotitolo", "MESSAGGIO": "messaggio", "CTA": "cta",
           "SCHERMO": "schermo", "FIGURA": "figura"}
DOVE = {"TITOLO": ("hook",), "SOTTOTITOLO": ("hook",), "MESSAGGIO": ("chiusura",), "CTA": ("chiusura",),
        "SCHERMO": ("schermo", "spiegazione", "broll", "hook")}


def _durata_s(valore: str) -> float | None:
    m = RE_DURATA.match(valore.strip())
    if not m:
        return None
    n = float(m.group(1).replace(",", "."))
    return n / 1000 if (m.group(2) or "").lower() == "ms" else n


def _attributi(testo: str | None) -> tuple[list[str], dict[str, str]]:
    flag, kv = [], {}
    if not testo:
        return flag, kv
    for parte in testo.split(","):
        parte = parte.strip()
        if not parte:
            continue
        if "=" in parte:
            k, v = parte.split("=", 1)
            kv[k.strip().lower()] = v.strip()
        else:
            flag.append(parte.lower())
    return flag, kv


def _senza_commenti(testo: str) -> str:
    """Sostituisce i commenti HTML con righe vuote, preservando la numerazione."""
    return RE_COMMENTO.sub(lambda m: "\n" * m.group(0).count("\n"), testo)


def _frontmatter(testo: str) -> tuple[dict, int, list[Diagnostica]]:
    righe = testo.split("\n")
    if not righe or righe[0].strip() != "---":
        return {}, 0, [errore("frontmatter YAML mancante (il file deve iniziare con ---)", 1)]
    for i in range(1, len(righe)):
        if righe[i].strip() == "---":
            try:
                meta = yaml.safe_load("\n".join(righe[1:i])) or {}
            except yaml.YAMLError as e:  # pragma: no cover
                return {}, i + 1, [errore(f"frontmatter YAML non valido: {e}", 1)]
            if not isinstance(meta, dict):
                return {}, i + 1, [errore("frontmatter YAML non è un dizionario", 1)]
            return meta, i + 1, []
    return {}, 0, [errore("frontmatter YAML non chiuso (manca il secondo ---)", 1)]


def _scena(n: int, attr: str | None, n_riga: int, errori: list, avvisi: list) -> Scena:
    flag, kv = _attributi(attr)
    tipo = "spiegazione"
    if flag:
        if flag[0] in TIPI_SCENA:
            tipo = flag[0]
        else:
            errori.append(errore(f"tipo di scena '{flag[0]}' sconosciuto (validi: {' | '.join(TIPI_SCENA)})", n_riga, n))
        for f in flag[1:]:
            avvisi.append(avviso(f"flag '{f}' ignorato sulla scena (il primo flag è il tipo)", n_riga, n))
    s = Scena(n=n, tipo=tipo, riga=n_riga)
    for k, v in kv.items():
        if k == "durata":
            s.durata_min_s = _durata_s(v)
            if s.durata_min_s is None:
                errori.append(errore(f"durata='{v}' non valida (es. 6s)", n_riga, n))
        elif k == "transizione":
            if v.lower() in TRANSIZIONI:
                s.transizione = v.lower()
            else:
                errori.append(errore(f"transizione='{v}' non valida ({'|'.join(TRANSIZIONI)})", n_riga, n))
        else:
            avvisi.append(avviso(f"attributo '{k}' sconosciuto sulla scena, ignorato", n_riga, n))
    return s


def parse_testo(testo: str, sorgente: Path | None = None) -> tuple[Reel, list[Diagnostica]]:
    """Ritorna (reel, avvisi). Solleva ErroreParse se ci sono errori strutturali."""
    meta, inizio, errori = _frontmatter(testo)
    avvisi: list[Diagnostica] = []
    righe = _senza_commenti(testo).split("\n")
    scene: list[Scena] = []
    corrente: Scena | None = None
    dentro = False

    for idx in range(inizio, len(righe)):
        n_riga = idx + 1
        riga = righe[idx].rstrip()
        if not riga.strip():
            continue
        m = RE_H2_SCENA.match(riga)
        if m:
            corrente = _scena(int(m.group(1)), m.group(2), n_riga, errori, avvisi)
            scene.append(corrente)
            dentro = True
            continue
        if RE_H2.match(riga):
            dentro, corrente = False, None
            continue
        if RE_H1.match(riga) or not dentro or corrente is None:
            continue
        n, tipo = corrente.n, corrente.tipo

        m = RE_CAMPO.match(riga)
        if m:
            campo, contenuto = m.group(1).upper(), m.group(2).strip()
            if not contenuto:
                errori.append(errore(f"{campo} vuoto", n_riga, n))
                continue
            if campo in RIPETIBILI:
                getattr(corrente, RIPETIBILI[campo]).append(contenuto)
                continue
            if campo == "CAPTION":
                v = contenuto.lower()
                if v in CAPTION or v == "sì":
                    if corrente.caption is not None:
                        errori.append(errore("secondo CAPTION nella stessa scena", n_riga, n))
                    corrente.caption = "si" if v == "sì" else v
                else:
                    errori.append(errore(f"CAPTION '{contenuto}' non valido ({' | '.join(CAPTION)})", n_riga, n))
                continue
            if campo == "RIQUADRO":
                v = contenuto.lower()
                if v in ("si", "sì", "no", PIENO) or v in POSIZIONI_RIQUADRO:
                    if corrente.riquadro is not None:
                        errori.append(errore("secondo RIQUADRO nella stessa scena", n_riga, n))
                    corrente.riquadro = "si" if v == "sì" else v
                else:
                    errori.append(errore(f"RIQUADRO '{contenuto}' non valido "
                                         f"(no | si | {PIENO} | {' | '.join(POSIZIONI_RIQUADRO)})", n_riga, n))
                continue
            if campo in DOVE and tipo not in DOVE[campo]:
                errori.append(errore(f"{campo} ammesso solo in una scena [{' | '.join(DOVE[campo])}]", n_riga, n))
                continue
            attr = SINGOLI[campo]
            if getattr(corrente, attr) is not None:
                errori.append(errore(f"secondo {campo} nella stessa scena", n_riga, n))
            else:
                setattr(corrente, attr, contenuto)
            continue

        testa = re.split(r"[\s:\[]", riga.strip(), 1)[0].upper()
        vicini = difflib.get_close_matches(testa, PREFISSI, n=1, cutoff=0.6)
        sugg = f" (forse intendevi '{vicini[0]}:'?)" if vicini else ""
        errori.append(errore(f"riga non riconosciuta: «{riga.strip()[:60]}»{sugg}", n_riga, n))

    if not scene:
        errori.append(errore("nessuna '## Scena N' trovata"))
    else:
        if scene[0].tipo != "hook":
            errori.append(errore("la Scena 1 deve essere [hook]: è il titolo che ferma lo scroll", scene[0].riga, scene[0].n))
        if scene[-1].tipo != "chiusura":
            errori.append(errore("l'ultima scena deve essere [chiusura]", scene[-1].riga, scene[-1].n))
        for s in scene[1:]:
            if s.tipo == "hook":
                errori.append(errore("seconda scena [hook]: ne è ammessa una sola, all'inizio", s.riga, s.n))
        for s in scene[:-1]:
            if s.tipo == "chiusura":
                errori.append(errore("scena [chiusura] non in fondo: ne è ammessa una sola, alla fine", s.riga, s.n))
        for s in scene:
            if s.tipo == "hook" and not s.titolo:
                errori.append(errore("scena [hook] senza TITOLO", s.riga, s.n))
            elif s.tipo == "hook" and s.schermo and not s.voce:
                errori.append(errore("hook a filmato senza VOCE: il titolo non va a schermo, il problema lo pone "
                                     "il presentatore", s.riga, s.n))
            elif s.tipo == "chiusura" and not s.messaggio:
                errori.append(errore("scena [chiusura] senza MESSAGGIO", s.riga, s.n))
            elif s.tipo in CON_FILE and not s.schermo:
                errori.append(errore(f"scena [{s.tipo}] senza SCHERMO: <file>", s.riga, s.n))
            elif s.tipo in ("spiegazione", *CON_FILE) and not s.voce:
                errori.append(errore(f"scena [{s.tipo}] senza VOCE: cosa dice il presentatore?", s.riga, s.n))
    if errori:
        raise ErroreParse(errori)
    return Reel(meta, scene, sorgente), avvisi


def parse(path: str | Path) -> tuple[Reel, list[Diagnostica]]:
    p = Path(path)
    return parse_testo(p.read_text(encoding="utf-8"), p)


# --- markdown dell'idea ---------------------------------------------------------------------------------

def sezione(testo: str, titolo: str) -> str | None:
    """Il corpo di `## titolo`, fino al `##` dopo; None se la sezione non c'è."""
    m = re.search(rf"^## {re.escape(titolo)}\s*$", testo, re.M)
    if not m:
        return None
    fine = re.search(r"^## ", testo[m.end():], re.M)
    return (testo[m.end():m.end() + fine.start()] if fine else testo[m.end():]).strip()


def riga_sotto_stato(testo: str, etichetta: str, valore: str, errore: type[Exception] = ValueError) -> str:
    """Scrive `**etichetta:** valore` sotto la riga `**Stato:**`, o la aggiorna se c'è già."""
    riga = f"**{etichetta}:** {valore}"
    if re.search(rf"^\*\*{etichetta}:\*\*.*$", testo, re.M):
        return re.sub(rf"^\*\*{etichetta}:\*\*.*$", lambda _: riga, testo, count=1, flags=re.M)
    if not re.search(r"^\*\*Stato:\*\*.*$", testo, re.M):
        raise errore(f"l'idea non ha la riga «**Stato:**» sotto cui scrivere «**{etichetta}:**»")
    return re.sub(r"^(\*\*Stato:\*\*.*)$", lambda m: f"{m.group(1)}\n{riga}", testo, count=1, flags=re.M)
