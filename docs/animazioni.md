# Manuale dell'animatore

Come si scrivono le animazioni dei reel: una classe Manim per scena, con la libreria di `tools/anim/`. Serve
all'agente animatore; la sezione 11 serve anche allo sceneggiatore. Esempio completo e funzionante:
`templates/esempio-reel.md` + `contenuti/animazioni/esempio-reel.py` (7 scene, tutti i componenti).

## 1. Dieci regole d'oro

1. **Una idea per scena.** A fine beat non più di ~6 elementi visibili.
2. **Tutto dentro `self.area.contenuto`**, posizionato con `area.metti(...)`: lascia libere l'interfaccia di
   Instagram e il riquadro del presentatore. Mai `to_edge`/`to_corner`.
3. **Testo solo con `testo()` o con i componenti.** Mai sotto 36 px (`misure.MINIMO_PX`); corpi da `CORPO_PX`.
4. **Un accento per beat.** Il colore accento vuol dire «guarda qui adesso».
5. **`run_time` sempre esplicito**, anche per `Write` (altrimenti lo sceglie Manim in base alla lunghezza).
6. **Mai oltre il confine del beat**: l'ingresso sta nel primo 35-60 % del beat, poi si tiene fermo.
7. **Azzera e ricostruisci**: ogni beat dichiara cosa resta; il resto esce all'inizio del beat dopo.
8. **Spessori dei tratti con `tratto(px)`**, mai con `px()`.
9. **Nei componenti, animazioni composte con `group=self`** quando il componente è già tutto in scena (sezione 10).
10. **Niente LaTeX, niente gradienti, niente colori scritti a mano**: `self.cfg.palette`.

## 2. Ciclo di lavoro

Si parte da una sceneggiatura in `stato: rivisto` (`uv run reel valida <file>` senza errori).

1. Scrivi `contenuti/animazioni/<slug>.py`: una classe `ScenaNN(ScenaReel)` per scena (sezione 3).
2. Renderizza in bassa qualità, una scena alla volta mentre la sistemi:
   ```
   uv run reel anima <file.md> --qualita l --scena 3
   uv run reel anima <file.md> --qualita l --debug      # con le guide: area contenuto, schermo, riquadro
   ```
   `anima` usa gli **stessi tempi dell'anteprima**: se non c'è la clip sintetizza la voce di prova (in cache, una
   frase alla volta) e stampa per ogni scena la durata, gli inizi dei beat e gli avvisi di tempo:
   ```
   scena 2 [spiegazione] 8.1s · beat 0.0 / 3.0 / 5.9 s (voce-sintetica) · manim 0.6s → …/scene/02.png  …
      ⚠ beat(1) parte 0.13 s dopo l'inizio della frase 2: accorcia le animazioni del beat 0
      ✗ testo-piccolo (fine beat 1): «esempio: numeri inventati» alto 30 px (minimo 36) [px 60,812→420,842]
   ```
   `⚠` sono gli avvisi di tempo, `✗` i controlli automatici (sezione 2bis). Con `--json` lo stesso resoconto esce
   come un solo oggetto JSON su stdout (`ok`, `scene[]` con `inizi_frasi_s`, `avvisi_tempi`, `controlli`, e `errore`
   con `traceback` se il render di una scena fallisce: le altre scene vanno avanti). È il formato da leggere per
   l'agente.
3. Guarda, al posto del video (Claude Code non vede i video), in `contenuti/render/<slug>/`:
   - `scene/NN.png`: il fotogramma al 60 % della scena, a piena risoluzione;
   - `fotogrammi/NN-filmstrip.png`: 6 fotogrammi con il loro istante: controlla che ogni ingresso cada sulla sua
     frase e che l'ultimo fotogramma sia completo.
4. Correggi e ripeti: **al massimo 5 giri**. Poi l'anteprima completa:
   ```
   uv run reel monta <file.md> --prova --anteprima
   ```
   e controlla `contact-sheet.png` e `report.json` (per scena: `inizi_frasi_s`, `origine_tempi`, `avvisi_tempi`).
5. **Fotogrammi fitti** prima di consegnare: il filmstrip ne ha 6 e i controlli guardano solo la fine dei beat, così
   un testo che sparisce o lampeggia *durante* un'animazione passa inosservato. Per ogni scena:
   ```
   ffmpeg -v error -y -i contenuti/render/<slug>/_scene/05.mp4 -vf "fps=4,scale=180:-1,tile=14x2" -frames:v 1 <scratchpad>/05.png
   ```
   e guarda l'immagine: nessun testo deve sparire, lampeggiare o finire coperto fra un fotogramma e l'altro.
6. Scrivi le «Note di animazione» nella sceneggiatura (beat scelti, cosa non ci stava, tempi Manim) e porta lo
   stato a `animato`.

Chiudi sempre con un rapporto breve:
```
Stato: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
File: contenuti/animazioni/<slug>.py
Comandi: anima ×N giri, monta --prova --anteprima (reel 51 s, 0 errori, 0 avvisi)
Avvisi rimasti: …
Cosa non ci stava / domande: …
```

## 2bis. Controlli automatici

`ScenaReel` controlla da sola lo stato della scena alla fine di ogni beat (quando chiami `beat(i)`) e alla
chiusura. Ogni violazione dice cosa, quando e dove (px della tela, origine in alto a sinistra); una violazione già
segnalata non si ripete nei beat dopo. **Zero violazioni prima di consegnare.**

| Controllo | Cosa trova | Rimedio |
|---|---|---|
| `testo-piccolo` | testo sotto 36 px (anche dopo uno `scale`) | corpo del ruolo giusto, meno testo; mai scalare sotto il minimo |
| `testo-fuori` | testo fuori dalla safe area (sotto l'interfaccia di Instagram) | `area.metti(...)` dentro `self.area.contenuto` |
| `riquadro` | qualcosa sul riquadro del presentatore | sposta o riduci; nelle scene `schermo` `RIQUADRO: alto-destra` |
| `testo-coperto` | un testo sotto una forma piena disegnata dopo | ordine dentro `play`, `group=self`, `set_z_index` |
| `testi-sovrapposti` | due testi uno sull'altro | `arrange`/`next_to` con `buff`; azzera il beat precedente |
| `colore`, `gradiente` | colori fuori palette (spesso il bianco o il rosso di default di Manim), riempimenti a più colori | `self.cfg.palette` |

Prima del render, un controllo statico del file segnala con il numero di riga i costrutti vietati: LaTeX
(`MathTex`, `Tex`, `BraceLabel`, `DecimalNumber` senza `mob_class=Text`, `BarChart`…), `to_edge`/`to_corner`,
`stroke_width=px(...)`, colori scritti in esadecimale, gradienti, 3D.

Limiti: i controlli guardano i riquadri di ingombro, non i pixel; non vedono il b-roll delle scene `schermo` né le
immagini; il corpo del testo di `Codice` lo garantisce il componente (solleva un errore se non ci sta).

## 3. Anatomia del file

```python
"""Animazioni di «Titolo del reel» (contenuti/sceneggiature/<slug>.md)."""
from manim import DOWN, LEFT, UP, FadeIn, FadeOut, VGroup

from tools.anim.base import ScenaReel
from tools.anim.componenti import Classifica, Etichetta, Frase, testo
from tools.anim.misure import px


class Scena02(ScenaReel):
    """Una riga: cosa racconta la scena."""

    def costruisci(self):
        a, col = self.area.contenuto, self.cfg.palette
        et = Etichetta(self.scena["testo"][0], pieno=False)
        a.metti(et, "alto", "sinistra")
        self.play(et.entra(), run_time=0.4)                  # beat 0: parte subito

        self.beat(1)                                          # la seconda frase della VOCE
        cl = Classifica([("si", 0.62), ("è", 0.21)], larghezza_px=760)
        cl.next_to(et, DOWN, buff=px(110), aligned_edge=LEFT)
        self.play(cl.entra(), run_time=min(1.4, 0.6 * self.durata_beat(1)))
```

- Il nome della classe è `Scena` + numero a due cifre; `costruisci()` al posto di `construct()`; la chiusura
  (`chiudi()`) è automatica e tiene l'ultimo fotogramma fino alla fine della clip.
- **`self.scena`**: i dati della sceneggiatura. Chiavi: `n`, `tipo`, `voce` (lista di frasi), `animazione`,
  `testo` (lista), `titolo`, `sottotitolo`, `messaggio`, `cta`, `schermo`, `riquadro`, `durata_min_s`,
  `transizione`, `inizi_frasi_s`. **Prendi i testi a schermo da qui**, non riscriverli nel codice.
- **`self.area`**: `contenuto` (dove va tutto), `schermo` (cornice del b-roll), `riquadro` (il presentatore,
  `None` se la scena non lo ha). Ogni `Area` ha `x0 y0 x1 y1`, `larghezza`, `altezza`, `centro`, `rettangolo()`,
  `metti()`.
- **`self.cfg.palette`**: `sfondo`, `testo`, `attenuato`, `accento`, `secondario`, `terziario`.

## 4. Tempo e beat

Una scena dura esattamente quanto la clip del presentatore (o la voce di prova). Ogni frase `VOCE:` è un beat.

| Metodo | Cosa fa |
|---|---|
| `self.beat(i)` | aspetta l'inizio della frase `i` (da 0) meno `ANTICIPO_S` (0,1 s: l'occhio arriva con la voce) |
| `self.durata_beat(i)` | secondi dall'inizio della frase `i` alla successiva (o alla fine della scena) |
| `self.fino_a(f)` | aspetta la frazione `f` della scena (per le scene senza VOCE) |
| `self.attendi_fino(s)` | aspetta l'istante `s` |
| `self.arrotonda(s)` | `run_time` arrotondato per difetto a fotogrammi interi |
| `self.t` | il tempo corrente della scena |

Gli inizi delle frasi (`inizi_frasi_s`) sono **esatti** nell'anteprima con voce sintetica (una frase alla volta,
pausa `pausa_frasi_s`); con le clip registrate, per ora, sono **stimati in proporzione alle parole**
(`origine_tempi`: `voce-sintetica`, `parole-clip`, `parole-stima`, `senza-voce`).

Regole:
- **Dentro il beat.** Somma i `run_time` di un beat e confrontala con `durata_beat(i)`: ingresso nel primo
  35-60 %, poi fermo. Se sfori, il beat dopo parte tardi: `beat()` non può tornare indietro e scrive un avviso;
  se sfora l'ultima animazione, il finale viene tagliato (altro avviso). **Zero avvisi prima di consegnare.**
- **Tante `play` corte si allungano**: Manim porta ogni `play` al fotogramma successivo (a 15 fps
  dell'anteprima, 0,21 s diventano 0,27 s). Nei cicli usa `self.arrotonda(...)` oppure un'unica `play`.
- **`run_time` di un gruppo** (`AnimationGroup`, `LaggedStart`) è la durata totale, non quella di ogni pezzo.
- **Ritmo veloce-veloce-LENTO**: i beat di preparazione sono rapidi, il punto chiave ha più tempo.
- **Azzera e ricostruisci**: all'inizio del beat esce ciò che non serve più (0,3-0,5 s), poi entra il nuovo.
  L'ultimo beat non sgombera mai: il suo fotogramma resta fino alla fine (e fa da chiusura).
  ```python
  self.beat(2)
  self.play(FadeOut(vecchio, shift=UP * 0.2), run_time=0.3)
  self.play(nuovo.entra(), run_time=min(1.0, 0.5 * self.durata_beat(2)))
  ```
- **L'uscita somiglia all'entrata**: `Create`↔`Uncreate`, `FadeIn(shift=UP)`↔`FadeOut(shift=UP)`.
- **Una sola enfasi per beat**: `Indicate`, `Circumscribe`, `Evidenzia` o un cambio di colore, non tutti.
- **Curve di velocità** (`rate_func=`): `smooth` (predefinita) quasi sempre; `rush_from` per ingressi decisi;
  `there_and_back` per un impulso che torna com'era; `linear` per riempimenti, contatori, movimenti costanti.
- **`lag_ratio`** 0,1-0,25 per 3-6 voci in sequenza (0 = insieme, 1 = una dopo l'altra).
- **Updater** (`add_updater`, `always_redraw`): alla fine del beat `clear_updaters()`, così il finale è fermo.
  `always_redraw` con del testo ricostruisce Pango a ogni fotogramma: finestre brevi.

## 5. Composizione 9:16

- **L'asse principale è alto → basso.** Sinistra → destra solo per 2-3 elementi corti (es. due etichette).
  In alto il contesto, al centro il fuoco, sotto le conseguenze.
- **Costruisci il gruppo, poi posizionalo**: `VGroup(...).arrange(DOWN, buff=px(40), aligned_edge=LEFT)`, poi
  `a.metti(gruppo, v, h, buff_px)` con `v` = `alto | centro | basso` e `h` = `sinistra | centro | destra`.
  Le relazioni con `next_to(..., buff=px(...))`: il `buff` sempre esplicito.
- **Allineamento a sinistra** per il testo che si legge; centrato solo per un titolo isolato.
- **Se non ci sta**, riduci il contenuto (meno parole, meno voci); scalare il gruppo intero è l'ultima risorsa e
  poi va ricontrollato il corpo minimo di 36 px.
- **Hook**: niente riquadro, l'area contenuto è più alta; il titolo è anche la copertina (fotogramma al 70 %).
- **Scene `schermo`**: il b-roll sta in `self.area.schermo` (lo mette sotto il montaggio); disegna la
  `CorniceSchermo(self.area.schermo)` e le etichette sopra o accanto. Per indicare un punto dell'immagine usa
  `area_px(self.cfg, x0, y0, x1, y1)` in pixel della tela (l'immagine è posata in `[schermo] x, y` del config).
  La cornice (`[schermo]`: x 60, y 600, 900×980 px) lascia libera la fascia alta: nelle scene `schermo` il riquadro
  va in alto (`RIQUADRO: alto-destra` o `alto-sinistra`); `reel valida` avvisa se copre la cornice.
- **Spazio vuoto**: meglio un'area ariosa che dieci elementi piccoli; ma una metà dello schermo vuota per tutta la
  scena è spreco: centra il gruppo nell'area (`a.metti(g, "centro", "sinistra")`).
- **Filo visivo e continuità fra le scene** (il presentatore l'ha apprezzato nel primo reel): 2-3 oggetti che
  ritornano per tutto il reel con lo stesso aspetto, e **ogni scena che parte dall'ultimo fotogramma della
  precedente**, ricostruito con funzioni di impaginazione condivise nel file (`disposizione_NN()`,
  `stato_finale_NN()`): la dissolvenza fra le scene non si vede e gli oggetti non saltano. Esempio:
  `contenuti/animazioni/generativa-non-creativa.py`. Per compattare o far crescere una carta, tienila a pezzi
  (riquadro, titolo, righe) con il riquadro sotto (`set_z_index(-1)`) e passa da uno stato all'altro con `Transform`.

## 6. Testo

| Ruolo (`CORPO_PX`) | px «Hg» | Per |
|---|---|---|
| `titolo` | 104 | hook |
| `punto` | 92 | un concetto isolato a tutto schermo |
| `messaggio` | 84 | chiusura, numeri del `Contatore` |
| `caption` | 48 | frasi, righe delle carte |
| `token` | 44 | cartellini, voci delle classifiche e delle liste |
| `etichetta` | 40 | pillole, titoli delle carte |
| `piede` | 36 | note («esempio: numeri inventati»), handle |

- `testo(s, ruolo, colore=None, peso=None, larghezza_px=None, allinea="left")` ritorna un `Blocco` di righe ad
  **altezza costante** (le righe e i cartellini si allineano sulla linea di base qualunque lettere contengano);
  `larghezza_px` va a capo da solo, `\n` forza l'a capo.
- `blocco.parola("creativa")` ritorna i glifi di una parola, per barrarla, colorarla o farla entrare da sola.
  Cerca la **prima occorrenza come sottostringa**: `parola("la")` trova anche il «la» dentro «parola».
- Nella sceneggiatura `==parola==` diventa colore accento (una per scena) e `**parola**` grassetto: la
  conversione in markup Pango e l'escape di `& < >` li fa `testo()`.
- **`Write` solo per 1-3 parole**; il resto entra con `FadeIn(shift=UP * 0.2)` o `per_righe()`.
- **Parola per parola** con `LaggedStart` (`AddTextWordByWord` in Manim 0.21 è dichiarato rotto):
  ```python
  b = testo("prende una delle più probabili", "caption")
  parole = ["prende", "una", "delle", "più", "probabili"]
  self.play(LaggedStart(*[FadeIn(b.parola(p), shift=UP * 0.1) for p in parole], lag_ratio=0.3), run_time=1.2)
  ```

## 7. Colore

Ruoli fissi in tutto il reel, così chi guarda impara il codice dopo due scene:
- `accento`: «guarda qui adesso» (la scelta, la parola che conta, la riga nuova); uno per beat;
- `testo`: il contenuto; `attenuato`: contesto, cose finite, note, voci scartate (o `fade(0.65)`);
- `secondario` / `terziario`: categorie (es. barre neutre, esito positivo);
- `sfondo`: il riempimento dei riquadri, così coprono ciò che sta sotto.

Niente gradienti, niente colori scritti nel codice, niente rosso/verde come unica differenza.

## 8. Componenti

Import da `tools.anim.componenti`. Tutti sono `VGroup` posizionabili; i metodi ritornano animazioni da `play`.

| Componente | Quando | Animazioni |
|---|---|---|
| `Titolo(s, larghezza_px=900, maiuscolo=True)` | hook, titoli di sezione | `entra()`, `per_righe(lag)`, `.parola(w)` |
| `Messaggio(s, cta=None)` | chiusura | `entra()`, `per_righe()` |
| `Caption(s, area=None)` | didascalia attenuata in fondo all'area | `entra()` |
| `Etichetta(s, colore=None, pieno=True)` | parola chiave a pillola (`TESTO:`) | `entra()`; `.testo` |
| `Barrato(parola)` | «non vuol dire X» (passa `blocco.parola(...)` o un `Blocco`) | `entra()` |
| `Freccia(da, a, s=None, colore=None)` | causa → effetto, «da qui a lì» | `entra()` |
| `Carta(titolo, righe, larghezza_px=900)` | contesto, prompt, biglietto | `entra()`, `aggiungi_riga(s)` |
| `Barra(s, frazione)` | una quantità | `cresci()`, `imposta(f)`, `bersaglio(f)` |
| `Classifica([(s, f), …], larghezza_px, esempio=True)` | candidati con probabilità (nota «esempio» sotto) | `entra()`, `aggiorna(frazioni, riordina=True)`, `scegli(i)`, `token(i)` |
| `Token(parola, colore=None)` | cartellino | `entra()`, `evidenzia()` |
| `Frase(parole, larghezza_px, ancora=punto)` | frase che si compone | `aggiungi(p, da=mob)`, `entra_una_alla_volta()` |
| `Lista(voci)` | 2-5 punti | `entra_una_alla_volta()` |
| `Contatore(valore, etichetta)` | un numero che cambia | `entra()`, `a(n)` |
| `Evidenzia(mob, buff=px(12))` | riquadro accento attorno a qualcosa (con `Create`) | — |
| `CorniceSchermo(area)` | bordo del b-roll | `entra()` |
| `Piede(area)` | handle del canale (vuoto se non configurato: controlla `len()`) | — |

Note: `Evidenzia(buff=...)` è in **unità**, non in px: scrivi `buff=px(12)`. `Classifica.scegli(i)` e
`aggiorna()` usano l'indice originale della voce, anche dopo un riordino. `Frase.aggiungi(token, da=...)` fa
volare il cartellino dal punto `da` (es. `cl.token(0)` dall'etichetta della barra).

Sempre da `tools.anim.componenti`:

| Componente | Quando | Animazioni |
|---|---|---|
| `Icona(nome, altezza_px=120, colore=None)` | un concetto con un simbolo (`Icona.disponibili()`: set Lucide in `assets/icone/`) | `entra()` |
| `ContatoreScorre(valore, etichetta, decimali=0)` | un numero che corre fino al valore (70.000.000.000) | `entra()`, `scorri(a)`, poi `ferma()` |
| `Codice(codice, linguaggio="python")` | 3-6 righe corte (~28 caratteri) di codice o di prompt, colori dalla palette | `entra()`, `righe_una_alla_volta()`, `evidenzia_riga(i)` |

Diagrammi, da `tools.anim.diagrammi`:

| Componente | Quando | Animazioni |
|---|---|---|
| `Flusso(passi, larghezza_px=760)` | passi in colonna uniti da frecce, uno per beat | `entra_passo(i)`, `attiva(i)`, `entra()` |
| `Nodo(s)` | un passo isolato | `entra()`, `accendi()`, `spegni()` |
| `Ciclo(stati, raggio_px=300)` | un ciclo (pensa → agisci → osserva) con un punto che viaggia | `entra()`, `vai()`, `accendi(k)` |
| `Confronto(prima, dopo, titolo_prima, titolo_dopo)` | prima e dopo in colonna | `mostra_prima()`, `boccia()`, `mostra_dopo()` |
| `Corrispondenza(sinistra, destra)` | abbinamenti fra due colonne | `entra()`, `collega(i, j, giusto=True)` |
| `Graffa(mob, s, direzione=RIGHT)` | «questo gruppo è il contesto» | `entra()` |
| `Tabella(righe, intestazione=True)` | poche righe × 2-3 colonne | `entra()`, `evidenzia(r, c=None)`; `cella(r, c)`, `riga(r)` |

Per vederli tutti, anche come esempio d'uso: `uv run python -m tools.anim.vetrina` (una scena di prova per
componente, con i controlli) → `contenuti/render/_vetrina/contact-sheet.png`.

## 9. Trasformazioni

| Animazione | Quando | Attenzione |
|---|---|---|
| `Transform(a, b)` | `a` cambia forma e resta l'oggetto vivo | `b` non entra in scena: dopo si usa `a` |
| `ReplacementTransform(a, b)` | l'identità cambia davvero | dopo si usa `b` |
| `FadeTransform(a, b)` | **testo che diventa un altro testo** | le lettere che «si sciolgono» di `Transform` sono illeggibili |
| `TransformFromCopy(a, b)` | la sorgente resta (una parola «copiata» in una carta) | |
| `TransformMatchingShapes(a, b)` | stesse parole riordinate | stesso font, peso e corpo, altrimenti non combaciano |
| `MoveToTarget` | cambiare più proprietà insieme | `mob.generate_target()`, poi modifica `mob.target` |

**Uno stato intero per beat.** Quando molti beat cambiano la stessa figura (una tabella, una classifica, una
riga di cartellini), costruisci lo stato del beat k a partire dai dati con la **stessa struttura** a ogni k
(stesso numero e ordine di pezzi; un pezzo assente diventa un segnaposto trasparente) e passa da uno all'altro:
```python
def stato(k):   # ritorna un VGroup con sempre gli stessi pezzi
    ...
vista = stato(0)
self.add(vista)
for k in range(1, len(self.inizi_frasi)):
    self.beat(k)
    self.play(Transform(vista, stato(k)), run_time=min(0.8, 0.5 * self.durata_beat(k)))
```
`Transform` fra gruppi accoppia i pezzi **per posizione nel gruppo**: se vuoi vedere un pezzo spostarsi, deve
restare nello stesso posto della lista (è così che `Classifica.aggiorna` fa scambiare le barre).

## 10. Trappole (e rimedio)

- **Spessori invisibili**: `stroke_width` si misura in centesimi di unità (1 = 1,2 px qui). Usa `tratto(px)`.
- **Un riquadro pieno copre il testo**: un `AnimationGroup` o un `LaggedStart` senza `group=` fa aggiungere a
  Manim un gruppo nuovo in cima alla scena. Nei componenti passa `group=self` **se il componente è già tutto in
  scena**; per far entrare solo una parte di un componente ancora fuori scena (`Flusso.entra_passo`) il gruppo non
  va passato, sennò Manim aggiunge in scena anche le parti non ancora entrate. Il controllo `testo-coperto` lo trova.
- **…anche solo durante le animazioni (e lo z_index non basta)**: durante una `play` il renderer disegna gli oggetti
  «in movimento» (dal primo animato nella lista della scena fino in fondo) sopra un'immagine fissa degli altri; lo
  `z_index` vale solo dentro ciascuno dei due insiemi. Un riquadro pieno finito in un gruppo accodato da un
  `LaggedStart` senza `group=` copre i testi fermi in quella `play` e in tutte le successive che animano qualcosa
  che nella lista sta prima di lui: il titolo di una carta che sparisce per mezzo secondo mentre la carta cresce.
  Rimedio: `group=` un oggetto **già in scena** (per una carta tenuta a pezzi, il suo riquadro). I controlli non lo
  vedono (girano a fine beat, a scena ferma): lo trovano solo i fotogrammi fitti (§2, passo 5).
- **`FadeOut` di un `VGroup` nuovo fatto di pezzi già in scena** li lascia in scena, trasparenti: un `FadeOut` per
  pezzo (`*[FadeOut(m) for m in pezzi]`).
- **Un updater lasciato attivo** (es. `ContatoreScorre` senza `ferma()`) fa ridisegnare ogni fotogramma del finale.
- **Ordine di impilamento**: gli oggetti nuovi entrano nell'ordine in cui compaiono dentro `self.play(...)`: il
  fondo prima, il testo dopo. Se serve, `mob.set_z_index(1)`.
- **Due `.animate` sullo stesso oggetto nella stessa `play`: vale solo l'ultima.** Concatenale
  (`box.animate.set_fill(acc).set_stroke(acc)`) o usa `generate_target`.
- **`self.add(x)` e poi `self.play(Create(x))`**: non si vede nulla. O l'uno o l'altro.
- **`AnimationGroup` vuota** solleva un errore: controlla le liste che possono essere vuote (es. `Piede`).
- **LaTeX nascosto (vietato)**: `Brace.get_text()`, `BraceLabel`, `DecimalNumber`/`Integer`/`Variable` (per
  default), i numeri degli assi, le etichette di `BarChart`, `IntegerTable`/`MathTable`. Al loro posto:
  `Brace(...)` + `brace.put_at_tip(testo(...))` o `BraceText`, il nostro `Contatore`, la nostra `Classifica`.
- **Senza LaTeX e utilizzabili**: `Code` (Pygments + Pango; i colori solo da uno stile Pygments), `Table` e
  `MobjectTable` (Pango), `SVGMobject`.
- **Icone SVG**: lo spessore del contorno non scala con `.scale()`, va fissato con `set_stroke(width=tratto(...))`.
- **Immagini** (`ImageMobject`): non sono vettoriali, vanno in un `Group` (non `VGroup`) ed entrano solo con
  dissolvenze o scala.
- **`MoveAlongPath` su una copia di una freccia** segue anche la punta: usa un arco senza punta fra gli stessi
  punti (`ArcBetweenPoints`).
- **`to_edge` e `to_corner`** misurano dal bordo della tela, non dall'area utile: finiscono sotto l'interfaccia.

## 11. Brief ANIMAZIONE: male e bene

Il brief nella sceneggiatura dice **quali oggetti, cosa cambia e su quale frase**. Una riga `ANIMAZIONE:` per
frase `VOCE:` quando i cambi sono più d'uno.

| Male | Bene |
|---|---|
| «Mostra il concetto di contesto.» | «Una carta "contesto" con la richiesta; entra la riga "Sii originale." e le barre si muovono appena.» |
| «Animazione sulla probabilità.» | «Sotto la frase, la colonna di tre candidate con le barre (esempio); la prima si accende e vola in coda.» |
| «Qualcosa che faccia capire che è banale.» | «La frase finita diventa un biglietto; un riquadro accento la incornicia con l'etichetta "la più probabile".» |
| «Grafica accattivante per l'hook.» | «Il titolo entra riga per riga; "creativa" viene barrata; sotto compare "probabile" in accento.» |
| «Spiega i passaggi.» | «Tre passi in colonna, uno per frase; il passo attivo in accento, quelli fatti attenuati.» |
| «Numeri che cambiano.» | «Il contatore sale da 4 a 13 mentre le parole si aggiungono una alla volta.» |

## 12. Prestazioni

- Mentre lavori: `anima --qualita l --scena N` (540×960 a 15 fps: la leggibilità va giudicata sul PNG della
  scena, non sulla bassa qualità).
- `monta` tiene in `_manim/cache.json` una chiave per scena (file delle animazioni, libreria `tools/anim`,
  config, dati della scena con gli inizi delle frasi): se nulla è cambiato la grafica non si rifà. `anima` non usa
  la cache e scrive in `_anima/`.
- Tempi misurati sull'esempio (7 scene, reel di 51 s, Mac M4 Pro):

| Comando | Manim | Totale |
|---|---|---|
| `monta --prova --anteprima` (tutto da rifare) | ~5 s | ~15 s |
| `monta --prova --anteprima` (cache) | 0 s | ~10 s |
| `monta --prova` (piena qualità, 1080×1920) | ~12 s | ~25 s |

## 13. Fonti e crediti

Queste regole sono state distillate e riscritte (nessun testo copiato) dalla documentazione di Manim e da alcune
raccolte della community per agenti di programmazione, adattandole al formato 9:16, a Pango senza LaTeX e alla
nostra libreria. Le trappole sono state verificate sul sorgente di Manim 0.21 o sui render di questo repo.
- [Manim Community 0.21](https://docs.manim.community/en/stable/): galleria di esempi e guide (MIT).
- [adithya-s-k/manim_skill](https://github.com/adithya-s-k/manim_skill), skill «manimce-best-practices» e
  «manim-composer» (MIT, © 2026 Adithya S Kolavi). La skill per ManimGL (CC BY-NC-SA) non è stata usata.
- [vumichien/manim-skill](https://github.com/vumichien/manim-skill): pipeline a ruoli, storyboard validato, rapporto
  finale con stato (Apache-2.0).
- [awesome-skills/manim-skill](https://github.com/awesome-skills/manim-skill): pattern per diagrammi, stati e
  confronti (il README dichiara MIT; il file di licenza non è presente: usato solo come ispirazione).
- [Yusuke710/manim-skill](https://github.com/Yusuke710/manim-skill): punti di sincronia frase → animazione (MIT).
- [manim-voiceover](https://github.com/ManimCommunity/manim-voiceover): l'idea di far partire i beat sulla voce
  (il plugin non è usato).
