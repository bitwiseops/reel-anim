"""`reel parlato`: il testo recitato in registrazione contro la VOCE, e --applica che lo riporta nel .md."""
import json

from tools.reel import clip as clipmod
from tools.reel import parlato
from tools.reel.parser import parse
from tools.reel.validate import check, ha_errori

MD = ("---\ntitolo: T\nslug: prova-parlato\nformato: reel\nmessaggio_centrale: M\n---\n\n"
      "<!--\nVOCE: dentro un commento, da non toccare\n-->\n\n"
      "## Scena 1 [hook]\nTITOLO: T\nVOCE: Una domanda?\n\n"
      "## Scena 2 [spiegazione]\nVOCE: Prima frase.\nANIMAZIONE: qualcosa\nVOCE: Seconda ==frase==.\n\n"
      "## Scena 3 [chiusura]\nMESSAGGIO: M\nVOCE: Fine.\n\n## Note\nVOCE: nelle note, da non toccare\n")


def test_confronto_e_applica(tmp_path, monkeypatch):
    monkeypatch.setattr(clipmod, "RADICE", tmp_path)
    md = tmp_path / "s.md"
    md.write_text(MD, encoding="utf-8")
    r, _ = parse(md)
    assert parlato.recitato(r) == {}
    clipmod.salva_parlato(r.slug, 2, ["Prima frase, detta meglio.", "Seconda ==frase==."])
    clipmod.salva_parlato(r.slug, 3, ["troppe", "righe"])                   # numero sbagliato: ignorata
    media = clipmod.cartella(r.slug)
    (media / "scena-01.mov").write_bytes(b"")
    (media / "scena-01.json").write_text(json.dumps({"inizi_frasi_s": [0.0], "voce": ["Una domanda, vera?"]}))
    cambi = parlato.recitato(r)
    assert cambi == {1: ["Una domanda, vera?"], 2: ["Prima frase, detta meglio.", "Seconda ==frase==."]}
    testo = parlato.confronto(r, cambi)
    assert "- Prima frase." in testo and "+ Prima frase, detta meglio." in testo and "= Seconda ==frase==." in testo
    assert parlato.applica(md, cambi) == 2
    nuovo = md.read_text(encoding="utf-8")
    assert "VOCE: Una domanda, vera?" in nuovo and "VOCE: Prima frase, detta meglio." in nuovo
    assert "dentro un commento, da non toccare" in nuovo and "VOCE: nelle note, da non toccare" in nuovo
    r2, diag = parse(md)
    assert [s.voce for s in r2.scene][:2] == [["Una domanda, vera?"], ["Prima frase, detta meglio.", "Seconda ==frase==."]]
    assert not ha_errori(diag + check(r2))
    assert parlato.recitato(r2) == {} and parlato.applica(md, {}) == 0
