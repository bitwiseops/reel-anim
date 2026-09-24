from __future__ import annotations

import pytest

from tools.anim.config import carica

from tools.broll.immagini import (DURATA_MIN_S, MARGINE_S, TENUTA_MIN_S, ImmaginiMancanti, comando,
                            componi, dissolvenza_s, dividi_per_immagini, finestre, montaggio, mossa, transizioni)


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


# --- la dissolvenza fra un'immagine e l'altra -----------------------------------------------------

def test_la_dissolvenza_e_quella_delle_transizioni_del_reel():
    cfg = carica()
    tr = cfg.dati["transizioni"]
    voluta = float(tr.get("immagini_s", tr["durata_s"]))
    assert dissolvenza_s([(0.0, 5.0), (5.0, 5.0)], cfg) == pytest.approx(voluta)


def test_con_una_sola_immagine_non_si_dissolve_niente():
    assert dissolvenza_s([(0.0, 8.0)]) == 0.0


def test_la_tenuta_piu_corta_accorcia_la_dissolvenza():
    """Una tenuta al minimo non può essere tutta dissolvenza: qualcosa deve restare fermo e solo."""
    t = dissolvenza_s([(0.0, 0.45), (0.45, 8.0)])
    assert t == pytest.approx(0.45 - TENUTA_MIN_S)
    assert 0 < t < DURATA_MIN_S - TENUTA_MIN_S


def test_gli_ingressi_tengono_la_durata_totale():
    """xfade non somma: l'uscita dura `offset + lunghezza dell'ultimo ingresso`."""
    tenute = [(0.0, 3.0), (3.0, 4.0), (7.0, 5.0)]
    lunghezze, offset = montaggio(tenute, 0.25)
    assert offset == [0.0, 3.0, 7.0]                       # le dissolvenze partono sugli inizi frase
    assert lunghezze[-1] == 5.0                            # l'ultima dura la sua tenuta e basta
    assert offset[-1] + lunghezze[-1] == pytest.approx(12.0)
    # ogni ingresso in mezzo deve arrivare almeno fino all'offset successivo più la dissolvenza
    for i in range(len(tenute) - 1):
        assert offset[i] + lunghezze[i] >= offset[i + 1] + 0.25


def test_senza_dissolvenza_le_lunghezze_sono_le_tenute():
    tenute = [(0.0, 3.0), (3.0, 4.0)]
    lunghezze, _ = montaggio(tenute, 0.0)
    assert lunghezze == [3.0, 4.0]
    assert sum(lunghezze) == pytest.approx(7.0)


def test_il_margine_non_allunga_il_risultato():
    tenute = [(0.0, 3.0), (3.0, 4.0)]
    lunghezze, offset = montaggio(tenute, 0.25)
    assert lunghezze[0] == pytest.approx(3.0 + 0.25 + MARGINE_S)
    assert offset[1] + lunghezze[1] == pytest.approx(7.0)   # il totale lo decide l'ultimo ingresso


def test_il_comando_usa_xfade_e_chiude_al_fotogramma(tmp_path):
    cfg = carica()
    img = [tmp_path / "a.png", tmp_path / "b.png", tmp_path / "c.png"]
    cmd = comando(img, [(0.0, 3.0), (3.0, 4.0), (7.0, 5.0)], tmp_path / "out.mp4", cfg)
    filtri = cmd[cmd.index("-filter_complex") + 1]
    nomi = transizioni(cfg)
    assert filtri.count("xfade=transition=") == 2
    assert f"xfade=transition={nomi[0]}:" in filtri and f"xfade=transition={nomi[1 % len(nomi)]}:" in filtri
    assert filtri.count("zoompan=") == 3
    assert "offset=3.000" in filtri and "offset=7.000" in filtri
    assert "concat=" not in filtri
    assert f"trim=end_frame={round(12.0 * cfg.fps)}" in filtri
    assert cmd[cmd.index("-map") + 1] == "[fin]"


def test_una_sola_immagine_resta_uno_stacco_solo(tmp_path):
    cfg = carica()
    cmd = comando([tmp_path / "a.png"], [(0.0, 6.0)], tmp_path / "out.mp4", cfg)
    filtri = cmd[cmd.index("-filter_complex") + 1]
    assert "xfade" not in filtri and "concat=n=1" in filtri


def test_le_mosse_cambiano_a_ogni_immagine():
    assert [mossa(i) for i in range(5)] == ["spinta", "carrellata", "allarga", "diagonale", "spinta"]
    assert mossa(0) != mossa(1)


def test_senza_chiave_resta_la_dissolvenza():
    from tools.anim.config import Config
    assert transizioni(Config({"transizioni": {}})) == ("fade",)


def test_piu_immagini_che_frasi_si_divide_la_tenuta_piu_lunga():
    tenute = dividi_per_immagini([(0.0, 2.5), (2.5, 6.0)], 3)
    assert tenute == [(0.0, 2.5), (2.5, 3.0), (5.5, 3.0)]
    assert sum(d for _, d in tenute) == pytest.approx(8.5)


def test_non_si_divide_sotto_la_tenuta_minima():
    assert dividi_per_immagini([(0.0, 2.0), (2.0, 2.5)], 3) == [(0.0, 2.0), (2.0, 2.5)]
    assert dividi_per_immagini([(0.0, 4.0)], 1) == [(0.0, 4.0)]
