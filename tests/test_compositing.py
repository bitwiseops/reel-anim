"""I comandi ffmpeg costruiti come liste di stringhe (senza eseguirli): filtergraph, posizioni, codifica, concat."""
from pathlib import Path

from tools.anim.config import carica
from tools.reel.compositing import Sorgenti, comando_concat, comando_scena, durata_concat, posizione_riquadro

GRAFICA = Path("/tmp/grafica.mp4")
DEST = Path("/tmp/scena.mp4")


def _filtri(cmd: list[str]) -> str:
    return cmd[cmd.index("-filter_complex") + 1]


def test_posizioni_del_riquadro():
    cfg = carica()
    assert posizione_riquadro(cfg, "si") == posizione_riquadro(cfg, "basso-destra") == (576, 1220, 360)
    assert posizione_riquadro(cfg, "basso-sinistra") == (84, 1220, 360)
    assert posizione_riquadro(cfg, "alto-destra") == (576, 220, 360)
    assert posizione_riquadro(cfg, "alto-sinistra") == (84, 220, 360)


def test_scena_senza_riquadro_con_voce_sintetica_in_anteprima():
    cmd = comando_scena(Sorgenti(GRAFICA, 4.0, "no", audio=Path("/tmp/voce.m4a")), DEST, anteprima=True)
    f = _filtri(cmd)
    assert "scale=1080:1920" in f and "alphamerge" not in f and "aresample=48000,apad[a]" in f
    assert cmd[cmd.index("-t") + 1] == "4.000" and "ultrafast" in cmd
    assert cmd[cmd.index("-ac") + 1] == "2"   # stereo anche con la voce mono


def test_scena_con_avatar_nel_riquadro():
    cmd = comando_scena(Sorgenti(GRAFICA, 5.0, "alto-destra", avatar=Path("/tmp/avatar.png")), DEST)
    f = _filtri(cmd)
    assert "alphamerge" in f and "crop=360:360" in f and "overlay=x=576:y=220" in f
    assert "anullsrc=r=48000:cl=stereo" in cmd and cmd[cmd.index("-crf") + 1] == "18"


def test_scena_con_la_clip_del_presentatore():
    f = _filtri(comando_scena(Sorgenti(GRAFICA, 5.0, "si", video_presentatore=Path("/tmp/scena-02.mov")), DEST))
    assert "loudnorm=I=-16" in f and "overlay=x=576:y=1220" in f


def test_scena_schermo_con_broll():
    sc = carica().dati["schermo"]
    cmd = comando_scena(Sorgenti(Path("/tmp/grafica.mov"), 6.0, "alto-destra", avatar=Path("/tmp/avatar.png"),
                                 schermo=Path("/tmp/chat.png")), DEST)
    f = _filtri(cmd)
    assert f"crop={sc['larghezza']}:{sc['altezza']}" in f and f"overlay=x={sc['x']}:y={sc['y']}" in f
    assert "format=rgba[gr]" in f and any(a.startswith("color=c=") for a in cmd)


def test_concat_con_dissolvenza_e_con_taglio():
    pezzi = [(Path("/tmp/1.mp4"), 4.0), (Path("/tmp/2.mp4"), 8.0), (Path("/tmp/3.mp4"), 6.0)]
    f = _filtri(comando_concat(pezzi, Path("/tmp/reel.mp4"), "dissolvenza", 0.25))
    assert "offset=3.750" in f and "offset=11.500" in f and f.count("acrossfade") == 2
    assert durata_concat(pezzi, "dissolvenza", 0.25) == 17.5
    assert "concat=n=3:v=1:a=1" in _filtri(comando_concat(pezzi, Path("/tmp/reel.mp4"), "taglio"))
    cmd = comando_concat(pezzi, Path("/tmp/reel.mp4"), "dissolvenza", 0.25)
    assert cmd[cmd.index("-ac") + 1] == "2"
    assert durata_concat(pezzi, "taglio", 0.25) == 18.0
