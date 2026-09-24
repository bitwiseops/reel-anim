from __future__ import annotations

from tools.broll.query import _parole, query_scena
from tools.reel.model import Scena


def test_parole_toglie_markup_e_parole_vuote():
    p = _parole("La **mail** di ==candidatura== che scrivi, e le tre righe.")
    assert "mail" in p and "candidatura" in p and "scrivi" in p
    assert "la" not in p and "che" not in p and "tre" not in p     # articoli, congiunzioni, numeri
    assert all("*" not in w and "=" not in w for w in p)


def test_parole_scarta_il_gergo_dei_brief():
    assert _parole("Il testo entra da sinistra e la carta sparisce in dissolvenza") == []


def test_query_solo_dal_brief_quando_c_e():
    """Il brief descrive cosa si vede; la VOCE no. Un sacchetto delle sue parole riporta filmati a caso."""
    s = Scena(n=2, tipo="spiegazione",
              voce=["Scrivi una mail di candidatura.", "La mail esce fluente."],
              animazione=["Mani che digitano su una tastiera, di notte."])
    q = query_scena(s)
    assert q == ["mani digitano tastiera notte"]
    assert not any("mail" in x for x in q)


def test_la_voce_entra_solo_senza_brief():
    s = Scena(n=2, tipo="spiegazione", voce=["Scrivi una mail di candidatura in fretta."])
    q = query_scena(s)
    assert len(q) == 1 and "mail" in q[0]


def test_query_scena_senza_niente_da_dire():
    assert query_scena(Scena(n=1, tipo="spiegazione")) == []


def test_query_al_massimo_tre_e_senza_doppioni():
    s = Scena(n=3, tipo="spiegazione",
              voce=["Una tastiera."],
              animazione=["Una tastiera.", "Una tastiera.", "Un ufficio vuoto di sera."])
    q = query_scena(s)
    assert len(q) <= 3
    assert len(q) == len(set(q))
