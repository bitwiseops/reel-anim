from pathlib import Path

from tools.anim.config import Config
from tools.reel import percorsi


def test_lavoro_fuori_dal_progetto_e_dal_config(tmp_path):
    cfg = Config({"percorsi": {"lavoro": str(tmp_path / "lav"), "cache_broll": str(tmp_path / "cache")}})
    assert percorsi.lavoro("x", cfg) == tmp_path / "lav" / "x"
    assert percorsi.cache_broll(cfg) == tmp_path / "cache"
    assert percorsi.lavoro_per("x", percorsi.riepilogo("x"), cfg) == tmp_path / "lav" / "x"


def test_con_out_esplicito_tutto_resta_insieme(tmp_path):
    assert percorsi.lavoro_per("x", tmp_path) == tmp_path


def test_senza_config_i_default():
    cfg = Config({})
    assert percorsi.radice_lavoro(cfg) == Path("~/Library/Caches/reel-anim").expanduser()


def test_relativo_o_assoluto(tmp_path):
    assert percorsi.relativo(tmp_path / "a" / "b.mp4", tmp_path) == "a/b.mp4"
    fuori = Path("/altrove/c.mp4")
    assert percorsi.relativo(fuori, tmp_path) == "/altrove/c.mp4"
    assert tmp_path / percorsi.relativo(fuori, tmp_path) == fuori
