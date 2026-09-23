"""`broll genera`: i prompt, il piano che si aggiorna, i crediti, e la resa a immagini.

Nessuna immagine vera: il client Meshy è sostituito da un finto che scrive un PNG su disco.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from broll import crediti
from broll.genera import PromptMancante, genera_scena, prompt_da_brief, soggetto
from broll.piano import Piano, ScenaBroll
from broll.rendi import ResaFallita, file_immagini, rendi_scena
from broll.scelta import controlla_scelta
from tools.reel.ffmpeg import ffprobe, trova_ffmpeg


def _png(dest: Path, colore=(40, 60, 90)) -> Path:
    from PIL import Image

    dest.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1080, 1920), colore).save(dest)
    return dest


def _finto(cartella: Path, conteggio: list[str]):
    """Un finto `meshy.genera`: scrive un PNG e ritorna la stessa scheda del vero."""
    def genera(prompt: str, n: int = 1, *, forza: bool = False, **_):
        conteggio.append(prompt)
        f = _png(cartella / f"meshy-{n}-{len(conteggio)}.png", (30 * n % 200, 70, 120))
        return f, {"fornitore": "meshy", "generata": True, "prompt": prompt, "indice": n,
                   "modello": "nano-banana-pro", "task": f"t-{n}", "quando": "2026-09-22",
                   "licenza": "Meshy — immagine generata", "file": None,
                   "candidato": f"meshy:abc-{n}", "da_cache": False}
    return genera


def _scena(**kw) -> ScenaBroll:
    base = dict(n=4, tipo="spiegazione", durata_s=9.0, origine_durata="report",
                inizi_frasi_s=[0.0, 3.0, 6.0],
                brief=["Un uomo in un ufficio vuoto guarda lo schermo",
                       "La città di notte dalla finestra"],
                voce=["Succede a tutti.", "E nessuno lo dice."])
    base.update(kw)
    return ScenaBroll(**base)


# --- i prompt -------------------------------------------------------------------------------------

def test_il_soggetto_passa_in_inglese_e_butta_il_gergo():
    s = soggetto("Entra da sinistra un uomo stanco in un ufficio vuoto")
    assert "man" in s and "office" in s and "empty" in s
    assert "sinistra" not in s and "entra" not in s          # gergo del montaggio: via (query.py)


def test_i_prompt_vengono_dal_brief_uno_per_riga():
    p = prompt_da_brief(_scena(), quante=2)
    assert len(p) == 2 and p[0] != p[1]
    assert all("no text" in x and "9:16" in x for x in p)
    assert "office" in p[0] and "city" in p[1]


def test_piu_immagini_che_righe_di_brief_cambiano_inquadratura():
    p = prompt_da_brief(_scena(), quante=4)
    assert len(p) == 4 and len(set(p)) == 4
    assert any("wide shot" in x for x in p) and any("close-up" in x for x in p)


def test_senza_brief_si_ripiega_sulla_voce():
    p = prompt_da_brief(_scena(brief=[]), quante=1)
    assert len(p) == 1 and "no text" in p[0]


def test_senza_niente_da_cui_ricavare_un_prompt_si_chiede_a_mano():
    with pytest.raises(PromptMancante, match="--prompt"):
        prompt_da_brief(_scena(brief=[], voce=[]), quante=2)


# --- il piano -------------------------------------------------------------------------------------

def test_genera_mette_nel_piano_file_prompt_e_registro(tmp_path):
    visti: list[str] = []
    s = _scena()
    schede, diag = genera_scena(s, None, quante=3, genera=_finto(tmp_path, visti))

    assert len(visti) == 3 and len(schede) == 3
    assert s.registro == "immagini" and s.stato == "scelto"
    assert s.file == "broll-scena-04.mp4"
    assert [t["prompt"] for t in s.scelti] == visti
    assert all(t["generata"] and t["file"] for t in s.scelti)
    assert diag == []


def test_i_prompt_passati_a_mano_vincono_sul_brief(tmp_path):
    visti: list[str] = []
    s = _scena()
    genera_scena(s, ["a dark server room", "  ", "a hand on a switch"], genera=_finto(tmp_path, visti))
    assert visti == ["a dark server room", "a hand on a switch"]      # le righe vuote non contano


def test_meno_immagini_che_frasi_avvisa(tmp_path):
    s = _scena(inizi_frasi_s=[0.0, 2.0, 4.0, 6.0])
    _, diag = genera_scena(s, ["uno"], genera=_finto(tmp_path, []))
    assert len(diag) == 1 and "--quante 4" in str(diag[0])


def test_il_piano_sopravvive_a_un_giro_di_broll_piano(tmp_path):
    """`broll piano` rifatto non deve buttare immagini che sono costate."""
    from broll.piano import eredita

    vecchia = _scena()
    genera_scena(vecchia, ["uno", "due"], genera=_finto(tmp_path, []))
    vecchio = Piano(slug="x", sorgente="s.md", hash_md="a", scene=[vecchia])
    nuova = _scena()                                    # il piano nuovo la riproporrebbe animata
    nuovo = Piano(slug="x", sorgente="s.md", hash_md="b", scene=[nuova])

    assert eredita(nuovo, vecchio) == [4]
    assert nuova.registro == "immagini" and len(nuova.scelti) == 2


# --- i controlli e i crediti ----------------------------------------------------------------------

def test_una_scena_a_immagini_senza_immagini_e_un_errore():
    s = _scena(registro="immagini")
    d = controlla_scelta(s)
    assert len(d) == 1 and "broll genera" in str(d[0])


def test_un_immagine_sparita_dalla_cache_si_rigenera(tmp_path):
    s = _scena()
    genera_scena(s, ["uno"], genera=_finto(tmp_path, []))
    file_immagini(s)[0].unlink()
    d = controlla_scelta(s)
    assert len(d) == 1 and "cache" in str(d[0])


def test_i_crediti_dicono_generata_e_non_inventano_un_autore(tmp_path):
    s = _scena()
    genera_scena(s, ["a dark server room"], genera=_finto(tmp_path, []))
    md = crediti.testo(Piano(slug="x", sorgente="s.md", hash_md="a", scene=[s]))
    assert "generata** con Meshy" in md and "nano-banana-pro" in md and "2026-09-22" in md
    assert "a dark server room" in md
    assert "autore non indicato" not in md
    assert "Immagini generate con Meshy" in md


def test_i_crediti_tengono_insieme_filmati_e_immagini(tmp_path):
    generata = _scena(n=4)
    genera_scena(generata, ["uno"], genera=_finto(tmp_path, []))
    filmata = _scena(n=6, registro="filmato", scelti=[
        {"candidato": "pexels:7", "fornitore": "pexels", "id": "7", "autore": "Tizio",
         "autore_url": "https://p/tizio", "url_pagina": "https://p/7", "licenza": "Pexels License"}])
    md = crediti.testo(Piano(slug="x", sorgente="s.md", hash_md="a", scene=[generata, filmata]))
    assert "Filmati: Tizio (Pexels)" in md and "Immagini generate con Meshy" in md


# --- la resa (lenta: serve ffmpeg) ----------------------------------------------------------------

@pytest.mark.slow
def test_rendi_a_immagini_rispetta_il_contratto_del_montaggio(tmp_path):
    trova_ffmpeg()
    s = _scena(durata_s=9.03, inizi_frasi_s=[0.0, 3.1, 6.4])
    genera_scena(s, ["uno", "due", "tre"], genera=_finto(tmp_path / "cache", []))
    dest = tmp_path / "media" / "broll-scena-04.mp4"
    video, diag = rendi_scena("x", s, dest=dest)

    info = ffprobe(video)
    assert (info["larghezza"], info["altezza"]) == (1080, 1920)
    assert info["audio"] is None
    assert info["fotogrammi"] == round(9.03 * 30)       # al fotogramma, come per i filmati
    assert s.stato == "reso" and s.file == "broll-scena-04.mp4"
    assert diag == [] and not list(dest.parent.glob("*.tmp*"))


@pytest.mark.slow
def test_rendi_a_immagini_con_una_sola_immagine_copre_tutta_la_scena(tmp_path):
    trova_ffmpeg()
    s = _scena(durata_s=4.0, inizi_frasi_s=[0.0, 2.0])
    genera_scena(s, ["uno"], genera=_finto(tmp_path / "cache", []))
    video, diag = rendi_scena("x", s, dest=tmp_path / "media" / "broll-scena-04.mp4")
    assert ffprobe(video)["fotogrammi"] == 120
    assert any("si ripetono" in str(d) for d in diag)


@pytest.mark.slow
def test_rendi_a_immagini_senza_immagini_si_rifiuta(tmp_path):
    s = _scena(registro="immagini")
    with pytest.raises(ResaFallita, match="nessuna immagine"):
        rendi_scena("x", s, dest=tmp_path / "out.mp4")


@pytest.mark.slow
def test_fra_un_immagine_e_l_altra_c_e_davvero_una_dissolvenza(tmp_path):
    """Le immagini finte sono tinte piatte: a metà dissolvenza il colore deve stare in mezzo."""
    from PIL import Image

    from broll.immagini import dissolvenza_s, finestre
    from tools.reel.ffmpeg import estrai_fotogramma

    trova_ffmpeg()
    s = _scena(durata_s=6.0, inizi_frasi_s=[0.0, 3.0])
    genera_scena(s, ["uno", "due"], genera=_finto(tmp_path / "cache", []))
    video, _ = rendi_scena("x", s, dest=tmp_path / "media" / "broll-scena-04.mp4")

    t = dissolvenza_s(finestre(s.inizi_frasi_s, s.durata_s))
    assert t > 0
    def rosso(istante: float) -> int:
        f = estrai_fotogramma(video, istante, tmp_path / f"f-{istante:.2f}.png")
        return Image.open(f).convert("RGB").getpixel((540, 960))[0]

    prima, meta, dopo = rosso(3.0 - t), rosso(3.0 + t / 2), rosso(3.0 + t + 0.2)
    assert prima == pytest.approx(30, abs=3) and dopo == pytest.approx(60, abs=3)
    assert prima + 4 < meta < dopo - 4          # né l'una né l'altra: le due immagini si sovrappongono
