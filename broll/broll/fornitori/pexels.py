"""Pexels Videos: ricerca e scaricamento.

Si cerca **in verticale**: è la risposta migliore a «il formato deve adattarsi al reel», perché un
filmato già 9:16 annulla la perdita del 68 % che il ritaglio impone a un 16:9. Se in verticale non c'è
niente si riprova senza vincolo, e il candidato porta con sé quanto campo gli resterà dopo il taglio.

Licenza Pexels: uso libero anche commerciale, credito non obbligatorio ma richiesto dal servizio. Il
credito lo scriviamo comunque in `CREDITI.md`: costa niente e toglie ogni dubbio.
"""
from __future__ import annotations

import json
from pathlib import Path

import requests

from ..credenziali import chiave
from . import Candidato, FornitoreNonConfigurato, RichiestaFallita

NOME = "pexels"
RICERCA = "https://api.pexels.com/videos/search"
LICENZA = "Pexels License"
SCADENZA_S = 30


def _chiave() -> str:
    v = chiave("PEXELS_API_KEY")
    if not v:
        raise FornitoreNonConfigurato("manca PEXELS_API_KEY (vedi `broll chiavi`)")
    return v


def _migliore(files: list[dict], altezza_voluta: int = 1920) -> dict | None:
    """Il file da scaricare: il più piccolo che copre l'altezza voluta, altrimenti il più grande.

    Prendere sempre il massimo spreca banda e disco: di un 4K, dopo il ritaglio a 1080×1920, si butta
    quasi tutto.
    """
    utili = [f for f in files if f.get("link") and f.get("height")]
    if not utili:
        return None
    coprono = [f for f in utili if int(f["height"]) >= altezza_voluta]
    if coprono:
        return min(coprono, key=lambda f: int(f["height"]))
    return max(utili, key=lambda f: int(f["height"]) * int(f.get("width") or 0))


def _candidato(v: dict, query: str) -> Candidato | None:
    f = _migliore(v.get("video_files") or [])
    if not f:
        return None
    utente = v.get("user") or {}
    return Candidato(
        fornitore=NOME, id=str(v.get("id")),
        url_pagina=v.get("url") or "", url_file=f["link"], anteprima=v.get("image") or "",
        larghezza=int(f.get("width") or v.get("width") or 0),
        altezza=int(f.get("height") or v.get("height") or 0),
        durata_s=float(v.get("duration") or 0), fps=float(f.get("fps") or 0),
        autore=utente.get("name") or "", autore_url=utente.get("url") or "",
        licenza=LICENZA, query=query)


def cerca(query: str, *, verticale: bool = True, durata_min_s: float = 0.0,
          limite: int = 12) -> list[Candidato]:
    """Candidati per una query. Se in verticale non c'è niente di abbastanza lungo, riprova libero."""
    for orientamento in (["portrait"] if verticale else []) + [None]:
        params = {"query": query, "per_page": min(max(limite, 1), 80)}
        if orientamento:
            params["orientation"] = orientamento
        try:
            r = requests.get(RICERCA, params=params, headers={"Authorization": _chiave()},
                             timeout=SCADENZA_S)
        except requests.RequestException as e:
            raise RichiestaFallita(f"pexels non raggiungibile: {e}") from e
        if r.status_code == 401:
            raise FornitoreNonConfigurato("pexels rifiuta la chiave (401): controlla PEXELS_API_KEY")
        if r.status_code == 429:
            raise RichiestaFallita("pexels: troppe richieste (429), riprova più tardi")
        if not r.ok:
            raise RichiestaFallita(f"pexels ha risposto {r.status_code}: {r.text[:200]}")
        trovati = [c for v in (r.json().get("videos") or []) if (c := _candidato(v, query))]
        buoni = [c for c in trovati if c.durata_s >= durata_min_s]
        if buoni:
            return buoni[:limite]
    return []


def scarica(c: Candidato, dest: Path) -> Path:
    """Scarica il filmato e gli scrive accanto il sidecar con provenienza e licenza."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        try:
            with requests.get(c.url_file, stream=True, timeout=SCADENZA_S) as r:
                r.raise_for_status()
                tmp = dest.with_suffix(dest.suffix + ".tmp")
                with tmp.open("wb") as f:
                    for pezzo in r.iter_content(chunk_size=1 << 16):
                        f.write(pezzo)
                tmp.replace(dest)
        except requests.RequestException as e:
            raise RichiestaFallita(f"scaricamento fallito ({c.chiave}): {e}") from e
    dest.with_suffix(".json").write_text(
        json.dumps(c.to_dict(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return dest
