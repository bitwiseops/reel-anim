"""Scena di prova della fase 0: titolo, caption, tre cartellini e una barra, 10 s. Nessun contenuto reale.

Uso: uv run python -m tools.anim.prova [--qualita l|m|h] [--out cartella]
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from manim import (BOLD, DOWN, LEFT, RIGHT, UP, Create, FadeIn, GrowFromEdge, Rectangle, RoundedRectangle, Text,
                   VGroup, Write, tempconfig)

from .base import ScenaReel
from .config import carica, opzioni_manim
from .misure import CORPO_PX, font_size_per, px


class Prova(ScenaReel):
    def costruisci(self):
        col, fam = self.cfg.palette, self.cfg.font.famiglia
        area = self.area.contenuto
        titolo = Text("Una parola\nalla volta", font=fam, weight=BOLD, font_size=font_size_per(CORPO_PX["titolo"]),
                      color=col.testo, line_spacing=0.9).move_to(area.centro + UP * 3.2)
        self.play(Write(titolo), run_time=1.2)
        self.beat(1)
        cartellini = VGroup()
        for parola in ("Caro", "Marco,", "oggi"):
            box = RoundedRectangle(corner_radius=px(18), width=px(300), height=px(110), stroke_color=col.attenuato,
                                   stroke_width=3, fill_color=col.sfondo, fill_opacity=1)
            t = Text(parola, font=fam, font_size=font_size_per(CORPO_PX["token"]), color=col.testo)
            cartellini.add(VGroup(box, t))
        cartellini.arrange(RIGHT, buff=px(24)).next_to(titolo, DOWN, buff=px(120))
        for c in cartellini:
            self.play(FadeIn(c, shift=UP * 0.3), run_time=0.4)
        self.beat(2)
        barra = Rectangle(width=px(720), height=px(34), stroke_width=0, fill_color=col.accento, fill_opacity=1)
        barra.next_to(cartellini, DOWN, buff=px(120)).align_to(cartellini, LEFT)
        etich = Text("probabile 62 %", font=fam, font_size=font_size_per(CORPO_PX["etichetta"]), color=col.accento)
        etich.next_to(barra, DOWN, buff=px(20)).align_to(barra, LEFT)
        self.play(GrowFromEdge(barra, LEFT), run_time=0.8)
        self.play(FadeIn(etich), run_time=0.3)
        caption = Text("esempio: i numeri sono inventati", font=fam, font_size=font_size_per(CORPO_PX["caption"]),
                       color=col.attenuato).move_to([area.centro[0], area.y0 + px(60), 0])
        self.play(FadeIn(caption), run_time=0.4)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--qualita", choices="lmh", default="h")
    ap.add_argument("--out", default=str(Path(__file__).resolve().parents[2] / "contenuti" / "render" / "_prova"))
    ap.add_argument("--debug", action="store_true")
    a = ap.parse_args(argv)
    cfg = carica()
    out = Path(a.out)
    t0 = time.time()
    with tempconfig(opzioni_manim(cfg, a.qualita, media_dir=out, output_file="prova")):
        s = Prova(durata_s=10.0, scena={"voce": ["a", "b", "c"], "riquadro": "si"}, debug=a.debug)
        s.render()
        file = Path(s.renderer.file_writer.movie_file_path)
    dt = time.time() - t0
    from ..reel.ffmpeg import ffprobe
    print(f"{file}  ({dt:.1f} s)  {ffprobe(file)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
