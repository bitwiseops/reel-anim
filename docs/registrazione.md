# Registrare le clip del presentatore

Ogni scena ha **una clip del presentatore**: la sua durata decide la durata della scena, la sua voce è l'audio del
reel, il suo volto va nel riquadro. Le clip si registrano con `uv run reel registra <file>` (§6): una **presa unica**
mentre scorre l'anteprima del reel, spezzata poi per scene. In alternativa si girano con il telefono e si copiano a
mano (§4); in quel caso il gobbo è `uv run reel gobbo <file> --scrivi` → `contenuti/media/<slug>/gobbo.txt`.

## 1. Prima di registrare

- La sceneggiatura è rivista, le animazioni sono fatte e l'anteprima `uv run reel monta <file> --prova --anteprima`
  è stata guardata e approvata: `registra` riproduce **quella** anteprima e ne usa i tempi. `monta --prova` ne lascia
  una copia stabile (`report-prova.json`, `reel-prova.mp4`) che il montaggio con le clip vere non sovrascrive: si può
  registrare di nuovo anche dopo aver montato.
- Se la sceneggiatura cambia dopo l'anteprima, rifai `monta --prova --anteprima` (l'app avvisa: «anteprima di una
  versione precedente»).

## 2. Inquadratura e luce

- Il riquadro è un cerchio di 360 px: volto al centro, testa e spalle, senza tagliare il mento. Nell'app il cerchio
  è disegnato sulla webcam e **prima di registrare lo puoi spostare e zoomare** (trascina col mouse, rotella o `+`/`−`
  per lo zoom, `W A S D` per spostarlo, `0` per tornare al quadrato centrale): la scelta resta in
  `contenuti/media/<slug>/inquadratura.json` e vale per le prese successive. Non si può scendere sotto 360 px di
  lato: il riquadro non ingrandisce mai i pixel. Con clip esterne il montaggio prende il quadrato centrale.
- **L'app registra in verticale, 1080×1920** (dal 2026-09-21: la fotocamera integrata la offre nativa). Serve per
  **apertura e chiusura, che sono a volto pieno**: lì si usa il fotogramma intero, senza ingrandire niente, e nella
  clip `scena-NN.mov` non c'è ritaglio. Nelle altre scene il montaggio ne prende il quadrato dell'inquadratura per il
  cerchio. Quindi inquadrati pensando a tutti e due: **nel fotogramma intero** (testa e spalle, spazio sopra la
  testa, niente di disordinato alle spalle, perché nell'apertura e nella chiusura si vede tutto) e **nel cerchio**.
  Nell'app, durante le scene a volto pieno il pannello del reel mostra la webcam a tutto schermo.
- Con clip esterne vanno bene verticale e orizzontale: il montaggio riempie la tela e ritaglia al centro, e per il
  cerchio porta il lato corto a 360 px. Un'orizzontale a volto pieno però va ingrandita di quasi il doppio: meglio
  girarle in verticale.
- Luce frontale e morbida, sfondo semplice, sguardo in camera. **Con poca luce la fotocamera scende a 15 fps**: il video
  della presa va a scatti (l'audio no).
- iPhone: HEVC e video ruotati vanno bene, il montaggio li ricodifica e li raddrizza.

## 3. Voce

- Nell'app: leggi il testo **karaoke** al ritmo con cui si accende. Le parole si accendono con i tempi della voce di
  prova: sono i tempi su cui l'animatore ha agganciato i beat, quindi l'animazione resta sincronizzata con te.
- Con il telefono: **mezzo secondo di silenzio** prima e dopo, **una breve pausa tra una frase e l'altra** (ogni frase
  è un beat).
- Microfono vicino, stanza silenziosa; il volume lo uniforma il montaggio (loudnorm a −16 LUFS).
- Leggi la frase così com'è scritta: se la cambi, va cambiata anche la sceneggiatura (e forse l'animazione).

## 4. I file

- Nome `scena-NN.mov` (vanno bene anche `.mp4`, `.webm`, `.m4v`) in `contenuti/media/<slug>/`, con NN a due cifre come
  nella sceneggiatura. Dal telefono: AirDrop e rinomina.
- Accanto alle clip tagliate da `registra` c'è `scena-NN.json` (gli inizi delle frasi seguiti nella presa). Una clip
  esterna non ce l'ha: i suoi beat vengono stimati a parole.
- Rifare una scena vuol dire sostituire solo quel file (con `registra`: una presa da quella scena).
- Controllo:
  ```
  uv run reel clip <file>
  ```
  per ogni scena ✔ o ✘, la durata, lo scarto dalla stima e da dove vengono i beat (`dalla presa` o `stimati`); oltre
  ±30 % compare un avviso (una frase saltata, o letta troppo lenta).

## 5. Il montaggio con le clip

- `uv run reel monta <file>` (senza `--prova`): ogni scena dura quanto la sua clip; una scena con voce ma senza clip è
  un errore «clip mancante». Con `--anteprima` è veloce, per guardare.
- Con le clip di `registra` gli inizi delle frasi sono **esatti** (`origine_tempi: presa` in `report.json`); con clip
  esterne sono **stimati in proporzione alle parole** fra i due silenzi di mezzo secondo (`parole-clip`). Se il numero
  di frasi nel sidecar non torna con la sceneggiatura, il montaggio avvisa e torna alla stima: registra di nuovo la scena.
- Poi: pacchetto social, approvazione, pubblicazione. Mai pubblicare un montaggio `--prova`; la pubblicazione la
  lancia il presentatore.

## 6. Registrazione guidata: `uv run reel registra <file>`

Un'app desktop (Tkinter + ffmpeg avfoundation) con tre pannelli: **la webcam** con il cerchio del riquadro, **il reel
con te dentro** (l'anteprima `--prova` con il tuo volto live nel riquadro, dove lo metterà il montaggio) e **il testo
karaoke** (la frase in corso con le parole che si accendono, la frase prima e quella dopo attenuate). I tre pannelli
stanno in fila **sopra**, con **il karaoke al centro** fra webcam e reel e la finestra centrata in alto: il testo
cade sotto la fotocamera del portatile e leggendo lo sguardo resta in camera (2026-09-23). I pannelli e prendono l'altezza che lo schermo lascia libera (`altezza_pannelli_px` in `[registrazione]`
per forzarla); **sotto** ci sono le scene (cliccabili), i pulsanti (● Registra, ▶ Prova, ■ Ferma, ◀ ▶ scena), su una
riga a parte i menu di microfono e fotocamera, e la riga di stato ad altezza fissa. All'avvio l'app misura la finestra
vera e, se sborda dallo schermo, rifà i pannelli più bassi (2026-09-23: sul portatile i comandi uscivano di sotto e di
lato anche a tutto schermo).
**Vu-meter** (2026-09-23): accanto ai menu dei dispositivi c'è il livello del microfono, acceso anche fuori dalla
presa: verde fra −18 e −3 dB di picco (il bersaglio), giallo se basso o alto, rosso se troppo basso o se satura
(«ha saturato» resta scritto). Il 23/09 le prese erano a −37 LUFS: alza il volume d'ingresso in Impostazioni di Sistema
→ Suono → Ingresso finché il parlato normale sta nel verde. Il montaggio pulisce la voce e la porta a −14 LUFS
(`config.toml [audio]`, `uv run reel audio <file>` per il prima/dopo), ma un segnale più alto in partenza porta meno
rumore.

Come funziona:
1. Scegli la scena di partenza con ← → o una cifra (default: la prima senza clip). Il pannello centrale mostra il
   fotogramma chiave di quella scena.
2. **Spazio**: l'app apre fotocamera e microfono (la prima volta macOS chiede il permesso per l'app del terminale), fa
   il conto alla rovescia 3-2-1 e parte: il reel scorre da **2 s prima** della scena scelta (così l'attacco è naturale)
   e la registrazione è continua. Il reel è muto: il microfono registra te.
3. La presa finisce a fine reel (o con **Spazio** per fermarla prima). L'app taglia subito le scene **coperte per
   intero** dalla presa in `scena-NN.mov` + `scena-NN.json`; una scena interrotta a metà non viene salvata.
Prima della presa puoi fare una **prova senza registrare** (`P` o ▶ Prova): il reel scorre dalla scena scelta con il
   volto live e il karaoke, ma non si apre il microfono e non si salva niente; Spazio, ■ o Esc la fermano.
4. Sbagliato qualcosa? Scegli la scena e rifai da lì: la presa nuova sostituisce solo le scene che copre.
   **Esc** esce (in presa: ferma, taglia, poi esce).

**Il testo si corregge qui** (2026-09-22): fuori dalla presa, da fermo o durante la prova, `E` (o ✎ Modifica testo)
rende modificabile il pannello del karaoke con le righe della scena scelta, una per frase (`==parola==` per l'evidenza
nelle caption). ⌘↩ salva, Esc annulla. Le righe devono restare tante quante le VOCE (i beat sono legati alle frasi);
vanno in `parlato.json` e la presa successiva le mostra nel karaoke e le scrive nel sidecar (`voce`). Il montaggio fa
le caption dal testo recitato; `uv run reel parlato <file>` mostra le differenze con la sceneggiatura e `--applica` ce
le riporta. Le scene con il testo cambiato hanno «✎» nella striscia e nel riepilogo finale.

Dove finiscono le cose, in `contenuti/media/<slug>/` (gitignored):
- `scena-NN.mov` (h264, quadrato dell'inquadratura scelta, audio PCM: lossless, lo ricodifica il montaggio) e
  `scena-NN.json`;
- `_prese/presa-NN.mov` (solo video) + `presa-NN.wav` (l'audio) + `presa-NN.log` (le prese intere, ~60 MB al minuto:
  si possono cancellare a montaggio approvato) e `_prese/prese.json` (registro: da quale istante del reel è partita
  ogni presa, quali scene ha dato, con quale inquadratura).

Il video lo cattura ffmpeg (avfoundation), **l'audio lo registra Python con PortAudio** (`sounddevice`): la cattura
audio di avfoundation perde il 10-15 % dei pacchetti (audio che finisce prima del video, gracchiante), PortAudio no.

Fotocamera e microfono si scelgono **dai due menu sotto la webcam** (prima di registrare; cambiando la fotocamera
l'anteprima riparte): la scelta resta salvata per nome in `contenuti/media/dispositivi.json` e vale per tutti i reel
su questa macchina. In alternativa `--dispositivi` elenca i dispositivi e `--video N --audio N` (indice o parte del
nome, anche in `config.local.toml` `[registrazione]`) li impongono per quella volta; senza scelta si usano la
fotocamera 0 e il microfono predefinito di sistema. Altre opzioni: `--da-scena N`;
`--spezza presa-NN` ritaglia le scene da una presa già registrata senza aprire la finestra (per esempio dopo aver
ritoccato `latenza_s`).

Sincronia: il clock è quello di Python. Il video della presa e l'anteprima della webcam vengono dallo stesso
processo ffmpeg, quindi l'app sa quale fotogramma della presa corrisponde all'istante in cui parte il reel (più la
latenza della fotocamera, `latenza_s` in config, 0,1 s); per l'audio conta i campioni registrati fino a quell'istante
(più la latenza d'ingresso riferita da PortAudio). Se nel montaggio il labiale o le animazioni risultassero spostati
di una costante rispetto alla voce, ritocca `latenza_s` in `config.local.toml` e rifai `--spezza` sulle prese.

Se fotocamera o microfono non partono: Impostazioni di Sistema → Privacy e sicurezza → Fotocamera / Microfono per
l'app del terminale; chiudi le altre app che usano la fotocamera; `--dispositivi`, `--video N`, `--audio N`. Il log
di ffmpeg è in `_prese/`.
