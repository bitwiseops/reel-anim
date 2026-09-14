from pathlib import Path

from tools.reel.model import Scena
from tools.reel.parser import parse, parse_testo
from tools.reel.stima import durata_stimata_s
from tools.reel.validate import LIMITI, check, frasi_di, ha_errori

RADICE = Path(__file__).resolve().parents[1]
FM = "---\ntitolo: T\nslug: prova-validate\nformato: reel\nmessaggio_centrale: M\n---\n\n"
VOCE_20 = "VOCE: " + " ".join(["parola"] * 20)


def _base(n_spiegazioni: int = 4) -> list[str]:
    """Un reel valido: hook, n spiegazioni da ~7,9 s, chiusura."""
    scene = ["## Scena 1 [hook]\nTITOLO: Un titolo\nVOCE: ti apro con una frase breve"]
    scene += [f"## Scena {k + 2} [spiegazione]\n{VOCE_20}\nANIMAZIONE: qualcosa" for k in range(n_spiegazioni)]
    scene.append(f"## Scena {n_spiegazioni + 2} [chiusura]\nMESSAGGIO: Il messaggio\nCTA: salva\nVOCE: chiudiamo qui\nANIMAZIONE: fine")
    return scene


def _check(scene: list[str], fm: str = FM):
    r, avvisi = parse_testo(fm + "\n\n".join(scene))
    return avvisi + check(r)


def _msg(diag) -> str:
    return " | ".join(d.msg for d in diag)


def test_esempio_e_reel_base_senza_diagnostiche():
    r, avvisi = parse(RADICE / "templates" / "esempio-reel.md")
    assert avvisi + check(r) == []
    assert _check(_base()) == []


def test_limiti_di_voce_testo_beat_ed_evidenzia():
    scene = _base()
    scene[0] = "## Scena 1 [hook]\nTITOLO: T\nVOCE: " + " ".join(["y"] * (LIMITI["parole_voce_hook_max"] + 1))
    scene[1] = ("## Scena 2 [spiegazione]\nVOCE: " + " ".join(["x"] * (LIMITI["parole_voce_max"] + 1)) +
                "\nANIMAZIONE: a\nTESTO: uno due tre quattro cinque")
    nb = LIMITI["beat_max"] + 1
    scene[2] = "## Scena 3 [spiegazione]\n" + "\n".join(f"VOCE: frase ==numero== {k} detta" for k in range(nb)) + "\nANIMAZIONE: 1\nANIMAZIONE: 2"
    d = _check(scene)
    m = _msg(d)
    assert not ha_errori(d)
    for atteso in (f"VOCE dell'hook di {LIMITI['parole_voce_hook_max'] + 1} parole", f"VOCE di {LIMITI['parole_voce_max'] + 1} parole",
                   "TESTO «uno due tre quattro", f"{nb} righe VOCE (max {LIMITI['beat_max']})",
                   f"2 righe ANIMAZIONE per {nb} righe VOCE", f"{nb} ==evidenzia== nella scena"):
        assert atteso in m


def test_frontmatter_e_durata_del_reel():
    m = _msg(_check(_base(), fm="---\ntitolo: T\nformato: carosello\nmessaggio_centrale: M\n---\n\n"))
    assert "'slug' mancante" in m and "'formato: reel' obbligatorio" in m
    lungo = _check(_base(12))       # 14 scene × ~7,9 s ≈ 105 s: avviso, non errore
    assert not ha_errori(lungo) and "reel stimato" in _msg(lungo) and "14 scene" in _msg(lungo)
    troppo = _check(_base(16))
    assert ha_errori(troppo) and f"oltre {LIMITI['reel_errore_s']} s" in _msg(troppo)


def test_controlli_di_lingua_parlata():
    scene = _base()
    scene[1] = ("## Scena 2 [spiegazione]\nVOCE: A ogni bivio, di solito, vince la strada più battuta.\n"
                "VOCE: Il testo non lo cerca: lo scrive lei.\nVOCE: Fluente, sì.\nVOCE: ==Originale==, no.\nANIMAZIONE: a")
    scene[2] = "## Scena 3 [spiegazione]\nVOCE: Comincia così: caro Marco, da domani la sveglia…\nVOCE: Vuol dire probabile.\nANIMAZIONE: a"
    m = _msg(_check(scene))
    assert "«Fluente, sì.» «Originale, no.»: frasi da titolo in fila" in m
    assert "«Fluente, sì.»: schema «X, sì. Y, no.»" in m and "«Originale, no.»: schema" in m
    assert "«Il testo non lo cerca: lo scrive lei.»: due punti come snodo" in m and "Comincia così" not in m.split("due punti")[0][-60:]
    assert "3 frasi da titolo nel reel" in m and "«Vuol dire probabile.»" in m
    # parlato: nessun avviso di lingua
    scene[1] = ("## Scena 2 [spiegazione]\nVOCE: Quindi a ogni bivio, quasi sempre, prende la strada più battuta.\n"
                "VOCE: E non è che il testo lo va a cercare da qualche parte, lo scrive lei, una parola dopo l'altra.\n"
                "VOCE: Viene fuori fluente, certo. Ma originale no, non può esserlo.\nANIMAZIONE: a")
    scene[2] = "## Scena 3 [spiegazione]\nVOCE: Comincia così: «caro Marco, da domani la sveglia…»\nVOCE: Se l'hai già finito in testa, vuol dire che era probabile.\nANIMAZIONE: a"
    scene[-1] = "## Scena 6 [chiusura]\nMESSAGGIO: M\nCTA: salva\nVOCE: L'IA non ha mai conosciuto Marco.\nVOCE: Tu sì.\nVOCE: Per dispetto.\nANIMAZIONE: fine"
    m = _msg(_check(scene))
    assert "da titolo" not in m and "schema" not in m and "due punti" not in m, m
    assert frasi_di(["Uno. Due? Tre… quattro", "cinque!"]) == ["Uno.", "Due?", "Tre…", "quattro cinque!"]   # le righe sono un flusso


def test_controlli_di_linguaggio():
    scene = _base()
    scene[0] = "## Scena 1 [hook]\nTITOLO: T\nVOCE: Generativa non vuol dire creativa."
    scene[-1] = ("## Scena 6 [chiusura]\nMESSAGGIO: " + " ".join(["parola"] * 13) + "\nCTA: salva\nVOCE: " +
                 " ".join(["x"] * 26) + "\nANIMAZIONE: fine")
    m = _msg(_check(scene))
    assert "l'hook non parla a chi guarda" in m and "MESSAGGIO di 13 parole" in m and "VOCE della chiusura di 26 parole" in m
    for voce in ("L'IA scrive quello che ti aspetti?", "Hai mai scritto «sii originale»", "Finisci tu questa frase"):
        scene[0] = f"## Scena 1 [hook]\nTITOLO: T\nVOCE: {voce}"
        assert "l'hook non parla" not in _msg(_check(scene)), voce


def test_schermo_mancante_e_riquadro_sopra_il_broll():
    scene = _base()
    scene[1] = f"## Scena 2 [schermo]\nSCHERMO: nessuno.mp4\n{VOCE_20}\nANIMAZIONE: a"
    d = _check(scene)
    assert ha_errori(d) and "SCHERMO: file 'nessuno.mp4' non trovato" in _msg(d) and "copre la cornice del b-roll" in _msg(d)
    scene[1] += "\nRIQUADRO: alto-destra"
    assert "copre la cornice" not in _msg(_check(scene))


def test_stima_della_durata():
    assert durata_stimata_s(Scena(1, tipo="hook")) == 3.5
    assert durata_stimata_s(Scena(2, voce=["uno due"])) == 2.5               # il minimo
    assert durata_stimata_s(Scena(3, voce=[" ".join(["p"] * 28)])) == round(28 / 2.8 + 0.8, 2)
    assert durata_stimata_s(Scena(4, voce=["a b"], durata_min_s=6)) == 6
