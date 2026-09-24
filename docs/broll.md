# broll — il materiale esterno dei reel

Sceglie e prepara i filmati che si alternano alle animazioni Manim: un piano visivo per scena, la
ricerca sui banchi di filmati, le immagini generate, i provini, il taglio e la resa a tutto schermo. Le
regole (registri a metà, metà Pexels e metà Meshy, clip senza volti) sono in `docs/regole-editoriali.md`
§3; la grammatica della scena `[broll]` in `docs/sceneggiatura.md` §2.

Il codice sta in `tools/broll/` e si lancia con `uv run broll <comando>` dalla radice del repo.

## Comandi

| | |
|---|---|
| `broll piano <sceneggiatura.md> [--da-capo]` | propone per ogni scena filmato o animazione, con le query ricavate dal brief `ANIMAZIONE:` (la VOCE solo se il brief manca); rilanciato tiene candidati e scelte. Scrive `contenuti/broll/<slug>/piano.json` |
| `broll stato <slug> [--json]` | a che punto è il piano (con `--json` nello schema dei workflow) |
| `broll cerca <slug> [--scena N] [--max 8]` | cerca i candidati su Pexels (verticali per primi) e li mette nel piano |
| `broll provini <slug> [--scena N]` | contact sheet dei candidati dalle miniature, senza scaricare i filmati |
| `broll scegli <slug> --scena N --candidato <fornitore:id> [--da S] [--ancora …] [--aggiungi]` | fissa il filmato della scena: da che secondo parte, dove si ritaglia un orizzontale; `--aggiungi` un secondo taglio |
| `broll genera <slug> --scena N [--prompt "…"]… [--quante 3] [--forza]` | genera con Meshy le immagini della scena, le mette nel piano e salva il contact sheet `immagini-scena-NN.png` da guardare |
| `broll rendi <slug> [--scena N] [--forza]` | scarica o compone il materiale scelto e scrive `contenuti/media/<slug>/broll-scena-NN.mp4` (1080×1920, muto, lungo quanto la scena), la filmstrip `reso-scena-NN.png` e `CREDITI.md`; si rifiuta se il filmato finisce prima del taglio (si parte prima con `--da` o si aggiunge un taglio) |
| `broll scrivi <slug> [--presto]` | porta nella sceneggiatura le scene rese: tipo `[broll]` e riga `SCHERMO:`, nient'altro; con `--presto` tutte quelle a filmato del piano, anche non ancora rese, così l'animatore parte subito |
| `broll chiavi` | quali chiavi dei servizi esterni sono configurate, **mascherate** |
| `broll prova-inquadratura <slug> --filmato <file>` | lo stesso fotogramma ritagliato a 9:16 in più punti, col riquadro del presentatore sopra: per vedere se il soggetto sopravvive al taglio (apri i PNG a grandezza piena) |

Il giro: `piano → scrivi --presto` (da qui parte l'animatore) `→ cerca → provini → scegli → rendi`; per le scene che
vanno a Meshy `genera → (contact sheet) → rendi`. Dopo la registrazione, se `monta` avvisa che un filmato è più corto
della scena, `broll piano` (tiene le scelte) e `broll rendi` lo rifanno lungo giusto. Banco di prova:
`tests/dati/demo-alternanza.md`.

## Le chiavi

`MESHY_API_KEY` (+ `MESHY_API_KEY_FALLBACK`), `PEXELS_API_KEY`, `PIXABAY_API_KEY`. I nomi sono quelli
già in uso in `~/Projects/3d-models-ai`, così la stessa chiave serve entrambi i progetti. Si leggono
dall'ambiente, poi da `.env` nella radice del repo, poi da `config.local.toml [broll]`: tutti e tre
fuori da git. Nessun comando stampa mai il valore di una chiave.

`broll chiavi` le elenca **mascherate** e dice a cosa servono: Pexels e Pixabay sono la *ricerca* (ne
serve almeno una), Meshy è la *generazione* (`broll genera`; senza, quel comando si ferma e lo dice).
Meshy ha due chiavi perché la seconda è la riserva: quando la prima finisce i crediti — 402, o un corpo
che parla di crediti — la POST si ripete sulla riserva e il polling prosegue **su quella**, perché il
task vive nell'account della chiave che l'ha creato.

## Dove finisce cosa

| | in git? | |
|---|---|---|
| `contenuti/broll/<slug>/piano.json` | **sì** | le scelte: id, tagli, autore, licenza, url, sha256, prompt delle immagini generate |
| `contenuti/broll/<slug>/CREDITI.md` | **sì** | attribuzione pronta per la didascalia (la scrive `rendi`) |
| `~/Library/Application Support/reel-anim/cache-broll/` (`[percorsi] cache_broll`) | no | i filmati scaricati (`rendi`) e le immagini generate, `meshy-<sha1 del prompt>-<n>.png` (`genera`) |
| `contenuti/media/<slug>/broll-scena-NN.mp4` | no | il filmato reso per la scena (`rendi`) |
| `~/Library/Caches/reel-anim/<slug>/broll/` (`[percorsi] lavoro`) | no | provini, prove di inquadratura, strisce di resa: `reel pulisci` |

Il piano è riproducibile, i byte no. Un'immagine generata non si riscarica da nessuna parte: quello che il
piano porta è **il prompt**, ed è quello che la rende rifacibile. Per questo il prompt sta anche in
`CREDITI.md`, dove l'immagine è dichiarata per quello che è — *generata con Meshy*, con modello e data,
senza un autore da citare.
