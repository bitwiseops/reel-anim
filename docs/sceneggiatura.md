# Scrivere una sceneggiatura

La sceneggiatura è un file markdown a grammatica rigida: da lì escono la validazione, il gobbo per registrare, le
animazioni e il montaggio. La grammatica da copiare è in `templates/reel.md`; un esempio che passa tutti i controlli
è `templates/esempio-reel/esempio-reel.md`. Serve allo sceneggiatore e al revisore (persone o agenti).

## 0. Il reel si guarda muto

Le regole sono in `docs/regole-editoriali.md` §1-2. Per la grammatica: le **caption** (il parlato scritto,
sincronizzato con la voce, in una fascia in fondo: `[caption]` nel config, `tools/reel/caption.py`) non le disegna
Manim, si **bruciano nel montaggio dopo la registrazione**, sui tempi della presa vera; nell'anteprima `--prova`
compaiono sui tempi della voce sintetica, così l'ingombro si vede prima di registrare. Quindi ogni scena animata ha la
riga `FIGURA:` (cosa si capisce guardando: è quello che il revisore verifica e l'animatore rende vero), e la deroga
`CAPTION: alto` sposta la fascia in cima per le scene in cui il testo *è* il contenuto, dichiarata nelle Note di
produzione. Se la figura non regge, la scena diventa materiale esterno (`[broll]`, anche con immagini Meshy), mai
testo. I controlli `parole-leggibili` e `caption` di `tools/anim/controlli.py` lo fanno rispettare.

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
| `tipo`, `pilastro`, `data_creazione`, `idea` | no | per il calendario |

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
| `hook` | Scena 1, obbligatoria | `TITOLO:` (obbligatorio, per la copertina), `SOTTOTITOLO:`, `VOCE:` | **a tutta tela** (`pieno`, sotto) |
| `spiegazione` | nel mezzo (tipo di default) | `VOCE:` obbligatoria, `FIGURA:` obbligatoria | sì, in alto a destra |
| `schermo` | nel mezzo | `SCHERMO:` obbligatorio, `VOCE:`, `FIGURA:` | sì: in alto (`RIQUADRO: alto-destra`, ora è il default) |
| `broll` | nel mezzo, mai due di fila | `SCHERMO:` obbligatorio, `VOCE:`; niente `TESTO:` | sì, sopra il filmato |
| `chiusura` | ultima, obbligatoria | `MESSAGGIO:` (obbligatorio), `CTA:` | **a tutta tela** (`pieno`, sotto) |

**`schermo` e `broll` non sono la stessa cosa.** In una scena `schermo` il materiale sta nella finestra 900×980 e
intorno c'è la grafica animata: serve a *mostrare* qualcosa (una chat, una schermata). In una scena `broll` si vede
**il filmato a tutto schermo e il riquadro del presentatore, nient'altro**: nessun testo, nessuna grafica, nessuna
classe Manim. Animazione e filmato non stanno mai insieme: si alternano fra scene — Manim spiega, il filmato tiene
l'attenzione. Per questo `valida` avvisa su due `[broll]` di fila e su un reel sbilanciato (sotto), e dà errore su un
`TESTO:` in una scena `[broll]`. La riga `ANIMAZIONE:` lì è facoltativa e non anima niente: descrive **cosa si vede
nel filmato** (soggetto, luogo, gesto), ed è da quella che `broll piano` ricava le query di ricerca.

**I due registri stanno a metà** e **i due estremi sono del presentatore a tutta tela** (`docs/regole-editoriali.md`
§3-4). Per la grammatica:
- l'equilibrio si conta sulle scene in mezzo (apertura e chiusura restano fuori); `valida` e `broll piano` avvisano
  fuori da metà ± una. Il numero di scene lo decide il contenuto, entro `LIMITI`;
- `RIQUADRO: pieno` è il default di `hook` e `chiusura`: niente `ANIMAZIONE:` né `FIGURA:`, nessuna classe Manim. Il
  `TITOLO:` (col `SOTTOTITOLO:`) vive solo in copertina; `MESSAGGIO:` e `CTA:` sono il testo per la caption del post.
  `RIQUADRO: si` riporta la scena al riquadro, `no` lo toglie;
- si registrano con la fotocamera in verticale (1080×1920, `config.toml [registrazione]`): le scene a volto pieno
  tengono il fotogramma intero, le altre ne ritagliano il quadrato del riquadro.

Non si scrive `[broll]` a mano: lo sceneggiatore scrive la scena come `[spiegazione]` con un brief che descrive
un'immagine filmabile; il sottosistema `broll` (`docs/broll.md`) propone quali scene vanno a filmato, il
presentatore sceglie dai provini, e `broll scrivi` cambia il tipo e aggiunge `SCHERMO:` **quando il file esiste già**.
Con `broll scrivi --presto` le scene si marcano subito dopo `broll piano`, prima che il filmato sia scelto e reso:
l'animatore parte intanto sulle altre scene (`reel anima` salta quelle a filmato) mentre si scelgono i filmati. Finché
il file manca `reel valida` dà un **avviso** («filmato non ancora reso») e `reel monta` si ferma con un errore.
Il filmato è reso sulla durata della scena di quel momento: dopo la registrazione `monta` avvisa se la presa vera è
più lunga, e si rifà `broll piano` + `broll rendi` (le scelte restano).

## 3. Le righe

| Riga | Quante | Cosa |
|---|---|---|
| `VOCE:` | più righe (limite in §4) | un pezzo di parlato detto a camera (una o due proposizioni): **una riga = un beat** dell'animazione |
| `ANIMAZIONE:` | una, oppure una per riga `VOCE:` | il brief per l'animatore (sezione 6) |
| `FIGURA:` | una per scena animata (obbligatoria) | cosa si capisce **guardando**, senza leggere niente a schermo, in una riga |
| `TESTO:` | poche, cortissime (§4) | un numero, una percentuale, una parola chiave: è un **extra**, non la spiegazione |
| `CAPTION:` | una | `no` (niente sottotitoli in questa scena) · `alto` (fascia in cima: deroga) · `basso` (default, anche in chiusura a volto pieno) |
| `TITOLO:` / `SOTTOTITOLO:` | una | solo nell'hook: il titolo della copertina, regge da solo |
| `MESSAGGIO:` / `CTA:` | una | solo nella chiusura: il testo della caption del post (CTA una riga) |
| `SCHERMO:` | una | un file in `contenuti/media/<slug>/` mostrato nella cornice (b-roll, screen recording, immagine) |
| `RIQUADRO:` | una | `pieno`, `no`, `si`, `basso-destra`, `basso-sinistra`, `alto-destra`, `alto-sinistra` |

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
| scene | 6-9 (minimo 5, massimo 10): il numero lo decide l'equilibrio fra i due registri |
| parole di `VOCE:` per scena | ≤ 70 (hook ≤ 25: l'aggancio si gioca nei primi secondi) |
| righe `VOCE:` per scena | ≤ 8 |
| `TITOLO:` / `MESSAGGIO:` | ≤ 10 / ≤ 25 parole (MESSAGGIO consigliato ≤ 12: è la frase memorabile della caption del post) |
| VOCE dell'hook | un «tu» o una domanda: l'hook è una promessa a chi guarda (`docs/linguaggio-reel.md` §1) |
| VOCE della chiusura | ≤ 25 parole: la risposta all'hook (o il suo perché), niente battuta |
| lingua parlata | niente frasi da titolo in fila (≤ 4 parole, senza «tu» né «io»), al massimo due nel reel fuori dalla chiusura; **l'eco non conta** (una frase corta che riprende una parola di quella prima: «…quasi quattro ore al giorno. Ogni giorno.»); niente «X, sì. Y, no.»; niente due punti come snodo (valgono solo per citare: «scrive: …») |
| `TESTO:` | ≤ 2 per scena, ≤ 2 parole ciascuno (numeri e percentuali non contano); avviso se ripete parole della VOCE |
| `FIGURA:` | obbligatoria nelle scene animate, ≤ 20 parole |
| testo a schermo (animazione) | mai più di **2 parole di fila**: lo fa rispettare il controllo `parole-leggibili` |
| `==evidenzia==` / emoji | 1 per scena |
| una scena | 2,5-26 s stimati |
| il reel | 30-150 s stimati (conta l'aggancio dei primi 15 s, non la durata; oltre 180 s è un errore) |
| `SCHERMO:` | il file deve esistere (errore in una scena `[schermo]`; in una scena a filmato è un avviso, «non ancora reso», e l'errore lo dà `monta`); il riquadro non deve coprire la cornice (avviso) |

## 5. La VOCE: prima il copione, poi i beat

Scritta per titoli («Fluente, sì. Originale, no.») la VOCE funziona sulla pagina e detta a camera suona recitata:
nessuno parla per aforismi. Per questo **il parlato si scrive prima della sceneggiatura, da un modello esterno, e la
sceneggiatura si adatta a lui**:

0. **Le tappe.** L'idea porta `## Tappe del parlato`: una riga numerata per scena, `N. (registro) i fatti`, con il
   registro `apertura`, `filmato: l'immagine`, `animazione` o `chiusura`; facoltativo `## Suggerimenti per il
   parlato`. È tutto quello che il modello sa del reel, oltre a tema e messaggio: i fatti che non ci sono non entrano.
1. **Il copione.** `uv run reel copione <idea>` compone il prompt da `templates/copione.md` (le regole del parlato)
   con sei trascrizioni intere di reelkit (`[stile] trascrizioni`, una per account, durata vicina al reel): il passo
   del parlato vero non sopravvive a una regola. Lo manda al primo modello della catena `config.toml [copione]
   modelli`; si scende al successivo solo se il precedente fallisce (errore, punti Poe che non bastano, cifre o un
   reel oltre l'errore di `valida` anche dopo **una** correzione chiesta allo stesso modello; le altre lunghezze
   restano avvisi nel frontmatter). A un modello che sfora con costanza si chiede meno (`[copione] taratura`).
   Scrive `contenuti/copioni/<idea>.md` (frontmatter: modello, catena, punti spesi, avvisi di stile) e il prompt
   accanto, aggiunge all'idea `**Copione:**` e porta lo stato a `copione`. `--prova-a-secco` stampa il prompt con
   saldo e stime; `--nota "…"` lo rigenera con una richiesta; `--modello X` usa un solo anello.
2. **I beat.** Lo sceneggiatore prende ogni scena del copione **alla lettera** e la spezza in righe `VOCE:` nei punti
   in cui cambia lo schermo: una riga = un beat = un pezzo di parlato (una o due proposizioni), non per forza una
   frase chiusa. Può dividere una scena in due, non cambiare parole.
3. **Gli scostamenti.** Si cambiano parole solo per un errore di `valida`, per un numero o un termine tecnico in una
   scena a filmato, o per un fatto che l'idea non ha: il minimo, elencato nelle Note di produzione sotto «Scostamenti
   dal copione». Una frase che non convince si segnala; la corregge il presentatore nel copione, o lo rigenera.
4. La revisione a voce la fa il presentatore **registrando** (`docs/regole-editoriali.md` §9).
5. `valida` (e già `reel copione`, negli avvisi del frontmatter) segnala le frasi da titolo in fila, lo schema «X, sì.
   Y, no.» e i due punti usati come snodo: lo sceneggiatore li riporta, non li riscrive.

- **Hook**: una domanda o un problema di chi guarda; non un titolo detto a voce. Il `TITOLO:` vive in copertina e può
  restare la tesi in forma di titolo.
- **Numeri**: solo veri, con la fonte nelle note di produzione (`docs/regole-editoriali.md` §5); quelli illustrativi
  si dichiarano come esempi anche a schermo (la `Classifica` lo scrive da sola).
- **Testi attribuiti a un modello** («Comincia così: …», «Ora scrive: …»): solo uscite vere, generate **prima** di
  scrivere la scena (`uv run reel uscite`, salvate e siglate in `contenuti/idee/uscite/<slug>-<data>.md`: la tappa
  T0b di `/pipeline`). Ogni parola viene da una sola uscita; i tagli si dichiarano nelle note di produzione e la
  caption dice modello e data. Il luogo comune da mostrare è quello che torna in quasi tutte le uscite. I ritocchi
  del presentatore valgono così come sono (`docs/regole-editoriali.md` §7).
- **Chiusura**: il messaggio centrale in parole semplici e una sola azione nella `CTA:`.
- Il presentatore leggerà la voce dal karaoke di `reel registra` così com'è: niente abbreviazioni, sigle da
  sciogliere, parole da pronunciare in modo ambiguo.
- **Struttura da uno schema di reelkit.** L'ideatore sceglie uno schema fra gli «Schemi riutilizzabili» di
  `pattern.md` (chiave `pattern` in `config.toml [stile]`), fatto di tecniche che compaiono in più account, e lo
  adatta nella `## Struttura narrativa` dell'idea; lo sceneggiatore distribuisce le fasi sulle scene e dichiara i tag
  nelle note di produzione. Le firme di un solo account non si copiano, un elenco non si legge a camera, e lo schema
  non scavalca i limiti né questo documento: se contraddice, vince il repo.

## 6. Il brief ANIMAZIONE

Dice **quali oggetti ci sono, cosa cambia e su quale frase**: l'animatore non deve indovinare. Il reel si guarda
muto (§0): il brief non chiede testi a schermo, ma **oggetti, stati e cambiamenti**. Per ogni beat:

1. **cosa c'è** in scena e in che scala (chi è grande, chi è piccolo);
2. **cosa cambia su questa frase**: entra, esce, si muove, si accende, si spezza, si riempie;
3. la **mossa grande** della scena, se c'è (`GRANDE:` davanti alla riga);
4. quali parole restano leggibili: **di norma nessuna**; altrimenti quali e per quanto.

Esempio: «Dieci figure uguali in due file da cinque, tutte spente; sulla voce sei si accendono una
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
