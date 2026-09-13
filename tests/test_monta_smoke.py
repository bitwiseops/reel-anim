import json
import shutil
from pathlib import Path

import pytest

from tools.reel.__main__ import main

RADICE = Path(__file__).resolve().parents[1]


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which("say"), reason="la voce di prova richiede macOS say")
def test_monta_prova_una_scena_con_inizi_delle_frasi_e_cache(tmp_path):
    args = ["monta", str(RADICE / "templates" / "esempio-reel.md"), "--prova", "--anteprima", "--scena", "2", "--out", str(tmp_path)]
    assert main(args) == 0
    e = json.loads((tmp_path / "report.json").read_text())["elementi"][0]
    assert e["scena"] == 2 and e["origine_tempi"] == "voce-sintetica" and e["origine_durata"] == "voce-sintetica"
    inizi = e["inizi_frasi_s"]
    assert len(inizi) == 3 and inizi[0] == 0.0 and inizi == sorted(set(inizi)) and inizi[-1] < e["durata_s"]
    assert (tmp_path / e["video"]).exists() and (tmp_path / e["filmstrip"]).exists()

    assert main(args) == 0   # niente è cambiato: la grafica Manim viene dalla cache
    e2 = json.loads((tmp_path / "report.json").read_text())["elementi"][0]
    assert e2["tempo_manim_s"] < 0.5 and e2["inizi_frasi_s"] == inizi
