from pathlib import Path

from tools.reel.model import Scena
from tools.reel.parser import parse, parse_testo
from tools.reel.stima import durata_stimata_s
from tools.reel.validate import LIMITI, check, ha_errori

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
    scene[2] = "## Scena 3 [spiegazione]\n" + "\n".join(f"VOCE: frase ==numero== {k}" for k in range(5)) + "\nANIMAZIONE: 1\nANIMAZIONE: 2"
    d = _check(scene)
    m = _msg(d)
    assert not ha_errori(d)
    for atteso in ("VOCE dell'hook di 16 parole", "VOCE di 36 parole", "TESTO «uno due tre quattro", "5 righe VOCE (max 4)",
                   "2 righe ANIMAZIONE per 5 righe VOCE", "5 ==evidenzia== nella scena"):
        assert atteso in m


def test_frontmatter_e_durata_del_reel():
    m = _msg(_check(_base(), fm="---\ntitolo: T\nformato: carosello\nmessaggio_centrale: M\n---\n\n"))
    assert "'slug' mancante" in m and "'formato: reel' obbligatorio" in m
    lungo = _check(_base(8))
    assert not ha_errori(lungo) and "reel stimato" in _msg(lungo) and "10 scene" in _msg(lungo)
    troppo = _check(_base(12))
    assert ha_errori(troppo) and "oltre 90 s" in _msg(troppo)


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
