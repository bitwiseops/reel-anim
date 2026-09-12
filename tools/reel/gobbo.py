"""Gobbo (teleprompter) per la registrazione: una scheda per scena con la VOCE, la durata target e il file atteso."""
from __future__ import annotations

from ..anim.config import carica
from .clip import nome_atteso, trova
from .model import Reel, testo_piano
from .stima import durata_stimata_s


def gobbo(r: Reel) -> str:
    cfg = carica()
    nome = cfg.presentatore.nome
    righe = [f"GOBBO · {r.meta.get('titolo', r.slug)} · {nome}", "",
             "Una clip per scena, letta a camera. Mezzo secondo di silenzio prima e dopo. Pausa breve tra le frasi.",
             f"Salva le clip in contenuti/media/{r.slug}/ con il nome indicato.", ""]
    for s in r.scene:
        clip = trova(r.slug, s.n)
        stato = f"registrata ({clip.name})" if clip else "da registrare"
        righe.append(f"── Scena {s.n} [{s.tipo}] · target ~{durata_stimata_s(s):.0f} s · {nome_atteso(s.n)} · {stato}")
        if s.tipo == "hook" and s.titolo:
            righe.append(f"   (a schermo: {testo_piano(s.titolo)})")
        for i, v in enumerate(s.voce, 1):
            righe.append(f"   {i}. {testo_piano(v)}")
        if not s.voce:
            righe.append("   (nessuna voce: solo animazione)")
        righe.append("")
    return "\n".join(righe)
