# Storico delle lezioni · revisore-tecnico

Copia integrale della sezione «Lezioni dalle sessioni» di `.claude/agents/revisore-tecnico.md` com'era il 2026-09-21, prima del
riordino in «Regole in vigore». **Gli agenti non caricano questo file**: è la cronaca (chi ha detto cosa, su quale
reel, cosa è stato superato e da cosa). Le lezioni nuove si aggiungono in fondo, con la data, quando serve ricordare
il *perché* di una regola; la regola stessa vive nell'agente.

## Lezioni dalle sessioni
- 2026-09-13, primo reel: il ❌ utile è stato su un aggettivo detto del risultato («nuovo, sì» per un biglietto che
  esiste identico in migliaia di copie) e sulla metafora visiva (una lente isolata = «l'IA non cerca sul web»).
  Controlla sempre gli aggettivi sul caso concreto mostrato e le icone isolate; nella seconda passata guarda solo le
  righe cambiate e dillo esplicitamente.
- 2026-09-13, terza passata (stesso reel):
  - Quando un claim esce dalla voce, cerca dove lo regge ancora l'animazione e chiedi che resti a schermo il tempo
    necessario (la colonna esce **dopo** che la parola è arrivata, non insieme).
  - Ogni «l'IA non sa / non cerca / non conosce» va provato contro i prodotti di oggi: ricerca web, memoria,
    connettori a mail e documenti, Copilot in ufficio. L'immagine giusta per questi casi è «passa dal contesto», non
    «nessun collegamento».
  - Un output scritto da noi pesa di più quanto più è in vista (letto a voce, a tutto schermo). O esce davvero da un
    modello, o la voce dice «può scrivere» e la caption lo dichiara esempio.
- 2026-09-14, i biglietti generati (stesso reel): la condizione di T3 era giusta. Su 16 uscite vere (Opus 5 e Sonnet 5)
  nessuna conteneva i nostri due biglietti, e una ha mostrato proprio il caso temuto: il luogo comune con il
  dettaglio attaccato («oggi si chiude un capitolo epico: quello della tua… guerra con la fotocopiatrice»). Quando il
  reel attribuisce un testo a un modello, chiedi le uscite vere (file in `contenuti/media/<slug>/`) e controlla che
  ogni parola venga da **una sola** uscita, con i tagli dichiarati; conta anche quante uscite ripetono lo stesso
  attacco, perché è la prova del «probabile».
- 2026-09-14, sera: le revisioni del presentatore hanno l'ultima parola, anche sui testi del modello. Un suo ritocco
  («il caffè potrai berlo sul divano» invece di «berlo caldo») non è un ❌: controlli solo che sia dichiarato in caption
  («tagliate e ritoccate da noi») e che non cambi un claim.
- 2026-09-15, la VOCE diventa parlato: le righe VOCE ora sono lunghe il doppio, con connettivi e riprese. Rileggi i
  claim nel testo lungo: una sfumatura si nasconde in un connettivo («quindi», «per questo») che trasforma una
  correlazione in una causa, o in un «quasi sempre» che diventa «sempre». Le idee ora arrivano anche da un link:
  i fatti presi dall'articolo si controllano contro l'articolo (punto 9), non contro quello che ricordi. Con
  `/pipeline … --tutto` un DA CORREGGERE ferma la corsa: scrivi le riformulazioni già dentro i limiti, così lo
  sceneggiatore le può applicare senza un altro giro.
- 2026-09-15, `generativa-probabile` (rifacimento del reel d'esempio con uscite vere già in archivio): un'animazione
  che «cambia vestito» a un oggetto con del testo dentro può mescolare a schermo le parole di due uscite; la
  condizione per l'animatore è che il testo vecchio esca. Un numero detto in VOCE per un modello («tutte e cinque»,
  Opus) va confrontato con l'altro modello della stessa prova (Sonnet: 0 su 5) e il confronto va in caption. I conti
  grezzi dei file di uscite non contano i plurali: ricontali. Le riformulazioni facoltative restano al presentatore:
  con `--tutto` il coordinatore non le applica, le porta nel report finale.

### 2026-09-20 · corse `scrivere-con-ia` e `generativa-probabile`
- **Scarica la pagina, non fidarti della lettura mediata.** Con `curl` la fonte di `scrivere-con-ia` si è letta intera
  (WebFetch ne dava un riassunto) e ha mostrato che la «mossa nostra» era il metodo dell'autore: ❌ contro la fonte.
- **Cerca gli artefatti dello strumento nelle uscite**: nome ed email dell'account, connettori (Drive, Gmail),
  inferenze sulla città o sull'ateneo. Segnala al coordinatore quelle rimaste nel file versionato, e controlla che la
  tesi del reel non sia smentita alla lettera dalle uscite stesse (formula + caption obbligatoria).
- **Un diagramma con conti veri si controlla anche nella forma**: nodo di partenza comune a tutte le uscite contate,
  etichette dei rami alla lettera, conto per modello. I conti giusti non bastano.
- Alla seconda passata si controlla solo ciò che è cambiato, più le aggiunte dello sceneggiatore oltre la lettera delle
  correzioni: vanno giudicate una per una (onesta / ritocco minimo).

### 2026-09-20 · REGOLA DEL PRESENTATORE: si verificano le fonti ufficiali, non gli articoli letti
L'ideatore legge liberamente articoli e blog per informarsi e non li cataloga: non chiedergli la bibliografia e non
rincorrerla. **Ogni numero e ogni affermazione di fatto del reel deve però poggiare su una fonte ufficiale**
(istituzioni, studi pubblicati, istituti di ricerca riconosciuti), verificata sulla pagina: chi, anno, cosa misura alla
lettera. Un numero che si ritrova solo in articoli, senza la fonte d'origine, è ❌ («numero senza fonte ufficiale»: si
toglie o si sostituisce). **Un'opinione di un commentatore qualunque non è un'autorità**: se il reel la usa come tale,
è ❌. Le posizioni del presentatore («l'ignoranza genera paura, la conoscenza la dissolve») sono opinioni dichiarate:
si controlla che non siano presentate come risultato di uno studio. Con `fonte: url` che punta al post di una persona qualunque
(precisazione del presentatore, stesso giorno): il post è uno spunto di riflessione, **nel reel non si cita** (né nome
né «secondo X» né sue frasi come punch) e il credito va in caption. Tu verifichi tre cose: che il reel non lo nomini;
che non presenti come propria invenzione o come fatto dimostrato ciò che è un'opinione sua (la mossa si presenta senza
paternità, niente «l'ho scoperto io»); che le note per la caption abbiano il credito con il link. La pagina si legge
comunque per intero, per sapere cosa viene da lì.

## 2026-09-24 · refactoring degli agenti
Tolti dall'agente i limiti vecchi nella riformulazione dei ❌ («VOCE ≤ 50 parole, hook ≤ 20, chiusura ≤ 18») e la
durata «30-90 s», superati dai limiti larghi del 2026-09-23 (oggi fa fede `reel valida`); tolte le date e gli
aneddoti (16 uscite, Opus 5 su 5 contro Sonnet 0 su 5, la «mossa nostra» scoperta con `curl`: restano qui sopra).
