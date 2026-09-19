from __future__ import annotations

import pytest

from broll.immagini import DURATA_MIN_S, ImmaginiMancanti, componi, finestre


def test_una_finestra_per_frase():
    # i beat veri della scena 4 di generativa-probabile
    t = finestre([0.0, 3.037, 5.656, 9.122, 10.929], 15.02)
    assert len(t) == 5
    assert [round(i, 2) for i, _ in t] == [0.0, 3.04, 5.66, 9.12, 10.93]
    assert round(sum(d for _, d in t), 2) == 15.02        # coprono la scena, senza buchi né code


def test_senza_beat_una_sola_immagine():
    assert finestre([], 8.0) == [(0.0, 8.0)]


def test_un_primo_beat_in_ritardo_non_lascia_il_campo_vuoto():
    t = finestre([1.4, 5.0], 9.0)
    assert t[0][0] == 0.0
    assert round(sum(d for _, d in t), 2) == 9.0


def test_le_finestre_troppo_corte_si_fondono():
    """Sotto la mezza dozzina di decimi il cambio è uno sfarfallio, non uno stacco."""
    t = finestre([0.0, 4.0, 4.0 + DURATA_MIN_S / 2], 9.0)
    assert len(t) == 2
    assert round(sum(d for _, d in t), 2) == 9.0


def test_i_beat_oltre_la_durata_si_scartano():
    t = finestre([0.0, 3.0, 99.0], 6.0)
    assert len(t) == 2
    assert round(sum(d for _, d in t), 2) == 6.0


def test_immagini_assenti(tmp_path):
    with pytest.raises(ImmaginiMancanti):
        componi([], [0.0], 5.0, tmp_path / "x.mp4")
    with pytest.raises(ImmaginiMancanti, match="assenti"):
        componi([tmp_path / "manca.png"], [0.0], 5.0, tmp_path / "x.mp4")
