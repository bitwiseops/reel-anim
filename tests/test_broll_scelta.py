from __future__ import annotations

import pytest

from tools.broll.crediti import testo as crediti
from tools.broll.piano import Piano, ScenaBroll
from tools.broll.scelta import TAGLIO_MIN_S, SceltaNonValida, ancora, confini, controlla_scelta, scegli


def _candidato(id_: str, durata_s: float = 20.0, larghezza: int = 1080, altezza: int = 1920, **altro) -> dict:
    return {"fornitore": "pexels", "id": id_, "url_pagina": f"https://www.pexels.com/video/{id_}/",
            "url_file": f"https://example.invalid/{id_}.mp4", "anteprima": "", "larghezza": larghezza,
            "altezza": altezza, "durata_s": durata_s, "fps": 25.0, "autore": "Ada Rossi",
            "autore_url": "https://www.pexels.com/@ada", "licenza": "Pexels License", "query": "ufficio",
            "resta_ritaglio": 1.0, **altro}


def _scena(**altro) -> ScenaBroll:
    base = dict(n=4, tipo="spiegazione", durata_s=9.0, origine_durata="report", registro="filmato",
                query=["ufficio"], candidati=[_candidato("111"), _candidato("222", durata_s=6.0)])
    return ScenaBroll(**{**base, **altro})


def test_scegli_copia_il_candidato_nel_taglio():
    s = _scena()
    t = scegli(s, "pexels:111", da_s=2.0, ancora_x=0.0)
    assert s.stato == "scelto" and s.scelti == [t]
    assert (t["candidato"], t["da_s"], t["ancora"]) == ("pexels:111", 2.0, 0.0)
    # i crediti non devono dipendere dalla lista dei candidati, che `cerca` rifà
    s.candidati = []
    assert t["autore"] == "Ada Rossi" and t["licenza"] == "Pexels License"


def test_scegli_sostituisce_e_aggiungi_accoda():
    s = _scena()
    scegli(s, "pexels:111")
    scegli(s, "pexels:222")
    assert [t["candidato"] for t in s.scelti] == ["pexels:222"]
    scegli(s, "pexels:111", aggiungi=True)
    assert [t["candidato"] for t in s.scelti] == ["pexels:222", "pexels:111"]


def test_scegli_rifiuta_quello_che_non_e_nei_provini():
    with pytest.raises(SceltaNonValida, match="non è fra i candidati"):
        scegli(_scena(), "pexels:999")
    with pytest.raises(SceltaNonValida, match="non a filmato"):
        scegli(_scena(registro="animazione"), "pexels:111")


def test_ancora_a_nome_o_a_numero():
    assert (ancora("sinistra"), ancora("centro"), ancora("0,25")) == (0.0, 0.5, 0.25)
    for sbagliata in ("sopra", "1.5"):
        with pytest.raises(SceltaNonValida):
            ancora(sbagliata)


def test_confini_un_taglio_tiene_tutta_la_scena():
    assert confini(1, [0.0, 3.0], 9.0) == [(0.0, 9.0)]


def test_confini_lo_stacco_cade_sul_beat_piu_vicino_alla_meta():
    # i beat veri della scena 4 di generativa-probabile: la metà è 7,51, il beat più vicino 9,122
    f = confini(2, [0.0, 3.037, 5.656, 9.122, 10.929], 15.02)
    assert f[1][0] == 9.122
    assert round(sum(d for _, d in f), 2) == 15.02


def test_confini_senza_beat_divide_in_parti_uguali():
    assert confini(3, [], 9.0) == [(0.0, 3.0), (3.0, 3.0), (6.0, 3.0)]


def test_confini_mai_un_taglio_lampo():
    """Un beat a ridosso dell'inizio o della fine non è un posto per uno stacco."""
    f = confini(2, [0.0, 0.4, 8.7], 9.0)
    assert all(d >= TAGLIO_MIN_S for _, d in f)


def test_controlla_un_filmato_che_finisce_prima_e_un_errore():
    s = _scena()
    scegli(s, "pexels:222")                          # 6 s per una scena di 9
    assert any(d.livello == "errore" and "ne ha ancora" in str(d) for d in controlla_scelta(s))
    scegli(s, "pexels:111", da_s=12.0)               # 20 s, ma partendo da 12 ne restano 8
    assert any(d.livello == "errore" for d in controlla_scelta(s))
    scegli(s, "pexels:111", da_s=5.0)
    assert controlla_scelta(s) == []


def test_controlla_due_tagli_corti_reggono_una_scena_lunga():
    s = _scena()
    scegli(s, "pexels:222")
    scegli(s, "pexels:222", da_s=0.5, aggiungi=True)      # 4,5 s a testa: 6 s bastano
    assert controlla_scelta(s) == []


def test_controlla_avvisa_sull_orizzontale():
    s = _scena(candidati=[_candidato("333", larghezza=3840, altezza=2160, resta_ritaglio=0.316)])
    scegli(s, "pexels:333")
    d = controlla_scelta(s)
    assert [x.livello for x in d] == ["avviso"] and "prova-inquadratura" in str(d[0])


def test_controlla_senza_scelta():
    assert [d.livello for d in controlla_scelta(_scena())] == ["errore"]


def test_crediti_un_autore_una_volta_sola():
    s2, s4 = _scena(n=2), _scena()
    scegli(s2, "pexels:111")
    scegli(s4, "pexels:222")
    t = crediti(Piano(slug="x", sorgente="", hash_md="", scene=[s2, s4]))
    assert "- Scena 2: [Ada Rossi](https://www.pexels.com/@ada) · Pexels · https://www.pexels.com/video/111/" in t
    assert t.rstrip().endswith("Filmati: Ada Rossi (Pexels)")
    assert "Nessun filmato scelto" in crediti(Piano(slug="x", sorgente="", hash_md="", scene=[_scena()]))
