# Pattern Manim

I **modi di fare** che tornano in ogni reel e che nessun componente incapsula. Ogni pattern ha: quando si usa, lo
snippet, e il nome della scena che lo prova. Il codice vero sta in `tools/anim/pattern.py`, dove ogni pattern ha la
sua scena renderizzata e passata dai controlli automatici:

```
uv run python -m tools.anim.pattern              # tutte le scene, contact sheet in contenuti/render/_pattern/
uv run python -m tools.anim.pattern --solo zoom
```

**Un pattern senza scena di prova non entra nel catalogo**, e la scena di prova si scrive **prima** del pattern: così
questo file non si riempie di codice che nessuno ha visto girare. Le fonti della comunità Manim sono in
`docs/animazioni.md` §13.

**La regola del tre**: quando un aiuto locale compare per la **terza** volta in `contenuti/animazioni/*.py`, diventa
un pattern (o un componente). Al massimo **due pattern nuovi per reel**: a fine lavoro l'animatore guarda gli aiuti
locali che ha scritto e dice nel rapporto quali sono candidati.

I componenti stanno altrove: `docs/animazioni.md` §8 (e la vetrina, `uv run python -m tools.anim.vetrina`).

---

## 1. `finestre` — un oggetto alla volta, senza accavallamenti

**Quando**: ogni volta che due cose si succedono nello stesso posto (una parola che lascia il posto a un'altra, tre
figure in fila). È il rimedio ai «testi sovrapposti per 0,3 s» che si vedono solo guardando a 8 fps.

```python
quanto = self.arrotonda(durata / len(tappe))
for i, mob in enumerate(tappe):
    self.play(FadeIn(mob), run_time=self.arrotonda(quanto * 0.35))
    self.wait(quanto * 0.3)
    if i < len(tappe) - 1:
        self.play(FadeOut(mob), run_time=self.arrotonda(quanto * 0.35))   # esce PRIMA che entri il prossimo
```

Scena di prova: `PatternFinestre`.

## 2. `rimbalzo(oltre)` — la carica che non esce dall'area

**Quando**: un oggetto che cresce di colpo (la mossa «carica e rimbalzo»). `rate_functions.ease_out_back` di Manim
arretra del 10 %: su una carta larga 860 px sono ~90 px fuori dall'area contenuto, e il controllo `testo-fuori`
protesta. Questa versione lascia scegliere di quanto sforare.

```python
def rimbalzo(oltre=0.06):
    def f(t):
        s = 1.70158 * (oltre / 0.10)
        t -= 1
        return t * t * ((s + 1) * t + s) + 1
    return f

self.play(carta.animate.become(grande), run_time=0.6, rate_func=rimbalzo(0.06))
```

Scena di prova: `PatternRimbalzo`.

## 3. `grande(s, larghezza_px)` — il corpo più grande che tiene una riga sola

**Quando**: una parola a tutta larghezza (la mossa di tipografia cinetica). `MarkupText` va a capo da solo — Pango
riceve una larghezza fissa e non la si può spegnere — quindi una parola larga diventa due righe senza che il codice
lo chieda, e comporre piccolo e ingrandire distanzia le lettere («SU BIRL A», visto a piena risoluzione).

```python
for ruolo in ("punch", "titolo", "messaggio"):
    blocco = testo(s, ruolo, peso="BOLD")
    if len(blocco.righe) == 1 and blocco.width * 120 <= larghezza_px:
        return blocco
```

Scena di prova: `PatternGrande` (che usa anche il pattern 1: la prima parola esce del tutto prima della seconda).

## 4. `riflesso` — «guarda qui» senza cambiare la figura

**Quando**: si vuole richiamare l'occhio su un oggetto che deve restare **identico**. Una banda chiara scende sopra
e si spegne: non tocca colori né larghezze, quindi la figura non afferma niente di nuovo (se le righe cambiassero,
direbbe «gliel'ha ritoccata lei»).

```python
banda = Rectangle(width=sopra.width * 1.05, height=px(26), stroke_width=0,
                  fill_color=self.cfg.palette.testo, fill_opacity=0.18)
banda.move_to(sopra.get_top() + UP * px(20))
self.add(banda)
self.play(banda.animate.move_to(sopra.get_bottom() + DOWN * px(20)), run_time=0.9)
self.remove(banda)
```

Scena di prova: `PatternRiflesso`.

## 5. `controlla_zoom` — verificare prima di ingrandire

**Quando**: prima di `self.zoom_su(...)`. Con la camera ingrandita quello che esce dalla cornice sparisce: se un
oggetto che deve restare leggibile non ci sta, meglio saperlo da un avviso che da un fotogramma.

```python
larghezza = self.cfg.frame_width / fattore
for m in dentro:
    if m.width > larghezza:
        self.avvisi.append(f"zoom {fattore}×: «{type(m).__name__}» non ci sta")
```

Scena di prova: `PatternZoom`.

## 6. `fine_scena` — l'ultimo fotogramma è il primo della scena dopo

**Quando**: due scene animate di fila senza stacco. L'ultimo fotogramma di una e il primo dell'altra devono
coincidere, altrimenti la dissolvenza mostra due stati diversi. Si dichiara lo stato di fine e la scena dopo lo
ricostruisce; si verifica confrontando i due fotogrammi (`ffmpeg` + differenza dei pixel).

```python
def fine_scena(mobs):
    return {type(m).__name__: (m.get_center()[0], m.get_center()[1], m.width) for m in mobs}
```

Scena di prova: `PatternFineScena`.
