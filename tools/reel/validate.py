"""Regole editoriali e strutturali del reel. Le costanti numeriche vivono SOLO qui (e vengono citate in CLAUDE.md)."""
from __future__ import annotations

from pathlib import Path

from .model import STATI, Diagnostica, Reel, avviso, conta_emoji, conta_parole, errore, evidenziate
from .stima import durata_stimata_s

LIMITI = {
    "scene_min": 5,
    "scene_max": 9,
    "scene_tipiche": (6, 8),
    "parole_voce_max": 35,        # per scena (≈ 12 s a 2,8 parole/s)
    "parole_voce_hook_max": 15,
    "beat_max": 4,                # righe VOCE per scena
    "parole_titolo_max": 10,
    "parole_messaggio_max": 25,
    "testo_max": 4,
    "parole_testo_max": 4,
    "evidenzia_max": 1,           # ==evidenzia== per scena
    "emoji_scena_max": 1,
    "scena_min_s": 2.5,
    "scena_max_s": 14,
    "reel_min_s": 30,
    "reel_max_s": 60,
    "reel_errore_s": 90,
}

RADICE = Path(__file__).resolve().parents[2]


def cartella_media(r: Reel) -> Path:
    return RADICE / "contenuti" / "media" / r.slug


def check(r: Reel) -> list[Diagnostica]:
    L = LIMITI
    d: list[Diagnostica] = []
    for campo in ("titolo", "slug", "messaggio_centrale"):
        if not str(r.meta.get(campo) or "").strip():
            d.append(errore(f"frontmatter: campo '{campo}' mancante o vuoto", 1))
    if r.formato != "reel":
        d.append(errore("frontmatter: 'formato: reel' obbligatorio", 1))
    if r.stato and r.stato not in STATI:
        d.append(avviso(f"frontmatter: stato '{r.stato}' sconosciuto ({' | '.join(STATI)})", 1))

    attesi = list(range(1, len(r.scene) + 1))
    if [s.n for s in r.scene] != attesi:
        d.append(errore(f"numerazione delle scene non consecutiva: {[s.n for s in r.scene]}", r.scene[0].riga))
    n = len(r.scene)
    if n < L["scene_min"] or n > L["scene_max"]:
        d.append(avviso(f"{n} scene: consigliate {L['scene_tipiche'][0]}-{L['scene_tipiche'][1]} (min {L['scene_min']}, max {L['scene_max']})"))
    elif not (L["scene_tipiche"][0] <= n <= L["scene_tipiche"][1]):
        d.append(avviso(f"{n} scene: il formato tipico è {L['scene_tipiche'][0]}-{L['scene_tipiche'][1]}"))

    totale = 0.0
    for s in r.scene:
        e = lambda m: d.append(errore(m, s.riga, s.n))  # noqa: E731
        a = lambda m: d.append(avviso(m, s.riga, s.n))  # noqa: E731
        if s.tipo == "hook":
            if s.titolo and conta_parole(s.titolo) > L["parole_titolo_max"]:
                a(f"TITOLO lungo ({conta_parole(s.titolo)} parole, max {L['parole_titolo_max']}): deve reggere da solo")
            if s.parole_voce > L["parole_voce_hook_max"]:
                a(f"VOCE dell'hook di {s.parole_voce} parole (max {L['parole_voce_hook_max']}): l'hook si gioca in 3-5 s")
        elif s.tipo == "chiusura":
            if s.messaggio and conta_parole(s.messaggio) > L["parole_messaggio_max"]:
                a(f"MESSAGGIO lungo ({conta_parole(s.messaggio)} parole, max {L['parole_messaggio_max']})")
            if not s.cta:
                a("chiusura senza CTA")
        if s.parole_voce > L["parole_voce_max"]:
            a(f"VOCE di {s.parole_voce} parole (max {L['parole_voce_max']}): spezza la scena in due")
        if len(s.voce) > L["beat_max"]:
            a(f"{len(s.voce)} righe VOCE (max {L['beat_max']}): troppi beat per una scena")
        if s.tipo != "hook" and not s.animazione:
            a("scena senza ANIMAZIONE: l'animatore non sa cosa disegnare")
        if s.voce and s.animazione and len(s.animazione) not in (1, len(s.voce)):
            a(f"{len(s.animazione)} righe ANIMAZIONE per {len(s.voce)} righe VOCE: o una sola, o una per frase (beat)")
        if len(s.testo) > L["testo_max"]:
            a(f"{len(s.testo)} TESTO (max {L['testo_max']})")
        for t in s.testo:
            if conta_parole(t) > L["parole_testo_max"]:
                a(f"TESTO «{t[:30]}» di {conta_parole(t)} parole (max {L['parole_testo_max']}): è un'etichetta, non una frase")
        ev = sum(len(evidenziate(t)) for t in s.testi)
        if ev > L["evidenzia_max"]:
            a(f"{ev} ==evidenzia== nella scena (max {L['evidenzia_max']}): una sola parola conta")
        emoji = sum(conta_emoji(t) for t in s.testi)
        if emoji > L["emoji_scena_max"]:
            a(f"{emoji} emoji nella scena (max {L['emoji_scena_max']})")
        if s.schermo:
            f = cartella_media(r) / s.schermo
            if not f.exists():
                e(f"SCHERMO: file '{s.schermo}' non trovato in {f.parent.relative_to(RADICE)}/")
        if s.tipo == "schermo" and s.riquadro_effettivo() != "no":
            pass  # il riquadro sopra lo schermo è ammesso: la cornice lascia libera la fascia in basso
        sec = durata_stimata_s(s)
        totale += sec
        if sec > L["scena_max_s"]:
            a(f"scena stimata {sec:.1f} s (max {L['scena_max_s']} s): troppa voce per una scena")
        elif sec < L["scena_min_s"]:
            a(f"scena stimata {sec:.1f} s, sotto i {L['scena_min_s']} s")
    if totale > L["reel_errore_s"]:
        d.append(errore(f"reel stimato {totale:.0f} s, oltre {L['reel_errore_s']} s: taglia scene o voce"))
    elif totale > L["reel_max_s"]:
        d.append(avviso(f"reel stimato {totale:.0f} s (target {L['reel_min_s']}-{L['reel_max_s']} s): accorcia la voce"))
    elif totale < L["reel_min_s"]:
        d.append(avviso(f"reel stimato {totale:.0f} s, sotto i {L['reel_min_s']} s"))
    return d


def ha_errori(diagnostiche: list[Diagnostica]) -> bool:
    return any(x.livello == "errore" for x in diagnostiche)
