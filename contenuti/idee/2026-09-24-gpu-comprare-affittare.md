# La GPU conviene comprarla solo se lavora ogni giorno

**Data:** 2026-09-24
**Tipo:** pillola
**Fonte:** testo (contenuti/spunti/2026-09-24-gpu-comprare-o-affittare.md)
**Stato:** sceneggiata
**Sceneggiatura:** contenuti/sceneggiature/2026-09-24-gpu-comprare-affittare.md
**Copione:** contenuti/copioni/2026-09-24-gpu-comprare-affittare.md

## Concetto AI illustrato
Far girare un modello di IA aperto (pesi scaricabili, licenza che lo permette) vuol dire tenere i suoi pesi nella
memoria di una scheda grafica mentre lavora: più il modello è grande, più memoria serve. Le strade sono due, e hanno
due forme di costo diverse.
- **Comprare** è un **costo fisso**: la scheda si paga tutta prima di accenderla, poi si aggiunge solo la corrente.
  Oggi la scheda da 32 GB (RTX 5090) in Italia si trova sui comparatori intorno ai 4.500 € (prezzo del giorno, 24
  settembre 2026: **esempio dichiarato**, non una fonte ufficiale). Il costo non scenderà presto per una ragione che
  sta a monte: Micron (giugno 2026) scrive che la domanda di memoria supera nettamente l'offerta, che le condizioni
  resteranno tese oltre il 2027 per la domanda spinta dall'IA e che l'offerta migliorerà solo gradualmente nel 2028.
  Il legame fra memoria scarsa e prezzo della scheda in negozio è una **nostra lettura**: Micron non parla di schede
  grafiche.
- **Affittare** è un **costo a consumo**: la scheda sta in un centro di calcolo, la si usa a distanza e si paga solo
  il tempo in cui è accesa. RunPod: la stessa RTX 5090 a 0,99 $ l'ora nel «secure cloud» (0,69 $ nel «community
  cloud», macchine di terzi), fatturata al secondo; le tasse si aggiungono sopra. Con l'IVA italiana (22%) e il cambio
  BCE del 23/09/2026 fanno circa 1,06 € l'ora.
- **Il punto di pareggio** è il numero di ore al mese in cui le due spese si equivalgono. Esempio dichiarato con i
  numeri del 23-24 settembre 2026: 4.500 € spalmati su 3 anni = 125 € al mese; ogni ora a casa costa circa 0,18 € di
  corrente (575 W della scheda × 31,63 cent/kWh ARERA); ogni ora in affitto 1,06 €. Si pareggia a
  125 / (1,06 − 0,18) ≈ **143 ore al mese**, cioè circa 4,7 ore al giorno tutti i giorni per tre anni. Sotto, conviene
  affittare.
- Cosa il conto **non** mette: il resto del PC (alimentatore da almeno 850 W, processore, memoria: favorisce il
  comprare, perché lo toglie), il valore di rivendita (favorisce il comprare, perché non lo conta), il fatto che il PC
  intero consuma più della sola scheda e a riposo molto meno. Il conto cambia molto con il prezzo (al listino di
  2.389 €, se confermato, il pareggio scende a circa 76 ore) e con l'orizzonte (su 2 anni sale a circa 214 ore).
- **Il limite dell'affitto**: i dati escono da casa. Nel community cloud girano su macchine di privati; nel secure
  cloud in centri di calcolo di partner. Se i dati non possono uscire (clienti, pazienti, segreti industriali) il
  conto delle ore non basta: è la seconda eccezione dell'opinione.

## Situazione
Una sera, il sito del negozio aperto: la scheda da 32 GB nel carrello, 4.500 €, il dito sul pulsante «acquista».
L'idea è far girare in casa un modello aperto, per provarlo o per non mandare fuori i propri documenti. Nessuno ha
contato quante ore al mese la scheda lavorerebbe davvero: una sera a settimana? Due ore al giorno? Tutto il giorno?
**Momento di prova** (scene 7-8): «quante ore al mese la terresti accesa, davvero?». Chi guarda fa la sua stima; poi
sul grafico un cursore «le tue ore» si ferma e si vede da che parte della linea di pareggio cade.

## Messaggio centrale
Oggi una GPU grande costa quasi il doppio e non scenderà presto, mentre in affitto si paga al secondo: comprarla
conviene solo se lavora molte ore, tutti i giorni, o se i dati non possono uscire da casa. Prima di comprare, conta le
ore.

## Struttura narrativa
**Schema di partenza**: @ingegneria.italia · r0039
> Negli ultimi mesi in [settore] c'è qualcosa che sta correndo più veloce di tutto: [costo]. Il motivo è [materia prima], o meglio [termine tecnico], che è [spiegazione in una riga]. In [periodo] il prezzo è salito del [numero]. Il punto è che [causa 1]. Tradotto: [versione semplice]. Ma c'è anche [causa 2]. E poi c'è un vincolo [di altra natura]: [causa 3]. Per noi questo si traduce in [ricaduta]. Quindi la domanda è: [alternativa possibile]? Siamo in [luogo]. Qui [oggetto] non viene [buttato], viene [rigenerato]. Si parte da [tappa 1]… [tappe]. E come dicevamo all'inizio, [la soluzione risponde al problema d'apertura]. [Firma].

**Adattamento**:
- [qualcosa che corre più veloce di tutto: il costo] → scena 2: la scheda da 32 GB oggi sui 4.500 €.
- [il motivo è la materia prima, o meglio…] → scene 3-4: la memoria, contesa dai centri di calcolo dell'IA; Micron:
  offerta sotto la domanda oltre il 2027, sollievo graduale nel 2028. Una causa sola, non tre.
- [per noi si traduce in: ricaduta] → chiusa della scena 4: non aspettarti sconti a breve.
- [quindi la domanda è: alternativa possibile?] → scena 5: e se non la comprassi? L'altra strada è affittarla.
- [siamo in… qui non viene buttato, viene rigenerato + le tappe] → scena 6: com'è fatto l'affitto (al secondo, solo
  quando lavora) e cosa costa la tua accesa a casa; scene 7-8: il conto in ore, che diventa la domanda vera.
- [come dicevamo all'inizio, la soluzione risponde al problema] → chiusura: risponde a «compri o affitti?» con
  l'opinione, le due eccezioni e la mossa.

**Tecniche**:
- `numeri-come-prova`: scene 2, 4, 6, 8, ogni cifra con la sua etichetta corta («Micron, 2026», «ARERA»).
- `domanda-pivot`: scena 7, «la domanda vera non è quanto costa, è quante ore la terresti accesa» (l'equivalente di
  «bisogna davvero comprarli sempre nuovi?»), che porta dal trend al conto.
- `cautela`: scena 8 e chiusura (è un esempio a tre anni, senza il resto del PC; e i dati che non possono uscire).
- `struttura-ad-anello`: la chiusura riprende la domanda dell'apertura, «la compri o la affitti?», e risponde.

**Escluse**:
- `elenco` (le tre cause dell'aumento): un elenco non si legge a camera; resta una causa sola, e le altre voci del
  conto (resto del PC, rivendita, orizzonte) vanno in caption.
- `presenza-sul-luogo` («siamo nello stabilimento»): il presentatore non va in un centro di calcolo; il luogo lo
  danno le clip delle scene 3 e 5.
- `sponsor-integrato` e `firma-di-chiusura`: firme di un solo account; qui non c'è sponsor e RunPod è solo la fonte
  del listino (in caption: «un fornitore fra tanti, prezzi del 24/09»).
- Il «tradotto:» dopo il termine tecnico: la versione semplice la fa la figura, non una seconda frase.

## Tappe del parlato
1. (apertura) Vuoi far girare un modello di IA aperto tutto tuo, per provarlo o perché i dati restano tuoi: la GPU la compri o la affitti a ore?
2. (animazione) La GPU da 32 GB che serve ai modelli più grandi, oggi in Italia, nei negozi si trova intorno ai 4.500 €.
3. (filmato: il corridoio di un centro di calcolo, file di server con le spie che lampeggiano, nessuna persona) E non scenderà presto: la memoria, oggi, se la contendono i grandi centri di calcolo dell'IA.
4. (animazione, grafico) Micron, giugno 2026: la domanda di memoria supera l'offerta e resterà così oltre il 2027; l'offerta migliorerà piano solo nel 2028.
5. (filmato: mani su un portatile sul tavolo di cucina, di sera, una barra di avanzamento che scorre sullo schermo) L'altra strada è non comprarla: la scheda resta lontana, tu la usi dal tuo computer e paghi solo quando lavora.
6. (animazione) In affitto la stessa GPU costa circa 1,06 € l'ora con l'IVA, e si paga al secondo; la tua, accesa a casa, costa circa 0,18 € l'ora di corrente.
7. (filmato: un orologio da parete che corre, le pagine di un calendario che si sfogliano) Allora la domanda vera non è quanto costa: è quante ore al mese la terresti accesa davvero. Contale adesso.
8. (animazione, grafico) Spalmata su tre anni, la scheda costa 125 € al mese prima di accenderla; comprarla conviene solo sopra circa 140 ore al mese, quasi 5 ore al giorno, tutti i giorni.
9. (chiusura) Io oggi la affitterei: comprarla ha senso solo se lavora ore ogni giorno o se i dati non possono uscire da casa. Prima di comprare, affittala per una sera e conta le ore. Battuta finale.

## Suggerimenti per il parlato
- È un'opinione dichiarata: nella chiusura il presentatore parla in prima persona («io oggi la affitterei»); nelle
  scene con i numeri le cifre sono della fonte, detta con l'etichetta corta.
- Tutti i numeri a voce sono arrotondati e con «circa»; nella scena 8 va detto che è un esempio su tre anni.
- Nelle tappe a filmato (3, 5, 7) niente «GPU», «cloud», numeri o nomi di aziende: sono le frasi generiche.
- Né lode né stroncatura: affittare costa poco ma i dati escono; comprare costa tanto ma la scheda resta tua.

## Come si mostra
Filo visivo: **la scheda** (una sagoma di GPU, rettangolo con due ventole, che si accende e si spegne), **il
cartellino del prezzo** e **il contatore delle ore**. Tornano in tutte le scene animate.
- **Scena 2**: la sagoma della scheda al centro, con appeso un cartellino. Il numero sul cartellino scorre e il
  cartellino si gonfia fino a 4.500 €, pesante, e la scheda si abbassa sotto il suo peso. Etichette: «32 GB», «€».
  Se il revisore conferma il listino NVIDIA (2.389 €), il cartellino parte da lì e si stira fino a 4.500: la figura
  del «quasi il doppio». GRANDE: il cartellino che si gonfia di scatto sull'ultimo numero.
- **Scena 4** (il trend che si vede): una linea del tempo 2026 → 2027 → 2028. Sopra, una linea «domanda» che sale;
  sotto, una linea «offerta» che resta staccata. Lo spazio fra le due è pieno di colore caldo per tutto il 2026-2027,
  e solo nel 2028 la linea dell'offerta (tratteggiata: è una previsione) comincia ad avvicinarsi, senza toccarla. Il
  cartellino della scena 2 resta appeso sopra il 2027, alto. Etichetta «Micron, 2026». GRANDE: zoom sul 2028 dove il
  vuoto comincia appena a chiudersi.
- **Scena 6**: due schede affiancate. A sinistra quella in affitto, con un tassametro: scorre solo mentre la scheda
  è accesa, si ferma di colpo quando si spegne (due accensioni brevi, due fermate). A destra quella di casa, con una
  spina e un contatore piccolo che scorre lento: «0,18 €/h» contro «1,06 €/h». Nessuna frase: due numeri, due gesti
  (accendi/spegni).
- **Scena 8** (il conto): un grafico. Asse orizzontale: ore al mese (0-300); verticale: € al mese. La linea
  «comprare» parte già alta, a 125, e sale piano (la corrente); la linea «affittare» parte da zero e sale ripida. Si
  incrociano a circa 140 ore: lì un punto e il numero «140 h». La zona a sinistra dell'incrocio si colora (vince
  l'affitto), quella a destra con l'altro colore. Poi il cursore «le tue ore» scivola da destra verso sinistra e si
  ferma a 12 ore (una sera a settimana, esempio dichiarato), ben dentro la zona dell'affitto. Sotto, un calendario di
  30 caselle si riempie di 5 ore ciascuna per mostrare cosa sono 140 ore. GRANDE: le due linee che si incrociano, con
  lo zoom sul punto.
- **Scene a filmato** (3, 5, 7): corridoio di server con le spie, mani su un portatile di sera, orologio e calendario.
  Senza volti. La 7 è la migliore candidata a Meshy (orologio e calendario in un'immagine sola, «wow» con una
  carrellata sulle lancette); la 3 regge bene su Pexels.
- Ultimo fotogramma animato: il grafico della scena 8 con il cursore fermo nella zona dell'affitto e la scheda di
  casa spenta accanto.

## Cosa impara chi guarda
- **Un modo nuovo di leggere** la scelta fra comprare e affittare: non «quanto costa la scheda», ma «quante ore la
  uso»; un costo fisso contro un costo a consumo, e il punto in cui si incrociano.
- **La mossa**: prima di comprare, affittare la scheda per una sera e usare il modello che si vuole davvero usare,
  poi segnare per un mese le ore in cui servirebbe. Con un modello aperto che sta in 16 GB, come gpt-oss-20b, basta
  anche una scheda più piccola in affitto (in caption: circa 0,36 € l'ora con l'IVA, circa 1 € per una sera di tre
  ore).
- **Il criterio**: a fine mese si sommano le ore segnate e si confrontano con il pareggio (circa 140 ore con i numeri
  di oggi, o il conto rifatto con i propri prezzi). Se si sta sotto, e i dati possono uscire, la scheda resta nel
  carrello.

## Pilastro
cosa può fare per te

## Perché ora
Le fonti sono di queste settimane: il listino RunPod letto il 24 settembre 2026 (uguale al 13), il cambio BCE del 23
settembre, la tariffa ARERA in vigore dal 1° luglio 2026 (l'aggiornamento del IV trimestre esce a fine settembre),
Micron del 24 giugno 2026. E la finestra conta: Micron dice che la memoria resterà scarsa oltre il 2027, quindi chi
pensa di aspettare lo sconto per comprare ha davanti almeno un anno. Il prezzo del giorno sui comparatori cambia in
settimane: **va riverificato il giorno prima della registrazione**, e con lui il pareggio.

## Fonte
Fonti ufficiali (lette il 24/09/2026):
- **NVIDIA**, pagina italiana della GeForce RTX 5090,
  https://www.nvidia.com/it-it/geforce/graphics-cards/50-series/rtx-5090/ — «GDDR7 da 32 GB»; «Potenza grafica
  totale (W): 575»; «Alimentazione di sistema richiesta (W): 1000»; alimentatore minimo 850 W. **Il prezzo sulla pagina
  è un segnaposto** («A partire da € XXX,00»): il listino di 2.389 € dello spunto **non è confermato** su una pagina
  NVIDIA (compare solo in comparatori e blog). Anche la pagina americana mostra «$XXX.00».
- **RunPod**, listino, https://www.runpod.io/pricing (letto il 24/09/2026, uguale al 13/09 dello spunto) — per ora,
  fatturazione al secondo: RTX 5090 32 GB 0,69 $ community / 0,99 $ secure; RTX 4090 0,34 / 0,74 $; RTX 3090 0,22 /
  0,50 $; H100 PCIe da 1,99 $. **Tasse**: https://docs.runpod.io/accounts-billing/sales-tax — «Runpod always charges it
  on top of your credit purchase»; l'aliquota dipende da indirizzo di fatturazione e metodo di pagamento. La pagina
  non nomina l'Italia: il 22% è l'aliquota IVA ordinaria italiana, applicata come ipotesi per un privato.
- **BCE**, tassi di riferimento EUR/USD,
  https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/eurofxref-graph-usd.en.html
  — 23/09/2026: 1 € = 1,1411 $ (quindi 1 $ = 0,8763 €).
- **ARERA**, comunicato del 25 giugno 2026 «Elettricità: Maggior Tutela +4,6% nel III trimestre 2026 per i clienti
  vulnerabili»,
  https://www.arera.it/comunicati-stampa/dettaglio/elettricita-maggior-tutela-46-nel-iii-trimestre-2026-per-i-clienti-vulnerabili
  (PDF: https://www.arera.it/fileadmin/allegati/com_stampa/26/Aggiornamento_Maggior_Tutela_III_trimestre_2026.pdf) —
  «Dal 1° luglio 2026, il prezzo di riferimento dell'energia elettrica per il cliente tipo sarà di 31,63 centesimi di
  euro per kilowattora, tasse incluse»; cliente tipo = vulnerabile in Maggior Tutela, 2.000 kWh/anno, 3 kW. **Il link
  dello spunto era quello del II trimestre**: il 31,63 è del III. Al 24/09 l'aggiornamento del IV trimestre non risulta
  ancora uscito. Misura il prezzo per un cliente tipo tutelato, non la bolletta di chi è sul mercato libero.
- **Micron**, Fiscal Q3 2026 Earnings Call Prepared Remarks, 24 giugno 2026,
  https://investors.micron.com/static-files/631b1a32-5537-46ae-8f40-82e42fc79dfe (dietro Cloudflare; letto dalla copia
  Wayback dell'11/07/2026) — «DRAM and NAND industry demand continues to significantly exceed industry supply. We
  expect tight conditions to persist beyond calendar 2027 as a result of AI-driven demand across all segments coupled
  with structural supply constraints»; «Even as we expect industry supply to improve gradually in 2028, we currently do
  not have line of sight as to when memory supply will be able to catch up with increasing demand»; «HBM's growth […]
  further pressures non-HBM supply»; PC e smartphone: ricavi in crescita «despite unit volume declines», dispositivi
  «at higher prices». Nuove fabbriche: ID1 (Idaho) prima produzione a metà 2027, ID2 a fine 2028. **Cosa non dice**:
  non parla di schede grafiche né di prezzi al dettaglio; la frase dello spunto «HBM del 2026 venduta con contratti
  pluriennali» e «nessun volume significativo prima dell'anno fiscale 2028» non si ritrova così nel testo letto (ci
  sono gli accordi pluriennali con i clienti, 2026-2030, e il «gradually in 2028»).
- **OpenAI**, scheda di gpt-oss-20b, https://huggingface.co/openai/gpt-oss-20b — «run within 16GB of memory»; 21
  miliardi di parametri, 3,6 miliardi attivi; pesi MoE quantizzati in MXFP4; licenza Apache 2.0. (Solo in caption.)

Esempio dichiarato, non fonte ufficiale:
- **Prezzo del giorno della RTX 5090 in Italia**: comparatori (Trovaprezzi, idealo), 24/09/2026. Non ho potuto aprire
  le pagine (403 e blocco); dalle ricerche risultano le 5090 dei partner da circa 4.050-4.500 € in su e la Founders
  Edition quasi introvabile. Nel reel: «intorno ai 4.500 €», data a schermo, da riverificare prima di registrare.

Il conto (tutte le voci, stessa data):
- Affitto: 0,99 $ × 0,8763 × 1,22 = 1,0585 €/h (secure; community 0,7377 €/h).
- Corrente: 0,575 kW × 0,3163 €/kWh = 0,1819 €/h (scheda a pieno carico; il PC intero consuma di più).
- Comprare: 4.500 € / 36 mesi = 125 €/mese; niente resto del PC, niente rivendita.
- Pareggio: 125 / (1,0585 − 0,1819) = 142,6 h/mese = 4,7 h/giorno (30,4 giorni). Varianti: community 225 h; listino
  2.389 € 76 h (secure) o 119 h (community); su 24 mesi 214 h (secure).
- Scelto il secure perché è il caso onesto per chi parla di dati (macchine in centri di calcolo, non di privati) e
  perché rende l'affitto più caro: l'opinione regge anche nel caso peggiore per lei.

## Angoli scartati
- **«I modelli aperti chiedono sempre meno memoria: prima di comprare guarda quanta ne serve al tuo»** (gpt-oss-20b
  in 16 GB): è il terzo pezzo del trend dello spunto, ma come centro cambia la tesi. Con un modello da 16 GB basta una
  scheda piccola, che costa molto meno anche da comprare, e il pareggio va rifatto con i suoi numeri (non li ho: nessun
  prezzo ufficiale di una 16 GB). Resta nella mossa e in caption.
- **«Perché le schede costano il doppio: la memoria se la prendono i data center»**: un trend senza mossa per chi
  guarda, e il legame col prezzo in negozio è una lettura nostra, non di Micron. Diventa le scene 3-4.
- **«Affittare vuol dire che i tuoi dati escono di casa»**: vero e importante, ma è l'eccezione dell'opinione, non il
  suo centro; sta nella chiusura e in caption.

## Note per il reel
**Query in inglese per le tappe a filmato**
- Scena 3 (centro di calcolo): `data center server racks blinking lights`, `server room corridor`, `server hardware
  close up LEDs`.
- Scena 5 (portatile di sera): `hands typing laptop kitchen night`, `laptop screen progress bar dark room`, `working
  on laptop at home evening hands`.
- Scena 7 (orologio e calendario): `wall clock time lapse`, `calendar pages flipping`, `clock hands moving close up`.
  Candidata a Meshy.

**Filo visivo**: la sagoma della scheda (accesa/spenta), il cartellino del prezzo, il contatore delle ore.

**Numeri** (tutti con la data): 4.500 € (esempio dichiarato, comparatori, 24/09/2026); 1,06 €/h (RunPod 0,99 $, IVA 22%,
BCE 23/09/2026); 0,18 €/h (NVIDIA 575 W × ARERA 31,63 c€/kWh); 125 €/mese e ~140 h/mese (conto nostro, esempio su tre
anni); Micron: oltre il 2027, gradualmente nel 2028. 2.389 € solo se il revisore lo trova su una pagina NVIDIA.

**MESSAGGIO candidato** (caption): «Una GPU grande oggi costa quasi il doppio e la memoria resterà scarsa oltre il
2027. In affitto si paga al secondo. Il conto con i numeri di oggi: comprarla conviene sopra circa 140 ore al mese.»

**CTA candidata**: «Mandalo a chi ha una scheda grafica nel carrello.»

**Claim per il revisore**
- «Intorno ai 4.500 €»: prezzo del giorno sui comparatori, non ufficiale; da riverificare il giorno prima della
  registrazione e da scrivere a schermo con la data. Se cambia, cambia il pareggio (125 €/mese e 140 h).
- Listino 2.389 €: non trovato su una pagina NVIDIA (segnaposto «XXX»); nel reel solo se confermato (marketplace
  NVIDIA Italia).
- «Se la contendono i grandi centri di calcolo dell'IA» (scena 3): parafrasi di Micron («AI-driven demand across all
  segments», «HBM's growth […] further pressures non-HBM supply»); Micron non parla di schede grafiche. Il reel non
  dice «il motivo è», dice «non scenderà presto».
- Scena 4: «resterà così oltre il 2027» e «migliorerà piano solo nel 2028» sono Micron alla lettera («beyond calendar
  2027», «improve gradually in 2028»), è una previsione dell'azienda.
- 1,06 €/h: IVA 22% è un'ipotesi (RunPod dice solo che le tasse si aggiungono e dipendono da indirizzo e pagamento).
- 0,18 €/h: sola scheda a pieno carico, prezzo del cliente tipo vulnerabile in Maggior Tutela; aggiornare se esce il
  IV trimestre ARERA prima della registrazione.
- 140 h/mese: esempio su tre anni, senza resto del PC e senza rivendita; dirlo come esempio.
- «Paghi solo quando lavora»: RunPod fattura al secondo i pod accesi; lo spazio disco persistente si paga anche da
  spento (da verificare sul listino, voce storage), quindi a voce «paghi solo quando lavora» vale per la scheda.

**Note per la caption**
- Le voci del conto (elenco, solo qui): prezzo del giorno 24/09 · affitto secure 0,99 $/h + IVA 22% al cambio BCE ·
  corrente ARERA 31,63 c€/kWh × 575 W · tre anni, senza resto del PC e senza rivendita · con il community cloud (0,69
  $/h, macchine di privati) il pareggio sale a circa 225 h · al listino NVIDIA (se confermato) scende a circa 76 h.
- La mossa in pratica: un modello aperto da 16 GB (gpt-oss-20b, OpenAI, Apache 2.0) gira anche su una RTX 4090 in
  affitto a 0,34 $/h, circa 0,36 € con l'IVA: una sera di tre ore costa circa 1 €. Con un modello così piccolo anche
  comprare una scheda piccola può convenire prima: il conto va rifatto con i suoi numeri.
- RunPod è un fornitore fra tanti, usato per il listino pubblico; nessun rapporto commerciale.
- Crediti delle clip (Pexels) e delle immagini generate (Meshy) come da `CREDITI.md`.
