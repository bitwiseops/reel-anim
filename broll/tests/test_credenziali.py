from __future__ import annotations

from broll.credenziali import chiave, chiavi, dove, mascherata

FINTA = "msy-" + "x" * 15          # finta, lunga 19: non è una chiave, serve solo a contare i caratteri


def test_mascherata_non_rivela_la_chiave():
    m = mascherata(FINTA)
    assert FINTA not in m
    assert m.startswith("msy-")
    assert "19 caratteri" in m
    assert mascherata(None) == "—"


def test_ambiente_ha_la_precedenza_sul_file(tmp_path, monkeypatch):
    import broll.credenziali as mod

    monkeypatch.setattr(mod, "RADICE", tmp_path)
    (tmp_path / ".env").write_text("MESHY_API_KEY=dal-file\n", encoding="utf-8")
    monkeypatch.setenv("MESHY_API_KEY", "dall-ambiente")
    assert chiave("MESHY_API_KEY") == "dall-ambiente"
    assert dove("MESHY_API_KEY") == "ambiente"


def test_ripiego_sul_file_env(tmp_path, monkeypatch):
    import broll.credenziali as mod

    monkeypatch.setattr(mod, "RADICE", tmp_path)
    monkeypatch.delenv("MESHY_API_KEY", raising=False)
    (tmp_path / ".env").write_text("# un commento\nALTRA=x\nMESHY_API_KEY='con-apici'\n", encoding="utf-8")
    assert chiave("MESHY_API_KEY") == "con-apici"      # apici tolti
    assert dove("MESHY_API_KEY") == ".env"


def test_chiave_assente(tmp_path, monkeypatch):
    import broll.credenziali as mod

    monkeypatch.setattr(mod, "RADICE", tmp_path)
    monkeypatch.delenv("PEXELS_API_KEY", raising=False)
    assert chiave("PEXELS_API_KEY") is None
    assert dove("PEXELS_API_KEY") == "—"


def test_riserva_dopo_la_principale(tmp_path, monkeypatch):
    """Come `meshy_api_keys()` in 3d-models-ai: la riserva entra quando la prima esaurisce i crediti."""
    import broll.credenziali as mod

    monkeypatch.setattr(mod, "RADICE", tmp_path)
    monkeypatch.setenv("MESHY_API_KEY", "prima")
    monkeypatch.setenv("MESHY_API_KEY_FALLBACK", "riserva")
    assert chiavi("meshy") == ["prima", "riserva"]


def test_pixabay_e_un_di_piu_non_un_requisito(tmp_path, monkeypatch):
    """Serve almeno un fornitore di ricerca, non tutti: con Pexels si cerca anche senza Pixabay."""
    import broll.credenziali as mod
    from broll.credenziali import configurati

    monkeypatch.setattr(mod, "RADICE", tmp_path)
    for n in ("PEXELS_API_KEY", "PIXABAY_API_KEY", "MESHY_API_KEY", "MESHY_API_KEY_FALLBACK"):
        monkeypatch.delenv(n, raising=False)
    monkeypatch.setenv("PEXELS_API_KEY", "x")
    assert configurati("ricerca") == ["pexels"]
    assert configurati("generazione") == []       # senza Meshy non si genera, ma si cerca lo stesso
