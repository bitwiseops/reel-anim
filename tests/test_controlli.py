import pytest
from manim import DOWN, LEFT, RIGHT, UP, Circle, FadeIn, RoundedRectangle

from tools.anim.base import ScenaReel
from tools.anim.componenti import Etichetta
from tools.anim.componenti import testo as blocco   # «testo» sembrerebbe un test a pytest
from tools.anim.controlli import esegui_controlli
from tools.anim.misure import px
from tools.reel.manim_render import lint_animazione


def _scena(riquadro: str = "si") -> ScenaReel:
    return ScenaReel(6.0, {"voce": ["a"], "riquadro": riquadro})


def _tipi(s: ScenaReel) -> set[str]:
    return {v.controllo for v in esegui_controlli(s, "prova")}


def test_scena_pulita_senza_violazioni():
    s = _scena()
    et = Etichetta("una parola")
    s.area.contenuto.metti(et, "alto", "sinistra")
    t = blocco("Una frase normale", "caption").next_to(et, DOWN, buff=px(40), aligned_edge=LEFT)
    s.add(et, t)
    assert esegui_controlli(s, "prova") == []


def test_testo_piccolo_e_fuori_dalla_safe_area():
    s = _scena()
    piccolo = blocco("minuscolo", "caption").scale(0.5)
    s.area.contenuto.metti(piccolo, "alto", "sinistra")
    fuori = blocco("fuori", "caption").move_to([s.cfg.frame_width / 2 - px(30), 0, 0])
    s.add(piccolo, fuori)
    assert {"testo-piccolo", "testo-fuori"} <= _tipi(s)


def test_elemento_sul_riquadro_del_presentatore():
    s = _scena("si")
    s.add(blocco("sul presentatore", "caption").move_to(s.area.riquadro.centro))
    assert "riquadro" in _tipi(s)
    assert "riquadro" not in _tipi(_scena("no"))


def test_testo_coperto_da_una_forma_disegnata_dopo():
    s = _scena()
    t = blocco("sotto", "caption")
    s.area.contenuto.metti(t, "centro", "centro")
    box = RoundedRectangle(width=4, height=1.5, fill_color=s.cfg.palette.sfondo, fill_opacity=1, stroke_width=0).move_to(t)
    s.add(t, box)
    assert "testo-coperto" in _tipi(s)
    giusta = _scena()
    giusta.add(box.copy(), t.copy())   # prima il riquadro, poi il testo
    assert "testo-coperto" not in _tipi(giusta)


def test_testi_sovrapposti_e_colore_fuori_palette():
    s = _scena()
    a = blocco("primo testo", "caption")
    s.area.contenuto.metti(a, "centro", "sinistra")
    b = blocco("secondo testo", "caption").move_to(a).shift(RIGHT * px(20))
    c = Circle(radius=0.5).move_to(s.area.contenuto.centro + UP * 2)   # colore di default di Manim
    s.add(a, b, c)
    tipi = _tipi(s)
    assert "testi-sovrapposti" in tipi and "colore" in tipi


def test_lint_del_file_delle_animazioni(tmp_path):
    f = tmp_path / "anim.py"
    f.write_text("x = MathTex('a')\n# commento con to_edge(UP)\ny.to_edge(UP)\nz = Line(stroke_width=px(4))\n"
                 "c = '#FF0000'\nn = DecimalNumber(3, mob_class=Text)\nok = blocco('ciao')  # nota #FFFFFF\n", encoding="utf-8")
    righe = {n for n, _ in lint_animazione(f)}
    assert righe == {1, 3, 4, 5}


@pytest.mark.slow
def test_i_controlli_girano_dentro_il_render(tmp_path):
    from tools.reel.manim_render import renderizza

    class Sbagliata(ScenaReel):
        def costruisci(self):
            self.play(FadeIn(blocco("minuscolo", "caption").scale(0.5)), run_time=0.3)

    res = renderizza(Sbagliata, 1.0, {"voce": ["a"]}, tmp_path, "sbagliata", "l")
    assert any(c.startswith("testo-piccolo (fine scena)") for c in res.controlli)


def test_la_camera_ha_le_proporzioni_della_tela_e_i_controlli_misurano_lo_schermo():
    s = _scena()
    assert abs(s.camera.frame.width - s.cfg.frame_width) < 1e-9 and abs(s.camera.frame.height - s.cfg.frame_height) < 1e-9
    t = blocco("piccolo", "caption").scale(0.6)   # 29 px a tela intera
    s.area.contenuto.metti(t, "centro", "centro")
    s.add(t)
    assert "testo-piccolo" in _tipi(s)
    s.camera.frame.set(width=s.cfg.frame_width / 1.5).move_to(t)   # ingrandito 1,5 volte: 43 px sullo schermo
    assert "testo-piccolo" not in _tipi(s) and abs(s.zoom - 1.5) < 1e-9
    s.camera.frame.set(width=s.cfg.frame_width / 3).move_to(t.get_center() + RIGHT * s.cfg.frame_width / 6)   # t tagliato dal bordo
    assert "testo-fuori" in _tipi(s)


def test_zoom_al_centro_dell_area_e_testi_fuori_campo_ignorati():
    s = _scena("si")
    t = blocco("dettaglio", "caption")
    s.area.contenuto.metti(t, "alto", "sinistra")
    larghezza, centro = s.inquadratura(t, 2)
    s.camera.frame.set(width=larghezza).move_to(centro)
    sullo_schermo = (t.get_center() - s.camera.frame.get_center()) * s.zoom
    assert abs(sullo_schermo[0] - s.area.contenuto.centro[0]) < 1e-6 and abs(sullo_schermo[1] - s.area.contenuto.centro[1]) < 1e-6
    fuori_campo = blocco("fuori campo", "caption").move_to([s.cfg.frame_width * 2, 0, 0])
    s.add(t, fuori_campo)
    assert esegui_controlli(s, "prova") == []


def test_primo_fotogramma_vuoto_nell_hook():
    vuoto = ScenaReel(4.0, {"voce": ["a"], "riquadro": "no", "tipo": "hook"})
    vuoto.controlla_primo_fotogramma()
    assert [v.controllo for v in vuoto.controlli] == ["fotogramma-vuoto"]
    pieno = ScenaReel(4.0, {"voce": ["a"], "riquadro": "no", "tipo": "hook"})
    pieno.add(blocco("titolo", "caption"))
    pieno.controlla_primo_fotogramma()
    spiegazione = ScenaReel(4.0, {"voce": ["a"], "riquadro": "si", "tipo": "spiegazione"})
    spiegazione.controlla_primo_fotogramma()
    assert pieno.controlli == [] and spiegazione.controlli == []


@pytest.mark.slow
def test_punch_e_zoom_tagliano_e_rimettono_la_scena(tmp_path):
    from tools.reel.manim_render import renderizza

    class ConPunch(ScenaReel):
        def costruisci(self):
            t = blocco("prima della battuta", "caption")
            self.area.contenuto.metti(t, "alto", "sinistra")
            self.add(t)
            self.play(self.zoom_su(t, 1.4), run_time=0.3)
            self.punch("tu sì", tenuta_s=0.4)
            assert t in self.mobjects and abs(self.zoom - 1.4) < 1e-6   # la scena torna com'era, camera compresa
            self.play(self.torna(), run_time=0.3)

    res = renderizza(ConPunch, 2.0, {"voce": ["a"], "riquadro": "si"}, tmp_path, "punch", "l")
    assert res.controlli == [] and res.avvisi == []
