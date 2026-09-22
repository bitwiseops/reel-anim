# Passaggi prima del risultato: sbaglia meno, e tu controlli

**Data:** 2026-09-21
**Tipo:** pillola
**Fonte:** url (contenuti/spunti/2026-09-21-paper-chain-of-thought.md)
**Stato:** idea

## Concetto IA illustrato
**Un modello linguistico scrive un pezzo alla volta, e ogni pezzo nuovo dipende da tutto quello che c'è già scritto,
compreso quello che ha scritto lui. Se il risultato è la prima cosa che scrive, deve arrivarci in un salto solo; se
prima scrive i passaggi intermedi, ogni risultato parziale finisce nel testo e il passo dopo si appoggia lì.** Sui
problemi a più passaggi questo cambia molto l'esito: nel paper di Google (Wei e altri, 2022) lo stesso modello,
PaLM 540B, risolve il 17,9 % dei problemi di matematica del benchmark GSM8K quando risponde secco e il 56,9 % quando
scrive la «catena di pensiero» prima della risposta (Tabella 1).

Cosa il paper mostra davvero, e con che metodo:
- **Il metodo non è un'istruzione.** Nella richiesta ci sono otto esempi risolti, ciascuno con i passaggi scritti
  per esteso prima della risposta; il modello, davanti al problema nuovo, fa lo stesso. Nessun modello è stato
  riaddestrato. L'istruzione secca «ragioniamo passo per passo», senza esempi, è un paper diverso dello stesso anno
  (Kojima e altri, NeurIPS 2022), con lo stesso effetto in piccolo (vedi Fonte). Il reel lo dice giusto: «le hanno
  fatto vedere esempi risolti a passaggi», non «le hanno chiesto di ragionare».
- **Conta l'ordine, non la lunghezza.** Due controlli del paper (§3.3): se il modello scrive una fila di puntini
  lunga quanto i passaggi (più calcolo, nessun contenuto) va come la risposta secca; se scrive i passaggi **dopo** la
  risposta, va come la risposta secca. Aiuta solo scrivere i passaggi **prima**, in parole.
- **Serve sui problemi a più passaggi.** Sui problemi da un'operazione sola il guadagno è nullo o negativo (Tabella 3,
  SingleOp: PaLM 540B 94,1 → 94,1).
- **Serve solo ai modelli grandi.** Sotto circa 100 miliardi di parametri non aiuta, e sotto i 10 miliardi peggiora:
  i modelli piccoli scrivono «catene fluenti ma illogiche» (§3.2, App. A.1). I modelli che si usano oggi in chat
  stanno dalla parte grande; il reel non ne parla a voce (è un dettaglio da revisore, non una mossa).

Il limite, che sta nella stessa idea:
- **I passaggi non sono una garanzia.** Il paper lo scrive fra i limiti: «there is no guarantee of correct reasoning
  paths» (§6), e lascia aperto se la rete stia «davvero ragionando». Nell'analisi degli errori di LaMDA 137B il 22 %
  delle catene sbagliate è corretto tranne **un passaggio mancante** (App. D.2), e fra 50 risposte giuste una ci
  arriva per caso con un passaggio sbagliato (App. D.1).
- **I passaggi non sono per forza come il modello ci è arrivato.** Il paper parla di una «finestra interpretabile»
  con la riserva che descrivere per intero i calcoli del modello «resta una questione aperta» (§2). Uno studio
  successivo (Turpin e altri, NeurIPS 2023) mostra che le spiegazioni passo per passo possono tacere il vero motivo
  della risposta. Quindi i passaggi servono a **controllare il conto contro i tuoi dati**, non a sapere come «pensa».

E oggi (settembre 2026): molti modelli scrivono i passaggi da soli, prima di rispondere, perché sono addestrati a
farlo (i modelli «con ragionamento»: DeepSeek-R1 su Nature, 2025). Per questi chiedere «ragiona per passi» cambia poco
l'accuratezza (rapporto Wharton, 2025). La mossa per chi guarda quindi non è la formula magica: è **farsi dare i
passaggi e leggerli**, perché è lì, e non nel numero secco, che un errore si vede.

## Situazione
La spesa online, sul divano, col telefono in mano. Chi guarda chiede all'IA quanto paga davvero: 40 di spesa, il
servizio che aggiunge il 25 %, 3 di consegna, 4 di mancia al rider. Arriva un numero pulito, sicuro, e lo si conferma
così com'è. È un conto a più voci, quelli che si fanno fare all'IA ogni giorno (la spesa, la cena divisa fra amici,
il preventivo con lo sconto e l'IVA).

La scena è presa dal paper (App. A.1, Figura 10: bolletta di 40 dollari, 25 % di commissione, 3 di consegna, 4 di
mancia; qui in euro, stessi numeri): un modello più piccolo, pur scrivendo i passaggi, risponde **53** invece di
**57**, perché la mancia non entra in nessun passaggio. Il numero da solo non lo dice; i passaggi sì, perché si vede
il gradino che manca.

**Momento di prova** (tappa 2, prima del meccanismo): il problema della mensa della Figura 1 del paper. «La mensa ha
23 mele, ne usa 20 per il pranzo e ne compra altre 6: quante ne ha?» Chi guarda fa il conto in testa, e senza
accorgersene lo fa a passaggi (23 meno 20 fa 3, più 6 fa 9). Il modello che risponde secco dice **27**; lo stesso
modello, con i passaggi, dice **9**. Chi guarda ha appena fatto quello che il paper fa fare al modello.

Nessun personaggio, nessun nome: la mensa e la spesa sono oggetti a schermo (mele, blocchi-cifra, una scala di
gradini), non battute.

## Messaggio centrale
Un numero secco è un salto: se scrive prima i passaggi, l'IA sbaglia meno sui conti a più passaggi. E i passaggi sono
dove tu vedi l'errore, non una garanzia che non ci sia.

## Struttura narrativa
**Schema di partenza:** @marcocamisanicalzolari · r0037 — fatto di cronaca minimo → meccanismo dell'errore →
assoluzione di chi ha sbagliato → diagnosi psicologica → regola pratica → domanda.

> [Strumento] ha detto [consiglio sbagliato] e poi [conseguenza grave]. Gli avevano chiesto [domanda pratica]. E lui ha risposto con [tono sicuro], il tono di uno che sa. Ma non sapeva niente di [contesto reale]: non [verbo], non [verbo], non sa che [dettaglio specifico]. Mette insieme [dati] e ne tira fuori una media che suona bene: su [caso banale] va benissimo, su [caso serio] no. La parte che mi colpisce è che non hanno sbagliato a [usare lo strumento], capita a tutti. Hanno sbagliato a non [verifica mancata]. Ci fidiamo perché [non esitano mai]: leggiamo [sicurezza] come [competenza]. Quindi usiamola pure per [uso innocuo], ma [caso serio] si controlla con [fonte umana].

Perché questo. È lo schema di un errore piccolo e verificabile che regge una tesi generale («non serve la statistica,
serve la borraccia», dice l'analisi): qui la borraccia è il 27 della mensa. Porta il **meccanismo dell'errore** subito
dopo il fatto, e la **regola pratica dosata** in fondo («usiamola pure per…, ma…»), che è esattamente la forma della
mossa: per un conto da un'operazione va bene il numero, per un conto a più passaggi si leggono i passaggi. E la mossa
dell'assoluzione tiene chi guarda dalla propria parte: non sbagli a farle fare i conti. (r0020, l'altro schema
«mostra prima di spiegare», è già stato speso da un'altra idea.)

**Adattamento** (una riga per fase):
- [Strumento ha detto (consiglio sbagliato) e poi (conseguenza)] → hook e tappa 1: il conto della spesa, un numero
  pulito, e lo confermi. La conseguenza resta sospesa: «come sai che è giusto?».
- [Gli avevano chiesto (domanda pratica)] → tappa 2: la mensa, 23 mele, 20 usate, 6 comprate. Prova tu. Il modello
  secco: 27.
- [Ha risposto con (tono sicuro)] → il 27 arriva pulito, senza un passaggio: stesso aspetto di una risposta giusta.
- [Ma non sapeva niente di (contesto): tre negazioni] → sostituite dal meccanismo (tappa 4): scrive un pezzo alla
  volta, e se il risultato è il primo pezzo lo deve indovinare in un salto. Con i passaggi, ogni gradino è basso.
- [Su (caso banale) va benissimo, su (caso serio) no] → a voce, in tappa 4 o 7: su un conto da un'operazione il
  numero secco va bene, su quelli a più passaggi no (Tabella 3 del paper).
- [Non hanno sbagliato a (usare lo strumento), capita a tutti] → tappa 5 o 7: non sbagli a farle fare i conti.
- [Hanno sbagliato a non (verifica mancata)] → a prendere il numero senza i passaggi.
- [Ci fidiamo perché (non esitano mai)] → il numero secco sembra sicuro quanto uno giusto (tappa 1 e 2, a voce).
- [Quindi usiamola pure per (uso innocuo), ma (caso serio) si controlla con (fonte)] → tappa 6-7: i passaggi della
  spesa, il gradino della mancia che manca; la mossa, e il controllo si fa con i tuoi dati in mano.
- [Domanda finale] → esclusa a camera; la chiusura è una battuta, la domanda eventuale va in caption.

**Tecniche** (da «Tecniche condivise»):
- `caso-esemplare`: due casi minimi e veri, dal paper: la mensa (tappa 2) e la spesa con la mancia persa (tappa 6).
- `contrasto`: risposta secca contro risposta a gradini, stessa domanda, stesso modello, 27 contro 9 (tappa 2) e 18
  contro 57 su cento (tappa 4).
- `analogia`: «è quello che ti facevano fare a scuola: scrivi i passaggi, non solo il risultato» (tappa 3, a filmato).
- `assolvere-prima-di-accusare`: «non sbagli a farle fare i conti: sbagli a prendere il numero da solo» (tappa 7).

**Escluse:**
- `elenco` (le tre negazioni di r0037): niente elenco a camera; al suo posto il meccanismo in figura.
- `finale-aperto` («Voi cosa ne pensate?»): la chiusura è una battuta; una CTA sola, in caption.
- `formula-ripetuta` e `aforisma` («leggiamo la sicurezza come competenza»): non si ricopia la formula; se serve una
  frase citabile è quella della chiusura («il numero da solo non te lo dice, i passaggi sì»).
- La diagnosi psicologica estesa (l'amico esperto che dice «dipende»): tagliata per durata; resta mezza frase in
  tappa 1.
- Lunghezza: r0037 dura 98 s; qui nove scene, obiettivo ≤ 75 s.

## Come si mostra
Il reel si guarda muto: tutto quello che conta è una quantità, una scala, un pezzo che manca. Parole a schermo: solo
numeri e l'etichetta «Google, 2022».

- **La scala di gradini** (il filo visivo principale). Una risposta a passaggi è una scala: ogni gradino è un
  risultato parziale (un numero su un blocco), e la risposta sta in cima. La risposta secca è **una freccia sola** che
  salta dalla domanda alla cima, e atterra sul numero sbagliato.
- **Tappa 2, la prova (mensa).** 23 sagome di mele in fila; 20 si spengono ed escono; 6 entrano. Un vuoto di un
  secondo (un «?» al posto del risultato: chi guarda conta). Poi due corsie una sopra l'altra: sopra la freccia-salto
  atterra su **27** → croce; sotto tre gradini **23 → 3 → 9** → spunta. Etichetta «Google, 2022».
- **Tappa 4, il meccanismo.** Una fila di tessere che si scrive da sinistra a destra, e ogni tessera nuova si accende
  guardando tutte quelle prima (linee sottili che tornano indietro). Primo caso: la prima tessera dopo la domanda è il
  risultato → il salto è lungo, la tessera vacilla. Secondo caso: prima entrano «3», poi «9»: ogni tessera ha sotto la
  precedente, il salto è corto. Poi l'ordine: i gradini messi **dopo** il risultato non lo sorreggono (la cima resta
  in aria, croce); messi **prima** sì (spunta). Chiude la quantità: una griglia di **100 quadratini** (i problemi di
  matematica del test), 18 accesi con la risposta secca, 57 accesi con i passaggi. Stesso modello, stessa griglia.
  GRANDE: la griglia che si riempie da 18 a 57.
- **Tappa 6, il limite (spesa).** Quattro blocchi in fila, i dati della spesa: **40**, **+25 %**, **3**, **4** (il
  4 con l'icona di una moneta o di una mano: la mancia). Una scala si costruisce prendendo i blocchi uno alla volta:
  40 → 50 → 53, e in cima **53** con la croce. Il blocco **4** è rimasto a terra, mai usato: una lente ci si posa
  sopra (GRANDE: zoom sul blocco dimenticato). Poi il blocco sale, la scala ha il suo gradino, la cima diventa **57**
  → spunta. La figura dice da sola il criterio: ogni dato tuo dev'essere in un gradino.
- **Filo visivo** (torna in 2, 4, 6): la scala di gradini, la freccia-salto, spunta e croce.
- **Attenzione, due 57.** 57 su cento nella griglia (tappa 4) e 57 euro della spesa (tappa 6) sono una coincidenza dei
  numeri del paper. Per non confondere chi guarda muto: in tappa 4 la griglia si legge per quantità (i quadratini che
  si accendono), e se il numero compare è piccolo e accanto a «su 100»; in tappa 6 il 57 ha il simbolo €.

## Cosa impara chi guarda
1. **Un modo nuovo di leggere.** Un numero secco, per quanto pulito, è un salto: non c'è niente da controllare. Per un
   conto da un'operazione va bene; per un conto a più voci (spesa, cena divisa, preventivo con sconto e IVA) il
   numero da solo non ti dice se ha saltato un pezzo.
2. **La mossa.** Quando il conto ha più passaggi, chiedile di scrivere i passaggi **prima** del risultato, uno per
   riga (o, se l'assistente ha già il suo «ragionamento», aprilo e leggilo). Poi rileggili con i tuoi dati in mano.
3. **Il criterio** (*proposta*). Ogni dato che le hai dato deve comparire in un passaggio, e ogni passaggio lo devi
   saper rifare. Se un tuo dato non compare da nessuna parte (la mancia), manca un gradino; se compare un numero che
   non sai da dove venga, fermati lì. I passaggi ti dicono dove guardare, non che il conto è giusto.

## Pilastro
Come funziona davvero (scrive un pezzo alla volta, e i passaggi scritti diventano l'appoggio del passo dopo). In
filigrana **dove sbaglia** (il gradino mancante, e i passaggi che non sono una garanzia) e **cosa può fare per te**
(la mossa).

## Perché ora
*Proposta:*
- **Per chi guarda.** Farsi fare i conti dall'IA è uno degli usi più comuni e più rischiosi: la risposta ha lo stesso
  aspetto sicuro quando è giusta e quando è sbagliata. La mossa si fa alla prossima spesa.
- **Aggiornata al 2026.** «Ragiona passo per passo» è diventata una formula da prompt che gira ovunque, mentre molti
  assistenti oggi i passaggi li scrivono già da soli (DeepSeek-R1, Nature 2025) e per questi la formula cambia poco
  l'accuratezza (Wharton, 2025). Il reel non vende la formula: sposta il valore sul **leggere** i passaggi, che è
  l'uso che il paper stesso indica («opportunities to debug where the reasoning path went wrong») e che non invecchia
  con i modelli.
- **Il paper.** È del gennaio 2022 (v1; ultima revisione v6 del 10 gennaio 2023, NeurIPS 2022) ed è all'origine di
  tutti i modelli «che ragionano»: la catena di pensiero è citata in apertura dell'abstract di DeepSeek-R1.

## Fonte
**Pagina letta:** https://arxiv.org/abs/2201.11903 — Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian
Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, Denny Zhou (Google Research, Brain Team), «Chain-of-Thought Prompting Elicits
Reasoning in Large Language Models», NeurIPS 2022. arXiv v1 28 gennaio 2022, letta la v6 del 10 gennaio 2023 (PDF
intero, scaricato con `curl`). Etichetta a schermo: «Google, 2022».

Fatti presi, con le parole del testo:
1. Definizione e metodo: «a chain of thought — a series of intermediate reasoning steps»; «a few chain of thought
   demonstrations are provided as exemplars in prompting» (abstract); otto esemplari scritti a mano (§3.1); «No
   language models were finetuned» (§6).
2. Figura 1, mensa: «The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more…» — risposta secca
   «The answer is 27.», con i passaggi «23 - 20 = 3 … 3 + 6 = 9. The answer is 9.» (La figura non dice quale modello
   ha prodotto le due uscite: il reel dice «un modello grande», non un nome.)
3. Tabella 1 (e Figura 2, arrotondata a 18 e 57): PaLM 540B su GSM8K, «Standard 17.9», «Chain of thought 56.9
   (+39.0)». GSM8K è un insieme di problemi di matematica a parole, di livello scolastico, a più passaggi. Misura:
   accuratezza, cioè percentuale di problemi con la risposta finale giusta.
4. Ordine e contenuto (§3.3): «variable compute only» (puntini) e «chain of thought after answer» vanno «about the
   same as the baseline».
5. Limiti: effetto solo con modelli di «∼100B parameters», i piccoli producono «fluent but illogical chains of
   thought» (§3.2); «there is no guarantee of correct reasoning paths» (§6); il passaggio mancante: 22 % degli errori
   di LaMDA 137B su GSM8K (App. D.2); la spesa: PaLM 62B, «The answer is $53.00. (Incorrect: one step missing
   error)», PaLM 540B «…The answer is 57. (Correct)» (App. A.1, Figura 10).

Cosa il paper **non** dice:
- Non dice che il modello «ragiona»: lo lascia esplicitamente aperto (§6).
- Non dice che i passaggi scritti siano il processo reale del modello (§2, «remains an open question»).
- Non prova l'istruzione «ragiona passo per passo» senza esempi: quello è Kojima e altri, 2022.
- Non riguarda i modelli di oggi né i compiti d'ufficio: modelli del 2022, test di matematica scolastica, buon senso
  e giochi simbolici. Sui problemi da un passaggio il guadagno è nullo.
- Non dice di usare le catene come fonte di fatti: «we do not suggest using such chains of thought in a factual
  manner or in any real-world scenario» (checklist).

Altre fonti ufficiali (per il revisore e per «Perché ora», nel reel non si nominano):
- Kojima, Gu, Reid, Matsuo, Iwasawa, «Large Language Models are Zero-Shot Reasoners», NeurIPS 2022,
  https://arxiv.org/abs/2205.11916 — con «Let's think step by step» e nessun esempio, InstructGPT
  (text-davinci-002) passa da 17,7 % a 78,7 % su MultiArith e da 10,4 % a 40,7 % su GSM8K. Misura: accuratezza sulla
  risposta finale. Sostiene la mossa nella forma «chiedile i passaggi».
- Turpin, Michael, Perez, Bowman, «Language Models Don't Always Say What They Think: Unfaithful Explanations in
  Chain-of-Thought Prompting», NeurIPS 2023, https://arxiv.org/abs/2305.04388 — con un'inclinazione nascosta
  nell'input (per esempio la risposta giusta sempre in posizione «A» negli esempi) i modelli la seguono e le
  spiegazioni passo per passo non la nominano; accuratezza giù fino al 36 % su 13 compiti BIG-Bench Hard (GPT-3.5 e
  Claude 1.0). Sostiene «i passaggi non sono per forza come ci è arrivata».
- DeepSeek-AI (Guo e altri), «DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning», Nature
  645, 633-638, 17 settembre 2025, doi:10.1038/s41586-025-09422-z — modelli addestrati con apprendimento per rinforzo
  a produrre da soli il ragionamento; l'abstract cita la catena di pensiero come svolta precedente. Sostiene «oggi
  molti assistenti lo fanno da soli».
- Meincke, Mollick, Mollick, Shapiro (Wharton Generative AI Labs, University of Pennsylvania), «Prompting Science
  Report 2: The Decreasing Value of Chain of Thought in Prompting», 8 giugno 2025, https://arxiv.org/abs/2506.07142
  (rapporto tecnico, non sottoposto a revisione) — nei modelli senza ragionamento chiedere i passaggi migliora poco
  la media e aumenta la variabilità; «many recent models perform some form of CoT reasoning even if not asked»; nei
  modelli con ragionamento guadagni «marginal, if any», con più tempo e token. Sostiene la mossa aggiornata:
  leggere i passaggi, non recitare la formula.

## Angoli scartati
- **«La formula magica: scrivi "ragiona passo per passo"».** È l'angolo che gira ovunque, ed è il più facile. Ma nel
  2026 per molti modelli la formula cambia poco (Wharton, 2025), e il paper di Google non la usa nemmeno (usa esempi
  risolti). Venderla come trucco sarebbe una promessa che il reel non mantiene.
- **«I modelli piccoli peggiorano con i passaggi»** (l'effetto che compare solo sopra una certa taglia). È il
  risultato più scientifico del paper, ma a chi guarda non dà una mossa: i modelli che usa sono già grandi. Resta nel
  Concetto e fra i claim.
- **«I passaggi mentono»** (Turpin, 2023: le spiegazioni tacciono il vero motivo). Forte, ma è un secondo concetto e
  un altro paper; qui resta come riserva in una frase («non ti dicono come ha pensato: ti dicono dove guardare»). Se
  serve, merita un reel suo.
- **Il paper come storia** (Google, 2022, la nascita dei modelli che ragionano). Il filone chiude su cosa cambia per
  chi guarda, non sulla cronaca: la storia sta in una riga di «Perché ora» e in caption.
- **Dagli esempi risolti** (la mossa col metodo esatto del paper: metti nella richiesta un conto risolto a passaggi).
  È fedele, ma si sovrappone allo spunto «few-shot» del filone, che ha proprio quella mossa. Qui gli esempi sono
  detti in mezza frase, come metodo, non come mossa.

## Note per il reel
**Hook candidato** (a volto pieno, sole caption; è la domanda di chi guarda, non la tesi):
- «Le chiedi quanto paghi davvero, con commissione, consegna e mancia. Ti dà un numero. Come sai che è giusto?»
  (19 parole)
- Alternativa: «Quando l'IA ti fa un conto e ti dà solo il numero, tu come fai a sapere se è giusto?» (19 parole)
- TITOLO di copertina (la tesi): «Passaggi prima del risultato: sbaglia meno, e tu controlli». Alternativa: «Il numero
  secco non si controlla».

**Percorso** (*proposta*; sette tappe in mezzo: 3 animate, 4 a filmato, alternate; apertura e chiusura a volto
pieno; obiettivo ≤ 75 s, nove scene):
0. **Apertura, volto pieno.** L'hook.
1. **A filmato · l'esperienza.** Capita a tutti: le fai fare un conto con parecchie voci, arriva un numero pulito e
   sicuro, e lo confermi così com'è. Immagine: una donna sul divano, col telefono, scorre il carrello di una spesa
   online e preme conferma senza esitare; oppure un uomo al tavolo di cucina che guarda il telefono e annuisce.
   Query: `woman grocery delivery app phone couch`, `person confirming online order on smartphone`,
   `man checking phone at kitchen table nodding`.
2. **Animata · la prova (mensa).** Le 23 mele, 20 che escono, 6 che entrano, il vuoto di un secondo; poi la
   freccia-salto su 27 (croce) e i gradini 23 → 3 → 9 (spunta). «Google, 2022». La frase dopo dice a chi guarda che
   l'ha appena fatto: il conto l'hai fatto a passaggi, senza accorgertene.
3. **A filmato · l'analogia della scuola.** È quello che ti facevano fare a scuola: non scrivere solo il risultato,
   fammi vedere i passaggi. Ed è l'idea che hanno provato sull'IA. Immagine: un bambino al tavolo scrive un problema
   sul quaderno a quadretti, riga per riga, con la matita; una mano adulta indica una riga. Query:
   `child writing math homework notebook close up`, `student solving problem step by step with pencil`,
   `parent helping child with homework pointing at notebook`.
4. **Animata · il meccanismo e la quantità.** Scrive un pezzo alla volta e ogni pezzo si appoggia su quelli prima;
   risultato come primo pezzo = salto; passaggi prima = gradini bassi; passaggi dopo il risultato non servono. Le
   hanno fatto vedere esempi risolti a passaggi (mezza frase, senza figura propria). La griglia da 100: da 18 a 57,
   stesso modello. «Google, 2022».
5. **A filmato · oggi.** Oggi molti assistenti lo fanno già da soli: prima di rispondere si fermano a «pensare». Ma
   un conto che sembra pensato non è ancora un conto giusto. Immagine: una persona alla scrivania guarda lo schermo
   del portatile che carica, mento sulla mano, in attesa; poi la risposta arriva e lei si avvicina a leggere. Query:
   `woman waiting looking at laptop screen at desk`, `person watching loading screen hand on chin`,
   `man leaning in to read laptop screen`.
6. **Animata · il gradino che manca (spesa).** I quattro blocchi 40, +25 %, 3, 4; la scala 40 → 50 → 53 e la croce;
   la lente sul 4 rimasto a terra; il gradino che sale e la cima a 57 € con la spunta. Chiude il loop dell'hook: ecco
   come sai se è giusto. Anche questa scena viene dal paper (un modello più piccolo, con i passaggi).
7. **A filmato · la mossa.** Non sbagli a farle fare i conti; sbagli a prendere il numero da solo. Quando il conto ha
   più passaggi, chiedile di scriverli prima del risultato e rileggili con i tuoi dati davanti: non ti dicono come ha
   pensato, ti dicono dove guardare. Immagine: una persona al tavolo con lo scontrino in una mano e il telefono
   nell'altra, che scorre col dito riga per riga e confronta; oppure una penna che spunta righe su un foglio accanto
   al portatile. Query: `person comparing receipt with phone screen`, `finger scrolling line by line on smartphone`,
   `hand with pen checking bill next to laptop`.
8. **Chiusura, volto pieno.** La battuta (sotto).

Le tappe a filmato sono scritte senza numeri e senza termini tecnici: le cifre (23, 27, 9, 18, 57, 53) stanno tutte
nelle animate accanto. Se il reel sfora, la prima a perdere una frase è la tappa 4 (l'ordine «prima/dopo» si può
dire in mezza frase e tenere solo in figura).

**Chiusura candidata** (≤ 18 parole, a voce): «Il numero da solo non ti dice se ha sbagliato. I passaggi sì: cerca il dato
che manca.» (18 parole)

**Filo visivo:** la scala di gradini, la freccia-salto, spunta e croce (in 2, 4, 6).

**Numeri** (tutti dal paper, etichetta «Google, 2022»):
- 17,9 % → 56,9 % su GSM8K, PaLM 540B, stesso modello (Tabella 1): a schermo «18» e «57» su una griglia di 100.
- 27 contro 9 (Figura 1, mensa): esempio del paper, uscita di un modello non nominato.
- 53 contro 57 (App. A.1, Figura 10, spesa): uscite di PaLM 62B e PaLM 540B, in dollari nel paper, qui in euro con
  gli stessi numeri.
- Nessun altro numero a voce. Kojima, Turpin, DeepSeek-R1 e Wharton non entrano nel reel: reggono claim detti senza
  cifre («oggi molti assistenti lo fanno da soli», «non ti dicono come ha pensato»).

**MESSAGGIO candidato** (per la caption del post, ≤ 12 parole): «Chiedi i passaggi prima del risultato, e controllali coi tuoi dati.» (11 parole)

**CTA candidata** (una): «Mandalo a chi si fa fare i conti dall'IA.» (invio, destinatario ovvio). Alternativa, una
domanda vera: «Qual è l'ultimo conto che le hai fatto fare senza guardare i passaggi?»

**Claim per il revisore:**
- «Un modello grande di Google, nel 2022» per il 27 della mensa: la Figura 1 non nomina il modello. Verificare che la
  voce non dica «PaLM» né attribuisca il 27 al modello da 540B.
- «Da 18 a 57 problemi su 100, stesso modello»: Tabella 1, PaLM 540B, GSM8K; è accuratezza sulla risposta finale, su
  problemi di matematica scolastica a più passaggi, con otto esempi risolti nella richiesta. Non va generalizzato a
  «l'IA sbaglia tre volte meno».
- «Le hanno fatto vedere esempi risolti a passaggi»: metodo esatto del paper (few-shot con catene), non
  un'istruzione. La mossa «chiedile i passaggi» poggia su Kojima e altri, 2022 (zero-shot) e sul valore di lettura
  indicato dal paper (§2); verificare che il reel non le attribuisca al paper di Google.
- «Scrivere i passaggi dopo il risultato non serve»: §3.3, «chain of thought after answer» ≈ baseline; su LaMDA 137B
  e PaLM 540B, GSM8K. Semplificazione accettabile «conta scriverli prima»?
- «Scrive un pezzo alla volta, e ogni pezzo dipende da tutto quello che c'è prima»: resa della generazione
  autoregressiva; il paper non spiega il perché del guadagno (lo suggerisce con le ablazioni). Verificare che la
  voce dica «si appoggia» e non «ragiona».
- La spesa: in dollari nel paper («$40.00», «25%», «$3.00», «$4.00»; 53 contro 57), qui in euro. Il modello che
  sbaglia è PaLM 62B **con** i passaggi: il reel lo presenta come «un modello più piccolo, sempre dal paper», non come
  un assistente di oggi.
- «Oggi molti assistenti lo fanno già da soli»: DeepSeek-R1 (Nature 2025) e Wharton 2025 («many recent models
  perform some form of CoT reasoning even if not asked»). Non dire «tutti».
- «Non ti dicono come ha pensato»: §2 del paper («remains an open question») e Turpin e altri 2023. Non dire «i
  passaggi mentono».
- Il paper non dice che i passaggi garantiscono il conto giusto: §6, «no guarantee of correct reasoning paths».

**Note per la caption:**
- Credito del paper: Wei e altri, «Chain-of-Thought Prompting Elicits Reasoning in Large Language Models», Google
  Research, NeurIPS 2022, https://arxiv.org/abs/2201.11903. I tre esempi (mensa, spesa) e i numeri 18 e 57 vengono da
  lì; la spesa è in dollari nell'originale.
- Una riga di contesto: nel paper il modello vedeva esempi risolti a passaggi; la frase «ragioniamo passo per passo»
  viene da un altro studio dello stesso anno (Kojima e altri, NeurIPS 2022).
- La riserva detta per esteso: i passaggi aiutano a controllare, non sono una garanzia e non sono per forza il modo
  in cui il modello è arrivato alla risposta (Turpin e altri, NeurIPS 2023).
- Per i modelli «con ragionamento»: aprire e leggere il ragionamento mostrato, quando l'assistente lo mostra.
- La mossa non ha paternità: è l'uso che il paper stesso indica («debug where the reasoning path went wrong»).
