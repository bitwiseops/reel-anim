from __future__ import annotations

from broll.piano import Piano, ScenaBroll, eredita
from broll.scrivi import applica

MD = """---
slug: x
---

## Scena 1 [hook]
TITOLO: T
VOCE: v

## Scena 2 [spiegazione, durata=9s]
VOCE: una frase
ANIMAZIONE: una persona alla scrivania

## Scena 3 [spiegazione]
VOCE: un'altra
ANIMAZIONE: una pila di fogli
TESTO: un'etichetta

## Scena 4 [chiusura]
MESSAGGIO: M
"""


def _scena(n: int, **altro) -> ScenaBroll:
    base = dict(n=n, tipo="spiegazione", durata_s=9.0, origine_durata="stima", registro="filmato",
                voce=["una frase"], stato="reso", file=f"broll-scena-{n:02d}.mp4")
    return ScenaBroll(**{**base, **altro})


def _media(tmp_path, *nomi):
    for n in nomi:
        (tmp_path / n).write_bytes(b"x")
    return tmp_path


def test_applica_cambia_il_tipo_e_aggiunge_schermo(tmp_path):
    testo, scritte, diag = applica(MD, [_scena(2)], _media(tmp_path, "broll-scena-02.mp4"))
    assert scritte == [2] and diag == []
    assert "## Scena 2 [broll, durata=9s]\nSCHERMO: broll-scena-02.mp4\nVOCE: una frase\nANIMAZIONE: una persona" in testo
    assert testo.replace("## Scena 2 [broll, durata=9s]\nSCHERMO: broll-scena-02.mp4\n",
                         "## Scena 2 [spiegazione, durata=9s]\n") == MD            # nient'altro è cambiato


def test_applica_due_volte_non_cambia_niente(tmp_path):
    media = _media(tmp_path, "broll-scena-02.mp4")
    testo, _, _ = applica(MD, [_scena(2)], media)
    di_nuovo, scritte, _ = applica(testo, [_scena(2)], media)
    assert di_nuovo == testo and scritte == []


def test_applica_non_tocca_una_scena_con_testo_ne_una_non_resa(tmp_path):
    media = _media(tmp_path, "broll-scena-03.mp4")
    testo, scritte, diag = applica(MD, [_scena(2), _scena(3)], media)       # la 2 non ha il file, la 3 ha un TESTO
    assert testo == MD and scritte == []
    msg = " | ".join(str(d) for d in diag)
    assert "non ancora resa" in msg and "ha un TESTO" in msg


def _piano(*scene: ScenaBroll) -> Piano:
    return Piano(slug="x", sorgente="", hash_md="", scene=list(scene))


def test_eredita_le_scelte_se_la_scena_dice_le_stesse_cose():
    vecchio = _piano(_scena(2, candidati=[{"id": "1"}], scelti=[{"candidato": "pexels:1"}]))
    nuovo = _piano(_scena(2, stato="da-scegliere", file="broll-scena-02.mp4"))
    assert eredita(nuovo, vecchio) == [2]
    assert nuovo.scena(2).scelti == [{"candidato": "pexels:1"}] and nuovo.scena(2).stato == "reso"


def test_eredita_durata_cambiata_torna_a_scelto():
    """È arrivata la presa vera: la scelta vale ancora, il file reso sulla stima no."""
    vecchio = _piano(_scena(2, scelti=[{"candidato": "pexels:1"}]))
    nuovo = _piano(_scena(2, stato="da-scegliere", durata_s=9.6))
    eredita(nuovo, vecchio)
    assert nuovo.scena(2).stato == "scelto" and "da rendere di nuovo" in nuovo.scena(2).note


def test_eredita_niente_se_la_voce_e_cambiata_o_la_scena_non_e_piu_a_filmato():
    vecchio = _piano(_scena(2, scelti=[{"candidato": "pexels:1"}]), _scena(3, scelti=[{"candidato": "pexels:2"}]))
    nuovo = _piano(_scena(2, stato="da-scegliere", voce=["un'altra frase"]),
                   _scena(3, stato="da-scegliere", registro="animazione"))
    assert eredita(nuovo, vecchio) == []
    assert nuovo.scena(2).scelti == [] and nuovo.scena(3).scelti == []


def test_applica_l_hook_resta_hook(tmp_path):
    md = MD.replace("TITOLO: T\nVOCE: v\n", "TITOLO: T\nVOCE: v\nRIQUADRO: no\n")
    testo, scritte, diag = applica(md, [_scena(1, tipo="hook")], _media(tmp_path, "broll-scena-01.mp4"))
    assert scritte == [1] and "## Scena 1 [hook]\nSCHERMO: broll-scena-01.mp4\nTITOLO: T" in testo
    assert "RIQUADRO: no" in " ".join(str(d) for d in diag)         # lo dice, non lo toglie: è del presentatore
