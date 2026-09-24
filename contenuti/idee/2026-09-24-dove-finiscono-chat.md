# Non scappare dal cloud: sappi quale interruttore hai toccato

**Data:** 2026-09-24
**Tipo:** pillola
**Fonte:** testo (contenuti/spunti/2026-09-24-privacy-dati-provider.md)
**Stato:** sceneggiata
**Sceneggiatura:** contenuti/sceneggiature/2026-09-24-dove-finiscono-chat.md
**Copione:** contenuti/copioni/2026-09-24-dove-finiscono-chat.md

## Concetto AI illustrato
Una chat mandata a un assistente in cloud ha tre destini distinti, che chi usa l'IA di solito confonde in uno solo
(«la cancello e sparisce»):
- **L'addestramento** (un interruttore). Sui piani personali la chat può entrare nei dati con cui si allena il
  modello successivo; lo decide un'impostazione. OpenAI, per ChatGPT e Codex personali: «we may use your content to
  train our models», e per uscire si spegne *Improve the model for everyone* (Impostazioni › Controlli dati) o si
  sceglie *Do not train on my content* nel Privacy Portal; vale per le conversazioni nuove. Anthropic, per Claude
  Free, Pro e Max (anche Claude Code da quegli account): dall'agosto 2025 l'utente sceglie se consentire l'uso per
  l'addestramento, e la scelta si cambia nelle impostazioni della privacy. Per i piani aziendali e per l'API, i due
  provider **di default non addestrano** (OpenAI: Business, Enterprise, Edu, API; Anthropic: Claude for Work, Gov,
  Education, API). Le chat temporanee (OpenAI) e in incognito (Anthropic) non addestrano.
- **La conservazione** (un orologio), che è un'altra cosa rispetto all'addestramento. Anthropic la scrive in chiaro:
  chat cancellate tolte dai sistemi entro 30 giorni; se consenti l'addestramento, dati de-identificati nelle
  pipeline di addestramento **fino a 5 anni**. OpenAI: chat temporanee fino a 30 giorni per sicurezza; log di
  controllo degli abusi dell'API fino a 30 giorni «unless longer retention is required by law». Una durata di
  conservazione dei dati usati per l'addestramento, per OpenAI, nelle pagine lette non c'è: il reel non confronta i
  due provider su questo punto.
- **L'obbligo legale** (qualcuno che da fuori può fermare la cancellazione). Nella causa del New York Times contro
  OpenAI, un ordine del tribunale federale di New York (ECF 33, 2025) ha obbligato OpenAI a «preserve and segregate
  all output log data that would otherwise be deleted», cioè anche le chat che gli utenti cancellavano. Con lo
  *Stipulation and Order* depositato il 9/10/2025 l'obbligo per il futuro è finito dal 26/09/2025; i dati già
  conservati restano, **tranne quelli di richieste dallo Spazio economico europeo, Svizzera e Regno Unito**. Non è
  stata una scelta dell'azienda: è un processo.

Il trend che tiene insieme i pezzi: le chat sono diventate materia prima. I provider chiedono di usarle, con tempi
che vanno da 30 giorni a 5 anni; le autorità contestano (il Garante nel 2024), i tribunali possono ordinare di
tenerle. Nello stesso tempo i modelli aperti sono diventati abbastanza piccoli da girare in casa: gpt-oss-20b di
OpenAI, licenza Apache 2.0, «run within 16GB of memory». Con un modello in casa la chat resta sul computer **se il
programma che lo fa girare non manda dati fuori**: è la condizione, non una garanzia del modello. Il limite: il
modello di casa è più piccolo e meno capace di quelli in cloud, e va installato.

## Situazione
Una sera, sul divano, incolli nella chat il referto delle analisi del sangue di tuo padre per capire che cosa vuol
dire quel valore segnato in grassetto. La risposta è chiara, chiudi, magari cancelli la conversazione. Il giorno dopo
non ci pensi più.
**Momento di prova** (scena 3): «Senza aprire niente: sai se il tuo interruttore dell'addestramento è acceso?».
L'interruttore compare a schermo in posizione incerta, a metà, per un secondo: chi guarda risponde nella testa prima
che scatti.

## Messaggio centrale
Non serve scappare dal cloud: serve sapere quale interruttore hai toccato e per quanto la tua chat resta in giro.
Per quello che non diresti a un estraneo, c'è un modello che gira in casa.

## Struttura narrativa
**Schema di partenza**: @ifarmsrlai · r0036
> [Tecnologia] è una risorsa enorme: [beneficio grande], [beneficio grande], ed è già dentro [luogo quotidiano]. Ma è anche un pericolo enorme se lasciata senza regole altrettanto forti. In [paese A] la corsa è tutta sull'acceleratore; in [paese B] invece [primato normativo]. Gli stati dovrebbero [prescrizione], invece di lasciarlo a [attore illegittimo]. È il rischio che sollevano [fonte terza]: che [scenario].

**Adattamento**:
- [risorsa enorme, già dentro un luogo quotidiano] → apertura e scena 2: la chat è il posto dove la sera incolliamo
  il referto di un genitore; la usiamo perché funziona.
- [ma pericolo se senza regole] → scene 3-5: le regole ci sono, e sono dei provider: un interruttore
  (l'addestramento) e un orologio (quanto la tengono), due cose diverse.
- [paese A / paese B] → il confronto non è fra i due provider (fatti, non giudizi) ma fra **chi scrive le regole**:
  i provider (scene 3-5) e, da fuori, garanti e tribunali (scene 6-7).
- [rischio sollevato da una fonte terza] → scena 7: il tribunale di New York che ordina di tenere anche le chat
  cancellate. Spostato **prima** della prescrizione, perché la chiusura è nostra.
- [prescrizione] → scena 8 e chiusura: la domanda-pivot «e se non uscisse di casa?», poi l'opinione (sapere quale
  interruttore hai toccato; l'indicibile in un modello di casa) e la mossa.

**Tecniche**:
- `contrasto`: scena 5 (30 giorni contro 5 anni: un mese contro un muro di giorni) e scena 8 (cloud contro casa).
- `autorità`: scena 7, il tribunale di New York nominato con un'etichetta corta; a voce «un tribunale di New York,
  nella causa del New York Times».
- `cautela`: scena 7 («non una scelta dell'azienda, e l'obbligo è finito») e scena 8 («se il programma non manda
  niente fuori»).
- `domanda-pivot`: scena 8, «e se la chat non uscisse proprio di casa?».

**Escluse**:
- `analogia` («ci dà i superpoteri»): la situazione concreta del referto fa già il lavoro; un'analogia in più
  allunga l'aggancio.
- `elenco` (la raffica di esempi dello schema: molecole, scuola, giocattoli): a voce un esempio solo, il referto;
  gli altri, se servono, in caption.
- `doppia-prospettiva` fra due paesi e l'orgoglio nazionale («in Italia siamo avanti»): il caso italiano del Garante
  è finito annullato per competenza, senza esame del merito; usarlo come vanto o come accusa sarebbe falso. Resta
  fuori dal parlato, con il dettaglio in `## Fonte` e in caption.
- Il rischio finale in bocca a terzi come ultima frase: la chiusura è un'opinione del presentatore, detta in prima
  persona.

## Tappe del parlato
1. (apertura) Quello che scrivi a ChatGPT o a Claude, dove va a finire? E se lo cancelli, sparisce davvero?
2. (filmato: di sera, due mani incollano un referto medico in una chat sul portatile, una lampada accesa) Ci
   incolliamo di tutto, anche il referto delle analisi di un genitore, e poi chiudiamo senza pensarci.
3. (animazione) Sui piani personali un interruttore decide se la tua chat allena i modelli: ChatGPT la usa finché non
   lo spegni, Claude ti chiede di scegliere. Sui piani aziendali e sull'API, di default, nessuno dei due addestra.
4. (filmato: un dito che trascina una conversazione nel cestino sullo schermo di un telefono) Spegnerlo però non
   dice quanto a lungo quella chat resta da qualche parte.
5. (animazione) Anthropic lo scrive: 30 giorni se l'addestramento è spento, fino a 5 anni se lo accendi. È un altro
   orologio, non lo stesso interruttore.
6. (filmato: un corridoio di server con le luci che lampeggiano, nessuna persona) E non decidono solo le aziende:
   fuori ci sono i garanti della privacy e i giudici.
7. (animazione) Nel 2025 un tribunale di New York, nella causa del New York Times, ha ordinato a OpenAI di tenere
   anche le chat che gli utenti cancellavano: un ordine del giudice, non una scelta dell'azienda. L'obbligo è finito
   a settembre 2025.
8. (animazione) E se la chat non uscisse proprio di casa? Un modello aperto di OpenAI sta in 16 GB di memoria, quella
   di un computer di casa; la chat resta lì se il programma che lo fa girare non manda niente fuori.
9. (chiusura) Non serve scappare dal cloud: serve sapere quale interruttore hai toccato, e quello che non diresti a
   un estraneo tenerlo in casa. Stasera apri le impostazioni e guardalo. Battuta finale.

## Suggerimenti per il parlato
- Equilibrio fra i provider: stessi verbi per tutti e due, nessun aggettivo di giudizio («peggio», «furbo»,
  «di nascosto»). Nella tappa 3 le due regole si dicono una dopo l'altra, con lo stesso peso.
- Tappa 7: il tribunale e il giornale si nominano, OpenAI si nomina solo come parte del processo; non dire che ha
  violato qualcosa.
- Tappa 8: il limite si dice senza drammi (più piccolo, meno capace), la condizione «se il programma non manda niente
  fuori» non si toglie.
- È un'opinione costruita sui fatti: la chiusura in prima persona va bene («io la vedo così»), i numeri no.

## Come si mostra
Filo: **la carta-chat** (un rettangolo arrotondato con l'icona `message-square` e 3 righe-sagoma, un'icona a goccia
di sangue o `file-text` per il referto), **l'interruttore** (un toggle grande, pillola con pallino), **l'orologio fatto
di giorni** (puntini). Tutto si capisce senza leggere: le sole parole a schermo sono nomi singoli e numeri.
- **Scena 3 (l'interruttore)**: al centro una carta-chat. Sotto, due corsie: a sinistra «personale», a destra
  «aziende» (una parola ciascuna, o le icone `user` e un palazzo). Nella corsia personale un toggle grande, che per 1 s
  resta a metà (il momento di prova), poi scatta su ON: la carta scivola in basso dentro un «pozzo» di carte
  ammucchiate che alimenta un'icona `brain` che si illumina (l'addestramento). Poi il toggle scatta su OFF e la carta
  successiva rimbalza di lato. I due marchi come parole singole, «ChatGPT» e «Claude», compaiono sopra due toggle
  identici, uno che parte già su ON (finché non lo spegni) e uno che parte a metà con un piccolo punto di domanda (ti
  chiede di scegliere). Nella corsia aziende un cancello chiuso fin dall'inizio: le carte ci passano accanto senza
  entrare nel pozzo. GRANDE: lo scatto del toggle, con la carta che cambia strada.
- **Scena 5 (l'orologio)**: 30 puntini in una fila corta a sinistra, etichetta «30 giorni». Poi, sul beat di «fino a
  5 anni», i puntini si moltiplicano e riempiono tutta l'area del contenuto: 1.825 puntini (5 × 365), cioè circa 61
  volte la fila corta, etichetta «5 anni». Accanto, piccolo, il toggle della scena 3 su ON: si capisce che il muro di
  giorni dipende dall'interruttore. Nessun logo accanto al muro (è il dato di Anthropic, ma la figura non mette i due
  provider a confronto). GRANDE: il riempimento che esplode a tutto riquadro.
- **Scena 7 (il cestino bloccato)**: la carta-chat viene trascinata verso un cestino; il coperchio si apre, ma una
  sbarra (o un'icona martelletto) cala e la carta resta sospesa sopra il cestino, chiusa in una scatola con un
  lucchetto. Etichetta «2025» sotto la sbarra. Poi la sbarra si alza su «set 2025» e le carte nuove cadono di nuovo
  nel cestino. Niente ritorno sulla scatola già chiusa: il dettaglio dei dati già conservati (e dell'esclusione
  europea) non si anima. GRANDE: la carta che si ferma a mezz'aria.
- **Scena 8 (la casa)**: la sagoma di una casa con dentro un portatile; la carta-chat gira dentro le pareti e,
  quando prova a uscire verso una nuvola in alto a sinistra, rimbalza sul muro. Una barra di memoria (icona
  `memory-stick`) si riempie fino a «16 GB». Il limite si vede: il cervello in casa (`brain`) è visibilmente più
  piccolo di quello nella nuvola. Sull'ultima frase una piccola freccia tratteggiata prova a uscire da una finestra
  della casa e si ferma a un «x»: la condizione (se il programma non manda niente fuori). GRANDE: la carta che
  rimbalza sul muro.
- Ultimo fotogramma animato: la casa con la carta dentro e, piccolo accanto, il toggle su OFF.
- **Scene a filmato** (2, 4, 6): mani sul portatile col referto di sera; dito sul telefono che cancella; corridoio di
  server. Senza volti. La 6 è la più «wow» tecnologica (Pexels ne ha molti); la 4 è la migliore candidata a Meshy
  (un'inquadratura di un telefono col cestino, poi uno zoom su una conversazione che si dissolve).
- Icone che mancano in `assets/icone/` (da aggiungere da Lucide, ISC): `trash-2`, `lock`, `house`, `gavel`,
  `toggle-right`, `cloud`.

## Cosa impara chi guarda
- **Un modo nuovo di leggere** la privacy di un'IA: non «è sicura o no», ma tre domande separate. Allena? (un
  interruttore). Per quanto la tengono? (un orologio). Chi da fuori può fermarne la cancellazione? (un giudice).
  Spegnere l'addestramento risponde alla prima, non alle altre due.
- **La mossa**: stasera aprire le impostazioni della propria IA e guardare l'interruttore dell'addestramento (in
  ChatGPT: Impostazioni › Controlli dati › «Migliora il modello per tutti»; in Claude: le impostazioni della
  privacy). Deciderlo, invece di lasciarlo com'è. E per le cose che non diresti a un estraneo, provare una chat
  temporanea (o in incognito), o un modello che gira sul proprio computer.
- **Il criterio**: chi guarda sa dire, senza riaprire l'app, in che posizione è il suo interruttore; e la prossima
  volta che sta per incollare un referto o un contratto si ferma un secondo e sceglie dove farlo.

## Pilastro
come funziona davvero

## Perché ora
Le pagine dei provider cambiano spesso e sono state aggiornate nelle ultime settimane: l'articolo di OpenAI su come
usa i dati risultava «Updated: 3 days ago» alla lettura del 2026-09-24; la pagina di Anthropic sulla conservazione
è aggiornata al 1° luglio 2026. Nello stesso anno si sono chiusi due capitoli giudiziari che toccano le chat: l'ordine
di conservazione di New York (finito a settembre 2025) e la sentenza del Tribunale di Roma sul Garante (18 marzo
2026). E i modelli aperti da tenere in casa sono diventati abbastanza piccoli per un computer normale (gpt-oss-20b,
agosto 2025).

## Fonte
Pagine ufficiali lette il 2026-09-24.
- **Anthropic, *Updates to Consumer Terms and Privacy Policy*, 28/08/2025** —
  https://www.anthropic.com/news/updates-to-our-consumer-terms. Misura: la regola per Claude Free, Pro e Max (anche
  Claude Code da quegli account); non si applica a Claude for Work, Government, Education, API (anche via Amazon
  Bedrock e Google Cloud Vertex AI). Alla lettera: conservazione di «five years, if you allow us to use your data for
  model training», altrimenti resta la conservazione di 30 giorni; «If you delete a conversation with Claude it will
  not be used for future model training»; la scelta si cambia nelle Privacy Settings; scadenza per gli utenti di
  allora: 8 ottobre 2025.
- **Anthropic Privacy Center, *How do you use personal data in model training?* (prodotti commerciali), aggiornata al
  16/03/2026** — https://privacy.claude.com/en/articles/7996885-how-do-you-use-personal-data-in-model-training.
  Misura: la regola per Claude for Work, API, Console. Alla lettera: «We will not use your chats or coding sessions
  to train our models, unless you choose to participate in our Development Partner Program»; eccezione: «If you
  explicitly report materials to us (e.g. via our thumbs up/down feedback mechanisms), or by otherwise explicitly
  opting in to training, then we may use those materials to train our models».
- **Anthropic Privacy Center, *How long do you store my data?*, aggiornata al 01/07/2026** —
  https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data. Misura: tempi di conservazione per i
  consumatori. Chat cancellate «Deleted from our back-end storage systems within 30 days»; con il consenso, dati
  de-identificati «for up to 5 years in our model training pipelines»; incognito non usato per l'addestramento;
  chat segnalate per violazioni fino a 2 anni (punteggi di sicurezza fino a 7); feedback col pollice: «we retain
  data associated with that submission for 5 years».
- **OpenAI Help Center, *How your data is used to improve model performance*** (aggiornato «3 days ago» alla
  lettura) — https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-improve-model-performance (letto
  tramite r.jina.ai: la pagina restituisce 403 a WebFetch e a curl). Alla lettera: «When you use our services for
  individuals, such as ChatGPT and Codex, we may use your content to train our models … To opt out, turn off Improve
  the model for everyone under Settings > Data controls»; «After you opt out, we won't use your new conversations»;
  «Temporary chats are not used to improve OpenAI models while they remain temporary»; «By default, we don't use
  inputs or outputs from ChatGPT Business, ChatGPT Enterprise, ChatGPT Edu, or our API to improve our models»; se si
  dà un feedback (pollice), «the entire conversation associated with that feedback may be used to train our models»
  anche dopo l'opt-out.
- **OpenAI Help Center, *Data controls in ChatGPT*** — https://help.openai.com/en/articles/7730893-data-controls-faq
  (stessa lettura indiretta). Chat temporanee: «may be retained for up to 30 days for safety purposes». La frase
  «attivo di default» per i piani personali compare nel riassunto della ricerca web di questa pagina ma non l'ho
  trovata nel testo estratto: il parlato dice «la usa finché non lo spegni», che discende dall'opt-out scritto.
- **OpenAI API, *Your data*** — https://developers.openai.com/api/docs/guides/your-data. I dati inviati all'API
  «not used to train or improve OpenAI models (unless you explicitly opt in)» dal 1° marzo 2023; log di controllo
  degli abusi «up to 30 days, unless longer retention is required by law»; Zero Data Retention solo per clienti
  idonei con approvazione.
- **Tribunale federale del Southern District of New York, *Stipulation and Order to Terminate OpenAI's Ongoing
  Obligations under the Preservation Order at ECF 33*, 25-md-03143 (SHS)(OTW), Document 922, depositato il
  09/10/2025, giudice Ona T. Wang** — copia del documento del fascicolo:
  https://cdn.arstechnica.net/wp-content/uploads/2025/10/NYT-v-OPenAI-Order-to-Terminate-OpenAIs-Preservation-Order-10-9-25.pdf
  (letto con `pdftotext`; l'originale è sul registro federale PACER / CourtListener, caso 1:23-cv-11195). Alla
  lettera: l'obbligo di «preserve and segregate all output log data that would otherwise be deleted on a going
  forward basis is terminated as of September 26, 2025»; OpenAI continua a conservare i dati già segregati prima del
  26/09/2025 «except for output log data corresponding to user requests originating from within the European
  Economic Area, Switzerland, or the United Kingdom»; conservazione mirata per gli account di un elenco di domini
  (Appendice A). La data dell'ordine originale (13 maggio 2025) viene dalle ricerche, non dal documento letto; la
  pagina OpenAI *How we're responding to The New York Times' data demands* (https://openai.com/index/response-to-nyt-data-demands/)
  restituisce 403. **Voce trovata in forma ufficiale** (il documento del tribunale): entra nel parlato, con «nel
  2025» e senza il giorno di maggio.
- **Garante per la protezione dei dati personali, comunicato del 20/12/2024** —
  https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10085432. Sanzione di 15 milioni a OpenAI
  (provvedimento n. 755 del 2/11/2024); contestati il trattamento per l'addestramento senza un'adeguata base
  giuridica, la trasparenza, la mancata verifica dell'età, la mancata notifica di una violazione di dati del marzo
  2023; campagna di comunicazione di sei mesi; atti trasmessi all'autorità irlandese come capofila.
- **Tribunale ordinario di Roma, Sezione diritti della persona e immigrazione, sentenza nella causa R.G. 4785/2025,
  giudice Damiana Colla, decisa il 18/03/2026** — testo della sentenza:
  https://dei.web.uniroma1.it/sites/default/files/allegati/2026-05/Trib_Roma_OpenAI_Garante_2026.pdf (letto con
  `pdftotext`; è una copia pubblicata dal Dipartimento DEI della Sapienza, non il sito del tribunale). Dispositivo:
  «in accoglimento del ricorso, annulla il provvedimento n. 755»; motivazione: «il primo motivo di ricorso deve
  essere accolto, con assorbimento degli altri», per la «pregiudiziale incompetenza dell'autorità resistente»
  (competente l'autorità irlandese come capofila dal 15/02/2024). Il merito delle violazioni non è esaminato.
  **Voce trovata in forma ufficiale** (il testo della sentenza), ma resta fuori dal parlato per scelta: si racconta
  bene solo con tre cautele, e la tappa 6 dice soltanto che i garanti esistono.
- **Hugging Face, scheda del modello openai/gpt-oss-20b (OpenAI, agosto 2025)** —
  https://huggingface.co/openai/gpt-oss-20b. Alla lettera: «the gpt-oss-20b model run within 16GB of memory»
  (quantizzazione MXFP4); licenza Apache 2.0; per l'hardware di consumo rimanda a Ollama e LM Studio.

## Angoli scartati
- **«Il pollice su vale come un sì»** (concetto: il feedback è una porta a parte; situazione: premi il pollice su una
  risposta sul referto; mossa: non dare feedback sulle chat delicate). Scartato come angolo intero: è un dettaglio
  sottile e vero per tutti e due i provider (OpenAI può addestrare sulla conversazione intera anche dopo
  l'opt-out; Anthropic tiene i dati del feedback 5 anni), ma senza il quadro dell'interruttore e dell'orologio non si
  capisce. Va nella caption come consiglio in più.
- **«La multa annullata: chi controlla le IA in Europa»** (concetto: lo sportello unico del GDPR, decide il paese
  dove l'azienda ha sede; situazione: il Garante italiano multa, il tribunale annulla; mossa: sapere a chi fare
  reclamo). Scartato: è diritto più che IA, la mossa è lontana dalla vita di chi guarda, e raccontato in fretta
  rischia di sembrare «OpenAI assolta» o «OpenAI colpevole», entrambi falsi.
- **«Cloud o casa: quando conviene il modello in locale»** (concetto: dimensione del modello e memoria; situazione:
  lo studio professionale con i dati dei clienti; mossa: provare un modello aperto sul portatile). Scartato come
  angolo intero: scivola nei costi e nell'hardware, che sono il tema di un altro reel, e il reel deve stare in piedi
  da solo; resta come scena 8, una sola, senza prezzi.

## Note per il reel
**Query in inglese per le tappe a filmato**
- Scena 2 (mani che incollano un referto in una chat, di sera): `hands typing laptop at night lamp` · `medical test
  results paper on desk laptop` · `close up hands laptop dark room screen glow`
- Scena 4 (dito che cancella una conversazione sul telefono): `finger swipe delete message smartphone close up` ·
  `smartphone screen trash icon delete` · `hand scrolling phone chat app close up`. Candidata a Meshy: un telefono
  in primo piano con una conversazione che si sbriciola dentro un cestino, poi zoom sul cestino.
- Scena 6 (corridoio di server, nessuna persona): `data center server racks blinking lights` · `server room corridor
  dolly shot` · `network servers leds close up`

**Filo visivo**: la carta-chat (scene 3, 5 piccola, 7, 8), il toggle (scene 3, 5 piccolo, 8 piccolo su OFF), i
puntini-giorno (scena 5, e come «2025 / set 2025» nella 7).

**Numeri** (tutti con fonte ufficiale): 30 giorni e 5 anni (Anthropic, 2025 e pagina aggiornata al 2026); 16 GB
(scheda di gpt-oss-20b, OpenAI su Hugging Face, 2025); 2025 e settembre 2025 (tribunale di New York, Document 922
del 9/10/2025). 1.825 puntini = 5 × 365: è un conto sulla cifra di Anthropic, non un numero nuovo; a schermo si
leggono solo «30 giorni» e «5 anni».

**MESSAGGIO candidato** (caption del post): «Non serve scappare dal cloud: serve sapere quale interruttore hai
toccato. Quello che non diresti a un estraneo, tienilo in casa.»
**CTA candidata**: una domanda vera — «Senza aprire l'app: il tuo interruttore dell'addestramento è acceso o spento?
Scrivilo nei commenti, poi vai a controllare.»

**Claim per il revisore**
- «ChatGPT la usa finché non lo spegni»: dal testo OpenAI «we may use your content to train our models … To opt out,
  turn off…» (piani personali). La formula «on by default» non l'ho trovata nel testo estratto: se il revisore vuole
  la parola «di default» deve trovarla sulla pagina.
- «Claude ti chiede di scegliere»: dall'annuncio Anthropic del 28/08/2025 (la scelta a chi si iscrive e, per chi c'era,
  entro l'8/10/2025). Non dire in che posizione era preimpostato l'interruttore nella finestra: le pagine lette non
  lo dicono alla lettera.
- «Sui piani aziendali e sull'API, di default, nessuno dei due addestra»: OpenAI (Business, Enterprise, Edu, API) e
  Anthropic (Privacy Center, prodotti commerciali, 16/03/2026: «We will not use your chats or coding sessions to
  train our models, unless you choose to participate in our Development Partner Program»). Eccezioni per tutti e due:
  opt-in esplicito e feedback col pollice.
- «30 giorni se l'addestramento è spento, fino a 5 anni se lo accendi»: sono tempi di Anthropic per i piani
  personali; i 5 anni riguardano dati de-identificati nelle pipeline di addestramento. Nessun confronto con OpenAI
  su questo punto.
- Tribunale di New York: l'ordine riguardava i dati di output di ChatGPT e dell'API che sarebbero stati cancellati;
  finito dal 26/09/2025 (ordine depositato il 9/10/2025). I dati già conservati restano, **ma non quelli di richieste
  dallo Spazio economico europeo**: per chi guarda dall'Italia la parte «restano» non vale, per questo non è nel
  parlato né nell'animazione. Non era una scelta di OpenAI, che l'ha contestato.
- Garante / Tribunale di Roma: non entrano nel parlato. Se qualcuno li aggiunge: la sanzione è stata annullata per
  incompetenza del Garante, senza esame del merito; mai «OpenAI ha violato la privacy» né «OpenAI è stata assolta».
- «La chat resta lì se il programma che lo fa girare non manda niente fuori»: condizione necessaria, non un fatto
  sul modello. Non nominare programmi specifici come «sicuri».
- «Un modello aperto di OpenAI sta in 16 GB»: è la memoria dichiarata con la quantizzazione MXFP4; nessuna promessa
  che sia veloce o all'altezza del cloud, e nessun prezzo di hardware.

**Note per la caption**
- Fonti con link e data di lettura (24/09/2026): Anthropic (annuncio del 28/08/2025 e Privacy Center), OpenAI (Help
  Center e documentazione API), ordine del tribunale di New York (Document 922, 9/10/2025), Garante (20/12/2024) e
  Tribunale di Roma (18/03/2026, annullamento per competenza, merito non esaminato), scheda di gpt-oss-20b.
- «Le regole cambiano: controllate le impostazioni, noi le abbiamo lette il 24 settembre 2026.»
- Consiglio in più (fuori dal parlato): il pollice su o giù è una porta a parte. OpenAI può usare per addestrare la
  conversazione intera legata al feedback anche se l'hai spento; Anthropic tiene i dati del feedback 5 anni (e, per i
  prodotti commerciali, scrive che può usare per addestrare i materiali segnalati col pollice).
- Dove sta l'interruttore: ChatGPT › Impostazioni › Controlli dati › «Migliora il modello per tutti»; Claude ›
  impostazioni della privacy. Chat temporanea (ChatGPT) e incognito (Claude) non addestrano.
- Immagini generate con Meshy, se la scena 4 passa a Meshy.
