# Scrivere una sceneggiatura

La sceneggiatura è un file markdown a grammatica rigida: da lì escono la validazione, il gobbo per registrare, le
animazioni e il montaggio. La grammatica da copiare è in `templates/reel.md`; un esempio che passa tutti i controlli
è `templates/esempio-reel.md`. Serve allo sceneggiatore e al revisore (persone o agenti).

## 1. Il file

Sta in `contenuti/sceneggiature/`; il nome del file è libero, conta lo `slug`. Il frontmatter:

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
| `hook` | Scena 1, obbligatoria | `TITOLO:` (obbligatorio), `SOTTOTITOLO:` | no (per default) |
| `spiegazione` | nel mezzo (tipo di default) | `VOCE:` obbligatoria | sì, in basso a destra |
| `schermo` | nel mezzo | `SCHERMO:` obbligatorio, `VOCE:` | sì: mettilo in alto (`RIQUADRO: alto-destra`) |
| `chiusura` | ultima, obbligatoria | `MESSAGGIO:` (obbligatorio), `CTA:` | sì |

## 3. Le righe

| Riga | Quante | Cosa |
|---|---|---|
| `VOCE:` | fino a 4 per scena | una frase detta a camera: **una frase = un beat** dell'animazione |
| `ANIMAZIONE:` | una, oppure una per frase `VOCE:` | il brief per l'animatore (sezione 6) |
| `TESTO:` | fino a 4, ≤ 4 parole | parole chiave che compaiono a schermo |
| `TITOLO:` / `SOTTOTITOLO:` | una | solo nell'hook: il titolo regge da solo (≤ 10 parole) |
| `MESSAGGIO:` / `CTA:` | una | solo nella chiusura (messaggio ≤ 25 parole, CTA una riga) |
| `SCHERMO:` | una | un file in `contenuti/media/<slug>/` mostrato nella cornice (b-roll, screen recording, immagine) |
| `RIQUADRO:` | una | `no`, `si`, `basso-destra`, `basso-sinistra`, `alto-destra`, `alto-sinistra` |

Dentro le righe: `==parola==` diventa il colore accento (una per scena: la parola che conta), `**parola**` grassetto.
Una riga che non è nessuna di queste è un errore, con il suggerimento del prefisso più vicino («`VOCI:` → forse
intendevi `VOCE:`»).

## 4. Tempi e limiti

- La durata vera di ogni scena la decide la **clip registrata**. Finché non c'è: stima = parole ÷ 2,8 + 0,8 s
  (minimo 2,5 s; hook senza voce 3,5 s). Nell'anteprima `--prova` la voce sintetica, una frase alla volta con 0,3 s
  di pausa.
- Ogni frase `VOCE:` è un beat: l'animazione di quel beat parte quando comincia la frase. Due cambi a schermo → due
  frasi; una frase lunga con tre cambi dentro non si può animare bene.

Limiti (fonte unica: `tools/reel/validate.py::LIMITI`; oltre il limite è un avviso, salvo dove scritto):

| Cosa | Limite |
|---|---|
| scene | 6-8 (minimo 5, massimo 9) |
| parole di `VOCE:` per scena | ≤ 35 (hook ≤ 15) |
| righe `VOCE:` per scena | ≤ 4 |
| `TITOLO:` / `MESSAGGIO:` | ≤ 10 / ≤ 25 parole (MESSAGGIO consigliato ≤ 12: una frase grande, il resto in caption) |
| VOCE dell'hook | un «tu» o una domanda: l'hook è una promessa a chi guarda (`docs/linguaggio-reel.md` §1) |
| VOCE della chiusura | ≤ 18 parole (~6-7 s): un payoff, non un riassunto |
| `TESTO:` | ≤ 4 per scena, ≤ 4 parole ciascuno |
| `==evidenzia==` / emoji | 1 per scena |
| una scena | 2,5-14 s stimati |
| il reel | 30-60 s stimati (oltre 90 s è un errore) |
| `SCHERMO:` | il file deve esistere (errore); il riquadro non deve coprire la cornice (avviso) |

## 5. Come si scrive la VOCE

- È **parlato**: frasi corte, una cosa per frase, soggetto e verbo. Si legge ad alta voce prima di consegnare.
- **Una frase per cambio a schermo.** 2-3 frasi per scena bastano; se ne servono di più, sono due scene.
- **Hook**: la tesi in meno di 15 parole, detta come un titolo, in 3-5 secondi. Il `TITOLO:` a schermo può essere
  diverso dalla voce, ma dice la stessa cosa.
- **Numeri**: solo veri, con la fonte nelle note di produzione; quelli illustrativi si dichiarano come esempi anche a
  schermo (la `Classifica` lo scrive da sola).
- **Testi attribuiti a un modello** («Comincia così: …», «Ora scrive: …»): solo uscite vere, generate **prima** di
  scrivere la scena (3-5 uscite per richiesta, salvate in `contenuti/media/<slug>/`). Ogni parola viene da una sola
  uscita; i tagli si dichiarano nelle note di produzione e la caption dice modello e data. Il luogo comune da
  mostrare è quello che torna in quasi tutte le uscite. Nel primo reel i due biglietti scritti da noi non sono mai
  usciti in 16 prove, e si sono rifatte le scene 2-7. **Le revisioni del presentatore hanno l'ultima parola**, anche
  su questi testi: un suo ritocco si applica così com'è e la caption lo dichiara («tagliate e ritoccate da noi»).
- **Chiusura**: il messaggio centrale in parole semplici e una sola azione nella `CTA:`.
- Il presentatore leggerà la voce dal gobbo così com'è: niente abbreviazioni, sigle da sciogliere, parole da
  pronunciare in modo ambiguo.

## 6. Il brief ANIMAZIONE

Dice **quali oggetti, cosa cambia e su quale frase**: l'animatore non deve indovinare. Esempio (scena 5
dell'esempio): «Una carta "contesto" con la richiesta del biglietto e, sotto, le candidate con le barre (esempio);
entra la riga "Sii originale." e le barre si muovono appena.» La tabella «male / bene» e i componenti disponibili
(carte, classifiche, flussi, cicli, confronti, tabelle, icone…) sono in `docs/animazioni.md` (§8 e §11).

## 7. Comandi

```
uv run reel valida <file>                       # errori, avvisi, durata stimata per scena e del reel
uv run reel gobbo <file> [--scrivi]             # il testo da leggere, scena per scena
uv run reel monta <file> --prova --anteprima    # anteprima con voce sintetica (dopo le animazioni)
```
`valida` stampa una riga per scena: `2:spieg 23p → ~9s [clip ✘]` (tipo, parole, durata stimata, clip registrata).
