# Registrare le clip del presentatore

Il presentatore registra **una clip per scena**: la sua durata decide la durata della scena, la sua voce è l'audio
del reel, il suo volto va nel riquadro. Per ora le clip si girano con il telefono e si copiano a mano; l'app di
registrazione guidata (fase 5, da fare prima della registrazione vera) automatizzerà ripresa e salvataggio.

## 1. Prima di registrare

- La sceneggiatura è rivista, le animazioni sono fatte e l'anteprima `--prova` è stata guardata.
- Il gobbo, una scheda per scena con il file atteso, la durata stimata e le frasi numerate:
  ```
  uv run reel gobbo <file> --scrivi      # → contenuti/media/<slug>/gobbo.txt
  ```

## 2. Inquadratura e luce

- Il riquadro è un cerchio di 360 px ritagliato **al centro** dell'inquadratura: volto al centro, testa e spalle,
  senza tagliare il mento.
- Verticale (9:16) od orizzontale (16:9) vanno bene tutte e due: il montaggio porta il lato corto a 360 px e prende il
  quadrato centrale. Meglio almeno 720 px sul lato corto.
- Luce frontale e morbida, sfondo semplice, sguardo in camera.
- iPhone: HEVC e video ruotati vanno bene, il montaggio li ricodifica e li raddrizza.

## 3. Voce

- **Mezzo secondo di silenzio** prima di cominciare e dopo l'ultima parola.
- **Una breve pausa tra una frase e l'altra**: ogni frase è un beat dell'animazione.
- Microfono vicino, stanza silenziosa; il volume lo uniforma il montaggio (loudnorm a −16 LUFS).
- Leggi la frase così com'è scritta: se la cambi, va cambiata anche la sceneggiatura (e forse l'animazione).

## 4. I file

- Nome `scena-NN.mov` (vanno bene anche `.mp4`, `.webm`, `.m4v`) in `contenuti/media/<slug>/`, con NN a due cifre come
  nella sceneggiatura. Dal telefono: AirDrop e rinomina.
- Rifare una scena vuol dire sostituire solo quel file.
- Controllo:
  ```
  uv run reel clip <file>
  ```
  per ogni scena ✔ o ✘, la durata e lo scarto dalla stima; oltre ±30 % compare un avviso (una frase saltata, o
  letta troppo lenta).

## 5. Il montaggio con le clip

- `uv run reel monta <file>` (senza `--prova`): ogni scena dura quanto la sua clip; una scena con voce ma senza clip è
  un errore «clip mancante».
- Con le clip, per ora, l'inizio di ogni frase è **stimato in proporzione alle parole** fra i due silenzi di mezzo
  secondo (`origine_tempi: parole-clip` in `report.json`). Pause regolari tra le frasi rendono la stima buona;
  l'allineamento vero, con il riconoscimento della voce, arriva con la fase 5.
- Poi: pacchetto social, approvazione, pubblicazione. Mai pubblicare un montaggio `--prova`; la pubblicazione la
  lancia il presentatore.

## 6. Registrazione guidata (fase 5, da fare)

`uv run reel registra <file>`: un'app desktop in Python (Tkinter + ffmpeg) che mostra la webcam e il testo da dire,
registra con un tasto e salva da sola la clip con il nome giusto. Decisione aperta: una clip per scena con il gobbo
(A), oppure una presa unica mentre scorre l'anteprima con il testo sincronizzato, spezzata poi per scene (B).
