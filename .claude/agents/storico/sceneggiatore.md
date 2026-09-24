# Storico delle lezioni · sceneggiatore

Copia integrale della sezione «Lezioni dalle sessioni» di `.claude/agents/sceneggiatore.md` com'era il 2026-09-21, prima del
riordino in «Regole in vigore». **Gli agenti non caricano questo file**: è la cronaca (chi ha detto cosa, su quale
reel, cosa è stato superato e da cosa). Le lezioni nuove si aggiungono in fondo, con la data, quando serve ricordare
il *perché* di una regola; la regola stessa vive nell'agente.

## Lezioni dalle sessioni
- **2026-09-13, primo reel** (archiviato in `contenuti/archivio/generativa-non-creativa/sceneggiatura.md`):
  - Il **filo visivo** proposto nelle Note di produzione (carta «richiesta», biglietto, colonna delle candidate) ha
    funzionato: il presentatore ha apprezzato molto il flusso delle animazioni. Proponilo sempre.
  - Il revisore ha bocciato «Il testo lo produce lei: nuovo, sì» detto del biglietto banale: un aggettivo sul
    risultato («nuovo», «originale», «creativo») va verificato sul caso che si mostra. Parla del processo (lo
    scrive, non lo recupera) quando il risultato non regge l'aggettivo; vale anche per le etichette `TESTO:`.
  - **La chiusura non ha convinto**: messaggio + tre mosse elencate in una carta + CTA, detto come una lista di
    consigli. Troppo didascalico, «poco linguaggio da reel». Non chiudere con un elenco letto a camera: la lista va
    in caption. Il presentatore ha scelto una chiusura a punchline sulla persona («L'IA non ha mai conosciuto Marco.
    Tu sì.»), un hook che parla al «tu» e il payoff letto a voce e mostrato grande (`docs/linguaggio-reel.md` §3).
- **2026-09-13, riscrittura dopo l'anteprima** (stesso file: scene 1, 6 e 7 dai blocchi di `docs/linguaggio-reel.md` §3):
  - Il payoff letto a voce e la chiusura a battuta costano secondi: tre scene riscritte hanno portato il reel da 55 a
    60 s, il massimo. Con un payoff e una chiusura da 4 frasi, le scene di spiegazione vanno tenute corte fin dalla
    prima stesura; se si deve tagliare, la frase candidata è la più astratta.
  - Se togli dalla VOCE un claim già approvato per far posto alla battuta (qui «sceglie ancora tra le prime»),
    faglielo portare da un oggetto del filo visivo («la» che vola dalla testa della colonna). Poi segnalalo al
    revisore con le scene che lo reggono ancora: non deve sparire in silenzio.
  - Nel brief va solo ciò che la libreria ha o sta per avere. Una funzione che non c'è (il riquadro grande) va nelle
    Note di produzione come «quando ci sarà», mai come richiesta. Se il fotogramma 0 è già pieno (titolo intero), la
    prima frase chiede comunque un movimento: sennò è un beat senza cambio.
  - `valida` ora ha i controlli di linguaggio: hook con un «tu» o una domanda, MESSAGGIO ≤ 12 parole, VOCE della
    chiusura ≤ 18 (era 25 fino al 2026-09-14). Il MESSAGGIO può essere solo la battuta («L'IA non ha mai conosciuto Marco. Tu sì.»), perché alla
    mossa concreta basta la VOCE. Se una frase della chiusura spiega la mossa dopo i due punti («è da lì che cambia
    la frase»), la spiegazione è la prima cosa da tagliare.
- **2026-09-14, dopo la seconda anteprima**: la chiusura di 20 parole in 4 frasi durava 7,8 s con la voce di prova,
  oltre i 6-7 s consigliati, e il presentatore l'ha fatta accorciare. Da allora `valida` avvisa sopra le 18
  parole (prima 25): una chiusura a battuta sta in **~15 parole** (18 è il massimo di `valida`). Per tagliare, la mossa generale diventa un pronome che
  riprende la battuta («Tu sì. / Scrivilo nella richiesta.» al posto di «Scrivi nella richiesta quello che sai solo
  tu.»): la generalizzazione la portano l'immagine e la caption. La battuta finale non si taglia.
- **2026-09-14, i biglietti generati davvero**: i due biglietti del primo reel li avevamo scritti noi, e su 16 uscite
  vere (Opus 5 e Sonnet 5) nessuna conteneva «oggi si chiude un capitolo» né «Lei no.». Il presentatore ha preferito i
  testi veri, anche a costo di rifare le scene 2-7. Da ora ogni testo che la VOCE attribuisce a un modello («Comincia
  così: …», «Ora scrive: …») viene da un'uscita vera, **generata prima di scrivere la scena**: più uscite per
  richiesta (3-5), si sceglie fra quelle, con i tagli dichiarati nelle Note di produzione. Il luogo comune giusto è
  quello che torna in quasi tutte le uscite (la sveglia: 6 su 6), non quello che ci aspettiamo noi.
  - Le revisioni del presentatore hanno comunque l'ultima parola: se ritocca un testo del modello («il caffè potrai
    berlo sul divano» al posto di «berlo caldo»), lo applichi così com'è e lo dichiari nelle note e in caption;
    non gli opponi la regola delle uscite vere. Evita anche le parole ripetute fra le richieste: «originale» nella
    prima richiesta toglieva forza a «Sii originale.» nella scena 5.
- **2026-09-15, la VOCE letta a camera era «molto poco umana»**: registrando il primo reel con `reel registra`, il
  presentatore ha trovato il parlato recitato. Le VOCE erano titoli in fila («Vuol dire probabile.», «Fluente, sì. /
  Originale, no.», «Il testo non lo cerca: lo scrive lei.»): i vincoli stretti (una frase = un beat, ≤ 35 parole,
  60 s) premiavano la compressione e la compressione produce epigrammi. Da allora: prima il monologo, poi i beat;
  limiti a 50 parole/90 s; `valida` avvisa sulle frasi da titolo, su «X, sì. Y, no.» e sui due punti come snodo. La
  verifica vera è il presentatore che legge in `reel registra`: se inciampa, la sceneggiatura non passa.
- **2026-09-15, reset dei contenuti e corsa completa**: il primo reel è in `contenuti/archivio/`, le lezioni sopra
  restano valide. Le idee ora le scrive l'`ideatore` da uno spunto (link, righe del presentatore, tema): se l'idea ha
  una sezione `## Fonte`, i fatti del reel vengono da lì e non si aggiungono numeri che la fonte non ha. Con
  `/pipeline … --tutto` nessuno rilegge la sceneggiatura prima del revisore: le frasi di cui sei meno sicuro vanno
  nel rapporto, perché il presentatore le legge solo nel report finale. Prima del monologo leggi
  la guida di stile distillata dal corpus (poi tolta con la VOCE passata al copione).
- **2026-09-15, `generativa-probabile`, prima sceneggiatura con la guida distillata dal corpus**: l'hook «fatto,
  poi domanda corta» della guida nuova sta nelle 20 parole. Il revisore ha segnalato due frasi che a voce si
  capiscono al contrario o dipendono da una scena prima: «Quindi scrivilo tu, nella richiesta» (si sente «scrivi tu
  il biglietto»; meglio «diglielo tu») e «Al suo posto scrivi…» (rimanda a una carta di un'altra scena). Rileggi le
  frasi con un pronome come le sentirebbe chi guarda senza lo schermo.
- **[SUPERATA il 2026-09-21: l'apertura è il presentatore a tutto schermo, vedi la regola in fondo]** **2026-09-19, nota del presentatore sull'apertura**: i primi 5-10 secondi
  devono catturare l'attenzione. L'hook è **un problema o una domanda** posta a chi guarda (non la tesi, non un
  preambolo), e lo sfondo in quel momento è **una clip che richiama quel problema**: la scena si vede prima di
  capirla. Scrivi l'apertura pensando alle due cose insieme: la VOCE pone il problema, la riga `ANIMAZIONE:`
  dell'apertura descrive **cosa si vede nel filmato** (soggetto, luogo, gesto: è da lì che `broll piano` prende le
  query), non una grafica da disegnare. La spiegazione animata comincia dopo, quando l'attenzione c'è già. Se
  l'apertura sta in due scene (hook + prima spiegazione), il filmato copre quella che pone il problema.
  Decisione del presentatore sullo stesso punto (hook a filmato, `docs/sceneggiatura.md` §2): nell'apertura **non
  c'è titolo a schermo**, c'è lui nel riquadro sopra la clip. Quindi nell'hook: niente `RIQUADRO: no`, niente
  `TESTO:`, la `VOCE:` deve reggere da sola (il problema lo dice lui), il `TITOLO:` lo scrivi per la copertina, e la
  riga `ANIMAZIONE:` descrive la clip senza nominare il titolo (se lo nomina, `broll piano` lascia l'hook animato).
- **2026-09-19, scene a filmato (`[broll]`, `docs/sceneggiatura.md` §2)**: animazione e filmato si alternano fra
  scene e non stanno mai insieme. Tu non scrivi `[broll]`: scrivi `[spiegazione]`. Ma una scena che **non ha niente
  da disegnare** (nessun meccanismo, quantità o figura: una scena d'attenzione, un'esperienza riconosciuta) scrivila
  perché possa andare a filmato: brief `ANIMAZIONE:` di **una riga** che descrive un'immagine filmabile (chi, dove,
  che gesto), e **nessun `TESTO:`** — sopra il filmato non va grafica, e `broll scrivi` una scena con `TESTO:` non la
  converte. Mai due scene così di fila. **Dal 2026-09-21 il tetto è diventato un obiettivo: le scene a filmato sono
  circa metà del reel** (vedi la regola in fondo).
- **2026-09-19, nota del presentatore: «la voce narrante deve risultare più umana e naturale»** (detta davanti
  all'anteprima di `generativa-probabile`, scritta con la sola guida distillata). Le regole non bastano a dare
  l'orecchio: da qui in poi leggi le trascrizioni vere prima del monologo (sopra) e fai la **prova dell'orecchio**
  dopo. Cosa tradiva la VOCE come scritta, in quel reel: le antitesi in coppia («Non sbagli a fartela scrivere, ci
  mancherebbe. / Sbagli se pensi che basti…»), le frasi tutte chiuse e della stessa misura, la metafora a effetto
  («Cambia il vestito, ma…»), la battuta che ferma la scena a ogni scena. Cosa fa chi parla davvero, nelle
  trascrizioni: frasi che si allungano con «che… e che…», il soggetto ripreso in coda, domande fatte a se stesso,
  «tra l'altro» e «appunto», un numero preciso al posto dell'aggettivo, e una frase su tre che non conclude niente ma
  porta alla successiva. Il limite di 50 parole per scena resta: il parlato naturale non è più lungo, è **meno
  simmetrico**. Non aggiungere intercalari a pioggia per sembrare parlato: uno o due per scena, dove servono a
  respirare.
- **2026-09-19, regola del presentatore: «ogni reel è a sé stante, non c'è una storia temporale continua»** (detta
  alla fermata 1 di `scrivere-con-ia`, la cui idea riprendeva azienda e vicenda di `generativa-probabile`: «il posto
  l'hai avuto»). Chi guarda un reel non ha visto gli altri: niente personaggi, aziende o vicende che proseguono da
  un reel all'altro, niente «come dicevamo», «la volta scorsa», «ricordi la mail?». Se serve un concetto già
  spiegato altrove, lo ridici in una frase come se fosse la prima volta. Nomi e situazioni inventati sono nuovi a
  ogni reel.

### 2026-09-20 · corse `scrivere-con-ia` e `generativa-probabile` (tre ❌ e un ❌ del revisore)
- **Un contatore non cambia metro di nascosto.** Se un numero a schermo conta una cosa («frasi tornate uguali») non può
  riapparire più avanti a contarne un'altra («frasi scritte da lei») con la stessa etichetta: l'etichetta dice il metro,
  cambia a vista, e dove il metro vecchio darebbe un numero scomodo il valore si spegne. Un valore iniziale si mostra
  solo se è vero con quell'etichetta («– su 5», non «5 su 5», prima che ci sia qualcosa da contare).
- **Un conto non sta accanto alla citazione di una sola uscita.** «10 su 10» vicino alla frase di C2 si legge «dieci su
  dieci hanno detto questo». Il conto si attacca alla cosa contata (le parole segnalate); la citazione entra dopo, senza
  numero accanto. Lo stesso per un'etichetta «4 su 10» vicino a una frase intera: agganciala alla sola parola contata.
- **La mossa della fonte si attribuisce.** Se la mossa del reel è il metodo dell'autore citato, la VOCE lo dice («ed è da
  lui che prendo la mossa»); non si presenta come nostra né come versione più mite della sua.
- **Un diagramma con conti veri afferma anche la sua forma.** Un bivio «6 · 3 · 1» disegnato a partire dal saluto di
  UNA uscita dice che tutte e dieci sono passate di lì: il nodo di partenza dev'essere comune a tutte le uscite contate
  (un'etichetta «saluto», non il saluto di A10), le etichette dei rami alla lettera («(vi) scrivo…» se due su sei dicono
  «vi scrivo»), e la didascalia dice cosa si è contato («dopo il saluto · 10 prove, 2 modelli»). Se i due modelli non
  concordano, il conto per modello va in caption.
- **Artefatti dello strumento nelle uscite.** `claude -p` passa al modello nome, email e connettori dell'account (Drive,
  Gmail) anche con `--tools ""`: le uscite possono contenere «mi chiamo Nome Cognome», offerte di salvare la bozza in
  Gmail, commenti sull'indirizzo universitario. Non sono prove né pro né contro la tesi; a schermo si tagliano (taglio
  dichiarato) e la caption dice che lo strumento li passava. Una formula come «quello che non le hai scritto, non lo sa»
  va scritta sapendo che le app hanno memoria, profilo e connettori.
- **Scene a filmato: query in inglese nelle Note.** Per l'hook e per ogni scena scritta per il filmato metti nelle Note
  di produzione 2-3 query in inglese (soggetto, azione, luogo): il coordinatore le mette in `piano.json`. Le parole
  italiane del brief non bastano («persona in piedi vicino alla finestra» ha riportato piedi nudi).
- **Obiettivo di durata.** Due corse su due sono uscite a 84-86 s con l'idea che chiedeva ≤ 75: la voce di prova poi
  ha dato 74,6 s su 86 stimati (la stima a 2,8 parole/s è larga). Non comprimere il parlato per la stima; elenca i tagli
  pronti e lascia decidere al presentatore.

### 2026-09-20 · REGOLA DEL PRESENTATORE: niente testo denso a schermo
Flavio, sull'anteprima di `scrivere-con-ia`: una mail intera che resta a schermo per scene intere non va. Quando il
filo visivo è un documento (mail, richiesta, annuncio, elenco), il brief `ANIMAZIONE:` dice **a ogni beat quale
frammento resta leggibile** (poche parole, quelle di cui parla la VOCE) e che il resto diventa righe-sagoma o esce. Il
documento intero si vede per un istante, quando entra. Scrivi testi-esempio corti: una bozza di 78 parole è già troppa
da mostrare; bastano le due-tre frasi che il reel usa davvero, con «[…]» dichiarato.

### 2026-09-20 · REGOLA DEL PRESENTATORE: a voce e a schermo solo fonti ufficiali
Flavio, su `scrivere-con-ia`: il post di una persona qualunque (Ptacek) è uno spunto di riflessione, non un'autorità.
**Nel reel non si cita**: niente nome in VOCE o a schermo, niente «secondo X», niente sue frasi come punch. Il credito va
nelle note per la caption («l'idea viene da un post di …», con il link). La mossa si presenta per quello che è, senza
paternità: non «me la sono inventata io», non «uno dice che». In VOCE e a schermo si nominano solo fonti ufficiali
(istituzioni, studi pubblicati, istituti di ricerca), e solo quando reggono un numero. Questa regola supera la lezione
«la mossa della fonte si attribuisce» qui sopra: l'attribuzione si fa in caption, non nel reel.

### 2026-09-21 · REGOLA DEL PRESENTATORE: i due registri stanno a metà, e si dividono anche il parlato
Nota di Flavio davanti ai due reel del regime muto (`ia-e-lavoro` e `scrivere-con-ia`, entrambi 2 scene a filmato su
7: troppo poche, cinque scene animate di fila).

**L'equilibrio.** Circa **metà delle scene va a filmato**, con una scena di tolleranza in più o in meno. Non è un
tetto da non superare, è il bersaglio: `valida` e `broll piano` avvisano anche quando i filmati sono **troppo pochi**.
Il numero di scene non è fisso: se per stare a metà ne servono otto o nove invece di sette, **aggiungile senza
allungare il reel** — le scene a filmato sono corte (4-7 s), quelle animate si tengono i 12-16 s. Otto scene in 80 s
valgono più di sei in 85. Resta tutto il resto: mai due scene a filmato di fila, mai `TESTO:` sopra un filmato, e il
tipo `[broll]` non lo scrivi tu (scrivi `[spiegazione]` con un brief filmabile, lo converte `broll scrivi`).

**La divisione del parlato — è questa la parte che cambia come scrivi la VOCE.**
- Nelle scene **a filmato** la voce dice le cose **generiche**: il problema di chi guarda, l'esperienza riconosciuta,
  la conseguenza, il passaggio da un blocco all'altro, la presa di posizione. **Niente numeri, niente conti, niente
  termini tecnici, nessun meccanismo**: sono proprio quelli che fanno restare la scena a Manim — `broll piano` cerca
  nel testo cifre e parole tecniche e non propone a filmato le scene che ne hanno. Una sola frase con un numero,
  messa lì per comodità, ti sbilancia il reel.
- Nelle scene **animate** va la **spiegazione complessa**: il meccanismo, le quantità, i confronti, i conti, tutto
  ciò che si capisce solo vedendolo disegnato. Lì la voce può essere densa, perché la figura la regge.
Quando scrivi il monologo, **dividilo in blocchi prima di tagliarlo in scene**: i pezzi che spiegano vanno insieme e
diventano scene animate; i pezzi che raccontano, riconoscono o concludono diventano le scene a filmato in mezzo. Se
un blocco «generico» contiene un numero, o lo sposti nella scena animata accanto o lo togli.

**Nelle Note di produzione** dichiara la divisione: quali scene proponi a filmato e perché la loro voce è generica,
e le query in inglese per ciascuna (`broll piano` le ricava dalle parole italiane del brief e Pexels le capisce male).

### 2026-09-21 · REGOLA DEL PRESENTATORE: apertura e chiusura sono lui, a tutto schermo
Detta da Flavio subito dopo quella dei registri a metà. **I due estremi del reel sono suoi**: si vede lui a tutta
tela che guarda in camera (`RIQUADRO: pieno`, il default di `hook` e `chiusura`: non devi scriverlo). Supera la
regola del 2026-09-19 sull'hook a filmato.
- **Apertura**: la VOCE pone il problema o la domanda di chi guarda, detta in faccia (hook ≤ 20 parole, come sempre).
  **Niente riga `ANIMAZIONE:` e niente `FIGURA:`**: non c'è niente da disegnare né una clip da cercare, e un brief che
  descrive un filmato è un avanzo del regime vecchio. Il `TITOLO:` resta obbligatorio ma è per la copertina.
- **Chiusura**: la VOCE dice la conclusione guardando in camera (≤ 18 parole), con le caption, **e nient'altro**:
  niente messaggio a schermo (decisione del presentatore dopo la prima anteprima, stessa sera). Niente `ANIMAZIONE:`
  e niente `FIGURA:`. `MESSAGGIO:` e `CTA:` restano obbligatori ma sono il testo per la **caption del post**: il
  messaggio in forma memorabile, la CTA come invito scritto. Quindi la chiusura deve reggersi **a voce**: la battuta
  finale è quella che dice lui, e l'ultima figura del reel sta nell'ultima scena animata prima.
- **L'equilibrio fra i registri non li conta**: la metà e metà si misura sulle scene in mezzo. Quindi con un corpo di
  7 scene ne servono 3 o 4 a filmato; il reel intero ne ha 9.
- La scena dopo l'apertura parte da uno stacco (dalla faccia alla prima figura, o al primo filmato): non c'è uno
  stato da riprendere. Lo stesso prima della chiusura.

## 2026-09-22 · perso-nel-mezzo
- Alla revisione Flavio chiede «ma che cos'è il "brano"?»: la parola veniva dal *passage* del paper. Diventa
  «paragrafo» in VOCE, a schermo e nelle note; la mossa resta «pezzo» perché parla del documento di chi guarda.
- Il revisore dà ❌ su «Poi chiedile la frase esatta da cui ha preso la risposta»: la citazione sembrava già la
  verifica. Riformulata in «…da cui l'ha presa, e cercala nel documento», accettata da Flavio.

## 2026-09-22 · gpu-comprare-o-affittare · clip senza volti, wow tecnologico
Sulle clip provvisorie del reel GPU (ragazzo sul divano, donna all'auto, uomo addormentato alla scrivania) Flavio:
«se non espressamente richiesto, meglio scegliere clip che non mostrano volti umani; preferire qualcosa che contiene
del tecnologico wow in funzione al resto». Regola in docs/regole-editoriali.md §3; negli agenti cosa cambia.

## 2026-09-22 · gpu-comprare-o-affittare · volto coperto e VOCE rivista registrando
Dopo la prima presa Flavio: «non voglio che leggi i fotogrammi dove compare il mio volto»; la revisione della VOCE si
fa in `reel registra` (tasto E, fuori dalla presa), le caption dal testo recitato, `reel parlato --applica` lo riporta
nel .md. Regole in docs/regole-editoriali.md §8-9; codice in fotogrammi.copri_volto, registra_app, monta.voce_recitata.

## 2026-09-22 · gpu-comprare-o-affittare · il rapporto esterno sul parlato
Un consulente ha riscritto la voce del reel GPU: troppo scritta, frasi lunghe, poche volte il «tu», nessuna
micro-pausa. Flavio ha accettato la direzione e ha deciso: limiti più larghi (hook 25 parole, 6 beat, reel 100 s),
«GPU» e «cloud» ammessi, l'eco che non conta come frase da titolo. Regole nel tema «VOCE e orecchio»; la sezione
«Come suona il parlato da social» stava nella guida di stile, poi tolta. Il reel GPU è stato riscritto e va registrato di nuovo.

## 2026-09-23 · la VOCE passa al copione
Flavio trovava che la VOCE scritta dai modelli Claude non suonasse abbastanza da social. Prova alla cieca sul reel
GPU, stesso brief e sei trascrizioni di reelkit (`contenuti/prove-parlato/gpu-comprare-o-affittare/`): la sua
classifica è stata gpt-5.4, deepseek-v4-pro, gemini-3.1-pro, e per ultima la VOCE dello sceneggiatore (grok-4.7 non
ha risposto per il 402 di Poe). Decisione: la pipeline diventa spunto → idea → **copione** → sceneggiatura; il
parlato lo scrive `uv run reel copione` con la catena in quell'ordine, e la sceneggiatura si adatta al copione.
Superate e tolte: «prima di scrivere la VOCE ascolta il parlato vero» (le trascrizioni ora vanno nel prompt del
copione) e «VOCE = parlato vero, prima il monologo e poi i beat» (le regole di scrittura stanno in
`templates/copione.md`). Le regole «VOCE e orecchio» restano, per leggere il copione e segnalare.

## 2026-09-23 · gpu-comprare-o-affittare · la scarsità nella scena 3
Flavio: i chip gialli della scena 3 «brutti e posizionati male», e «una scheda video con dei chip mancanti non
trasmette proprio bene l'idea della scarsità». Proposte tre figure (scaffale, torta, coda): scelto lo scaffale di
negozio; il revisore l'ha bocciato (❌: scarsità nei negozi senza fonte, NVIDIA Q4 FY2026 parla di scorte sane nei
canali) e ha proposto la rastrelliera d'uscita della produzione, accettata. Regola nel tema «Numeri, conti e
diagrammi»; icone Lucide `memory-stick` e `factory` aggiunte in `assets/icone/`.

## 2026-09-24 · refactoring degli agenti
Tolte dall'agente le date fra parentesi, i limiti numerici (li controlla `reel valida`, fonte `LIMITI`) e le regole
che ripetevano `docs/regole-editoriali.md` o `docs/sceneggiatura.md` §5 (restano i rimandi). Superate e tolte: «nessun
personaggio, le idee dei caroselli in chat diventano materiale per le animazioni» (regime vecchio; resta la regola
generale in regole §10), «l'hook fatto + domanda corta della guida di stile» (guida tolta), il limite «chiusura più
lunga di 18 parole» dello schema (oggi in LIMITI).
