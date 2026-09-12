"""Libreria Manim del reel: base (ScenaReel, aree) e componenti. `from tools.anim import *` nelle animazioni."""
from manim import DOWN, LEFT, ORIGIN, RIGHT, UP, BOLD  # noqa: F401

from .base import Area, Aree, ScenaReel, aree  # noqa: F401
from .componenti import *  # noqa: F401,F403
from .misure import CORPO_PX, px, unita  # noqa: F401
