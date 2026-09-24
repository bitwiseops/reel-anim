"""I banchi di filmati, dietro una sola interfaccia.

Un candidato è una proposta, non ancora un file: porta con sé da dove viene, di chi è e con che licenza,
perché quelle sono le cose che finiscono in `piano.json` e in `CREDITI.md`, cioè in git. I byte no.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Candidato:
    fornitore: str
    id: str
    url_pagina: str
    url_file: str
    anteprima: str          # miniatura: si guarda questa nei provini, invece di scaricare il filmato
    larghezza: int
    altezza: int
    durata_s: float
    fps: float
    autore: str
    autore_url: str
    licenza: str
    query: str = ""

    @property
    def chiave(self) -> str:
        return f"{self.fornitore}:{self.id}"

    def resta_dopo_il_ritaglio(self, larghezza: int = 1080, altezza: int = 1920) -> float:
        """Quanta parte del campo sopravvive al ritaglio 9:16, fra 0 e 1."""
        if not self.larghezza or not self.altezza:
            return 0.0
        proporzione, obiettivo = self.larghezza / self.altezza, larghezza / altezza
        return min(1.0, obiettivo / proporzione) if proporzione > obiettivo else 1.0

    def to_dict(self) -> dict:
        return {"fornitore": self.fornitore, "id": self.id, "url_pagina": self.url_pagina,
                "url_file": self.url_file, "anteprima": self.anteprima, "larghezza": self.larghezza,
                "altezza": self.altezza, "durata_s": self.durata_s, "fps": self.fps,
                "autore": self.autore, "autore_url": self.autore_url, "licenza": self.licenza,
                "query": self.query, "resta_ritaglio": round(self.resta_dopo_il_ritaglio(), 3)}

    @classmethod
    def da_dict(cls, d: dict) -> Candidato:
        """Da un candidato o da un taglio del piano, che ha anche campi suoi (`da_s`, `ancora`…)."""
        return cls(**{c: d[c] for c in cls.__dataclass_fields__ if c in d})


class FornitoreNonConfigurato(RuntimeError):
    pass


class RichiestaFallita(RuntimeError):
    pass
