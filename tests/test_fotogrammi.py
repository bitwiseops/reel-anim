import json
import os
import subprocess
from pathlib import Path

import pytest
from PIL import Image

from tools.reel.ffmpeg import trova_ffmpeg
from tools.reel.fotogrammi import strisce_fitte, tempi_dal_report, tempi_fitti, video_scena


def test_tempi_fitti_finestra_attorno_a_ogni_beat():
    t = tempi_fitti([0.0, 4.0, 9.5], 10.0, fps=8, finestra_s=1.3)
    assert len(t) == 3
    assert t[0][0] == 0.0 and t[0][1] == 0.125 and t[0][-1] <= 1.3      # il primo beat non può partire prima dello zero
    assert t[1][0] == 3.8 and len(t[1]) == 11 and t[1][-1] == 5.05      # 0,2 s prima della frase, 1,3 s a 8 fps
    assert t[2][0] == 9.3 and t[2][-1] <= 9.95                          # tagliata alla fine della scena
    assert all(b > a for finestra in t for a, b in zip(finestra, finestra[1:]))


def test_tempi_fitti_casi_limite():
    assert tempi_fitti([], 5.0) == []
    assert tempi_fitti([0.0, 7.0], 5.0)[1] == []                        # un beat oltre la durata: finestra vuota, l'indice resta
    assert len(tempi_fitti([1.0], 5.0, fps=10, finestra_s=1.0)[0]) == 11
    assert tempi_fitti([1.0], 5.0, fps=0) == [[]]


def test_tempi_dal_report_e_ripiego_sul_report_di_prova(tmp_path):
    assert tempi_dal_report(tmp_path) == {}
    elementi = [{"scena": 1, "durata_s": 6.3, "inizi_frasi_s": [0.0, 4.8]}, {"scena": 2, "durata_s": 3.0}]
    (tmp_path / "report-prova.json").write_text(json.dumps({"elementi": elementi}), encoding="utf-8")
    assert tempi_dal_report(tmp_path) == {1: {"durata_s": 6.3, "inizi_frasi_s": [0.0, 4.8]}, 2: {"durata_s": 3.0, "inizi_frasi_s": []}}
    (tmp_path / "report.json").write_text(json.dumps({"elementi": elementi[:1]}), encoding="utf-8")
    assert list(tempi_dal_report(tmp_path)) == [1]                      # report.json, se c'è, vince


def test_video_scena_per_sorgente(tmp_path):
    assert video_scena(tmp_path, 2) is None and video_scena(tmp_path, 2, "anima") is None
    for k, risoluzione in enumerate(("1920p30", "960p15")):
        p = tmp_path / "_anima" / "videos" / risoluzione / "scena-02.mp4"
        p.parent.mkdir(parents=True)
        p.write_bytes(b"")
        os.utime(p, (1000 + k, 1000 + k))
    (tmp_path / "_scene").mkdir()
    (tmp_path / "_scene" / "02.mp4").write_bytes(b"")
    assert video_scena(tmp_path, 2) == tmp_path / "_scene" / "02.mp4"
    assert video_scena(tmp_path, 2, "anima").parent.name == "960p15"    # il render più recente


@pytest.fixture(scope="module")
def clip(tmp_path_factory) -> Path:
    ff, _ = trova_ffmpeg()
    dest = tmp_path_factory.mktemp("clip") / "c.mp4"
    subprocess.run([ff, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=s=270x480:r=30:d=3",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(dest)], check=True)
    return dest


@pytest.mark.slow
def test_strisce_fitte_nomi_e_dimensioni(clip, tmp_path):
    png = strisce_fitte(clip, 3.0, [0.0, 1.5], tmp_path, 4, fps=8, finestra_s=1.0)
    assert [p.name for p in png] == ["04-fitti-b0.png", "04-fitti-b1.png", "04-fitti-scena.png"]
    assert not list(tmp_path.glob("_*"))                                # le cartelle di lavoro spariscono
    b0 = Image.open(png[0])                                             # 9 fotogrammi da 270 px: 6 per riga, due righe
    assert b0.size == (6 * 270 + 5 * 12, 2 * (480 + 34) + 12)
    anima = strisce_fitte(clip, 3.0, [0.0], tmp_path, 4, sorgente="anima")   # nomi a parte: non sovrascrive la scena montata
    assert [p.name for p in anima] == ["04-fitti-anima-b0.png", "04-fitti-anima-scena.png"] and png[0].exists()
    scena = Image.open(png[2])                                          # 12 fotogrammi a 4 fps da 180 px: 10 per riga
    assert scena.size == (10 * 180 + 9 * 12, 2 * (320 + 34) + 12)


@pytest.mark.slow
def test_cmd_strisce_senza_report_fa_solo_la_scena_intera(clip, tmp_path, capsys):
    from tools.reel.__main__ import main
    md = Path(__file__).resolve().parents[1] / "templates" / "esempio-reel.md"
    (tmp_path / "_scene").mkdir()
    (tmp_path / "_scene" / "02.mp4").write_bytes(clip.read_bytes())
    assert main(["strisce", str(md), "--out", str(tmp_path), "--json"]) == 0
    j = json.loads(capsys.readouterr().out)
    assert [s["scena"] for s in j["scene"]] == [2] and "nessun report" in j["scene"][0]["avvisi"][0]
    assert [Path(p).name for p in j["scene"][0]["strisce"]] == ["02-fitti-scena.png"]
    (tmp_path / "report.json").write_text(json.dumps({"elementi": [{"scena": 2, "durata_s": 3.0, "inizi_frasi_s": [0.0, 1.2]}]}), encoding="utf-8")
    assert main(["strisce", str(md), "--out", str(tmp_path), "--scena", "2", "--json"]) == 0
    j = json.loads(capsys.readouterr().out)
    assert len(j["scene"][0]["strisce"]) == 3 and not j["scene"][0]["avvisi"]
    assert main(["strisce", str(md), "--out", str(tmp_path), "--scena", "5"]) == 1
    anima = tmp_path / "_anima" / "videos" / "960p15" / "scena-02.mp4"
    anima.parent.mkdir(parents=True)
    anima.write_bytes(clip.read_bytes())
    assert main(["strisce", str(md), "--out", str(tmp_path), "--sorgente", "anima", "--json"]) == 0
    nomi = [Path(p).name for p in json.loads(capsys.readouterr().out)["scene"][0]["strisce"]]
    assert nomi == ["02-fitti-anima-b0.png", "02-fitti-anima-b1.png", "02-fitti-anima-scena.png"]
