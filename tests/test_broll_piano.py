from __future__ import annotations

import json

from tools.broll.piano import RADICE, Piano, ScenaBroll, _proponi, controlla, da_sceneggiatura, salva
from tools.reel.model import Scena

ESEMPIO = RADICE / "templates" / "esempio-reel.md"


def _scene(tipi: list[str]) -> list[Scena]:
    return [Scena(n=i + 1, tipo=t) for i, t in enumerate(tipi)]


def test_proponi_salta_hook_chiusura_e_schermo():
    scene = _scene(["hook", "schermo", "chiusura"])
    assert _proponi(scene) == set()


def test_controlla_segnala_filmati_adiacenti():
    p = Piano(slug="x", sorgente="", hash_md="", scene=[
        ScenaBroll(n=1, tipo="spiegazione", durata_s=5, origine_durata="stima", registro="filmato", query=["a"]),
        ScenaBroll(n=2, tipo="spiegazione", durata_s=5, origine_durata="stima", registro="filmato", query=["b"]),
    ])
    msg = " ".join(str(d) for d in controlla(p))
    assert "entrambe a filmato" in msg


def _scene_broll(n: int, filmati: set[int]) -> list[ScenaBroll]:
    return [ScenaBroll(n=k, tipo="spiegazione", durata_s=5, origine_durata="stima",
                       registro="filmato" if k in filmati else "animazione",
                       query=["a"] if k in filmati else []) for k in range(1, n + 1)]


def test_controlla_equilibrio_fra_i_due_registri():
    """Regola del presentatore (2026-09-21): metà delle scene a filmato, ± una."""
    in_equilibrio = Piano(slug="x", sorgente="", hash_md="", scene=_scene_broll(8, {2, 4, 6, 8}))
    assert "metà ± una" not in " ".join(str(d) for d in controlla(in_equilibrio))
    troppi = Piano(slug="x", sorgente="", hash_md="", scene=_scene_broll(8, {1, 2, 3, 4, 5, 6}))
    assert "troppo materiale esterno" in " ".join(str(d) for d in controlla(troppi))
    pochi = Piano(slug="x", sorgente="", hash_md="", scene=_scene_broll(8, {2}))
    assert "troppo poche" in " ".join(str(d) for d in controlla(pochi))


def test_controlla_senza_filmati():
    p = Piano(slug="x", sorgente="", hash_md="", scene=[
        ScenaBroll(n=1, tipo="spiegazione", durata_s=5, origine_durata="stima")])
    assert "nessuna scena a filmato" in " ".join(str(d) for d in controlla(p))


def test_da_sceneggiatura_sull_esempio_del_repo():
    p, diag = da_sceneggiatura(ESEMPIO)
    assert p.slug == "esempio-reel"
    assert len(p.scene) == 7
    assert p.hash_md and len(p.hash_md) == 16
    # l'hook e la chiusura restano animate, sempre
    assert p.scena(1).registro == "animazione"
    assert p.scene[-1].registro == "animazione"
    # la scena [schermo] dell'esempio ha già il suo materiale nella finestra: non la si tocca
    schermo = [s for s in p.scene if s.tipo == "schermo"]
    assert schermo and all(s.registro == "animazione" for s in schermo)
    # ogni scena a filmato ha una query e un nome di file previsto
    for s in p.filmati:
        assert s.query and s.file == f"broll-scena-{s.n:02d}.mp4"


def test_giro_completo_su_disco(tmp_path, monkeypatch):
    import tools.broll.piano as mod

    monkeypatch.setattr(mod, "RADICE", tmp_path)
    p = Piano(slug="prova", sorgente="x.md", hash_md="abc", scene=[
        ScenaBroll(n=1, tipo="spiegazione", durata_s=4.5, origine_durata="stima", registro="filmato",
                   query=["mani che digitano"], file="broll-scena-01.mp4")])
    dest = salva(p)
    assert dest == tmp_path / "contenuti" / "broll" / "prova" / "piano.json"
    assert not list(dest.parent.glob("*.tmp"))          # scrittura atomica: niente residui
    letto = mod.carica_piano("prova")
    assert letto.to_dict() == json.loads(dest.read_text(encoding="utf-8"))
    assert letto.scena(1).query == ["mani che digitano"]
    assert letto.quando                                  # `salva` timbra la data


def test_tecnica_riconosce_cosa_va_disegnato():
    from tools.broll.piano import _tecnica

    # un meccanismo, una figura della libreria, una quantità: si spiega disegnando
    assert _tecnica(Scena(n=2, tipo="spiegazione", voce=["Il modello sceglie la parola più probabile."]))
    assert _tecnica(Scena(n=2, tipo="spiegazione", animazione=["Tre barre che salgono, una per candidato."]))
    assert _tecnica(Scena(n=2, tipo="spiegazione", voce=["Su cento righe, novanta sono uguali."]))
    # niente da mostrare: è una scena d'attenzione, e lì lavora meglio il filmato
    assert not _tecnica(Scena(n=2, tipo="spiegazione", voce=["Hai presente quando mandi quella mail?"]))


def test_proponi_lascia_animate_le_scene_tecniche():
    scene = [Scena(n=1, tipo="hook"),
             Scena(n=2, tipo="spiegazione", voce=["Hai presente quella mail?"]),
             Scena(n=3, tipo="spiegazione", animazione=["Una classifica di parole candidate."]),
             Scena(n=4, tipo="spiegazione", voce=["E ti siedi lì, davanti allo schermo."]),
             Scena(n=5, tipo="spiegazione", voce=["Il modello calcola la probabilità."]),
             Scena(n=6, tipo="chiusura")]
    # la 2 e la 4 non hanno niente da disegnare e non sono attaccate: vanno entrambe a filmato
    assert _proponi(scene) == {2, 4}


def test_marcatori_non_scattano_per_sottostringa():
    """«accento» non è «cento» e «barrata» non è «barra»: i brief di questo repo dicono l'una e l'altra
    a ogni riga, e senza confini di parola ogni scena risultava tecnica."""
    from tools.broll.piano import _marcatori

    s = Scena(n=2, tipo="spiegazione",
              animazione=["«Creativa» viene barrata; sotto compare la parola in accento."],
              voce=["Hai presente quando scrivi quella mail?"])
    assert _marcatori(s) == []


def test_i_tempi_dei_brief_non_sono_quantita():
    """«entro 0,5 s» è regia, non un numero da mostrare; «10 su 10» sì."""
    from tools.broll.piano import _marcatori

    regia = Scena(n=2, tipo="spiegazione", animazione=["Il titolo sale entro 0,5 s e tiene ~1 s."])
    quantita = Scena(n=3, tipo="spiegazione", animazione=["Sotto, l'etichetta «10 su 10»."])
    assert _marcatori(regia) == []
    assert _marcatori(quantita) == ["una quantità"]


def test_proponi_alterna_e_salta_l_hook():
    """Una sì una no, mai due di fila; l'apertura è il presentatore: non si propone nemmeno con un brief filmabile."""
    scene = _scene(["hook", "spiegazione", "spiegazione", "spiegazione", "spiegazione", "chiusura"])
    scene[0].animazione = ["Una persona apre la posta il lunedì mattina, la casella è piena."]
    assert _proponi(scene) == {2, 4}                    # solo le scene in mezzo, alternate


def test_una_quantita_a_lettere_nel_brief_non_rende_tecnica_la_scena():
    """«A metà pagina» nel brief descrive l'immagine; «metà» nella VOCE è una quantità da mostrare (2026-09-21)."""
    scene = _scene(["hook", "spiegazione", "spiegazione", "chiusura"])
    scene[1].animazione = ["Un uomo rilegge un foglio stampato, si ferma a metà pagina e ci tiene sopra il dito."]
    assert _proponi(scene) == {2}
    scene[1].voce = ["E di quei sei, metà potrebbe risentirne."]
    assert 2 not in _proponi(scene)


def test_le_durate_del_report_valgono_solo_per_la_stessa_voce(tmp_path, monkeypatch):
    """Dopo una ristrutturazione la «scena 3» del montaggio di prima è un'altra scena (2026-09-21)."""
    import json as _json
    import tools.broll.piano as piano
    md = tmp_path / "s.md"
    md.write_text("---\ntitolo: T\nslug: prova-durate\nformato: reel\nmessaggio_centrale: M\n---\n\n"
                  "## Scena 1 [hook]\nTITOLO: T\nVOCE: ti apro con una domanda?\n\n"
                  "## Scena 2 [spiegazione]\nVOCE: una frase qui.\nVOCE: e poi un'altra.\nANIMAZIONE: a\nFIGURA: f\n\n"
                  "## Scena 3 [chiusura]\nMESSAGGIO: M\nCTA: c\nVOCE: chiudo.\n", encoding="utf-8")
    out = tmp_path / "contenuti" / "render" / "prova-durate"
    monkeypatch.setattr(piano, "riepilogo", lambda slug: out)
    out.mkdir(parents=True)
    elementi = [{"scena": 2, "durata_s": 14.2, "inizi_frasi_s": [0.0, 1.0], "parole_voce": 6},    # stessa voce
                {"scena": 3, "durata_s": 99.0, "inizi_frasi_s": [0.0, 1.0, 2.0], "parole_voce": 30}]  # un'altra
    (out / "report.json").write_text(_json.dumps({"elementi": elementi}), encoding="utf-8")
    p, _ = piano.da_sceneggiatura(md)
    assert p.scena(2).origine_durata == "report" and p.scena(2).durata_s == 14.2
    assert p.scena(3).origine_durata == "stima" and p.scena(3).durata_s != 99.0
