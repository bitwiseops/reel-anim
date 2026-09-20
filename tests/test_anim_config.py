from pathlib import Path

from tools.anim.config import Config, _fondi, carica, opzioni_manim, registra_font


def test_config_default_e_misure():
    cfg = carica()
    assert cfg.larghezza == 1080 and cfg.altezza == 1920 and cfg.fps == 30
    assert cfg.frame_width == 9 and cfg.frame_height == 16 and cfg.px_per_unita == 120
    assert cfg.palette.sfondo.startswith("#") and cfg.font.famiglia
    assert all(f.exists() for f in cfg.font_file())
    assert cfg.percorso("stile", "guida") == Path(__file__).resolve().parents[1] / "docs/stile-parlato.md"


def test_override_locale(tmp_path):
    base = tmp_path / "config.toml"
    base.write_text('[canale]\nnome = ""\nhandle = ""\n[palette]\nsfondo = "#000000"\naccento = "#FFFFFF"\n', encoding="utf-8")
    loc = tmp_path / "config.local.toml"
    loc.write_text('[canale]\nhandle = "@mio"\n[palette]\naccento = "#FF0000"\n', encoding="utf-8")
    cfg = carica(base, loc)
    assert cfg.canale.handle == "@mio" and cfg.palette.accento == "#FF0000" and cfg.palette.sfondo == "#000000"
    assert _fondi({"a": {"b": 1, "c": 2}}, {"a": {"c": 3}}) == {"a": {"b": 1, "c": 3}}


def test_opzioni_manim_qualita_e_trasparenza():
    cfg = carica()
    h = opzioni_manim(cfg, "h")
    assert (h["pixel_width"], h["pixel_height"], h["frame_rate"]) == (1080, 1920, 30) and h["format"] == "mp4"
    l = opzioni_manim(cfg, "l", trasparente=True, media_dir=Path("/tmp/x"), output_file="s")
    assert (l["pixel_width"], l["pixel_height"], l["frame_rate"]) == (540, 960, 15)
    assert l["transparent"] and l["movie_file_extension"] == ".mov" and l["media_dir"] == "/tmp/x" and l["output_file"] == "s"


def test_font_registrati_in_pango():
    import manimpango
    cfg = carica()
    assert len(registra_font(cfg)) == 4
    assert any(cfg.font.famiglia.lower() == f.lower() for f in manimpango.list_fonts())


def test_aree_lasciano_libero_il_riquadro():
    from tools.anim.base import aree
    cfg = carica()
    senza = aree(cfg, None)
    con = aree(cfg, "si")
    assert senza.riquadro is None and con.riquadro is not None
    assert con.contenuto.y1 < senza.contenuto.y1          # il riquadro sta in alto: il contenuto scende sotto la sua fascia
    assert con.riquadro.larghezza * cfg.px_per_unita == cfg.riquadro.dimensione_px
    assert con.riquadro.x1 <= senza.contenuto.x1 + 1e-6   # dentro la safe area a destra
