# Scrivere una sceneggiatura

La sceneggiatura è un file markdown a grammatica rigida: da lì escono la validazione, il gobbo per registrare, le
animazioni e il montaggio. La grammatica da copiare è in `templates/reel.md`; un esempio che passa tutti i controlli
è `templates/esempio-reel.md`. Serve allo sceneggiatore e al revisore (persone o agenti).

## 0. Il reel si guarda muto (regola del presentatore, 2026-09-20)

Quasi nessuno attiva l'audio. Perciò nel video ci sono le **caption**: il parlato scritto, sincronizzato con la voce,
in una fascia in fondo allo schermo (`[caption]` nel config, `tools/reel/caption.py`). Non le disegna Manim: si
**bruciano nel montaggio dopo la registrazione**, perché i tempi che contano sono quelli della presa vera, non quelli
della voce di prova. Nell'anteprima `--prova` compaiono sui tempi della voce sintetica, così l'ingombro si vede prima
di registrare.

Da qui discende tutto il resto:

1. **L'animazione non contiene testo necessario a capire.** Chi guarda sta leggendo la caption: non può leggere anche
   una frase a schermo. Vanno bene **numeri, percentuali, una parola** (due solo se sono un'espressione sola:
   «Fondo Monetario», «19 punti»). Non vanno bene le frasi, i documenti, le citazioni.
2. **L'esempio si deve poter mostrare.** Prima di fissarlo, chiediti «che figura è?»: una quantità, un gesto, un
   prima/dopo, due forme a confronto, qualcosa che si rompe o si riempie. Se il punto dell'esempio è *quali parole*
   (una mail, un prompt, l'uscita di un modello), o si cambia esempio o serve una deroga dichiarata.
3. **Ogni scena animata ha la riga `FIGURA:`**: una riga che dice cosa si capisce guardando, senza leggere niente.
   È quello che il revisore verifica e che l'animatore deve rendere vero.
4. **Deroga**: `CAPTION: alto` sposta la fascia in cima e libera il fondo, per le scene in cui il testo *è* il
   contenuto. Al massimo **due scene per reel**, dichiarate nelle Note di produzione. Un reel intero in deroga non si
   fa: si cambia esempio.
5. **Se la figura non regge, si cambia registro, non si scrive.** Quando un concetto non si riesce ad animare, o è
   troppo complesso per spiegarlo in pochi secondi con una figura, la scena diventa **materiale esterno**: una clip
   pertinente (`[broll]`, sottosistema `broll/`) oppure **immagini generate con Meshy** messe in
   `contenuti/media/<slug>/` e richiamate con `SCHERMO:`. Il testo a schermo non è mai il ripiego: è la cosa che chi
   guarda non può leggere.
6. Nella **chiusura** le caption sono spente (`CAPTION: no` è il default per quel tipo): il `MESSAGGIO:` è già la
   frase detta, scritta grande. Stessa cosa dove l'animatore usa un `punch`.

I controlli automatici lo fanno rispettare: `parole-leggibili` (mai più di due parole di fila a schermo, salvo
etichette marcate) e `caption` (niente disegni dentro la fascia) in `tools/anim/controlli.py`.

## 1. Il file

Sta in `contenuti/sceneggiature/`, con nome `AAAA-MM-GG-<slug>.md` (la data della prima stesura); per il codice
conta solo lo `slug`. Il frontmatter:

| Campo | Obbligatorio | Cosa |
|---|---|---|
| `titolo` | sì | il titolo di lavoro |
| `slug` | sì | dà il nome a tutto il resto: `contenuti/animazioni/<slug>.py`, `contenuti/media/<slug>/` (clip, b-roll), `contenuti/render/<slug>/` |
| `formato` | sì | sempre `reel` |
| `messaggio_centrale` | sì | una frase: cosa si porta a casa chi guarda |
| `stato` | no | `sceneggiatura → rivisto → animato → montato → approvato → pubblicato` |
| `tipo`, `pilastro`, `data_creazione`, `idea` | no | per il calendario e il cruscotto |

Dopo le scene si possono aggiungere le sezioni `## Note di produzione`, `## Revisione tecnica`, `## Note di
animazione`, `## Pacchetto social`: non vanno a schermo. I commenti HTML `<!-- … -->` sono ignorati ovunque.

## 2. Le scene

```
## Scena N [tipo, durata=6s, transizione=taglio]
```
N consecutivo da 1; il primo flag è il tipo; `durata=` (anche `500ms`) è la durata minima, o la durata di una scena
senza voce; `transizione=taglio | dissolvenza` viene letta ma per ora il montaggio usa quella del config per tutte
le giunzioni.

| Tipo | Dove | Righe proprie | Riquadro del presentatore |
|---|---|---|---|
| `hook` | Scena 1, obbligatoria | `TITOLO:` (obbligatorio), `SOTTOTITOLO:`; con `SCHERMO:` è un hook a filmato (sotto) | no (per default); sì nell'hook a filmato |
| `spiegazione` | nel mezzo (tipo di default) | `VOCE:` obbligatoria, `FIGURA:` obbligatoria | sì, in alto a destra |
| `schermo` | nel mezzo | `SCHERMO:` obbligatorio, `VOCE:`, `FIGURA:` | sì: in alto (`RIQUADRO: alto-destra`, ora è il default) |
| `broll` | nel mezzo, mai due di fila | `SCHERMO:` obbligatorio, `VOCE:`; niente `TESTO:` | sì, sopra il filmato |
| `chiusura` | ultima, obbligatoria | `MESSAGGIO:` (obbligatorio), `CTA:` | sì |

**`schermo` e `broll` non sono la stessa cosa.** In una scena `schermo` il materiale sta nella finestra 900×980 e
intorno c'è la grafica animata: serve a *mostrare* qualcosa (una chat, una schermata). In una scena `broll` si vede
**il filmato a tutto schermo e il riquadro del presentatore, nient'altro**: nessun testo, nessuna grafica, nessuna
classe Manim. Animazione e filmato non stanno mai insieme: si alternano fra scene — Manim spiega, il filmato tiene
l'attenzione. Per questo `valida` avvisa su due `[broll]` di fila e su più di metà reel a filmato, e dà errore su un
`TESTO:` in una scena `[broll]`. La riga `ANIMAZIONE:` lì è facoltativa e non anima niente: descrive **cosa si vede
nel filmato** (soggetto, luogo, gesto), ed è da quella che `broll piano` ricava le query di ricerca.

**L'hook a filmato (decisione del presentatore, 2026-09-19).** I primi 5-10 secondi devono catturare l'attenzione:
il presentatore, **nel riquadro**, pone un problema o una domanda, e dietro c'è **una clip che lo richiama**. È uno
`[hook]` con la riga `SCHERMO:`: a schermo non c'è nessun titolo e nessuna grafica, il riquadro c'è per default
(`si`, non `no`), la `VOCE:` è obbligatoria. Il `TITOLO:` resta obbligatorio ma **vive solo in copertina** (e il
`SOTTOTITOLO:` con lui): scrivilo per chi vede la griglia del profilo, non per chi sta guardando il reel. Conta
nell'alternanza come una scena a filmato: la Scena 2 dopo un hook a filmato è animata. La riga `ANIMAZIONE:`
dell'hook descrive **cosa si vede nella clip** (chi, dove, che gesto): se invece parla del titolo, `broll piano`
lascia l'hook a Manim, com'era prima.

Non si scrive `[broll]` a mano (né `SCHERMO:` nell'hook): lo sceneggiatore scrive la scena come `[spiegazione]` con un brief che descrive
un'immagine filmabile; il sottosistema `broll` (`broll/README.md`) propone quali scene vanno a filmato, il
presentatore sceglie dai provini, e `broll scrivi` cambia il tipo e aggiunge `SCHERMO:` **quando il file esiste già**.
Il filmato è reso sulla durata della scena di quel momento: dopo la registrazione `monta` avvisa se la presa vera è
più lunga, e si rifà `broll piano` + `broll rendi` (le scelte restano).

## 3. Le righe

| Riga | Quante | Cosa |
|---|---|---|
| `VOCE:` | fino a 5 per scena | un pezzo di parlato detto a camera (una o due proposizioni): **una riga = un beat** dell'animazione |
| `ANIMAZIONE:` | una, oppure una per riga `VOCE:` | il brief per l'animatore (sezione 6) |
| `FIGURA:` | una per scena animata (obbligatoria) | cosa si capisce **guardando**, senza leggere niente a schermo (≤ 20 parole) |
| `TESTO:` | fino a 2, ≤ 2 parole | un numero, una percentuale, una parola chiave: è un **extra**, non la spiegazione |
| `CAPTION:` | una | `no` (niente sottotitoli in questa scena) · `alto` (fascia in cima: deroga) · `basso` (default) |
| `TITOLO:` / `SOTTOTITOLO:` | una | solo nell'hook: il titolo regge da solo (≤ 10 parole) |
| `MESSAGGIO:` / `CTA:` | una | solo nella chiusura (messaggio ≤ 12 parole consigliate, 25 al massimo; CTA una riga) |
| `SCHERMO:` | una | un file in `contenuti/media/<slug>/` mostrato nella cornice (b-roll, screen recording, immagine) |
| `RIQUADRO:` | una | `no`, `si`, `basso-destra`, `basso-sinistra`, `alto-destra`, `alto-sinistra` |

Dentro le righe: `==parola==` diventa il colore accento (una per scena: la parola che conta), `**parola**` grassetto.
Una riga che non è nessuna di queste è un errore, con il suggerimento del prefisso più vicino («`VOCI:` → forse
intendevi `VOCE:`»).

## 4. Tempi e limiti

- La durata vera di ogni scena la decide la **clip registrata**. Finché non c'è: stima = parole ÷ 2,8 + 0,8 s
  (minimo 2,5 s; hook senza voce 3,5 s). Nell'anteprima `--prova` la voce sintetica, una frase alla volta con 0,3 s
  di pausa.
- Ogni riga `VOCE:` è un beat: l'animazione di quel beat parte quando comincia la riga. Due cambi a schermo → due
  righe; una riga lunga con tre cambi dentro non si può animare bene. La riga non deve essere una frase chiusa: può
  essere una proposizione («e non è che il testo lo va a cercare,»), purché sia un pezzo di parlato che si dice tutto
  d'un fiato.

Limiti (fonte unica: `tools/reel/validate.py::LIMITI`; oltre il limite è un avviso, salvo dove scritto):

| Cosa | Limite |
|---|---|
| scene | 6-8 (minimo 5, massimo 9) |
| parole di `VOCE:` per scena | ≤ 50 (hook ≤ 20) |
| righe `VOCE:` per scena | ≤ 5 |
| `TITOLO:` / `MESSAGGIO:` | ≤ 10 / ≤ 25 parole (MESSAGGIO consigliato ≤ 12: una frase grande, il resto in caption) |
| VOCE dell'hook | un «tu» o una domanda: l'hook è una promessa a chi guarda (`docs/linguaggio-reel.md` §1) |
| VOCE della chiusura | ≤ 18 parole (~6-7 s): un payoff, non un riassunto |
| lingua parlata | niente frasi da titolo in fila (≤ 4 parole, senza «tu» né «io»), al massimo una nel reel fuori dalla chiusura; niente «X, sì. Y, no.»; niente due punti come snodo (valgono solo per citare: «scrive: …») |
| `TESTO:` | ≤ 2 per scena, ≤ 2 parole ciascuno (numeri e percentuali non contano); avviso se ripete parole della VOCE |
| `FIGURA:` | obbligatoria nelle scene animate, ≤ 20 parole |
| testo a schermo (animazione) | mai più di **2 parole di fila**: lo fa rispettare il controllo `parole-leggibili` |
| `==evidenzia==` / emoji | 1 per scena |
| una scena | 2,5-19 s stimati |
| il reel | 30-90 s stimati (oltre 120 s è un errore) |
| `SCHERMO:` | il file deve esistere (errore); il riquadro non deve coprire la cornice (avviso) |

## 5. Come si scrive la VOCE: prima il monologo, poi i beat

Il presentatore, registrando il primo reel (2026-09-15), ha trovato la VOCE «molto poco umana»: letta a camera era una
fila di titoli («Vuol dire probabile.», «Fluente, sì. Originale, no.», «Il testo non lo cerca: lo scrive lei.»). Scritti
funzionano, detti suonano recitati: nessuno parla per aforismi. Da allora:

0. **Prima ancora si ascolta.** `uv run reel stile --trascrizioni --lingua it` elenca i reel veri trascritti in
   reelkit, col percorso del testo: se ne leggono **quattro-sei interi**, di almeno tre account diversi e di durata
   vicina alla nostra, prima di scrivere una riga. La guida `docs/stile-parlato.md` dà le regole, le trascrizioni danno
   l'orecchio: chi parla davvero allunga la frase con «che… e che…», riprende il soggetto in coda («non ne vediamo
   traccia, di questi alieni»), si fa le domande da solo («E allora perché?»), infila «tra l'altro», «appunto», «ben»,
   dà il numero preciso, e non chiude ogni frase con il fiocco. Si prende **il passo, non le frasi**: sono reel di
   altri, e Whisper sbaglia i nomi, quindi da lì non si prende nessun fatto e nessuna battuta.
1. **Prima si scrive il parlato intero della scena**, come lo si direbbe a un collega: con «io» e «tu», i connettivi
   («quindi», «cioè», «guarda», «e non è che…»), il verbo in ogni frase, qualche ripresa. Frasi di 6-18 parole di norma; una catena parlata («…e quindi… che poi…»)
   può arrivare a 25 se si dice in un fiato.
2. **Poi lo si spezza in righe `VOCE:`** nei punti in cui cambia lo schermo: una riga = un beat = un pezzo di parlato
   (una o due proposizioni), non per forza una frase chiusa. 2-5 righe per scena.
3. **La prova dell'orecchio**: metti il tuo monologo accanto a una delle trascrizioni lette. Se a colpo d'occhio si
   capisce qual è quello scritto — frasi tutte della stessa lunghezza, simmetrie («Non sbagli a X. Sbagli se Y.»),
   terne, ogni frase che chiude un pensiero — è ancora scritto: scioglilo. Il parlato vero è **asimmetrico**.
   E poi: lo diresti così al bar? Se una riga si può leggere solo come un titolo, riscrivila con un verbo.
   Punta a un solo aforisma, la battuta finale: nella chiusura è libera, fuori `valida` ne tollera uno.
4. `valida` avvisa sulle frasi da titolo in fila, sullo schema «X, sì. Y, no.» e sui due punti usati come snodo; lo
   sceneggiatore li porta a zero. La verifica vera è il presentatore che la legge in `reel registra`.

Esempio (scena 4 del primo reel). Scritto: «A ogni bivio, di solito, vince la strada più battuta. Il testo non lo
cerca: lo scrive lei. Fluente, sì. Originale, no.» Parlato: «Quindi a ogni bivio, quasi sempre, prende la strada più
battuta. E non è che il testo lo va a cercare da qualche parte: lo scrive lei, una parola dopo l'altra. Viene fuori
fluente, certo. Ma originale no, non può esserlo.» Stesso contenuto, stessi quattro beat, il doppio delle parole.

- **Hook**: una domanda o una promessa a chi guarda in ≤ 20 parole, in 4-8 secondi (20 parole ≈ 8 s); non un titolo
  detto a voce. Il `TITOLO:` a schermo resta la tesi in forma di titolo.
- **Numeri**: solo veri, con la fonte nelle note di produzione; quelli illustrativi si dichiarano come esempi anche a
  schermo (la `Classifica` lo scrive da sola).
- **Testi attribuiti a un modello** («Comincia così: …», «Ora scrive: …»): solo uscite vere, generate **prima** di
  scrivere la scena (5 per richiesta con Opus e 5 con Sonnet, salvate e siglate in
  `contenuti/idee/uscite/<slug>-<data>.md`: la tappa T0b di `/pipeline`). Ogni parola viene da una sola
  uscita; i tagli si dichiarano nelle note di produzione e la caption dice modello e data. Il luogo comune da
  mostrare è quello che torna in quasi tutte le uscite. Nel primo reel i due biglietti scritti da noi non sono mai
  usciti in 16 prove, e si sono rifatte le scene 2-7. **Le revisioni del presentatore hanno l'ultima parola**, anche
  su questi testi: un suo ritocco si applica così com'è e la caption lo dichiara («tagliate e ritoccate da noi»).
- **Chiusura**: il messaggio centrale in parole semplici e una sola azione nella `CTA:`.
- Il presentatore leggerà la voce dal karaoke di `reel registra` così com'è: niente abbreviazioni, sigle da
  sciogliere, parole da pronunciare in modo ambiguo.

- **Struttura da uno schema di reelkit.** L'ideatore sceglie uno schema fra gli «Schemi riutilizzabili» di
  `pattern.md` (chiave `pattern` in `config.toml [stile]`), fatto di tecniche che compaiono in più account, e lo
  adatta nella `## Struttura narrativa` dell'idea; lo sceneggiatore distribuisce le fasi sulle scene e dichiara i tag
  nelle note di produzione. Le firme di un solo account non si copiano, un elenco non si legge a camera, e lo schema
  non scavalca i limiti né questo documento: se contraddice, vince il repo.

## 6. Il brief ANIMAZIONE

Dice **quali oggetti ci sono, cosa cambia e su quale frase**: l'animatore non deve indovinare. Da quando il reel si
guarda muto (§0) il brief non chiede più testi a schermo, ma **oggetti, stati e cambiamenti**. Per ogni beat:

1. **cosa c'è** in scena e in che scala (chi è grande, chi è piccolo);
2. **cosa cambia su questa frase**: entra, esce, si muove, si accende, si spezza, si riempie;
3. la **mossa grande** della scena, se c'è (`GRANDE:` davanti alla riga);
4. quali parole restano leggibili: **di norma nessuna**; altrimenti quali e per quanto.

Esempio, regime nuovo: «Dieci figure uguali in due file da cinque, tutte spente; sulla voce sei si accendono una
dopo l'altra e sotto resta il numero grande, con l'etichetta della fonte.» Niente frasi a schermo: il concetto è
nella quantità.

La tabella «male / bene» e i componenti disponibili — quelli che spiegano **senza parole** (quantità a pittogrammi,
sagome di un documento, gesto, verdetto, lente, prima/dopo) e quelli che invece sono contenitori di testo, da usare
solo con una deroga dichiarata — sono in `docs/animazioni.md` (§8 e §11).

## 7. Comandi

```
uv run reel valida <file>                       # errori, avvisi, durata stimata per scena e del reel
uv run reel gobbo <file> [--scrivi]             # il testo da leggere, scena per scena
uv run reel monta <file> --prova --anteprima    # anteprima con voce sintetica (dopo le animazioni)
```
`valida` stampa una riga per scena: `2:spieg 23p → ~9s [clip ✘]` (tipo, parole, durata stimata, clip registrata).
