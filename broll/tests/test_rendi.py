from __future__ import annotations

import subprocess

import pytest

from broll.fornitori import Candidato
from broll.piano import ScenaBroll
from broll.rendi import ResaFallita, fotogrammi, rendi_scena
from tools.reel.ffmpeg import ffprobe, trova_ffmpeg


def test_fotogrammi_la_somma_torna_anche_con_bordi_scomodi():
    # 15,02 s a 30 fps = 451 fotogrammi; arrotondando le durate una per una se ne perde uno
    finestre = [(0.0, 9.122), (9.122, 5.898)]
    assert sum(fotogrammi(finestre, 30)) == round(15.02 * 30)
    assert fotogrammi([(0.0, 3.0), (3.0, 3.0), (6.0, 3.0)], 30) == [90, 90, 90]


def test_candidato_da_un_taglio_del_piano():
    taglio = {"fornitore": "pexels", "id": "7", "url_pagina": "", "url_file": "u", "anteprima": "",
              "larghezza": 1080, "altezza": 1920, "durata_s": 9.0, "fps": 25.0, "autore": "", "autore_url": "",
              "licenza": "Pexels License", "query": "q", "resta_ritaglio": 1.0,
              "candidato": "pexels:7", "da_s": 2.0, "ancora": 0.5, "sha256": "abc"}
    assert Candidato.da_dict(taglio).chiave == "pexels:7"


def _filmato(dest, durata_s: float, misura: str = "1280x720", fps: int = 25):
    """Un 16:9 a 25 fps con l'audio: tutto quello che la resa deve togliere di mezzo."""
    ff, _ = trova_ffmpeg()
    subprocess.run([ff, "-y", "-loglevel", "error",
                    "-f", "lavfi", "-i", f"testsrc2=size={misura}:rate={fps}:duration={durata_s}",
                    "-f", "lavfi", "-i", f"sine=frequency=440:duration={durata_s}",
                    "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac",
                    str(dest)], check=True)
    return dest


def _scena(tagli: list[dict], durata_s: float, inizi: list[float]) -> ScenaBroll:
    return ScenaBroll(n=4, tipo="spiegazione", durata_s=durata_s, origine_durata="report", registro="filmato",
                      inizi_frasi_s=inizi, stato="scelto", scelti=tagli, file="broll-scena-04.mp4")


@pytest.mark.slow
def test_rendi_due_tagli_rispetta_il_contratto(tmp_path):
    a, b = _filmato(tmp_path / "a.mp4", 6), _filmato(tmp_path / "b.mp4", 5, fps=60)
    tagli = [{"candidato": "pexels:a", "fornitore": "pexels", "id": "a", "da_s": 1.0, "ancora": 0.0},
             {"candidato": "pexels:b", "fornitore": "pexels", "id": "b", "da_s": 0.0, "ancora": 1.0}]
    s = _scena(tagli, 6.03, [0.0, 2.9, 4.4])
    dest, diag = rendi_scena("x", s, dest=tmp_path / "out" / "broll-scena-04.mp4",
                             procura=lambda t: {"a": a, "b": b}[t["id"]])
    info = ffprobe(dest)
    assert (info["larghezza"], info["altezza"]) == (1080, 1920)
    assert info["audio"] is None
    assert info["fotogrammi"] == round(6.03 * 30)
    assert diag == [] and s.stato == "reso"
    assert all(len(t["sha256"]) == 64 for t in s.scelti)
    assert not list(dest.parent.glob("*.tmp*"))


@pytest.mark.slow
def test_rendi_un_filmato_troppo_corto_non_lascia_un_file_a_meta(tmp_path):
    corto = _filmato(tmp_path / "c.mp4", 2)
    s = _scena([{"candidato": "pexels:c", "fornitore": "pexels", "id": "c", "da_s": 0.0, "ancora": 0.5}], 5.0, [])
    dest = tmp_path / "out" / "broll-scena-04.mp4"
    with pytest.raises(ResaFallita, match="finisce prima"):
        rendi_scena("x", s, dest=dest, procura=lambda t: corto)
    assert s.stato == "scelto" and not dest.exists() and not list(dest.parent.glob("*"))


@pytest.mark.slow
def test_rendi_avvisa_se_il_file_non_e_piu_quello_del_piano(tmp_path):
    f = _filmato(tmp_path / "d.mp4", 4)
    s = _scena([{"candidato": "pexels:d", "fornitore": "pexels", "id": "d", "da_s": 0.0, "ancora": 0.5,
                 "sha256": "0" * 64}], 3.0, [])
    _, diag = rendi_scena("x", s, dest=tmp_path / "out.mp4", procura=lambda t: f)
    assert len(diag) == 1 and "sha256 diverso" in str(diag[0])
