# broll — il materiale esterno dei reel

Sceglie e prepara i filmati che si alternano alle animazioni Manim: un piano visivo per scena, la
ricerca sui banchi di filmati, i provini, il taglio e la resa a tutto schermo.

**È un progetto `uv` a sé.** Ha il suo `pyproject.toml`, il suo `uv.lock` e il suo `.venv`: il lock e
l'ambiente della radice non vedono mai le sue dipendenze. È la ragione per cui esiste questa cartella
invece di un modulo dentro `tools/` — quando arriveranno torch e compagnia (M7, gruppo `ml`), `uv sync`
alla radice continuerà a scaricare i 282 MB di oggi e `uv run reel` resterà istantaneo.

```bash
uv sync --project broll                 # la prima volta
uv run --project broll broll <comando>  # sempre, dalla radice del repo
uv run --directory broll pytest -q      # i suoi test (quelli della radice non li raccoglie)
```

`--project` e non `--directory`: il primo sceglie l'ambiente senza cambiare la cartella corrente, così i
percorsi relativi che passi sulla riga di comando restano quelli che vedi.

## Comandi

| | |
|---|---|
| `broll piano <sceneggiatura.md> [--da-capo]` | propone il piano visivo (rilanciato **tiene candidati e scelte** delle scene che dicono ancora le stesse frasi; se la durata è cambiata la scena torna a `scelto`, da rendere di nuovo): per ogni scena, filmato o animazione, con le query di ricerca. Scrive `contenuti/broll/<slug>/piano.json` |
| `broll stato <slug> [--json]` | a che punto è il piano; con `--json` l'esito nello schema dei workflow |
| `broll cerca <slug> [--scena N] [--max 8]` | cerca i candidati su Pexels (verticali per primi) e li mette nel piano |
| `broll provini <slug> [--scena N]` | contact sheet dei candidati, dalle **miniature**: si sceglie senza scaricare i filmati |
| `broll scegli <slug> --scena N --candidato <fornitore:id> [--da S] [--ancora …] [--aggiungi]` | fissa nel piano il filmato della scena: da che secondo parte, dove si ritaglia un orizzontale (`sinistra \| centro \| destra \| 0-1`). Con `--aggiungi` un secondo taglio nella stessa scena: lo stacco cade sull'inizio frase più vicino alla divisione in parti uguali |
| `broll rendi <slug> [--scena N] [--forza]` | scarica i filmati scelti (cache in `contenuti/media/_cache-broll/`), li ritaglia a 9:16 e scrive `contenuti/media/<slug>/broll-scena-NN.mp4`: 1080×1920, muto, lungo quanto la scena **al fotogramma**. Poi una filmstrip `reso-scena-NN.png` da guardare e `CREDITI.md` |
| `broll scrivi <slug>` | porta nella sceneggiatura le scene **già rese**: il tipo diventa `[broll]` e compare la riga `SCHERMO:`, nient'altro cambia. Non converte una scena con `TESTO:` (toglierlo è una scelta del presentatore) e non salva se il risultato non passa `valida`. Si torna indietro con `git checkout` del `.md` |
| `broll chiavi` | quali chiavi dei servizi esterni sono configurate, **mascherate** |
| `broll prova-inquadratura <slug> --filmato <file>` | lo stesso fotogramma ritagliato a 9:16 in più punti, col riquadro del presentatore sopra |
| `broll prova-immagini <slug> --scena N --immagini …` | immagini ferme montate sugli inizi frase della scena, con la filmstrip per verificare gli stacchi |

## Le chiavi

`MESHY_API_KEY` (+ `MESHY_API_KEY_FALLBACK`), `PEXELS_API_KEY`, `PIXABAY_API_KEY`. I nomi sono quelli
già in uso in `~/Projects/3d-models-ai`, così la stessa chiave serve entrambi i progetti. Si leggono
dall'ambiente, poi da `.env` nella radice del repo, poi da `config.local.toml [broll]`: tutti e tre
fuori da git. Nessun comando stampa mai il valore di una chiave.

## La regola

**Animazione e filmato non stanno mai insieme.** Si alternano fra scene: Manim spiega le cose tecniche,
il filmato tiene l'attenzione. In una scena di filmato si vede il filmato a tutto schermo (1080×1920) e
il riquadro del presentatore sopra, niente altro — nessun testo, nessuna grafica generata.

**I due registri stanno a metà** (regola del presentatore, 2026-09-21): circa metà delle scene va a
filmato, ± una, e `piano` avvisa anche quando sono troppo poche. La divisione vale anche per il parlato:
sulle clip la voce dice le cose generiche, nelle animazioni va la spiegazione complessa. Per questo una
scena con numeri o termini tecnici resta animata: se ne restano troppe, è la sceneggiatura che non sta
dividendo i registri.

C'è un terzo registro, **immagini composte**, per quando non esiste né una clip filmata né una animata:
immagini trovate fuori o generate con Meshy, montate **una per frase** sugli `inizi_frasi_s` che
`report.json` già calcola esatti, così quello che si vede richiama quello che il presentatore sta dicendo
in quel momento. Ogni immagine si muove piano (carrellata a verso alternato), perché un fermo immagine
per otto secondi è il «fermo morto» che `docs/animazioni.md` vieta. Verso il montaggio è identico agli
altri due: **un solo file per scena**, già 1080×1920 e già lungo quanto la scena.

Da qui due conseguenze pratiche. La prima: una scena di filmato **non ha una classe Manim** e non va
renderizzata, quindi il compositing ci mette il filmato al posto della grafica e tutto il resto
(riquadro, audio, transizioni) resta com'è. La seconda: l'unica scelta difficile è il ritaglio, perché
un 16:9 portato a 1920 di altezza diventa largo 3413 e del filmato originale ne resta meno di un terzo.

`prova-inquadratura` serve a quello: mostra lo stesso fotogramma ancorato a sinistra, al centro e a
destra, con il riquadro del presentatore al suo posto, così si vede se il soggetto sopravvive al taglio
e se il volto glielo copre. Il contact sheet è una miniatura: per decidere apri i PNG a grandezza piena,
che il comando elenca.

## Dove finisce cosa

| | in git? | |
|---|---|---|
| `contenuti/broll/<slug>/piano.json` | **sì** | le scelte: id, tagli, autore, licenza, url, sha256 |
| `contenuti/broll/<slug>/CREDITI.md` | **sì** | attribuzione pronta per la didascalia (la scrive `rendi`) |
| `contenuti/media/_cache-broll/` | no | i filmati scaricati, ricostruibili dal piano (li scarica `rendi`) |
| `contenuti/media/<slug>/broll-scena-NN.mp4` | no | il filmato reso per la scena (`rendi`) |
| `contenuti/render/<slug>/broll/` | no | provini e prove di inquadratura |

Il piano è riproducibile, i byte no: la stessa divisione che il repo fa già fra
`contenuti/animazioni/<slug>.py` e `contenuti/render/`.

## Stato

M1 fatta: scheletro, `piano`, `stato`, `prova-inquadratura`. M2 fatta (2026-09-19): il tipo `[broll]` in
`tools/reel/` (model, parser, validate, compositing, monta), così `reel monta` mette il filmato al posto della grafica
Manim. Della M3 ci sono Pexels e i provini (`cerca`, `provini`); della M4 `scegli`, `rendi`, `scrivi` e i crediti.
Mancano Pixabay e Meshy (M3), `taglio.py` per gli stacchi interni al filmato d'origine (M4), l'agente e la tappa
T2b della pipeline (M5). Nessuna dipendenza pesante.

Il giro intero: `piano → cerca → provini → scegli → rendi → scrivi`, poi `uv run reel valida` e `uv run reel monta`.
Dopo la registrazione le scene durano quanto le prese vere: se `monta` avvisa che un filmato è più corto della
scena, `broll piano` (tiene le scelte) e `broll rendi` lo rifanno lungo giusto.

Per provare tutto il giro c'è `broll/esempi/demo-alternanza.md`: sei scene, due d'attenzione. Sui reel
veri il piano dà — correttamente — zero scene a filmato, perché ogni scena ha qualcosa da disegnare.

`rendi` si rifiuta se il filmato finisce prima del taglio: allungarlo con un fermo immagine sarebbe il
«fermo morto» che `docs/animazioni.md` vieta. Si parte prima (`--da`) o si aggiunge un taglio. La durata
che Pexels dichiara è arrotondata al secondo, quindi un candidato «12 s» per una scena di 11,9 è al
limite: il controllo vero lo fa `rendi` contando i fotogrammi del file scritto. Il piano completo e le milestone successive sono in
`~/.claude/plans/prima-di-toccare-qualsiasi-memoized-tiger.md`.

Le query vengono **solo dal brief `ANIMAZIONE:`**, che è già una descrizione di cosa si vede. La VOCE
entra soltanto se il brief manca: un sacchetto delle sue parole più frequenti non descrive un'immagine.
Verificato sui provini il 2026-09-19, dove «pensa scegli fretta cambiata volte» riportava un traliccio,
un'impalcatura e un'auto; con il solo brief i candidati sono tutti pertinenti.

`broll piano` decide con un'euristica: una scena che nomina un meccanismo, una quantità o una figura
della libreria ha qualcosa da disegnare e resta animata; le altre sono scene d'attenzione e vanno a
filmato, alternate e al massimo metà del reel (il bersaglio è proprio metà: sotto metà − una avvisa). Le query di ricerca sono le parole piene del brief
`ANIMAZIONE:` e della `VOCE:`. Dalla M5 decide e scrive l'agente, che legge la scena invece di cercarci
dentro delle parole; questa resta il ripiego.
