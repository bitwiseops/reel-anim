# Stile parlato (guida per la VOCE)

Come parlano le persone nei reel che il presentatore ha scelto e analizzato (reelkit), ridotto a regole da applicare
al monologo di ogni scena. La scrive l'agente `stilista`; i limiti del repo (`docs/sceneggiatura.md` §4) valgono sopra.

## Corpus
- Percorso: ~/Projects/reelkit/export.md
- Letto il: 2026-09-15
- Reel letti: 14 (account: @geopop, @gianluigiballarani, @nove, @simorizzo_ai)

«N su 14» dice in quanti reel torna una cosa; qui c'è solo quello che torna in almeno 7. Le frasi sono contate per
intero in r0009, r0011, r0012 e r0014 (83 frasi), a campione negli altri. La punteggiatura è di Whisper, quindi
anche i confini delle frasi sono approssimati. Tre reel sono trailer sotto i 50 s (r0004, r0005, r0006) e dieci
superano i 90 s: da quei reel si prende il passo, non la lunghezza.

## Attacchi
- **Si parte dal fatto, già strano** (10 su 14): una persona o una cosa, con una cifra o un paradosso, nella prima
  frase. «Questo ragazzo ha vinto 200.000 dollari con un singolo prompt.» (r0009)
- **Nessun saluto, nessun annuncio** (14 su 14 senza saluto). Il tema lo annunciano solo r0002 e r0004 («vediamo»):
  il presentatore li ha segnati come «nessuno shock» e «sembra l'intro».
- **Prima frase**: nel corpus 8-27 parole (r0004 arriva a 41), mediana 19. Qui l'hook intero sta in 20 parole: il
  fatto in 10-14, poi la domanda.
- **Il «tu» o la domanda li chiede il repo, il corpus no**: in nessuno dei 14 ci sono nelle prime 20 parole. Si
  aggiunge dopo il fatto una domanda corta, come fa il corpus più avanti: «Cosa è successo?» (r0015), «Ma com'è
  possibile che sia successo?» (r0012). Adattamento, 12 parole: la frase di r0009 e poi «Com'è possibile?».

## Connettivi e ritmo
- **«E» apre la frase** (11 su 14) e porta avanti il racconto: «E così lascia un messaggio.» (r0015)
- **«Ma» fa la svolta** (9 su 14), spesso in una frase corta: «Ma la Cina continua.» (r0011)
- **«Perché» detto ad alta voce** (11 su 14) e **«quindi» per la conseguenza** (8 su 14): «Quindi sì, il prompt gli ha
  fatto guadagnare 200.000 dollari.» (r0009). «Cioè» torna in 5 su 14; «guarda», «ecco», «e allora» in uno solo, «e
  non è che» in nessuno: vanno bene, ma la base sono E, Ma, Perché, Quindi.
- **Il termine tecnico si traduce subito** (12 su 14; gli altri due non ne hanno), con «quindi», «cioè», «ovvero» o
  un'immagine: «prompt engineering, quindi consiste nello scrivere bene la domanda» (r0002), «una specie di
  gigantesco schema elettrico» (r0012).
- **La parola chiave e il numero tornano 2-3 volte** (14 su 14): «rallentare» in quasi ogni frase di r0011, «60
  volte» tre volte in r0003, «200.000 dollari» tre volte in r0009.
- **Tre membri dentro una frase con il verbo** (9 su 14), l'ultimo il più forte: «il testo era troppo corretto,
  troppo formale, troppo grammaticalmente pulito» (r0014). È una frase sola, non un elenco.
- **Una domanda a metà apre la spiegazione** (7 su 14), e la risposta arriva nella frase dopo: «Il risultato?»
  (r0009), «Che cos'è questa nuova architettura?» (r0007).
- **Chi guarda sta dentro la frase** (13 su 14): «tu» per il gesto («se hai uno studio», r0008), «noi» per
  l'esperienza comune («quando pensiamo a Chernobyl», r0006).
- **L'«io» è una reazione o una domanda che il presentatore si è fatto** (7 su 14): «la parte che più mi ha
  impressionato» (r0008), «la prima domanda che mi sono fatto» (r0009), «secondo me» (r0011).

## Lunghezza delle frasi
- **Due frasi su tre fra 6 e 18 parole**: nei quattro reel contati per intero la mediana è 13-17 parole, il 50-65 %
  sta fra 6 e 18, il 26-37 % sopra. Qui 6-18 (§5): la frase lunga del corpus (20-36 parole, con un «ovvero», una
  citazione, un contesto) si spezza alla virgola in due righe `VOCE:`, ognuna sotto le 18.
- **Frasi corte con il verbo per l'azione o la svolta** (10 su 14, 3-5 parole): «Gli altri lo trovano.» (r0015),
  «Perché consuma pochissimo.» (r0008). Qui `valida` conta come frase da titolo ogni frase di 4 parole o meno, senza
  «tu» né «io» e senza punto di domanda, e ne tollera una fuori dalla chiusura. La seconda si lega alla precedente
  con «e» («E così lascia un messaggio, e gli altri lo trovano.», adattamento) oppure diventa una domanda («Il risultato?»).
- **Velocità**: 2,9-3,1 parole al secondo nei quattro reel contati, in linea con la stima del repo (2,8).

## Come si chiude
- **L'ultima frase ribalta o riprende l'hook, oppure è una domanda** (8 su 14). Ribalta: «Tutti potrebbero essere
  d'accordo sul fatto che sarebbe più sicuro rallentare. E proprio per questo nessuno rallenterà.» (r0011, l'hook
  era «nessuno rallenterà davvero»). Domanda con risposta corta: «E tu fino a dove eri arrivato?» (r0002).
- **La battuta comincia spesso con «E»** (6 degli 8): «E per costruirgli un social capace di manipolare la
  dopamina, meno di una settimana.» (r0012)
- **Poi si smette**: nessuno dei 14 riassume. 10 su 14 chiudono con una firma fissa di una o due parole («Buona
  giornata.», «Ciao!»). Se ne adottiamo una la sceglie il presentatore, e rientra nelle 18 parole della chiusura.
- **Lunghezza**: nel corpus le ultime due frasi fanno 17-29 parole, qui la VOCE della chiusura resta sotto le 18.
  La prima metà del contrasto chiude la penultima scena («Pensate che per ricostruire tutti quei collegamenti ci
  sono voluti quasi dieci anni.», r0012) e alla chiusura resta la battuta (14 parole).

## Cosa evitare
- **Saluti e annunci in apertura**: nessun saluto in 14 su 14, nessun «oggi vediamo» in 12 su 14.
- **Il riassunto finale**: in nessuno dei 14.
- **Due frasi senza verbo di fila**: mancano in 13 su 14; fa eccezione r0007 («E quindi ottimizzato. Tutto
  praticamente.»), in un punto che la trascrizione ha doppiato. Lo schema «X, sì. Y, no.» non c'è in nessuno.
- **La CTA di rito** («Fammi sapere con un commento qua sotto cosa ne pensi e seguimi per rimanere aggiornato sul
  mondo delle AI.», r0009 e altri tre di @simorizzo_ai): qui una sola azione, legata al reel (`docs/linguaggio-reel.md` §8).
- **Sigle e nomi inglesi a raffica**: la trascrizione ne storpia quasi tutti, in 11 su 14 («l'EI», «OpenEA»,
  «Mixed Roof Experts»), segno che a voce si capiscono male. Qui una sigla si dice sciolta la prima volta, o non si
  dice (§5).

## Citazioni
Testuali dalle trascrizioni (punteggiatura di Whisper):
- «Questo ragazzo ha vinto 200.000 dollari con un singolo prompt.» (@simorizzo_ai/r0009: il fatto in 10 parole)
- «Il motivo è che secondo la prof il testo era troppo corretto, troppo formale, troppo grammaticalmente pulito.»
  (@gianluigiballarani/r0014: tre membri)
- «Ma com'è possibile che sia successo?» (@gianluigiballarani/r0012: la domanda che apre la spiegazione)
- «Siamo partiti con il prompt engineering, quindi consiste nello scrivere bene la domanda da porre all'intelligenza
  artificiale.» (@simorizzo_ai/r0002: il termine tradotto subito)
- «Ma la parte che più mi ha impressionato è che tutto questo consuma 150 Watt, praticamente nulla.»
  (@simorizzo_ai/r0008: l'io come reazione)
- «E così lascia un messaggio. Gli altri lo trovano.» (@gianluigiballarani/r0015: frasi corte con il verbo)
- «Diciamocelo, oggi quando pensiamo a Chernobyl associamo un concetto di morte e distruzione.» (@nove/r0006: il noi)
- «Tutti potrebbero essere d'accordo sul fatto che sarebbe più sicuro rallentare. E proprio per questo nessuno
  rallenterà.» (@gianluigiballarani/r0011: la chiusura che ribalta l'hook, 17 parole)

## Da provare nel prossimo reel
- **Prima il limite, poi il rilancio** (5 su 14): «Ovviamente non dimostra che il moscerino comprende Doom…», poi
  «Ma per la prima volta…» (r0012). Per un ricercatore è la mossa naturale: dire cosa non si può dire, e perché conta lo stesso.
- **L'esperimento mentale al «noi»**: «Mettiamo che gli Stati Uniti…», poi «E adesso mettiamoci dalla parte del...
  della Cina.» (r0011). Chi guarda ragiona invece di ascoltare (`docs/linguaggio-reel.md` §3).
- **Una citazione diretta, detta come la direbbe chi la dice**: «Oh mio Dio! Abbiamo trovato altri agenti!» (r0015).
  Da noi solo uscite vere del modello (§5).
