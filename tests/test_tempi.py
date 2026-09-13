import pytest

from tools.anim.base import CODA_S, ScenaReel, inizi_per_parole


def test_inizi_proporzionali_alle_parole():
    assert inizi_per_parole(["a b", "c d e f"], 0, 6) == [0.0, 2.0]
    assert inizi_per_parole(["**una** frase ==sola=="], 1.5, 9) == [1.5]
    assert inizi_per_parole([], 0, 5) == []
    assert inizi_per_parole(["a", "b c"], 3, 3) == [3.0, 3.0]      # intervallo nullo: tutte insieme
    i = inizi_per_parole(["uno due", "tre", "quattro cinque sei"], 0.5, 7.5)
    assert i[0] == 0.5 and i == sorted(i) and i[-1] < 7.5


def test_scena_usa_gli_inizi_veri_o_la_stima():
    s = ScenaReel(6.0, {"voce": ["a b", "c"], "inizi_frasi_s": [0.0, 2.5]})
    assert s.inizi_frasi == [0.0, 2.5]
    assert s.durata_beat(0) == 2.5 and s.durata_beat(1) == 3.5
    stimata = ScenaReel(6.0, {"voce": ["a b", "c d"], "inizi_frasi_s": [0.0]})   # lunghezza sbagliata: si stima
    assert stimata.inizi_frasi == inizi_per_parole(["a b", "c d"], 0.0, 6.0 - CODA_S)


def test_beat_con_indici_sbagliati():
    s = ScenaReel(6.0, {"voce": ["a", "b"]})
    with pytest.raises(IndexError):
        s.beat(2)
    muta = ScenaReel(4.0, {})
    muta.beat(0)   # senza VOCE beat(0) non fa nulla
    with pytest.raises(ValueError):
        muta.beat(1)


def test_arrotonda_a_fotogrammi_interi():
    from manim import config
    s = ScenaReel(6.0, {"voce": ["a"]})
    f = 1 / config.frame_rate
    r = s.arrotonda(0.21)
    assert r <= 0.21 and abs(r / f - round(r / f)) < 1e-6
    assert s.arrotonda(0.0) == f      # mai zero: almeno un fotogramma
