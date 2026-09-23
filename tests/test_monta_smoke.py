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


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which("say"), reason="la voce di prova richiede macOS say")
def test_monta_prova_una_scena_broll_senza_manim(tmp_path, monkeypatch):
    """Una scena [broll] non ha una classe Manim: il filmato fa da grafica, e se è corto `monta` lo dice."""
    import subprocess

    from tools.reel import clip, validate
    from tools.reel.ffmpeg import ffprobe, trova_ffmpeg

    media = tmp_path / "media"
    shutil.copytree(RADICE / "contenuti" / "media" / "esempio-reel", media)     # il b-roll della scena 6
    monkeypatch.setattr(clip, "cartella", lambda slug: media)
    monkeypatch.setattr(validate, "cartella_media", lambda r: media)
    subprocess.run([trova_ffmpeg()[0], "-y", "-loglevel", "error", "-f", "lavfi", "-i",
                    "testsrc2=size=1080x1920:rate=30:duration=2", "-pix_fmt", "yuv420p", str(media / "broll-scena-03.mp4")],
                   check=True)
    testo = (RADICE / "templates" / "esempio-reel.md").read_text(encoding="utf-8")
    md = tmp_path / "esempio-reel.md"
    testo = testo.replace("## Scena 3 [spiegazione]\n", "## Scena 3 [broll]\nSCHERMO: broll-scena-03.mp4\n")
    # sopra il filmato niente grafica: via TESTO e FIGURA della scena diventata [broll]
    testo = testo.replace("FIGURA: la stessa scelta ripetuta molte volte produce un testo intero.\nTESTO: 14\n", "")
    md.write_text(testo, encoding="utf-8")

    out = tmp_path / "out"
    assert main(["monta", str(md), "--prova", "--anteprima", "--scena", "3", "--out", str(out)]) == 0
    e = json.loads((out / "report.json").read_text())["elementi"][0]
    assert e["tipo_scena"] == "broll" and e["tempo_manim_s"] == 0.0 and e["schermo"] == "broll-scena-03.mp4"
    assert not list((out / "_manim").glob("*"))                     # Manim non è partito
    assert len(e["avvisi_tempi"]) == 1 and "il filmato dura 2.00 s" in e["avvisi_tempi"][0]
    probe = ffprobe(out / e["video"])
    assert (probe["larghezza"], probe["altezza"]) == (1080, 1920) and probe["audio"]
    assert abs(probe["durata_s"] - e["durata_s"]) < 0.1


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which("say"), reason="la voce di prova richiede macOS say")
def test_filmato_non_ancora_reso_anima_procede_e_monta_si_ferma(tmp_path, monkeypatch, capsys):
    """Dopo `broll scrivi --presto` la scena è [broll] ma il file non c'è: `valida` avvisa, `anima` salta la scena
    e non si blocca, `monta` dà l'errore col comando da lanciare e non arriva al reel."""
    from tools.reel import clip, validate

    media = tmp_path / "media"
    shutil.copytree(RADICE / "contenuti" / "media" / "esempio-reel", media)
    monkeypatch.setattr(clip, "cartella", lambda slug: media)
    monkeypatch.setattr(validate, "cartella_media", lambda r: media)
    testo = (RADICE / "templates" / "esempio-reel.md").read_text(encoding="utf-8")
    testo = testo.replace("## Scena 3 [spiegazione]\n", "## Scena 3 [broll]\nSCHERMO: broll-scena-03.mp4\n")
    testo = testo.replace("FIGURA: la stessa scelta ripetuta molte volte produce un testo intero.\nTESTO: 14\n", "")
    md = tmp_path / "esempio-reel.md"
    md.write_text(testo, encoding="utf-8")
    out = tmp_path / "out"

    assert main(["valida", str(md)]) == 0
    assert "non ancora reso" in "".join(capsys.readouterr())

    assert main(["anima", str(md), "--scena", "3", "--json", "--out", str(out)]) == 0
    esito = json.loads(capsys.readouterr().out)
    assert esito["ok"] and esito["scene"] == []                     # niente da animare, e nessun blocco di validazione

    assert main(["monta", str(md), "--prova", "--anteprima", "--scena", "3", "--out", str(out)]) == 1
    err = capsys.readouterr().err
    assert "filmato 'broll-scena-03.mp4' non trovato" in err and "broll rendi esempio-reel" in err
    report = json.loads((out / "report.json").read_text())
    assert report["elementi"] == [] and report["reel"] is None and not (out / "reel-9x16.mp4").exists()


def test_raccordi_del_riquadro_fra_volto_pieno_e_scena_vicina():
    """Il raccordo del 2026-09-22 vive nella scena a volto pieno e guarda la scena vicina: se quella ha il riquadro
    il volto ci si rimpicciolisce dentro, altrimenti resta lo stacco secco."""
    from tools.reel.monta import raccordi_riquadro
    from tools.reel.parser import parse_testo

    testo = """---
titolo: Prova
slug: prova
data_creazione: 2026-09-22
stato: animato
formato: reel
tipo: pillola
pilastro: come funziona
messaggio_centrale: Una prova.
---

# Prova

## Scena 1 [hook, durata=5s]
TITOLO: Uno
SOTTOTITOLO: Due
VOCE: Prima riga.

## Scena 2 [spiegazione, durata=10s]
VOCE: Seconda riga.
ANIMAZIONE: qualcosa

## Scena 3 [spiegazione, durata=10s]
RIQUADRO: no
VOCE: Terza riga.
ANIMAZIONE: qualcosa

## Scena 4 [chiusura, durata=5s]
MESSAGGIO: Tre
CTA: Quattro
VOCE: Quarta riga.
"""
    r, _ = parse_testo(testo)
    assert raccordi_riquadro(r, r.scene[0]) == (None, "si")      # l'apertura si rimpicciolisce nella scena 2
    assert raccordi_riquadro(r, r.scene[1]) == (None, None)      # non è a volto pieno: niente raccordo
    assert raccordi_riquadro(r, r.scene[3]) == (None, None)      # prima della chiusura c'è una scena senza riquadro
