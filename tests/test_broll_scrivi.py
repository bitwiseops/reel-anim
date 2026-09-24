from __future__ import annotations

from pathlib import Path

from tools.broll.piano import Piano, ScenaBroll, eredita
from tools.broll.scrivi import applica

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


# ── `scrivi --presto`: le scene si marcano prima che il filmato esista, così l'animatore parte intanto ──────────

def test_presto_marca_anche_le_scene_non_rese(tmp_path):
    scene = [_scena(2, stato="da-scegliere"), _scena(3, stato="da-scegliere")]
    testo, scritte, diag = applica(MD, scene, tmp_path, presto=True)          # in media non c'è nessun file
    assert scritte == [2]
    assert "## Scena 2 [broll, durata=9s]\nSCHERMO: broll-scena-02.mp4\nVOCE: una frase" in testo
    msg = " | ".join(str(d) for d in diag)
    assert "non ancora resa" not in msg
    assert "ha un TESTO" in msg and "## Scena 3 [spiegazione]" in testo       # il TESTO resta una scelta del presentatore
    assert applica(testo, scene, tmp_path, presto=True)[:2] == (testo, [])    # due volte non cambia niente


def test_presto_senza_file_nel_piano_usa_il_nome_di_rendi(tmp_path):
    testo, scritte, _ = applica(MD, [_scena(2, stato="da-scegliere", file=None, registro="immagini")], tmp_path, presto=True)
    assert scritte == [2] and "SCHERMO: broll-scena-02.mp4" in testo


def test_presto_non_tocca_le_scene_animate_e_l_hook_resta_hook(tmp_path):
    scene = [_scena(1, tipo="hook", stato="da-scegliere"), _scena(2, registro="animazione", stato="da-scegliere", file=None)]
    testo, scritte, _ = applica(MD, scene, tmp_path, presto=True)
    assert scritte == [1] and "## Scena 1 [hook]\nSCHERMO: broll-scena-01.mp4\nTITOLO: T" in testo
    assert "## Scena 2 [spiegazione, durata=9s]\nVOCE: una frase" in testo


def test_senza_presto_una_scena_non_resa_resta_com_e(tmp_path):
    testo, scritte, diag = applica(MD, [_scena(2, stato="scelto")], tmp_path)
    assert testo == MD and scritte == [] and "non ancora resa" in str(diag[0])


def _sceneggiatura(tmp_path):
    """Il banco di prova del sottosistema riportato a prima di `scrivi`, con uno slug che non ha media."""
    testo = (Path(__file__).parent / "dati" / "demo-alternanza.md").read_text(encoding="utf-8")
    testo = testo.replace("slug: demo-alternanza", "slug: prova-presto-senza-media")
    for n in (2, 4):
        testo = testo.replace(f"## Scena {n} [broll]\nSCHERMO: broll-scena-{n:02d}.mp4\n", f"## Scena {n} [spiegazione]\n")
    md = tmp_path / "prova-presto.md"
    md.write_text(testo, encoding="utf-8")
    return md, testo


def test_scrivi_presto_salva_e_la_sceneggiatura_regge_valida(tmp_path):
    """Il file che manca è un avviso di `valida`, non un errore: la ri-validazione passa e il `.md` si salva."""
    from tools.broll.scrivi import scrivi
    from tools.reel.parser import parse
    from tools.reel.validate import check
    md, prima = _sceneggiatura(tmp_path)
    p = Piano(slug="prova-presto-senza-media", sorgente="", hash_md="",
              scene=[_scena(2, stato="da-scegliere"), _scena(4, stato="da-scegliere")])
    assert scrivi(p, md)[0] == [] and md.read_text(encoding="utf-8") == prima      # senza --presto: niente da scrivere
    scritte, diag = scrivi(p, md, presto=True)
    assert scritte == [2, 4] and not [d for d in diag if d.livello == "errore"]
    assert not list(tmp_path.glob("*.tmp"))                                   # scrittura atomica: il .tmp non resta
    r, avvisi = parse(md)
    d = avvisi + check(r)
    assert [s.n for s in r.scene if s.a_filmato] == [2, 4]
    assert not [x for x in d if x.livello == "errore"]
    assert sum("non ancora reso" in x.msg for x in d) == 2


def test_scrivi_presto_non_salva_se_il_risultato_non_passa_valida(tmp_path):
    from tools.broll.scrivi import scrivi
    md, prima = _sceneggiatura(tmp_path)
    prima = prima.replace("## Scena 2 [spiegazione]\n", "## Scena 2 [spiegazione]\nRIQUADRO: pieno\n")   # [broll] + pieno: errore
    md.write_text(prima, encoding="utf-8")
    p = Piano(slug="prova-presto-senza-media", sorgente="", hash_md="", scene=[_scena(2, stato="da-scegliere")])
    scritte, diag = scrivi(p, md, presto=True)
    assert scritte == [] and any("non la salvo" in str(d) for d in diag)
    assert md.read_text(encoding="utf-8") == prima


def test_piano_rifatto_dopo_presto_rispetta_le_scene_e_non_perde_le_query(tmp_path):
    """Dopo `scrivi --presto` le scene sono [broll] nel `.md`: `broll piano` le tiene a filmato ed eredita query e candidati."""
    from tools.broll.piano import da_sceneggiatura
    from tools.broll.scrivi import scrivi
    md, _ = _sceneggiatura(tmp_path)
    vecchio, _ = da_sceneggiatura(md)
    a_filmato = [s.n for s in vecchio.scene if s.registro == "filmato"]
    assert a_filmato
    for n in a_filmato:
        vecchio.scena(n).query = [{"q": "scelta a mano"}]
        vecchio.scena(n).candidati = [{"id": "1"}]
    scritte, _ = scrivi(vecchio, md, presto=True)
    assert scritte == a_filmato
    nuovo, _ = da_sceneggiatura(md)
    assert [s.n for s in nuovo.scene if s.registro == "filmato"] == a_filmato
    assert eredita(nuovo, vecchio) == a_filmato
    for n in a_filmato:
        assert nuovo.scena(n).query == [{"q": "scelta a mano"}] and nuovo.scena(n).candidati == [{"id": "1"}]
        assert nuovo.scena(n).file == f"broll-scena-{n:02d}.mp4"


def test_eredita_la_scena_broll_anche_con_la_voce_corretta_registrando():
    """Dal 22/09 la VOCE si corregge in `reel registra`: la scena [broll] resta la stessa e tiene le immagini pagate."""
    vecchio = _piano(_scena(2, tipo="broll", registro="immagini", scelti=[{"candidato": "meshy:a-1"}]))
    nuovo = _piano(_scena(2, tipo="broll", stato="da-scegliere", voce=["il testo recitato"]))
    assert eredita(nuovo, vecchio) == [2]
    s = nuovo.scena(2)
    assert s.registro == "immagini" and s.scelti == [{"candidato": "meshy:a-1"}] and "VOCE cambiata" in s.note
