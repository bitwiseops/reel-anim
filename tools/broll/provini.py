"""I provini: un contact sheet dei candidati, per scegliere senza scaricare i filmati.

Si guardano le **miniature** che il fornitore dà già pronte, non i filmati: scegliere fra dieci candidati
scaricandoli tutti costa banda e disco per buttarne nove. Il filmato si scarica solo quando è scelto.

È lo stesso canale con cui Claude Code «guarda» i video nel resto del repo (`contact_sheet.genera`), e
lo stesso che il presentatore apre alla fermata.
"""
from __future__ import annotations

from pathlib import Path

import requests

from tools.reel.contact_sheet import genera as contact
from tools.reel.model import Diagnostica, avviso

from tools.anim.config import RADICE
SCADENZA_S = 30


def cartella(slug: str) -> Path:
    """Provini, contact sheet dei candidati e strisce di resa: lavoro transitorio, fuori dal progetto."""
    from tools.reel.percorsi import lavoro
    return lavoro(slug) / "broll"


def scarica_anteprima(candidato: dict, dest: Path) -> Path | None:
    url = candidato.get("anteprima")
    if not url:
        return None
    if dest.exists():
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        r = requests.get(url, timeout=SCADENZA_S)
        r.raise_for_status()
    except requests.RequestException:
        return None
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_bytes(r.content)
    tmp.replace(dest)
    return dest


def _etichetta(c: dict) -> str:
    resta = c.get("resta_ritaglio")
    pezzi = [f"{c['fornitore']}:{c['id']}",
             f"{c.get('larghezza')}×{c.get('altezza')} · {c.get('durata_s', 0):.0f}s"]
    if resta is not None and resta < 1:
        pezzi.append(f"resta {resta:.0%} dopo il ritaglio")
    if c.get("autore"):
        pezzi.append(c["autore"])
    return "\n".join(pezzi)


def provini_immagini(slug: str, n: int, scelti: list[dict]) -> tuple[Path | None, list[Diagnostica]]:
    """Il contact sheet delle immagini generate di una scena: si guardano **prima** di rendere.

    Le immagini sono già su disco (la cache di `broll genera`), quindi non si scarica niente: serve solo a
    vederle in fila, con il prompt sotto, nell'ordine in cui andranno sui beat.
    """
    diag: list[Diagnostica] = []
    elementi = []
    for i, t in enumerate(scelti, start=1):
        f = Path(t.get("file") or "").expanduser()
        f = f if f.is_absolute() else RADICE / f
        if not f.exists():
            diag.append(avviso(f"immagine {i} non trovata ({f.name})", scena=n))
            continue
        prompt = (t.get("prompt") or "").strip()
        elementi.append({"file": str(f), "animata": True,
                         "etichetta": f"{i}. {t.get('modello') or 'meshy'}\n{prompt[:160]}"})
    if not elementi:
        diag.append(avviso("nessuna immagine da mostrare", scena=n))
        return None, diag
    dest = contact(elementi, diag, cartella(slug) / f"immagini-scena-{n:02d}.png",
                   colonne=min(3, len(elementi)), larghezza_cella=300)
    return dest, diag


def provini_scena(slug: str, n: int, candidati: list[dict], durata_s: float = 0.0,
                  scelto: str | None = None) -> tuple[Path | None, list[Diagnostica]]:
    """Contact sheet dei candidati di una scena. Segna in rosso quelli che non reggono la scena."""
    diag: list[Diagnostica] = []
    if not candidati:
        diag.append(avviso("nessun candidato da mostrare", scena=n))
        return None, diag

    out = cartella(slug)
    elementi = []
    for c in candidati:
        f = scarica_anteprima(c, out / f"cand-{n:02d}-{c['fornitore']}-{c['id']}.jpg")
        if not f:
            diag.append(avviso(f"miniatura non scaricata per {c['fornitore']}:{c['id']}", scena=n))
            continue
        corto = durata_s and c.get("durata_s", 0) < durata_s
        if corto:
            diag.append(avviso(f"{c['fornitore']}:{c['id']} dura {c.get('durata_s', 0):.0f}s, "
                               f"la scena {durata_s:.1f}s: andrà ripetuto o allungato", scena=n))
        etichetta = _etichetta(c)
        if scelto == f"{c['fornitore']}:{c['id']}":
            etichetta = "SCELTO · " + etichetta
        elementi.append({"file": str(f), "etichetta": etichetta, "animata": True,
                         "problema": bool(corto)})
    if not elementi:
        return None, diag
    dest = contact(elementi, diag, out / f"candidati-scena-{n:02d}.png",
                   colonne=min(4, len(elementi)), larghezza_cella=300)
    return dest, diag
