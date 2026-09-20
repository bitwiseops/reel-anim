# Generativa non vuol dire creativa: la candidatura di chiunque

**Data:** 2026-09-20
**Tipo:** pillola
**Fonte:** testo (contenuti/spunti/2026-09-15-generativa-probabile.md)
**Stato:** idea
**Sceneggiatura archiviata:** contenuti/archivio/generativa-probabile/2026-09-20/sceneggiatura.md (regime vecchio, 2026-09-20)
**Uscite:** contenuti/idee/uscite/generativa-probabile-2026-09-20.md

Reel a sé stante: chi lo guarda non ha visto nient'altro. Azienda, annuncio, persone e vicenda sono inventati da capo
per questo reel. Le mail mostrate verranno da uscite vere (tappa T0b), generate sulle richieste scritte in fondo:
questa idea **non contiene testi attribuiti a un modello** e tutto quello che dice sulle uscite è un'ipotesi da
contare. (Cosa si è guardato del lavoro precedente per non ripetersi sta solo in fondo, in «Note interne».)

## Concetto AI illustrato
Un modello linguistico produce testo **continuando** quello che ha davanti. A ogni passo calcola, per ogni possibile
pezzo successivo (un *token*: spesso un pezzo di parola, non una parola intera), quanto è probabile che venga dopo
**tutto ciò che c'è prima**: le istruzioni di sistema, la tua richiesta, il testo che ha già scritto. Poi ne estrae
uno a sorte fra i più probabili (campionamento con temperatura e top-p: quindi non per forza il primo, e non lo stesso
ogni volta), lo aggiunge in fondo e ricomincia. «Generativa», in senso tecnico, vuol dire questo: un modello che
rappresenta la probabilità dei testi e ne produce campioni. La parola descrive **come** nasce il testo, non **quanto**
è originale.

Da qui due conseguenze, che sono la stessa cosa vista da due lati.
- **Il lato buono.** Le continuazioni ad alta probabilità sono grammaticali, nel registro giusto, nella forma che il
  genere si aspetta. Una mail di candidatura è un genere molto codificato (oggetto, saluto, perché scrivo, cosa so
  fare, disponibilità, saluti) e il modello ne ha visti moltissimi esempi: in pochi secondi la scrive corretta e
  ordinata.
- **Il limite.** Le continuazioni più probabili sono anche le più battute: le più frequenti nei testi e, dopo il
  post-training, quelle che le persone hanno premiato di più, perché chi valuta tende a preferire il familiare
  (Kirk et al., ICLR 2024; Zhang et al., 2025, sul *typicality bias*). Su richieste aperte lo stesso modello
  interrogato più volte, e modelli diversi fra loro, convergono su risposte simili (Jiang et al., *Artificial
  Hivemind*, NeurIPS 2025). *Riferimenti citati a memoria: da verificare dal revisore; nessuno entra in VOCE.*

Il punto che regge il reel: **di chi scrive, il modello ha solo quello che sta nel contesto.** Se tre persone diverse
incollano lo stesso annuncio e fanno la stessa richiesta, il modello ha davanti lo stesso testo tre volte: non può
scrivere tre mail che parlano di tre persone, perché di quelle persone nel contesto non c'è niente. Dove servirebbero
i fatti di chi si candida può solo lasciare un buco (un segnaposto fra parentesi) oppure riempirlo con il plausibile
(un'esperienza generica che vale per chiunque): *quale delle due cose fa, lo dicono le uscite A*.

«Sii originale.» è contesto anche lui, e qualcosa sposta: rende più probabili le continuazioni che **nei testi**
seguono una richiesta di originalità (un attacco a effetto, un'immagine sul prodotto dell'azienda: *ipotesi da
verificare sulle uscite B*). Ma non aggiunge nessuna informazione su chi scrive: l'originalità che ottieni è
l'originalità più probabile, e chi sei tu resta vuoto come prima. Una riga con un fatto vero e specifico aggiunge
invece informazione, e cambia la probabilità di molti pezzi successivi: quel fatto diventa l'argomento della mail. Nel
modello non è cambiato niente (stessi pesi, stesso modo di estrarre): è ancora una continuazione probabile, ma di un
altro inizio.

Due cautele, perché il reel non sia né una lode né una stroncatura. Primo: non si dice che l'IA «non è creativa».
Doshi & Hauser (Science Advances, 2024: *da verificare*) trovano racconti giudicati più creativi uno per uno e più
simili fra loro nel complesso; il reel dice che **il nome non promette originalità** e che l'uscita senza fatti tuoi
è quella di chiunque. Secondo: la mossa ha un limite. Dato un fatto, il modello può abbellirlo o aggiungerne di
plausibili intorno (*da verificare sulle uscite C*): la mail si rilegge, e ogni fatto dev'essere tuo davvero.

## Situazione
*Proposta* (lo spunto dà la situazione, la mail di risposta a un annuncio; scena, azienda e persone sono mie).

C'è un annuncio, fisso per tutto il reel e dichiarato inventato a schermo («annuncio, azienda e persone inventati»):

> **Torrefazione Tostavento (Pesaro): assistenza clienti.** Tostiamo caffè e lo spediamo in tutta Italia dal nostro
> negozio online. Cerchiamo una persona che risponda a mail e telefonate dei clienti e segua ordini, resi e
> abbonamenti. Serve almeno un anno di lavoro a contatto con il pubblico. Tempo pieno, in sede, dal lunedì al venerdì.

All'annuncio rispondono **tre persone diverse**, che a schermo sono tre schede (oggetti, non personaggi: non parlano
e non hanno una storia):
- **Ilaria, 26 anni**: due stagioni alla reception di un campeggio;
- **Dario, 43 anni**: da tre anni al banco di una ferramenta;
- **Nadia, 35 anni**: cassa e reclami in un supermercato.

Tutte e tre incollano l'annuncio e scrivono all'IA la stessa cosa: «Devo rispondere a questo annuncio di lavoro. Mi
scrivi la mail di candidatura?».

**Momento di prova (scena 2).** A schermo le tre schede in alto e, sotto, **una** delle mail tornate (un'uscita A
vera). La domanda a chi guarda: «di chi è?». Il vuoto dura un secondo: tre linee tratteggiate vanno dalla mail alle
tre schede e nessuna si decide. Poi la risposta: si accendono tutte e tre. Non si può dire, perché nella mail non c'è
niente che appartenga a una persona sola; e non per sfortuna: lei aveva davanti la stessa richiesta tre volte. *Ipotesi
da verificare sulle uscite A:* dove dovrebbe esserci chi scrive, la mail ha segnaposto («[numero] anni», «[azienda]»)
oppure esperienze generiche buone per tutti. In tutti e due i casi la prova regge; cambia la frase che la commenta
(«ti lascia i buchi» o «li riempie con frasi che valgono per chiunque»).

**L'errore comune (scena 3).** Alla richiesta si aggiunge «Sii originale.». La mail cambia attacco (*ipotesi da
verificare sulle uscite B:* un'apertura a effetto sul caffè, e in più uscite la stessa idea). Stessa domanda, «di chi
è?», e stesse tre linee accese: è cambiato l'inizio della mail, non quello che lei sa di chi scrive. Qui si apre il
loop: una mail che si capisce di chi è si può avere, ma non chiedendole di essere originale. E la domanda che gira la
scena: dov'è il trucco?

**La mossa (scena 6).** Dalla richiesta esce «Sii originale.» ed entra una riga che sa solo Dario (dettaglio
inventato e dichiarato tale): «Da tre anni lavoro al banco di una ferramenta: al telefono rispondo io, una trentina di
chiamate al giorno, e i clienti arrabbiati li passano a me.» Torna una mail nuova (uscita C vera). Terza volta la
stessa domanda, «di chi è?»: due linee si spengono, ne resta una. Si chiude il loop: non è diventata creativa, ha
continuato un inizio diverso, e quell'inizio l'ha scritto lui. Poi la domanda passa a chi guarda: qual è la riga che
sai solo tu?

Potenziale e limite nella stessa vicenda. Potenziale: la prima mail è corretta, educata e pronta in pochi secondi, e
per tutte le mail in cui non serve distinguersi (spostare un appuntamento, chiedere un preventivo, confermare una
consegna) la strada battuta è quella giusta; con una riga vera lo stesso meccanismo scrive una mail che è di una
persona sola. Limite: senza fatti tuoi scrive la mail di chiunque, «sii originale» cambia l'attacco e non quello che
sa di te, e anche con la riga vera va riletta, perché intorno al tuo fatto può metterne altri che tuoi non sono.

## Messaggio centrale
«Generativa» non vuol dire creativa: l'IA continua quello che le scrivi, un pezzo alla volta, prendendo una delle
continuazioni più probabili, e se di te non le scrivi niente la candidatura che torna va bene per chiunque. Chiederle
«sii originale» cambia l'attacco; scriverle un dettaglio vero che sai solo tu cambia la mail.

## Struttura narrativa
**Schema di partenza:** @yousciences · r0020 — dimostrazione paradossale → "dov'è il trucco?" → definizione per
contrasto → catalogo quotidiano → rilettura di un'immagine mitica.

> Guardate [oggetto]. Se [azione A], fa [effetto A]. Se [azione B], fa [effetto B]. Dov'è il trucco? Si tratta di [nome + ricetta]. In [caso normale] [grandezza] è costante; qui invece dipende da [variabile]. Come anche [esempi quotidiani]. Quindi [conseguenza spettacolare]. Forse [rilettura di un'immagine nota].

Perché questo. È uno schema che **mostra prima di spiegare** («il cosa prima del perché», dice l'analisi): la
dimostrazione sta in testa, e questo mette il momento di prova nella scena 2 senza forzature. Porta l'errore comune
**prima** del meccanismo: così una sola spiegazione rende conto di tutte e due le mail deludenti, e la mossa discende
dal meccanismo invece di arrivare come consiglio. La «definizione per contrasto» è la forma esatta della tesi
(«generativa» non vuol dire X, vuol dire Y), la ricetta replicabile è la mossa, e la rilettura finale di una cosa
nota è la chiusura a battuta: qui la cosa nota è la parola «generativa», che chi guarda ha letto su ogni prodotto.
Dello schema si prende l'ossatura, non il registro: r0020 dura 92 s ed è, per la sua stessa analisi, «il reel meno
divulgativo» dell'account.

**Adattamento** (una riga per fase):
- [Guardate (oggetto)] → l'hook a filmato pone la domanda di chi guarda; il «guarda» apre la scena 2: tre persone, un
  annuncio, la stessa richiesta.
- [Se (azione A), fa (effetto A)] → se le chiedi la mail e basta, torna una mail che non si capisce di chi è (la
  prova: «di chi è?», tre linee accese).
- [Se (azione B), fa (effetto B)] → se aggiungi «sii originale», cambia l'attacco e le tre linee restano accese. Nello
  schema le due azioni danno effetti opposti; qui il paradosso è che due richieste diverse danno **lo stesso** effetto.
- [Dov'è il trucco?] → la domanda che gira il reel, detta così o quasi: le hai chiesto originalità e ti ha ridato la
  mail di tutti, dov'è il trucco?
- [Si tratta di (nome + ricetta)] → il nome è «generativa», e la ricetta è come scrive: continua quello che ha
  davanti, un pezzo alla volta, prendendo una delle continuazioni più probabili.
- [In (caso normale) la grandezza è costante; qui dipende da (variabile)] → una persona che scrive parte da quello che
  sa di sé, qualunque cosa le chiedi; lei parte **solo** da quello che c'è scritto prima. Tre richieste uguali, un solo
  inizio.
- [Come anche (esempi quotidiani)] → il lato buono: per spostare un appuntamento o chiedere un preventivo la strada
  più battuta è proprio quella che vuoi. Una coppia di esempi a voce, non un catalogo.
- [Quindi (conseguenza)] → la mossa: cambia l'inizio. Una riga vera che sai solo tu, e la terza prova: resta una
  linea sola.
- [Forse (rilettura di un'immagine nota)] → la rilettura della parola: generativa vuol dire che continua, e da dove
  si parte lo scrivi tu. Battuta, MESSAGGIO, CTA.

**Tecniche** (da «Tecniche condivise»):
- `contrasto`: la definizione per contrasto della scena 4 (da dove parte una persona, da dove parte lei) e, nella
  stessa carta, «Sii originale.» che esce e la riga vera che entra.
- `domanda-pivot`: «dov'è il trucco?» a fine scena 3, la frase-ponte che porta dalla dimostrazione al meccanismo.
  (Nell'analisi di r0020 il tag è `dov-e-il-trucco`, visto una volta sola; l'analisi stessa la descrive come
  domanda-pivot, che è la tecnica condivisa.)
- `ricetta-replicabile`: la mossa della scena 6 è una riga che chi guarda può scrivere domani, con il modo di
  controllare se ha funzionato (la prova «di chi è?» rifatta sulla propria mail).
- `battuta-finale`: la chiusura rilegge la parola «generativa» in una frase, e lì il reel finisce.

L'imperativo d'attacco dello schema («Guardate») resta come parola d'avvio della scena 2 («Guarda»), non come tecnica
a sé.

**Escluse:**
- `elenco`: il catalogo quotidiano non si legge a camera. A voce due esempi dentro una frase con il verbo; gli altri
  in caption.
- `immagine-mitica`: nessuna immagine mitica o religiosa; si rilegge una parola d'uso comune, non un miracolo.
- `conseguenza-spettacolare` (tag visto una volta): la mossa non promette un esito («ti chiamano»): promette solo una
  mail che si capisce di chi è.
- `coppia-di-opposti` (visto una volta): rovesciata, come scritto sopra; non si finge che B dia un effetto opposto ad A.
- La formulazione tecnica (nello schema: tau, dipendenza non lineare): qui sarebbero temperatura e top-p. Tagliata:
  resta «una delle più probabili», che dice la stessa cosa senza gergo.
- Firme di @yousciences (`intercalare-firma`, il «Capito?» in coda; `catena-di-conseguenze`): non si copiano. r0020
  non ha una CTA: qui ce n'è una sola, come chiede `docs/linguaggio-reel.md` §8.
- Lunghezza: lo schema è da 92 s e nove mosse; qui sette scene e obiettivo ≤ 75 s. La prima a perdere una frase è la
  scena 5 (il lato buono si dice in una frase sola), poi il conto della scena 3.

## Cosa impara chi guarda
1. **Un modo nuovo di leggere.** L'IA non scrive «su di te»: continua quello che ha davanti. Se nella richiesta di te
   non c'è niente, nella mail non può esserci niente di tuo. Non è un difetto del modello, è il suo modo di
   funzionare, e per le mail in cui non devi distinguerti è un vantaggio.
2. **La mossa.** Prima di chiedere la mail, scrivi nella richiesta una riga vera che sai solo tu: un lavoro fatto, un
   numero tuo, un dettaglio di com'è la tua giornata. Un fatto, non un aggettivo (non «sono paziente e motivato», ma
   «i clienti arrabbiati li passano a me»). Al posto di «sii originale», non in aggiunta.
3. **Il criterio** (*proposta*). Copri la firma e rifai la prova: si capisce che l'hai scritta tu e non un altro che ha
   risposto allo stesso annuncio? Se al tuo posto potrebbe esserci chiunque, manca ancora un fatto tuo. Poi il
   controllo inverso: ogni fatto che c'è nella mail dev'essere tuo davvero, perché quello che non le hai dato può
   averlo messo lei.

## Pilastro
Come funziona davvero (cosa vuol dire «generare»: continuare quello che c'è prima, un pezzo alla volta, con una delle
continuazioni più probabili). In filigrana **cosa può fare per te**: una riga vera nella richiesta sposta tutta la
mail.

## Perché ora
*Proposta:*
- **Per chi guarda.** «Generativa» sta nel nome di quasi ogni prodotto che usa, e la traduzione spontanea è
  «creativa»: da lì viene la mossa sbagliata, chiedere originalità invece di dare informazioni. La candidatura è il
  caso in cui l'equivoco costa di più, perché è un testo che serve proprio a distinguerti. Nessun dato su quanti
  candidati usano l'IA né su cosa ne pensa chi seleziona: non ho una fonte, e il reel non lo dice.
- **Per il canale.** Una mossa che si fa domani su un gesto che molti fanno già, con una prova che chi guarda può
  rifare sulla propria mail. E il destinatario dell'invio è ovvio.
- **Non invecchia.** Il criterio «si capisce che l'hai scritta tu?» vale con qualunque modello. Invecchiano solo i
  conti sulle uscite, che vanno in caption con modello e data.

## Fonte
Non si applica (fonte: testo).

## Angoli scartati
- **«Finisci tu la frase»** (la mail si ferma su una formula di rito e chi guarda la completa). È la prova più
  diretta del «probabile», ma mostra solo che le formule sono prevedibili; non dice perché la mail non parla di te né
  perché la riga vera funziona. La prova «di chi è?» tiene insieme tesi, errore e mossa con lo stesso gesto, tre volte.
- **«Senza fatti tuoi, l'IA te li inventa»** (la mail che attribuisce a chi scrive esperienze mai dichiarate). Forte
  e utile, ma è un secondo concetto (il plausibile al posto del vero): qui resta nel criterio e in caption. Se le
  uscite A lo mostrano in modo netto, merita un reel suo.
- **«Chi seleziona riconosce le mail scritte con l'IA».** Senza una fonte è una promessa che il reel non può
  mantenere, e sposta il tema dal meccanismo al giudizio degli altri.
- **Il bingo delle formule** (chi guarda scommette quali frasi fatte ci saranno, poi si accendono). Divertente, ma è
  una scommessa con un conto, e resta sulla superficie (le parole) invece che sul punto (cosa sa di te).
- **Più mosse insieme** (dettaglio, parole vietate, farsi dare cinque versioni): il reel ne ha una. Le altre, con i
  loro limiti, in caption.
- **Opus contro Sonnet**: se le uscite mostrano esiti diversi, è una riga di caption, non un tema.

## Note per il reel
**Hook candidato** (problema di chi guarda, in coppia con l'immagine; a schermo nessun titolo, il presentatore nel
riquadro sopra la clip):
- Frase: «Se la candidatura te la scrive l'IA, e la chiede anche quello seduto accanto a te, quanto si somigliano?»
  (19 parole)
- Clip dietro: **una fila di candidati seduti in una sala d'attesa prima di un colloquio**, uno accanto all'altro
  sulle sedie lungo il muro, vestiti in modo simile, cartellina sulle ginocchia o telefono in mano; qualcuno guarda
  di lato il vicino. Inquadratura frontale o di tre quarti a figura intera, camera ferma o in lenta carrellata lungo
  la fila; luce da ufficio. Nessuno viene chiamato, nessuno viene scartato: è attesa, non giudizio. Query per Pexels:
  `job candidates waiting room`, `people waiting for interview sitting in a row`, `applicants hallway chairs job interview`.
- Alternativa: «La candidatura che ti scrive l'IA è scritta bene. Ma si capisce che l'hai mandata tu?» (16 parole),
  stessa clip. La prima è la consigliata: «quello seduto accanto a te» è già nell'immagine, e la domanda trova
  risposta nella scena 2.
- Cautela per la clip e per la frase: il «se… e la chiede anche» è un'ipotesi, non un fatto. Il reel non afferma che
  gli altri candidati usano l'IA.
- TITOLO della copertina (la tesi, vive solo in griglia): «Generativa non vuol dire creativa». Alternativa: «La
  candidatura che va bene per chiunque».

**Percorso** (*proposta*, sette scene; la VOCE la scrive lo sceneggiatore):
1. **Hook a filmato**: la domanda.
2. **Animata · la dimostrazione e la prova.** «Guarda»: tre schede, un annuncio, la stessa richiesta; una mail vera;
   «di chi è?»; il vuoto di un secondo; tutte e tre le linee accese. La frase che dice a chi guarda cosa ha appena
   fatto: non hai saputo scegliere, e non è colpa tua, nella mail non c'è niente da cui capirlo.
3. **Animata · l'errore comune.** Entra «Sii originale.»; la mail cambia attacco (zoom sull'attacco, poi si torna
   alla mail intera); stessa prova, stesse tre linee. Il conto vero («io l'ho chiesta dieci volte, e N cominciano
   dal caffè»: solo se le uscite B lo danno). Si apre il loop e arriva la domanda-pivot: dov'è il trucco?
4. **Animata · il meccanismo.** La definizione per contrasto, e il bivio: la frase avanza, a ogni bivio strade grosse
   e strade sottili, ne prende una delle grosse, non sempre la stessa. Da dove parte: solo da quello che c'è scritto
   prima.
5. **A filmato (candidata) · il lato buono.** Per la mail che sposta un appuntamento o chiede un preventivo la strada
   battuta è quella giusta, e in dieci secondi è fatta. Per una candidatura no, perché serve a distinguerti.
6. **Animata · la mossa e la terza prova.** Esce «Sii originale.», entra la riga della ferramenta; la mail nuova; «di
   chi è?»; due linee si spengono. Si chiude il loop: è ancora la continuazione probabile, ma di un altro inizio, e
   l'inizio l'ha scritto lui. Poi al «tu»: qual è la riga che sai solo tu?
7. **Chiusura**: la rilettura della parola, la battuta, il MESSAGGIO, la CTA.

Obiettivo ≤ 75 s: con sette scene sono circa 190 parole di VOCE (stima del repo: parole ÷ 2,8 + 0,8 s a scena). La
scena 4 è la più densa: non più di quattro beat, e una sola idea per beat.

**Scene a filmato oltre l'hook** (animazione e filmato si alternano, mai due filmati di fila, mai più di metà):
- **Scena 5, consigliata.** Non ha niente da disegnare (è un'esperienza, non un meccanismo) e cade a due terzi del
  reel, dove l'attenzione cala. Immagine: **una persona in piedi, al banco di un bar o alla fermata, che scrive una
  risposta veloce sul telefono con il pollice e lo rimette in tasca**, piano medio o primo piano sulle mani. Query:
  `person typing on phone standing coffee bar`, `replying email smartphone close up hands`, `commuter texting phone
  bus stop`. Con hook e scena 5 i filmati sono 2 su 7, mai adiacenti.
- **Seconda candidata, solo se lo sceneggiatore sale a otto scene:** una scena breve (5-6 s) fra la 3 e la 4 che
  porta da sola la domanda-pivot. Immagine: **una persona che legge un foglio stampato, aggrotta la fronte e lo gira
  per guardare il retro**, come a cercare il trucco. Query: `person turning paper over confused`, `reading letter
  puzzled office`. Costa 0,8 s di stima e qualche parola alle altre scene: io resto a sette.

**Filo visivo** (tre oggetti che tornano in tutte le scene animate):
- **le tre schede** (Ilaria, Dario, Nadia: nome, età, una riga) con le **linee** che le legano alla mail
  (`Corrispondenza`). È l'oggetto del loop: tre linee accese (scene 2 e 3), attenuate mentre si spiega (scena 4), una
  sola alla fine (scena 6). Nella chiusura resta la scheda di Dario, o una scheda vuota con «tu».
- **il foglio «prima | dopo»**: un solo foglio con una riga di confine. Sopra, quello che c'è prima (la richiesta, con
  l'annuncio agganciato e attenuato); sotto, quello che scrive lei (la mail). Il testo attraversa il confine: la mail
  è la continuazione della richiesta, e si vede. La parte sopra cambia tre volte, e ogni stato è **esattamente** una
  delle richieste qui sotto (A, poi B, poi C).
- **il bivio**: la frase che avanza lungo una strada che si dirama, con rami di spessore diverso. Le etichette dei
  rami sono varianti **davvero comparse** nello stesso punto in uscite diverse (per esempio le formule di saluto o la
  prima frase), e lo spessore è **il conto vero** di quante uscite su dieci hanno preso quel ramo, con le sigle. Se le
  uscite non offrono un punto pulito, il bivio resta con la dicitura a schermo «esempio: spessori inventati». In
  scena 6 torna per un beat: con la riga della ferramenta sopra il confine, il ramo grosso è un altro.

Cambi grandi candidati (uno per scena): le tre linee che si accendono insieme con «TUTTI E TRE» a punch (scena 2);
zoom sull'attacco della mail B e ritorno alla mail intera (scena 3); zoom dentro il bivio (scena 4); due linee che si
spengono e «FERRAMENTA» a punch, nello stile di «TUTTI E TRE» (scena 6); riquadro del presentatore grande sulla
battuta, con la parola «GENERATIVA» grande (scena 7). Due scene di fila non hanno la stessa composizione: schede+mail
(2), mail in primo piano (3), bivio (4), filmato (5), foglio prima|dopo + schede (6).

**Testi del modello: richieste da generare (T0b).** Nel reel compaiono mail attribuite a un modello: vanno generate
davvero prima della sceneggiatura, 5 con Opus e 5 con Sonnet per richiesta (sigle A1-A10, B1-B10, C1-C10; 1-5 Opus,
6-10 Sonnet), da una cartella neutra e con un prompt di sistema neutro. Le tre richieste sono identiche salvo
l'aggiunta finale; nella base non compare la parola «originale». L'annuncio, fisso, è questo:

> Torrefazione Tostavento (Pesaro): assistenza clienti. Tostiamo caffè e lo spediamo in tutta Italia dal nostro negozio online. Cerchiamo una persona che risponda a mail e telefonate dei clienti e segua ordini, resi e abbonamenti. Serve almeno un anno di lavoro a contatto con il pubblico. Tempo pieno, in sede, dal lunedì al venerdì.

Una richiesta per riga, pronta per `claude -p`:

- **A · base:** `Devo rispondere a questo annuncio di lavoro. Mi scrivi la mail di candidatura? «Torrefazione Tostavento (Pesaro): assistenza clienti. Tostiamo caffè e lo spediamo in tutta Italia dal nostro negozio online. Cerchiamo una persona che risponda a mail e telefonate dei clienti e segua ordini, resi e abbonamenti. Serve almeno un anno di lavoro a contatto con il pubblico. Tempo pieno, in sede, dal lunedì al venerdì.»`
- **B · errore comune (+ «Sii originale.»):** `Devo rispondere a questo annuncio di lavoro. Mi scrivi la mail di candidatura? «Torrefazione Tostavento (Pesaro): assistenza clienti. Tostiamo caffè e lo spediamo in tutta Italia dal nostro negozio online. Cerchiamo una persona che risponda a mail e telefonate dei clienti e segua ordini, resi e abbonamenti. Serve almeno un anno di lavoro a contatto con il pubblico. Tempo pieno, in sede, dal lunedì al venerdì.» Sii originale.`
- **C · la mossa (+ un dettaglio vero):** `Devo rispondere a questo annuncio di lavoro. Mi scrivi la mail di candidatura? «Torrefazione Tostavento (Pesaro): assistenza clienti. Tostiamo caffè e lo spediamo in tutta Italia dal nostro negozio online. Cerchiamo una persona che risponda a mail e telefonate dei clienti e segua ordini, resi e abbonamenti. Serve almeno un anno di lavoro a contatto con il pubblico. Tempo pieno, in sede, dal lunedì al venerdì.» Da tre anni lavoro al banco di una ferramenta: al telefono rispondo io, una trentina di chiamate al giorno, e i clienti arrabbiati li passano a me.`

Note per chi genera:
- Il dettaglio di C è **inventato e dichiarato tale** (a schermo o in caption: «candidato e dettaglio inventati»). Il
  presentatore può riscriverlo a modo suo prima di T0b: in quel caso cambia solo la riga finale di C.
- Nelle richieste non c'è nessun nome di persona, ed è voluto: è quello che fa chi chiede di fretta. I nomi delle
  schede (Ilaria, Dario, Nadia) stanno solo a schermo: se si cambiano non si rigenera niente.
- **Nessun dato personale vero**: `claude -p` può passare al modello nome ed email dell'account, che finiscono in
  firma. Nel file delle uscite vanno sostituiti con «Nome Cognome» e «nome.cognome@email.it» (e così ogni ente o
  ateneo riconoscibile), dichiarando il ritocco; a schermo non vanno mai.
- A schermo la parte «prima» del foglio mostra la prima frase della richiesta e la riga aggiunta; l'annuncio sta
  agganciato sotto, con le stesse parole.

**Cosa cercare nelle uscite** (ipotesi da verificare, non risultati: ogni conto con la sigla di ciascuna uscita,
contando anche varianti e plurali):
- **A.** Dove dovrebbe esserci chi scrive: segnaposto fra parentesi («[numero] anni», «[azienda]»), oppure esperienze
  generiche non dichiarate nella richiesta («ho maturato esperienza a contatto con il pubblico»)? Quante uscite fanno
  l'una e quante l'altra cosa (ipotesi: i due modelli si comportano in modo diverso). C'è in qualche uscita A un
  fatto che appartiene a una sola delle tre schede? (Ipotesi: no. Se sì, quell'uscita non si usa per la prova.)
  Quali formule di rito tornano e in quante uscite. Un punto in cui le uscite si diramano in poche varianti contabili
  (il saluto, la prima frase): è il materiale del bivio. Uscite che, prima o dopo la mail, **chiedono i tuoi dati** o
  invitano a completarla: se ci sono, è la mossa suggerita dal modello stesso, da dire in caption e forse in una
  frase della scena 6.
- **B.** L'attacco cambia in modo visibile? Su che cosa (ipotesi: un'immagine sul caffè, la tostatura, l'aroma)? In
  quante uscite torna la stessa idea d'attacco. Sotto l'attacco, restano segnaposto o esperienze generiche come in A?
  C'è in qualche uscita B un fatto che distingue una delle tre schede? (Ipotesi: no.) Se B non cambia in modo
  visibile, la scena 3 si riscrive su «cambia poco»; se B distingue davvero una persona, l'ipotesi è smentita e la
  scena si riscrive sul risultato vero: il reel non lo forza.
- **C.** La ferramenta, il telefono, i clienti arrabbiati entrano nella mail, e in che punto (ipotesi: diventano
  l'argomento del secondo capoverso)? La prova regge, cioè la mail indica una scheda sola? Resta la cornice di rito
  uguale ad A (saluto, chiusa)? Se sì è il limite della mossa, da dire in caption. **Il modello aggiunge o gonfia
  fatti** («ho gestito con successo centinaia di reclami», anni o numeri cambiati)? Se sì è il secondo controllo del
  criterio, e va detto almeno in caption.

**Numeri.** In questa idea nessuno. In VOCE al massimo due, tutti conti sulle uscite, ricontati con le sigle; modello
e data in caption. Gli spessori del bivio sono conti veri oppure «esempio: spessori inventati» a schermo, mai una via
di mezzo. «Tre anni», «una trentina di chiamate», età e mestieri delle schede sono **esempio dichiarato**.

**MESSAGGIO candidato** (≤ 12 parole):
- «Lei continua quello che trova. Tu scrivile qualcosa che sai solo tu.» (12)
- Alternative: «Se non gliel'hai scritto, non lo sa. Scrivilo.» (8); «L'originale della tua mail sei tu. Mettiti
  nella richiesta.» (9).

**Chiusura a battuta** (*proposta*, ≤ 18 parole di VOCE, la più forte per ultima; sceglie lo sceneggiatore): la
rilettura della parola, ancorata alla vicenda. Due direzioni: «Generativa vuol dire che continua. Da dove si parte,
glielo scrivi tu.» (12), oppure sull'oggetto: «La ferramenta non se l'è inventata lei. Ce l'ha messa chi sta al
banco da tre anni.» (17). Niente riassunto, niente elenco.

**CTA** (una): «Mandalo a chi sta per rispondere a un annuncio» (invio, destinatario ovvio, nessun claim).

**Claim per il revisore** (con le formule prudenti)
- «Un pezzo alla volta»: sono token, non parole. «Un pezzo» è più vicino al vero di «una parola»; se lo sceneggiatore
  preferisce «una parola alla volta» è una semplificazione da dichiarare in caption.
- «Prende **una delle** continuazioni più probabili»: mai «la più probabile», mai «sempre». Il modello campiona, e
  per questo dieci richieste uguali danno dieci mail diverse nelle parole.
- «Di te sa solo quello che le scrivi»: vero per il contesto, ma il contesto può contenere più della richiesta (la
  memoria o il profilo in certe app; qui la CLI passa nome ed email dell'account). Formula prudente: «**se non
  gliel'hai scritto, non lo sa**». In caption: con la memoria attiva l'app può sapere altro di te.
- «Tre persone, la stessa richiesta»: le tre persone sono inventate e nessuna ha mandato niente. Quello che è vero, e
  si può dire, è che la stessa richiesta è stata fatta dieci volte e che nella richiesta non c'è niente su chi
  scrive. La VOCE non dice «l'ha scritta uno di questi tre»: dice «tutti e tre le scrivono la stessa cosa, e questa è
  la mail che torna».
- «Non si capisce di chi è» / «va bene per chiunque»: si sostiene solo sulle uscite A e B, con le sigle. Mai
  «identiche»: «intercambiabili», «si somigliano».
- «Sii originale» è **insufficiente, non inutile**: cambia l'attacco. La VOCE dice «non è chiedendoglielo che la mail
  diventa tua», non «chiederlo non serve a niente». L'attacco di B non si chiama «originale» né «creativo».
- La terza prova non deve suonare come «il dettaglio ha reso l'IA creativa»: è ancora una continuazione probabile, di
  un altro inizio.
- Il bivio: le frequenze su dieci uscite di **due modelli diversi** non sono le probabilità del modello. Formula: «su
  dieci volte, N hanno preso questa strada»; mai percentuali, mai «la probabilità è». Meglio ancora contare per
  modello (5 e 5) e scegliere un punto dove i due concordano.
- «Generativa vuol dire che continua»: parafrasi onesta di «modello che produce campioni da una distribuzione sui
  testi», ma è una parafrasi. Non si dice che l'IA «non è creativa» (Doshi & Hauser): si dice che il nome non lo
  promette.
- Non si afferma che gli altri candidati usano l'IA, né che chi seleziona se ne accorge, né che la mail con il
  dettaglio ottiene più risposte: nessuna fonte. L'hook è al condizionale («se… e la chiede anche…»).
- Limite di buon senso della mossa, in caption: il dettaglio dev'essere vero e tuo, senza dati riservati del datore
  di lavoro attuale; la mail si rilegge, e i fatti che non sono tuoi si tolgono.
- I riferimenti del «Concetto» (Kirk et al. 2024; Zhang et al. 2025; Jiang et al. 2025; Doshi & Hauser 2024) sono a
  memoria: da verificare prima di metterli in caption. Nessuno entra in VOCE.
- **Omonimia.** «Torrefazione Tostavento» è un nome inventato per questo reel; due ricerche web del 2026-09-20
  («Torrefazione Tostavento», «Tostavento caffè azienda») non hanno trovato aziende con questo nome (il più vicino è
  «Tostini Caffè», che non gli somiglia abbastanza da confondersi). **Va ricontrollato dal revisore** (ricerca web,
  registro imprese, marchi) **prima di T0b**: il nome sta nell'annuncio e quindi nelle richieste, e se cambia le
  uscite si rigenerano. Pesaro è una città vera scelta a caso: nessun riferimento a torrefazioni reali della zona.
- Le uscite vengono dalla CLI con un prompt di sistema neutro, non da un'app: non si dice «in chat».

**Domande per il presentatore** (con `--tutto` nessuno risponde prima della fine: per ognuna c'è l'opzione che
consiglio, ed è quella scritta nell'idea)
1. *Le tre schede hanno un nome o restano «candidato 1, 2, 3»?* Consiglio i nomi propri senza cognome: scaldano la
   scena, non sono personaggi (non parlano) e non toccano le richieste.
2. *Il dettaglio della ferramenta va bene o lo riscrivi tu?* Consiglio di tenerlo: è un fatto di vita e non un
   indicatore da curriculum, e «li passano a me» è la riga che resta in testa. Se lo riscrivi, va fatto prima di T0b.
3. *Il secondo filmato è la scena 5?* Consiglio di sì, e di restare a sette scene.
4. *Spessori del bivio veri o inventati?* Consiglio veri, se le uscite danno un punto pulito; altrimenti dichiarati
   inventati.

**Per lo sceneggiatore**
- Leggi `~/Projects/reelkit/analisi/r0020.md` e `trascrizioni/r0020.txt` per l'ordine delle mosse («il cosa prima del
  perché», «Dov'è il trucco?», il «Forse» finale); il passo del parlato prendilo dalle trascrizioni che indica
  `docs/stile-parlato.md`, non da r0020 (gergo, frasi da manuale).
- La domanda «di chi è?» torna tre volte con le stesse parole: è la parola chiave che si ripete, e va detta uguale.
- In caption: la dichiarazione dei testi (modello, data, tagli e ritocchi nostri, «annuncio, azienda, persone e
  dettaglio inventati»), il criterio in due controlli, il lato buono con gli altri esempi, il limite dei fatti
  aggiunti, la nota sulla memoria delle app, le altre mosse con i loro limiti.

**Note interne (per non ripetersi; niente di questo entra nel reel)**
- Ogni reel è a sé stante: nessun richiamo ad altri reel, nessuna azienda o persona che prosegue. Qui non compaiono
  «Acme Arredi», «Quattroassi Arredi», Giulia, Carla, Marco.
- La corsa archiviata dello stesso slug (`contenuti/archivio/generativa-probabile/`) aveva speso: lo schema r0037, il
  cursore che si ferma su una frase aperta («finisci tu la frase») due volte, la colonna delle candidate
  (`Classifica`), l'annuncio di un addetto marketing in un negozio di arredi, la newsletter «da 300 a 2.100», la
  chiusura «poteva firmarla chiunque». Qui: schema r0020, prova «di chi è?» tre volte, schede + foglio prima|dopo +
  bivio, torrefazione e assistenza clienti, la ferramenta. L'idea della mail «di chiunque» lì era la battuta finale;
  qui è il dispositivo di tutto il reel, e la battuta finale è un'altra (la rilettura della parola).
- Da quelle uscite (30 mail, 2026-09-16) ho preso **solo ipotesi**: Opus lasciava segnaposto e invitava a completare,
  Sonnet tendeva a esperienze generiche, «Sii originale.» spostava l'attacco sul prodotto dell'azienda (il divano),
  e la CLI metteva in firma nome ed email dell'account. Nessuno di quei conti vale qui: annuncio e richieste sono
  nuovi.
- `contenuti/idee/2026-09-19-scrivere-con-ia.md` (in lavorazione) usa lo schema r0040, una mail di lavoro già scritta
  e fatta riscrivere, la scommessa su un numero, il contatore delle frasi, una carta «richiesta» che cambia tre
  volte, l'hook con una persona perplessa davanti al portatile. Qui: altro schema, nessun contatore, la prova è una
  scelta fra tre schede, la richiesta non è una carta a sé ma la metà alta di un foglio, l'hook è una sala d'attesa.
  Resta in comune, per natura, che la richiesta cambia tre volte (A, B, C).
- Formule già passate da un revisore in lavori precedenti e riusate qui da zero: «una delle più probabili», mai «la
  più probabile»; «se non gliel'hai detto»; «insufficiente, non inutile»; «non si dice in chat».
