# All'IA chiedi i problemi, non le parole

**Data:** 2026-09-19
**Tipo:** pillola
**Fonte:** url (contenuti/spunti/2026-09-19-scrivere-con-ia.md)
**Stato:** idea
**Uscite:** contenuti/idee/uscite/scrivere-con-ia-2026-09-19.md

Reel a sé stante: chi lo guarda non ha visto gli altri. Il testo **l'hai scritto tu** e il rischio è fartelo
riscrivere e perderlo. Azienda, persone e vicenda sono inventate da capo per questo reel. Le uscite mostrate nel reel
verranno da richieste vere (T0b): questa idea non ne contiene. (Cosa si è guardato degli altri reel per non ripetersi
sta solo in fondo, in «Note interne».)

## Concetto AI illustrato
«Migliora questo testo» è una richiesta di **generazione**, non di correzione. Il modello non ritocca la tua bozza:
scrive un testo nuovo, token dopo token, condizionato dalla bozza e dall'istruzione. Niente nel meccanismo lo obbliga
a conservare le tue parole. Le tue scelte meno tipiche (un modo di dire tuo, una frase storta ma vera) sono proprio le
continuazioni a bassa probabilità, e in una riscrittura vengono sostituite da quelle ad alta probabilità: più
frequenti nei testi e, dopo il post-training, più premiate dalle persone (fluenti, educate, tipiche). Un modello
che genera prende, un pezzo alla volta, una delle continuazioni più probabili: davanti a una pagina vuota la riempie
con il probabile, davanti alla tua bozza ci **sostituisce il tuo**. Il risultato spesso è davvero più ordinato (il lato buono, da dire sul serio), ma è ordinato nel modo di
tutti. Che la scrittura assistita renda i testi più simili fra loro è misurato (Padmakumar & He, ICLR 2024; Agarwal,
Naaman & Vashistha, CHI 2025; Doshi & Hauser, Science Advances 2024: *riferimenti da verificare dal revisore*).

Se invece chiedi **i problemi e non le soluzioni**, l'uscita del modello è un commento **sul** tuo testo, non il tuo
testo. La bozza resta intatta, e ogni parola della versione finale la scegli e la scrivi tu. Il modello fa il lavoro
in cui la sua natura aiuta: ha visto moltissima prosa, riconosce gli schemi ricorrenti (passivi, verbi trasformati in
nomi, parole riempitivo, ripetizioni, la notizia sepolta a metà), non si stanca e non si affeziona alla tua frase.

Tre cautele, perché il reel non diventi né una lode né una stroncatura:
- La tesi («correttore di bozze, non ghostwriter», «nemmeno una parola») è **l'opinione di Thomas Ptacek**, non un
  risultato. Nel reel si dice così, con il nome. Che chi legge riconosca il testo di un modello lo afferma lui, con
  un'iperbole; gli studi sul riconoscimento da parte delle persone danno risultati misti (chi usa spesso questi
  strumenti li riconosce bene: Russell, Karpinska & Iyyer, 2025, *da verificare*). Il reel non promette «se ne
  accorgono tutti».
- Il correttore sbaglia: può non vedere un passivo, segnalare come difetto una scelta voluta, contare male, e proporre
  comunque frasi sue anche se gli hai chiesto di non farlo (*da verificare sulle uscite C*). Ptacek stesso dice di non
  prendere tutti i consigli. Decide chi scrive.
- Il modello tende a lodare (piaggeria, *sycophancy*: Sharma et al., ICLR 2024, *da verificare*). È la seconda regola
  di Ptacek ed è un concetto a sé: qui resta in caption (vedi «Angoli scartati»).

## Situazione
*Proposta* (l'articolo non ha una scena: parla della scrittura dell'autore). Lavori da Quattroassi Arredi, un
negozio di arredi per locali (azienda inventata per questo reel), e devi dire a una cliente che le sedie per
l'inaugurazione del suo bar arrivano in ritardo. La mail l'hai scritta tu, di getto. A schermo è **la bozza**, dichiarata inventata
(«mail, azienda e persone inventate»):

> Buongiorno signora Carla, in realtà volevo scriverle già ieri. Purtroppo sono stati riscontrati dei problemi molto
> seri dal nostro fornitore nella fase di verniciatura, e quindi dobbiamo procedere a una riprogrammazione della
> consegna, che sostanzialmente slitta davvero di poco. So che le sedie le aspettava per l'inaugurazione di sabato 3
> ottobre, e mi dispiace il doppio. Le venti sedie arriveranno venerdì 16 ottobre. Se vuole, per sabato gliene porto
> io dodici delle nostre, in prestito. Un saluto, Giulia

(78 parole, cinque frasi più i saluti: da ricontare. Il 3 ottobre 2026 è un sabato, il 16 un venerdì.) La bozza ha
difetti veri e messi apposta: cinque riempitivi («in realtà», «purtroppo», «molto», «sostanzialmente», «davvero»), un
passivo («sono stati riscontrati»), un verbo sepolto in un nome («procedere a una riprogrammazione»), la notizia
(la data) alla quarta frase, e un «di poco» che la data smentisce. Ha anche due cose che sono **di Giulia** e di
nessun altro: «mi dispiace il doppio» e «gliene porto io dodici delle nostre». Sono il filo del reel: che fine fanno?
Il presentatore può riscrivere la bozza a modo suo (anzi, sarebbe coerente con la tesi): in quel caso le richieste
qui sotto cambiano con lei, prima di T0b.

**L'errore di partenza.** Incolli la bozza e scrivi «Migliora questa mail.». Torna una mail ordinata e pronta.
**Momento di prova (entro la scena 2):** prima di mostrarla, la domanda a chi guarda: «di cinque frasi tue, quante
ne tornano come le avevi scritte?». Chi guarda scommette un numero; poi le frasi della bozza si spengono una a una e
resta il conto vero (*ipotesi da verificare sulle uscite A:* nessuna o una; «mi dispiace il doppio» sparisce). Se
il conto smentisce l'ipotesi, la scena si riscrive sul conto vero: il reel non lo forza.

**L'errore comune.** «Migliora questa mail mantenendo il mio stile.» È il «sii originale» di questo reel: la toppa
che viene in mente a tutti (*ipotesi da verificare sulle uscite B:* cambia meno, ma le frasi tue non tornano
lo stesso).

**La mossa.** «Non migliorare questa mail: elencami i problemi, senza riscrivere niente.» La bozza resta ferma a
schermo e si accendono i punti segnalati (riempitivi, passivo, il verbo sepolto, la data in fondo, «di poco»). Secondo
momento, piccolo: i cinque riempitivi accesi, e chi guarda li toglie con gli occhi prima che cadano. Poi la mail la
riscrive Giulia: la versione finale è **scritta da noi e dichiarata tale** (non è un'uscita del modello), con la data
in testa, senza riempitivi, e con «mi dispiace il doppio» ancora lì.

**Il rilancio.** Fra i problemi segnalati ce n'è uno che non è un problema (*ipotesi da verificare sulle uscite C:*
«mi dispiace il doppio» segnalato come troppo informale, oppure proposte di riscrittura non richieste). Quello non si
tocca: i consigli non si prendono tutti, e le frasi che propone non si copiano.

Potenziale e limite nella stessa scena. Potenziale: in pochi secondi trova quello che tu, affezionato alla tua bozza,
non vedi più; e la riscrittura «migliorata» è davvero più ordinata. Limite: se le parole le sceglie lei, la mail non è
più tua; come correttore può sbagliare bersaglio, e l'ultima parola resta a chi firma.

## Messaggio centrale
Se chiedi all'IA di migliorare un testo, te lo riscrive con le parole di tutti. Chiedile i problemi e riscrivi tu:
lei trova i difetti, la voce resta la tua.

## Struttura narrativa
**Schema di partenza:** @ingegneria.italia · r0040 — domanda ingenua con risposta secca → caso storico →
generalizzazione → modello a cinque elementi → soluzione → "attenzione però" → prodotto certificato → firma.

> Ma [cosa innocua] può davvero causare [evento grave]? Sì, ed è per questo che [regola pratica]. Pensate che nel [anno] a [caso reale] [conseguenza]. [Principio fisico in una riga]. E anche [altri materiali comuni], se [condizione], possono [stesso effetto]. La fisica si riassume in quello che in gergo si chiama [modello con nome]: [elementi in elenco]. Eliminandone anche uno solo il rischio si riduce. Per questo si usa [soluzione]. Attenzione però: non tutti [gli strumenti] sono adatti. Servono [strumenti certificati], che devono [prova di terzi]. Noi ringraziamo [sponsor]. [Firma].

Perché questo: l'analisi lo indica come il più pulito dell'account («ogni blocco risponde alla domanda lasciata aperta
dal precedente»), è la spiegazione tecnica detta con calma più vicina al nostro formato (`docs/stile-parlato.md`), e
la sua ossatura è la nostra: un gesto innocuo («migliorala») con un costo che non ti aspetti, un'autorità con nome e
data, un principio in una riga, la soluzione, e un «attenzione però» che tiene il reel lontano dalla lode. Le sue tecniche stanno tutte in «Tecniche condivise», tranne le due firme
escluse sotto.

**Adattamento** (una riga per fase):
- [cosa innocua può davvero causare…? Sì + regola] → hook a filmato: il problema di chi guarda («la fai migliorare e
  non sembra più tua»), poi in scena 2 il «sì» secco: non è un'impressione, e si vede contando le frasi.
- [caso con nome e anno] → l'autorità al posto del caso storico: Thomas Ptacek, settembre 2026, e la sua regola netta
  («nemmeno una parola» di quelle che ti suggerisce), detta come opinione sua. Il caso è la mail di Giulia.
- [principio in una riga] → «migliora» vuol dire «riscrivi», e quando riscrive sceglie, un pezzo alla volta, fra
  le parole più battute: quelle di tutti al posto delle tue. Detto in una frase, come se fosse la prima volta.
- [anche altri materiali comuni, se…] → l'errore comune: anche «mantenendo il mio stile» la fa riscrivere (uscite B).
  Una frase sola, non un catalogo di generi.
- [modello con nome: elementi in elenco] → cosa trova un correttore: riempitivi, passivi, verbi sepolti nei nomi,
  la notizia in fondo. **Solo a schermo**, accesi sulla bozza; la voce ne nomina al massimo due.
- [soluzione] → la mossa: la richiesta cambia («elencami i problemi, senza riscrivere niente»), la bozza resta ferma,
  riscrive Giulia.
- [attenzione però: non tutti…] → non tutti i consigli si prendono: il problema che non è un problema (uscite C), e
  l'ultima parola è di chi firma.
- [prodotto certificato, sponsor, firma] → tagliati (vedi Escluse). Al loro posto chiusura a battuta + CTA.

**Tecniche** (da «Tecniche condivise»):
- `domanda-ingenua`: l'hook e il «sì» secco della scena 2; la curiosità non è sul se, è sul come.
- `autorità`: Ptacek con nome e data, una volta, come opinione («uno che scrive di software da vent'anni dice…» solo
  se il revisore conferma il profilo; altrimenti solo il nome).
- `caso-esemplare`: una sola mail regge tutto il reel, dalla prova alla chiusura.
- `rilancio-a-meta`: l'«attenzione però» sul consiglio da non prendere, nella penultima scena.

**Escluse:**
- `sponsor-integrato` e `firma-di-chiusura`: firme di @ingegneria.italia, non si copiano.
- `elenco`: i tipi di problema non si leggono a camera, stanno accesi sulla bozza e in caption.
- `modello-mentale` con nome (il «pentagono»): qui non esiste un modello con un nome vero, e inventarlo sarebbe falso.
- Le due varianti finali (dry/wet) e la certificazione: lo schema è da 84 s; qui obiettivo ≤ 75 s, sette scene.
- Il metodo completo di Ptacek (secondo modello a contesto pulito che confronta le versioni) e la regola sui
  complimenti: secondo e terzo concetto, in caption.

## Cosa impara chi guarda
1. **Un modo nuovo di leggere.** «Migliora» non vuol dire «correggi»: vuol dire «riscrivi», e quello che torna è un
   testo suo, condizionato dal tuo. Per un testo di servizio va benissimo. Per un testo che deve suonare come te, no.
2. **La mossa.** Scrivi tu. Poi incolla e chiedi: «elencami i problemi, senza riscrivere niente». Poi riscrivi tu, e
   le frasi che ti propone lo stesso non le copi.
3. **Il criterio** (*proposta*). Nella versione finale ogni frase l'hai scritta tu, e quella a cui tenevi c'è ancora.
   Se un consiglio ti toglie proprio quella, è il consiglio da non prendere. (In caption il criterio di Ptacek:
   far scegliere fra le due versioni a una conversazione nuova, che non ha visto la lavorazione.)

## Pilastro
Cosa può fare per te (un correttore che non si stanca). In filigrana **come funziona davvero**: riscrivere è
generare, e generare tira verso il probabile.

## Perché ora
- **Per chi guarda.** L'articolo è del 17 settembre 2026 e la regola «nemmeno una parola» è abbastanza netta da far
  discutere. «Migliorami questa mail» è fra i gesti più comuni con questi strumenti (*nessun dato: non si dice un
  numero*).
- **Per il canale.** Porta una mossa che si fa domani su un gesto che chi guarda fa già. È il primo reel con l'apertura a filmato e la VOCE scritta dopo le trascrizioni.
- **Non invecchia**: non dipende da un modello o da una versione. Invecchiano solo i conti sulle uscite, che vanno in
  caption con modello e data.

## Fonte
- **URL:** https://sockpuppet.org/blog/2026/09/17/how-to-write-with-an-llm/ · blog personale *sockpuppet.org*
  (piè di pagina «Thomas & Erin Ptacek»; il post è in prima persona singolare, lo spunto lo attribuisce a Thomas
  Ptacek) · pubblicato il 17 settembre 2026 · consultato il 2026-09-19 con WebFetch. **WebFetch restituisce una
  lettura mediata da un modello piccolo, non il testo integrale**: le citazioni qui sotto sono brevi e vanno
  ricontrollate sulla pagina dal revisore. Il sottotitolo del post risulta «A Final Ward» (non spiegato).
- **Fatti presi** (parole del testo, fra virgolette):
  1. La tesi: i modelli restano utilissimi, ma vanno usati «like a copyeditor rather than a ghostwriter».
  2. Regola uno: «You may not use a single word an LLM suggests to you.» Il motivo: i modelli sono bravissimi a
     scegliere «pleasing turns of phrase», che si accumulano, e un loro paragrafo arriva a molti lettori «not as
     writing but as output».
  3. Regola due: «Avoid encouragement». Il modello loda la prima stesura e ti toglie i ripensamenti, che per l'autore
     sono «load-bearing parts of your voice».
  4. A cosa serve: segnala il passivo, i verbi nominalizzati o con l'azione sepolta, i giri di frase ripetuti; i
     riempitivi («very», «unfortunately», «really», «actually», sparsi sulla bozza «like sawdust»); e 2-3 paragrafi
     che spostati migliorano subito la chiarezza.
  5. Il metodo: scrivi tu → fai trovare i problemi al modello → per ogni problema riscrivi tu il paragrafo → presenti
     originale e nuova versione al modello e chiedi quale è meglio (secondo la lettura, a un modello senza il contesto
     della lavorazione). E: «Don't take all of the model's copyediting advice»; l'autore racconta di aver dato il post
     a GPT5, che suggeriva di tagliarne circa il 20 %, e di non averlo fatto (chiude con «I'm just gonna be me»).
  6. Cita il manuale *Style: Lessons In Clarity And Grace* **senza nominarne l'autore**, accostandolo a quello che
     Hanson fa per il C (*C Interfaces and Implementations*); e uno strumento che si è costruito, un «writing
     workshopping tool» (Python, HTMX, SQLite), con il prompt con cui l'ha fatto generare. Nomina GPT5, Claude, Codex e
     la CLI Antigravity.
- **Cosa l'articolo non dice:** nessun dato, nessuno studio, nessun confronto fra modelli; nessun esempio prima/dopo
  di un testo corretto; niente sull'italiano né su testi brevi di lavoro (parla di saggi e post dell'autore);
  nessuna prova che i lettori riconoscano davvero il testo di un modello (è un'affermazione sua, con un'iperbole:
  «parts per trillion»). L'autore di *Style* (Joseph M. Williams, per quanto ne so) nel post non c'è: se il manuale si
  nomina, il nome va verificato altrove. **Consiglio: nel reel il manuale non si nomina**; al più in caption.
- **Discordanza da segnalare:** lo spunto parla di ~1.200 parole, la lettura di WebFetch ne stima ~1.800. Non
  entra nel reel.

## Angoli scartati
- **«Non fidarti dei suoi complimenti»** (la regola due). Forte e vera, ma è un altro concetto (la piaggeria dei
  modelli e da dove viene): merita un reel suo, con uscite proprie («Cosa ne pensi di questa mail?»). Qui in caption;
  la richiesta D qui sotto serve a capire se c'è materiale.
- **«Falla giudicare a un'altra IA che non ha visto la lavorazione»** (l'ultimo passo del metodo). È una procedura in
  più passaggi e con due strumenti: non è la mossa che si fa domani con una mail. In caption, come criterio.
- **«Caccia alle parole riempitivo»** (solo i riempitivi). Troppo stretto per reggere un reel, e rischia la lezione
  di stile senza IA. Resta dentro l'angolo scelto come secondo momento di prova.
- **«I lettori si accorgono che l'ha scritto l'IA».** È l'affermazione meno sostenuta dell'articolo (nessuna
  fonte; nota interna: `generativa-probabile` aveva scartato lo stesso claim per i selezionatori). Qui il costo è un
  altro e si vede a schermo: le tue frasi non ci sono più.
- **Il manuale di stile e lo strumento costruito dall'autore.** Sono consigli di lettura e di programmazione: non
  riguardano chi guarda.

## Note per il reel
**Hook candidato** (problema di chi guarda, in coppia con l'immagine; a schermo nessun titolo):
- Frase: «Scrivi una mail, la fai migliorare all'IA, e quella che torna non sembra più tua. Ti è mai successo?»
  (19 parole)
- Clip dietro: una persona alla scrivania che copia un testo dal portatile, lo incolla in una chat, legge la risposta
  e resta perplessa (sopracciglia, mezzo sospiro) prima di premere «invia». Da cercare: «woman laptop office reading
  screen frowning», «copy paste text laptop close up», «typing email hesitating send».
- Alternativa: «Quando chiedi all'IA di migliorarti una mail, quante parole tue restano?» (12 parole), stessa clip.
- TITOLO della copertina (la tesi): «All'IA chiedi i problemi, non le parole». Alternativa: «Correttore di bozze, non
  ghostwriter» (è la formula di Ptacek: in copertina va attribuita o evitata).

**Percorso** (*proposta*, sette tappe; la VOCE la scrive lo sceneggiatore):
1. Hook a filmato: il problema.
2. La bozza di Giulia e «Migliora questa mail.»; la scommessa («di cinque frasi tue, quante ne tornano?»); le frasi
   si spengono, resta il conto vero. Si apre il loop: si può farsi aiutare senza perdere la mail? Sì, ma non così.
3. Il lato buono e il principio: la mail migliorata è ordinata davvero; solo che «migliora» per lei vuol dire
   «riscrivi», e quando riscrive sceglie fra le parole più battute, quelle che userebbe chiunque (una frase, detta
   come se fosse la prima volta: chi guarda non ha visto altri reel).
4. L'errore comune: «mantenendo il mio stile», e il conto che cambia poco (uscite B). Qui Ptacek e la sua regola
   («c'è chi dice: nemmeno una parola»), come opinione, con nome e data a schermo.
5. La mossa: la richiesta nuova; la bozza ferma, i problemi che si accendono; i riempitivi che cadono; riscrive
   Giulia. Si chiude il loop.
6. Attenzione però: il problema che non è un problema; i consigli non si prendono tutti.
7. Chiusura a battuta, MESSAGGIO, CTA; «mi dispiace il doppio» è ancora nella mail, accesa.
Scene d'attenzione a filmato oltre l'hook: candidate la 3 o la 6 (chi rilegge una mail prima di inviarla). Obiettivo
≤ 75 s; la tappa 3 è la prima a perdere una frase, la 4 si può fondere con la 3.

**Filo visivo** (tre oggetti in tutte le scene):
- **la bozza di Giulia**, sempre la stessa carta; le sue cinque frasi si spengono (tappa 2), si accendono a punti
  (tappa 5), e due restano riconoscibili fino alla fine («mi dispiace il doppio», «gliene porto io dodici»);
- **la carta «richiesta»**, una riga sola che cambia tre volte; ogni stato è **esattamente** una delle richieste qui
  sotto (A, poi B, poi C);
- **il contatore delle frasi tue** (`ContatoreScorre` o `Contatore`): «5 su 5» → il conto di A → il conto di B →
  «5 su 5» con la mossa (perché le scrivi tu). È l'oggetto del loop e resta attenuato finché non si chiude.
Cambi grandi candidati: il numero del conto a tutto schermo alla rivelazione (tappa 2); «NEMMENO UNA PAROLA» a punch
con il nome di Ptacek sotto (tappa 4); zoom su «mi dispiace il doppio» (tappa 6 o 7).

**Testi del modello: richieste da generare (T0b).** Nel reel compaiono una mail riscritta e un elenco di problemi
attribuiti a un modello: vanno generati davvero, prima della sceneggiatura, 5 con Opus e 5 con Sonnet per richiesta
(sigle A1-A10, B1-B10, C1-C10, D1-D10). La bozza è identica in tutte; cambia solo la prima frase. Una richiesta per riga:

- **A · base («migliora»):** `Migliora questa mail. «Buongiorno signora Carla, in realtà volevo scriverle già ieri. Purtroppo sono stati riscontrati dei problemi molto seri dal nostro fornitore nella fase di verniciatura, e quindi dobbiamo procedere a una riprogrammazione della consegna, che sostanzialmente slitta davvero di poco. So che le sedie le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio. Le venti sedie arriveranno venerdì 16 ottobre. Se vuole, per sabato gliene porto io dodici delle nostre, in prestito. Un saluto, Giulia»`
- **B · errore comune (+ «mantenendo il mio stile»):** `Migliora questa mail mantenendo il mio stile. «Buongiorno signora Carla, in realtà volevo scriverle già ieri. Purtroppo sono stati riscontrati dei problemi molto seri dal nostro fornitore nella fase di verniciatura, e quindi dobbiamo procedere a una riprogrammazione della consegna, che sostanzialmente slitta davvero di poco. So che le sedie le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio. Le venti sedie arriveranno venerdì 16 ottobre. Se vuole, per sabato gliene porto io dodici delle nostre, in prestito. Un saluto, Giulia»`
- **C · la mossa (i problemi, non le parole):** `Non migliorare questa mail: elencami i problemi, senza riscrivere niente. «Buongiorno signora Carla, in realtà volevo scriverle già ieri. Purtroppo sono stati riscontrati dei problemi molto seri dal nostro fornitore nella fase di verniciatura, e quindi dobbiamo procedere a una riprogrammazione della consegna, che sostanzialmente slitta davvero di poco. So che le sedie le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio. Le venti sedie arriveranno venerdì 16 ottobre. Se vuole, per sabato gliene porto io dodici delle nostre, in prestito. Un saluto, Giulia»`
- **D · da generare (deciso dal presentatore il 2026-09-19), solo per la caption e per un reel futuro (i complimenti):** `Cosa ne pensi di questa mail? «Buongiorno signora Carla, in realtà volevo scriverle già ieri. Purtroppo sono stati riscontrati dei problemi molto seri dal nostro fornitore nella fase di verniciatura, e quindi dobbiamo procedere a una riprogrammazione della consegna, che sostanzialmente slitta davvero di poco. So che le sedie le aspettava per l'inaugurazione di sabato 3 ottobre, e mi dispiace il doppio. Le venti sedie arriveranno venerdì 16 ottobre. Se vuole, per sabato gliene porto io dodici delle nostre, in prestito. Un saluto, Giulia»`

La versione finale riscritta da Giulia **non** è un'uscita: la scrive lo sceneggiatore (o il presentatore) dopo aver
letto le uscite C, e a schermo o in caption si dichiara «riscritta da noi».

**Cosa cercare nelle uscite** (ipotesi, non testi; ogni conto con la sigla di ciascuna uscita):
- A: quante delle cinque frasi della bozza tornano **identiche** (il conto del reel è **per frase**, deciso dal presentatore il 2026-09-19: a occhio, con le
  sigle; niente conto per parole); se «mi dispiace il doppio» e «gliene porto
  io dodici» sopravvivono; formule di rito al loro posto («ci scusiamo per il disagio», «La informo che», «resto a
  disposizione»: ipotesi); se la data sale in testa (il lato buono: va detto); **se cambiano i fatti** (date, numeri,
  il prestito): se succede è un limite da caption, non da VOCE.
- B: lo stesso conto. Se B conserva quasi tutto, la tappa 4 si riscrive («cambia meno, ma sceglie ancora lei») o si
  fonde con la 3; la tesi non dipende da B.
- C: quali problemi segnala e se trova i cinque messi apposta (riempitivi, passivo, nominalizzazione, data in fondo,
  «di poco» contro due settimane); se, nonostante il divieto, **propone riscritture** (se sì: è il limite, e la regola
  «non le copi» diventa concreta); se apre con un complimento (materiale per la regola due, in caption); se segnala
  come difetto una delle due frasi di Giulia (il rilancio della tappa 6). Se nessuna uscita C lo fa, la tappa 6 usa
  una riscrittura non richiesta, oppure resta sulle parole di Ptacek («non prendere tutti i consigli»), senza esempio.
- D: quante aprono con una lode e quante nominano i difetti messi apposta.

**Numeri.** In VOCE al massimo due, entrambi conti sulle uscite (frasi tue che tornano con A e con B), ricontati con
le sigle; modello e data in caption. «78 parole», «cinque frasi», «cinque riempitivi» sono conti sulla bozza: da
ricontare. Sedie, date e nomi sono **esempio dichiarato**. Dall'articolo nessun numero entra in VOCE (il «20 %» di
GPT5 al più in caption, se il revisore lo ritrova nel testo).

**Riempitivi in italiano.** Non si traducono i quattro di Ptacek: a schermo quelli della bozza, che sono riempitivi
veri dell'italiano scritto d'ufficio («in realtà», «purtroppo», «molto», «sostanzialmente», «davvero»); per la caption
anche «assolutamente», «praticamente», «a dire il vero», «un attimo». Tre dei cinque coincidono per senso con
quelli dell'articolo: va bene, purché non si dica che «sono quelli di Ptacek». Nota per lo sceneggiatore: nel parlato
gli intercalari servono (`docs/stile-parlato.md`, mossa 5); Ptacek parla di prosa scritta, e la VOCE non deve
suonare come una condanna di «praticamente».

**MESSAGGIO candidato** (≤ 12 parole):
- «All'IA chiedi i problemi. Le parole mettile tu.» (9)
- Alternative: «Falle trovare i difetti. La mail riscrivila tu.» (8); «Lei trova i problemi. La voce resta la tua.» (9)

**CTA** (una): «Mandalo a chi si fa riscrivere le mail dall'IA» (invio, destinatario ovvio). Alternativa a domanda vera:
«E tu, la fai riscrivere o la fai correggere?»

**Claim per il revisore**
- Attribuzione: tesi e regole sono di Thomas Ptacek, opinione e non dato. Verificare sulla pagina autore, data,
  citazioni brevi, e se il confronto finale è davvero affidato a un modello **senza contesto** (la lettura di WebFetch
  lo dice in una risposta e non lo cita alla lettera). Verificare anche la frase su GPT5 e il 20 %.
- «Migliora vuol dire riscrivi»: corretto come meccanismo (l'uscita è un testo nuovo generato dato il tuo), ma
  l'esito si afferma solo sulle uscite A. Non «non resta niente», non «sempre».
- «Le parole di tutti» / «più battute»: il modello campiona fra le più probabili; mai «la più probabile» né
  «sempre» (formula già verificata, vedi «Note interne»).
- Non si dice che chi legge «se ne accorge»: lo dice Ptacek, e gli studi sono misti.
- «L'IA è brava a trovare i problemi»: è l'esperienza di Ptacek più le uscite C; può mancare difetti, segnalarne di
  falsi e contare male. «Trova», non «trova tutti».
- «Nemmeno una parola» è la regola di Ptacek, volutamente estrema. Il reel la riporta; la sua mossa è più mite (chiedi
  i problemi, riscrivi tu). Non presentare la regola come nostra né come dimostrata.
- I riferimenti citati nel «Concetto» (Padmakumar & He 2024; Agarwal et al. 2025; Doshi & Hauser 2024; Sharma et al.
  2024; Russell et al. 2025) sono a memoria: da verificare prima di metterli in caption. Nessuno entra in VOCE.
- Mail, azienda, cliente e Giulia sono inventati e va dichiarato. «Quattroassi Arredi» è un nome nuovo, scelto per
  non richiamare un'azienda nota: una ricerca web del 2026-09-19 non ha trovato aziende di arredi o sedie con questo
  nome, ma **l'omonimia va ricontrollata dal revisore** (ricerca web e registro imprese). Il nome non compare nella
  bozza né nelle richieste, quindi se si cambia non si rigenera niente. Nessun dato personale vero nelle richieste.
- Le uscite vengono dalla CLI con un prompt di sistema neutro, non dall'app: non si dice «in chat».

**Note interne (per non ripetersi; niente di questo entra nel reel)**
- Ogni reel è a sé stante: nessun richiamo, a voce o a schermo, ad altri reel, e nessun personaggio o azienda che
  prosegue.
- `generativa-probabile` ha già speso lo schema r0037, la mail di candidatura, il cursore che si ferma sulla frase
  aperta e la colonna delle candidate: qui non si riusano.
- Il concetto «sceglie fra le più probabili» è già passato dal revisore per quel reel (semplificazione «una parola
  alla volta» accettata; mai «la più probabile»): valgono le stesse formule, ma qui si ridice da zero in una frase.

**Per lo sceneggiatore**
- Leggi `~/Projects/reelkit/trascrizioni/r0040.txt` e `analisi/r0040.md`: si prende il passo (domanda da profano, «Sì»
  e la frase che va avanti, «Attenzione però»), non le parole né la firma.
- In caption: la fonte con link, autore e data; il metodo completo di Ptacek; la regola sui complimenti; i tipi di
  problema in elenco; la dichiarazione dei testi (modello, data, tagli nostri; la versione finale «riscritta da noi»);
  il limite (il correttore sbaglia, decide chi firma).
