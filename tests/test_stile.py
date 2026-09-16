import os
from pathlib import Path

from tools.anim.config import RADICE, carica
from tools.reel.__main__ import main
from tools.reel.stile import conta_reel, leggi_guida, leggi_pattern, stato

EXPORT = """# Reel analizzati

2 reel, raggruppati per account. Per ognuno: trascrizione dell'audio (Whisper) e analisi della struttura narrativa.

## @uno

### r001 · 0:42

- URL: https://example.com/r1

**Trascrizione**

Allora, guarda, ti spiego una cosa.

**Analisi**

Attacco al tu.

### r002 · 1:05

- URL: https://example.com/r2

**Trascrizione**

Sai perché succede?

**Analisi**

Domanda.
"""


def _cfg(tmp_path, corpus: str, guida: str, pattern: str = ""):
    base = tmp_path / "config.toml"
    base.write_text(f'[stile]\ncorpus = "{corpus}"\nguida = "{guida}"\npattern = "{pattern}"\n', encoding="utf-8")
    return carica.__wrapped__(base, tmp_path / "nessun-locale.toml")   # senza cache: i test riscrivono lo stesso file


def _guida(p: Path, reel: int, data: str = "2999-01-01") -> Path:
    p.write_text(f"# Stile parlato\n\n## Corpus\n- Percorso: x\n- Letto il: {data}\n- Reel letti: {reel}\n", encoding="utf-8")
    return p


def test_percorso_espande_tilde_relativo_e_vuoto(tmp_path):
    cfg = _cfg(tmp_path, "~/reelkit/export.md", "docs/stile-parlato.md")
    assert cfg.percorso("stile", "corpus") == Path.home() / "reelkit/export.md"
    assert cfg.percorso("stile", "guida") == RADICE / "docs/stile-parlato.md"
    assert cfg.percorso("stile", "assente") is None and cfg.percorso("nessuna", "x") is None
    assert _cfg(tmp_path, "", "g.md").percorso("stile", "corpus") is None


def test_conta_reel_e_leggi_guida(tmp_path):
    corpus = tmp_path / "export.md"
    corpus.write_text(EXPORT, encoding="utf-8")
    assert conta_reel(corpus) == 2 and conta_reel(tmp_path / "manca.md") == 0 and conta_reel(None) == 0
    assert leggi_guida(_guida(tmp_path / "g.md", 1, "2026-09-15")) == {"data": "2026-09-15", "reel": 1}
    assert leggi_guida(tmp_path / "manca.md") == {"data": None, "reel": None}


def test_verdetti(tmp_path):
    corpus = tmp_path / "export.md"
    corpus.write_text(EXPORT, encoding="utf-8")
    guida = tmp_path / "stile.md"
    assert stato(_cfg(tmp_path, str(corpus), str(guida)))["verdetto"] == "manca"
    _guida(guida, 1)
    assert stato(_cfg(tmp_path, str(corpus), str(guida)))["verdetto"] == "da rifare"
    _guida(guida, 2)
    s = stato(_cfg(tmp_path, str(corpus), str(guida)))
    assert s["verdetto"] == "aggiornata" and s["reel"] == 2
    _guida(guida, 2, "2000-01-01")                      # il corpus è stato toccato dopo la guida
    assert stato(_cfg(tmp_path, str(corpus), str(guida)))["verdetto"] == "da rifare"
    assert stato(_cfg(tmp_path, "", str(guida)))["verdetto"] == "provvisoria"
    assert stato(_cfg(tmp_path, str(tmp_path / "manca.md"), str(guida)))["verdetto"] == "provvisoria"


def test_leggi_pattern(tmp_path):
    p = tmp_path / "pattern.md"
    p.write_text("# Pattern ricorrenti\n\n30 reel analizzati, 118 tag distinti.\n", encoding="utf-8")
    r = leggi_pattern(p)
    assert r["esiste"] and r["reel"] == 30 and r["tag"] == 118 and len(r["data"]) == 10
    assert leggi_pattern(tmp_path / "manca.md") == {"esiste": False, "reel": None, "tag": None, "data": None}
    assert leggi_pattern(None)["esiste"] is False
    p.write_text("# Pattern ricorrenti\n\nniente numeri qui\n", encoding="utf-8")
    r = leggi_pattern(p)
    assert r["esiste"] and r["reel"] is None and r["tag"] is None
    s = stato(_cfg(tmp_path, "", "g.md", str(p)))
    assert s["pattern"] == p and s["pattern_esiste"] and s["pattern_reel"] is None
    assert stato(_cfg(tmp_path, "", "g.md"))["pattern"] is None


def test_comando_stile_stampa_e_esce_zero(capsys):
    assert main(["stile"]) == 0
    out = capsys.readouterr().out
    assert "corpus:" in out and "guida:" in out and "pattern:" in out and "verdetto:" in out
