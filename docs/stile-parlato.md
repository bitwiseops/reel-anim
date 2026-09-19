# Stile parlato (guida per la VOCE)

Come parlano le persone nei reel che il presentatore ha scelto e analizzato (reelkit), ridotto a regole da applicare
al monologo di ogni scena. La scrive l'agente `stilista`; i limiti del repo (`docs/sceneggiatura.md` §4) valgono sopra.
Qui c'è solo il parlato: la struttura (schemi, svolte, tag) sta in `~/Projects/reelkit/pattern.md`.

## Corpus
- Percorso: ~/Projects/reelkit/export.md
- Letto il: 2026-09-16
- Reel letti: 30 (account: @geopop, @gianluigiballarani, @ifarmsrlai, @inregola.it, @marcocamisanicalzolari, @marcomontemagno, @nove, @primaopoilive, @simorizzo_ai, @yousciences)

«N su 30» dice in quanti reel torna una cosa: qui c'è solo quello che torna in almeno 15. Tre account fanno 16 reel su
30 (@simorizzo_ai 6, @gianluigiballarani 5, @yousciences 5): dove una regola sta vicino a 15 lo dico accanto.
Le frasi le ho contate per intero in nove reel: r0006, r0009, r0011, r0012, r0014, r0017, r0023, r0033 e r0037.
Negli altri le ho contate a campione. La punteggiatura è di Whisper, quindi anche i confini delle frasi sono
approssimati. Nei conteggi non entrano r0034 (trascrizione inaffidabile) e le code allucinate di r0018 e r0020.
Quattro reel sono estratti da dirette (r0027, r0028, r0029, r0035) e cinque stanno sotto i 50 s (r0004, r0005,
r0006, r0033, r0034). Sedici superano i 90 s: da quelli si prende il passo, non la lunghezza.

## Attacchi
- **Si entra subito nel contenuto** (28 su 30): con un fatto concreto (13), una tesi già conclusa (9) o una domanda
  (5). «Gemini ha detto di portare meno acqua e poi li hanno dovuti salvare.» (r0037)
- **Nessun saluto e nessun annuncio**: nessuno dei 30 saluta in apertura. Il tema lo annunciano solo r0004 e r0002
  («vediamo»), che il presentatore ha segnato come «sembra l'intro» e «nessuno shock».
- **La prima frase è corta**: nel corpus va da 3 a 41 parole, con una mediana di 12-13, e in 18 su 30 sta sotto le
  15. La frase dopo la allarga o la spiega: «Dove sono tutti quanti? È la domanda alla base del paradosso di Fermi.» (r0019)
- **Il «tu» o la domanda li chiede il repo; nel corpus li usano 8 reel su 30, di tre account**, nelle prime 20
  parole. Con il «noi» si arriva a 15. Due modi: «La cosa incredibile è che tu oggi l'ubiquità la compri.» (r0029,
  10 parole), oppure il fatto e subito una domanda corta, «Cosa è successo?» (r0015).

## Connettivi e ritmo
- **«E» apre la frase** (22 su 30) e porta avanti il racconto: «E così lascia un messaggio.» (r0015)
- **«Ma» fa la svolta** (22 su 30, in 16 in testa alla frase), spesso in una frase corta: «Ma c'è di più.» (r0016),
  «Ma la Cina continua.» (r0011)
- **«Perché» detto ad alta voce** (22 su 30) e **«quindi» per la conseguenza** (16 su 30). Esempio: «Quindi l'universo è
  una gigantesca memoria» (r0017). «Cioè» torna in 10 reel su 30; «allora», «insomma» e «beh» in 4-5; «no?» in fondo
  alla frase in 4, tutti parlati liberi (r0027, r0028, r0029, r0037). Vanno bene tutti, ma la base resta E, Ma,
  Perché, Quindi.
- **Il termine tecnico si traduce subito** (20 su 24; gli altri sei reel non ne hanno). Lo fanno con «quindi», «cioè»,
  «ovvero» o con un'immagine: «Senza più la gravità del Sole, quindi la curvatura della geometria dello spazio-tempo»
  (r0016), «Una specie di gigantesco schema elettrico» (r0012). Chi non traduce (r0027, r0034) lo fa apposta.
- **La parola chiave e il numero tornano 2-4 volte** (30 su 30): «tracce» quattro volte in r0017, «8 minuti e 20
  secondi» due volte in r0016, «200.000 dollari» tre volte in r0009.
- **Tre membri dentro una frase con il verbo** (22 su 30), spesso con la stessa parola in testa e l'ultimo membro più
  forte: «più intelligente, più veloce, ma estremamente più efficiente» (r0003), «si consuma energia, si produce
  lavoro, si dissipa calore» (r0017). È una frase sola, non un elenco.
- **Una domanda a metà apre la spiegazione** (17 su 30), e la risposta arriva nella frase dopo: «Dov'è il trucco?»
  (r0020), «Il risultato?» (r0009), «Perché dico fortunatamente?» (r0035).
- **Chi guarda sta dentro la frase** (29 su 30). Il «tu» o il «voi» servono per il gesto e la domanda («Hai mai visto
  Breaking Bad?», r0024); il «noi» per l'esperienza comune («quando pensiamo a Chernobyl», r0006). Gli account di
  scienza e di opinione usano soprattutto il «noi», quelli pratici il «tu».

## Lunghezza delle frasi
- **Due frasi su tre stanno fra 6 e 18 parole**. Nei nove reel contati la mediana è 11-17 parole in otto reel e 23 in
  r0033, un monologo di 32 s in quattro frasi. Fra 6 e 18 parole sta il 50-75 % delle frasi, sopra il 12-37 %. Qui
  il limite è 6-18 (§5): la frase lunga del corpus (20-30 parole, con un «ovvero», un elenco o una citazione) si
  spezza alla virgola in due righe `VOCE:`, ognuna sotto le 18.
- **Frasi corte con il verbo per l'azione o la svolta** (15 su 30, sei account; 3-5 parole): «Gli altri lo trovano.»
  (r0015), «Perché non vediamo nessuno.» (r0019). Qui `valida` conta come frase da titolo ogni frase di 4 parole o
  meno senza «tu», senza «io» e senza punto di domanda, e ne tollera una fuori dalla chiusura. Dalla seconda in poi
  la frase si lega alla precedente con «e», oppure diventa una domanda («Il risultato?»).
- **Velocità**: nei reel parlati a camera e contati per intero vanno 2,8-3,3 parole al secondo (r0009, r0011, r0012,
  r0014, r0033, r0037), in linea con la stima del repo (2,8). Dove ci sono dimostrazioni o musica si scende a
  1,9-2,3 (r0006, r0017, r0023): lì le pause le fa l'immagine.

## Come si chiude
- **L'ultima frase è una battuta, riprende l'hook o fa una domanda** (21 su 30). La battuta ribalta o mette a
  contrasto: «E per costruirgli un social capace di manipolare la dopamina, meno di una settimana.» (r0012). La
  ripresa dell'hook: r0018 apre con «Avevamo costruito…» e chiude con «Insomma, abbiamo costruito un piccolo
  laboratorio di dinamica dei fluidi a casa.». La domanda: «E tu fino a dove eri arrivato?» (r0002), «Voi cosa ne
  pensate?» (r0037).
- **Poi si smette**: nessuno dei 30 chiude su un riassunto. 15 su 30, da cinque account, hanno una firma fissa di una
  o due parole: «Buona giornata.», «Ciao!», «Capito?». Se ne adottiamo una la sceglie il presentatore, e rientra
  nelle 18 parole della chiusura.
- **Lunghezza**: nel corpus le ultime due frasi fanno 8-47 parole; qui la VOCE della chiusura resta sotto le 18.
  La prima metà del contrasto chiude la penultima scena («Pensate che per ricostruire tutti quei collegamenti ci
  sono voluti quasi dieci anni.», r0012) e alla chiusura resta la battuta (14 parole).

## Cosa evitare
- **Saluti e annunci in apertura**: nessun reel su 30 saluta, e solo 2 annunciano il tema con «vediamo».
- **Il riassunto finale**: nessuno dei 30 lo fa. Quando c'è un riepilogo («Quindi meno tasse, una seconda residenza e…»,
  r0025), sta prima della battuta e in una frase sola.
- **Due frasi senza verbo di fila**: 28 reel su 30 non le hanno. Fanno eccezione r0007 («E quindi ottimizzato. Tutto
  praticamente.») e r0016 («Magari attratta da un altro pianeta.» e poi «Insomma, un pianeta errante…»).
- **Lo schema «X, sì. Y, no.» in due frasi**: non c'è in nessuno dei 30. Il contrasto sta dentro una frase con il
  verbo: «che su una ricetta va benissimo, in quota no» (r0037).
- **La CTA di rito o a parola chiave**: la usano 7 reel su 30, tutti di due account. C'è la CTA fissa («Fammi sapere
  cosa ne pensi con un commento qua sotto e seguimi per rimanere aggiornato sul mondo delle AI.», r0009) e quella a
  parola chiave («Scrivi USA nei commenti e ti spieghiamo come funziona.», r0024). Qui si usa una sola azione, legata
  al reel (`docs/linguaggio-reel.md` §8).
- **Sigle e nomi inglesi a raffica**: in 15 reel su 30 la trascrizione ne storpia almeno uno («l'EI», «OpenEA»,
  «EGI», e l'IVA diventata «una gran parte dell'internet»), segno che a voce si capiscono male. Qui una sigla si
  dice per intero la prima volta, oppure non si dice (§5).

## Citazioni
Testuali dalle trascrizioni (punteggiatura di Whisper):
- «Gemini ha detto di portare meno acqua e poi li hanno dovuti salvare.» (@marcocamisanicalzolari/r0037: il fatto
  e la conseguenza in 13 parole)
- «Il motivo è che secondo la prof il testo era troppo corretto, troppo formale, troppo grammaticalmente pulito.»
  (@gianluigiballarani/r0014: tre membri)
- «Dove sono tutti quanti? È la domanda alla base del paradosso di Fermi. Dove sono gli alieni?»
  (@yousciences/r0019: il termine tradotto subito)
- «Che cos'è la memoria? Eh, per creare un ricordo devono avvenire dei processi fisici.» (@yousciences/r0017: la
  domanda che apre la spiegazione)
- «E così lascia un messaggio. Gli altri lo trovano.» (@gianluigiballarani/r0015: frasi corte con il verbo)
- «E probabilmente ora starai pensando, bello, ma che me ne faccio?» (@inregola.it/r0025: il «tu» e l'obiezione di
  chi guarda)
- «Tutti potrebbero essere d'accordo sul fatto che sarebbe più sicuro rallentare. E proprio per questo nessuno
  rallenterà.» (@gianluigiballarani/r0011: la chiusura che ribalta l'hook, 17 parole)
- «Nessuno ci ha minacciato, nessuno ci ha rubato niente, ma la nostra vita digitale sarà congelata, inaccessibile,
  sospesa.» (@marcocamisanicalzolari/r0033: la battuta finale in 18 parole)

## Da provare nel prossimo reel
- **Il «questo» su quello che si vede** (10 su 30): «Questo ragazzo ha vinto 200.000 dollari con un singolo prompt.»
  (r0009), «Guardate questo fluido.» (r0020). Da noi la VOCE indica quello che l'animazione mostra in quel beat.
- **Prima il limite, poi il rilancio** (6 su 30): «Ovviamente non dimostra che il moscerino comprende Doom…» e poi «Ma
  per la prima volta…» (r0012); «Quest'ipotesi va trattata con cautela…» e poi «Eppure…» (r0015). Per un ricercatore
  è la mossa naturale: dire cosa non si può affermare, e perché la cosa conta lo stesso.
- **L'obiezione di chi guarda, detta con le sue parole** (4 su 30): «Capita a tutti, no?» (r0037), «ma che me ne
  faccio?» (r0025). La frase dopo risponde, e chi guarda si sente dalla parte giusta.
