from pathlib import Path

from tools.reel.gobbo import gobbo
from tools.reel.parser import parse, parse_testo

RADICE = Path(__file__).resolve().parents[1]


def test_gobbo_dell_esempio():
    r, _ = parse(RADICE / "templates" / "esempio-reel.md")
    g = gobbo(r)
    assert g.startswith("GOBBO · Generativa non vuol dire creativa")
    assert "── Scena 1 [hook]" in g and "scena-07.mov" in g and "da registrare" in g
    assert "(a schermo: Generativa non vuol dire creativa)" in g
    assert "   1. L'IA scrive quello che ti aspetti?" in g and "   3. Vuol dire probabile." in g
    assert "==" not in g and "**" not in g   # il presentatore legge testo piano


def test_scena_senza_voce():
    r, _ = parse_testo("---\ntitolo: T\nslug: prova-gobbo\nformato: reel\nmessaggio_centrale: M\n---\n\n"
                       "## Scena 1 [hook]\nTITOLO: T\n\n## Scena 2 [chiusura]\nMESSAGGIO: M\n")
    assert "(nessuna voce: solo animazione)" in gobbo(r)
