# Quello che metti in mezzo, l'IA lo legge peggio

**Data:** 2026-09-21
**Tipo:** pillola
**Fonte:** url (contenuti/spunti/2026-09-21-paper-lost-in-the-middle.md)
**Stato:** sceneggiata
**Sceneggiatura:** contenuti/sceneggiature/2026-09-21-perso-nel-mezzo.md

Reel a sé stante, filone «i paper che hanno cambiato l'IA». Nessun personaggio, nessuna azienda, nessun nome
inventato: l'oggetto della situazione è «un documento lungo» (un contratto d'affitto, esempio dichiarato), quindi non
c'è omonimia da chiudere. **Nessun testo attribuito a un modello: la tappa T0b si salta.** Il paper l'ho letto per
intero dal PDF di arXiv (v3, 20 novembre 2023, `curl` + `pdftotext`), tabelle dell'appendice comprese; i numeri
vengono dalla Tabella 1 e dalla Tabella 6. Le righe dello spunto (idea in una frase, figura, mossa) sono del
presentatore: le tengo, le preciso dove il paper dice un'altra cosa (vedi «Mossa: cosa ho cambiato rispetto allo
spunto») e marco come *proposta* quello che aggiungo io.

## Concetto AI illustrato
**Un modello linguistico non legge tutto il testo che gli dai con la stessa attenzione: usa meglio quello che sta
all'inizio e alla fine, e peggio quello che sta in mezzo. Misurato, fa una curva a U.**

Come lo hanno misurato (Liu e altri, Stanford, 2023; TACL 2024). Si fa una domanda di cultura generale (dalle ricerche
vere su Google, con la risposta presa da Wikipedia) e insieme alla domanda si danno al modello **20 brani** di
Wikipedia (circa 4000 token, qualche pagina di testo): **uno solo** contiene la risposta, gli altri 19 parlano dello
stesso argomento ma non la contengono. Poi si ripete tutto spostando il brano giusto: primo, quinto, decimo,
quindicesimo, ventesimo. Il contenuto è identico, cambia solo **la posizione**. Se il modello usasse tutto il testo
allo stesso modo, la precisione resterebbe piatta. Invece fa una U: alta quando il brano giusto è in testa, alta (un
po' meno) quando è in coda, bassa in mezzo.

I numeri, per uno dei modelli provati (GPT-3.5-Turbo, 20 brani, Tabella 6): **75,8 %** di risposte giuste col brano
giusto al primo posto, **53,8 %** al decimo, **63,2 %** al ventesimo. E il dato che fa male: lo stesso modello,
**senza nessun brano**, cioè a memoria, risponde giusto nel **56,1 %** dei casi (Tabella 1, «closed-book»). Con il
brano giusto messo in mezzo fa peggio che se non gli avessi dato niente. Il paper lo dice così: «in the worst case,
performance in 20- and 30-document settings is lower than performance without any input documents».

Tre precisazioni per non semplificare in falso:
- **Non tutti i modelli del paper fanno una U profonda.** Claude-1.3, per esempio, va da 59,9 % (primo) a 56,8 %
  (decimo) a 60,1 % (ventesimo): la U c'è, ma è bassa, e in mezzo resta sopra la sua prova a memoria (48,3 %). La
  figura del reel usa GPT-3.5-Turbo e lo dichiara come «uno dei modelli». Anche GPT-4, provato su un sottoinsieme di
  500 domande, «still shows a U-shaped performance curve» (Appendice D).
- **Non dipende dal non riuscire a leggere un testo lungo.** Gli stessi modelli, a cui si dà il solo brano giusto,
  rispondono bene (76-88 %, «oracle», Tabella 1). E nemmeno dall'avere una finestra più grande: le versioni «a
  contesto lungo» (16K, 100K) hanno curve «nearly identical» a quelle normali. Il testo ci sta tutto; è il **modo di
  usarlo** che dipende dalla posizione.
- **Il perché non è chiuso.** L'attenzione di un transformer può, in linea di principio, pescare qualunque parola del
  testo («technically equally capable of retrieving any token»): la U è una preferenza imparata, non un limite
  meccanico. Il paper fa tre prove preliminari: i modelli che leggono il testo in tutte e due le direzioni
  (encoder-decoder) sono più stabili, ma solo su testi della lunghezza su cui sono stati addestrati; mettere la
  domanda anche **prima** dei documenti aiuta molto nella ricerca di una chiave in un elenco, ma **quasi niente** nelle
  domande sui documenti; e la U c'è anche nei modelli prima dell'addestramento a seguire istruzioni, quindi non è
  colpa solo di quello. Chiamano in causa l'effetto di posizione seriale della psicologia (Ebbinghaus, Murdock 1962):
  anche le persone, di una lista, ricordano meglio le prime e le ultime voci. È un'analogia che fanno loro, non una
  spiegazione del meccanismo.

La conseguenza pratica, che il paper scrive nella parte sul caso reale (§5): **più contesto non vuol dire risposte
migliori**. Passare da 20 a 50 brani migliora la risposta di «∼1.5%» per GPT-3.5-Turbo e «∼1%» per Claude-1.3, mentre
allunga il testo; le vie che indica sono **riordinare** (portare l'informazione che serve verso l'inizio) e **dare
meno documenti** quando si può.

**E oggi?** I modelli del paper sono del 2023. Le fonti ufficiali recenti dicono due cose insieme:
- l'effetto è più piccolo sulle ricerche semplici: i produttori dichiarano ricerche di una singola informazione quasi
  perfette su testi lunghissimi (Google: «around 99%» per un singolo «ago»; OpenAI, per GPT-4.1: «strong performance»
  fino a un milione di token sui test dell'ago nel pagliaio);
- ma non è sparito, e peggiora appena il compito si fa meno letterale o chiede più cose insieme: NoLiMa (Adobe
  Research e LMU Monaco, ICML 2025) su 13 modelli che dichiarano almeno 128K token trova che a 32K token 11 scendono
  sotto la metà della loro prestazione su testi corti, e riosserva un effetto «lost-in-the-middle» nei compiti a un
  passaggio; Google scrive che con più «aghi» il modello «does not perform with the same accuracy».

E soprattutto: **chi costruisce i modelli, nel 2025-2026, dà ancora il consiglio di posizione** nelle proprie guide
(Anthropic: documenti lunghi in cima, domanda in fondo; Google: domanda alla fine; OpenAI: istruzioni all'inizio e
alla fine del contesto lungo). Il reel lo dice onestamente: la curva di oggi non è quella del 2023, la mossa resta
buona.

## Situazione
Una cosa che chi usa l'IA ha fatto almeno una volta: **incolli (o carichi) un documento lungo e fai una domanda**. Il
contratto d'affitto di trenta pagine, e ti serve sapere con quanto preavviso puoi dare disdetta; la clausola sta a
metà, fra le spese condominiali e il deposito. Lo dai tutto all'IA, «così sa tutto», e in fondo scrivi la domanda.
La risposta è sicura, ordinata, e generica: «di solito il preavviso è di sei mesi», come se quella pagina non ci
fosse. (Esempio dichiarato: il paper non misura contratti, misura brani di Wikipedia e domande di cultura generale.)

Il momento di prova per chi guarda (*proposta*): prima di mostrare la curva, il presentatore gli chiede di scommettere.
«Il pezzo con la risposta lo sposto: in testa, in mezzo, in fondo. Dove lo trova meglio?» Chi guarda di solito dice
«non cambia niente, l'ha letto tutto», oppure «in fondo, è l'ultima cosa che ha letto». La U smentisce tutte e due.

A schermo la situazione diventa oggetti, non battute: una pila di fogli-sagoma, un foglio acceso che è quello giusto,
un punto interrogativo in fondo alla pila (la domanda), e un grafico che si disegna mentre il foglio si sposta.

## Messaggio centrale
L'IA non legge tutto quello che le dai con la stessa attenzione: l'inizio e la fine sì, il mezzo meno. Quindi quello
che conta non lasciarlo in mezzo: mettilo in cima, e la domanda in fondo.

## Struttura narrativa
**Schema di partenza:** @gianluigiballarani · r0012 — elenco assurdo → spiegazione scientifica → ridimensionamento
onesto → contrasto finale ironico.

> È un pessimo momento per essere [soggetto], perché [cosa assurda]. [Elenco in crescendo]. Tutto in pochi giorni. Com'è possibile? [Scoperta + numeri + analogia]. Ovviamente non significa che [lettura esagerata]. Ma per la prima volta [vera novità]. Per [cosa seria] ci sono voluti [tempo lungo]; per [cosa frivola], [tempo brevissimo].

Perché questo. È lo schema del corpus costruito su **un fenomeno strano che si vede → la domanda «com'è possibile?» →
la spiegazione con i numeri e un'analogia → il ridimensionamento onesto → il rilancio**. Al nostro reel serve proprio
questa coppia finale: il paper è del 2023, i modelli di oggi sbagliano meno, e il reel deve dirlo **senza** smontarsi
(«ovviamente non significa che… ma…»). L'analogia dello schema qui c'è già ed è del paper stesso (la lista che ricordi
all'inizio e alla fine). Le tecniche portanti (`domanda-pivot`, `analogia`, `ridimensionamento`, `contrasto`) stanno
tutte in «Tecniche condivise». Gli schemi già usati dalle altre idee (r0045, r0037, r0040, r0020) li ho evitati.

**Adattamento** (una riga per fase):
- [È un pessimo momento per essere X, perché (cosa assurda)] → l'apertura a volto pieno porta la cosa strana come
  esperienza di chi guarda: gli hai dato tutto il documento e la risposta ignora proprio il pezzo che ti serviva.
- [elenco in crescendo] → non un elenco: una sola esperienza, allargata in una frase sul filmato («gli dai tutto,
  così sa tutto…»). L'elenco di esempi (contratto, verbale, tesi, regolamento) va in caption.
- [Com'è possibile?] → la domanda-pivot diventa la scommessa di chi guarda: «dove lo trova meglio: in testa, in
  mezzo, in fondo?», con un vuoto di un secondo prima della curva.
- [scoperta + numeri + analogia] → l'esperimento dei venti brani e la U (tre punti, tre numeri, «Stanford, 2023»);
  l'analogia della lista della spesa sul filmato; poi il numero che fa male: in mezzo, peggio che senza documenti.
- [Ovviamente non significa che (lettura esagerata)] → «erano modelli di qualche anno fa, e quelli di oggi su una
  ricerca semplice sbagliano molto meno».
- [Ma per la prima volta (vera novità)] → il rilancio cambia segno: «ma chi li costruisce ti dà ancora lo stesso
  consiglio», e la mossa, fatta vedere: il foglio giusto esce dal fondo della U e sale in cima; la domanda resta in
  fondo.
- [contrasto finale: tempo lungo / tempo brevissimo] → contrasto finale a battuta, sul prima/dopo della mossa: il
  documento è lo stesso, cambia dove metti il pezzo che conta.

**Tecniche** (da «Tecniche condivise»):
- `domanda-pivot`: la scommessa «in testa, in mezzo o in fondo?» fra la situazione e la curva (scena 3).
- `analogia`: la lista della spesa, di cui ricordi le prime e le ultime voci (scena 4, a filmato); è l'analogia del
  paper stesso (§6.3), detta come analogia e non come spiegazione.
- `ridimensionamento`: «erano modelli di qualche anno fa» (scena 6), subito seguito dal rilancio.
- `contrasto`: stesso documento, stesse parole, risultato diverso solo per la posizione (scena 3 e chiusura); e la
  linea «senza documenti» contro il punto in mezzo (scena 5).

**Escluse:**
- `gancio-ironico` e `satira` («è un pessimo momento per essere…»): l'ironia di r0012 è il registro di quell'account
  e qui sposterebbe l'attenzione dal problema di chi guarda; l'apertura è una domanda sua.
- `elenco-in-crescendo`: un elenco letto a camera no (la chiusura a elenco non è piaciuta, e anche a metà è
  un elenco); gli esempi di documenti lunghi vanno in caption.
- `firma-di-chiusura` («Buona giornata.»): è una firma, non si copia.
- Il contrasto di **tempi** di r0012 (dieci anni contro una settimana): non c'è un contrasto di tempi vero nel nostro
  tema e inventarlo sarebbe una forzatura; resta il contrasto di posizione.
- Lunghezza: r0012 dura oltre un minuto e mezzo e ha nove mosse; qui otto scene e obiettivo ≤ 70 s. Se serve
  tagliare, la prima a perdere un beat è la scena 5 (il perché va in caption), poi la scena 6 si riduce a una frase.

## Come si mostra
*Il reel si guarda muto: le caption col parlato sono in fondo, a schermo non c'è niente da leggere. Qui la figura che
regge il concetto senza parole.*

**La figura madre: una fila di venti fogli, uno acceso, e una curva che si disegna mentre il foglio acceso si
sposta.** Venti fogli-sagoma identici (righe grigie, nessun testo leggibile) in fila da sinistra a destra, come le
pagine di un documento stese sul tavolo. Uno è acceso (colore d'accento): è quello con la risposta. In fondo alla
fila, dopo il ventesimo, una carta col punto interrogativo: la domanda. Sopra la fila, un grafico vuoto: in orizzontale
la posizione del foglio acceso, in verticale quante volte la risposta è giusta.

- **Scena 3 — la U che si disegna (una quantità, un gesto).** Il foglio acceso sta al primo posto: sopra di lui si
  accende un punto in alto, «76». Il foglio scivola al decimo posto: il punto cade, «54». Scivola al ventesimo: risale
  a metà, «63». La linea unisce i punti: è una U storta, più alta a sinistra. Si capisce senza leggere: stessa fila,
  stesso foglio, solo spostato, e la risposta giusta cala in mezzo. Etichetta piccola in basso: «Stanford, 2023».
- **Scena 5 — qualcosa che si svuota (prima/dopo).** La fila di fogli si dissolve; resta solo la carta col punto
  interrogativo, da sola: il modello senza documenti. Una linea tratteggiata orizzontale si stende sul grafico, a
  «56». Poi tornano i fogli e la U: il punto in mezzo sta **sotto** la linea tratteggiata e pulsa. La figura dice:
  dargli il foglio giusto e metterlo in mezzo è peggio che non dargli niente. Nessuna parola serve; al più «0 fogli»
  accanto alla linea tratteggiata (due parole).
- **Scena 7 — il gesto della mossa (prima/dopo).** Stessa fila, stesso grafico. Il foglio acceso è nel fondo della U
  (decimo posto). Una mano-freccia lo solleva e lo porta in testa alla fila, sotto il punto alto della curva, che si
  riaccende. La carta col punto interrogativo resta in fondo, in un punto anch'esso alto. Poi (facoltativo) metà dei
  fogli grigi escono dalla fila e la fila si accorcia: «dagliene meno». Chi guarda vede il gesto che farà domani:
  prendere il pezzo che conta e spostarlo.

**Mossa wow candidata**: la linea tratteggiata «senza documenti» che scende sul grafico e il punto di mezzo che le
passa sotto (scena 5). È l'unico momento in cui un numero rovescia l'intuizione («più informazioni, meno risposte
giuste»), e si vede in un colpo.

Le due scene a filmato che fanno da analogia e da passaggio (lista della spesa, telefono vecchio e nuovo) sono in
«Note per il reel», con le query.

## Cosa impara chi guarda
- **Un modo nuovo di leggere**: quando l'IA «ignora» un pezzo del documento, non è che non l'abbia ricevuto; è che
  stava nel punto in cui guarda meno. Il testo lungo non è letto in modo uniforme: l'inizio e la fine pesano di più.
- **La mossa, per domani**: prima di chiedere qualcosa su un documento lungo, prendi il pezzo che conta (la clausola,
  il paragrafo, la tabella) e mettilo **in cima**; la domanda mettila **in fondo**. Se non sai dov'è il pezzo che conta,
  non darle tutto in una volta: dagliene un pezzo alla volta.
- **Il criterio per capire se ha funzionato** (*proposta*): chiedile di riportare la frase esatta del documento da cui
  ha preso la risposta. Se la frase c'è, ed è nel pezzo che ti serviva, ha letto il punto giusto; se ti dà una frase
  generica o che non ritrovi, la risposta non viene dal tuo documento.

## Pilastro
Dove sbaglia (e, con la mossa, cosa può fare per te).

## Perché ora
Oggi i documenti lunghi all'IA si danno di continuo: si caricano PDF interi, cartelle di file, conversazioni lunghe
settimane, e le finestre di contesto dichiarate arrivano a un milione di token. La promessa implicita è «le dai tutto
e sa tutto». Il paper del 2023 è quello che ha dato un nome a questo punto cieco («lost in the middle») ed è ancora
citato come riferimento; le guide ufficiali dei produttori, aggiornate nel 2025-2026, ripetono il consiglio di
posizione. È il momento giusto per un reel che non dice «l'IA legge male» ma «l'IA legge in un certo modo, e tu
puoi approfittarne».

## Fonte
**La pagina letta (la fonte dello spunto, ufficiale: studio pubblicato).**
- Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang, «Lost in
  the Middle: How Language Models Use Long Contexts», *Transactions of the Association for Computational Linguistics*,
  vol. 12, pp. 157-173, 2024 (DOI 10.1162/tacl_a_00638). Preprint arXiv 2307.03172, v3 del 20 novembre 2023, letto
  per intero dal PDF: https://arxiv.org/abs/2307.03172 · pubblicazione: https://aclanthology.org/2024.tacl-1.9/.
  Stanford University (con UC Berkeley e Samaya AI). Etichetta a schermo: «Stanford, 2023».
- **Fatti presi, con le parole del testo:**
  1. «performance is often highest when relevant information occurs at the beginning or end of the input context,
     and significantly degrades when models must access relevant information in the middle of long contexts, even
     for explicitly long-context models» (abstract). La figura 1 la chiama «U-shaped performance curve», con «primacy
     bias» e «recency bias».
  2. Il compito: una domanda (NaturalQuestions-Open, ricerche vere su Google) e k documenti, «exactly one of the
     documents contains the answer»; «k − 1 “distractor” documents» recuperati apposta come i più pertinenti senza
     la risposta; posizione spostata cambiando l'ordine (§2.1). Misura: accuratezza = una delle risposte corrette
     compare nell'uscita.
  3. Tabella 6 (20 documenti, circa 4K token), GPT-3.5-Turbo: 75,8 % (posizione 1), 57,2 % (5), **53,8 % (10)**,
     55,4 % (15), 63,2 % (20). Tabella 1: GPT-3.5-Turbo closed-book **56,1 %**, oracle 88,3 %. Testo: «GPT-3.5-Turbo's
     multi-document QA performance can drop by more than 20%—in the worst case, performance in 20- and 30-document
     settings is lower than performance without any input documents (i.e., closed-book performance; 56.1%)» (§2.3).
  4. «Extended-context models are not necessarily better at using input context» (§2.3): curve «nearly
     superimposed» fra GPT-3.5-Turbo e la versione 16K.
  5. §5: «Using more than 20 retrieved documents only marginally improves reader performance (∼1.5% for GPT-3.5-Turbo
     and ∼1% for Claude-1.3)»; suggerisce «effective reranking of retrieved documents (pushing relevant information
     closer to the start of the input context) or ranked list truncation (retrieving fewer documents when
     appropriate)».
  6. §6.3: la U ha una connessione con il «serial-position effect» della psicologia (Ebbinghaus 1913; Murdock 1962):
     «humans tend to best remember the first and last elements of the list»; e «the self-attention mechanisms […] is
     technically equally capable of retrieving any token from their contexts».
- **Cosa il paper non dice:**
  - Niente sui modelli di oggi: i modelli sono di metà 2023 (GPT-3.5-Turbo 0613, Claude-1.3, MPT-30B, LongChat-13B;
    GPT-4 solo su 500 domande; Llama-2 in appendice). Testi fino a circa 6K token nelle domande sui documenti, 16K
    nella ricerca di chiavi: molto meno dei contesti di oggi.
  - Non misura documenti come contratti o verbali, né conversazioni: brani di Wikipedia e domande fattuali brevi, più
    un compito sintetico di chiavi e valori.
  - Non spiega il perché: le prove del §4 sono dichiarate «preliminary». Non dice che la causa è l'attenzione o
    l'addestramento; dice cosa cambia la curva e cosa no.
  - Non prova la mossa «dì dove guardare», né quella di «spezzare il documento»: la prima non è misurata; della
    seconda c'è solo il parente stretto «meno documenti» (§5). Mettere la domanda **anche prima** dei documenti
    «minimally affects performance trends in the multi-document question answering task» (§4.2): nel paper **non** è
    una cura per le domande sui documenti.
  - La U non è uguale per tutti: per Claude-1.3 è bassa, e in mezzo non scende sotto la prova a memoria.

**Fonti ufficiali sul «vale ancora oggi?» (studi pubblicati e documentazione dei produttori).**
- Modarressi, Deilamsalehy, Dernoncourt, Bui, Rossi, Yoon, Schütze, «NoLiMa: Long-Context Evaluation Beyond Literal
  Matching», ICML 2025 (PMLR 267), Adobe Research e LMU Monaco: https://proceedings.mlr.press/v267/modarressi25a.html
  (arXiv 2502.05167). Misura: domande in cui la domanda e l'informazione nascosta nel testo hanno poche parole in
  comune. Fatti: 13 modelli che dichiarano almeno 128K token; «at 32K, 11 models drop below 50% of their strong
  short-length baselines»; GPT-4o da 99,3 % a 69,7 %; nei compiti a un passaggio riosservano un calo quando
  l'informazione sta in mezzo (dal riassunto di WebFetch della versione HTML: **frase esatta da ritrovare** nel
  testo, vedi claim).
- Anthropic, documentazione «Prompting best practices», sezione sui documenti lunghi (pagina consultata il
  2026-09-21, che elenca i modelli Claude attuali): «Put longform data at the top: Place your long documents and
  inputs near the top of your prompt, above your query, instructions, and examples»; «Queries at the end can improve
  response quality by up to 30 percent in tests, especially with complex, multidocument inputs»; e «ask Claude to
  quote relevant parts of the documents first». https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
  Misura: test interni non descritti; il 30 % non entra nel reel.
- Google, Gemini API, «Long context» (aggiornata il 2026-06-22): «the model's performance will be better if you put
  your query / question at the end of the prompt (after all the other context)»; singolo «ago» circa 99 %, con più
  «aghi» «the model does not perform with the same accuracy». https://ai.google.dev/gemini-api/docs/long-context
- OpenAI, «GPT-4.1 Prompting Guide» (cookbook, 2025): «If you have long context in your prompt, ideally place your
  instructions at both the beginning and end of the provided context, as we found this to perform better than only
  above or below.» https://developers.openai.com/cookbook/examples/gpt4-1_prompting_guide
- Per l'analogia: Murdock, B. B. Jr. (1962), «The serial position effect of free recall», *Journal of Experimental
  Psychology*, 64(5), 482 (citato dal paper; non letto da me: entra solo come analogia, senza numeri).

## Angoli scartati
- **«Più contesto non vuol dire risposte migliori»** (il §5: da 20 a 50 documenti, +1,5 %). Concetto vero e utile, ma
  la figura (due curve che si appiattiscono, «saturates») è più astratta della U, e la mossa («dagliene meno») è la
  metà debole di quella principale. Resta come coda della mossa e in caption.
- **«Finestra grande non vuol dire lettura attenta»** (versioni 16K e 100K identiche alle normali). Buono come
  obiezione («ma il mio modello ha un milione di token!»), ma è un confronto fra nomi di modelli del 2023 che chi
  guarda non conosce; lo tengo come una frase nella scena 6, non come tesi.
- **La psicologia della lista (effetto di posizione seriale) come tesi** («l'IA ricorda come noi»): è l'analogia del
  paper, non il suo risultato, e usata come tesi diventa un'antropomorfizzazione che il paper non sostiene. Resta
  analogia, in una scena a filmato.
- **La ricerca di chiavi (JSON) come esempio**: più pulita come esperimento, ma nessuno a casa cerca UUID; e lì mettere
  la domanda prima e dopo risolve quasi tutto, il che confonderebbe la mossa.

## Note per il reel
**Hook candidato** (la sola frase, detta da lui a tutto schermo, nessuna immagine):
- «Hai mai incollato un documento lungo all'IA, e la risposta ha ignorato proprio il punto che ti serviva?» (18 parole)
- Alternativa: «Dai all'IA un documento di trenta pagine: secondo te le legge tutte con la stessa attenzione?» (16)
- **TITOLO della copertina** (la tesi): «Quello che metti in mezzo, l'IA lo legge peggio». Alternative: «L'IA legge
  l'inizio e la fine. Il mezzo, meno»; «Perso nel mezzo: dove l'IA legge peggio».

**Percorso** (*proposta*, otto scene; sei in mezzo: tre animate e tre a filmato, alternate, nessuna coppia di filmati;
la VOCE la scrive lo sceneggiatore):
1. **Apertura, volto pieno**: l'hook.
2. **A filmato · la situazione.** Voce generica: succede a tutti, gli dai tutto «così sa tutto», e la risposta è
   sicura ma sembra non aver visto quella pagina. Immagine: **una persona alla scrivania, di sera, che scorre con la
   rotella un documento lunghissimo sul portatile, si ferma, rilegge lo schermo e aggrotta la fronte**; oppure mani
   che sfogliano un plico di fogli spillati. Query: `person scrolling long document on laptop`, `frustrated woman
   reading laptop screen at night`, `hands flipping through thick stack of papers`.
3. **Animata · la scommessa e la U.** I venti fogli, uno acceso, la domanda in fondo. «Dove lo trova meglio?», un
   secondo di vuoto, poi il foglio scivola: 76 → 54 → 63, la curva si disegna. «Stanford, 2023». Qui stanno i numeri
   e il meccanismo dell'esperimento (stesso contenuto, cambia solo il posto).
4. **A filmato · l'analogia.** Voce generica: anche a noi succede; di una lista ricordi le prime cose e le ultime, e
   quelle in mezzo le dimentichi (detto come somiglianza, non come spiegazione). Immagine: **al supermercato, una
   persona con il carrello si ferma in una corsia, guarda il foglietto della spesa, poi alza gli occhi come chi cerca
   di ricordare cosa manca**. Query: `man reading shopping list in supermarket aisle`, `woman trying to remember
   grocery list`, `handwritten shopping list in hand grocery store`.
5. **Animata · il numero che rovescia.** La fila sparisce, resta la domanda da sola; la linea tratteggiata a 56;
   tornano i fogli, il punto di mezzo sotto la linea. «Con il foglio giusto in mezzo, peggio che senza fogli.» Una
   frase sul perché, prudente: la macchina potrebbe guardare dappertutto, ma ha imparato a guardare di più i bordi,
   e il perché preciso non lo sa ancora nessuno.
6. **A filmato · il ridimensionamento e il rilancio.** Voce generica: erano modelli di qualche anno fa, e quelli di
   oggi su una ricerca semplice sbagliano molto meno; ma le istruzioni di chi li costruisce dicono ancora la stessa
   cosa. (Niente anni e niente numeri a voce qui: «2023» sta già in scena 3.) Immagine: **un vecchio telefono e uno
   nuovo appoggiati accanto su un tavolo, una mano prende quello nuovo**. Query: `old mobile phone next to new
   smartphone on table`, `hand picking up new smartphone from desk`, `comparing old and new phones`.
7. **Animata · la mossa.** Il foglio acceso esce dal fondo della U e sale in testa, la domanda resta in fondo, i punti
   si riaccendono in alto; facoltativo, metà dei fogli grigi esce. Qui il criterio: chiedile la frase esatta da cui
   ha preso la risposta (a schermo: una virgoletta che si accende sul foglio in testa, niente testo).
8. **Chiusura, volto pieno**: la battuta.

Obiettivo ≤ 70 s, circa 170-180 parole di VOCE. La scena più densa è la 3: non più di quattro beat (la situazione a
schermo, la scommessa, la curva, l'etichetta della fonte).

**Filo visivo** (tre oggetti che tornano in tutte le scene animate; niente testo denso):
- **La fila dei venti fogli-sagoma** (componente `Sagome` o `Fila` di fogli), sempre nella stessa posizione in basso
  nell'area del contenuto.
- **Il foglio acceso** (colore d'accento): quello con la risposta. Si sposta in scena 3, resta in mezzo in scena 5,
  sale in testa in scena 7.
- **La carta col punto interrogativo** in fondo alla fila: la domanda. Resta sola in scena 5 (senza documenti),
  resta in fondo in scena 7.
- Il grafico con la U sopra la fila, gli stessi assi in tutte e tre le scene; numeri solo come punti: «76», «54»,
  «63», «56» (tratteggiato). Mai più di un numero nuovo per beat.
Due scene animate di fila non si vedono mai (in mezzo c'è sempre un filmato), ma la 3, la 5 e la 7 devono avere un
cambio grande diverso: il foglio che scivola (3), la fila che si svuota e la linea che cala (5), il foglio sollevato
in testa (7).

**Numeri.** In VOCE al massimo tre, tutti da Liu e altri (TACL 2024, preprint 2023), GPT-3.5-Turbo con 20 brani:
«tre volte su quattro» col brano in testa (75,8 %), «poco più di una su due» in mezzo (53,8 %), e il confronto con
«senza documenti» (56,1 %). A schermo come punti del grafico, arrotondati: 76, 54, 63, 56. «Venti fogli» è il numero
dell'esperimento (20 documenti), non un esempio. Il contratto di trenta pagine e la clausola sulla disdetta sono
**esempio dichiarato**. Nessun numero dai documenti dei produttori o da NoLiMa entra nel reel (vanno in caption, se
il presentatore vuole).

**Chi si nomina nel reel.** A voce e a schermo solo l'etichetta «Stanford, 2023», perché regge i numeri della curva.
Nessun autore a voce. Le guide dei produttori si dicono in generale («chi li costruisce»), senza marchi; i nomi
vanno in caption. Nessuna idea viene da un post o da un articolo non ufficiale: nessun credito di quel tipo da
annotare.

**Mossa: cosa ho cambiato rispetto allo spunto.** Lo spunto dice «le cose importanti mettile all'inizio o alla fine
della richiesta; un documento lungo dallo a pezzi, o dì dove guardare». Tengo la prima metà, precisata così: **il
pezzo che conta in cima, la domanda in fondo** (in cima lo dice il §5 del paper, «pushing relevant information closer
to the start»; la domanda in fondo la dicono le guide di Anthropic e Google). «Dallo a pezzi» diventa la coda «se non
sai dov'è, dagliene un pezzo alla volta» (parente di «retrieving fewer documents», §5). **«Dì dove guardare» lo tolgo
dal reel**: il paper non lo misura, e la sua prova più vicina (ripetere la domanda anche prima dei documenti) nelle
domande sui documenti non ha cambiato quasi niente (§4.2). Se il presentatore lo vuole, va come consiglio senza
prova, e il revisore deve saperlo.

**MESSAGGIO candidato** (per la caption del post, ≤ 12 parole):
- «Il pezzo che conta in cima, la domanda in fondo.» (10)
- Alternative: «L'IA legge l'inizio e la fine. Il mezzo, meno.» (9); «Non lasciare in mezzo quello che conta.» (7)

**Chiusura a battuta** (*proposta*, ≤ 18 parole di VOCE, sceglie lo sceneggiatore): «Il documento è lo stesso, le
parole sono le stesse. Cambia solo dove metti il pezzo che conta.» (18) Seconda direzione: «Darle tutto non vuol dire
che legga tutto. Quello che conta, non lasciarlo in mezzo.» (17)

**CTA** (una): «Salvalo per la prossima volta che incolli un documento lungo.» Alternativa, invio con destinatario
ovvio: «Mandalo a chi carica PDF interi all'IA e si fida della risposta.»

**Claim per il revisore** (con le formule prudenti)
- **«La U»**: vale per il compito di domande su 20 brani di Wikipedia, con modelli del 2023. Formula: «in un
  esperimento di Stanford», «uno dei modelli provati». Mai «tutte le IA», mai «ogni volta».
- **I numeri 76 / 54 / 63 e 56**: GPT-3.5-Turbo (0613), 20 documenti, Tabella 6 e Tabella 1. «Tre volte su quattro»
  per 75,8 % e «poco più di una su due» per 53,8 % reggono; non dire «il doppio» né «crolla del 30 %» (sono 22 punti
  percentuali, il paper scrive «more than 20%»).
- **«In mezzo peggio che senza documenti»**: vale per GPT-3.5-Turbo (e il paper dice «in the worst case», con 20 e 30
  documenti). **Non** vale per Claude-1.3 (in mezzo 56,8 %, a memoria 48,3 %). Formula: «per uno dei modelli, con il
  foglio giusto in mezzo, andava peggio che senza fogli». Mai generalizzare.
- **Il perché**: nessuna causa detta come certa. Formula: «ha imparato a guardare di più i bordi, e il perché preciso
  non è ancora chiaro». Non dire «perché l'attenzione si concentra ai bordi» come meccanismo dimostrato.
- **L'analogia della lista**: il paper la fa (§6.3), come connessione, non come spiegazione. Formula: «un po' come
  noi con la lista della spesa». Non dire «ricorda come noi» né «ha la memoria corta».
- **«Oggi sbagliano molto meno su una ricerca semplice»**: si appoggia alle dichiarazioni dei produttori (Google
  «around 99%» su un singolo ago; OpenAI su GPT-4.1) e a NoLiMa (cali forti appena il compito non è letterale). Da
  controllare: **la frase esatta di NoLiMa sull'effetto «lost-in-the-middle» nei compiti a un passaggio** (l'ho presa
  dal riassunto della pagina HTML, non l'ho letta nel PDF). Se non si ritrova, la scena 6 si appoggia solo alle guide
  dei produttori e si dice «l'effetto è più piccolo, non sparito» senza citare NoLiMa.
- **«Chi li costruisce dà ancora lo stesso consiglio»**: tre guide ufficiali (Anthropic, Google, OpenAI), citate
  sopra con le parole esatte; attenzione alla differenza: Anthropic e Google parlano di **domanda in fondo**, OpenAI di
  **istruzioni in cima e in fondo**, il paper di **informazione che serve verso l'inizio**. La mossa del reel («pezzo
  che conta in cima, domanda in fondo») è la sintesi di queste; non va attribuita a nessuno in particolare.
- **Le date**: paper su arXiv a luglio 2023 (v3 novembre 2023), pubblicato su TACL nel 2024. Etichetta «Stanford,
  2023» come da spunto; se il revisore preferisce l'anno di pubblicazione, «Stanford, 2024».
- **Il contratto di trenta pagine** è esempio dichiarato: il paper usa circa 4000 token (qualche pagina). Non dire che
  il paper ha provato contratti né documenti di trenta pagine.

**Note per la caption**
- Fonte: Liu e altri, «Lost in the Middle: How Language Models Use Long Contexts», Stanford University, TACL 2024
  (arXiv 2023), https://arxiv.org/abs/2307.03172. Dire nel testo che il grafico è di GPT-3.5-Turbo con 20 brani di
  Wikipedia, e che i modelli di oggi mostrano un effetto più piccolo sulle ricerche semplici.
- La mossa non è nostra: viene dal paper (§5, riordinare e dare meno documenti) e dalle guide di Anthropic, Google e
  OpenAI (link sopra). In caption una riga: «il consiglio lo danno le guide ufficiali di chi costruisce i modelli».
- Esempi di documenti lunghi, in elenco (solo in caption): il contratto d'affitto, il verbale della riunione, il
  regolamento di condominio, la tesi da riassumere, la chat di gruppo di un mese.
- La tecnica di controllo («chiedile di citare la frase esatta») è nella guida di Anthropic («ask Claude to quote
  relevant parts of the documents first»): se si usa come criterio, dirlo in caption.
- Analogia: effetto di posizione seriale (Murdock, 1962), citato dal paper.
