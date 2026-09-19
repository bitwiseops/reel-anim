# Uscite vere · scrivere-con-ia · 2026-09-19

Generate il 2026-09-19 dalla tappa T0b di `/pipeline` con `claude -p` (2.1.278 (Claude Code)), da una cartella neutra:
`--model opus|sonnet --system-prompt "Sei un assistente che scrive testi su richiesta." --tools "" --no-session-persistence`.
Sigle: 1-5 Opus, 6-10 Sonnet. Mail, cliente e Giulia inventate; la bozza è identica nelle quattro richieste, cambia solo
la prima frase. Testi riportati così come sono usciti, con un solo ritocco: `claude -p` passa al modello nome ed email
dell'account; in A5 il modello ha usato il cognome del presentatore come esempio («Gentile signora …»), qui sostituito
da «Cognome» (1 sostituzione su 40 uscite; nome ed email non compaiono). A schermo non vanno mai i dati veri.
La richiesta D non entra in questo reel: serve alla caption e a un eventuale reel sui complimenti del modello.

Prima lettura grezza del coordinatore (**da ricontare a mano, uscita per uscita, prima di portare un numero nel reel**):
- A e B: l'unica frase della bozza che torna quasi sempre identica è «Le venti sedie arriveranno venerdì 16 ottobre»;
  «mi dispiace il doppio» sparisce dalla mail in quasi tutte le A (resta in alcune B: B1, B2, B5); «gliene porto io»
  non torna in nessuna mail, resta il prestito con altre parole. Alcune uscite aggiungono fatti che la bozza non ha
  (A5: consegna il 2 ottobre, risposta entro il 28 settembre). A3 e B2 non chiudono con la firma: da guardare a parte.
- C: tutte e dieci segnalano «mi dispiace il doppio» come difetto («vago», «colloquiale», «un po' infantile» in C2):
  regge la tappa «attenzione però». Tutte segnalano «di poco» e «in realtà».

## A · base («migliora»)

**Richiesta:**

> Migliora questa mail. «Buongiorno signora Carla, in realtà volevo scriverle già ieri. Purtroppo sono stati riscontrati dei problemi molto seri dal nostro fornitore nella fase di verniciatura, e quindi dobbiamo procedere a una riprogrammazione della consegna, che sostanzialmente slitta davvero di poco. So che le sedie le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio. Le venti sedie arriveranno venerdì 16 ottobre. Se vuole, per sabato gliene porto io dodici delle nostre, in prestito. Un saluto, Giulia»

### A1 · Opus (opus)

Ecco la versione riscritta:

---

**Oggetto: Consegna sedie – nuova data e soluzione per l'inaugurazione**

Buongiorno signora Carla,

le scrivo per comunicarle un contrattempo sulla sua consegna.

Il nostro fornitore ha riscontrato un problema serio nella fase di verniciatura e questo ci obbliga a riprogrammare: le venti sedie saranno consegnate **venerdì 16 ottobre**, invece della data prevista.

Mi rendo conto che le aspettava per l'inaugurazione di sabato 3 ottobre e me ne dispiace sinceramente.

Per non lasciarla senza sedute quel giorno, le propongo questa soluzione: le porto io dodici sedie delle nostre, in prestito, così può coprire l'evento e restituirmele con calma dopo la consegna definitiva.

Mi faccia sapere se la soluzione le va bene o se preferisce che studiamo un'alternativa: sono a disposizione.

Un cordiale saluto,
Giulia

---

**Cosa ho cambiato e perché**

- **Aggiunto l'oggetto**: dice subito che c'è un problema *e* che c'è già una soluzione.
- **Tolto "in realtà volevo scriverle già ieri"**: non aggiunge nulla e parte con una piccola scusa che indebolisce il tono.
- **Tolto "slitta davvero di poco"**: sono quasi due settimane di ritardo su un evento saltato. Minimizzare rischia di irritare; meglio dire la data e basta.
- **"mi dispiace il doppio" → "me ne dispiace sinceramente"**: più sobrio e professionale.
- **Il prestito diventa una proposta strutturata**, non un ripensamento buttato lì ("se vuole, gliene porto io..."): specifico che può restituirle dopo, così l'offerta sembra solida e non un favore imbarazzato.
- **Chiusura con call to action**: chiede una risposta e apre a soluzioni diverse.

**Un punto da valutare**: dodici sedie su venti lasciano comunque uno scoperto. Se può recuperarne altre otto, anche di modello diverso, varrebbe la pena dirlo esplicitamente; se non è possibile, forse conviene accennarlo lei per prima ("so che non coprono l'intero fabbisogno, ma...") così non sembra una svista.

### A2 · Opus (opus)

Ecco una versione riscritta:

**Oggetto: Consegna sedie — nuova data e soluzione per sabato 3 ottobre**

Buongiorno signora Carla,

le scrivo con qualche giorno di ritardo, di cui mi scuso: volevo comunicarle la notizia solo con una soluzione già pronta.

Il nostro fornitore ha riscontrato un problema serio nella fase di verniciatura e siamo costretti a riprogrammare la consegna. Le venti sedie arriveranno **venerdì 16 ottobre**, quindi dopo l'inaugurazione di sabato 3: mi rendo conto che è un contrattempo pesante e me ne dispiace sinceramente.

Per non lasciarla scoperta, posso prestarle **dodici sedie delle nostre** per l'inaugurazione, consegnate in loco entro venerdì 2 ottobre e ritirate quando le nuove saranno arrivate. Se dodici non bastano, mi dica pure di quante avrebbe bisogno: vedo cosa riesco a recuperare.

Mi faccia sapere e organizzo subito.

Un cordiale saluto,
Giulia

**Cosa ho cambiato e perché:**

- **Aggiunto l'oggetto**, che anticipa sia il problema sia il fatto che c'è una soluzione.
- **Tolto "slitta davvero di poco"**: tra il 3 e il 16 ottobre passano quasi due settimane e l'inaugurazione salta. Minimizzare un ritardo che il cliente vedrà benissimo indebolisce la sua credibilità; meglio nominarlo con chiarezza e compensare con i fatti.
- **Date messe in evidenza** e reso esplicito il rapporto tra le due (arrivo *dopo* l'inaugurazione), così non deve fare il conto da sola.
- **Il prestito diventa un'offerta concreta**, non un "se vuole": con data di consegna, modalità di ritiro e disponibilità ad aumentare il numero. È la parte che salva il rapporto, quindi merita spazio.
- **"Mi dispiace il doppio" → scuse una volta sola, all'inizio**, sul ritardo nello scrivere; poi il dispiacere sul merito. Ripetere le scuse sposta l'attenzione da lei al cliente in modo poco utile.
- **Chiusura con una richiesta d'azione** ("mi faccia sapere"), che facilita la risposta.

Se preferisce un tono più informale — immagino ci sia un rapporto consolidato — posso ammorbidirla; e se il prestito delle dodici sedie non è ancora certo, conviene formularlo al condizionale.

### A3 · Opus (opus)

**Versione riscritta**

> **Oggetto: Consegna sedie — nuova data: venerdì 16 ottobre**
>
> Buongiorno signora Carla,
>
> le scrivo con un giorno di ritardo, e me ne scuso: volevo darle una data certa prima di contattarla.
>
> Il nostro fornitore ha riscontrato un problema serio in fase di verniciatura e la consegna delle venti sedie slitta a **venerdì 16 ottobre**. So quanto contava di averle per l'inaugurazione di sabato 3 ottobre, e mi dispiace sinceramente che questo intoppo capiti proprio ora.
>
> Per non lasciarla scoperta le propongo una soluzione: posso portarle **dodici sedie nostre in prestito** già venerdì 2, così sabato ha comunque una sala allestita. Me le restituirà con comodo dopo il 16.
>
> Mi faccia sapere se le va bene e mi organizzo per il trasporto. Se preferisce sentirci a voce, mi chiami pure quando vuole.
>
> Un caro saluto,
> Giulia

**Cosa ho cambiato e perché**

- **«slitta davvero di poco» l'ho tolto.** Sono tredici giorni e l'inaugurazione salta: minimizzare rischia di irritare, perché è la cliente a decidere se è poco. Meglio la data nuda e le scuse.
- **«mi dispiace il doppio» → una formula più chiara.** L'originale è simpatico ma vago; ho legato il dispiacere al fatto concreto (l'inaugurazione).
- **Il ritardo nello scrivere diventa un motivo, non una colpa** («volevo darle una data certa»).
- **Il prestito passa da ripensamento a proposta strutturata**, con data di consegna e restituzione: così è una soluzione, non un favore buttato lì.
- **Aggiunto oggetto e call to action finale**, perché la mail chiede una risposta.

Un punto da valutare: dodici sedie su venti coprono il 60%. Se sa già che alla cliente ne servono di più, meglio dirlo esplicitamente («so che non bastano, ma è quanto riesco a liberare») piuttosto che lasciarglielo scoprire sabato.

### A4 · Opus (opus)

**Oggetto: Consegna sedie – nuova data e una soluzione per l'inaugurazione**

Gentile signora Carla,

le scrivo con un giorno di ritardo rispetto a quanto avrei voluto, e me ne scuso.

Il nostro fornitore ha riscontrato un problema serio nella fase di verniciatura: le venti sedie arriveranno venerdì 16 ottobre. So che le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace davvero — è un contrattempo che cade nel momento peggiore.

Per non lasciarla scoperta, le propongo questo: posso portarle io dodici sedie delle nostre, in prestito, consegnandole entro venerdì 2 ottobre così da averle in sala per l'inaugurazione. Al ritiro penso io, senza alcun costo per lei.

Mi faccia sapere entro lunedì se le va bene, così organizzo il trasporto.

Un caro saluto,
Giulia

---

**Cosa ho cambiato e perché**

- **Tolto «slitta davvero di poco»**: sono tredici giorni *dopo* l'inaugurazione. Minimizzare un ritardo che il cliente vedrà benissimo indebolisce la credibilità di tutto il resto della mail.
- **Tolto «mi dispiace il doppio»**: suona come una formula. Meglio dire concretamente *perché* dispiace (cade nel momento peggiore).
- **Messo in evidenza il rimedio**: nell'originale il prestito delle dodici sedie arrivava in fondo, quasi come un ripensamento («se vuole»). È la parte più importante della mail: va trattata come una proposta seria, con data di consegna, ritiro e gratuità esplicitati.
- **Aggiunta una richiesta di risposta con scadenza**: altrimenti la palla resta in aria e rischiate di arrivare a mercoledì senza decisione.
- **Aggiunto un oggetto** che anticipa sia il problema sia il fatto che esiste una soluzione.

Se conosce il cognome della signora, «Gentile signora [Cognome]» è più appropriato in un rapporto commerciale; «signora Carla» va bene solo se vi date già confidenza così.

### A5 · Opus (opus)

**Oggetto: Consegna sedie – nuova data e una soluzione per sabato 3**

Gentile signora Carla,

le scrivo con un giorno di ritardo rispetto a quanto avrei voluto, e me ne scuso.

Il nostro fornitore ha riscontrato un problema serio nella fase di verniciatura e questo ci costringe a riprogrammare la consegna: le venti sedie arriveranno **venerdì 16 ottobre**.

So quanto contasse averle per l'inaugurazione di sabato 3 ottobre, e mi dispiace davvero: è una data che non si sposta.

Proprio per questo le propongo una soluzione. Posso portarle **dodici sedie delle nostre in prestito**, consegnate venerdì 2 ottobre e ritirate quando le sue saranno arrivate. Se dodici non bastano, mi dica di quante avrebbe bisogno e vedo cosa riesco a recuperare.

Mi faccia sapere entro lunedì 28 settembre così organizzo il trasporto. Per qualsiasi cosa sono a sua disposizione.

Un cordiale saluto,
Giulia

---

**Cosa ho cambiato e perché**

- **Tolto "slitta davvero di poco".** Il ritardo è di tredici giorni e salta l'inaugurazione: minimizzarlo rischia di irritare, non di rassicurare. Meglio dire la data e basta.
- **Data nuova subito, in evidenza.** Era l'informazione più importante e arrivava in fondo.
- **"Mi dispiace il doppio" → scusa singola e concreta.** Una scusa chiara pesa più di una enfatizzata.
- **Il prestito diventa una proposta strutturata**, non un ripiego buttato lì: data di consegna, ritiro, e apertura a trovarne altre (dodici su venti potrebbero non bastare).
- **Aggiunta una scadenza per la risposta**, altrimenti la cosa resta sospesa proprio nei giorni in cui serve muoversi.
- **Aggiunto l'oggetto**, che orienta subito alla lettura.

Un'ultima nota: se il rapporto è formale, "Gentile signora Cognome" (o il suo cognome) funziona meglio di "signora Carla", che mescola registri.

### A6 · Sonnet (sonnet)

Buongiorno signora Carla,

avrei voluto scriverle già ieri, ma preferivo darle una comunicazione precisa. Il nostro fornitore ha riscontrato un problema serio nella fase di verniciatura, e siamo costretti a riprogrammare la consegna. Il ritardo sarà comunque contenuto: le venti sedie arriveranno venerdì 16 ottobre.

So che le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace molto per il disagio. Per non lasciarla scoperta, sabato posso portarle io dodici sedie della nostra dotazione, in prestito, fino all'arrivo dell'ordine.

Se la soluzione le va bene, mi dica pure e organizzo il trasporto. Resto a sua disposizione per qualsiasi necessità.

Un cordiale saluto,
Giulia

---

**Cosa ho cambiato:**
- **"Slitta davvero di poco"**: tra il 3 e il 16 ottobre ci sono più di due settimane, quindi ho scritto "contenuto", che è più onesto e meno rischioso.
- **"Mi dispiace il doppio"**: sostituito con un'espressione più professionale.
- **Ordine delle informazioni**: prima il problema, poi la nuova data, poi la soluzione, così la mail si legge in modo lineare.
- **Prestito**: ho aggiunto una chiusura che invita a rispondere, così la proposta diventa operativa.
- **Punto da verificare**: le sedie in prestito sono dodici e quelle ordinate venti. Se all'inaugurazione ne servono di più, conviene dirlo alla signora Carla o valutare se ne avete altre.

### A7 · Sonnet (sonnet)

Ecco una versione migliorata, più chiara e cordiale:

**Oggetto: Aggiornamento sulla consegna delle sedie**

Buongiorno signora Carla,

avrei voluto scriverle già ieri, e mi scuso per il ritardo nel comunicarle questa notizia.

Il nostro fornitore ha riscontrato dei problemi nella fase di verniciatura, per cui siamo costretti a riprogrammare la consegna. Lo slittamento è contenuto: le venti sedie arriveranno venerdì 16 ottobre.

So che le aspettava per l'inaugurazione di sabato 3 ottobre e me ne dispiaccio sinceramente. Per non lasciarla in difficoltà, se lo desidera posso portarle io per sabato dodici delle nostre sedie in prestito, così da avere comunque i posti a sedere per l'evento.

Mi faccia sapere se la soluzione le è utile, e nel caso ci accordiamo sull'orario della consegna.

Un cordiale saluto,
Giulia

---

**Cosa ho cambiato:**
- **Tono più sicuro:** ho tolto "molto seri" e "davvero di poco", che si contraddicevano e creavano ansia senza informare.
- **Notizia in evidenza:** la nuova data è ora ben visibile.
- **Data e giorno:** una nota, il 16 ottobre 2026 cade di venerdì e il 3 ottobre di sabato, quindi le date sono coerenti.
- **Proposta concreta:** ho aggiunto un invito a rispondere, così la soluzione del prestito si chiude in fretta.

Una nota: lo slittamento è di due settimane, quindi "di poco" potrebbe non essere percepito così dalla signora. Ho preferito "contenuto", ma se preferisce può indicare direttamente "due settimane dopo".

### A8 · Sonnet (sonnet)

Ecco una versione migliorata: più chiara, diretta e cordiale.

**Oggetto:** Ritardo nella consegna delle sedie – proposta per l'inaugurazione

Buongiorno signora Carla,

avrei voluto scriverle già ieri, ma ho preferito aspettare di avere un quadro più preciso. Purtroppo il nostro fornitore ha riscontrato dei problemi nella fase di verniciatura, e siamo costretti a rinviare la consegna.

Le venti sedie arriveranno venerdì 16 ottobre, quindi con circa due settimane di ritardo. So che le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace sinceramente per il disagio.

Per non lasciarla senza posti a sedere, posso portarle io dodici delle nostre sedie in prestito già per sabato 3. Mi faccia sapere se la soluzione le è utile e mi organizzo di conseguenza.

Resto a disposizione per qualsiasi necessità.

Un cordiale saluto,
Giulia

**Cosa ho cambiato:**
- **Ritardo quantificato:** nell'originale «slitta di poco» era vago e poco credibile, visto che si tratta di due settimane. Dirlo chiaramente ispira più fiducia.
- **Tono:** ho tolto «problemi molto seri» e «mi dispiace il doppio», che suonavano allarmanti o colloquiali, e ho usato un dispiacere più sobrio.
- **Proposta concreta:** il prestito delle sedie è ora presentato come soluzione, con un invito a rispondere.
- **Oggetto:** aggiunto, per far capire subito di cosa si tratta.

Nota: ho scritto «avrei voluto scriverle già ieri, ma ho preferito aspettare di avere un quadro più preciso». Se non è il vero motivo, modifica o elimina la frase.

### A9 · Sonnet (sonnet)

**Oggetto: Ritardo nella consegna delle sedie e soluzione per l'inaugurazione**

Buongiorno signora Carla,

avrei voluto scriverle già ieri, e mi scuso per non averlo fatto. Il nostro fornitore ha riscontrato un problema nella fase di verniciatura, e la consegna delle sedie subirà quindi un ritardo.

So che le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace molto per il disagio. Le venti sedie arriveranno venerdì 16 ottobre.

Per non lasciarla in difficoltà, posso portarle sabato dodici sedie del nostro showroom in prestito, così da avere comunque i posti necessari per l'evento. Mi dica pure se le fa piacere e a che ora preferisce che passi.

Resto a disposizione per qualsiasi esigenza.

Un cordiale saluto,
Giulia

---

**Cosa ho cambiato:**
- **Coerenza:** "problemi molto seri" e "slitta di poco" si contraddicevano. Inoltre due settimane non sono poche per chi ha un'inaugurazione. Ho tolto il minimizzare e ho lasciato solo i fatti.
- **Scuse più naturali:** "mi dispiace il doppio" suonava strano, quindi l'ho sostituito con "mi dispiace molto per il disagio".
- **Proposta concreta:** ho reso più chiara l'offerta delle dodici sedie e ho chiesto una conferma con l'orario.
- **Oggetto:** l'ho aggiunto, così la mail si capisce subito.

Ho scritto "showroom" al posto di "delle nostre" per esempio, ma va corretto se le sedie in prestito vengono da un altro posto. Le date sono giuste: il 3 ottobre 2026 è un sabato e il 16 ottobre è un venerdì.

### A10 · Sonnet (sonnet)

Ecco una versione migliorata, più chiara e cordiale:

**Oggetto:** Aggiornamento sulla consegna delle sedie

Buongiorno signora Carla,

avrei voluto scriverle già ieri, e mi scuso per non averlo fatto prima.

Purtroppo il nostro fornitore ha riscontrato dei problemi nella fase di verniciatura, e dobbiamo quindi riprogrammare la consegna. Le venti sedie arriveranno venerdì 16 ottobre.

So che le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace davvero molto per il disagio. Per non lasciarla senza, se lo desidera posso portarle io per sabato 3 ottobre dodici sedie delle nostre, in prestito, fino all'arrivo dell'ordine.

Resto a disposizione per qualsiasi necessità.

Un cordiale saluto,
Giulia

---

**Cosa ho cambiato:**
- **Tolto "slitta davvero di poco":** dal 3 al 16 ottobre sono più di due settimane, e per un'inaugurazione non è poco. Minimizzare rischia di irritare la cliente.
- **Tolto "molto seri":** i dettagli del problema non servono e creano allarme; conta la nuova data.
- **Ordine più logico:** problema, nuova data, scuse, soluzione.
- **"Mi dispiace il doppio"** sostituito con una formula più professionale.
- **Precisata la data del prestito** (sabato 3 ottobre), così non ci sono ambiguità.

Nota: le sedie in prestito sono dodici, mentre l'ordine è di venti. Se vuole, può aggiungere se le altre otto servono o meno, oppure se può portarne di più.

## B · errore comune («mantenendo il mio stile»)

**Richiesta:**

> Migliora questa mail mantenendo il mio stile. «Buongiorno signora Carla, in realtà volevo scriverle già ieri. Purtroppo sono stati riscontrati dei problemi molto seri dal nostro fornitore nella fase di verniciatura, e quindi dobbiamo procedere a una riprogrammazione della consegna, che sostanzialmente slitta davvero di poco. So che le sedie le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio. Le venti sedie arriveranno venerdì 16 ottobre. Se vuole, per sabato gliene porto io dodici delle nostre, in prestito. Un saluto, Giulia»

### B1 · Opus (opus)

Ecco la versione rivista, con lo stesso tono diretto e cordiale:

---

Buongiorno signora Carla,

in realtà volevo scriverle già ieri, ma preferivo prima avere una data certa da darle.

Il nostro fornitore ha riscontrato problemi seri nella fase di verniciatura, e questo ci costringe a riprogrammare la consegna: le venti sedie arriveranno **venerdì 16 ottobre**.

So che le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio: per il ritardo e per il momento in cui arriva.

Se le fa comodo, per sabato le porto io dodici sedie delle nostre, in prestito. Le monto e le ritiro con calma nei giorni successivi, senza nessun costo per lei. Mi faccia sapere entro la settimana e organizzo il trasporto.

Un saluto,
Giulia

---

**Cosa ho cambiato e perché**

- **Ho togliere il "slitta davvero di poco"**: tra il 3 e il 16 ottobre passano quasi due settimane, e attenuare il ritardo rischia di suonare poco sincero proprio nel momento in cui lei si trova senza sedie all'inaugurazione. Meglio dare la data secca e passare subito alla soluzione.
- **La data è ora in evidenza e anticipata**: era l'informazione che le interessa di più, ma arrivava in fondo.
- **Il "volevo scriverle ieri" ha una motivazione**: così non sembra un'esitazione, ma la scelta di non darle notizie a metà.
- **L'offerta delle dodici sedie è più concreta**: montaggio, ritiro, gratuità e una scadenza per la risposta. Come era formulata prima ("se vuole") rischiava di restare una cortesia che lei non si sentiva di accettare.

Se preferisce, posso prepararle anche una variante un po' più formale (nel caso il rapporto con la signora Carla sia più di lavoro che di conoscenza) oppure una più breve, da tre righe.

### B2 · Opus (opus)

**Versione rivista**

> **Oggetto: Sedie — nuova data di consegna e una soluzione per sabato**
>
> Buongiorno signora Carla,
>
> volevo scriverle già ieri, mi scuso per il ritardo.
>
> Il nostro fornitore ha riscontrato problemi seri nella fase di verniciatura e purtroppo dobbiamo riprogrammare la consegna: le venti sedie arriveranno **venerdì 16 ottobre**.
>
> So che le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio.
>
> Per non lasciarla scoperta: se vuole, sabato le porto io dodici delle nostre sedie, in prestito. Mi faccia sapere entro mercoledì così mi organizzo con il trasporto.
>
> Un saluto,
> Giulia

**Cosa ho cambiato e perché**

- **Tolto «slitta davvero di poco».** È la frase più rischiosa della mail: la consegna arriva *dopo* l'inaugurazione, quindi minimizzare suona come se non avesse capito il problema. Meglio dare la data e basta — è l'unica cosa che le interessa davvero.
- **Data nuova subito dopo il problema**, non tre righe più in fondo.
- **La soluzione ha una riga tutta sua** («per non lasciarla scoperta»): era la parte migliore della mail ma si perdeva in coda, quasi come un ripensamento.
- **Aggiunta una scadenza per la risposta** — senza, il prestito resta un'offerta vaga e lei deve ricordarsi di richiamarla. Cambi pure la data se mercoledì è troppo stretto.
- **Mantenuti** il suo tono diretto, il «mi dispiace il doppio» (onesto e personale, funziona) e la chiusura asciutta.

Se preferisce una versione ancora più breve, o vuole aggiungere un gesto di compensazione (sconto sul trasporto, per esempio), me lo dica e la riscrivo.

### B3 · Opus (opus)

Ecco la versione rivista — stessa voce (diretta, cordiale, un po' informale), ma più chiara e più solida sulle cose che contano.

---

**Oggetto: Consegna sedie — nuova data e una proposta per sabato**

Buongiorno signora Carla,

volevo scriverle già ieri, e mi scuso per il ritardo.

Il nostro fornitore ha riscontrato problemi seri in fase di verniciatura e dobbiamo riprogrammare la consegna: le venti sedie arriveranno **venerdì 16 ottobre**.

So bene che le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace doppiamente: per il disguido in sé e per il momento in cui capita.

Per non lasciarla scoperta sabato, le propongo questo: le porto io dodici sedie delle nostre, in prestito, così l'inaugurazione si fa comunque. Me lo confermi e organizzo la consegna in tempo per l'allestimento.

Resto a disposizione per qualsiasi cosa.

Un saluto,
Giulia

---

**Cosa ho cambiato e perché**

- **Tolto "slitta davvero di poco".** Dal 3 al 16 ottobre passano quasi due settimane, e la consegna arriva *dopo* l'inaugurazione: minimizzare rischia di suonare poco sincero e di irritare. Meglio dare la data e passare subito alla soluzione.
- **Data in evidenza.** È l'informazione che la signora Carla cerca leggendo: va trovata al primo colpo d'occhio.
- **Il prestito diventa una proposta concreta**, non un "se vuole" buttato lì. Chiude con una richiesta d'azione chiara (una conferma), che è il modo più rapido per risolvere.
- **Aggiunto un oggetto**, che già dalla casella dice problema + rimedio.
- **Mantenuto il suo stile:** frasi brevi, tono personale, "mi dispiace doppiamente", nessun burocratese.

Se preferisce una versione ancora più asciutta o un po' più formale (magari con il "lei" più distaccato), la preparo volentieri.

### B4 · Opus (opus)

Ecco la mail rivista, con lo stesso tono diretto e caldo dell'originale:

---

**Oggetto: Consegna sedie — nuova data e una proposta per sabato**

Buongiorno signora Carla,

volevo scriverle già ieri, e mi scuso per il ritardo.

Il nostro fornitore ha riscontrato dei problemi seri nella fase di verniciatura e siamo costretti a riprogrammare la consegna: le venti sedie arriveranno **venerdì 16 ottobre**.

So bene che le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace doppiamente.

Nel frattempo, se le fa comodo, per sabato posso portarle io dodici delle nostre in prestito: così l'inaugurazione non ne risente. Mi dica pure e organizzo tutto.

Un saluto,
Giulia

---

**Cosa ho cambiato e perché:**

- **Ho tolto «slitta davvero di poco».** Tra il 3 e il 16 ottobre passano quasi due settimane: minimizzare rischia di irritare chi ha un'inaugurazione da salvare. Meglio dare subito la data nuova, in chiaro, e passare alla soluzione.
- **La data nuova sale in alto e in grassetto**, così è la prima cosa che si legge.
- **La proposta del prestito diventa una vera offerta operativa** («mi dica pure e organizzo tutto»), non un'ipotesi buttata lì: è il punto forte della mail, quello che trasforma un disguido in un gesto di cura.
- **Oggetto esplicito**, che anticipa sia il problema sia il fatto che c'è una soluzione.
- Piccole limature: «mi dispiace doppiamente» al posto di «mi dispiace il doppio», e le scuse iniziali che chiudono il riferimento a «volevo scriverle già ieri».

Se preferisce una versione ancora più asciutta, o al contrario più formale (con il «Gentile Signora» e il «Cordiali saluti»), me lo dica e la adatto.

### B5 · Opus (opus)

Ecco la mail rivista — stesso tono diretto e caldo, solo con l'informazione principale messa più in evidenza e qualche passaggio più asciutto.

---

**Oggetto: Consegna sedie — nuova data (venerdì 16 ottobre)**

Buongiorno signora Carla,

volevo scriverle già ieri, e mi dispiace non averlo fatto.

Il nostro fornitore ha riscontrato dei problemi seri nella fase di verniciatura, e questo ci costringe a riprogrammare la consegna: le venti sedie arriveranno **venerdì 16 ottobre**.

So che le aspettava per l'inaugurazione di sabato 3 ottobre, e per questo mi dispiace il doppio.

Una soluzione però ce l'ho: per sabato posso portarle io dodici delle nostre, in prestito. Se le va bene, me lo faccia sapere e organizzo tutto senza che lei debba pensarci.

Un saluto,
Giulia

---

**Cosa ho cambiato e perché:**

- **Ho tolto "slitta davvero di poco".** Dal 3 al 16 ottobre passano quasi due settimane: minimizzare rischia di irritare la signora Carla nel momento stesso in cui legge la nuova data. Meglio dire la cosa e passare subito alla soluzione.
- **Ho anticipato la data nuova**, anche nell'oggetto: è l'informazione che lei cerca per prima.
- **Ho reso il prestito una proposta concreta** invece di un "se vuole" un po' timido — è il suo punto di forza, vale la pena valorizzarlo.
- **Ho tenuto** "mi dispiace il doppio" e il registro colloquiale: sono suoi e funzionano.

Se preferisce una versione ancora più breve, o al contrario con una riga in più sul perché del ritardo, la preparo volentieri.

### B6 · Sonnet (sonnet)

Ecco una versione rifinita, che mantiene il tono cordiale e diretto:

**Oggetto:** Consegna sedie: aggiornamento

Buongiorno signora Carla,

avrei voluto scriverle già ieri. Purtroppo il nostro fornitore ha riscontrato dei problemi molto seri nella fase di verniciatura, quindi dobbiamo riprogrammare la consegna. Le venti sedie arriveranno venerdì 16 ottobre.

So che le aspettava per l'inaugurazione di sabato 3 ottobre, e questo dispiace doppiamente anche a me. Per non lasciarla in difficoltà, se vuole sabato le porto io dodici delle nostre sedie in prestito.

Mi faccia sapere se le va bene, così organizzo tutto.

Un saluto,
Giulia

**Cosa ho cambiato:**
- Ho tolto "slitta davvero di poco". Il ritardo è di due settimane e la signora Carla potrebbe non essere d'accordo. Meglio dare la data e lasciarle giudicare.
- Ho aggiunto una chiusura che chiede una risposta, perché l'offerta delle sedie in prestito richiede una conferma.
- Ho snellito qualche passaggio ("in realtà", "sostanzialmente") per rendere il testo più scorrevole, senza perdere il tono personale.

Se preferisce che il ritardo sembri meno grave, posso proporre una versione che lo minimizzi senza essere scorretta.

### B7 · Sonnet (sonnet)

**Versione migliorata**

Buongiorno signora Carla,

avrei voluto scriverle già ieri. Purtroppo il nostro fornitore ha riscontrato dei problemi molto seri nella fase di verniciatura, quindi dobbiamo riprogrammare la consegna. Le venti sedie arriveranno venerdì 16 ottobre.

So che le aspettava per l'inaugurazione di sabato 3 ottobre, e questo mi dispiace ancora di più. Se le fa piacere, per sabato le porto io dodici delle nostre sedie in prestito, così può essere tranquilla per l'evento.

Resto a disposizione per qualsiasi cosa.

Un saluto,
Giulia

**Cosa ho cambiato**
- Ho tolto "slitta davvero di poco". Dal 3 al 16 ottobre passano due settimane, e la signora Carla potrebbe non essere d'accordo. Meglio dare la data e lasciare che sia lei a giudicare.
- "Mi dispiace il doppio" l'ho reso con "mi dispiace ancora di più", che è più naturale ma ha lo stesso tono.
- Ho ordinato i contenuti in questo modo: prima il motivo, poi la nuova data, poi la soluzione. Così la proposta del prestito risulta più evidente.
- Ho aggiunto una riga di chiusura, "Resto a disposizione...", per un tono più cordiale.

Se preferisce un tono più diretto e asciutto, posso preparare anche una versione più breve.

### B8 · Sonnet (sonnet)

**Oggetto: Consegna delle sedie: aggiornamento**

Buongiorno signora Carla,

in realtà volevo scriverle già ieri. Purtroppo il nostro fornitore ha riscontrato dei problemi molto seri nella fase di verniciatura, quindi dobbiamo riprogrammare la consegna.

So che aspettava le sedie per l'inaugurazione di sabato 3 ottobre, e mi dispiace doppiamente. Le venti sedie arriveranno venerdì 16 ottobre.

Per non lasciarla scoperta, se vuole sabato le porto io dodici delle nostre, in prestito.

Mi faccia sapere e mi organizzo di conseguenza.

Un saluto,
Giulia

---

Ho tolto "slitta davvero di poco" perché tra il 3 e il 16 ottobre passano due settimane. La signora Carla potrebbe non essere d'accordo, e con il ritardo che minimizza si rischia di sembrare poco sensibili. Se preferisce mantenere quel tono più rassicurante, può scrivere "il ritardo è contenuto", ma io eviterei.

### B9 · Sonnet (sonnet)

**Versione migliorata**

Buongiorno signora Carla,

in realtà volevo scriverle già ieri. Purtroppo il nostro fornitore ha riscontrato dei problemi molto seri nella fase di verniciatura, e dobbiamo quindi riprogrammare la consegna.

So che aspettava le sedie per l'inaugurazione di sabato 3 ottobre, e per questo mi dispiace ancora di più. Le venti sedie arriveranno venerdì 16 ottobre.

Se le fa comodo, per sabato posso portarle io dodici delle nostre in prestito, così per l'inaugurazione è a posto.

Un saluto,
Giulia

**Cosa ho cambiato**
- Ho tolto "slitta davvero di poco". Due settimane di ritardo non sono poche per chi aveva una data precisa, e la frase rischia di sembrare minimizzante. Se preferisce mantenerla, potrebbe scrivere "il ritardo è contenuto".
- Ho reso il tono un po' più diretto ("sostanzialmente" e "in realtà" appesantivano la frase).
- Ho riformulato "mi dispiace il doppio" in "mi dispiace ancora di più", che suona un po' più curato ma resta colloquiale.
- Ho aggiunto "così per l'inaugurazione è a posto" per chiudere l'offerta in modo rassicurante.

Se vuole una versione ancora più vicina all'originale o più formale, la preparo volentieri.

### B10 · Sonnet (sonnet)

Buongiorno signora Carla,

in realtà avrei voluto scriverle già ieri. Purtroppo il nostro fornitore ha riscontrato dei problemi molto seri nella fase di verniciatura, e dobbiamo quindi riprogrammare la consegna, che comunque slitta di pochissimo.

So che aspettava le sedie per l'inaugurazione di sabato 3 ottobre, e questo mi dispiace doppiamente. Le venti sedie arriveranno venerdì 16 ottobre.

Se le fa comodo, per sabato 3 posso portarle io dodici delle nostre, in prestito.

Un saluto,
Giulia

---

Note sulle modifiche:
- Ho corretto la data ambigua: "sabato" diventa "sabato 3", così non c'è dubbio su quale sabato si intenda.
- Ho evitato la frase "problemi molto seri… slitta davvero di poco", che stonava un po' (seri ma di poco). Ho lasciato "molto seri" perché è nel suo stile, ma se preferisce un tono più rassicurante può usare "problemi imprevisti".
- Una precisazione: la consegna slitta di due settimane e mezzo, non proprio "di pochissimo". Se vuole, può togliere "di pochissimo" per non sminuire il ritardo.

## C · la mossa (i problemi, non le parole)

**Richiesta:**

> Non migliorare questa mail: elencami i problemi, senza riscrivere niente. «Buongiorno signora Carla, in realtà volevo scriverle già ieri. Purtroppo sono stati riscontrati dei problemi molto seri dal nostro fornitore nella fase di verniciatura, e quindi dobbiamo procedere a una riprogrammazione della consegna, che sostanzialmente slitta davvero di poco. So che le sedie le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio. Le venti sedie arriveranno venerdì 16 ottobre. Se vuole, per sabato gliene porto io dodici delle nostre, in prestito. Un saluto, Giulia»

### C1 · Opus (opus)

# Problemi della mail

**1. "in realtà volevo scriverle già ieri"**
Apertura che non aggiunge nulla e anzi ammette un ritardo nella comunicazione. Sposta l'attenzione su di te invece che sul problema della cliente.

**2. "sono stati riscontrati dei problemi... dal nostro fornitore"**
Passivo + scarico di responsabilità. La cliente ha un contratto con te, non con il fornitore. Meglio assumersi la cosa in prima persona.

**3. "slitta davvero di poco"**
È falso e si smaschera due righe dopo: dal 3 al 16 ottobre sono quasi due settimane, e per di più *dopo* l'inaugurazione. Minimizzare un danno che la cliente vedrà subito nei numeri suona come presa in giro e mina la credibilità di tutto il resto.

**4. Ordine delle informazioni sbagliato**
La data nuova (16 ottobre) — il dato che la cliente cerca — arriva solo al quarto periodo, dopo preamboli e scuse. Dovrebbe essere subito.

**5. "mi dispiace il doppio"**
Espressione vaga e un po' leziosa. Non dice nulla di concreto.

**6. Manca il riconoscimento esplicito del vero problema**
L'inaugurazione di sabato 3 resta senza sedie. La mail lo sfiora ("so che le aspettava per...") ma non lo affronta: non c'è una frase che dica apertamente "sabato lei resta scoperta".

**7. La soluzione è messa come un ripensamento**
"Se vuole, per sabato gliene porto io dodici delle nostre, in prestito" — è la parte più utile di tutta la mail, ma è buttata lì in fondo, condizionale, quasi timida. Ed è la cosa che salva il rapporto.

**8. Dodici contro venti: il divario non è nominato**
Mancano 8 sedie e nessuno lo dice. La cliente deve fare il conto da sola e scoprire il buco. Meglio dichiararlo e, se possibile, proporre come coprirlo.

**9. Nessuna richiesta di risposta né tempi**
"Se vuole" non ha una scadenza. Per organizzare il prestito serve sapere entro quando decidere, e chi fa cosa (consegna, ritiro, orari).

**10. Nessun accenno a compensazione o garanzia**
Un ritardo di questa portata su un evento di solito richiede almeno un gesto: sconto, priorità, penale, o quantomeno una conferma ferma che il 16 è una data certa e non un'altra stima.

**11. "Le venti sedie arriveranno venerdì 16 ottobre"**
Detto come un fatto neutro, senza indicare *perché* stavolta la data è affidabile. Dopo uno slittamento, una data nuda non rassicura.

**12. Registro incerto**
"Buongiorno signora Carla" (informale, nome di battesimo) convive con "procedere a una riprogrammazione della consegna" (burocratico). E la chiusura "Un saluto, Giulia" è sbrigativa per una mail che comunica un disservizio.

**13. Oggetto assente**
Non c'è riga oggetto. Su una comunicazione urgente come questa, è ciò che determina se viene letta oggi o venerdì.

### C2 · Opus (opus)

Ecco i problemi, in ordine di gravità.

## Sostanza e credibilità

- **"slitta davvero di poco" è falso.** Da sabato 3 a venerdì 16 ottobre ci sono tredici giorni, ed è quasi peggio il fatto che la nuova data cada *dopo* l'evento. Minimizzare così espone al rischio di sembrare in malafede, non rassicurante.
- **Contraddizione interna:** "problemi molto seri" e "slitta davvero di poco" non possono stare nella stessa mail. O la cosa è grave o è irrilevante.
- **Il punto centrale non è mai detto.** Non c'è nessuna frase che dica "le sedie non ci saranno per l'inaugurazione". La destinataria deve arrivarci da sola confrontando due date messe a distanza di righe.
- **Nessuna garanzia sulla nuova data.** Una previsione è già saltata; il 16 ottobre viene dato per certo senza spiegare perché stavolta dovrebbe reggere.
- **Il buco delle otto sedie mancanti è ignorato.** Ne servono venti, se ne offrono dodici in prestito e la differenza non viene nominata, né si propone un'alternativa (noleggio, consegna parziale del fornitore, altro).

## Struttura e gerarchia delle informazioni

- **L'incipit parla di chi scrive, non della cliente.** "In realtà volevo scriverle già ieri" confessa un ritardo nella comunicazione, non lo giustifica e non lo scusa: parte in debito.
- **La notizia utile — la data nuova — arriva quarta**, dopo premesse, giustificazioni tecniche e dispiaceri.
- **La soluzione, cioè la parte davvero preziosa, è relegata in coda** e introdotta da un "se vuole" che la fa sembrare un ripiego imbarazzato invece che un rimedio concreto.
- **Nessuna richiesta di risposta.** Manca un "mi faccia sapere entro X", e manca qualsiasi recapito per una replica urgente.

## Responsabilità e scuse

- **Passivo + scaricabarile:** "sono stati riscontrati dei problemi... dal nostro fornitore". Nessuno è soggetto della frase. Per la cliente il fornitore non esiste: il contratto è con chi scrive.
- **"Mi dispiace il doppio" non è una scusa**, è un modo di dire vago e un po' infantile. Non compare mai un "mi scuso".
- **"Dobbiamo procedere a una riprogrammazione"** presenta una decisione unilaterale già chiusa, senza chiedere nulla e senza offrire opzioni.
- **Nessun gesto riparatorio** oltre al prestito: niente sconto, niente omaggio, niente riconoscimento del danno a un'inaugurazione.

## Lingua e tono

- **Riempitivi e attenuatori a raffica:** "in realtà", "purtroppo", "sostanzialmente", "davvero", "molto seri". Tolti quelli, resta metà mail.
- **Burocratese inutile:** "procedere a una riprogrammazione della consegna" al posto di "la consegna slitta".
- **Dettaglio tecnico irrilevante** ("fase di verniciatura") mentre mancano i dettagli che servono: se il 16 è arrivo in magazzino o consegna a destinazione, quando e dove arriverebbero le sedie in prestito, per quanto tempo, a che titolo (gratuite?).
- **Registro ibrido e incoerente:** "signora Carla" mescola formale e confidenziale; la firma è un "Giulia" secco, senza cognome, ruolo, azienda.
- **Nessun riferimento all'ordine** (numero, modello, conferma d'ordine) e — per quanto si vede — nessun oggetto che anticipi il contenuto.

Il difetto che li riassume tutti: la mail è scritta per gestire l'imbarazzo di chi la manda, non il problema di chi la riceve.

### C3 · Opus (opus)

## Struttura e ordine delle informazioni

- **La notizia principale non è mai detta in chiaro.** Da nessuna parte c'è scritto "sabato 3 le sedie non ci saranno": il cliente deve dedurlo incrociando due date. Il fatto più grave è lasciato implicito.
- **Apertura sprecata.** "In realtà volevo scriverle già ieri" è la prima cosa che legge Carla: ammette un ritardo, non lo spiega, non se ne scusa e rinvia il contenuto vero. Se non aggiunge nulla, va tolta; se un giorno di ritardo conta, va giustificata.
- **La nuova data e la soluzione arrivano in fondo**, dopo la spiegazione tecnica. L'ordine utile è: cosa succede → cosa faccio io per rimediare → perché è successo.
- **Manca un riferimento all'ordine** (numero, data, conferma) e un oggetto che segnali l'urgenza.

## Tono e credibilità

- **Contraddizione interna:** "problemi molto seri" + "slitta davvero di poco". O è serio o è poco: le due cose insieme fanno sembrare che si stia minimizzando in malafede.
- **"Slitta davvero di poco" è falso dal punto di vista del cliente.** Sono 13 giorni e soprattutto è dall'altra parte dell'evento. Per Carla non è uno slittamento: è un'inaugurazione senza sedie.
- **Passivo deresponsabilizzante:** "sono stati riscontrati dei problemi… dal nostro fornitore". Il cliente ha un rapporto con Giulia, non col fornitore. Scaricare a monte indebolisce, non protegge.
- **"Mi dispiace il doppio" non è una scusa** ed è anche ambiguo (doppio rispetto a cosa? al ritardo della mail? al disagio?). Manca un "mi scuso" esplicito.
- **Nessun riconoscimento concreto delle conseguenze**: ospiti, foto, un locale che apre vuoto. L'empatia si ferma a "so che le aspettava".
- **Burocratese fuori registro:** "procedere a una riprogrammazione della consegna" in una mail che altrove è colloquiale.

## Buchi operativi (i più costosi)

- **Ammanco di 8 sedie non nominato.** Ne servono 20, se ne offrono 12. Il problema resta lì, e la mail non dice né come coprirlo né che se ne sta occupando.
- **Il prestito copre solo sabato.** Se l'attività apre il 3 e resta aperta, servono sedie anche dal 5 al 16. Durata del prestito non indicata.
- **Il prestito è tutto da definire:** modello, colore e stato estetico (decisivo per un'inaugurazione), chi consegna e a che ora, chi ritira, gratuito o no, chi risponde di eventuali danni.
- **"Se vuole…" scarica l'onere sul cliente.** Una soluzione va proposta come già organizzata, con un'alternativa, non come un favore che Carla deve avere l'iniziativa di accettare.
- **Nessuna richiesta di risposta entro una data**, benché ogni giorno perso riduca le chance di trovare un noleggio.
- **Nessuna garanzia sul 16 ottobre.** Perché quella data dovrebbe reggere, se non ha retto la precedente? Manca un impegno, una verifica fatta, un piano B.
- **Nessuna compensazione commerciale** (sconto, consegna gratuita, qualcosa sul prezzo): a fronte di un evento mancato, l'assenza è vistosa.
- **Consegna del 16 non specificata:** dove, a che ora, con che preavviso.
- **La verniciatura resta vaga:** non si capisce se il colore/finitura ordinato sarà rispettato o se cambierà qualcosa.
- **Canale probabilmente sbagliato:** una notizia così, a due settimane dall'evento, andava data per telefono e poi messa per iscritto. E comunque manca un recapito diretto per richiamare.

## Forma

- **"Signora Carla"**: titolo formale + nome di battesimo, registro incerto. E la firma è il solo "Giulia", senza cognome, ruolo, azienda, telefono.
- **"Un saluto"** è molto leggero per una comunicazione di disservizio.
- **"Le sedie le aspettava"** — ridondanza tollerabile nel parlato, stonata in una mail di scuse che dovrebbe risultare curata.

Nota di verifica: le date sono coerenti tra loro — nel 2026 il 3 ottobre cade di sabato e il 16 di venerdì. Lì non ci sono errori.

### C4 · Opus (opus)

Ecco i problemi, in ordine di gravità.

**1. Il punto centrale è mascherato.** «Slitta davvero di poco» è falso: dal 3 ottobre al 16 ottobre sono due settimane, e soprattutto il ritardo cade *dopo* l'evento. Non è uno slittamento piccolo, è un mancato appuntamento. Minimizzare così rischia di irritare più del ritardo stesso.

**2. La notizia arriva tardi e sepolta.** La data del 16 ottobre — l'unica informazione che conta davvero — compare a metà mail, dopo premesse, scuse e spiegazioni. Chi legge deve cercarla.

**3. L'apertura è autoreferenziale.** «In realtà volevo scriverle già ieri» parla del mittente, non della destinataria, e ammette un ritardo nella comunicazione senza spiegarlo né scusarsene davvero. Se non si è scritto ieri, dirlo peggiora soltanto.

**4. Passivo che nasconde la responsabilità.** «Sono stati riscontrati dei problemi... dal nostro fornitore»: costruzione contorta che scarica la colpa sul fornitore. Per la cliente il fornitore non esiste: la controparte è Giulia.

**5. Nessuna assunzione di responsabilità esplicita.** Manca una frase che dica chiaramente «me ne assumo la responsabilità» o anche solo «mi dispiace, è un mio problema da risolvere».

**6. «Mi dispiace il doppio» è vago e colloquiale.** Non si capisce quali siano le due ragioni. Suona come un riempitivo.

**7. La soluzione è proposta in modo troppo debole.** «Se vuole, per sabato gliene porto io dodici delle nostre, in prestito» è l'elemento più utile di tutta la mail ed è buttato lì come ripensamento, in fondo, introdotto da un «se vuole» che scarica la decisione sulla cliente. Andrebbe proposto con convinzione.

**8. Dodici contro venti: il divario non è affrontato.** Mancano otto sedie per l'inaugurazione e la mail non lo nomina. La cliente ci arriverà da sola, e si chiederà perché Giulia non ne abbia parlato.

**9. Nessuna operatività sul prestito.** Non si dice quando verrebbero consegnate, se sono compatibili con le altre, chi le ritira e quando, se c'è un costo. Restano tutte domande aperte.

**10. Nessuna garanzia sulla nuova data.** Dopo aver mancato una scadenza, dire «arriveranno venerdì 16» senza spiegare perché questa volta la data è sicura non rassicura.

**11. Nessuna richiesta di risposta né tempi.** La mail si chiude senza chiedere nulla, mentre l'evento è tra due settimane e una decisione sul prestito va presa in fretta.

**12. Registro incerto.** «Buongiorno signora Carla» mescola formale e confidenziale; «Un saluto» è sbrigativo per una mail che comunica un disservizio; non c'è oggetto, né recapito per un contatto diretto.

**13. Sbilanciamento generale.** Scuse e attenuanti occupano più spazio di fatti e rimedi. Il rapporto dovrebbe essere rovesciato.

### C5 · Opus (opus)

## Problemi di sostanza

1. **Il punto centrale non è mai detto.** Da nessuna parte c'è la frase "le sedie non ci saranno per l'inaugurazione". La cliente deve arrivarci da sola confrontando 3 ottobre e 16 ottobre. È l'informazione più importante della mail ed è l'unica lasciata implicita.
2. **"Slitta davvero di poco" è falso rispetto a ciò che conta.** Sono tredici giorni, ma soprattutto il ritardo cade *oltre* la data dell'evento: per la cliente non è "poco", è "troppo tardi". Il minimizzatore, per giunta rafforzato da "davvero", rischia di suonare come se chi scrive non avesse capito la gravità — o la stesse mascherando.
3. **La contraddizione interna è visibile.** "Problemi molto seri" + "slitta davvero di poco" non stanno in piedi insieme: o il problema è serio, o la conseguenza è trascurabile.
4. **La causa resta vaga e la nuova data non è garantita.** "Problemi nella fase di verniciatura" non dice nulla, e nulla assicura che il 16 ottobre sia una data solida e non un secondo rinvio in arrivo.
5. **La soluzione è sottodimensionata e non spiegata.** Dodici sedie su venti: ne mancano otto, e non lo si dice. Non si dice che sedie siano, se siano presentabili in un'inaugurazione, quando verrebbero portate, quando riprese, a che costo.
6. **Manca tutto il resto del rimedio.** Nessuna alternativa (noleggio, consegna parziale anticipata, reperimento altrove), nessuna forma di compensazione, nessuna assunzione di responsabilità per il disagio.
7. **Nessuna richiesta di risposta.** Non si chiede una conferma, non si indica entro quando serve saperlo — eppure per organizzare un prestito entro sabato una scadenza servirebbe.

## Problemi di struttura

8. **Ordine delle informazioni rovesciato.** Si apre con un preambolo irrilevante (volevo scriverle ieri), poi la causa, poi il commento minimizzante, e solo al quarto passaggio la data nuova. La conseguenza sull'evento e la proposta di soluzione finiscono in fondo.
9. **L'offerta delle dodici sedie sembra un ripensamento.** Collocata in coda e introdotta da "se vuole", ha il peso di un dettaglio, non di una soluzione d'emergenza.

## Problemi di tono e responsabilità

10. **Il passivo scarica la colpa.** "Sono stati riscontrati dei problemi dal nostro fornitore": il fornitore è un problema interno a chi scrive, la cliente ha un contratto con Giulia. La forma impersonale allontana la responsabilità proprio nel momento in cui andrebbe assunta.
11. **Manca una scusa esplicita.** "Mi dispiace il doppio" è colloquiale, impreciso (doppio rispetto a cosa?) e non equivale a "mi scuso".
12. **La mail è centrata su chi scrive.** Il mio ritardo nello scrivere, il mio fornitore, il mio dispiacere: il disagio della cliente — un'inaugurazione senza sedie — non viene mai nominato per quello che è.
13. **L'apertura è controproducente.** Ammettere di non aver scritto ieri, senza spiegarne il motivo né scusarsene, introduce un secondo ritardo di cui la cliente non aveva bisogno di sapere.

## Problemi di lingua

14. **Riempitivi e attenuatori.** "In realtà", "sostanzialmente", "davvero": tutti indeboliscono o allungano senza aggiungere.
15. **Burocratese.** "Dobbiamo procedere a una riprogrammazione della consegna" dove basterebbe un verbo semplice.
16. **Registro incoerente.** "Signora Carla" mescola formula formale e nome di battesimo; poi si scende a "gliene porto io", "un saluto".
17. **Firma incompleta.** Solo "Giulia": mancano cognome, ruolo, azienda, telefono — e nella mail non compare alcun riferimento d'ordine né, presumibilmente, un oggetto informativo.

### C6 · Sonnet (sonnet)

**Problemi della mail**

**Tono e coerenza**
- **Contraddizione centrale:** "problemi molto seri" e subito dopo "slitta davvero di poco". Il lettore non capisce se la situazione è grave o no.
- **Minimizzazione:** 3 → 16 ottobre sono 13 giorni e la cliente perde comunque l'inaugurazione. "Sostanzialmente" e "davvero di poco" suonano come se le si stesse togliendo importanza al disagio.
- **Scarico di responsabilità:** "sono stati riscontrati dei problemi… dal nostro fornitore" è impersonale e mette la colpa su un terzo. Alla cliente interessa il risultato, non chi ha sbagliato.
- **"Mi dispiace il doppio":** l'espressione è colloquiale e un po' leggera per una cattiva notizia. Inoltre non c'è una scusa esplicita per il ritardo.
- **Apertura difensiva:** "in realtà volevo scriverle già ieri" attira l'attenzione sul ritardo della comunicazione. Sembra una giustificazione e non aggiunge nulla di utile.

**Struttura**
- **Notizia principale in ritardo:** la data nuova arriva a metà testo, dopo giri di parole. Il testo è un unico blocco senza gerarchia.
- **Scuse in mezzo alla frase:** il dispiacere compare in un inciso, dopo la minimizzazione.
- **Dettagli inutili:** "fase di verniciatura" è un dettaglio tecnico che non serve alla cliente. Il motivo, invece, resta vago.
- **Gergo:** "riprogrammazione della consegna" è burocratico.

**Contenuto e affidabilità**
- **Promessa troppo netta:** "arriveranno venerdì 16 ottobre" è categorico, ma la mail dice che i problemi sono "molto seri". Non si dice se la data è confermata dal fornitore.
- **Nuova data senza contesto:** non si dice dove e a che ora arrivano le sedie, né se saranno consegnate e montate.
- **Offerta poco chiara:** "dodici delle nostre" copre solo 12 sedie su 20. Non si dice se bastano per l'inaugurazione o se sono simili a quelle ordinate ("delle nostre" è generico).
- **"Per sabato" ambiguo:** non è indicata la data (3 ottobre), e "sabato" può confondersi con la consegna del venerdì 16.
- **Logistica mancante:** non si dice quando le porta, chi le ritira dopo e cosa succede al momento della consegna definitiva.
- **Offerta passiva:** "Se vuole" lascia tutto alla cliente. Non c'è una scadenza per rispondere né un'azione richiesta.
- **Nessun gesto commerciale:** non c'è compensazione, sconto o altro riconoscimento del disagio.
- **Nessun passo successivo:** manca una proposta di telefonata o una richiesta di conferma. La mail si chiude senza chiarire cosa succede dopo.

**Forma**
- "Le sedie le aspettava" è una dislocazione tipica del parlato. Nello scritto professionale stona.
- Nell'insieme si mescolano registro formale ("signora Carla", "riscontrati") e colloquiale ("dispiace il doppio").
- Il saluto "Un saluto" è sbrigativo per una comunicazione negativa.
- La firma è solo "Giulia", senza cognome, ruolo o recapito.

### C7 · Sonnet (sonnet)

Problemi che vedo:

**Coerenza logica e fattuale**
1. **Date incoerenti col calendario:** il 3 ottobre 2026 è un sabato (corretto), ma il 16 ottobre 2026 è un venerdì (corretto). Le date quadrano, però il ritardo è di due settimane, quindi definire lo slittamento «davvero di poco» è una minimizzazione contraddetta dai fatti.
2. **Contraddizione tra «problemi molto seri» e «slitta di poco»:** i due toni si scontrano e la seconda affermazione appare poco credibile.
3. **«Sostanzialmente» e «davvero»:** attenuativi che indeboliscono ulteriormente il messaggio invece di chiarirlo.

**Tono e relazione col cliente**
4. **Inizio difensivo:** «in realtà volevo scriverle già ieri» suona come una giustificazione e lascia intendere un ritardo nella comunicazione, oltre a non aggiungere nulla di utile.
5. **«Mi dispiace il doppio»:** espressione poco chiara e informale (il doppio rispetto a cosa?). Le scuse arrivano tra l'altro dopo la notizia e in modo indiretto, senza un vero «mi scuso per il disagio».
6. **Attribuzione della colpa al fornitore:** scaricare la responsabilità su terzi dà un'impressione poco professionale; il cliente ha un rapporto con Giulia/la sua azienda, non con il fornitore.
7. **«Problemi molto seri» senza dettagli:** allarma senza spiegare; non è chiaro cosa sia successo, né se la nuova data sia certa.

**Struttura e chiarezza**
8. **Informazione chiave arrivata tardi:** la nuova data di consegna compare solo a metà, dopo giri di parole; conviene dichiarare subito il ritardo.
9. **Lessico burocratico:** «procedere a una riprogrammazione della consegna» è pesante e distante.
10. **Impatto sull'inaugurazione non affrontato bene:** «so che le aspettava per l'inaugurazione» ammette il danno ma non lo riconosce apertamente; il messaggio non dice esplicitamente che le sedie non ci saranno all'evento.
11. **Offerta di soluzione formulata debolmente:** «Se vuole» rende l'aiuto opzionale e quasi esitante. Manca inoltre chiarezza su: chi trasporta e ritira le sedie prestate, quando, e se sono equivalenti a quelle ordinate. Inoltre dodici su venti non coprono l'intero fabbisogno e non viene spiegato il perché.
12. **Nessuna garanzia sulla nuova data:** non è detto se il 16 ottobre sia confermato, né cosa succede in caso di ulteriori slittamenti.
13. **Nessuna proposta di compensazione:** sconto, rimborso o altro gesto commerciale non sono menzionati.
14. **Nessun invito a un contatto:** manca un'offerta di sentirsi per telefono o di confermare la ricezione.

**Forma**
15. **Registro misto:** «Buongiorno signora Carla» è formale, ma il resto è colloquiale («gliene porto io», «le nostre»).
16. **Chiusura sbrigativa:** «Un saluto» è secco dopo una notizia negativa; manca una formula più cortese e la disponibilità a chiarimenti.
17. **Paragrafo unico:** un blocco di testo unico rende difficile individuare le informazioni essenziali (nuova data, soluzione proposta).

### C8 · Sonnet (sonnet)

Ecco i problemi che vedo nella mail:

**Contenuto e coerenza**
- **Contraddizione sul ritardo:** dice che la consegna «slitta davvero di poco», ma si passa dal 3 al 16 ottobre, cioè oltre due settimane, e la consegna manca proprio all'inaugurazione. Minimizzare così può sembrare poco serio.
- **Il «di poco» è anche in contrasto con «problemi molto seri»:** i due giudizi si smentiscono.
- **Problemi «molto seri» senza spiegazione:** non si capisce cosa sia successo né perché il nuovo termine sia affidabile. Non c'è alcuna garanzia sulla data del 16 ottobre.
- **Scaricabarile sul fornitore:** «dal nostro fornitore» sposta la colpa senza assumersi la responsabilità verso la cliente.
- **Nessuna scusa vera:** «mi dispiace il doppio» è una formula un po' goffa e sproporzionata. Non è chiaro perché «il doppio», e suona quasi retorica.

**Informazioni mancanti o ambigue**
- **Nessuna certezza sulla proposta delle sedie:** «dodici delle nostre» sono meno delle venti ordinate. Non è detto se bastino per l'inaugurazione né se siano simili a quelle ordinate.
- **Mancano i dettagli pratici del prestito:** orario, luogo, ritiro a fine prestito, chi si occupa di eventuali danni.
- **Nessuna richiesta di risposta:** non chiede alla signora di confermare né dice entro quando serve la sua decisione.
- **Nessuna compensazione:** nessuno sconto o gesto commerciale per il disagio.
- **Data del 16 ottobre:** non è indicato l'orario né se sia una consegna o una spedizione.

**Tono e forma**
- **Attacco poco efficace:** «in realtà volevo scriverle già ieri» suona come una giustificazione e mette in luce il ritardo anche nella comunicazione. Inoltre la cattiva notizia arriva solo dopo questa premessa.
- **«Purtroppo… e quindi… che sostanzialmente…»:** frase lunga, con troppi incisi e un lessico burocratico («sono stati riscontrati», «riprogrammazione», «sostanzialmente»).
- **Forma impersonale:** «sono stati riscontrati» toglie soggetto e responsabilità.
- **«Se vuole»:** l'offerta è formulata in modo passivo e quasi svogliato, mentre dovrebbe essere presentata come soluzione concreta.
- **Registro incoerente:** si alternano formule molto formali («Buongiorno signora Carla», «riprogrammazione») e colloquiali («gliene porto io», «davvero di poco»).
- **Chiusura sbrigativa:** «Un saluto» è troppo secco dopo una notizia negativa. Manca inoltre l'invito a sentirsi per parlarne.
- **Manca l'oggetto** (se è un'email vera): non si vede, e per una comunicazione di questo tipo sarebbe utile.
- **Ripetizione:** «sedie» e «le venti sedie» ricorrono a breve distanza, e la frase «So che le sedie le aspettava per l'inaugurazione» risulta pesante con il doppio pronome.

### C9 · Sonnet (sonnet)

Ecco i problemi che vedo, senza riscrivere nulla:

**Contenuto e coerenza**
1. **"Slitta davvero di poco"**: dal 3 al 16 ottobre sono due settimane e la consegna salta l'inaugurazione. Minimizzare contraddice i fatti e può irritare la cliente.
2. **"Problemi molto seri" e "slitta di poco"** si contraddicono: se i problemi sono seri, il ritardo non dovrebbe essere lieve, oppure la gravità è esagerata.
3. **"Mi dispiace il doppio"**: espressione vaga e poco naturale, che suona come una formula. Non è chiaro doppio rispetto a cosa.
4. **"Sono stati riscontrati dei problemi"**: forma impersonale che evita la responsabilità e non spiega nulla di concreto. Il dettaglio sulla verniciatura è tecnico e non interessa alla cliente.
5. **Scarico di responsabilità sul fornitore**: dare la colpa a terzi risulta poco professionale, perché per la cliente il referente è la vostra azienda.

**Informazioni mancanti o poco chiare**
6. **Data di arrivo poco affidabile**: il 16 ottobre è dichiarato senza alcuna garanzia. Dopo un problema "molto serio" la cliente potrebbe dubitare che sarà rispettato.
7. **Non è chiaro se il 16 è la consegna alla cliente** o l'arrivo da voi.
8. **Il prestito delle sedie è formulato in modo condizionale e sbrigativo** ("se vuole"): non è chiaro se le sedie sono gratuite, chi si occupa del ritiro dopo, né quando le riprenderete. Inoltre dodici su venti non coprono il fabbisogno e non si dice come gestire le otto mancanti.
9. **Nessuna proposta di compensazione** (sconto, altro) né alcuna richiesta di conferma alla cliente.
10. **Mancano un invito a rispondere e un'azione successiva** (ad esempio, quando la sentirete).

**Tono e stile**
11. **"In realtà volevo scriverle già ieri"**: introduce una giustificazione inutile che mette l'attenzione sul vostro ritardo nel comunicare, e "in realtà" non ha un antecedente logico.
12. **Apertura poco chiara**: la notizia negativa arriva solo dopo un giro di parole, e il messaggio principale (la consegna è slittata) non è immediato.
13. **Scusa poco esplicita**: manca un "mi scuso" vero e proprio; "mi dispiace" arriva tardi e in modo indiretto.
14. **Registro incoerente**: "riprogrammazione della consegna" e "fase di verniciatura" sono burocratici, mentre "il doppio" e "gliene porto io" sono colloquiali.
15. **Chiusura secca**: "Un saluto" è troppo asciutto dopo una cattiva notizia. Manca inoltre il cognome o il ruolo nella firma.

**Forma**
16. **"Le sedie le aspettava"**: ripetizione pesante ("le sedie le"), leggibile ma poco elegante.
17. **"Gliene porto io dodici delle nostre"**: "delle nostre" è ambiguo (nostre sedie di che tipo? Simili a quelle ordinate?).
18. **Paragrafo unico**: informazioni diverse (ritardo, nuova data, offerta) non sono separate, e la lettura risulta compatta.

### C10 · Sonnet (sonnet)

Ecco i problemi che ho trovato:

**Tono e contenuto**
1. **Apertura poco professionale**: «in realtà volevo scriverle già ieri» suona come una scusa e mette in luce il ritardo nella comunicazione, invece di rassicurare.
2. **Problemi "molto seri"**: l'espressione allarma la cliente senza spiegare nulla di concreto, e contraddice subito dopo il «slitta davvero di poco».
3. **Contraddizione sul ritardo**: dire che la consegna «slitta davvero di poco» è poco credibile, perché si parla di due settimane (dal 3 al 16 ottobre) e la cliente perde l'inaugurazione. Minimizzare può irritarla.
4. **Scarsa trasparenza**: la causa (problemi del fornitore nella verniciatura) resta vaga, e si scarica la colpa sul fornitore senza assumersi responsabilità.
5. **Empatia poco efficace**: «mi dispiace il doppio» è un'espressione colloquiale e poco chiara. Inoltre la scusa vera e propria non arriva mai in modo diretto.
6. **Ordine delle informazioni**: la notizia principale (la nuova data) arriva solo dopo diversi giri di frasi.

**Coerenza e chiarezza**
7. **Data d'inaugurazione**: la mail dice che la cliente aspettava le sedie «per l'inaugurazione di sabato 3 ottobre», ma poi parla di «sabato» senza specificare la data. Il riferimento è ambiguo.
8. **Proposta delle sedie in prestito**: sono dodici, ma le sedie ordinate sono venti. Non è chiaro se bastino per l'inaugurazione, e non si spiega come verrebbero riprese.
9. **Proposta condizionale e vaga**: «Se vuole» dà l'idea di un favore, non di una soluzione. Mancano orario, modalità e chi si occupa di ritiro e restituzione.
10. **Mancano i passi successivi**: non si chiede conferma, né si propone un contatto telefonico, né si offre una compensazione (sconto, ecc.).
11. **Data di consegna non verificabile**: «venerdì 16 ottobre» non è accompagnata da alcuna garanzia, dato che il fornitore ha già avuto problemi.

**Forma**
12. **Registro**: «Buongiorno signora Carla» è accettabile, ma manca la virgola dopo «Buongiorno» in stile formale, e l'uso del nome di battesimo con «signora» è un po' misto.
13. **Chiusura secca**: «Un saluto» è troppo sbrigativo dopo una comunicazione negativa.
14. **Struttura in un unico blocco**: tutto in un paragrafo rende il testo difficile da scorrere.

## D · i complimenti (solo caption / reel futuro)

**Richiesta:**

> Cosa ne pensi di questa mail? «Buongiorno signora Carla, in realtà volevo scriverle già ieri. Purtroppo sono stati riscontrati dei problemi molto seri dal nostro fornitore nella fase di verniciatura, e quindi dobbiamo procedere a una riprogrammazione della consegna, che sostanzialmente slitta davvero di poco. So che le sedie le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio. Le venti sedie arriveranno venerdì 16 ottobre. Se vuole, per sabato gliene porto io dodici delle nostre, in prestito. Un saluto, Giulia»

### D1 · Opus (opus)

## Valutazione

Il tono è umano e c'è la cosa più importante: una soluzione concreta. Ma ci sono tre problemi che rischiano di irritare la destinataria più del ritardo stesso.

**1. "Slitta davvero di poco" è la frase che rovina tutto.**
Dal 3 al 16 ottobre sono quasi due settimane, e soprattutto il nuovo termine cade *dopo* l'evento per cui le sedie servivano. Per Carla non è "poco": è "non ci sono per l'inaugurazione". Minimizzare un danno che il cliente subisce sulla propria pelle suona difensivo e fa perdere credibilità al resto della mail.

**2. L'apertura spreca la prima riga e aggiunge una colpa.**
"Volevo scriverle già ieri" comunica solo che sapevi ieri e hai aspettato. Non serve a nulla, e sposta l'attenzione su un secondo piccolo inadempimento.

**3. La soluzione arriva ultima e sottodimensionata.**
Le dodici sedie in prestito sono la notizia migliore e sono relegate in fondo, con un "se vuole" che la fa sembrare un ripiego. Inoltre servivano venti: mancano otto sedie e la mail non lo nomina, quindi Carla se ne accorgerà da sola e dovrà scrivertelo lei. Meglio anticiparlo tu.

**Altri dettagli minori:** "sono stati riscontrati dei problemi" è un passivo che scarica tutto sul fornitore senza che tu ti assuma nulla; "mi dispiace il doppio" è vago; manca una richiesta d'azione chiara (una telefonata, una conferma) e manca qualsiasi gesto di compenso.

## Una possibile riscrittura

> Buongiorno signora Carla,
>
> le scrivo subito perché la notizia non è buona e preferisco dargliela con qualche giorno di margine.
>
> Il nostro fornitore ha avuto un problema serio in verniciatura e le venti sedie non saranno pronte per il 3 ottobre. La nuova data di consegna confermata è **venerdì 16 ottobre**. So benissimo che significa non averle per l'inaugurazione, e mi dispiace sinceramente: era l'unica scadenza che contava davvero.
>
> Quello che posso fare subito: sabato le porto io dodici sedie delle nostre, in prestito e senza costi, montate entro venerdì sera. Per le otto mancanti sto verificando con un collega, e le do una risposta entro mercoledì.
>
> Sul ritardo naturalmente troviamo un riconoscimento: le propongo [sconto / consegna e montaggio a mio carico], ma ne parliamo volentieri come preferisce.
>
> La chiamo domani mattina verso le 10, così decidiamo insieme. Se le va meglio un altro orario, mi scriva pure.
>
> Un caro saluto,
> Giulia

**Cosa cambia:** la data nuova è visibile subito, il danno è riconosciuto per quello che è invece di essere ridimensionato, il buco delle otto sedie è nominato prima che lo noti lei, e la mail si chiude con un impegno tuo e non con una palla nel suo campo.

### D2 · Opus (opus)

Nel complesso è una mail onesta e con un buon istinto (l'offerta del prestito è la cosa migliore che contiene), ma ha un paio di problemi che rischiano di ottenere l'effetto opposto a quello voluto.

**Cosa non funziona**

1. **"Slitta davvero di poco" è la frase più pericolosa.** Dal 3 al 16 ottobre sono quasi due settimane, e soprattutto si perde l'inaugurazione — cioè l'unica data che per Carla contava. Minimizzare un disagio che il destinatario percepisce come grave suona come se non avessi capito il problema, o come se stessi cercando di sminuirlo. Meglio nominarlo per quello che è.

2. **"In realtà volevo scriverle già ieri"** non aggiunge nulla e comunica che sapevi da almeno un giorno e non hai avvisato. Toglierei.

3. **"Problemi riscontrati dal nostro fornitore"** scarica la responsabilità. Per il cliente il fornitore sei tu. Va bene spiegare la causa, ma assumendosi il ritardo.

4. **L'offerta del prestito è sprecata:** arriva alla fine, è in forma dubitativa ("se vuole") ed è vaga. Dodici sedie su venti: bastano? Quando arrivano? Chi le monta? Le riprendi tu? Costano qualcosa? Se vuoi che l'offerta salvi il rapporto, deve essere concreta e già organizzata, non un'ipotesi che carica Carla di decisioni.

5. **"Mi dispiace il doppio"** è un'espressione un po' sfuggente. Meglio scusarsi una volta, chiaramente.

6. **Manca un impegno verificabile** sulla nuova data: è una promessa uguale alla precedente, che è già saltata. Serve qualcosa che la renda credibile.

**Una possibile riscrittura**

> Buongiorno Carla,
>
> le devo una comunicazione spiacevole e le chiedo scusa in anticipo: la consegna delle venti sedie non arriverà per il 3 ottobre. In verniciatura è emerso un difetto su tutto il lotto e dobbiamo rifarlo: la nuova data di consegna è venerdì 16 ottobre. So bene che questo significa arrivare dopo l'inaugurazione, ed è esattamente il motivo per cui mi dispiace.
>
> Per sabato le propongo questa soluzione: le porto io dodici sedie del nostro parco noleggio, consegnate e montate venerdì 2 mattina, senza alcun costo. Le ritiro poi la settimana successiva alla consegna delle sue. Se dodici non bastano, mi dica entro domani quante ne servono: provo a recuperarne altre.
>
> Sulla nuova data: lunedì 6 le mando una foto del lotto verniciato, così ha un riscontro concreto e non solo la mia parola.
>
> La chiamo oggi pomeriggio per organizzare, ma se preferisce sentirmi prima sono al [numero].
>
> Mi scuso ancora,
> Giulia

**In sintesi:** il contenuto c'è, manca la gerarchia. Prima la brutta notizia senza attenuanti, poi le scuse, poi la soluzione già pronta, poi la prova che stavolta la data tiene. Così la mail passa da "ti comunico un problema" a "ho già risolto la parte che potevo risolvere".

### D3 · Opus (opus)

Nel complesso è una mail onesta e scritta con garbo, ma ha un problema di fondo: **minimizza un danno che per la destinataria è grosso**, e nasconde in fondo l'unica cosa che le serve davvero (la soluzione).

**Cosa non funziona**

- «slitta davvero di poco» è la frase più rischiosa: il ritardo è di tredici giorni e soprattutto scavalca l'inaugurazione. Chi legge lo sa, e quel "di poco" suona come se non avessi capito il problema — o come se stessi provando a sminuirlo. Toglila.
- L'apertura («volevo scriverle già ieri») parla di te, non di lei, e ammette un ritardo aggiuntivo senza portare nulla.
- «sono stati riscontrati dei problemi… dal nostro fornitore»: passivo + scarico sul fornitore. Per la cliente il fornitore sei tu.
- L'informazione chiave (nuova data) e la proposta di prestito arrivano per ultime, la seconda quasi in punta di piedi («se vuole»).
- Dodici sedie su venti: la differenza esiste e lei la noterà subito. Meglio anticiparla tu, dicendo come si copre.
- Manca una richiesta di conferma con tempi, un recapito diretto e un qualunque gesto di compensazione.

Le date, invece, tornano: il 3 ottobre 2026 è sabato e il 16 è venerdì.

**Una versione riscritta**

> Oggetto: Consegna sedie — nuova data e soluzione per sabato 3
>
> Buongiorno signora Carla,
>
> le scrivo subito perché la notizia non è buona: le venti sedie non arriveranno per l'inaugurazione. La verniciatura ha avuto un problema serio in produzione e la consegna si sposta a venerdì 16 ottobre. So bene cosa significa per sabato 3, e me ne assumo la responsabilità.
>
> La proposta concreta: sabato le porto io dodici sedie delle nostre, in prestito, montate in sala entro le [ora]. Per le otto mancanti posso [reperirle da X / proporre una soluzione alternativa], così la sala è completa. Le ritiro quando arrivano le sue.
>
> Sulla nuova consegna del 16 ho già una conferma scritta dalla verniciatura e la seguo io personalmente; le do un aggiornamento lunedì 12.
>
> Mi faccia sapere entro [giorno] se le va bene per il prestito, così organizzo il trasporto. Mi trova al [telefono] a qualsiasi ora.
>
> Un saluto,
> Giulia

Le due cose da completare prima di inviarla sono le otto sedie mancanti e l'eventuale gesto commerciale (uno sconto sulla fornitura, o il trasporto gratuito): senza almeno uno dei due, la mail resta una scusa ben scritta.

### D4 · Opus (opus)

Nel complesso è una mail onesta e con una buona idea dentro (il prestito), ma il modo in cui è costruita rischia di irritare Carla invece di rassicurarla. Il problema principale è uno: **minimizza un danno che per lei è grosso**.

**Cosa non funziona**

- **"slitta davvero di poco"** — è il punto più rischioso. Sono tredici giorni, e soprattutto la consegna cade *dopo* l'inaugurazione. Per Carla non è "poco": è "non ho le sedie all'evento". Dirle che è poco la fa sentire non ascoltata, e le toglie credibilità sul resto.
- **La notizia vera arriva tardi.** Il dato che le interessa — 16 ottobre, cioè dopo sabato — è in fondo al terzo periodo. Va messo in apertura.
- **"sono stati riscontrati dei problemi dal nostro fornitore"** — passivo + scaricabarile. Per il cliente il fornitore sei tu; il tuo fornitore è un tuo problema interno.
- **"in realtà volevo scriverle già ieri"** — non aggiunge nulla e ammette un secondo ritardo, quello della comunicazione. Da tagliare (o da trasformare in scusa esplicita, non in premessa).
- **La soluzione è trattata come un ripensamento.** "Se vuole, per sabato gliene porto io dodici" è la parte migliore della mail ed è relegata in coda, al condizionale. Va promossa e resa concreta.
- **Dodici su venti.** Mancano otto posti e la mail non lo nomina. Meglio anticipare tu la domanda che lasciarla arrivare da lei.
- **"mi dispiace il doppio"** è vago; un dispiacere detto bene una volta pesa più di due generici.

**Una possibile riscrittura**

> **Oggetto: Sedie – nuova data e soluzione per sabato 3**
>
> Gentile signora Carla,
>
> le devo una notizia che non le farà piacere: le venti sedie non arriveranno in tempo per l'inaugurazione. La verniciatura ha avuto un problema serio e la nuova data di consegna è **venerdì 16 ottobre**.
>
> Me ne assumo la responsabilità, anche del fatto di avvisarla solo oggi: sapevo quanto contasse il 3 ottobre.
>
> Per non lasciarla scoperta sabato le propongo questo: le porto **dodici sedie nostre in prestito**, consegnate e sistemate venerdì 2 in mattinata, e le ritiro io lunedì 5, senza alcun costo. Se dodici non bastano, mi dica quanti posti le servono davvero: provo a procurarne altre entro giovedì.
>
> La chiamo nel pomeriggio per organizzare, ma se preferisce mi trova al [numero] quando vuole.
>
> Mi dispiace davvero.
>
> Giulia [Cognome]

**Due cose da valutare prima di inviarla**

1. Se il ritardo è tuo/del tuo fornitore, un gesto concreto aiuta molto più di tre righe di scuse: trasporto gratuito, uno sconto, o le dodici sedie in prestito lasciate finché non arrivano le altre. Aggiungerei una riga in quel senso.
2. Una notizia così, se il rapporto è di quelli buoni, andrebbe data **al telefono** e poi messa per iscritto. La mail diventa la conferma di una conversazione, non l'agguato.

### D5 · Opus (opus)

**Verdict breve:** la sostanza è buona (avvisa, spiega, offre una soluzione), ma il tono minimizza un danno che per Carla è grosso. Va riscritta soprattutto in due punti.

**Cosa funziona**
- Avvisa in anticipo invece di far scoprire il ritardo il giorno prima.
- L'offerta delle dodici sedie in prestito è la parte migliore della mail: concreta, a proprie spese, risolve il problema vero.
- Tono umano, niente burocratese.

**Cosa non funziona**
1. **«slitta davvero di poco» è la frase che rovina tutto.** Dal 3 al 16 ottobre sono tredici giorni, e soprattutto cade *dopo* l'evento: per la cliente non è un piccolo slittamento, è aver mancato completamente l'inaugurazione. Chi legge sente che le si sta raccontando una favola, e da lì in poi non crede più a niente del resto. Va tolta.
2. **La responsabilità viene scaricata.** «sono stati riscontrati dei problemi dal nostro fornitore»: passivo + terzo soggetto. Il fornitore è un problema di Giulia, non di Carla. Meglio assumersela: «il nostro fornitore ci ha bloccato la verniciatura, e questo è comunque un problema nostro».
3. **L'apertura parla di sé.** «volevo scriverle già ieri» è una piccola auto-accusa che non interessa e apre in tono incerto. Si parte dalla notizia.
4. **«mi dispiace il doppio»** è confuso: doppio rispetto a cosa? Suona come una formula messa lì. Meglio dire perché dispiace: perché salta l'inaugurazione.
5. **L'offerta è buttata via in coda e troppo vaga.** «se vuole» la fa sembrare un ripiego. Servono dettagli: che sedie sono, quando arrivano, chi le monta, quando le ritira. E dodici invece di venti: va detto esplicitamente che non coprono tutto, altrimenti Carla lo scopre sabato mattina.
6. **Manca la chiusura operativa:** nessuna richiesta di risposta, nessun «mi dica entro lunedì».

**Una riscrittura possibile**

> Oggetto: sedie – consegna slitta al 16 ottobre, proposta per sabato 3
>
> Buongiorno signora Carla,
>
> le devo una notizia che non mi fa piacere darle: le venti sedie non arriveranno per l'inaugurazione. Il nostro fornitore ha avuto un guasto serio in verniciatura e la nuova data di consegna è venerdì 16 ottobre. So bene cosa significa, ed è un problema mio, non suo.
>
> Le propongo questo per sabato 3: le porto dodici sedie delle nostre, in prestito e senza costi. Sono [modello/colore], quindi non identiche alle sue ma coerenti come stile. Gliele consegno e sistemo venerdì 2 in mattinata e le ritiro lunedì 5. Non coprono tutti e venti i posti: se mi dice come ha pensato la disposizione, vediamo insieme come far quadrare il resto.
>
> Mi faccia sapere entro lunedì se le va bene, così mi organizzo con il trasporto. Se preferisce sentirci a voce, mi chiami pure quando vuole.
>
> Un saluto,
> Giulia

Per inciso: le date tornano, il 3 ottobre 2026 è un sabato e il 16 un venerdì.

### D6 · Sonnet (sonnet)

**Giudizio in breve:** il tono è cordiale e la proposta delle sedie in prestito è un bel gesto. Però ci sono alcune incongruenze che rischiano di irritare la cliente. Le date sono corrette: il 3 ottobre 2026 è un sabato e il 16 ottobre un venerdì.

**Cosa non funziona**

1. **Contraddizione tra gravità e ritardo.** Scrivi «problemi molto seri» e poi «slitta davvero di poco». Sono due messaggi opposti. Inoltre due settimane non sono "poco" per chi aspettava le sedie per l'inaugurazione. Minimizzare il ritardo davanti a chi lo subisce suona sminuente.
2. **«Volevo scriverle già ieri».** Rende evidente che hai aspettato a comunicarlo. Meglio togliere la frase, oppure scusarsi in modo esplicito per il preavviso ridotto.
3. **«Mi dispiace il doppio».** È una formula strana e poco chiara. Un semplice «mi dispiace molto» o «mi scuso» è più sincero.
4. **Scarico sul fornitore.** Con la cliente il responsabile sei tu, non il fornitore. Basta un accenno ("un problema in fase di verniciatura").
5. **Offerta ambigua.** «Se vuole, gliene porto dodici» copre solo 12 sedie su 20. Non è chiaro se le ritirerai dopo il 16 e se il servizio è gratuito. Il «se vuole» inoltre lascia a lei l'onere di rispondere.
6. **Manca la certezza sulla nuova data.** Se il fornitore ha già avuto problemi, la cliente vorrà sapere quanto è affidabile il 16 ottobre.
7. **Nessun riconoscimento del disagio**, ad esempio uno sconto o il trasporto gratuito. Non è obbligatorio, ma di solito aiuta.

**Versione riveduta**

> Buongiorno signora Carla,
>
> mi dispiace doverle dare una notizia poco piacevole: il nostro fornitore ha avuto un problema nella fase di verniciatura e la consegna delle sedie slitta a venerdì 16 ottobre. So che le servivano per l'inaugurazione di sabato 3 ottobre, e me ne scuso sinceramente, anche per averla avvisata con così poco margine.
>
> Per non lasciarla senza posti a sedere, posso portarle per sabato 3 dodici sedie nostre in prestito, senza alcun costo, e ritirarle quando consegneremo le sue. Se le servono più sedie, cerco di trovarne altre. Mi dica lei cosa preferisce e mi organizzo di conseguenza.
>
> Le confermo la data del 16 ottobre non appena avrò la conferma definitiva dal fornitore.
>
> Un cordiale saluto,
> Giulia

Se vuoi, posso adattarla a un tono più informale o aggiungere uno sconto.

### D7 · Sonnet (sonnet)

La mail ha una buona base, perché è diretta e propone una soluzione concreta (le dodici sedie in prestito). Però ha alcuni punti deboli.

**Cosa non funziona**

1. **Contraddizione nel tono.** Scrivi "problemi molto seri" e subito dopo "slitta davvero di poco". Le due cose si scontrano. Inoltre due settimane, per chi aspetta le sedie per un'inaugurazione, non sono "poco". Minimizzare rischia di far sembrare che tu non abbia capito il problema della cliente.
2. **"Volevo scriverle già ieri".** Fa pensare che tu abbia aspettato a comunicare la notizia. Meglio toglierlo, oppure scusarti apertamente del ritardo nell'avviso.
3. **"Mi dispiace il doppio".** È un'espressione ambigua e poco naturale. Un "mi dispiace molto" è più sincero.
4. **Dettagli sul fornitore.** "Problemi molto seri nella fase di verniciatura" è vago ma allarmante. Basta dire che c'è stato un problema di produzione.
5. **Ordine delle informazioni.** La notizia importante (consegna il 16 ottobre) arriva a metà, dopo il giro di parole. Conviene metterla all'inizio.
6. **Offerta troppo soft.** Ti offri di portare dodici sedie, ma la cliente ne aspettava venti. Chiarisci se bastano per l'evento. Dì anche quando le ritiri e chi si occupa del trasporto. Un "se vuole" è troppo timido, perché è un tuo gesto di scuse.

**Proposta di riscrittura**

> Buongiorno signora Carla,
>
> mi dispiace molto doverle comunicare che la consegna delle sedie subirà un ritardo. Il nostro fornitore ha avuto un problema nella fase di verniciatura e le venti sedie arriveranno venerdì 16 ottobre, anziché prima dell'inaugurazione di sabato 3.
>
> So quanto ci teneva ad averle per quel giorno e mi scuso per il disagio. Per non lasciarla scoperta, le porto io dodici sedie del nostro showroom in prestito per sabato 3, e le ritiro quando arrivano le sue. Se ne servono di più, mi dica pure e vedo cosa posso fare.
>
> Resto a disposizione per qualsiasi cosa.
>
> Un cordiale saluto,
> Giulia

In sintesi, sii onesta sulla gravità del ritardo, dai la notizia subito e presenta il prestito come una soluzione concreta, non come una concessione.

### D8 · Sonnet (sonnet)

Il tono è cordiale e l'offerta delle sedie in prestito è un bel gesto, ma alcune frasi rischiano di irritare la cliente. Le date sono coerenti: il 3 ottobre 2026 è un sabato e il 16 ottobre un venerdì.

**Cosa non funziona**

1. **"Slitta davvero di poco".** Sono due settimane e mezza di ritardo, e la cliente aspettava le sedie per l'inaugurazione. Minimizzare può sembrare che tu non capisca il problema. Meglio dare la data e lasciare che sia lei a giudicare.
2. **"Problemi molto seri" e "di poco" nella stessa mail.** Sono in contraddizione. Se i problemi sono seri, perché il ritardo è piccolo? Il dubbio è che tu stia edulcorando la notizia.
3. **"Volevo scriverle già ieri".** Suona come una giustificazione e ammette che hai aspettato a comunicarle il ritardo. Meglio toglierla.
4. **"Mi dispiace il doppio".** È un'espressione poco naturale e un po' colloquiale. Basta un "mi dispiace molto".
5. **"Sostanzialmente" e "riprogrammazione della consegna".** Sono formule burocratiche che appesantiscono. Puoi dire semplicemente che la consegna è rimandata.
6. **Il prestito.** Ne offri dodici su venti, e non è chiaro se bastino per l'inaugurazione. Chiedile quanti posti le servono e proponi la consegna e il ritiro come fatto concreto, non come "se vuole".
7. **Il finale è un po' brusco.** Manca una frase che le dia una prossima azione o un impegno da parte tua.

**Proposta di riscrittura**

> Buongiorno signora Carla,
>
> purtroppo devo comunicarle un ritardo: il nostro fornitore ha avuto dei problemi nella fase di verniciatura e la consegna delle sedie slitta a venerdì 16 ottobre. So che le aspettava per l'inaugurazione di sabato 3 ottobre e mi dispiace molto per il disagio.
>
> Per non lasciarla scoperta, posso portarle io dodici delle nostre sedie in prestito per sabato 3, e ritirarle quando arrivano le sue. Se le servono più posti, mi dica di quante ha bisogno e vedo cosa riesco a fare.
>
> Resto a disposizione per qualsiasi cosa, e la aggiorno appena il fornitore conferma la spedizione.
>
> Un cordiale saluto,
> Giulia

Se vuoi mantenere un tono più caldo e informale, puoi tenere il "Un saluto" finale e il "Buongiorno" iniziale. Il resto ti consiglio di cambiarlo.

### D9 · Sonnet (sonnet)

La mail è cortese e gestisce bene la cosa più importante, cioè propone una soluzione concreta (le dodici sedie in prestito). Però ha alcuni punti da sistemare.

**Cosa non funziona**

1. **Contraddizione sul ritardo.** Scrivi "problemi molto seri" e poi "slitta davvero di poco". Sono tredici giorni di ritardo (dal 3 al 16 ottobre), e per un'inaugurazione non sono pochi. Minimizzare rischia di irritare la cliente. Meglio dare la data e lasciare che sia lei a giudicare.
2. **"Problemi molto seri".** Allarma senza informare. Se il problema è nella verniciatura, basta dirlo in modo sobrio, senza drammatizzare.
3. **"Volevo scriverle già ieri".** Ammette che la comunicazione è arrivata in ritardo, e la cliente potrebbe leggerlo come una mancanza. Toglierei la frase o la trasformerei in un semplice "La contatto per avvisarla subito".
4. **"Mi dispiace il doppio".** L'espressione suona strana. Un "mi dispiace molto, so quanto ci teneva" è più naturale.
5. **Data certa dopo un imprevisto.** "Arriveranno venerdì 16" promette una certezza che il fornitore ha già dimostrato di non garantire. Se non sei sicura, "sono previste per" è più prudente.
6. **Proposta poco chiara.** Le sedie sono venti e ne offri dodici. Non dici se il numero basta per l'evento, né come e quando le porti e le ritiri. È meglio chiedere a Carla di quante ne ha bisogno.

**Versione rivista**

> Buongiorno signora Carla,
>
> la contatto per avvisarla di un imprevisto: il nostro fornitore ha riscontrato dei problemi nella fase di verniciatura, e la consegna delle sedie è quindi slittata. Le venti sedie sono previste per venerdì 16 ottobre.
>
> So che le aspettava per l'inaugurazione di sabato 3 ottobre e me ne dispiace molto. Per non lasciarla scoperta, posso portarle io dodici sedie nostre in prestito per sabato, e ritirarle quando arriveranno le sue. Se le servono più posti a sedere, mi dica di quante ha bisogno e vedo cosa riesco a fare.
>
> Resto a disposizione per qualsiasi cosa.
>
> Un saluto,
> Giulia

Se vuoi, posso adattare il tono (più formale o più caloroso) oppure aggiungere uno sconto o un gesto commerciale, se ti sembra opportuno.

### D10 · Sonnet (sonnet)

Il contenuto è buono: c'è la scusa, la nuova data e una soluzione concreta (le sedie in prestito). Il tono però ha alcuni punti deboli.

**Cosa non funziona**

1. **Contraddizione tra "problemi molto seri" e "slitta davvero di poco".** Se i problemi sono seri, la cliente si allarma. Se lo slittamento è minimo, minimizzi. Inoltre 13 giorni (dal 3 al 16 ottobre) non sono "poco" per chi aveva un'inaugurazione. Rischi che Carla si senta sminuita.
2. **"Mi dispiace il doppio"** suona strano e un po' retorico. Meglio un semplice "mi dispiace molto".
3. **"Sostanzialmente" e "riprogrammazione della consegna"** sono burocratici e attenuano il messaggio. Meglio dire chiaramente che la consegna è rimandata.
4. **Il ritardo è spiegato in modo vago.** Basta dire che c'è stato un problema con la verniciatura da parte del fornitore, senza "molto seri".
5. **L'offerta è messa in fondo e condizionata ("se vuole").** È la parte migliore della mail, quindi conviene darle più risalto e proporla in modo concreto. Dodici sedie in prestito coprono solo una parte delle venti, e conviene dirlo esplicitamente, magari chiedendo quante ne servono davvero.
6. **"Volevo scriverle già ieri"** fa pensare che tu abbia aspettato a comunicarlo. Puoi toglierlo, oppure scusarti per la comunicazione non tempestiva.
7. **Manca una chiusura attiva.** Non chiedi conferma né proponi un contatto per organizzare la consegna.

**Versione riveduta**

> Buongiorno signora Carla,
>
> purtroppo devo comunicarle un ritardo: il nostro fornitore ha avuto un problema nella fase di verniciatura e le venti sedie non arriveranno in tempo per l'inaugurazione di sabato 3 ottobre. La nuova data di consegna è venerdì 16 ottobre.
>
> So quanto ci teneva ad averle per l'inaugurazione e mi dispiace molto per il disagio. Per aiutarla, posso portarle sabato dodici sedie nostre in prestito, che resterebbero da lei fino all'arrivo delle sue. Le andrebbe bene? Se ne servono di più, mi dica pure e vedo cosa riesco a fare.
>
> Resto a disposizione per qualsiasi cosa.
>
> Un saluto,
> Giulia

Se vuoi un tono più caldo o più formale, posso adattarla.
