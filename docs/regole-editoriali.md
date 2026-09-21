# Regole editoriali del presentatore

Le regole che valgono per **tutti** i reel e per **tutti** gli agenti. Questa è la fonte unica: gli agenti in
`.claude/agents/` dicono solo «cosa cambia per te» e rimandano qui; il dettaglio operativo sta nei manuali indicati.
Quando il presentatore cambia una regola si corregge **qui**, poi nelle righe «cosa cambia per te» degli agenti
toccati. Una regola superata si toglie (la cronaca sta in `.claude/agents/storico/`).

## 1. Il reel si guarda muto (2026-09-20)
Chi guarda non ha l'audio: sul video vengono bruciate le **caption** con il parlato, in una fascia in fondo (dopo la
registrazione, `tools/reel/caption.py`). Chi legge la caption non può leggere anche un testo nell'animazione.
- L'animazione **spiega per figure**: quantità, gesto, prima/dopo, due forme a confronto, qualcosa che si rompe o si
  riempie. Mai più di due parole di fila a schermo; numeri, percentuali e parole singole sì.
- Ogni scena animata ha la riga `FIGURA:` (cosa si capisce guardando, senza leggere); `TESTO:` è un extra, al massimo
  due righe da una-due parole.
- **Se la figura non regge non si ripiega sul testo**: si propone una clip (`[broll]`) o immagini generate con
  **Meshy**. Deroga `CAPTION: alto` se il testo *è* il contenuto: al massimo due scene per reel, dichiarate.
- Perché: i reel si guardano in gran parte senza audio, e due testi insieme non si leggono.
- Dettaglio: `docs/sceneggiatura.md` §0 · `docs/animazioni.md` §0 e §8 · controlli `parole-leggibili` e `caption`.

## 2. Niente testo denso che resta a schermo (2026-09-20)
Un testo lungo (un documento, una richiesta, un elenco) si vede **un istante** (≤ 1-1,5 s: il tempo di riconoscere
«è una mail», non di leggerla). Poi resta leggibile solo il frammento di cui parla la VOCE in quel beat, e il resto
diventa **righe-sagoma** (o esce). Attenuare a grigio lasciando il testo leggibile non basta. A fine beat, oltre una
ventina di parole leggibili (esclusi titoli ed etichette) è troppo.
- Dettaglio: `docs/animazioni.md` §10 («Testo denso») e componente `Sagome` in §8.

## 3. I due registri stanno a metà (2026-09-21)
**Circa metà delle scene in mezzo va a filmato** (± una; apertura e chiusura non si contano), e animazione e filmato
si alternano fra scene senza mai stare insieme.
- Sulle **clip** la voce dice le cose **generiche**: il problema di chi guarda, l'esperienza riconosciuta, la
  conseguenza, il passaggio, la presa di posizione. Niente numeri, conti, termini tecnici, meccanismi.
- Nelle **animazioni** va la **spiegazione complessa**: meccanismo, quantità, confronti, conti.
- Per stare a metà **si aggiungono scene, non secondi**: le scene a filmato sono corte (4-7 s), le animate tengono i
  12-16 s. Mai due scene a filmato di fila, mai `TESTO:` sopra un filmato. Il tipo `[broll]` lo scrive `broll scrivi`.
- Perché: Manim spiega, la clip tiene l'attenzione; cinque scene animate di fila stancano.
- Dettaglio: `docs/sceneggiatura.md` §2 · `broll/README.md` · `valida` e `broll piano` avvisano anche sui *troppo pochi*.

## 4. Apertura e chiusura sono il presentatore, a tutto schermo (2026-09-21)
I due estremi del reel sono lui a tutta tela che guarda in camera (`RIQUADRO: pieno`, default di `hook` e `chiusura`),
con le **sole caption**.
- **Apertura**: la VOCE pone il problema o la domanda di chi guarda (≤ 20 parole). Niente `ANIMAZIONE:`, niente
  `FIGURA:`, niente clip, nessuna classe Manim. Il `TITOLO:` resta obbligatorio ma serve alla **copertina**.
- **Chiusura**: la VOCE dice la conclusione (≤ 18 parole), **senza messaggio a schermo** e senza classe Manim.
  `MESSAGGIO:` e `CTA:` restano obbligatori ma sono il testo per la **caption del post**. L'ultima figura del reel è
  l'ultimo fotogramma dell'ultima scena animata.
- La scena dopo l'apertura e quella prima della chiusura partono o finiscono su uno **stacco**: niente raccordo.
- Dettaglio: `docs/sceneggiatura.md` §2 · `docs/animazioni.md` §5 · registrazione verticale 1080×1920.

## 5. Si citano solo fonti ufficiali (2026-09-20)
Per informarsi si legge tutto (articoli, blog, newsletter) **senza catalogarlo**. Ma ogni numero e ogni affermazione
di fatto del reel poggia su una **fonte ufficiale**, verificata sulla pagina: istituzioni e organismi (WEF, FMI, OCSE,
ILO, Commissione europea, Eurostat, Eurobarometro, Banca d'Italia, Istat, INAPP…), studi pubblicati, istituti di
ricerca riconosciuti (Pew, Gallup, McKinsey Global Institute, Goldman Sachs Research…). Chi, anno, link, **cosa
misura alla lettera**.
- Un numero che si ritrova solo in articoli, senza la fonte d'origine, non entra.
- **L'opinione di una persona qualunque non è un'autorità**: un post è uno spunto di riflessione. Nel reel non si
  cita (né nome, né «secondo X», né sue frasi come punch); il **credito va nella caption del post**, con il link.
  La mossa si presenta per quello che è, senza paternità: né «me la sono inventata io» né «uno dice che».
- A voce e a schermo le fonti ufficiali si nominano solo quando reggono un numero, con un'etichetta corta
  («Fondo Monetario, 2024»).

## 6. Ogni reel è a sé stante (2026-09-19)
Chi guarda un reel non ha visto gli altri: niente personaggi, aziende o vicende che proseguono, niente «come
dicevamo» o «ricordi la mail?». Nomi e situazioni inventati sono nuovi a ogni reel; un concetto già spiegato altrove
si ridice in una frase, come fosse la prima volta. Gli altri reel si leggono solo per **non ripetersi**.

## 7. Le revisioni del presentatore hanno l'ultima parola (2026-09-14)
Un suo ritocco, anche a un testo attribuito a un modello, si applica così com'è: non gli si oppone una regola. Si
controlla solo che sia **dichiarato in caption** («tagliate e ritoccate da noi») e che non cambi un claim.

## 8. Costanti di linguaggio
Tutto in italiano; si scrive «IA», mai «AI». Nessun personaggio e nessun dialogo: il presentatore parla a camera.
La chiusura è una battuta, mai un elenco letto a camera (gli elenchi vanno in caption). Il reel non è né una lode né
una stroncatura: potenziale e limite stanno nella stessa idea. I testi attribuiti a un modello sono **uscite vere**
(`uv run reel uscite`, `contenuti/idee/uscite/`), con i tagli dichiarati. Dettaglio: `docs/linguaggio-reel.md`.
