from pathlib import Path

import pytest

from tools.reel.parser import ErroreParse, parse, parse_testo

RADICE = Path(__file__).resolve().parents[1]
FM = "---\ntitolo: T\nslug: prova-parser\nformato: reel\nmessaggio_centrale: M\n---\n\n"


def _errori(corpo: str) -> str:
    with pytest.raises(ErroreParse) as e:
        parse_testo(FM + corpo)
    return " | ".join(d.msg for d in e.value.diagnostiche)


def test_esempio_completo():
    r, avvisi = parse(RADICE / "templates" / "esempio-reel.md")
    assert avvisi == [] and r.slug == "esempio-reel" and len(r.scene) == 7
    assert [s.tipo for s in r.scene] == ["hook"] + ["spiegazione"] * 4 + ["schermo", "chiusura"]
    hook, s2, s6, fine = r.scene[0], r.scene[1], r.scene[5], r.scene[6]
    assert hook.titolo == "Generativa non vuol dire creativa" and hook.sottotitolo == "Vuol dire ==probabile=="
    assert hook.riquadro_effettivo() == "no"
    assert len(s2.voce) == 3 and len(s2.animazione) == 3 and s2.testo == ["una parola alla volta"]
    assert s6.schermo == "chat-fotocopiatrice.png" and s6.riquadro_effettivo() == "alto-destra"
    assert fine.messaggio.startswith("Non chiederle") and fine.cta and fine.riquadro_effettivo() == "si"


def test_attributi_commenti_e_righe_ripetibili():
    r, avvisi = parse_testo(FM + "## Scena 1 [hook, durata=4s, transizione=taglio]\nTITOLO: T\n<!-- commento\nsu due righe -->\n\n"
                            "## Scena 2 [spiegazione, durata=500ms, colore=rosso]\nVOCE: una\nVOCE: due\nANIMAZIONE: a\n"
                            "RIQUADRO: sì\n\n## Scena 3 [chiusura]\nMESSAGGIO: M\nCTA: segui\n")
    s1, s2 = r.scene[0], r.scene[1]
    assert s1.durata_min_s == 4 and s1.transizione == "taglio"
    assert s2.durata_min_s == 0.5 and s2.voce == ["una", "due"] and s2.riquadro == "si"
    assert any("'colore' sconosciuto" in a.msg for a in avvisi)


def test_frontmatter_mancante():
    with pytest.raises(ErroreParse) as e:
        parse_testo("## Scena 1 [hook]\nTITOLO: T\n")
    assert "frontmatter" in e.value.diagnostiche[0].msg


def test_riga_sconosciuta_con_suggerimento():
    assert "forse intendevi 'VOCE:'" in _errori("## Scena 1 [hook]\nTITOLO: T\nVOCI: ciao\n\n## Scena 2 [chiusura]\nMESSAGGIO: M\n")


def test_regole_delle_scene():
    msg = _errori("## Scena 1 [spiegazione]\nVOCE: v\nTITOLO: fuori posto\n\n## Scena 2 [boh]\nVOCE: v\n\n"
                  "## Scena 3 [spiegazione]\nANIMAZIONE: a\nRIQUADRO: centro\n")
    for atteso in ("deve essere [hook]", "TITOLO ammesso solo", "tipo di scena 'boh'", "senza VOCE", "RIQUADRO 'centro'",
                   "l'ultima scena deve essere [chiusura]"):
        assert atteso in msg


def test_campi_obbligatori_e_vuoti():
    msg = _errori("## Scena 1 [hook]\nVOCE:\n\n## Scena 2 [schermo]\nVOCE: v\n\n## Scena 3 [chiusura]\nCTA: c\n")
    for atteso in ("VOCE vuoto", "[hook] senza TITOLO", "[schermo] senza SCHERMO", "[chiusura] senza MESSAGGIO"):
        assert atteso in msg
