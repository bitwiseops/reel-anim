"""Registrazione guidata: timeline dal report, karaoke, comandi ffmpeg, prese e spezzatura (senza webcam)."""
import json
import shutil
import subprocess
import time
from pathlib import Path

import pytest

from tools.anim.config import carica
from tools.reel import clip as clipmod
from tools.reel import registra as reg
from tools.reel.ffmpeg import ffprobe, trova_ffmpeg
from tools.reel.parser import parse, parse_testo
from tools.reel.percorsi import impronta

MD = ("---\ntitolo: T\nslug: prova-registra\nformato: reel\nmessaggio_centrale: M\n---\n\n"
      "## Scena 1 [hook]\nTITOLO: T\nVOCE: L'IA scrive quello che ti aspetti?\nVOCE: Non è creativa.\nVOCE: Vuol dire ==probabile==.\n\n"
      "## Scena 2 [spiegazione]\nVOCE: Prima frase della due.\nVOCE: Seconda frase.\nVOCE: Terza, più lunga, con molte parole dentro.\n\n"
      "## Scena 3 [chiusura]\nMESSAGGIO: M\nVOCE: Scrivilo nella richiesta.\nVOCE: Fine.\n")

# i numeri sono quelli del report vero di generativa-non-creativa (scene 1-2) più una chiusura
REPORT = {"prova": True, "hash_md": "abcdef0123456789", "cartella": "/tmp/render",
          "elementi": [
              {"scena": 1, "tipo_scena": "hook", "durata_s": 6.142, "inizi_frasi_s": [0.0, 2.155, 4.391], "t_inizio_s": 0.0, "t_fine_s": 6.14, "riquadro": "no"},
              {"scena": 2, "tipo_scena": "spiegazione", "durata_s": 8.717, "inizi_frasi_s": [0.0, 2.138, 5.667], "t_inizio_s": 5.89, "t_fine_s": 14.61, "riquadro": "si"},
              {"scena": 3, "tipo_scena": "chiusura", "durata_s": 7.25, "inizi_frasi_s": [0.0, 3.0], "t_inizio_s": 14.36, "t_fine_s": 21.61, "riquadro": "si"}],
          "reel": {"file": "reel-9x16.mp4", "durata_s": 21.61, "fps": 30}}


def _timeline() -> reg.Timeline:
    r, _ = parse_testo(MD)
    return reg.timeline_da_report(REPORT, r, carica())


def test_timeline_dal_report():
    tl = _timeline()
    assert [s.n for s in tl.scene] == [1, 2, 3] and tl.durata_s == 21.61 and tl.sovrapposizione_s == 0.25
    s1, s2 = tl.scene[0], tl.scene[1]
    assert s1.riquadro == "no" and s2.riquadro == "si"
    assert [f.testo for f in s1.frasi][2] == "Vuol dire probabile." and s1.frasi[2].parole == ("Vuol", "dire", "probabile.")
    assert (s1.frasi[0].t_inizio_s, s1.frasi[0].t_fine_s) == (0.0, 1.855)          # fine = frase dopo − pausa 0,3
    assert s1.frasi[2].t_fine_s == 5.642                                            # ultima: fine scena − coda 0,5
    assert s2.frasi[0].t_inizio_s == 5.89 and s2.frasi[1].t_inizio_s == pytest.approx(8.028)
    assert tl.scena_a(-1.0) is None and tl.scena_a(3.0) is s1 and tl.scena_a(21.61) is None
    assert tl.scena_a(5.95) is s2       # nella sovrapposizione vince la scena che comincia
    assert tl.indice(3) == 2 and tl.scena_n(2) is s2 and len(tl.frasi) == 8


def test_timeline_rifiuta_report_non_pronto(tmp_path):
    r, _ = parse_testo(MD)
    cfg = carica()
    with pytest.raises(reg.ReportNonPronto):
        reg.timeline_da_report({**REPORT, "prova": False}, r, cfg)
    with pytest.raises(reg.ReportNonPronto):
        reg.timeline_da_report({**REPORT, "reel": None}, r, cfg)
    with pytest.raises(reg.ReportNonPronto):
        reg.timeline_da_report({**REPORT, "elementi": REPORT["elementi"][:2]}, r, cfg)
    with pytest.raises(reg.ReportNonPronto):
        reg.carica_timeline(r, tmp_path, cfg)          # manca report.json
    # anteprima di una sceneggiatura precedente: avviso, non errore
    md = tmp_path / "prova-registra.md"
    md.write_text(MD, encoding="utf-8")
    r2, _ = parse(md)
    (tmp_path / "reel-9x16.mp4").write_bytes(b"")
    (tmp_path / "report.json").write_text(json.dumps({**REPORT, "cartella": str(tmp_path)}), encoding="utf-8")
    tl, diag = reg.carica_timeline(r2, tmp_path, cfg)
    assert tl.reel == tmp_path / "reel-9x16.mp4" and len(diag) == 1 and "versione precedente" in diag[0].msg
    (tmp_path / "report.json").write_text(json.dumps({**REPORT, "cartella": str(tmp_path), "hash_md": impronta(md)}))
    assert reg.carica_timeline(r2, tmp_path, cfg)[1] == []
    # dopo il montaggio con le clip vere report.json non è più --prova: vale la copia stabile report-prova.json
    (tmp_path / "report.json").write_text(json.dumps({**REPORT, "prova": False, "cartella": str(tmp_path)}))
    with pytest.raises(reg.ReportNonPronto):
        reg.carica_timeline(r2, tmp_path, cfg)
    (tmp_path / "reel-prova.mp4").write_bytes(b"")
    (tmp_path / "report-prova.json").write_text(json.dumps({**REPORT, "cartella": str(tmp_path), "hash_md": impronta(md),
                                                            "reel": {**REPORT["reel"], "file": "reel-prova.mp4"}}))
    tl, diag = reg.carica_timeline(r2, tmp_path, cfg)
    assert tl.reel.name == "reel-prova.mp4" and diag == []


def test_karaoke():
    tl = _timeline()
    k = reg.karaoke(tl, -1.5)                    # pre-roll prima del reel
    assert k.scena is None and k.frase is None and k.prossima is tl.scene[0].frasi[0] and k.attesa_s == 1.5
    accese = [reg.karaoke(tl, t / 100).accese for t in range(0, 186)]
    assert accese == sorted(accese) and accese[0] == 0 and accese[-1] == 5 and reg.karaoke(tl, 0.5).frase is tl.scene[0].frasi[0]
    assert reg.parole_accese(tl.scene[0].frasi[0], 1.855) == 6 and reg.parole_accese(tl.scene[0].frasi[0], 0.0) == 0
    k = reg.karaoke(tl, 5.75)                    # tra l'ultima frase della 1 e la prima della 2
    assert k.frase is None and k.precedente is tl.scene[0].frasi[2] and k.prossima is tl.scene[1].frasi[0]
    assert k.attesa_s == pytest.approx(0.14) and k.scena is tl.scene[0]
    k = reg.karaoke(tl, 6.0)
    assert k.scena is tl.scene[1] and k.frase is tl.scene[1].frasi[0] and 0 < k.frazione_scena < 0.05
    assert reg.karaoke(tl, 21.5).prossima is None and reg.karaoke(tl, 21.5).attesa_s == 0


def test_comando_cattura_doppia_uscita(tmp_path, monkeypatch):
    monkeypatch.setattr(reg, "DISPOSITIVI_SCELTI", tmp_path / "dispositivi.json")
    opz = reg.opzioni(carica(), video="1", audio=None)
    cmd = reg.comando_cattura(opz, Path("/tmp/_prese/presa-01.mov"), (480, 270))
    assert cmd[cmd.index("-i") + 1] == "1" and "avfoundation" in cmd and cmd[cmd.index("-pixel_format") + 1] == "nv12"
    f = cmd[cmd.index("-filter_complex") + 1]
    assert f.startswith("[0:v]fps=30,split=2") and "scale=480:270" in f
    assert "h264_videotoolbox" in cmd and "-an" in cmd and "pcm_s16le" not in cmd and cmd[cmd.index("mov") - 1] == "-f"
    assert cmd.count("passthrough") == 2 and cmd[-1] == "pipe:1" and cmd.count("-map") == 2   # l'audio lo registra PortAudio
    solo = reg.comando_cattura(opz, None, (480, 270))
    assert solo[solo.index("-i") + 1] == "1" and "-an" not in solo and solo.count("-map") == 1 and "mov" not in solo
    lavfi = reg.comando_cattura({**opz, "codec": "libx264"}, Path("/tmp/p.mov"), (160, 90), sorgente=["-f", "lavfi", "-i", "testsrc"])
    assert "avfoundation" not in lavfi and "libx264" in lavfi and "-realtime" not in lavfi and "ultrafast" in lavfi


def test_comando_riproduzione_e_taglio():
    tl = _timeline()
    opz = reg.opzioni(carica())
    assert reg.snap_fotogramma(-2.0, 30) == 0.0 and reg.snap_fotogramma(3.89, 30) == pytest.approx(116 / 30)
    cmd = reg.comando_riproduzione(tl.reel, reg.snap_fotogramma(3.89, 30), (405, 720))
    assert cmd[cmd.index("-ss") + 1] == "3.867" and "-an" in cmd and "scale=405:720" in cmd and cmd[-1] == "pipe:1"
    p = reg.nuova_presa("presa-01", 1, -2.0, 90, 0.0, opz, 22.0, "abc", n0=48000, latenza_audio_s=0.02,
                        inquadratura={"x": 420, "y": 0, "lato": 1080})
    assert p.t_file(0.0) == pytest.approx(3.0 + 0.1 + 2.0) and p.file == "_prese/presa-01.mov" and p.audio == "_prese/presa-01.wav"
    assert p.t_audio(0.0) == pytest.approx(1.0 + 0.02 + 2.0)
    wav = Path("/tmp/p.wav")
    c1 = reg.comando_taglio(p, tl.scene[0], Path("/tmp/p.mov"), Path("/tmp/scena-01.mov"), opz, wav)
    c2 = reg.comando_taglio(p, tl.scene[1], Path("/tmp/p.mov"), Path("/tmp/scena-02.mov"), opz, wav)
    ss = [float(c1[i + 1]) for i, a in enumerate(c1) if a == "-ss"]
    assert ss == [pytest.approx(5.1), pytest.approx(3.02)] and c1[c1.index("-ss", c1.index("-ss") + 1) + 3] == str(wav)
    ss2 = float(c2[c2.index("-ss") + 1])
    assert ss2 - ss[0] == pytest.approx(6.142 - 0.25, abs=0.01)   # le clip adiacenti condividono la dissolvenza
    assert c1[c1.index("-t") + 1] == "6.133" and float(c1[c1.index("-t") + 1]) * 30 == pytest.approx(184, abs=0.01)
    assert c1[c1.index("-map") + 1] == "0:v" and "1:a" in c1 and c1[c1.index("-vf") + 1] == "crop=1080:1080:420:0"
    assert "loudnorm" not in " ".join(c1) and "pcm_s16le" in c1 and c1[-1] == "/tmp/scena-01.mov"
    vecchia = reg.nuova_presa("presa-00", 1, -2.0, 90, 0.0, opz, 22.0, "abc", con_audio=False)   # audio dentro il mov, niente ritaglio
    c0 = reg.comando_taglio(vecchia, tl.scene[0], Path("/tmp/p.mov"), Path("/tmp/s.mov"), opz)
    assert "0:a" in c0 and "-vf" not in c0 and c0.count("-ss") == 1


def test_scene_coperte():
    tl = _timeline()
    opz = reg.opzioni(carica())
    da2 = reg.nuova_presa("presa-01", 2, 3.89, 0, 0.0, opz, 15.0, "abc")
    assert [s.n for s in reg.scene_coperte(tl, da2)] == [2]
    assert [s.n for s in reg.scene_coperte(tl, reg.nuova_presa("p", 2, 3.89, 0, 0.0, opz, 21.61, "abc"))] == [2, 3]
    assert [s.n for s in reg.scene_coperte(tl, reg.nuova_presa("p", 1, -2.0, 0, 0.0, opz, 22.0, "abc"))] == [1, 2, 3]
    assert reg.scene_coperte(tl, reg.nuova_presa("p", 3, 12.36, 0, 0.0, opz, 20.0, "abc")) == []


STDERR_DISPOSITIVI = """[AVFoundation indev @ 0x12] AVFoundation video devices:
[AVFoundation indev @ 0x12] [0] Fotocamera di MacBook Pro
[AVFoundation indev @ 0x12] [1] OBS Virtual Camera
[AVFoundation indev @ 0x12] [2] Capture screen 0
[AVFoundation indev @ 0x12] AVFoundation audio devices:
[AVFoundation indev @ 0x12] [0] Microfono MacBook Pro
: Input/output error
"""


def test_dispositivi():
    video, audio = reg.dispositivi(STDERR_DISPOSITIVI)
    assert video == [(0, "Fotocamera di MacBook Pro"), (1, "OBS Virtual Camera"), (2, "Capture screen 0")]
    assert audio == [(0, "Microfono MacBook Pro")]
    assert reg.indice_dispositivo("OBS", video) == 1 and reg.indice_dispositivo("2", video) == 2 and reg.indice_dispositivo(0, video) == 0
    with pytest.raises(ValueError):
        reg.indice_dispositivo("iPhone", video)


def test_dispositivi_scelti(tmp_path, monkeypatch):
    monkeypatch.setattr(reg, "DISPOSITIVI_SCELTI", tmp_path / "dispositivi.json")
    cfg = carica()
    assert reg.dispositivi_scelti() == {} and reg.opzioni(cfg)["audio"] is None
    reg.salva_dispositivi_scelti({"video": "OBS Virtual Camera"})
    reg.salva_dispositivi_scelti({"audio": "Microfono MacBook Pro"})
    assert reg.dispositivi_scelti() == {"video": "OBS Virtual Camera", "audio": "Microfono MacBook Pro"}
    o = reg.opzioni(cfg)
    assert o["video"] == "OBS Virtual Camera" and o["audio"] == "Microfono MacBook Pro"
    assert reg.opzioni(cfg, video=2)["video"] == 2                      # la riga di comando vince
    reg.salva_dispositivi_scelti({"audio": ""})                          # «predefinito»: si toglie la scelta
    assert reg.opzioni(cfg)["audio"] is None
    video, _ = reg.dispositivi(STDERR_DISPOSITIVI)
    assert reg.indice_dispositivo("OBS Virtual Camera", video) == 1


def test_riquadro_in_scala_e_dimensioni_pipe(tmp_path, monkeypatch):
    monkeypatch.setattr(reg, "DISPOSITIVI_SCELTI", tmp_path / "dispositivi.json")
    cfg = carica()
    assert reg.riquadro_in_scala(cfg, "si", 0.375) == (216, 82, 135)   # «si» = alto-destra
    assert reg.dimensioni_pipe("1920x1080", 480) == (480, 270) and reg.dimensioni_pipe("1080x1920", 405) == (404, 720)
    o = reg.opzioni(cfg)
    assert o["fps"] == 30 and o["latenza_s"] == 0.10 and o["video"] == 0 and o["audio"] is None


def test_inquadratura(tmp_path):
    assert reg.inquadratura_default("1920x1080") == {"x": 420, "y": 0, "lato": 1080}
    lim = lambda q: reg.limita_inquadratura(q, "1920x1080", 360)   # noqa: E731
    assert lim({"x": 1500, "y": 500, "lato": 600}) == {"x": 1320, "y": 480, "lato": 600}
    assert lim({"x": -5, "y": -5, "lato": 100}) == {"x": 0, "y": 0, "lato": 360}       # mai sotto il riquadro
    assert lim({"x": 0, "y": 0, "lato": 5000}) == {"x": 0, "y": 0, "lato": 1080}
    assert reg.carica_inquadratura(tmp_path, "1920x1080", 360) == {"x": 420, "y": 0, "lato": 1080}
    reg.salva_inquadratura(tmp_path, {"x": 600, "y": 100, "lato": 720})
    assert reg.carica_inquadratura(tmp_path, "1920x1080", 360) == {"x": 600, "y": 100, "lato": 720}
    (tmp_path / "inquadratura.json").write_text("rotto")
    assert reg.carica_inquadratura(tmp_path, "1920x1080", 360)["lato"] == 1080


def test_parlato_corretto_in_registrazione(tmp_path, monkeypatch):
    """Il testo cambiato nella finestra (parlato.json) sostituisce la VOCE nel karaoke e finisce nel sidecar; i tempi
    restano quelli dell'anteprima. Una correzione con un altro numero di righe non vale."""
    r, _ = parse_testo(MD)
    cfg = carica()
    tl = reg.timeline_da_report(REPORT, r, cfg, {2: ["Uno ==nuovo==.", "Due.", "Tre."], 3: ["solo una riga"]})
    s2 = tl.scena_n(2)
    assert [f.testo for f in s2.frasi] == ["Uno nuovo.", "Due.", "Tre."] and s2.frasi[0].grezzo == "Uno ==nuovo==."
    assert s2.frasi[1].t_inizio_s == _timeline().scena_n(2).frasi[1].t_inizio_s
    assert [f.testo for f in tl.scena_n(3).frasi] == ["Scrivilo nella richiesta.", "Fine."]
    tl2 = reg.con_voce(_timeline(), 3, ["Scrivilo tu.", "Basta."])
    assert [f.grezzo for f in tl2.scena_n(3).frasi] == ["Scrivilo tu.", "Basta."] and tl2.scena_n(2) == _timeline().scena_n(2)
    with pytest.raises(ValueError):
        reg.con_voce(_timeline(), 3, ["una sola"])
    p = reg.nuova_presa("presa-01", 2, 3.89, 12, 0.02, reg.opzioni(cfg), 21.61, "abc")
    d = json.loads(reg.scrivi_sidecar(tmp_path / "scena-02.mov", s2, p).read_text())
    assert d["voce"] == ["Uno ==nuovo==.", "Due.", "Tre."]
    (tmp_path / "scena-02.mov").write_bytes(b"")
    assert clipmod.voce_presa(tmp_path / "scena-02.mov") == d["voce"] and clipmod.voce_presa(None) is None
    monkeypatch.setattr(clipmod, "RADICE", tmp_path)
    clipmod.salva_parlato("x", 4, ["a", "b"])
    clipmod.salva_parlato("x", 2, ["c"])
    assert clipmod.carica_parlato("x") == {2: ["c"], 4: ["a", "b"]}
    clipmod.salva_parlato("x", 4, None)
    assert clipmod.carica_parlato("x") == {2: ["c"]} and clipmod.carica_parlato("y") == {}


def test_caption_dal_testo_recitato(tmp_path, monkeypatch):
    """In ordine: la voce del sidecar (presa), parlato.json, la VOCE del .md."""
    from tools.reel import monta
    r, _ = parse_testo(MD)
    s = r.scene[1]
    media = tmp_path / "contenuti" / "media" / r.slug
    media.mkdir(parents=True)
    monkeypatch.setattr(clipmod, "RADICE", tmp_path)
    presa = monta.TempiScena(8.0, "clip", None, [0.0, 2.1, 5.6], "presa")
    stima = monta.TempiScena(8.0, "stima", None, [0.0, 2.1, 5.6], "parole-stima")
    assert monta.voce_recitata(r, s, stima) == s.voce
    clipmod.salva_parlato(r.slug, 2, ["P1.", "P2.", "P3."])
    assert monta.voce_recitata(r, s, stima) == ["P1.", "P2.", "P3."]
    (media / "scena-02.mov").write_bytes(b"")
    (media / "scena-02.json").write_text(json.dumps({"inizi_frasi_s": [0.0, 2.1, 5.6], "voce": ["S1.", "S2.", "S3."]}))
    assert monta.voce_recitata(r, s, presa) == ["S1.", "S2.", "S3."]
    assert monta._voce_report(r, s, presa)["voce_cambiata"] is True
    (media / "scena-02.json").write_text(json.dumps({"inizi_frasi_s": [0.0, 2.1, 5.6]}))    # presa di prima: niente voce
    assert monta.voce_recitata(r, s, presa) == ["P1.", "P2.", "P3."]


def test_sidecar_e_registro(tmp_path):
    tl = _timeline()
    opz = reg.opzioni(carica())
    assert reg.prossima_presa(tmp_path) == "presa-01"
    p = reg.nuova_presa("presa-01", 2, 3.89, 12, 0.02, opz, 21.61, "abc")
    side = reg.scrivi_sidecar(tmp_path / "scena-02.mov", tl.scene[1], p)
    d = json.loads(side.read_text())
    assert side.name == "scena-02.json" and d["inizi_frasi_s"] == [0.0, 2.138, 5.667] and d["origine_tempi"] == "presa"
    assert d["t_presa_s"] == pytest.approx(0.02 + 12 / 30 + 0.1 + 2.0, abs=0.001)
    assert clipmod.tempi_presa(tmp_path / "scena-02.mov") == [0.0, 2.138, 5.667] and clipmod.tempi_presa(tmp_path / "x.mov") is None
    p.scene = [2, 3]
    reg.aggiorna_registro(tmp_path, p)
    assert reg.registro(tmp_path)[0]["scene"] == [2, 3] and reg.presa_dal_registro(tmp_path, "presa-01").k0 == 12
    reg.aggiorna_registro(tmp_path, p)      # stessa presa: sostituita, non duplicata
    assert len(reg.registro(tmp_path)) == 1 and reg.prossima_presa(tmp_path) == "presa-02"
    (tmp_path / "_prese" / "presa-05.mov").write_bytes(b"")
    assert reg.prossima_presa(tmp_path) == "presa-06"


def test_tempi_scena_con_sidecar(tmp_path, monkeypatch):
    from tools.reel import monta
    r, _ = parse_testo(MD)
    media = tmp_path / "contenuti" / "media" / r.slug
    media.mkdir(parents=True)
    (media / "scena-02.mov").write_bytes(b"")
    monkeypatch.setattr(clipmod, "RADICE", tmp_path)
    monkeypatch.setattr(monta, "ffprobe", lambda p: {"durata_s": 8.0})
    (media / "scena-02.json").write_text(json.dumps({"inizi_frasi_s": [0.0, 2.1, 5.6], "origine_tempi": "presa"}))
    t = monta.tempi_scena(r, r.scene[1])
    assert (t.durata_s, t.origine, t.origine_tempi, t.inizi_frasi_s) == (8.0, "clip", "presa", [0.0, 2.1, 5.6])
    assert monta.tempi_scena(r, r.scene[1], ignora_clip=True).origine == "stima"       # --prova non guarda le clip
    (media / "scena-02.json").write_text(json.dumps({"inizi_frasi_s": [0.0, 2.1]}))     # frasi cambiate: si torna alla stima
    assert monta.tempi_scena(r, r.scene[1]).origine_tempi == "parole-clip"
    assert clipmod.stato(r.slug, [1, 2])[1]["tempi"] == "presa" and clipmod.stato(r.slug, [1])[0]["presente"] is False


# --- lenti: ffmpeg vero, sorgente lavfi al posto della webcam -----------------------------------------

LAVFI = ["-re", "-f", "lavfi", "-i", "testsrc=size=320x240:rate=30"]


def _opz_test() -> dict:
    # il microfono predefinito, non quello salvato sulla macchina (può non essere collegato)
    return {**reg.opzioni(carica()), "audio": None, "codec": "libx264", "bitrate": "1M", "risoluzione": "320x240"}


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="serve ffmpeg")
def test_spezza_presa_lavfi(tmp_path):
    ff, _ = trova_ffmpeg()
    presa = tmp_path / reg.PRESE / "presa-01.mov"
    presa.parent.mkdir()
    subprocess.run([ff, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=red:s=320x240:r=30:d=12", "-c:v", "libx264",
                    "-pix_fmt", "yuv420p", "-an", str(presa)], check=True)
    subprocess.run([ff, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=14",
                    "-c:a", "pcm_s16le", str(presa.with_suffix(".wav"))], check=True)
    f = lambda testo, a, b: reg.Frase(testo, tuple(testo.split()), a, b)   # noqa: E731
    tl = reg.Timeline((reg.ScenaTL(1, "hook", 0.0, 5.0, "no", (f("Ciao a tutti.", 0.0, 4.5),)),
                       reg.ScenaTL(2, "chiusura", 4.75, 4.0, "si", (f("Fine.", 4.75, 6.0), f("Davvero.", 6.5, 8.25)))),
                      8.75, 30, tmp_path / "reel.mp4", "abc", 0.25)
    p = reg.nuova_presa("presa-01", 1, 0.0, 0, 0.0, {**_opz_test(), "latenza_s": 0.0}, 12.0, "abc", n0=48000,
                        inquadratura={"x": 40, "y": 0, "lato": 240})
    chiamate = []
    fatte = reg.spezza(tl, p, tmp_path, _opz_test(), avanzamento=lambda i, n, s: chiamate.append((i, n, s.n)))
    assert [x.name for x in fatte] == ["scena-01.mov", "scena-02.mov"] and chiamate == [(0, 2, 1), (1, 2, 2)]
    p1, p2 = ffprobe(fatte[0]), ffprobe(fatte[1])
    assert abs(p1["durata_s"] - 5.0) < 0.05 and abs(p2["durata_s"] - 4.0) < 0.05 and p2["audio"] == "pcm_s16le" and p2["audio_hz"] == 48000
    assert (p1["larghezza"], p1["altezza"]) == (240, 240)     # ritagliata sull'inquadratura
    assert json.loads((tmp_path / "scena-02.json").read_text())["inizi_frasi_s"] == [0.0, 1.75]
    assert reg.registro(tmp_path)[0]["scene"] == [1, 2] and p.scene == [1, 2]


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="serve ffmpeg")
def test_cattura_lavfi_file_e_pipe_allineati(tmp_path):
    from tools.reel.cattura import Cattura, Riproduttore
    opz = _opz_test()
    presa = tmp_path / "presa-01.mov"
    c = Cattura(reg.comando_cattura(opz, presa, (160, 120), sorgente=LAVFI), (160, 120), tmp_path / "presa-01.log")
    c.avvia()
    t0 = time.monotonic()
    while c.k < 1 and time.monotonic() - t0 < 10:
        time.sleep(0.05)
    assert c.k >= 1 and c.vivo()
    time.sleep(1.5)
    k, rgb = c.ultimo()
    assert len(rgb) == 160 * 120 * 3 and k >= 30
    assert c.ferma() == 0, c.errore()      # `q` chiude il file con il moov
    pr = ffprobe(presa)
    assert pr["codec"] == "h264" and pr["audio"] is None and pr["durata_s"] > 1.0
    assert pr["fotogrammi"] == c.k         # file e pipe hanno ricevuto gli stessi fotogrammi
    assert pr["inizio_video_s"] >= 0
    # la presa si rilegge come un reel: il fotogramma k è l'istante t0 + k/fps
    rp = Riproduttore(reg.comando_riproduzione(presa, 0.5, (80, 60)), (80, 60), 0.5, 30)
    rp.avvia()
    time.sleep(0.5)
    assert rp.prossimo_fino_a(0.4) is None
    fr = rp.prossimo_fino_a(0.6)
    assert fr is not None and len(fr) == 80 * 60 * 3
    rp.ferma()


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="serve ffmpeg")
def test_app_modifica_il_testo_fuori_dalla_presa(tmp_path, monkeypatch):
    """E apre la modifica: Spazio e le cifre non fanno niente, un numero di righe sbagliato non si salva, il
    salvataggio aggiorna la timeline e parlato.json; Esc annulla."""
    import tkinter as tk
    from tools.reel.registra_app import AppRegistra
    try:
        tk.Tk().destroy()
    except tk.TclError:
        pytest.skip("Tk senza schermo")
    monkeypatch.setattr(clipmod, "RADICE", tmp_path)
    r, _ = parse_testo(MD)
    tl = _timeline()
    render, media = tmp_path / "render", tmp_path / "media"
    render.mkdir()
    media.mkdir()
    app = AppRegistra(r, tl, {**_opz_test(), "sorgente": LAVFI}, carica(), media, render, [], da_scena=2)
    app.root.withdraw()
    evento = type("E", (), {"char": "e"})()
    app._tasto(evento)
    assert app.stato == "modifica" and app.t_karaoke.get("1.0", "end").strip().split("\n")[0] == "Prima frase della due."
    app._spazio()
    app._tasto(type("E", (), {"char": "3"})())
    assert app.stato == "modifica" and app.da_scena == 2 and app.cattura is None     # niente presa, niente cambio scena
    app.t_karaoke.delete("1.0", "end")
    app.t_karaoke.insert("1.0", "Solo una riga.")
    app._salva_modifica()
    assert app.stato == "modifica" and "servono 3 righe" in app.messaggio
    app.t_karaoke.delete("1.0", "end")
    app.t_karaoke.insert("1.0", "Prima ==nuova==.\n\nSeconda.\nTerza.\n")
    app._salva_modifica()
    assert app.stato == "pronto" and [f.testo for f in app.tl.scena_n(2).frasi] == ["Prima nuova.", "Seconda.", "Terza."]
    assert clipmod.carica_parlato(r.slug) == {2: ["Prima ==nuova==.", "Seconda.", "Terza."]}
    app._tasto(evento)
    app.t_karaoke.insert("1.0", "rovinata ")
    app._esc()
    assert app.stato == "pronto" and app.tl.scena_n(2).frasi[0].grezzo == "Prima ==nuova==."
    app._chiudi()


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="serve ffmpeg")
def test_app_presa_completa_senza_webcam(tmp_path):
    """La finestra (nascosta) con una sorgente lavfi al posto della webcam: presa dall'inizio alla fine del reel, poi le
    clip tagliate con i sidecar. Serve uno schermo: senza Tk si salta."""
    import tkinter as tk
    from tools.reel.registra_app import AppRegistra
    try:
        tk.Tk().destroy()
    except tk.TclError:
        pytest.skip("Tk senza schermo")
    sd = pytest.importorskip("sounddevice")
    try:
        sd.query_devices(kind="input")
    except Exception:  # noqa: BLE001
        pytest.skip("nessun microfono")
    ff, _ = trova_ffmpeg()
    render, media = tmp_path / "render", tmp_path / "media"
    (render / "scene").mkdir(parents=True)
    media.mkdir()
    reel = render / "reel-9x16.mp4"
    subprocess.run([ff, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "testsrc=size=1080x1920:rate=30:d=4", "-c:v", "libx264",
                    "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(reel)], check=True)
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(reel), "-frames:v", "1", str(render / "scene" / "01.png")], check=True)
    r, _ = parse_testo("---\ntitolo: T\nslug: prova-app\nformato: reel\nmessaggio_centrale: M\n---\n\n"
                       "## Scena 1 [hook]\nTITOLO: T\nVOCE: Prima.\n\n## Scena 2 [chiusura]\nMESSAGGIO: M\nVOCE: Seconda.\nVOCE: Terza.\n")
    report = {"prova": True, "hash_md": "x", "cartella": str(render), "reel": {"file": "reel-9x16.mp4", "durata_s": 4.0, "fps": 30},
              "elementi": [{"scena": 1, "durata_s": 2.0, "inizi_frasi_s": [0.0], "t_inizio_s": 0.0, "riquadro": "no"},
                           {"scena": 2, "durata_s": 2.25, "inizi_frasi_s": [0.0, 1.0], "t_inizio_s": 1.75, "riquadro": "si"}]}
    cfg = carica()
    tl = reg.timeline_da_report(report, r, cfg)
    opz = {**_opz_test(), "sorgente": LAVFI, "conto_alla_rovescia_s": 1, "preroll_s": 0.5, "coda_presa_s": 0.2, "timeout_apertura_s": 15}
    app = AppRegistra(r, tl, opz, cfg, media, render, [])
    app.lato_minimo = 120      # la cattura di prova è 320x240: sotto il riquadro vero (360), che vieterebbe lo zoom
    app._zoom(-1)      # come farebbe il presentatore: un po' di zoom, poi lo spostamento a destra
    app._tasto(type("E", (), {"char": "d"})())
    assert app.inq["lato"] < 240 and app.inq["x"] > 40
    app.root.withdraw()
    esito: dict = {"stati": set()}
    t0 = time.monotonic()

    def passo():   # al posto del presentatore: Spazio appena la fotocamera dà un fotogramma, poi si aspetta la fine
        if "avviato" not in esito and app.stato == "pronto" and app.anteprima and app.anteprima.k >= 1:
            esito["avviato"] = True
            app._spazio()
        if "avviato" in esito:
            esito["stati"].add(app.stato)
        if (app.stato == "pronto" and app.prese_fatte) or app.stato == "errore" or time.monotonic() - t0 > 60:
            esito["stato"], esito["messaggio"] = app.stato, app.messaggio
            esito["anteprima_viva"] = bool(app.anteprima and app.anteprima.vivo())
            app._chiudi()
            return
        app.root.after(50, passo)

    app.root.after(200, passo)
    app.esegui()
    assert esito.get("stato") == "pronto", esito.get("messaggio")
    assert {"apertura", "conto", "presa", "spezzo"} <= esito["stati"]
    p = app.prese_fatte[0]
    assert p.nome == "presa-01" and p.scene == [1, 2] and p.da_scena == 1 and p.t_reel0_s == -0.5 and p.k0 >= 1
    assert p.t_reel_stop_s >= 4.2 and (media / "_prese" / "presa-01.mov").exists()
    wav = ffprobe(media / "_prese" / "presa-01.wav")
    assert wav["audio"] == "pcm_s16le" and abs(wav["durata_s"] - (p.t_reel_stop_s - p.t_reel0_s + p.n0 / 48000)) < 0.5
    assert p.n0 > 0 and p.latenza_audio_s > 0 and p.inquadratura == app.inq and p.inquadratura["lato"] < 240
    for n, d in ((1, 2.0), (2, 2.25)):
        pr = ffprobe(media / f"scena-{n:02d}.mov")
        assert abs(pr["durata_s"] - d) < 0.05 and pr["audio"] == "pcm_s16le" and pr["larghezza"] == app.inq["lato"]
    assert json.loads((media / "scena-02.json").read_text())["inizi_frasi_s"] == [0.0, 1.0]
    assert esito["anteprima_viva"]     # dopo la presa riparte l'anteprima


def test_a_volto_pieno_la_clip_tiene_il_fotogramma_intero():
    """Apertura e chiusura (dal 2026-09-21): la tela è il presentatore, niente quadrato dell'inquadratura."""
    from dataclasses import replace
    tl = _timeline()
    opz = reg.opzioni(carica())
    p = reg.nuova_presa("presa-01", 1, -2.0, 90, 0.0, opz, 22.0, "abc", inquadratura={"x": 0, "y": 420, "lato": 1080})
    normale = reg.comando_taglio(p, tl.scene[0], Path("/tmp/p.mov"), Path("/tmp/a.mov"), opz, Path("/tmp/p.wav"))
    pieno = reg.comando_taglio(p, replace(tl.scene[0], riquadro="pieno"), Path("/tmp/p.mov"), Path("/tmp/b.mov"), opz,
                               Path("/tmp/p.wav"))
    assert normale[normale.index("-vf") + 1] == "crop=1080:1080:0:420" and "-vf" not in pieno


def test_livello_dbfs_e_giudizio():
    from tools.reel.registra import dbfs, giudizio_livello
    assert dbfs(32767) == pytest.approx(0.0, abs=0.01)
    assert dbfs(16384) == pytest.approx(-6.02, abs=0.01)
    assert dbfs(0) == -90.0
    assert [giudizio_livello(x) for x in (0.0, -2.0, -10.0, -24.0, -40.0)] == ["satura", "alto", "buono", "basso", "troppo basso"]
