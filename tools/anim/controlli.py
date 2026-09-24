"""Controlli automatici sullo stato di una scena, eseguiti da ScenaReel a fine di ogni beat e alla chiusura.

Claude Code non vede il video: questi controlli trovano da soli i difetti che nei fotogrammi sfuggono (o costano un
giro in più): testo troppo piccolo o fuori dalla safe area, testo coperto da una forma disegnata sopra, testi
sovrapposti, elementi sul riquadro del presentatore, colori fuori palette e gradienti. Ogni violazione dice cosa,
quando (quale beat) e dove (px dello schermo, origine in alto a sinistra). Misurano quello che si vede: se la camera
è ingrandita o spostata (ScenaReel.zoom_su), posizioni e corpi del testo sono quelli sullo schermo.
"""
from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from manim import DL, UR, ManimColor, MarkupText, Mobject, Text, VMobject
from manim.utils.family import extract_mobject_family_members

from ..reel.model import RE_NUMERO
from .componenti import Riga
from .misure import FATTORE_FONT_SIZE, MINIMO_PX, PX_PER_UNITA

TOLLERANZA_PX = 2.0
COPERTURA_MIN = 0.3          # frazione del testo coperta da una forma piena disegnata dopo
SOVRAPPOSIZIONE_MIN = 0.15   # frazione del testo più piccolo coperta da un altro testo
DISTANZA_COLORE = 2.5 / 255  # tolleranza sul canale per riconoscere un colore della palette
PAROLE_DI_FILA_MAX = 2       # i reel si guardano muti: a spiegare è la caption, non il testo a schermo
                             # (numeri e percentuali non contano; le etichette si marcano con componenti.etichetta)

_PAROLINE = {"su", "di", "e", "o", "a", "in", "per", "col", "con", "da", "il", "la", "lo", "i", "le", "un", "una"}

Rett = tuple[float, float, float, float]   # x0, y0, x1, y1 in unità Manim


@dataclass(frozen=True)
class Violazione:
    controllo: str   # testo-piccolo | testo-fuori | riquadro | caption | parole-leggibili | testo-coperto |
                     # testi-sovrapposti | colore | gradiente
    momento: str     # «fine beat 1», «fine scena»               | fotogramma-vuoto (hook)
    messaggio: str
    bbox_px: tuple[int, int, int, int] | None = None

    def __str__(self) -> str:
        dove = f" [px {self.bbox_px[0]},{self.bbox_px[1]}→{self.bbox_px[2]},{self.bbox_px[3]}]" if self.bbox_px else ""
        return f"{self.controllo} ({self.momento}): {self.messaggio}{dove}"


@dataclass
class _Testo:
    nome: str
    glifi: list[VMobject]
    hg_px: float
    rett: Rett   # sullo schermo
    esente: bool = False   # etichetta di una figura o parola detta (Punch, MESSAGGIO, CTA, titolo di copertina)


def parole_di_contenuto(s: str) -> list[str]:
    """Le parole che chi guarda deve leggere: fuori i numeri, le percentuali, la punteggiatura e le paroline di
    servizio («6 su 10» = un numero, non tre parole)."""
    fuori = []
    for w in s.split():
        nudo = w.strip(".,;:!?«»\"'()[]…-–—").lower()
        if not nudo or RE_NUMERO.match(nudo) or nudo in _PAROLINE:
            continue
        fuori.append(nudo)
    return fuori


def _blocchi(testi: list[_Testo]) -> list[tuple[list[_Testo], int]]:
    """Raggruppa le righe che si leggono di fila (stessa colonna, una sotto l'altra) e conta le parole di ciascun
    gruppo: una frase spezzata su tre righe da due parole resta una frase."""
    liberi = [t for t in testi if not t.esente]
    liberi.sort(key=lambda t: -t.rett[3])
    gruppi: list[list[_Testo]] = []
    for t in liberi:
        for g in gruppi:
            u = g[-1]
            salto = u.rett[1] - t.rett[3]                      # aria fra la riga sopra e questa
            riga = max(u.hg_px, t.hg_px) / PX_PER_UNITA
            largo = min(u.rett[2], t.rett[2]) - max(u.rett[0], t.rett[0])
            if -riga * 0.2 <= salto <= riga * 0.8 and largo > 0:
                g.append(t)
                break
        else:
            gruppi.append([t])
    return [(g, sum(len(parole_di_contenuto(t.nome)) for t in g)) for g in gruppi]


def _rett(m: Mobject) -> Rett:
    a, b = m.get_critical_point(DL), m.get_critical_point(UR)
    return float(a[0]), float(a[1]), float(b[0]), float(b[1])


def _unione(rr: list[Rett]) -> Rett:
    return min(r[0] for r in rr), min(r[1] for r in rr), max(r[2] for r in rr), max(r[3] for r in rr)


def _area(r: Rett) -> float:
    return max(0.0, r[2] - r[0]) * max(0.0, r[3] - r[1])


def _inter(a: Rett, b: Rett) -> float:
    return _area((max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])))


def _px(r: Rett, cfg) -> tuple[int, int, int, int]:
    fw, fh = cfg.frame_width, cfg.frame_height
    return (round((r[0] + fw / 2) * PX_PER_UNITA), round((fh / 2 - r[3]) * PX_PER_UNITA),
            round((r[2] + fw / 2) * PX_PER_UNITA), round((fh / 2 - r[1]) * PX_PER_UNITA))


def _vista(scena) -> tuple[Callable[[Rett], Rett], float]:
    """Da coordinate della scena a coordinate dello schermo (come se la camera fosse a tela intera) e ingrandimento."""
    cornice = getattr(getattr(scena.renderer, "camera", None), "frame", None)
    if cornice is None:
        return (lambda r: r), 1.0
    z = scena.cfg.frame_width / cornice.width
    cx, cy = float(cornice.get_center()[0]), float(cornice.get_center()[1])
    if abs(z - 1) < 1e-9 and abs(cx) < 1e-9 and abs(cy) < 1e-9:
        return (lambda r: r), 1.0
    return (lambda r: ((r[0] - cx) * z, (r[1] - cy) * z, (r[2] - cx) * z, (r[3] - cy) * z)), z


def _riempita(m: Mobject) -> bool:
    return isinstance(m, VMobject) and m.has_points() and m.get_fill_opacity() > 0.02


def _tratto(m: Mobject) -> bool:
    return isinstance(m, VMobject) and m.has_points() and m.get_stroke_width() > 0 and m.get_stroke_opacity() > 0.02


def _visibile(m: Mobject) -> bool:
    return _riempita(m) or _tratto(m)


def _breve(s: str, n: int = 28) -> str:
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


def _famiglia(scena, escludi: set[int]) -> list[Mobject]:
    return [m for m in extract_mobject_family_members(scena.mobjects, use_z_index=True) if id(m) not in escludi]


def contenuto_visibile(scena, escludi: set[int] | None = None) -> bool:
    """C'è qualcosa di visibile in scena adesso? (per il primo fotogramma dell'hook)"""
    return any(m.has_points() and _visibile(m) for m in _famiglia(scena, escludi or set()))


def _testi(famiglia: list[Mobject], vista: Callable[[Rett], Rett], z: float) -> list[_Testo]:
    """Ogni testo visibile: le Riga della libreria (altezza dal puntello «Hg») e i Text/MarkupText usati a mano."""
    out: list[_Testo] = []
    visti: set[int] = set()
    for m in famiglia:
        if isinstance(m, Riga):
            visti.update(id(x) for x in m.glifi.get_family())
            glifi = [g for g in m.glifi.family_members_with_points() if _visibile(g)]
            if glifi:
                hg = m.puntello.height * PX_PER_UNITA if m.allineata else float(m.glifi.font_size) * FATTORE_FONT_SIZE
                out.append(_Testo(m.piano, glifi, hg * z, vista(_unione([_rett(g) for g in glifi])),
                                  bool(getattr(m, "_etichetta", False))))
    for m in famiglia:
        if isinstance(m, (Text, MarkupText)) and id(m) not in visti:
            glifi = [g for g in m.family_members_with_points() if _visibile(g)]
            if glifi:
                out.append(_Testo(str(getattr(m, "original_text", "testo")), glifi, float(m.font_size) * FATTORE_FONT_SIZE * z,
                                  vista(_unione([_rett(g) for g in glifi])), bool(getattr(m, "_etichetta", False))))
    return out


def _tocca_riquadro(r: Rett, m: Mobject, riq, forma: str, z: float = 1.0) -> bool:
    tol = TOLLERANZA_PX / PX_PER_UNITA
    if forma != "cerchio":
        return _inter(r, (riq.x0 + tol, riq.y0 + tol, riq.x1 - tol, riq.y1 - tol)) > 0
    cx, cy = float(riq.centro[0]), float(riq.centro[1])
    raggio = riq.larghezza / 2 - tol
    dx, dy = max(r[0] - cx, 0.0, cx - r[2]), max(r[1] - cy, 0.0, cy - r[3])
    if dx * dx + dy * dy >= raggio * raggio:
        return False
    if not _riempita(m):   # solo contorno: conta se il cerchio incontra il bordo, non se sta tutto dentro la forma
        w = m.get_stroke_width() * 0.01 * z + tol
        dentro = (r[0] + w <= cx - raggio and cx + raggio <= r[2] - w and r[1] + w <= cy - raggio and cy + raggio <= r[3] - w)
        return not dentro
    return True


def esegui_controlli(scena, momento: str, escludi: set[int] | None = None) -> list[Violazione]:
    """Controlla ciò che la scena ha in questo istante (ordine di disegno compreso). `escludi`: id da ignorare (guide)."""
    cfg = scena.cfg
    vista, z = _vista(scena)
    famiglia = _famiglia(scena, escludi or set())
    foglie = [m for m in famiglia if m.has_points() and _visibile(m)]
    ordine = {id(m): k for k, m in enumerate(foglie)}
    rett = {id(m): vista(_rett(m)) for m in foglie}
    schermo = (-cfg.frame_width / 2, -cfg.frame_height / 2, cfg.frame_width / 2, cfg.frame_height / 2)
    testi = [t for t in _testi(famiglia, vista, z) if _inter(t.rett, schermo) > 0]   # del tutto fuori campo: non si vede
    testo_di = {id(g): t for t in testi for g in t.glifi}
    v: list[Violazione] = []

    for t in testi:
        if t.hg_px < MINIMO_PX - 1:
            v.append(Violazione("testo-piccolo", momento, f"«{_breve(t.nome)}» alto {t.hg_px:.0f} px (minimo {MINIMO_PX})",
                                _px(t.rett, cfg)))

    s, fw, fh = cfg.dati["safe_area"], cfg.frame_width, cfg.frame_height
    safe = (-fw / 2 + s.get("sinistra", 60) / PX_PER_UNITA, -fh / 2 + s["basso"] / PX_PER_UNITA,
            fw / 2 - s["destra"] / PX_PER_UNITA, fh / 2 - s["alto"] / PX_PER_UNITA)
    for t in testi:
        r = t.rett
        fuori = max(safe[0] - r[0], safe[1] - r[1], r[2] - safe[2], r[3] - safe[3]) * PX_PER_UNITA
        if fuori > TOLLERANZA_PX:
            v.append(Violazione("testo-fuori", momento, f"«{_breve(t.nome)}» esce di {fuori:.0f} px dalla safe area "
                                "(sotto l'interfaccia di Instagram)", _px(r, cfg)))

    riq = scena.area.riquadro
    if riq is not None:
        forma = str(cfg.dati["riquadro"].get("forma", "cerchio"))
        colpiti = [(m, rett[id(m)]) for m in foglie if _tocca_riquadro(rett[id(m)], m, riq, forma, z)]
        if colpiti:
            nomi: list[str] = []
            for m, _ in colpiti:
                t = testo_di.get(id(m))
                n = f"«{_breve(t.nome)}»" if t else type(m).__name__
                if n not in nomi:
                    nomi.append(n)
            elenco = ", ".join(nomi[:4]) + (f" e altri {len(nomi) - 4}" if len(nomi) > 4 else "")
            v.append(Violazione("riquadro", momento, f"sul riquadro del presentatore: {elenco}",
                                _px(_unione([r for _, r in colpiti]), cfg)))

    cap = getattr(scena.area, "caption", None)
    if cap is not None:
        tol = TOLLERANZA_PX / PX_PER_UNITA
        fascia = (cap.x0 - tol, cap.y0 - tol, cap.x1 + tol, cap.y1 + tol)
        dentro = [(m, rett[id(m)]) for m in foglie if _inter(rett[id(m)], fascia) > 0]
        if dentro:
            nomi: list[str] = []
            for m, _ in dentro:
                t = testo_di.get(id(m))
                n = f"«{_breve(t.nome)}»" if t else type(m).__name__
                if n not in nomi:
                    nomi.append(n)
            elenco = ", ".join(nomi[:4]) + (f" e altri {len(nomi) - 4}" if len(nomi) > 4 else "")
            v.append(Violazione("caption", momento, f"nella fascia delle caption (che si bruciano nel montaggio): "
                                f"{elenco} → tienili in self.area.contenuto", _px(_unione([r for _, r in dentro]), cfg)))

    for gruppo, quante in _blocchi(testi):
        if quante > PAROLE_DI_FILA_MAX:
            frase = " ".join(t.nome for t in gruppo)
            v.append(Violazione("parole-leggibili", momento, f"«{_breve(frase, 40)}» è una frase da leggere "
                                f"({quante} parole, massimo {PAROLE_DI_FILA_MAX}): a spiegare è la caption, il testo a "
                                "schermo è un extra. Numeri e percentuali non contano; se è l'etichetta di una figura "
                                "marcala con componenti.etichetta()", _px(_unione([t.rett for t in gruppo]), cfg)))

    piene = [m for m in foglie if id(m) not in testo_di and m.get_fill_opacity() >= 0.5 and _riempita(m)]
    for t in testi:
        area_t = _area(t.rett)
        ultimo = max(ordine.get(id(g), -1) for g in t.glifi)
        for m in piene:
            if area_t > 0 and ordine[id(m)] > ultimo and _inter(t.rett, rett[id(m)]) / area_t > COPERTURA_MIN:
                v.append(Violazione("testo-coperto", momento, f"«{_breve(t.nome)}» coperto da un {type(m).__name__} disegnato "
                                    "sopra (ordine di impilamento: group=self, ordine dentro play, set_z_index)", _px(t.rett, cfg)))
                break

    for i in range(len(testi)):
        for j in range(i + 1, len(testi)):
            a, b = testi[i], testi[j]
            minima = min(_area(a.rett), _area(b.rett))
            if minima > 0 and _inter(a.rett, b.rett) / minima > SOVRAPPOSIZIONE_MIN:
                v.append(Violazione("testi-sovrapposti", momento, f"«{_breve(a.nome, 20)}» e «{_breve(b.nome, 20)}» si sovrappongono",
                                    _px(_unione([a.rett, b.rett]), cfg)))

    palette = [np.array(ManimColor(c).to_rgb()) for c in cfg.dati["palette"].values()]
    fuori_palette: dict[str, set[str]] = {}
    gradienti: set[str] = set()
    for m in foglie:
        colori = []
        if _riempita(m):
            if len({c.to_hex() for c in m.get_fill_colors()}) > 1:
                gradienti.add(type(m).__name__)
            colori.append(m.get_fill_color())
        if _tratto(m):
            colori.append(m.get_stroke_color())
        for c in colori:
            rgb = np.array(c.to_rgb())
            if min(float(np.abs(rgb - p).max()) for p in palette) > DISTANZA_COLORE:
                fuori_palette.setdefault(c.to_hex(), set()).add(type(m).__name__)
    if fuori_palette:
        v.append(Violazione("colore", momento, "fuori palette: " + "; ".join(
            f"{h} ({', '.join(sorted(n))})" for h, n in sorted(fuori_palette.items())) + " → usa self.cfg.palette"))
    if gradienti:
        v.append(Violazione("gradiente", momento, f"riempimento a più colori in {', '.join(sorted(gradienti))}"))
    return v
