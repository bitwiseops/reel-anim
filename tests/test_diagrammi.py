import pytest

from tools.anim.componenti import Codice, ContatoreScorre, Icona
from tools.anim.diagrammi import Ciclo, Confronto, Corrispondenza, Flusso, Graffa, Tabella
from tools.anim.misure import px

LARGHEZZA = px(900) + 1e-6


def test_flusso_e_ciclo():
    f = Flusso(["a", "b", "c"])
    assert len(f.nodi) == 3 and len(f.frecce) == 2 and f.width <= LARGHEZZA
    assert f.nodi[0].get_center()[1] > f.nodi[1].get_center()[1]   # dall'alto in basso
    c = Ciclo(["pensa", "agisci", "osserva"])
    assert len(c.stati) == len(c.archi) == 3 and c.width <= LARGHEZZA
    c.vai()
    assert c.corrente == 1


def test_confronto_corrispondenza_graffa_tabella():
    co = Confronto("prima riga", "dopo riga")
    co.boccia()
    assert len(co.barre) == 1
    cr = Corrispondenza(["gatto", "auto"], ["animale", "veicolo"])
    cr.collega(0, 0)
    cr.collega(1, 0, giusto=False)
    assert len(cr.linee) == 2 and cr.width <= LARGHEZZA
    t = Tabella([["modello", "parametri"], ["piccolo", ""]])
    assert (t.n_righe, t.n_col) == (2, 2) and t.linea is not None
    assert t.cella(1, 1).righe[0].piano == "–"
    g = Graffa(t, "dati")
    assert g.etichetta.get_center()[0] > t.get_right()[0]


def test_icona_contatore_codice():
    assert {"brain", "bot"} <= set(Icona.disponibili())
    with pytest.raises(FileNotFoundError):
        Icona("non-esiste")
    assert abs(Icona("brain", 120).height - px(120)) < 1e-6
    assert ContatoreScorre(0, "parametri")._formato(70_000_000_000) == "70.000.000.000"
    assert ContatoreScorre(0, decimali=1)._formato(1234.5) == "1.234,5"
    Codice("x = 1")
    with pytest.raises(ValueError):
        Codice("questa_riga_di_codice_e_decisamente_troppo_lunga_per_un_reel = 1")


@pytest.mark.slow
def test_vetrina_senza_violazioni(tmp_path):
    from tools.anim.vetrina import main
    assert main(["--qualita", "l", "--out", str(tmp_path)]) == 0
