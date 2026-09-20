"""Caption: divisione in blocchi, tempi, disegno e presenza nel filtergraph."""
from __future__ import annotations

from pathlib import Path

from tools.anim.config import carica
from tools.reel import caption
from tools.reel.compositing import Sorgenti, comando_scena

VOCE = [
    "Guarda, dieci posti di lavoro in un paese avanzato.",
    "Uno studio del Fondo Monetario Internazionale ha stimato quanti sono esposti.",
    "Sono ==sei==, e lo dicono loro, non io.",
]
INIZI = [0.0, 3.2, 8.4]
DURATA = 13.9


def _blocchi():
    return caption.blocchi(VOCE, INIZI, DURATA, carica())


def test_i_blocchi_coprono_le_frasi_senza_scavalcarle():
    bb = _blocchi()
    assert bb, "nessun blocco"
    for b in bb:
        assert b.t0 < b.t1
        inizio_frase = INIZI[b.frase]
        fine_frase = INIZI[b.frase + 1] if b.frase + 1 < len(INIZI) else DURATA
        assert inizio_frase - 1e-6 <= b.t0 and b.t1 <= fine_frase + 1e-6   # mai a cavallo di due frasi
    for a, z in zip(bb, bb[1:], strict=False):
        assert z.t0 >= a.t1 - 1e-6            # in ordine e senza accavallarsi
    # il testo della frase si ritrova per intero nei suoi blocchi
    for i, frase in enumerate(VOCE):
        assert " ".join(b.testo for b in bb if b.frase == i) == frase


def test_nessun_blocco_dura_meno_del_minimo():
    minimo = float(carica().dati["caption"]["durata_min_s"])
    for b in _blocchi():
        assert b.t1 - b.t0 >= minimo - 1e-6, f"«{b.testo}» dura {b.t1 - b.t0:.2f} s"


def test_i_blocchi_stanno_in_due_righe():
    c = carica().dati["caption"]
    massimo = int(c["caratteri_riga_max"]) * int(c["righe_max"])
    for b in _blocchi():
        assert len(b.testo) <= massimo
        assert len(b.testo.split()) <= int(c["parole_blocco"]) * 2   # il raddoppio è il ripiego dei blocchi corti


def test_frase_corta_resta_un_blocco_solo():
    bb = caption.blocchi(["Ti è mai successo?"], [0.0], 2.0, carica())
    assert len(bb) == 1 and bb[0].testo == "Ti è mai successo?"


def test_la_punteggiatura_resta_attaccata_alla_parola_in_accento():
    parole = caption._parole_accento("Sono ==sei==, e lo dicono loro.")
    assert ("sei,", True) in parole and ("Sono", False) in parole


def test_il_png_e_in_cache_e_grande_quanto_la_fascia(tmp_path: Path):
    cfg = carica()
    b = _blocchi()[0]
    f1 = caption.disegna(b, tmp_path, cfg)
    scritto = f1.stat().st_mtime_ns
    f2 = caption.disegna(b, tmp_path, cfg)
    assert f1 == f2 and f2.stat().st_mtime_ns == scritto   # stesso testo, stesso file: non si ridisegna
    from PIL import Image
    _, _, w, h = caption.fascia(cfg)
    assert Image.open(f1).size == (w, h)


def test_la_fascia_sta_dentro_la_safe_area_e_sotto_il_contenuto():
    cfg = carica()
    s = cfg.dati["safe_area"]
    x, y, w, h = caption.fascia(cfg, "basso")
    assert x == s["sinistra"] and x + w == cfg.larghezza - s["destra"]
    assert y + h == cfg.altezza - s["basso"]
    xa, ya, _, _ = caption.fascia(cfg, "alto")
    assert ya == s["alto"] and xa == x


def test_attiva_segue_la_scena():
    cfg = carica()
    assert caption.attiva(cfg, None) == "basso"
    assert caption.attiva(cfg, "no") is None
    assert caption.attiva(cfg, "alto") == "alto"


def test_le_caption_finiscono_nel_filtergraph(tmp_path: Path):
    png = tmp_path / "cap.png"
    png.write_bytes(b"")
    src = Sorgenti(grafica=Path("/tmp/grafica.mp4"), durata_s=5.0, riquadro="no",
                   caption=((png, 0.0, 1.2), (png, 1.2, 3.0)), caption_xy=(60, 1380))
    cmd = comando_scena(src, tmp_path / "out.mp4")
    filtri = cmd[cmd.index("-filter_complex") + 1]
    assert filtri.count("overlay=x=60:y=1380") == 2
    assert "enable='between(t,0.000,1.200)'" in filtri and "enable='between(t,1.200,3.000)'" in filtri
    assert cmd.count(str(png)) == 2
