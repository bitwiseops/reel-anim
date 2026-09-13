import shutil
import wave
from pathlib import Path

import pytest

from tools.reel.ffmpeg import ffprobe
from tools.reel.voce import sintetizza_frase, sintetizza_frasi, unisci_wav


def _wav(p: Path, secondi: float, hz: int = 48000) -> Path:
    with wave.open(str(p), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(hz)
        w.writeframes(b"\x01\x00" * int(secondi * hz))
    return p


def test_unisci_wav_inizi_al_campione(tmp_path):
    a, b = _wav(tmp_path / "a.wav", 0.5), _wav(tmp_path / "b.wav", 1.0)
    inizi, durata = unisci_wav([a, b], 0.3, tmp_path / "u.wav")
    assert inizi == [0.0, 0.8] and durata == 1.8
    with wave.open(str(tmp_path / "u.wav")) as w:
        assert w.getnframes() == int(1.8 * 48000)


def test_unisci_wav_rifiuta_formati_diversi_e_liste_vuote(tmp_path):
    with pytest.raises(ValueError):
        unisci_wav([_wav(tmp_path / "a.wav", 0.1), _wav(tmp_path / "b.wav", 0.1, hz=44100)], 0.3, tmp_path / "u.wav")
    with pytest.raises(ValueError):
        unisci_wav([], 0.3, tmp_path / "u.wav")


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which("say"), reason="la voce di prova richiede macOS say")
def test_sintetizza_frasi_inizi_esatti_e_cache(tmp_path, monkeypatch):
    frasi = ["Prima frase.", "Seconda frase, un po' più lunga."]
    v = sintetizza_frasi(frasi, tmp_path / "01.m4a")
    prima = sintetizza_frase(frasi[0], tmp_path / "frasi")          # già in cache: stesso file
    with wave.open(str(prima)) as w:
        d1 = w.getnframes() / w.getframerate()
    assert v.inizi_s[0] == 0.0 and abs(v.inizi_s[1] - (d1 + 0.3)) < 0.002
    p = ffprobe(v.audio)
    assert p["audio"] == "aac" and p["audio_hz"] == 48000 and abs(p["durata_s"] - v.durata_s) < 0.06

    import tools.reel.voce as voce
    vero = voce.subprocess.run

    def senza_say(cmd, *a, **k):
        assert Path(cmd[0]).name != "say", "say rilanciato nonostante la cache"
        return vero(cmd, *a, **k)

    monkeypatch.setattr(voce.subprocess, "run", senza_say)
    assert sintetizza_frasi(frasi, tmp_path / "02.m4a").inizi_s == v.inizi_s
