# Uscite vere · generativa-probabile · 2026-09-20

Generate il 2026-09-20 dalla tappa T0b di `/pipeline` con `claude -p` (2.1.278 (Claude Code)), da una cartella neutra:
`--model opus|sonnet --system-prompt "Sei un assistente che scrive testi su richiesta." --tools "" --no-session-persistence`.
Sigle: 1-5 Opus (claude-opus-5), 6-10 Sonnet (claude-sonnet-5). Azienda, annuncio e dettaglio della ferramenta sono
inventati; l'annuncio è identico nelle tre richieste, cambia solo la coda. Testi riportati così come sono usciti, con un
solo ritocco: `claude -p` passa al modello nome ed email dell'account anche da una cartella neutra, e il modello li ha
usati in firma, nell'oggetto e in «mi chiamo …» in 23 uscite su 30 (53 sostituzioni: «Nome Cognome»,
«nome.cognome@email.it», dominio dell'ateneo → «ateneo.it»). **Attenzione per il reel:** quel nome non viene dalla
richiesta ma dalla CLI; la tesi «se non gliel'hai scritto, non lo sa» si giudica sul resto della mail (esperienze,
motivazioni), non sulla firma. A schermo non vanno mai i dati veri. In B3 un'inferenza sulla città dell'account è sostituita da «[di un'altra città]».
**Secondo artefatto dello strumento (trovato dal revisore, 2026-09-20):** `--tools ""` non spegne i connettori
dell'account: A2 e A5 dicono di aver provato ad aprire il Drive, A4 A7 A10 B1 B2 B4 C7 offrono la bozza in Gmail, e nove
uscite sanno che l'indirizzo è universitario. Le uscite restano vere, ma la caption deve dire che lo strumento passava
nome, email e connettori; per un conto pulito servirebbe rigenerare senza identità dell'account. Uscite ritoccate: A1 A2 A3 A6 A7 A9 B1 B2 B3 B4 B6 B7 B8 B9 B10 C1 C2 C4 C5 C6 C7 C9 C10.

Prima lettura grezza del coordinatore (conti automatici e attacchi letti a occhio: **da ricontare a mano, uscita per
uscita, prima di portare un numero o un giudizio nel reel**):
- A: **tutte e dieci lasciano segnaposto fra parentesi quadre** (da 4 a 8 per uscita, contando anche `[telefono]`):
  esperienze, anni, ruolo e azienda precedente sono buchi da riempire, non fatti inventati. È il caso previsto
  dall'idea: la mail «vale per chiunque» perché i fatti di chi scrive mancano, e il commento onesto è più vicino a «ti
  lascia i buchi» che a «te li inventa». Gli attacchi sono quasi tutti varianti di «(vi) scrivo per candidarmi alla
  posizione di assistenza clienti» o «mi chiamo … e desidero candidarmi»: da guardare se c'è un punto pulito per il bivio.
- B: i segnaposto restano (da 5 a 11). In circa metà delle uscite cambia l'attacco e va sul caffè o sul mestiere (B4,
  B6, B7, B9 «ho letto il vostro annuncio con il caffè accanto»); nelle altre (B1, B2, B3, B5, B8, B10) l'attacco è
  ancora quello di A. Da verificare che nessuna B contenga un fatto che distingua una delle tre schede.
- C: **tutte e dieci nominano la ferramenta**, e i segnaposto scendono a 1-4 (spesso solo telefono e nome). Da
  controllare a mano se il modello gonfia i fatti (tre anni, una trentina di chiamate, i clienti arrabbiati) o ne
  aggiunge di suoi: se succede è materiale per la caption e per il revisore.
- Il nome in firma e in «mi chiamo Nome Cognome» viene dalla CLI, non dalla richiesta (vedi sopra): non si usa come
  prova né pro né contro la tesi, e le uscite che aprono con «mi chiamo …» a schermo vanno tagliate dopo quella frase
  o evitate.

## A · base

**Richiesta:**

> Devo rispondere a questo annuncio di lavoro. Mi scrivi la mail di candidatura? «Torrefazione Tostavento (Pesaro): assistenza clienti. Tostiamo caffè e lo spediamo in tutta Italia dal nostro negozio online. Cerchiamo una persona che risponda a mail e telefonate dei clienti e segua ordini, resi e abbonamenti. Serve almeno un anno di lavoro a contatto con il pubblico. Tempo pieno, in sede, dal lunedì al venerdì.»

### A1 · Opus (opus)

Ecco una bozza. Ho lasciato tra parentesi quadre i punti che devi riempire tu, perché non conosco il tuo percorso.

---

**Oggetto:** Candidatura per assistenza clienti — [Nome Cognome]

Buongiorno,

ho letto il vostro annuncio per una persona da inserire nel servizio clienti e vorrei propormi.

Negli ultimi [X] anni ho lavorato a contatto con il pubblico presso [azienda/negozio], dove mi occupavo di [rispondere alle richieste dei clienti allo sportello e al telefono / gestire ordini e resi / ecc.]. È un lavoro che mi ha insegnato soprattutto due cose: ascoltare bene prima di rispondere e non lasciare mai una richiesta in sospeso senza dare almeno un aggiornamento. Mi è capitato spesso di gestire reclami e situazioni poco piacevoli, e ho imparato che la calma e la chiarezza risolvono quasi tutto.

Mi interessa in particolare il fatto che si tratti di un prodotto vostro, tostato da voi: credo sia più facile assistere bene un cliente quando si conosce davvero quello che si vende, e sarei contento di impararlo.

Sono disponibile a tempo pieno in sede a Pesaro e [posso iniziare da / sono disponibile con preavviso di …].

In allegato trovate il mio curriculum. Resto a disposizione per un colloquio.

Cordiali saluti,
[Nome Cognome]
[Telefono] — nome.cognome@email.it

---

Due note pratiche:

- **Nell'annuncio non c'è un indirizzo mail.** Controlla sul sito della torrefazione o nella pagina dove hai trovato l'inserzione: spesso c'è un riferimento tipo `lavoraconnoi@` o un modulo da compilare.
- **Se hai un indirizzo personale**, userei quello invece di quello universitario — per una candidatura fuori dall'ambito accademico è più coerente.

Se mi dici che lavoro hai fatto finora e da quando sei disponibile, te la riscrivo già completa senza parentesi.

### A2 · Opus (opus)

Non ho accesso al tuo Drive (il permesso non è stato concesso), quindi ho lasciato tra parentesi quadre i punti che devi riempire tu con la tua esperienza vera.

**Oggetto:** Candidatura assistenza clienti — Nome Cognome

Buongiorno,

scrivo per candidarmi alla posizione di assistenza clienti nel vostro negozio online.

Ho [numero] anni di lavoro a contatto con il pubblico: [es. due anni al banco di una libreria a Pesaro, dove gestivo ordini su richiesta e clienti abituali]. Mi sono occupato di [es. risposte a mail e telefonate, gestione dei resi, reclami]. È un lavoro in cui ho imparato che la maggior parte dei problemi si risolve rispondendo in fretta e dicendo le cose come stanno, anche quando la risposta non è quella che il cliente spera.

Gli abbonamenti e la spedizione di un prodotto fresco come il caffè tostato mi sembrano la parte più delicata: ritardi e scorte sbagliate si sentono subito. [Se hai esperienza con spedizioni, gestionali, e-commerce o software tipo Shopify/Zendesk, aggiungila qui in una riga.]

Sono di [città] e la sede a Pesaro non è un problema, così come l'orario pieno dal lunedì al venerdì.

In allegato il mio curriculum. Resto a disposizione per un colloquio.

Cordiali saluti,
Nome Cognome
[telefono] — nome.cognome@email.it

Due avvertenze pratiche:

- Se l'indirizzo universitario è l'unico che hai, va bene, ma un indirizzo personale dà meno l'impressione di una candidatura "di passaggio" tra un esame e l'altro.
- Il requisito dell'anno a contatto col pubblico è l'unico vero filtro dell'annuncio: se ce l'hai, mettilo nella prima riga del corpo; se non ce l'hai, meglio dirlo apertamente invece di girarci intorno.

Se mi dici cosa hai fatto davvero (dove, quanto tempo, che mansioni), te la riscrivo senza parentesi.

### A3 · Opus (opus)

Ecco una bozza. Ho lasciato tra parentesi quadre i punti che solo tu puoi riempire.

**Oggetto:** Candidatura – Assistenza clienti

Gentile team di Tostavento,

scrivo in riferimento all'annuncio per la posizione di addetto all'assistenza clienti.

Ho [numero] anni di esperienza a contatto con il pubblico: [es. "due anni al banco di una caffetteria a Pesaro, dove gestivo anche le prenotazioni telefoniche e i reclami" / "un anno e mezzo come addetto al customer care per un negozio online di articoli sportivi, con gestione di mail, resi e solleciti"]. In quel ruolo mi sono occupato soprattutto di [rispondere a richieste via mail e telefono / seguire gli ordini dalla conferma alla consegna / gestire resi e rimborsi], imparando a tenere insieme tempi di risposta rapidi e un tono che mettesse il cliente a suo agio anche quando qualcosa era andato storto.

Della vostra offerta mi interessa in particolare la parte sugli abbonamenti: è un rapporto che continua nel tempo e richiede di conoscere i clienti abituali, le loro preferenze e i loro tempi. Mi sembra il tipo di lavoro in cui la cura dei dettagli si vede.

[Se hai un interesse reale per il caffè, una riga qui: es. "Bevo caffè in moka e negli ultimi anni mi sono avvicinato alle tostature chiare; ho seguito un corso base di degustazione." Se non ce l'hai, togli questo paragrafo: meglio niente che una frase costruita.]

Abito a [città] e la sede di Pesaro è facilmente raggiungibile per me; sono disponibile per un impiego a tempo pieno dal lunedì al venerdì, a partire da [data].

In allegato trovate il mio curriculum. Resto a disposizione per un colloquio.

Cordiali saluti,
Nome Cognome
[telefono]
[email]

---

Due cose su cui posso migliorare la bozza, se mi dai gli elementi:

1. **La tua esperienza concreta** — dove hai lavorato col pubblico e cosa facevi esattamente. Il secondo paragrafo è la parte che decide se ti chiamano, e ora è generico.
2. **Il caffè** — se è un interesse vero, vale la pena svilupparlo; se no, lascialo perdere, una torrefazione piccola riconosce subito l'entusiasmo di facciata.

Dimmi pure e te la riscrivo su misura.

### A4 · Opus (opus)

Ecco una bozza. Ho lasciato tra parentesi quadre le cose che solo tu puoi riempire.

**Oggetto:** Candidatura per assistenza clienti — [Nome Cognome]

Buongiorno,

scrivo in risposta al vostro annuncio per la posizione di assistenza clienti presso Torrefazione Tostavento.

Ho [numero] anni di esperienza a contatto con il pubblico: [es. "per due anni ho lavorato al banco di una libreria indipendente a Pesaro, dove seguivo anche gli ordini su richiesta dei clienti e la gestione dei resi"]. È un lavoro che mi ha insegnato ad ascoltare prima di rispondere, a gestire con calma le situazioni in cui qualcosa è andato storto e a tenere in ordine pratiche che si accumulano — ordini da rintracciare, richieste in sospeso, clienti a cui va ridata una risposta entro la giornata.

Mi interessa in particolare il vostro contesto: un prodotto artigianale venduto online richiede un rapporto con il cliente diverso da quello di un e-commerce qualsiasi, e mi piacerebbe occuparmene. [Se vero e se ti va, una riga personale: "Bevo il vostro caffè da tempo" oppure "Mi sto avvicinando al mondo della torrefazione e vorrei conoscerlo dall'interno".]

Sono [residente a Pesaro / disponibile a trasferirmi] e disponibile a tempo pieno in sede dal lunedì al venerdì, con inizio [data].

In allegato trovate il mio curriculum. Resto a disposizione per un colloquio.

Cordiali saluti,
[Nome Cognome]
[Telefono] · [email]

---

Due note:
- Nell'annuncio non c'è l'indirizzo a cui scrivere — se lo hai, dimmelo e ti preparo la mail già pronta come bozza in Gmail.
- Se mi racconti in due righe che lavoro hai fatto finora, riscrivo il secondo paragrafo su misura invece di lasciartelo da compilare: è la parte che pesa di più in una candidatura del genere.

### A5 · Opus (opus)

Non ho accesso al tuo Drive (permesso non concesso), quindi ho scritto la mail con dei segnaposto tra parentesi quadre nei punti che solo tu puoi riempire.

**Oggetto:** Candidatura per assistenza clienti — [Nome Cognome]

---

Buongiorno,

scrivo in merito all'annuncio per la posizione di addetto all'assistenza clienti presso la vostra torrefazione.

Ho [numero] anni di esperienza a contatto con il pubblico: [ruolo] presso [azienda/negozio], dove mi occupavo di [rispondere a richieste dei clienti / gestire ordini e resi / risolvere problemi di spedizione — tieni solo ciò che è vero]. È un lavoro che mi ha insegnato soprattutto a capire in fretta cosa serve davvero a chi scrive o telefona, e a dare una risposta chiara anche quando la notizia non è quella sperata.

La vostra ricerca mi interessa perché [motivo concreto: es. seguire un cliente dall'ordine all'abbonamento significa costruire un rapporto che dura, non chiudere un ticket / ho piacere a lavorare per una realtà che cura il prodotto dall'inizio alla fine].

Sono disponibile per un impiego a tempo pieno in sede a Pesaro, dal lunedì al venerdì, a partire da [data].

In allegato trovate il mio curriculum. Resto a disposizione per un colloquio.

Cordiali saluti,
[Nome Cognome]
[telefono] — [email]

---

Tre cose da sistemare prima di inviare:

1. **Il secondo paragrafo è il cuore della candidatura.** Se hai un dato concreto (quante richieste gestivi al giorno, un gestionale che conosci, lingue), mettilo lì al posto delle frasi generiche.
2. **Il "motivo concreto"**: evita "amo il caffè" se non hai nulla da aggiungere — è la frase che scriveranno tutti. Se invece hai lavorato nel settore o sei cliente loro, dillo.
3. **L'indirizzo di invio**: usa una mail personale, non quella universitaria, a meno che non sia il tuo unico contatto abituale.

Se mi dici che lavoro hai fatto e per quanto, te la riscrivo su misura senza segnaposto.

### A6 · Sonnet (sonnet)

Ecco una bozza della mail di candidatura:

**Oggetto:** Candidatura assistenza clienti – Torrefazione Tostavento

Gentili signori,

vi scrivo per candidarmi alla posizione di assistenza clienti che avete pubblicato. Il vostro lavoro, tostare il caffè e spedirlo in tutta Italia attraverso il negozio online, mi interessa molto, e mi piacerebbe contribuire a mantenere alta la qualità del rapporto con i vostri clienti.

Ho [X anni] di esperienza di lavoro a contatto con il pubblico, maturata come [ruolo] presso [azienda/negozio]. In questo ruolo mi sono occupato di [rispondere a richieste e reclami, gestire ordini e resi, ecc.], imparando ad ascoltare con attenzione, a risolvere i problemi con rapidità e a mantenere un tono cordiale anche nelle situazioni più delicate. Sono abituato a lavorare sia al telefono sia per iscritto e a seguire una pratica dall'inizio alla fine, comprese le questioni legate a ordini, resi e abbonamenti.

Sono disponibile a lavorare a tempo pieno, in sede, dal lunedì al venerdì, e sono pronto a trasferirmi a Pesaro / vivo già a Pesaro [scegliere l'opzione corretta].

In allegato trovate il mio curriculum. Sarò lieto di approfondire la mia candidatura in un colloquio, quando vorrete.

Vi ringrazio per l'attenzione e vi porgo cordiali saluti,

Nome Cognome
[telefono] – nome.cognome@email.it

---

Ho lasciato tra parentesi quadre i dettagli che solo tu conosci: anni e tipo di esperienza, mansioni concrete e la tua situazione rispetto a Pesaro. L'annuncio chiede almeno un anno a contatto con il pubblico, quindi conviene metterlo in evidenza. Se hai esperienza con gestionali di e-commerce o con il caffè (anche solo come appassionato), aggiungilo: farebbe la differenza. Vuoi che la adatti con i tuoi dati reali?

### A7 · Sonnet (sonnet)

Ecco una bozza della mail di candidatura.

**Oggetto:** Candidatura assistenza clienti – Torrefazione Tostavento

Gentile Torrefazione Tostavento,

mi chiamo Nome Cognome e scrivo per candidarmi alla posizione di assistenza clienti che avete pubblicato.

Ho maturato [X anni] di esperienza a contatto con il pubblico come [ruolo, es. addetto alle vendite / receptionist / barista] presso [nome azienda], dove mi occupavo di [gestire richieste dei clienti, risolvere problemi, seguire ordini e pratiche]. Questo lavoro mi ha insegnato ad ascoltare con attenzione, a rispondere in modo chiaro e cordiale e a trovare soluzioni concrete anche nelle situazioni più delicate, qualità che ritengo fondamentali per seguire clienti che acquistano online, tra ordini, resi e abbonamenti.

Mi interessa molto il vostro progetto: unire la cura della tostatura artigianale a un servizio di spedizione in tutta Italia richiede attenzione al prodotto e ai clienti, ed è un ambiente in cui mi piacerebbe crescere. Sono disponibile a lavorare a tempo pieno in sede, dal lunedì al venerdì, e a trasferirmi a Pesaro [oppure: sono già residente a Pesaro / zona].

Allego il mio curriculum e resto a disposizione per un colloquio, anche telefonico, in qualsiasi momento.

Ringraziandovi per l'attenzione, vi porgo cordiali saluti.

Nome Cognome
[telefono]
nome.cognome@email.it

---

Prima di inviarla, completa le parti tra parentesi quadre: anni ed esperienza reale (l'annuncio chiede almeno un anno a contatto con il pubblico, quindi conviene metterlo in evidenza), e la tua situazione rispetto a Pesaro, visto che il lavoro è in sede. Se hai esperienza con gestionali, e-commerce o assistenza via mail e telefono, aggiungila: è un punto forte per questo ruolo.

Se mi dai qualche dettaglio sulle tue esperienze, la rendo più precisa e personale. Posso anche prepararla come bozza in Gmail, se vuoi.

### A8 · Sonnet (sonnet)

Ecco una bozza della mail di candidatura:

**Oggetto:** Candidatura – Assistenza clienti

Gentile team di Torrefazione Tostavento,

mi chiamo [Nome Cognome] e desidero candidarmi per la posizione di assistenza clienti che avete pubblicato.

Ho [numero] anni di esperienza in ruoli a contatto con il pubblico, maturata come [ruolo, es. addetto/a vendite, receptionist, operatore call center] presso [azienda/e]. In queste esperienze mi sono occupato/a di rispondere a richieste di clienti via mail e telefono, gestire ordini e risolvere problemi in modo rapido e cortese. [Se pertinente: aggiungere un'esperienza con resi, spedizioni, e-commerce o abbonamenti.]

Il vostro progetto mi interessa perché unisce un prodotto artigianale, il caffè tostato, alla vendita online in tutta Italia. Credo che il rapporto con il cliente sia decisivo in questo tipo di attività, e mi piacerebbe contribuire a renderlo il più chiaro e affidabile possibile, dall'ordine fino all'assistenza dopo l'acquisto.

Sono disponibile a lavorare a tempo pieno, in sede a Pesaro, dal lunedì al venerdì. [Se non risiedi a Pesaro: indicare la disponibilità a trasferirti o i tempi previsti.]

In allegato trovate il mio curriculum. Sarò lieto/a di approfondire in un colloquio, quando preferite.

Ringrazio per l'attenzione e porgo cordiali saluti.

[Nome Cognome]
[Telefono]
[Email]

---

Le parti tra parentesi quadre vanno completate con i tuoi dati. Se mi dici la tua esperienza (ruoli, anni, mansioni) e dove abiti, posso personalizzarla e renderla più incisiva. Ricordati di allegare il CV.

### A9 · Sonnet (sonnet)

**Oggetto:** Candidatura assistenza clienti – Torrefazione Tostavento

Gentile team di Torrefazione Tostavento,

mi chiamo Nome Cognome e desidero candidarmi per la posizione di addetto all'assistenza clienti che avete pubblicato.

Ho [X anni] di esperienza a contatto con il pubblico come [ruolo, es. addetto alla vendita / operatore di call center] presso [azienda]. In quel lavoro mi occupavo di [rispondere a richieste via mail e telefono / gestire ordini e resi / seguire reclami]. Ho imparato ad ascoltare con attenzione, a spiegare le cose in modo chiaro e a risolvere i problemi senza far perdere tempo al cliente.

Mi piace l'idea di lavorare per una realtà che tosta il proprio caffè e lo porta in tutta Italia dal negozio online. Credo che, per un prodotto così, un'assistenza cortese e precisa faccia la differenza. Sono abituato a seguire un ordine dall'inizio alla fine, comprese le pratiche di reso e la gestione degli abbonamenti. Sono inoltre disponibile a lavorare a tempo pieno, in sede, dal lunedì al venerdì.

Allego il mio curriculum e resto a disposizione per un colloquio, anche telefonico, nei giorni e negli orari che preferite.

La ringrazio per l'attenzione e le porgo cordiali saluti.

Nome Cognome
[telefono] · nome.cognome@email.it

---

Prima di inviarla, sostituisci le parti tra parentesi quadre con la tua esperienza reale. L'annuncio chiede almeno un anno a contatto con il pubblico, quindi conviene dirlo esplicitamente. Ricorda anche che il lavoro è a Pesaro, in sede: se non abiti lì, aggiungi una riga sulla tua disponibilità a trasferirti e sulla data da cui potresti iniziare.

Se mi racconti le tue esperienze, la rendo più personale.

### A10 · Sonnet (sonnet)

Ecco una bozza della mail di candidatura. Ho lasciato tra parentesi quadre i dati da completare con le tue informazioni reali.

**Oggetto:** Candidatura assistenza clienti – [Nome Cognome]

Gentile Torrefazione Tostavento,

vi scrivo per candidarmi alla posizione di assistenza clienti che avete pubblicato.

Ho [numero] anni di esperienza di lavoro a contatto con il pubblico, maturata come [ruolo] presso [azienda/luogo]. In quel ruolo mi occupavo di [es. accogliere i clienti, gestire richieste e reclami, seguire ordini e pagamenti], e ho imparato a rispondere in modo chiaro e cordiale anche nelle situazioni più delicate. [Se hai esperienza con mail, telefono o e-commerce, aggiungi qui una frase: ad esempio, "Ho gestito quotidianamente la posta elettronica e le telefonate dei clienti, occupandomi anche di resi e spedizioni."]

Mi piace l'idea di lavorare per un'azienda che unisce un prodotto artigianale come il caffè tostato a un negozio online che raggiunge tutta Italia. Credo che seguire ordini, resi e abbonamenti richieda attenzione ai dettagli e la capacità di far sentire il cliente ascoltato: sono qualità che considero centrali nel mio modo di lavorare.

Sono disponibile a un impiego a tempo pieno, in sede a Pesaro, dal lunedì al venerdì [se non risiedi a Pesaro, indica quando puoi trasferirti o come raggiungerai la sede].

In allegato trovate il mio curriculum. Sarò lieto/a di approfondire in un colloquio, anche telefonico, quando preferite.

Ringrazio per l'attenzione e porgo cordiali saluti,

[Nome Cognome]
[Telefono]
[Email]

---

Se mi dici che esperienze hai avuto e dove abiti, la personalizzo e tolgo tutte le parti tra parentesi. Se vuoi, posso anche prepararla come bozza in Gmail.

## B · errore comune (+ «Sii originale.»)

**Richiesta:**

> Devo rispondere a questo annuncio di lavoro. Mi scrivi la mail di candidatura? «Torrefazione Tostavento (Pesaro): assistenza clienti. Tostiamo caffè e lo spediamo in tutta Italia dal nostro negozio online. Cerchiamo una persona che risponda a mail e telefonate dei clienti e segua ordini, resi e abbonamenti. Serve almeno un anno di lavoro a contatto con il pubblico. Tempo pieno, in sede, dal lunedì al venerdì.» Sii originale.

### B1 · Opus (opus)

Ecco una proposta. Ho lasciato tra parentesi quadre i punti da riempire con la tua esperienza reale — sono quelli che fanno la differenza, quindi vale la pena essere specifici.

**Oggetto:** Candidatura assistenza clienti — ho letto bene la parte sugli abbonamenti

---

Buongiorno,

scrivo per candidarmi alla posizione di assistenza clienti presso Tostavento.

Parto da una cosa che ho imparato in [X anni] dietro [al banco di / al telefono di / alla reception di ...]: chi scrive a un'assistenza clienti quasi mai scrive del problema vero. Il cliente che manda una mail per un ordine in ritardo spesso sta chiedendo se il caffè arriverà prima di domenica, quando ha gente a pranzo. E chi vuole disdire un abbonamento, se glielo chiedi con garbo, otto volte su dieci ti dice che il macinato era troppo fine o che due chili al mese sono troppi — cioè ti sta regalando un'informazione che vale più della disdetta stessa.

Il mio lavoro finora è stato questo: capire la domanda vera, rispondere in modo chiaro e non far sentire nessuno un numero di pratica. Da [nome azienda / tipo di attività] gestivo [descrivi: quante persone al giorno, che tipo di richieste, se usavi gestionali o caselle condivise, se seguivi resi o pratiche fino alla chiusura]. Mi è rimasta l'abitudine di chiudere il cerchio: ricontattare chi aveva avuto un problema anche dopo che il problema era risolto.

Sul caffè non voglio vendermi per quello che non sono: [sono un semplice appassionato che compra grani e macina a casa / ho lavorato un anno come barista / sto imparando]. Ma la merce che spedite è viva, ha una data di tostatura che conta, e immagino che parecchie domande dei vostri clienti riguardino proprio quello — quando è stato tostato, come conservarlo, che macinatura scegliere. È materia che ho voglia di studiare seriamente, perché un'assistenza che sa rispondere nel merito è anche il modo più economico che avete per farvi ricomprare.

Sono [di Pesaro / disponibile a trasferirmi a Pesaro / raggiungo Pesaro da ...] e la sede fissa dal lunedì al venerdì è esattamente ciò che cerco.

Allego il curriculum. Se volete farvi un'idea di come scrivo a un cliente arrabbiato, mandatemi una mail difficile davvero ricevuta da voi: vi rispondo come risponderei se già lavorassi lì.

Grazie per il tempo,
Nome Cognome
[telefono] · nome.cognome@email.it

---

**Tre note sul perché è scritta così**

- L'apertura non dice "sono motivato e dinamico": mostra che capisci il mestiere. È la parte che ti fa leggere fino in fondo, quindi non toglierla.
- Il paragrafo sul caffè ti protegge dal rischio di sembrare finto appassionato. Se davvero non ne sai molto, dillo: vale più dell'entusiasmo di facciata.
- La chiusura con la "mail difficile" è la mossa più rischiosa e anche la più efficace: un'azienda piccola apprezza chi si offre di dimostrare invece di dichiarare. Se ti sembra troppo ardita, sostituiscila con: *"Sono disponibile per un colloquio quando vi è comodo, anche in sede."*

Se mi dici che lavoro hai fatto finora e se sei già a Pesaro, te la riscrivo compilata e pronta da inviare — o te la mando direttamente in bozza su Gmail.

### B2 · Opus (opus)

Ecco la mail. Ho evitato le formule da lettera-tipo e ho puntato su un'idea concreta: nel caffè spedito, l'assistenza clienti è l'ultimo pezzo del prodotto. Le parentesi quadre sono le uniche cose che devi sostituire con i tuoi dati veri.

---

**Oggetto:** Candidatura assistenza clienti — chi risponde è l'ultimo passaggio del caffè

Buongiorno,

vi scrivo per l'annuncio dell'assistenza clienti.

Una cosa che ho imparato lavorando a contatto con il pubblico è che chi scrive o telefona lo fa quasi sempre in un momento poco sereno: l'ordine non è arrivato, il macinato è sbagliato, l'abbonamento è partito due giorni prima dello stipendio. In quei minuti la persona che risponde *è* l'azienda. Voi tostate con cura e spedite in tutta Italia: sarebbe un peccato che tutto quel lavoro si giocasse su una mail rimasta senza risposta per tre giorni.

Vengo da [un anno e mezzo] come [banconista / addetto al front office] a [luogo], dove gestivo [circa 60 clienti al giorno e i reclami sugli ordini]: ho imparato a fare tre cose che qui servono ogni giorno — capire il problema prima di rispondere, dire "ho sbagliato noi" senza girarci intorno, e tenere traccia di tutto così che il collega dopo di me non ricominci da zero.

Sui vostri prodotti sono all'inizio: conosco [la differenza tra una moka e una V60 e poco altro]. Ma è la parte che si studia, e mi interessa studiarla. Il resto — la pazienza al telefono, l'ordine nelle pratiche — l'ho già portato a casa.

Sono disponibile a tempo pieno in sede a Pesaro e volentieri passo a conoscervi in torrefazione.

Grazie per il tempo,
Nome Cognome
[telefono] · nome.cognome@email.it

---

Due note:
- **Il titolo dell'oggetto** è la parte più rischiosa e la più memorabile: se preferisci qualcosa di neutro, usa `Candidatura per assistenza clienti — Nome Cognome`.
- **Se non hai ancora un anno di esperienza col pubblico**, dimmi cosa hai fatto davvero e riscrivo il secondo paragrafo: meglio un dettaglio vero e piccolo che un ruolo gonfiato, in un'azienda di quindici persone se ne accorgono al primo colloquio.
- Se il tuo indirizzo universitario ti sembra fuori luogo per una candidatura non accademica, ti conviene usare un indirizzo personale.

Vuoi che te la salvi come bozza in Gmail?

### B3 · Opus (opus)

Ecco la mail. Ho evitato le formule da lettera di presentazione standard e l'ho impostata su quello che davvero fa chi risponde ai clienti di un e-commerce piccolo.

---

**Oggetto:** Candidatura assistenza clienti — Nome Cognome

Buongiorno,

vi scrivo per l'annuncio sulla posizione in assistenza clienti.

Chi risponde alle mail di una torrefazione online, di fatto, parla con le persone quasi sempre nel momento sbagliato: quando il corriere è in ritardo, quando l'abbonamento è partito una settimana prima del previsto, quando il pacco arriva ammaccato e dentro c'è un regalo. In un negozio di quartiere quei momenti si risolvono guardandosi in faccia; online restano solo una mail e il tono con cui è scritta. È il lavoro che mi interessa fare: non smaltire ticket, ma fare in modo che chi ha avuto un problema ordini di nuovo.

Ho [X] anni di lavoro a contatto con il pubblico presso [azienda/contesto], dove mi sono occupato di [1-2 attività concrete: gestione ordini, reclami, cassa, centralino...]. Ho imparato tre cose che qui credo servano: rispondere prima che il cliente debba sollecitare, dire chiaramente cosa è andato storto senza nascondersi dietro le procedure, e tenere traccia di tutto, perché su resi e abbonamenti i dettagli contano e la memoria no.

Sono disponibile a tempo pieno, in sede a Pesaro, dal lunedì al venerdì, e posso iniziare [dal / con un preavviso di...].

Allego il curriculum. Se vi va, sono volentieri disponibile per un colloquio: mi trovate al [numero] o a questo indirizzo.

Grazie per l'attenzione e buona giornata,

Nome Cognome
[telefono] · [email]

---

**Da completare prima di inviare:** anni ed ex datore di lavoro, due attività concrete che hai svolto, data di disponibilità, telefono.

**Due note pratiche:**
- Valuta di scrivere da un indirizzo personale invece che da quello universitario: `@ateneo.it` può far pensare a una candidatura di passaggio, mentre loro cercano qualcuno stabile in sede.
- Se non sei già a Pesaro o in zona, aggiungi mezza riga sul fatto che sei disponibile a trasferirti: per un impiego a tempo pieno in presenza è la prima cosa che si chiedono leggendo un CV con contatti [di un'altra città].

### B4 · Opus (opus)

Ecco una proposta. Ho lasciato tra parentesi quadre i punti da personalizzare con i tuoi dati reali — il resto è pronto da copiare.

---

**Oggetto:** Candidatura assistenza clienti — [Nome Cognome]

Buongiorno,

quando si vende caffè online, chi risponde alle mail è l'unica persona che il cliente incontra davvero: il prodotto arriva chiuso in un sacchetto, la tostatura non si vede, e tutto quello che resta dell'azienda è il tono con cui viene gestito un ordine in ritardo o un abbonamento da modificare. È il motivo per cui mi interessa il vostro annuncio.

Ho [due anni] di esperienza a contatto con il pubblico presso [azienda/negozio], dove [mi occupavo di accogliere i clienti, gestire le richieste al telefono e risolvere i problemi sugli ordini]. Ho imparato due cose che mi porto dietro: che una risposta chiara e veloce vale più di una risposta perfetta scritta tre giorni dopo, e che chi si lamenta di un reso quasi sempre vuole solo capire cosa sta succedendo.

Sono abituato a lavorare con [gestionali/CRM: indica quelli che conosci] e a tenere traccia delle pratiche aperte senza perdere pezzi per strada. [Bevo caffè con una certa serietà e sarei contento di imparare a raccontarlo bene a chi lo compra.]

Vivo a [città] e la sede di Pesaro non è un problema: l'orario a tempo pieno dal lunedì al venerdì è esattamente quello che cerco.

Allego il curriculum. Resto a disposizione per un colloquio, di persona o al telefono.

Un saluto,
[Nome Cognome]
[telefono] — nome.cognome@email.it

---

Due note:
- **Il terzo paragrafo va tagliato** se non hai esperienza con gestionali: meglio corto e vero che lungo e generico.
- Se vuoi, dimmi due righe sul lavoro che hai fatto finora e ti riscrivo il secondo paragrafo con dettagli concreti al posto dei segnaposto — è la parte che fa la differenza. Posso anche salvartela direttamente come bozza in Gmail.

### B5 · Opus (opus)

Ecco la mail. L'ho tenuta corta — chi legge candidature per un ruolo così ne ha una pila — e ho puntato l'originalità su una cosa sola: dimostrare di aver capito che lavoro è davvero, invece di elencare aggettivi su me stesso.

---

**Oggetto:** Candidatura assistenza clienti — [Nome Cognome]

Buongiorno,

scrivo per la posizione di assistenza clienti pubblicata da Tostavento.

Chi scrive a una torrefazione online quasi mai scrive per parlare di caffè. Scrive perché il corriere ha lasciato il pacco dal vicino sbagliato, perché ha ordinato la macinatura per la moka e gli è arrivata quella per l'espresso, perché parte due settimane e non sa come mettere in pausa l'abbonamento. Sotto la domanda che fa ce n'è sempre un'altra: *questo prodotto che ho pagato arriva o no, e c'è qualcuno dall'altra parte*. Il lavoro, per come lo intendo, è rispondere a entrambe — in fretta, in italiano vero, senza risposte preconfezionate che si vedono a un chilometro.

È quello che ho fatto negli ultimi [X anni] da [ruolo] presso [azienda], dove gestivo [mail/telefono/banco: sostituisci con il canale reale] e mi occupavo di [ordini / resi / reclami / rapporto con i corrieri]. Ho imparato che un reso gestito bene fa tornare il cliente più di un ordine andato liscio, e che quasi tutto si risolve dicendo subito come stanno le cose, anche quando la notizia non è buona.

Sono di [città], disponibile a tempo pieno in sede a Pesaro dal lunedì al venerdì, e posso iniziare [data / con preavviso di X settimane].

In allegato il CV. Se vi va, sono volentieri disponibile per un colloquio.

Grazie per l'attenzione,
[Nome Cognome]
[telefono] · [mail]

---

**Da sistemare prima di inviare:** tutti i campi tra parentesi quadre — soprattutto il paragrafo sull'esperienza, che regge tutta la mail. Se il tuo anno "a contatto con il pubblico" è stato in bar, negozio o reception invece che via mail, non nasconderlo: scrivilo e aggiungi mezza riga sul fatto che al banco impari a leggere una persona in tre secondi, cosa che via mail serve uguale.

Se mi dici cosa hai fatto davvero, te la riscrivo su misura.

### B6 · Sonnet (sonnet)

**Oggetto:** Candidatura assistenza clienti – da chi sa che un caffè arrivato tardi rovina la colazione

Gentile team di Tostavento,

il vostro caffè viaggia da Pesaro fino alla cucina di chi lo ordina. Quando qualcosa va storto, come un pacco in ritardo, una miscela sbagliata o un abbonamento da modificare, il cliente ha spesso il primo caffè della giornata già in dubbio. In quel momento chi risponde fa la differenza, e mi candido per essere quella persona.

Mi chiamo [Nome Cognome]. Da [durata, es. due anni] lavoro a contatto con il pubblico come [ruolo] presso [azienda/luogo]. Lì ho imparato tre cose che credo servano anche da voi:

- **Ascoltare prima di rispondere.** Spesso il problema vero non è quello scritto nella prima riga della mail.
- **Chiudere le questioni, non rimandarle.** Un reso o un ordine smarrito si segue fino alla soluzione, e il cliente deve saperlo senza doverlo chiedere.
- **Restare cordiale anche alla ventesima telefonata della giornata.** Il tono giusto si allena, e lo curo con attenzione.

[Se vero, aggiungi una riga concreta: un risultato ottenuto, una gestione di ordini o resi, l'uso di un gestionale o di un e-commerce.]

Sono disponibile a un impiego a tempo pieno, in sede a Pesaro, dal lunedì al venerdì. [Se serve: precisa se risiedi già a Pesaro o da quando potresti trasferirti.]

Allego il mio curriculum. Sarei felice di raccontarvi di persona come lavoro, magari davanti a una tazzina delle vostre.

Cordiali saluti,
[Nome Cognome]
[Telefono] · nome.cognome@email.it

---

Ho lasciato tra parentesi quadre i punti che solo tu puoi compilare: ruolo, durata dell'esperienza, un dato concreto e la tua situazione riguardo a Pesaro. Se mi dici di più sul tuo percorso, posso rendere la mail più personale. Posso anche prepararne una versione più breve e sobria, se preferisci un tono più formale.

### B7 · Sonnet (sonnet)

**Oggetto:** Candidatura assistenza clienti – [Nome Cognome]

Gentile team di Tostavento,

il caffè che arriva a casa di qualcuno è l'unico contatto fisico che avete con i clienti. Tutto il resto passa da una mail o da una telefonata, ed è lì che decido di candidarmi: voglio essere la persona che risponde.

Mi chiamo Nome Cognome e ho [X anni] di esperienza a contatto con il pubblico come [ruolo, es. addetto alla vendita / operatore di sportello / cameriere] presso [azienda]. Quel lavoro mi ha insegnato tre cose che credo servano anche da voi:

- **Un ordine in ritardo non è un numero.** Dietro c'è qualcuno che aspettava il suo caffè per la colazione di domani. Rispondo prima con una soluzione e poi con le spiegazioni.
- **Un reso si gestisce meglio con un sorriso.** Un cliente che restituisce un pacco e viene trattato bene spesso ordina di nuovo.
- **Un abbonamento è una relazione.** Vuol dire ricordarsi le preferenze, avvisare prima che sorgano problemi e non far sentire nessuno un codice cliente.

Sono abituato a tenere in ordine molte pratiche aperte insieme, a scrivere mail chiare e a mantenere la calma quando dall'altra parte c'è qualcuno che ha fretta. La disponibilità a tempo pieno, in sede a Pesaro, dal lunedì al venerdì, per me va bene. [Se serve, aggiungi: sono già residente a Pesaro / sono disposto a trasferirmi.]

Nel CV in allegato trovate i dettagli. Mi farebbe piacere raccontarvi di persona come lavoro, magari davanti a una tazza di quello che tostate.

Grazie per l'attenzione e a presto,

Nome Cognome
[telefono] · nome.cognome@email.it

---

Prima di inviarla, sostituisci le parti tra parentesi quadre con i tuoi dati reali. L'annuncio chiede almeno un anno di lavoro a contatto con il pubblico, quindi indica chiaramente durata e ruolo. Non conosco la tua esperienza, per questo non l'ho inventata. Se vuoi, dimmi da dove parti e la adatto: posso renderla più formale, più breve o più informale.

### B8 · Sonnet (sonnet)

**Oggetto:** Candidatura assistenza clienti: chi risponde quando il caffè non arriva (o arriva troppo presto)

Buongiorno,

mi chiamo Nome Cognome e mi candido per la posizione di assistenza clienti presso Tostavento.

Chi scrive a un'assistenza clienti di caffè di solito ha una di queste urgenze: il pacco non è arrivato, la macinatura è sbagliata, l'abbonamento è arrivato proprio mentre era in vacanza. Sono problemi piccoli, ma la mattina senza caffè non lo sembrano. Per questo penso che rispondere bene voglia dire capire l'urgenza prima ancora di cercare la soluzione, e poi risolvere in modo concreto, senza formule di rito.

Ho [X anni] di esperienza a contatto con il pubblico come [ruolo] presso [azienda/attività], dove mi occupavo di [gestione reclami / ordini / resi / telefonate e mail]. Ho imparato a mantenere la calma quando l'interlocutore non ce l'ha, a spiegare le cose in modo semplice e a non lasciare mai una richiesta senza un seguito chiaro. Sono abituato a seguire una pratica dall'inizio alla fine: ordine, spedizione, eventuale reso o rimborso, e a tenere tutto tracciato in modo che nessun cliente debba ripetere la propria storia due volte.

Sono disponibile a lavorare a tempo pieno in sede, dal lunedì al venerdì, [e a trasferirmi a Pesaro / e già residente a Pesaro]. Mi piacerebbe mettere queste competenze al servizio di un prodotto artigianale come il vostro, che spedite in tutta Italia e che quindi merita un'assistenza all'altezza.

Allego il mio CV e sono a disposizione per un colloquio, anche telefonico. E se vorrete metterci alla prova, sono pronto a rispondere a una mail di un cliente arrabbiato: sarebbe un ottimo modo per conoscerci.

Cordiali saluti,
Nome Cognome
[telefono] · nome.cognome@email.it

---

Ho lasciato tra parentesi quadre i dettagli che solo tu conosci: anni ed esperienza reali, ruolo, e la tua situazione rispetto a Pesaro. Se me li dai, rifinisco il testo. Posso anche prepararne una versione più formale o più breve.

### B9 · Sonnet (sonnet)

**Oggetto:** Candidatura assistenza clienti – Nome Cognome

Gentile team di Tostavento,

ho letto il vostro annuncio con il caffè accanto, che mi sembrava il minimo. Vi scrivo per candidarmi come addetto all'assistenza clienti.

Un cliente che scrive a una torrefazione online di solito vuole sapere una cosa sola: dov'è il suo caffè, o come sistemare quello che non è andato come doveva. Rispondere bene significa dare una risposta chiara e sapere già cosa succede dopo. Il lavoro che vedo nel vostro annuncio, tra ordini, resi e abbonamenti, è proprio questo.

Ho [X anni] di esperienza a contatto con il pubblico come [ruolo] presso [azienda/luogo]. Lì ho imparato tre cose che porterei da voi:

- **Ascoltare prima di rispondere.** Spesso il problema reale emerge dopo la prima frase.
- **Chiudere le questioni.** Preferisco seguire una pratica fino alla soluzione, invece di passarla da una persona all'altra.
- **Restare cordiale quando il cliente non lo è.** Al telefono e per mail, con un tono chiaro e mai burocratico.

[Se vero: aggiungere una riga su strumenti gestionali o e-commerce già usati, o sul vostro interesse per il caffè.]

Sono disponibile a lavorare a tempo pieno in sede a Pesaro, dal lunedì al venerdì, [e a iniziare da data/entro tempi]. Allego il mio CV e sarei felice di raccontarvi di persona come lavoro.

Grazie per l'attenzione.

Cordiali saluti,
Nome Cognome
[telefono] · nome.cognome@email.it

---

Prima di inviarla, sostituisci le parti tra parentesi con i tuoi dati reali: esperienza, ruolo e data di disponibilità. Ho scelto di non inventare nulla. Se mi dici dove hai lavorato finora, rendo le tre righe centrali più specifiche. Se invece vuoi un tono più sobrio, posso toglierti l'apertura sul caffè.

### B10 · Sonnet (sonnet)

**Oggetto:** Candidatura assistenza clienti – da uno che sa che un caffè in ritardo è una piccola tragedia

Gentile team di Tostavento,

mi chiamo Nome Cognome e mi candido per la posizione di assistenza clienti.

Vendere caffè online ha una particolarità: chi scrive al servizio clienti spesso non ha un problema tecnico, ha una mattina che non parte. Il pacco non è arrivato, la macinatura era sbagliata, l'abbonamento andava sospeso prima delle ferie. Per questo credo che rispondere bene conti quanto tostare bene. Serve rapidità, ma anche chiarezza e un po' di tatto.

Ho [X anni] di esperienza a contatto con il pubblico come [ruolo] presso [azienda/attività], dove mi sono occupato di [gestione richieste, reclami, ordini, resi, telefonate…]. Lì ho imparato tre cose che porterei da voi:

- **Ascoltare prima di rispondere.** Spesso il cliente arrabbiato ha ragione a metà, e capire quale metà fa risparmiare tempo a tutti.
- **Tenere il filo di un ordine dall'inizio alla fine.** Per me un reso o un abbonamento non è un ticket da chiudere, ma una storia da seguire finché il cliente non è davvero a posto.
- **Scrivere mail che si leggono volentieri.** Brevi, gentili, senza formule da modulo.

Sono disponibile a lavorare a tempo pieno, in sede a Pesaro, dal lunedì al venerdì. [Se serve: sono già residente a Pesaro / sono disponibile a trasferirmi entro …].

Allego il mio CV e sarei felice di raccontarvi di persona come lavoro, magari davanti a una tazzina delle vostre.

Grazie per l'attenzione e a presto,

Nome Cognome
[telefono] · nome.cognome@email.it

---

**Prima di inviarla:**
- Compila le parti tra parentesi con la tua esperienza reale. L'annuncio chiede almeno un anno a contatto con il pubblico, quindi va indicato in modo esplicito.
- Se abiti fuori Pesaro, chiarisci subito la questione trasferimento, perché la sede è un requisito.
- Se hai già bevuto o comprato il loro caffè, aggiungi una riga con un dettaglio vero (una miscela, un'origine). Farà più effetto di qualsiasi complimento generico.

Se mi racconti la tua esperienza, la riscrivo su misura e con un tono più formale o più informale, come preferisci.

## C · la mossa (+ un dettaglio vero)

**Richiesta:**

> Devo rispondere a questo annuncio di lavoro. Mi scrivi la mail di candidatura? «Torrefazione Tostavento (Pesaro): assistenza clienti. Tostiamo caffè e lo spediamo in tutta Italia dal nostro negozio online. Cerchiamo una persona che risponda a mail e telefonate dei clienti e segua ordini, resi e abbonamenti. Serve almeno un anno di lavoro a contatto con il pubblico. Tempo pieno, in sede, dal lunedì al venerdì.» Da tre anni lavoro al banco di una ferramenta: al telefono rispondo io, una trentina di chiamate al giorno, e i clienti arrabbiati li passano a me.

### C1 · Opus (opus)

Ecco la mail, pronta da copiare.

**Oggetto:** Candidatura assistenza clienti — Nome Cognome

Buongiorno,

scrivo in risposta al vostro annuncio per la posizione di assistenza clienti presso Torrefazione Tostavento.

Da tre anni lavoro al banco di una ferramenta, dove mi occupo anche di tutto il centralino: rispondo a una trentina di chiamate al giorno tra richieste di disponibilità, consigli sui prodotti e verifiche sugli ordini. Nel tempo sono diventato il riferimento per i clienti più difficili: quando una telefonata si mette male, i colleghi la passano a me. Ho imparato che quasi sempre basta ascoltare fino in fondo, dire con chiarezza cosa si può fare e poi farlo davvero, richiamando io per primo quando c'è un aggiornamento.

È un lavoro che mi piace e che vorrei continuare a fare in un contesto come il vostro, dove il rapporto con il cliente non finisce con la vendita ma prosegue tra ordini, resi e abbonamenti. Mi riconosco in un prodotto curato, che ha bisogno di un'assistenza altrettanto curata.

Sono disponibile a tempo pieno e in sede, dal lunedì al venerdì.

Allego il mio curriculum e resto a disposizione per un colloquio, di persona o al telefono.

Cordiali saluti,
Nome Cognome
[telefono] — [email]

---

Tre cose prima di inviarla:

- **L'indirizzo mittente.** Se scrivi dalla mail universitaria, valuta di usarne una personale con nome e cognome: per un'azienda privata è più immediata.
- **Pesaro.** Se non ci abiti, una riga in più sul fatto che sei disponibile a trasferirti (o che sei già in zona) toglie il dubbio principale a chi legge.
- **Il CV.** Ricordati di allegarlo davvero — la frase lo dà per scontato.

### C2 · Opus (opus)

Ecco la mail. Ho tenuto un tono semplice e concreto, mettendo in evidenza i tre anni al banco, il telefono e la gestione dei clienti difficili — cioè esattamente quello che chiedono.

---

**Oggetto:** Candidatura per assistenza clienti

Buongiorno,

ho letto il vostro annuncio per una persona da inserire nell'assistenza clienti e vorrei propormi.

Da tre anni lavoro al banco di una ferramenta. È un lavoro fatto di persone: al telefono rispondo io, una trentina di chiamate al giorno, e quando un cliente è arrabbiato lo passano a me. Ho imparato a farlo parlare, a capire cosa è andato storto davvero e a dirgli con chiarezza cosa posso fare e in quanto tempo. Quasi sempre la telefonata finisce bene.

Mi occupo anche di ordini, di ritiri e di resi, quindi seguire una pratica dall'inizio alla fine e tenere le cose in ordine è parte della mia giornata. Rispondere per iscritto non mi spaventa: scrivo in modo chiaro e senza far perdere tempo a chi legge.

Mi interessa il vostro lavoro perché vendete un prodotto che ha bisogno di essere spiegato, e chi compra caffè online spesso ha domande vere: il tipo di macinatura, i tempi di consegna, l'abbonamento da modificare. Mi piacerebbe portare a Tostavento lo stesso modo di lavorare che ho al banco.

Sono disponibile a tempo pieno, in sede, dal lunedì al venerdì. In allegato trovate il mio curriculum. Resto a disposizione per un colloquio, di persona o al telefono.

Grazie per l'attenzione e buona giornata,

[Nome e cognome]
[Telefono]
nome.cognome@email.it

---

Due cose da sistemare prima di inviare:

- **Destinatario:** l'annuncio non riporta l'indirizzo email dell'azienda — recuperalo dal sito o dall'annuncio originale.
- **Allegato:** ricordati di allegare davvero il CV, visto che la mail lo cita.

Se vuoi, posso fartene una versione più breve (5-6 righe) oppure adattarla nel caso la candidatura vada inviata tramite un modulo del sito anziché per mail.

### C3 · Opus (opus)

Ecco la mail. Ho lasciato tra parentesi quadre solo le cose che non so (nome, contatti, eventuale disponibilità/residenza): sostituiscile prima di inviare.

---

**Oggetto:** Candidatura per assistenza clienti

Buongiorno,

scrivo in merito all'annuncio per la posizione di assistenza clienti presso Torrefazione Tostavento.

Da tre anni lavoro al banco di una ferramenta, dove mi occupo della vendita diretta e, soprattutto, del telefono: rispondo io a una trentina di chiamate al giorno, tra richieste di disponibilità, ordini, resi e problemi post-vendita. Con il tempo sono diventato anche la persona a cui i colleghi passano i clienti più arrabbiati, perché riesco a farli parlare, capire dove si è inceppata la cosa e proporre una soluzione concreta senza far salire il tono.

È un lavoro che mi ha insegnato a essere rapido ma preciso: tenere traccia di cosa è stato promesso a chi, richiamare quando si è detto che si richiama, e dare risposte chiare anche quando la risposta non è quella che il cliente sperava. Mi sembrano le stesse qualità che servono per seguire ordini, resi e abbonamenti di un negozio online.

Cerco una posizione a tempo pieno in sede e la vostra corrisponde a quello che sto cercando. [Sono di Pesaro / Sono facilmente raggiungibile dalla vostra sede.]

Allego il curriculum. Resto a disposizione per un colloquio, di persona o al telefono, quando vi è comodo.

Cordiali saluti,
[Nome Cognome]
[telefono] — [email]

---

Due note:
- **L'allegato**: nell'annuncio non c'è un indirizzo mail, quindi controlla dove vogliono la candidatura (modulo sul sito o indirizzo in fondo alla pagina) e ricordati di allegare davvero il CV.
- **La frase sulla residenza**: se non abiti a Pesaro ma sei disposto a spostarti, scrivilo esplicitamente ("sono disponibile a trasferirmi") — per un lavoro in sede è la prima cosa che guardano.

### C4 · Opus (opus)

Ecco la mail, pronta da copiare.

**Oggetto:** Candidatura per assistenza clienti

---

Buongiorno,

scrivo in risposta al vostro annuncio per la posizione di assistenza clienti.

Da tre anni lavoro al banco di una ferramenta. Il telefono lo gestisco io: una trentina di chiamate al giorno tra richieste di disponibilità, ordini da seguire e resi da sistemare. Quando un cliente è arrabbiato, di solito lo passano a me — mi trovo a mio agio nel far parlare la persona, capire dove si è rotta la catena e dirle con chiarezza cosa succede adesso, anche quando la risposta non è quella che sperava.

È un lavoro che mi ha abituato a tenere insieme due cose: la precisione su ordini e pratiche, e il tono giusto con chi ho davanti o al telefono. Mi sembra il nucleo anche del ruolo che cercate, con la differenza che il cliente non è più davanti al banco ma dall'altra parte di una mail.

Il caffè come prodotto mi interessa e mi piacerebbe imparare a conoscerlo bene: credo che per rispondere con proprietà a chi ordina serva sapere cosa c'è nel sacchetto.

Allego il mio curriculum. Resto a disposizione per un colloquio, di persona o al telefono.

Cordiali saluti,
Nome Cognome
[telefono]

---

Tre cose prima di inviarla:

- **Indirizzo del destinatario:** l'annuncio che mi hai riportato non lo contiene. Cercalo sul sito della torrefazione o nel testo originale dell'annuncio.
- **Sede:** non ho scritto nulla sulla tua disponibilità a lavorare a Pesaro perché non so dove abiti. Se sei fuori zona, conviene aggiungere una riga esplicita ("sono a X, disponibile a trasferirmi / già in zona"): un annuncio "in sede" fa scartare in fretta chi sembra lontano.
- **Mittente:** se scrivi dall'indirizzo ateneo.it, valuta se usarne uno personale — per una candidatura fuori dall'ambito universitario è di solito più lineare.

### C5 · Opus (opus)

Ecco la mail. È volutamente asciutta: per un ruolo di assistenza clienti conta più un esempio concreto che gli aggettivi.

---

**Oggetto:** Candidatura assistenza clienti — Nome Cognome

Buongiorno,

scrivo in merito all'annuncio per la posizione di assistenza clienti presso Tostavento.

Da tre anni lavoro al banco di una ferramenta. Il telefono lo gestisco io: una trentina di chiamate al giorno tra richieste di disponibilità, ordini da seguire e problemi su pezzi già venduti. Quando un cliente si arrabbia, in negozio lo passano a me — è diventato il mio compito, e ho imparato che quasi sempre la soluzione è ascoltare fino in fondo, dire con chiarezza cosa posso e cosa non posso fare, e poi richiamare quando ho promesso di richiamare.

È un lavoro fatto di cose che tornano: capire in fretta di cosa ha bisogno una persona, tenere insieme più pratiche aperte senza perderne il filo, rispondere anche quando la notizia da dare non è quella che il cliente spera. Mi sembrano le stesse cose che servono per seguire ordini, resi e abbonamenti di un negozio online.

Sono disponibile a tempo pieno, in sede, dal lunedì al venerdì. Resto volentieri a disposizione per un colloquio, di persona o al telefono.

Grazie per l'attenzione,

Nome Cognome
[telefono]
nome.cognome@email.it

---

Tre cose da sistemare prima di inviarla:

- **Destinatario:** nell'annuncio che mi hai girato non c'è l'indirizzo a cui scrivere — va recuperato dal testo originale o dal sito.
- **Indirizzo mittente:** ho messo quello universitario perché è l'unico che conosco, ma per una candidatura fuori dall'ambito accademico un indirizzo personale fa un effetto migliore. Se ne hai uno, userei quello.
- **Pesaro:** se non abiti già in zona, aggiungerei mezza riga sul punto (che ti trasferisci, o che sei già lì) — su un full time in sede è la prima cosa che si chiedono leggendo.

Se mi dici che vuoi un tono più caldo — tipo due righe sul caffè, se davvero ti interessa — te la riscrivo, ma senza forzare: l'entusiasmo finto in una mail si sente.

### C6 · Sonnet (sonnet)

Oggetto: Candidatura – Assistenza clienti

Gentile team di Torrefazione Tostavento,

mi chiamo [Nome e Cognome] e vorrei candidarmi per la posizione di assistenza clienti che avete pubblicato.

Da tre anni lavoro al banco di una ferramenta, dove il contatto con il pubblico è la parte principale del mio lavoro. Rispondo io al telefono, circa una trentina di chiamate al giorno, e sono la persona a cui vengono passati i clienti più arrabbiati. Ho imparato ad ascoltare con calma, a capire dove sta il problema e a trovare una soluzione concreta, anche quando il cliente arriva già irritato. È un'abilità che mi sembra molto utile per seguire ordini, resi e abbonamenti, dove spesso ci si trova a gestire ritardi, errori o aspettative disattese.

Sono abituato a un lavoro a ritmo pieno e a tenere insieme più richieste alla volta senza perdere precisione. Sono disponibile a lavorare a tempo pieno, in sede, dal lunedì al venerdì, e mi piacerebbe mettere la mia esperienza al servizio di un'azienda che cura il proprio prodotto come fate voi.

Allego il mio curriculum e resto a disposizione per un colloquio, anche telefonico.

Cordiali saluti,
[Nome e Cognome]
[Telefono] · nome.cognome@email.it

---

Ho lasciato tra parentesi quadre nome e telefono. Se vuoi, posso aggiungere una riga sul tuo interesse per il caffè o sulla tua conoscenza di strumenti come gestionali o e-commerce, se ne hai esperienza.

### C7 · Sonnet (sonnet)

Oggetto: Candidatura assistenza clienti – Torrefazione Tostavento

Gentile Torrefazione Tostavento,

mi chiamo Nome Cognome e desidero candidarmi alla posizione di assistenza clienti che avete pubblicato.

Da tre anni lavoro al banco di una ferramenta, a contatto diretto con il pubblico ogni giorno. Sono la persona che risponde al telefono: gestisco circa trenta chiamate al giorno, con richieste che vanno dalle informazioni sui prodotti alla verifica di ordini e disponibilità. Quando un cliente è insoddisfatto o arrabbiato, la chiamata viene passata a me, e ho imparato ad ascoltare, mantenere la calma e trovare una soluzione concreta, che sia un cambio, un rimborso o una spiegazione chiara.

Credo che questa esperienza sia molto vicina a ciò che cercate: rispondere con precisione e cortesia a clienti che scrivono o telefonano, seguire un ordine fino alla consegna e gestire resi e problemi senza perdere il rapporto con la persona. Il caffè è un prodotto che le persone scelgono con cura, e mi piacerebbe contribuire a farle sentire seguite anche a distanza.

Sono disponibile a lavorare a tempo pieno, in sede a Pesaro, dal lunedì al venerdì.

Allego il mio curriculum e resto a disposizione per un colloquio, anche telefonico, nei giorni e negli orari che preferite.

Cordiali saluti,
Nome Cognome
nome.cognome@email.it
[numero di telefono]

---

Due note: ho scritto che sei disponibile a lavorare a Pesaro in sede, quindi se dovessi trasferirti conviene dirlo esplicitamente (ad esempio "sono disposto a trasferirmi"). Inoltre, se hai un indirizzo email più adatto del tuo account universitario, usalo. Se vuoi, posso anche prepararla come bozza in Gmail.

### C8 · Sonnet (sonnet)

Oggetto: Candidatura assistenza clienti – Torrefazione Tostavento

Gentili signori,

vi scrivo per candidarmi alla posizione di addetto all'assistenza clienti presso Torrefazione Tostavento.

Da tre anni lavoro al banco di una ferramenta, a diretto contatto con il pubblico. Gestisco in prima persona il telefono, con circa trenta chiamate al giorno, e sono la persona a cui i colleghi passano i clienti più insoddisfatti. Ho quindi maturato esperienza concreta nel capire in fretta il problema, mantenere la calma e trovare una soluzione che lasci il cliente soddisfatto. Sono competenze che ritengo direttamente utili per seguire ordini, resi e abbonamenti di un negozio online.

Mi piacerebbe mettere questa esperienza al servizio di una realtà che cura il proprio prodotto e i propri clienti come la vostra. Sono disponibile a lavorare a tempo pieno, in sede, dal lunedì al venerdì.

Allego il mio curriculum e resto a disposizione per un colloquio, anche telefonico, nei giorni e negli orari che preferite.

Cordiali saluti,

[Nome e cognome]
[Telefono]
[Email]

---

Due note: ho lasciato tra parentesi quadre i tuoi dati di contatto. Se hai già usato un e-commerce o gestito ordini, resi o consegne in ferramenteria, aggiungilo, perché rafforza la candidatura. Se vuoi, posso anche adattare il tono (più formale o più diretto).

### C9 · Sonnet (sonnet)

Oggetto: Candidatura assistenza clienti – Torrefazione Tostavento

Gentile Torrefazione Tostavento,

mi chiamo Nome Cognome e desidero candidarmi per la posizione di addetto all'assistenza clienti che avete pubblicato.

Da tre anni lavoro al banco di una ferramenta, a contatto diretto con il pubblico. Sono io la persona che risponde al telefono: gestisco circa trenta chiamate al giorno, dalle richieste di informazioni ai problemi con gli ordini. Quando un cliente è insoddisfatto o arrabbiato, i colleghi lo passano a me: ho imparato ad ascoltare con calma, a capire il problema e a trovare una soluzione concreta, lasciando la persona soddisfatta del servizio ricevuto.

Questa esperienza mi ha dato pratica nella gestione di richieste, reclami e ordini, cioè le attività che caratterizzano il ruolo che cercate, compresi resi e abbonamenti. Sono abituato a lavorare con continuità, a tempo pieno e in sede, dal lunedì al venerdì, e la vostra impostazione mi si adatta bene.

Mi piacerebbe mettere queste competenze al servizio di un'azienda che lavora un prodotto artigianale come il caffè e lo porta ai clienti in tutta Italia. Allego il mio curriculum e resto a disposizione per un colloquio, anche telefonico, nei giorni e negli orari che preferite.

La ringrazio per l'attenzione e porgo cordiali saluti.

Nome Cognome
nome.cognome@email.it
[numero di telefono]

---

Due note: ho lasciato il segnaposto per il telefono, da completare. Inoltre l'annuncio è di Pesaro e lavoro in sede: se non abiti già lì, conviene aggiungere una riga sulla tua disponibilità a trasferirti e da quando. Se vuoi, posso anche aggiungere un accenno alla tua passione per il caffè, se ce l'hai.

### C10 · Sonnet (sonnet)

Oggetto: Candidatura assistenza clienti – Torrefazione Tostavento

Gentile Torrefazione Tostavento,

mi chiamo Nome Cognome e vi scrivo per candidarmi alla posizione di addetto all'assistenza clienti che avete pubblicato.

Da tre anni lavoro al banco di una ferramenta, a contatto diretto con il pubblico. Sono io a rispondere al telefono, con una trentina di chiamate al giorno, e quando un cliente è arrabbiato la chiamata passa a me. Ho imparato ad ascoltare con calma, a capire in fretta dove sta il problema e a proporre una soluzione concreta, anche quando la risposta non è quella che il cliente sperava. Questo vale per un ordine in ritardo, per un reso o per un dubbio su un prodotto.

Sono abituato a seguire una richiesta fino alla sua chiusura, e penso sia questo che conta per gestire bene ordini, resi e abbonamenti di un negozio online. Sono disponibile a lavorare a tempo pieno in sede dal lunedì al venerdì.

Mi piacerebbe mettere questa esperienza al servizio di un'azienda che spedisce in tutta Italia un prodotto artigianale come il vostro caffè. Allego il mio curriculum e resto a disposizione per un colloquio, anche telefonico.

Ringrazio per l'attenzione e porgo cordiali saluti,

Nome Cognome
nome.cognome@email.it
[numero di telefono]

---

Due note: non ho scritto nulla sul trasferimento a Pesaro, perché non so dove abiti. Se vivi altrove, conviene aggiungere una riga sulla tua disponibilità a trasferirti. Ricordati anche di inserire il numero di telefono e di allegare il CV. Se hai usato strumenti come un gestionale ordini o un CRM, aggiungili: qui contano.
