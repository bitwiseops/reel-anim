# Generativa non vuol dire creativa: vuol dire probabile

**Data:** 2026-09-15
**Tipo:** pillola
**Fonte:** testo (contenuti/spunti/2026-09-15-generativa-probabile.md)
**Stato:** sceneggiata
**Sceneggiatura:** contenuti/sceneggiature/2026-09-15-generativa-probabile.md

Rifacimento voluto del reel dell'esempio (`templates/esempio-reel.md`) e del primo reel archiviato
(`contenuti/archivio/generativa-non-creativa/`), questa volta parlato a camera e senza personaggi. Stessa tesi,
stessa situazione (il biglietto per Marco), materiale vero già generato. Cambia la struttura: **chi guarda fa la
stessa prova due volte**, e la seconda volta la prova dice una cosa diversa.

## Concetto AI illustrato
Un modello linguistico genera testo in modo autoregressivo. A ogni passo calcola una distribuzione di probabilità su
tutto il vocabolario (token, spesso pezzi di parola, non parole intere). La distribuzione è condizionata da tutto quello
che viene prima: istruzioni di sistema, richiesta, testo già scritto. Il modello campiona un token fra i più probabili
(temperatura, top-p: non sempre il primo), lo aggiunge al testo e ricomincia. «Generativa» in senso tecnico vuol dire
proprio questo: il modello rappresenta la probabilità dei testi e ne estrae dei campioni. Il nome non dice niente sulla
creatività; «vuol dire probabile» è la parafrasi più vicina alla definizione.

Da questo meccanismo vengono le due facce dell'uscita. Le continuazioni ad alta probabilità sono grammaticali e
tipiche, quindi il testo è **fluente**. Sono anche quelle che compaiono più spesso nei testi, e dopo il post-training
quelle che le persone hanno premiato, perché le persone preferiscono il familiare (Kirk et al., ICLR 2024; Zhang et al.,
2025). Quindi il testo è **banale**. Su una richiesta aperta modelli diversi, e lo stesso modello interrogato più volte,
convergono sulle stesse risposte (Jiang et al., *Artificial Hivemind*, NeurIPS 2025).

Anche «sii originale» è contesto, e sposta la distribuzione. La sposta però verso l'«originale» tipico (il finto
documento: verbale, bugiardino, certificato, un genere che si vende già in cartoleria) e non aggiunge nessuna
informazione su Marco. Il contenuto del biglietto di tutti (sveglia, riunioni, caffè) resta, perché nel contesto non
c'è niente che lo sostituisca. Un dettaglio vero e specifico aggiunge invece informazione, e cambia la distribuzione di
molti token dopo: la fotocopiatrice diventa il tema. Nel modello non cambia niente: stessi pesi, stesso modo di
scegliere. L'uscita resta una continuazione ad alta probabilità, ma di un altro contesto. Anche la battuta nuova, infatti,
torna uguale in più uscite: è la nuova strada battuta. Il reel non dice che l'IA «non è» creativa: nel senso di Doshi &
Hauser (Science Advances, 2024) le storie scritte con l'IA sono più creative una per una e più simili fra loro nel
complesso. Dice che il nome non lo promette e che l'uscita di default è la più battuta.

Da sapere, fuori dal reel: il dettaglio non cambia tutto. Con la richiesta del dettaglio senza «originale» (D2), Opus 5
apre ancora con «Caro Marco, dopo tanti anni…» in 4 risposte su 5: la cornice resta e il dettaglio entra nel tema e nel
P.S. Con Sonnet 5 resta anche la cornice del biglietto di tutti («dopo anni di onorato servizio», «meritato riposo»).

## Situazione
*Proposta (dall'archivio, adattata al parlato):* in ufficio va in pensione Marco, e il biglietto lo firma tutto
l'ufficio. Tocca a te scriverlo, e lo chiedi all'IA: «Un biglietto per la pensione di Marco. Lo firma tutto l'ufficio.»
È una scena che chiunque abbia lavorato in un ufficio riconosce, e il biglietto che esce lo riconosce anche chi non ha
mai usato l'IA.

A schermo ci sono tre oggetti: la carta «richiesta», il biglietto che si scrive un pezzo alla volta e un cursore che si
ferma.

**Momento di prova 1 (hook).** Il biglietto si scrive fino a «Caro Marco, finalmente potrai spegnere la…» e il cursore
lampeggia. Chi guarda dice «sveglia» prima che compaia: ha appena fatto quello che fa il modello, cioè ha guardato le
parole prima e ha preso la più probabile. È anche il biglietto di tutti, e in 5 risposte su 5 di Opus la sveglia c'è.

**L'errore comune.** Nella richiesta si aggiunge «Sii originale.». Il vestito cambia: tre volte su cinque esce un
«VERBALE DELLA RIUNIONE STRAORDINARIA DELL'UFFICIO», con lo stesso titolo. Dentro però ci sono ancora la sveglia e «le
riunioni che potevano essere una mail».

**Momento di prova 2 (payoff).** «Sii originale.» esce dalla carta, ed entra la riga vera: «Marco ha passato una vita
a litigare con la fotocopiatrice.» In fondo al biglietto nuovo: «La fotocopiatrice ci ha chiesto di salutarti. Poi si
è…» e il cursore si ferma di nuovo. Chi guarda dice «inceppata», e l'ha finita di nuovo. Quindi è ancora probabile, ma
probabile dopo la fotocopiatrice. Senza quella riga non la finiva nessuno, lei compresa, e quella riga gliel'hai data
tu.

Nella stessa scena ci sono il potenziale e il limite. Il potenziale: il primo biglietto è corretto, cortese e pronto da
firmare, e con una riga vera lo stesso meccanismo scrive una cosa che vale solo per Marco. Il limite: lasciata a sé scrive
il biglietto di tutti, «sii originale» cambia il vestito e non il contenuto, e anche la battuta nuova è la più
probabile, solo di un altro contesto.

## Messaggio centrale
«Generativa» non vuol dire creativa: l'IA scrive una parola alla volta e a ogni passo prende una delle più probabili,
e per questo il testo viene fluente e per questo viene banale. Se vuoi una frase che non abbiano già scritto tutti, non
chiederle di essere originale: cambia quello che viene prima, cioè dalle un dettaglio vero che sai solo tu.

## Cosa impara chi guarda
1. **Un modo nuovo di leggere.** Se una frase dell'IA la finisci in testa prima che la scriva, è la continuazione più
   probabile: quella che scriverebbe chiunque. Non è un difetto del modello, è il suo funzionamento. *Proposta:* per una
   mail formale, un riassunto o un'istruzione la strada battuta è proprio quella che vuoi; prendila e vai.
2. **La mossa.** Prima di chiedere, scrivi nella richiesta una cosa vera che sai solo tu. *Proposta:* un fatto, non un
   aggettivo: non «è simpatico», ma «ha passato una vita a litigare con la fotocopiatrice». Messo al posto di «sii
   originale», perché «sii originale» cambia il vestito e non il biglietto.
3. **Il criterio** (*proposta*). Rileggi la risposta e chiediti se l'avrebbe potuta finire anche chi non conosce Marco.
   Se sì, è ancora il biglietto di tutti, e va aggiunta un'altra cosa vera. Se la finisci solo perché sai della
   fotocopiatrice, il dettaglio ha fatto il suo lavoro. Il criterio del primo reel («se la finisci ancora in testa, il
   contesto era quello di tutti», punto 31 della revisione) va corretto così, perché con la prova 2 chi guarda la finisce
   anche la seconda volta.

## Pilastro
Come funziona davvero (cosa fa il modello quando «genera»: sceglie il probabile, un pezzo alla volta, dato quello che
viene prima). In filigrana c'è **cosa può fare per te**: una riga nella richiesta basta a spostare il biglietto.

## Perché ora
*Proposta:*
- **Per chi guarda.** «Generativa» è nel nome di ogni prodotto, e quasi tutti la traducono con «creativa». Da lì
  nascono la delusione («mi scrive sempre le stesse frasi») e la mossa sbagliata («le chiedo di essere originale»).
  Biglietti e messaggi di saluto sono una richiesta che quasi tutti hanno fatto o faranno. E Sonnet 5, con cui nelle
  nostre prove il dettaglio finisce spesso attaccato al biglietto di tutti («dopo anni di onorato servizio… la
  fotocopiatrice»), dal 30/06/2026 è il modello predefinito dei piani Free e Pro (da ricontrollare nell'app il giorno
  della pubblicazione; fonte nella revisione archiviata, V15).
- **Per il canale.** Il primo reel non è mai stato registrato con la VOCE parlata. Le 76 uscite vere del
  2026-09-14 ci sono già, e le richieste senza «originale» (A2, C2, D2) permettono per la prima volta di mostrare a
  schermo **esattamente** la richiesta che ha prodotto ogni testo. Con la pipeline nuova diventa il reel di riferimento.
- **Non invecchia**: il criterio «se lo finisci tu, è probabile» vale per qualunque modello. Invecchiano solo i conti,
  che stanno in caption con modello e data.

## Fonte
Non si applica (fonte: testo). Il materiale d'archivio che l'idea usa è elencato nelle Note per il reel.

## Angoli scartati
- **«Non lo cerca, lo scrive lei»** (generativa = produce, non recupera; il database barrato della scena 4
  archiviata). Scartato perché è la frase più astratta del primo reel ed è un secondo concetto: chi guarda non fa
  niente di diverso domani. Va in caption, se serve.
- **Le tre mosse** (dettaglio, parole vietate, cinque proposte da scartare). Scartato perché il reel ha una mossa sola,
  e le altre due hanno i limiti dei punti 26-27 della revisione (il sinonimo successivo; cinque varianti dello stesso
  luogo comune). In caption, con i limiti.
- **«Chiedere originalità ti dà la battuta più vista di internet».** Con «Sii originale.» la frase «riunioni che
  potevano essere una mail» passa da 1 risposta su 10 (A2) a 6 su 10 (C2). Fa ridere, ma è un reel sul prompt, non su
  «generativa»; e sono pochi campioni. Qui resta un beat dentro l'errore comune.
- **Opus contro Sonnet** (lo stesso dettaglio, due esiti: la lettera della fotocopiatrice oppure «oggi si chiude un
  capitolo epico… con la fotocopiatrice»). Scartato perché il concetto è un altro (i modelli non sono uguali). Resta in
  caption come limite della mossa (V15, obbligatoria nel primo reel).
- **Il bivio con i rami** (scena 4 archiviata) come scena a sé. Scartato perché ripete la colonna delle candidate: nel
  parlato costa una scena intera, e la prova 1 lo ha già fatto provare.
- **La battuta «Per dispetto.»** come payoff (primo reel). Non è un angolo diverso ma una scelta di testo: la metto nelle
  note come alternativa, con le sue condizioni.

## Note per il reel
**Hook candidato** (una prova, al «tu», con la frase aperta):
- «Finisci tu la frase, prima dell'IA. Caro Marco, finalmente potrai spegnere la…» (12 parole).
- Alternativa con la situazione: «Hai chiesto all'IA un biglietto per un collega in pensione? Finisci tu. Caro Marco,
  finalmente potrai spegnere la…» (18 parole).
- Il TITOLO della copertina resta la tesi: «Generativa non vuol dire creativa». Al fotogramma 0 ci sono già la carta
  «richiesta» e «Caro Marco,» nel biglietto (niente schermo vuoto, niente parola sola).
- Senza due punti come snodo nella VOCE (`valida` avvisa); la frase del biglietto si introduce con un punto.

**Percorso** (*proposta*, sei tappe; le righe VOCE le scrive lo sceneggiatore):
1. Hook, prova 1: il cursore dopo «spegnere la».
2. «Sveglia», detto da chi guarda e poi a schermo; «io l'ho chiesto cinque volte, e la sveglia c'era tutte e cinque»;
   si apre il loop: si può avere una frase che non abbiano scritto tutti? Sì, ma non chiedendolo.
3. Il meccanismo: una parola alla volta, la colonna delle candidate con «sveglia» in testa. «Hai fatto la stessa cosa
   che fa lei.» Per questo il biglietto è fluente, e per questo è quello di tutti. Qui entra anche il lato buono (mail
   formali).
4. L'errore comune: «Sii originale.» nella carta. Il biglietto cambia vestito (il verbale); dentro si accendono
   «sveglia» e «una mail».
5. La mossa e la prova 2: «Sii originale.» esce, entra la riga della fotocopiatrice, «Poi si è…», il cursore,
   «inceppata». Si chiude il loop: è ancora probabile, ma dopo la fotocopiatrice, e quella l'hai scritta tu.
6. Chiusura: la battuta, il MESSAGGIO, la CTA; l'ultimo fotogramma prepara il primo dell'hook (replay continuo).

Obiettivo: ≤ 75 s. Con il parlato (2,8 parole/s) sono ~200 parole in tutto: la tappa 3 è la prima a perdere una frase.

**Filo visivo** (tre oggetti in tutte le scene):
- **la carta «richiesta»**, cioè «quello che viene prima». È intera nell'hook, poi riceve «Sii originale.», che dopo
  viene tolta e sostituita dalla riga della fotocopiatrice. Ogni stato della carta è **esattamente** una richiesta
  generata davvero (A2, poi C2, poi D2);
- **il biglietto con il cursore**, il vuoto da riempire. Si ferma due volte, sullo stesso gesto: «spegnere la ▌» e
  «Poi si è ▌». Nella 4 è lo stesso oggetto con il vestito da verbale (un'intestazione sopra), e dentro si accendono le
  stesse parole;
- **la colonna delle candidate** (`Classifica`, «esempio: numeri inventati»). Dopo «spegnere la» c'è «sveglia» in
  testa; alla prova 2, dopo «si è», ci sono «inceppata» e «bloccata». Stesso oggetto, contesto diverso, vincitrice
  diversa.

Cambi grandi candidati: «SVEGLIA» a tutto schermo alla rivelazione (tappa 2) e «INCEPPATA» alla prova 2 (tappa 5), con
lo stesso stile, come firma delle battute. Riquadro del presentatore grande sulle due reazioni («Visto?») e sulla
chiusura, quando ci sarà.

**Numeri** (tutti veri, dal file delle uscite; da ricontrollare dal revisore prima che vadano in VOCE o in caption):
- A2, la sola richiesta, Opus 5: sveglia in **5 risposte su 5**, contando il plurale «sveglie» (`A2-opus-1`). Il conto
  grezzo del file dice 4 perché cerca solo «sveglia». Con Sonnet 5 invece 0 su 5, e 2 risposte su 5 non scrivono il
  biglietto ma chiedono prima i dettagli (`A2-sonnet-3`, `-5`). «La porta dell'ufficio (per te) resta (sempre) aperta»
  in 4 su 5 di Opus (`A2-opus-1` … `-4`).
- C2, con «Sii originale.»: «VERBALE DELLA RIUNIONE STRAORDINARIA DELL'UFFICIO», titolo identico, in **3 su 5** di Opus
  (`C2-opus-1`, `-3`, `-4`); sveglia 5 su 5 con Opus e 3 su 5 con Sonnet (con il plurale; il conto grezzo dice 4 e 2);
  «riunioni che potevano essere una mail» in 6 su 10 (`C2-opus-2`, `-3`; `C2-sonnet-2` … `-5`), contro 1 su 10 in A2.
- D2, con il dettaglio e senza «originale»: in 5 su 5 di Opus c'è un P.S. sulla fotocopiatrice; 3 su 5 finiscono con la
  macchina che si inceppa o si blocca (`D2-opus-1`, `-3`, `-5`), e 2 su 5 hanno la stessa idea, «saluta e poi si
  inceppa» (`D2-opus-1`, `-5`). Sveglia in 1 su 10, non 0 (`D2-opus-1`, «niente sveglie»). Il «20 su 20» del primo reel
  valeva per B e D, non si trasferisce.
- In VOCE al massimo due numeri: «tutte e cinque» (tappa 2) e «tre volte su cinque» (tappa 4). Il resto va in caption.
  Il presentatore li può dire in prima persona («io l'ho chiesto cinque volte»): è la sua prova. Non si dice «in chat»
  (V16: le uscite vengono dalla CLI).

**Testi attribuiti al modello: da dove prenderli.** Non va generato niente di nuovo. Tutto sta in
`contenuti/archivio/generativa-non-creativa/biglietti-claude-2026-09-14.md` (Claude Opus 5 e Sonnet 5, 2026-09-14,
Claude Code 2.1.270, CLI e non app; condizioni nell'intestazione del file). Ogni parola viene da una sola uscita
(`docs/sceneggiatura.md` §5). Il file resta in archivio; se la pipeline lo vuole in `contenuti/media/generativa-probabile/`,
lo copia il presentatore.

*Set consigliato: richieste senza «originale»* (sezione «Senza "originale" nella prima riga»). La carta a schermo
coincide parola per parola con la richiesta che ha prodotto il testo.
- Carta, tappe 1-3 (A2): «Un biglietto per la pensione di Marco. Lo firma tutto l'ufficio.»
- Prova 1: `A2-opus-5`, «Versione spiritosa»: «Caro Marco, / finalmente potrai spegnere la sveglia senza sensi di
  colpa!» Per l'hook basta fermarsi a «la». **Attenzione**: è la seconda di tre proposte della risposta, quindi la
  VOCE non può dire «comincia così»; «ha scritto» sì. Alternativa da un biglietto unico: `A2-opus-4`, «…e per le
  mattine senza sveglia.» (prova su «senza…»).
- Carta, tappa 4 (C2): la stessa riga, più «Sii originale.»
- Il vestito, tappa 4: `C2-opus-3`, tutto dalla stessa uscita. Il titolo «VERBALE DELLA RIUNIONE STRAORDINARIA
  DELL'UFFICIO» e, dal «Punto 3», «punta la sveglia solo quando vuole lui;» e «non partecipa più alle riunioni che
  "potevano essere una mail".» Tagli da dichiarare: tutto quello che c'è fra il titolo e il Punto 3, e la prima voce
  del Punto 3 («può ignorare tutte le mail…»). Sul vestito nessuna etichetta «nuovo» né «originale» (X5).
- Carta, tappa 5 (D2): «Un biglietto per la pensione di Marco. Lo firma tutto l'ufficio. Marco ha passato una vita a
  litigare con la fotocopiatrice.»
- Prova 2: `D2-opus-5`, il P.S.: «La fotocopiatrice ci ha chiesto di salutarti. Poi si è inceppata.» (la voce non
  legge «P.S.»: «e in fondo aggiunge…»). Può comparire anche il fronte della stessa uscita, «Caro Marco, finalmente
  libero. (E anche lei.)». Fa rima con la prova 1 (stesso «Caro Marco, finalmente»), ma a voce va detto senza la
  parentesi.
- Candidate: «sveglia» dopo «spegnere la» è vera; le altre due candidate vanno inventate, e la `Classifica` le dichiara.
  Dopo «si è», «inceppata» (`D2-opus-5`) e «bloccata» (`D2-opus-3`) sono vere tutte e due. Barre sempre inventate:
  l'API non restituisce le probabilità.

*Set d'archivio* (i testi del primo reel, già scelti e ritoccati dal presentatore). Vengono da richieste **con**
«originale» nella prima riga, quindi la carta a schermo non coincide con la richiesta: nel primo reel era dichiarato
con «richieste quasi uguali».
- `A-opus-2` proposta 1, ritoccato: «Caro Marco, da domani la sveglia la decidi tu, e il caffè potrai berlo sul
  divano.» La prova si ferma dopo «sveglia» e ha più risposte giuste («la decidi tu», «non suona più»).
- `C-opus-1`, il bugiardino («PENSIONE®» / «Principio attivo: tempo libero al 100%.» / «Eccipienti: sveglia spenta,
  caffè bevuto seduto.»), con i tagli di X1.
- `B-opus-1`: «Caro Marco, sono io. Quella in fondo al corridoio.» + «Da quando esci da quella porta prometto di
  funzionare alla perfezione. Per dispetto.» Fa più ridere di «Poi si è inceppata», ma la sua richiesta contiene anche
  «Sii originale.», che il reel dice di togliere, e non è una prova (non si indovina). Valgono le condizioni V12 e X10.

*Da non riusare con il set consigliato*: la colonna «da / oggi / sono» dopo «Caro Marco,» (scene 5-6 del primo reel).
Con D2 Opus apre ancora con «dopo» in 4 su 5, quindi il riordino con «sono» in testa lì sarebbe falso: vale solo per le
richieste B e D. Il riordino da mostrare è quello dopo «si è».

**MESSAGGIO candidato** (≤ 12 parole):
- «Non chiederle di essere originale. Dalle un dettaglio che sai solo tu.» (12) È la tesi con la mossa, e riporta a
  schermo il «solo tu» che la voce del primo reel aveva perso (U3).
- Alternative: «Se la finisce chiunque, è il biglietto di tutti.» (9, il criterio come battuta); «L'IA non ha mai
  conosciuto Marco. Tu sì.» (8, la chiusura scelta dal presentatore per il primo reel; porta con sé T8, memoria e
  connettori).

**CTA** (una): «Mandalo a chi scrive i biglietti in ufficio» (del primo reel, nessun claim, T12). Il destinatario è
ovvio, e un invio con chi non ci segue vale più di un salvataggio.

**Claim per il revisore**
- «Una parola alla volta»: in realtà sono token. È una semplificazione accettata (punto 7 della revisione archiviata).
- «Prende una delle più probabili», mai «la più probabile» o «sempre»: il modello campiona.
- «Se l'hai finita tu, era probabile»: è un indizio, non una misura. La prevedibilità per chi legge e la probabilità per
  il modello sono correlate, non identiche.
- La prova 2 («l'hai finita di nuovo: è ancora probabile, ma dopo la fotocopiatrice»): va verificato che non si legga
  come «il dettaglio ha reso l'IA creativa». Il sostegno viene dai dati: la stessa idea di P.S. in 2 su 5, la macchina
  che si inceppa o si blocca in 3 su 5.
- **«Non chiederle di essere originale»: attenzione ai nostri dati.** Da solo «originale» cambia il vestito e non il
  contenuto (C2: sveglia 5 su 5 con Opus). Insieme al dettaglio, invece, sembra aiutare la trovata: la fotocopiatrice
  scrive la lettera in 3 su 5 con D (dove «originale» è nella prima riga) e in 0 su 5 con D2 (senza). Sono cinque
  campioni, quindi è un indizio. La tesi resta, ma la VOCE va tarata come nel primo reel: «originale» è insufficiente,
  non inutile. Per esempio «non è chiedendolo che cambia il biglietto», e non «chiederlo non serve».
- «Sii originale cambia il vestito»: il verbale con lo stesso titolo in 3 su 5 (C2). «Nuovo» e «originale» non vanno
  detti del vestito (X5). Il contesto delle prove non era neutro: `C2-opus-3` scrive «ufficio universitario» e
  `C2-opus-2` «Roma» (W1). Non si scrive «contesto neutro».
- «Tutte e cinque» (sveglia) e «tre volte su cinque» (verbale) valgono per Opus 5; la caption dichiara modello e data.
  Con Sonnet 5 la sveglia della A2 è 0 su 5.
- «Quella riga gliel'hai data tu» / «la parte nuova l'hai messa tu»: l'ingrediente è tuo, la combinazione del modello
  (T5, V12). In caption: «Il dettaglio l'hai messo tu, la battuta l'ha scritta lei.»
- Il limite della mossa va in caption. La cornice resta («Caro Marco, dopo tanti anni» in 4 su 5 anche con il
  dettaglio), e con Sonnet 5 il dettaglio si attacca al luogo comune (V15).
- Il lato buono del probabile (mail formali, riassunti) deve stare nella VOCE o almeno in caption (punto 32).
- Icone isolate che affermano (T13), la lente al posto del database (S6): se tornano, valgono le stesse cautele.

**Per lo sceneggiatore**
- `docs/stile-parlato.md` oggi è ancora provvisoria (Reel letti: 0); lo stilista la sta rifacendo sui 14 reel di
  reelkit. Rileggila prima di scrivere il monologo.
- Le due reazioni dopo le prove («Visto?», «L'hai finita di nuovo, eh?») sono il posto naturale per l'«io» e il «tu»
  del presentatore, a camera.
- In caption, dalla revisione archiviata: la dichiarazione dei testi («estratti da risposte più lunghe di Claude
  Opus 5, 14 settembre 2026: le parole sono sue, i tagli nostri», V3), il criterio corretto (sopra), il limite con
  Sonnet (V15), la riga di V12, il lato buono del probabile. Consigliata V17: in 10 risposte su 10 della A2 il modello
  chiede qualcosa di Marco, cioè la mossa del reel la suggerisce lui stesso.
