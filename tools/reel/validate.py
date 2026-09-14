"""Regole editoriali e strutturali del reel. Le costanti numeriche vivono SOLO qui (e vengono citate in CLAUDE.md)."""
from __future__ import annotations

from pathlib import Path

import re

from .model import STATI, Diagnostica, Reel, avviso, conta_emoji, conta_parole, errore, evidenziate, testo_piano
from .stima import durata_stimata_s

LIMITI = {
    "scene_min": 5,
    "scene_max": 9,
    "scene_tipiche": (6, 8),
    "parole_voce_max": 50,        # per scena (≈ 18 s a 2,8 parole/s): parlato vero, non titoli (dal 2026-09-15; era 35)
    "parole_voce_hook_max": 20,
    "parole_voce_chiusura_max": 18,   # la chiusura è un payoff, non un riassunto (docs/linguaggio-reel.md §8)
    "beat_max": 5,                # righe VOCE per scena (una riga = un beat = un pezzo di parlato)
    "parole_titolo_max": 10,
    "parole_messaggio_max": 25,
    "parole_messaggio_consigliate": 12,   # una frase grande a schermo; il resto in caption
    "testo_max": 4,
    "parole_testo_max": 4,
    "evidenzia_max": 1,           # ==evidenzia== per scena
    "emoji_scena_max": 1,
    "scena_min_s": 2.5,
    "scena_max_s": 19,
    "reel_min_s": 30,
    "reel_max_s": 90,             # Instagram non penalizza i video lunghi (docs/linguaggio-reel.md §0); era 60 fino al 2026-09-15
    "reel_errore_s": 120,
    "frasi_titolo_reel_max": 1,   # un solo aforisma per reel fuori dalla chiusura (la battuta finale è a parte)
}

RADICE = Path(__file__).resolve().parents[2]


def cartella_media(r: Reel) -> Path:
    return RADICE / "contenuti" / "media" / r.slug


def _riquadro_su_schermo(riquadro: str) -> bool:
    """Il riquadro del presentatore in quella posizione tocca la cornice [schermo] del config?"""
    from ..anim.config import carica
    from .compositing import posizione_riquadro
    cfg = carica()
    x, y, d = posizione_riquadro(cfg, riquadro)
    sc = cfg.dati["schermo"]
    return x < sc["x"] + sc["larghezza"] and x + d > sc["x"] and y < sc["y"] + sc["altezza"] and y + d > sc["y"]


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
    titoli_reel: list[str] = []
    for s in r.scene:
        e = lambda m: d.append(errore(m, s.riga, s.n))  # noqa: E731
        a = lambda m: d.append(avviso(m, s.riga, s.n))  # noqa: E731
        # lingua parlata (docs/sceneggiatura.md §5): euristiche, quindi avvisi
        frasi = frasi_di(s.voce)
        titoli = frasi_titolo(frasi)
        if len(titoli) >= 2:
            a(f"«{titoli[0]}» «{titoli[1]}»: frasi da titolo in fila: dille con un verbo (docs/linguaggio-reel.md §2)")
        if s.tipo != "chiusura":
            titoli_reel += titoli
        for f in frasi:
            if schema_si_no(f):
                a(f"«{f}»: schema «X, sì. Y, no.»: è scritto, non parlato")
        for riga in s.voce:
            if due_punti_snodo(riga):
                a(f"«{testo_piano(riga)[:50]}»: due punti come snodo: nel parlato è «cioè», «e allora», o due frasi")
        if s.tipo == "hook":
            if s.titolo and conta_parole(s.titolo) > L["parole_titolo_max"]:
                a(f"TITOLO lungo ({conta_parole(s.titolo)} parole, max {L['parole_titolo_max']}): deve reggere da solo")
            if s.parole_voce > L["parole_voce_hook_max"]:
                a(f"VOCE dell'hook di {s.parole_voce} parole (max {L['parole_voce_hook_max']}): l'hook si gioca in 3-5 s")
            if s.voce and not parla_a_chi_guarda(s.voce):
                a("l'hook non parla a chi guarda: nessun «tu» e nessuna domanda nella VOCE (docs/linguaggio-reel.md §1)")
        elif s.tipo == "chiusura":
            n_msg = conta_parole(s.messaggio or "")
            if n_msg > L["parole_messaggio_max"]:
                a(f"MESSAGGIO lungo ({n_msg} parole, max {L['parole_messaggio_max']})")
            elif n_msg > L["parole_messaggio_consigliate"]:
                a(f"MESSAGGIO di {n_msg} parole: a schermo ne reggono {L['parole_messaggio_consigliate']} "
                  "(una frase grande; il resto in caption)")
            if s.parole_voce > L["parole_voce_chiusura_max"]:
                a(f"VOCE della chiusura di {s.parole_voce} parole (max {L['parole_voce_chiusura_max']}): "
                  "la chiusura è un payoff, non un riassunto")
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
        if s.schermo and s.riquadro_effettivo() != "no" and _riquadro_su_schermo(s.riquadro_effettivo()):
            a(f"il riquadro ({s.riquadro_effettivo()}) copre la cornice del b-roll: usa RIQUADRO: alto-destra, alto-sinistra o no")
        sec = durata_stimata_s(s)
        totale += sec
        if sec > L["scena_max_s"]:
            a(f"scena stimata {sec:.1f} s (max {L['scena_max_s']} s): troppa voce per una scena")
        elif sec < L["scena_min_s"]:
            a(f"scena stimata {sec:.1f} s, sotto i {L['scena_min_s']} s")
    if len(titoli_reel) > L["frasi_titolo_reel_max"]:
        d.append(avviso(f"{len(titoli_reel)} frasi da titolo nel reel ({' / '.join('«' + t + '»' for t in titoli_reel)}): "
                        "al massimo un aforisma, ed è la battuta finale"))
    if totale > L["reel_errore_s"]:
        d.append(errore(f"reel stimato {totale:.0f} s, oltre {L['reel_errore_s']} s: taglia scene o voce"))
    elif totale > L["reel_max_s"]:
        d.append(avviso(f"reel stimato {totale:.0f} s (target {L['reel_min_s']}-{L['reel_max_s']} s): accorcia la voce"))
    elif totale < L["reel_min_s"]:
        d.append(avviso(f"reel stimato {totale:.0f} s, sotto i {L['reel_min_s']} s"))
    return d


_RE_TU = re.compile(r"\b(tu|ti|te|tuo|tua|tuoi|tue|voi|vi|vostro|vostra|hai|sei|sai|vuoi|puoi|fai|devi|pensi)\b|\bt'|"
                    r"\b(scrivi|chiedi|guarda|prova|immagina|finisci|saluta|pensa|metti|senti|vedi|dai|dille|dalle|dagli)\w*",
                    re.IGNORECASE)   # gli imperativi anche con il clitico attaccato: «scrivilo», «salutami»


def parla_a_chi_guarda(frasi: list[str]) -> bool:
    """Una domanda o un «tu» (pronomi e verbi alla seconda persona più comuni): l'hook è una promessa a chi guarda,
    non un titolo (docs/linguaggio-reel.md §1). Euristica: un imperativo senza pronome può sfuggire."""
    s = testo_piano(" ".join(frasi))
    return "?" in s or bool(_RE_TU.search(s))


_RE_FRASE = re.compile(r"[^.!?…]+[.!?…]*")
_RE_IO = re.compile(r"\b(io|mi|mio|mia|sono|ho|so|dico|provo|vedo|penso|faccio|chiedo|voglio|posso)\b", re.IGNORECASE)
_RE_SI_NO = re.compile(r",\s*(sì|no)\s*[.!…]*$", re.IGNORECASE)
_RE_DICE = re.compile(r"(scriv\w*|dic\w*|dett\w*|rispond\w*|chied\w*|legg\w*|così|esempio|tipo|ecco)\s*$", re.IGNORECASE)


def frasi_di(righe: list[str]) -> list[str]:
    """Le frasi (su . ! ? …) di tutte le righe VOCE, in testo piano."""
    return [f.strip() for f in _RE_FRASE.findall(testo_piano(" ".join(righe))) if f.strip()]


def frasi_titolo(frasi: list[str]) -> list[str]:
    """Le frasi «da titolo»: ≤ 4 parole, non una domanda, senza un «tu» né un «io». Lette a camera suonano recitate
    (docs/linguaggio-reel.md §2); ne è ammessa una per reel, la battuta. Euristica: un verbo alla terza persona in
    tre parole («Lo scrive lei.») viene contato lo stesso."""
    return [f for f in frasi if "?" not in f and conta_parole(f) <= 4 and not _RE_TU.search(f) and not _RE_IO.search(f)]


def schema_si_no(frase: str) -> bool:
    """«Fluente, sì.» «Originale, no.»: la coppia secca da scritto."""
    return bool(_RE_SI_NO.search(testo_piano(frase)))


def due_punti_snodo(riga: str) -> bool:
    """Due punti che nel parlato non si dicono: non introducono una citazione («Comincia così: caro Marco…», «scrive: …»)
    ma uno snodo logico («Il testo non lo cerca: lo scrive lei.»)."""
    s = testo_piano(riga)
    for m in re.finditer(":", s):
        prima, dopo = s[:m.start()], s[m.end():].lstrip()
        if dopo[:1] in ("«", '"', "“", "'", "‘") or _RE_DICE.search(prima):
            continue
        return True
    return False


def ha_errori(diagnostiche: list[Diagnostica]) -> bool:
    return any(x.livello == "errore" for x in diagnostiche)
