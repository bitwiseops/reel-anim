# Generativa vuol dire probabile: la tua candidatura, uguale a tutte

**Data:** 2026-09-16
**Tipo:** pillola
**Fonte:** testo (contenuti/spunti/2026-09-15-generativa-probabile.md)
**Stato:** sceneggiata
**Sceneggiatura:** contenuti/sceneggiature/2026-09-15-generativa-probabile.md
**Uscite:** contenuti/idee/uscite/generativa-probabile-2026-09-16.md

Rifacimento con lo stesso slug. La versione precedente (il biglietto per la pensione di Marco) è nella storia git al
commit 3ae4d09, e da lì vengono il meccanismo e i claim già verificati dal revisore. La tesi non cambia, cambia la
situazione: **la mail di risposta a un annuncio di lavoro**, una cosa che chi guarda fa davvero e dove essere uguale
agli altri candidati costa caro. Le mail mostrate nel reel verranno da uscite vere (T0b): questa idea non ne contiene.

## Concetto AI illustrato
Un modello linguistico genera testo in modo autoregressivo. A ogni passo calcola una distribuzione di probabilità su
tutto il vocabolario (token, spesso pezzi di parola, non parole intere). La distribuzione dipende da tutto quello che
viene prima: le istruzioni di sistema, la richiesta, il testo già scritto. Il modello campiona un token fra i più
probabili (con temperatura e top-p, quindi non sempre il primo), lo aggiunge al testo e ricomincia. In senso tecnico
«generativa» vuol dire proprio questo: il modello rappresenta la probabilità dei testi e ne estrae campioni. Il nome
non dice niente sulla creatività, e «vuol dire probabile» è la parafrasi più vicina alla definizione.

Da questo meccanismo vengono le due facce dell'uscita. Le continuazioni ad alta probabilità sono grammaticali e
tipiche, quindi la mail è **fluente**: registro giusto, struttura giusta (oggetto, saluto, perché mi candido, cosa so
fare, disponibilità, saluti). Sono anche le continuazioni più frequenti nei testi, e dopo il post-training quelle che
le persone hanno premiato, perché le persone preferiscono il familiare (Kirk et al., ICLR 2024; Zhang et al., 2025).
Quindi la mail è **generica**. Una lettera di presentazione è un genere con formule fissatissime, e il modello le ha
viste moltissime volte. Su una richiesta aperta, modelli diversi e lo stesso modello interrogato più volte convergono
sulle stesse risposte (Jiang et al., *Artificial Hivemind*, NeurIPS 2025).

Anche «Sii originale.» è contesto, e sposta la distribuzione. La sposta però verso l'«originale» tipico (un attacco
a effetto, una domanda retorica, «non sono il solito candidato»: *ipotesi da verificare sulle uscite B*) e non aggiunge
nessuna informazione sul candidato. Quello che la mail dice di te resta vuoto, perché nel contesto non c'è niente che
lo riempia. Un dettaglio vero e specifico (un progetto, un numero) aggiunge invece informazione, e cambia la
distribuzione di molti token dopo: il numero diventa l'argomento della mail. Nel modello non cambia niente: stessi
pesi, stesso modo di scegliere. L'uscita resta una continuazione ad alta probabilità, ma di un altro contesto.

Due cautele. Il reel non dice che l'IA «non è» creativa: nel senso di Doshi & Hauser (Science Advances, 2024) i testi
scritti con l'IA sono più creativi uno per uno e più simili fra loro nel complesso. Dice che il nome non lo promette e
che l'uscita di default è la più battuta. Inoltre, quando mancano i fatti, il modello tende a riempire il vuoto con
fatti plausibili: la mail base può attribuire al candidato esperienze e competenze generiche o inventate («ho gestito
campagne…»), oppure lasciare segnaposto («[Nome]», «[azienda precedente]»). È lo stesso meccanismo visto da un altro
lato: il probabile al posto del vero (*da verificare sulle uscite A*).

## Situazione
*Proposta:* hai trovato un annuncio che ti interessa e chiedi all'IA di scrivere la mail di candidatura. A schermo c'è
l'**annuncio**, fisso per tutto il reel e dichiarato inventato:

> **Acme Arredi (Padova) cerca un addetto o un'addetta marketing.** Gestirai social, newsletter e promozioni nei
> negozi. Chiediamo due anni di esperienza e una scrittura chiara. Contratto a tempo indeterminato.

(Azienda inventata: in sovraimpressione «annuncio e azienda inventati».) Accanto c'è la carta «richiesta» con la
richiesta base, e sotto la mail che si scrive un pezzo alla volta, con un cursore che si ferma.

**Momento di prova 1 (hook).** La mail si scrive fino a una frase aperta presa da un'uscita vera e il cursore
lampeggia. Chi guarda la finisce prima che compaia: ha fatto quello che fa il modello, cioè ha guardato le parole
prima e ha preso la più probabile. *Ipotesi da verificare sulle uscite A:* la chiusa «Resto a disposizione per un
eventuale… colloquio» oppure l'attacco «Ho letto con grande… interesse». Si sceglie la frase che torna in più uscite
e che si ferma su una parola sola.

**L'errore comune.** Nella richiesta si aggiunge «Sii originale.». Cambia il vestito (l'attacco, il tono), ma dentro
restano le formule della mail di prima e di te non si sa niente di più. Quello che si accende a schermo dipende dalle
uscite B.

**Momento di prova 2 (payoff).** «Sii originale.» esce dalla carta, ed entra la riga vera: «Nel mio lavoro attuale ho
portato la newsletter di un negozio di biciclette da 300 a 2.100 iscritti in un anno.» La mail nuova si ferma di nuovo
su una frase aperta che chi guarda finisce **solo perché conosce il dettaglio** (*ipotesi:* «…da 300 a 2.100…
iscritti»). Quindi è ancora probabile, ma probabile dopo il tuo numero, e quel numero gliel'hai dato tu.

Nella stessa scena ci sono il potenziale e il limite. Il potenziale: la prima mail è corretta, educata e pronta da
spedire in pochi secondi, e con una riga vera lo stesso meccanismo scrive una mail che parla di te. Il limite: lasciata
a sé scrive la mail di chiunque, «sii originale» cambia il vestito e non il contenuto, e senza fatti tuoi può
metterne di plausibili al loro posto.

## Messaggio centrale
«Generativa» non vuol dire creativa: l'IA scrive una parola alla volta prendendo una delle più probabili, e per
questo la tua candidatura viene fluente e uguale a quella di chiunque. Non chiederle di essere originale: dalle un
dettaglio vero che sai solo tu.

## Struttura narrativa
**Schema di partenza:** @marcocamisanicalzolari · r0037 — fatto di cronaca minimo → meccanismo dell'errore →
assoluzione di chi ha sbagliato → diagnosi psicologica → regola pratica → domanda.

> [Strumento] ha detto [consiglio sbagliato] e poi [conseguenza grave]. Gli avevano chiesto [domanda pratica]. E lui ha risposto con [tono sicuro], il tono di uno che sa. Ma non sapeva niente di [contesto reale]: non [verbo], non [verbo], non sa che [dettaglio specifico]. Mette insieme [dati] e ne tira fuori una media che suona bene: su [caso banale] va benissimo, su [caso serio] no. La parte che mi colpisce è che non hanno sbagliato a [usare lo strumento], capita a tutti. Hanno sbagliato a non [verifica mancata]. Ci fidiamo perché [non esitano mai]: leggiamo [sicurezza] come [competenza]. Quindi usiamola pure per [uso innocuo], ma [caso serio] si controlla con [fonte umana].

Perché questo: è il reel del corpus più vicino al nostro (un caso minuscolo di uso quotidiano dell'IA, il meccanismo
senza gergo, il limite dosato e non vietato, una regola pratica), e tutti i suoi tag stanno in «Tecniche condivise».
Il suo meccanismo («una media che suona bene») è quasi il nostro.

**Adattamento** (una riga per fase):
- [fatto minimo + conseguenza] → la prova 1: la mail di candidatura che si ferma sulla frase aperta, e chi guarda la
  finisce. Al posto della conseguenza grave, la posta in gioco detta al «tu»: la tua mail la leggono accanto a quelle
  degli altri.
- [domanda pratica] → la carta «richiesta» con l'annuncio: «Scrivi la mail per candidarmi a questo annuncio.»
- [tono sicuro, il tono di uno che sa] → la mail è fluente, ordinata, pronta: il lato buono, detto sul serio.
- [non sapeva niente del contesto: tre negazioni concrete] → «non sa che progetto hai fatto, non sa i tuoi numeri, non
  sa perché vuoi proprio quel posto». Una frase sola con tre verbi, e a schermo tre segnaposto vuoti nella mail.
- [una media che suona bene: su un caso banale va benissimo, su uno serio no] → il meccanismo: una parola alla volta,
  la colonna delle candidate. Per una mail di conferma o per spostare un appuntamento la strada battuta va benissimo,
  per una candidatura no.
- [non hanno sbagliato a usarla, hanno sbagliato a non…] → «Non sbagli a fartela scrivere, lo facciamo tutti. Sbagli
  a pensare che basti scriverle "sii originale".» Qui entra l'errore comune con le uscite B.
- [diagnosi psicologica] → tagliata (vedi Escluse); ne resta la formula come aforisma: «È scritta bene. Solo che è
  scritta per chiunque.» (*proposta*)
- [regola pratica con fonte umana] → la mossa e la prova 2: la riga vera nella richiesta, la mail nuova che finisci
  solo tu. La fonte umana sei tu: il dettaglio lo sai solo tu.
- [domanda finale] → chiusura a battuta + CTA «invia» (vedi Escluse).

**Tecniche** (da «Tecniche condivise»):
- `caso-esemplare`: una sola mail per un solo annuncio regge tutta la tesi, dall'hook alla chiusura.
- `contrasto`: fluente e generica; mail di conferma contro candidatura; «Sii originale.» contro il dettaglio vero,
  nella stessa carta.
- `assolvere-prima-di-accusare`: prima della mossa, «non sbagli a usarla». Tiene dalla sua parte chi ha appena
  riconosciuto la propria mail.
- `aforisma`: uno solo, sulla battuta («scritta per chiunque» o la variante scelta dallo sceneggiatore), detto a
  camera con il riquadro grande.

**Escluse:**
- *Diagnosi psicologica* («ci fidiamo perché non esitano mai») e l'analogia dell'amico esperto (`analogia`): sono un
  secondo concetto (la sicurezza scambiata per competenza, cioè le allucinazioni), e con sei fasi il reel sfora i 75
  s. Il riempire i vuoti con fatti plausibili resta in caption.
- `elenco`: le tre negazioni non si leggono come lista, diventano una frase con tre verbi (i «tre membri» di
  `docs/stile-parlato.md`) e a schermo tre segnaposto.
- `formula-ripetuta` come anafora: resta solo la ripetizione della parola chiave «probabile» (2-3 volte).
- `finale-aperto` («Voi cosa ne pensate?»): è una domanda generica. Qui una CTA sola, e l'invio ha un destinatario
  ovvio (chi sta cercando lavoro).
- La cronaca con conseguenza grave: non c'è un fatto di cronaca, e inventarlo sarebbe falso. Lo sostituisce la prova.

## Cosa impara chi guarda
1. **Un modo nuovo di leggere.** Se una frase della mail la finisci in testa prima che la scriva, è la continuazione
   più probabile, quella che avrebbe potuto scrivere chiunque. Non è un difetto, è il funzionamento. *Proposta:* per
   una mail di servizio (conferme, appuntamenti, solleciti) la strada battuta è proprio quella che vuoi.
2. **La mossa.** Prima di chiedere, scrivi nella richiesta un fatto vero che sai solo tu: un progetto, un numero, il
   motivo per cui vuoi proprio quel posto. Un fatto, non un aggettivo: non «sono creativo e motivato», ma «ho portato
   la newsletter da 300 a 2.100 iscritti». Al posto di «sii originale», che cambia il vestito e non la mail.
3. **Il criterio** (*proposta*). Rileggi la mail e chiediti se l'avrebbe potuta firmare un altro candidato. Se sì, è
   ancora la mail di tutti, e va aggiunto un altro fatto tuo. Poi controlla che ogni fatto nella mail sia tuo davvero:
   quello che non le hai dato, può averlo messo lei.

## Pilastro
Come funziona davvero (cosa fa il modello quando «genera»: sceglie il probabile, un pezzo alla volta, dato quello che
viene prima). In filigrana c'è **cosa può fare per te**: una riga vera nella richiesta sposta tutta la mail.

## Perché ora
*Proposta:*
- **Per chi guarda.** Settembre è il mese in cui si torna a cercare lavoro, e scrivere la mail di candidatura con
  l'IA è ormai un gesto comune. «Generativa» è nel nome di ogni prodotto, e quasi tutti la traducono con «creativa»:
  da lì nasce la mossa sbagliata («sii originale»). Nessun dato su quanti candidati usano l'IA o su cosa ne pensano i
  selezionatori: se serve un numero, va cercato con una fonte, altrimenti non si dice.
- **Per il canale.** Il biglietto per Marco faceva sorridere, ma costava poco sbagliarlo. La candidatura ha una posta
  in gioco vera, e il destinatario dell'invio è ovvio. È anche il primo reel con uno schema preso dal corpus di
  reelkit.
- **Non invecchia**: il criterio «se lo finisci tu, è probabile» vale per qualunque modello. Invecchiano solo i conti,
  che vanno in caption con modello e data.

## Fonte
Non si applica (fonte: testo).

## Angoli scartati
- **Il biglietto per Marco** (versione del 3ae4d09): la tesi è la stessa, ma lo spunto chiede una situazione più
  utile. Le sue uscite (`contenuti/media/generativa-probabile/biglietti-claude-2026-09-14.md`, copia di quella in
  archivio) non servono più: la mail non le usa. Se toglierle lo decide il presentatore.
- **«Senza fatti tuoi, l'IA te li inventa»** (la mail base che attribuisce esperienze generiche). È forte e molto
  utile, ma è un secondo concetto (dove sbaglia: fatti plausibili al posto dei veri). Va in caption come limite; se le
  uscite A lo mostrano in modo netto, può diventare un reel a sé.
- **«I selezionatori riconoscono le mail scritte con l'IA».** Senza fonte è una promessa che il reel non può
  mantenere, e sposta il tema dal meccanismo al giudizio di altri.
- **Le tre mosse** (dettaglio, parole vietate, più proposte da scartare): il reel ha una mossa sola. Le altre in
  caption, con i loro limiti (il sinonimo successivo; varianti dello stesso luogo comune).
- **Opus contro Sonnet**: se le uscite mostrano esiti diversi, resta in caption come limite della mossa.

## Note per il reel
**Hook candidato** (una prova, al «tu», con la frase aperta presa da un'uscita A vera):
- «Hai scritto la candidatura con l'IA? Finisci tu la frase. Resto a disposizione per un eventuale…» (16 parole; la
  frase aperta è un'ipotesi, va sostituita con quella che le uscite confermano).
- Alternativa in prima persona (il caso, poi la sfida): «Ho chiesto all'IA cinque volte la stessa candidatura. Finisci
  tu come chiude…» (12 parole; «cinque» solo se si riferisce a una sola serie di uscite, cioè 5 Opus o 5 Sonnet).
- TITOLO della copertina: la tesi, «Generativa non vuol dire creativa». Al fotogramma 0 ci sono già l'annuncio, la
  carta «richiesta» e l'oggetto della mail (niente schermo vuoto). Niente due punti come snodo nella VOCE.

**Percorso** (*proposta*, sei tappe; le righe VOCE le scrive lo sceneggiatore):
1. Hook, prova 1: la mail si ferma sulla frase aperta.
2. La parola rivelata; «io l'ho chiesta N volte, e c'era in N» (conto vero, con le sigle); la posta in gioco (la tua
   mail la leggono accanto alle altre); si apre il loop: si può avere una mail che parla di te? Sì, ma non chiedendolo.
3. Il meccanismo: una parola alla volta, la colonna delle candidate; «hai fatto la stessa cosa che fa lei». Il lato
   buono e il `contrasto` (mail di conferma sì, candidatura no); le tre negazioni in una frase, con i segnaposto vuoti.
4. `assolvere-prima-di-accusare` e l'errore comune: «Sii originale.» entra nella carta; la mail cambia vestito, dentro
   si accendono le stesse formule.
5. La mossa e la prova 2: «Sii originale.» esce, entra la riga vera; la mail nuova si ferma e chi guarda la finisce
   grazie al numero. Si chiude il loop: è ancora probabile, ma dopo il tuo numero, e quello l'hai scritto tu.
6. Chiusura: l'`aforisma`, il MESSAGGIO, la CTA; l'ultimo fotogramma prepara il primo dell'hook (replay continuo).

Obiettivo ≤ 75 s (~200 parole a 2,8 parole/s): la tappa 3 è la prima a perdere una frase.

**Filo visivo** (tre oggetti in tutte le scene):
- **la carta «richiesta» con l'annuncio agganciato**, cioè «quello che viene prima». L'annuncio non cambia mai; la
  riga sotto riceve «Sii originale.», che poi viene tolta e sostituita dalla riga vera. Ogni stato della carta è
  **esattamente** una delle richieste qui sotto (A, poi B, poi C);
- **la mail con il cursore**: oggetto, saluto, corpo. Si ferma due volte con lo stesso gesto. Nella tappa 3 mostra i
  tre segnaposto vuoti (progetto, numeri, perché proprio voi); nella 4 cambia vestito; nella 5 il numero riempie un
  segnaposto;
- **la colonna delle candidate** (`Classifica`, «esempio: numeri inventati»): dopo la frase aperta della prova 1 la
  parola vera in testa; alla prova 2 la parola del dettaglio in testa. Stesso oggetto, contesto diverso, vincitrice
  diversa. Le barre sono sempre inventate: la CLI non restituisce le probabilità.

Cambi grandi candidati: la parola della prova 1 a tutto schermo alla rivelazione (tappa 2) e quella della prova 2
(tappa 5), nello stesso stile; riquadro del presentatore grande sulle due reazioni e sull'aforisma.

**Testi del modello: richieste da generare (T0b).** Nel reel compaiono mail attribuite a Claude: vanno generate
prima della sceneggiatura, 5 con Opus e 5 con Sonnet per richiesta (sigle A1-A10, B1-B10, C1-C10). Le tre richieste
sono identiche salvo l'aggiunta finale; nella base non c'è la parola «originale». Ogni richiesta sta su una riga:

- **A · base:** `Scrivi la mail per candidarmi a questo annuncio. «Acme Arredi (Padova) cerca un addetto o un'addetta marketing. Gestirai social, newsletter e promozioni nei negozi. Chiediamo due anni di esperienza e una scrittura chiara. Contratto a tempo indeterminato.»`
- **B · errore comune (+ «Sii originale.»):** `Scrivi la mail per candidarmi a questo annuncio. «Acme Arredi (Padova) cerca un addetto o un'addetta marketing. Gestirai social, newsletter e promozioni nei negozi. Chiediamo due anni di esperienza e una scrittura chiara. Contratto a tempo indeterminato.» Sii originale.`
- **C · la mossa (+ un dettaglio vero):** `Scrivi la mail per candidarmi a questo annuncio. «Acme Arredi (Padova) cerca un addetto o un'addetta marketing. Gestirai social, newsletter e promozioni nei negozi. Chiediamo due anni di esperienza e una scrittura chiara. Contratto a tempo indeterminato.» Nel mio lavoro attuale ho portato la newsletter di un negozio di biciclette da 300 a 2.100 iscritti in un anno.`

A schermo la carta mostra la prima frase e la riga aggiunta; l'annuncio sta nel suo riquadro, con le stesse parole.
Nessun nome del candidato nella richiesta: è voluto (è quello che fa chi chiede di fretta), e i segnaposto che ne
escono sono materiale per la tappa 3.

**Cosa cercare nelle uscite** (ipotesi, non testi: vanno confermate o scartate contando sulle uscite, con le sigle e
contando anche le varianti, come «colloquio conoscitivo» o i plurali):
- A: formule di rito come «con grande interesse», «entusiasta», «la vostra realtà», «mi permetto di», «resto a
  disposizione per un eventuale colloquio», «in allegato il mio curriculum»; segnaposto fra parentesi; esperienze
  attribuite al candidato che la richiesta non contiene; con Sonnet, risposte che chiedono prima i dettagli (nel
  biglietto succedeva in 2 su 5: se torna, conta come «la mossa la suggerisce lei stessa», in caption).
- B: un attacco a effetto o una domanda retorica ripetuti fra le uscite (l'«originale» tipico) e le stesse formule di
  A dentro. Se B non cambia il vestito in modo visibile, la tappa 4 si riscrive su «cambia poco».
- C: il numero come argomento centrale; una frase aperta che si completa solo conoscendo il dettaglio; la cornice di
  rito che resta (saluto e chiusa uguali ad A: se succede, è il limite della mossa, in caption); numeri gonfiati o
  fatti aggiunti al dettaglio.

**Numeri**: nessuno in questa idea. In VOCE al massimo due, tutti ricontati sulle uscite con la sigla di ciascuna
uscita, e con il modello (Opus 5 o Sonnet 5) e la data in caption. «2.100 iscritti» è un **esempio dichiarato**
(candidato inventato), e a schermo va segnalato così.

**MESSAGGIO candidato** (≤ 12 parole):
- «Non chiederle di essere originale. Dalle un dettaglio che sai solo tu.» (12)
- Alternative: «Se poteva firmarla chiunque, è la mail di tutti.» (9, il criterio); «L'IA non ti conosce. Il
  dettaglio mettilo tu.» (8).

**CTA** (una): «Mandalo a chi sta cercando lavoro» (invio, destinatario ovvio, nessun claim).

**Claim per il revisore**
- «Una parola alla volta»: in realtà token. Semplificazione già accettata nella revisione del primo reel.
- «Prende una delle più probabili», mai «la più probabile» o «sempre»: il modello campiona.
- «Se l'hai finita tu, era probabile»: è un indizio, non una misura. La prevedibilità per chi legge e la probabilità
  per il modello sono correlate, non identiche.
- La prova 2 non deve suonare come «il dettaglio ha reso l'IA creativa»: è ancora probabile, ma dato un altro
  contesto.
- «Sii originale» è **insufficiente, non inutile**: nel biglietto, insieme al dettaglio, sembrava aiutare la trovata.
  Da ricontrollare su B e C; la VOCE dice «non è chiedendolo che cambia la mail», non «chiederlo non serve».
- Il vestito di B non si chiama «nuovo» né «originale» (X5 della revisione archiviata).
- «Uguale a quella di chiunque» / «la leggono accanto alle altre»: la prima si sostiene solo con le uscite (stesso
  modello, stessa richiesta); non si afferma che gli altri candidati usano l'IA, né che i selezionatori la
  riconoscono (nessuna fonte).
- «Quello che non le hai dato, può averlo messo lei»: vale solo se le uscite A mostrano fatti attribuiti al candidato
  che la richiesta non contiene; altrimenti va detto come rischio generale e solo in caption.
- La mossa ha un limite di buon senso, da dire in caption: il dettaglio dev'essere vero e tuo, e non deve contenere
  dati riservati del datore di lavoro attuale. E la mail finale si rilegge.
- Annuncio, azienda e candidato sono inventati, e va dichiarato a schermo o in caption. «Acme Arredi» è scelto per
  non richiamare un'azienda nota; il revisore controlli che non coincida con un'azienda reale di Padova (se sì, si
  cambia nome e si rigenerano le uscite).
- Le uscite vengono dalla CLI con un prompt di sistema neutro, non dall'app: non si dice «in chat» (V16 del primo reel).

**Per lo sceneggiatore**
- Leggi `~/Projects/reelkit/trascrizioni/r0037.txt`: il passo «non sapeva niente di quella montagna… su una ricetta
  va benissimo, in quota no… non hanno sbagliato a usare l'intelligenza artificiale, capita a tutti» è il ritmo da
  prendere, non le parole.
- In caption: la dichiarazione dei testi (modello, data, tagli nostri), il criterio del punto 3, il limite dei fatti
  plausibili, «il dettaglio l'hai messo tu, la mail l'ha scritta lei», il lato buono del probabile, le altre due mosse
  con i loro limiti.
