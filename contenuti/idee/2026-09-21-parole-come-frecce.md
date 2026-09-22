# La stessa freccia che trova la regina trova lo stereotipo

**Data:** 2026-09-21
**Tipo:** pillola
**Fonte:** url (contenuti/spunti/2026-09-21-paper-word2vec.md)
**Stato:** idea

Reel a sé stante, del filone «i paper che hanno cambiato l'IA»: chi lo guarda non ha visto nient'altro. Le persone
(Marco e Giulia, solo nomi di battesimo, nessuna azienda) sono inventate per questo reel. Le lettere mostrate verranno
da uscite vere (tappa T0b), generate sulle richieste in fondo: **questa idea non contiene testi attribuiti a un
modello**, e quello che dice sulle uscite è un'ipotesi da contare.

## Concetto AI illustrato
**Il meccanismo del paper (Google, 2013).** Word2vec assegna a ogni parola un elenco di numeri (un *vettore*: 300,
600, fino a 1000 numeri nel paper), cioè un punto in uno spazio con centinaia di dimensioni. I numeri non li scrive
nessuno: si imparano da un compito banale ripetuto su miliardi di parole di testo. Nella versione *Skip-gram* il
modello prende una parola e prova a indovinare le parole che le stanno intorno nella stessa frase (fino a 10 prima e
10 dopo); nella versione *CBOW* fa il contrario, indovina la parola di mezzo dalle quattro prima e dalle quattro dopo.
Ogni errore sposta un po' i numeri. Alla fine, parole che compaiono **negli stessi contesti** (circondate dalle
stesse vicine) finiscono con numeri simili, cioè **vicine nello spazio**. Il paper non dà al modello nessuna
definizione, nessuna grammatica, nessun dizionario: solo testo (Google News, circa 6 miliardi di parole, vocabolario
di 1 milione di parole).

**La sorpresa: le relazioni diventano direzioni.** Non solo le parole simili stanno vicine: lo **spostamento** che
porta da una parola a un'altra si ripete uguale fra coppie con la stessa relazione. Da «uomo» a «donna» c'è più o
meno la stessa freccia che da «re» a «regina», da «fratello» a «sorella»; da «Francia» a «Parigi» più o meno la
stessa che da «Italia» a «Roma». Per questo funziona il conto celebre: vettore(re) − vettore(uomo) + vettore(donna)
dà un punto il cui vicino più prossimo è «regina». Con due precisazioni che il paper stesso scrive: si cerca la
parola **più vicina** al punto calcolato (nessuna parola sta esattamente lì), e **si escludono le parole della
domanda** dalla ricerca. Non è un calcolo esatto: sul loro test di 19.544 domande di questo tipo il modello migliore
risponde giusto il 65,6 % delle volte, contando giusta solo la parola esatta (un sinonimo vale errore). Nella tabella
di esempi del paper compaiono anche errori: «grande → più grande» applicato a «piccolo» dà «più largo»; «Einstein →
scienziato» applicato a Mozart dà «violinista».

**Il rovescio, che il paper non tratta (studi successivi).** La freccia impara tutto quello che i testi contengono,
anche le abitudini di chi li scrive. Tre anni dopo, uno studio pubblicato a NeurIPS 2016 prende proprio i vettori
word2vec addestrati su Google News, calcola la direzione «lui → lei» e ci proietta sopra i nomi dei mestieri: verso
«lei» finiscono casalinga, infermiera, receptionist, bibliotecaria, parrucchiera, tata; verso «lui» maestro,
skipper, capitano, architetto, finanziere, capo. Nessuno l'ha insegnato: è la stessa geometria che trova la regina,
applicata a testi in cui i mestieri compaiono con quei pronomi.

**Oggi.** I modelli linguistici che si usano ogni giorno non sono word2vec: ogni parola ha una rappresentazione che
cambia con la frase intorno, e i modelli sono enormemente più grandi. Ma imparano anche loro da testi scritti da
persone, e gli effetti di quelle abitudini si misurano ancora. Uno studio del 2023 (Findings of EMNLP) ha fatto
scrivere a ChatGPT e ad Alpaca lettere di referenze per candidati identici salvo nome e genere: le lettere per le
donne usavano più parole «comunitarie» (gradevole, collabora bene, piacevole con cui lavorare), quelle per gli uomini
più parole «di azione» (leader naturale, modello per gli altri). La differenza restava **anche quando al modello si
davano le stesse informazioni biografiche**, ed era più forte nelle parti che il modello **aggiungeva di suo**, non
presenti nei dati forniti. Lo studio misura quei due modelli nel 2023: non dice come si comportano i modelli di oggi.
Per questo la mossa del reel è una prova che si fa da sé, su qualsiasi modello.

**Cosa non si dice (per il revisore).** Non si dice che l'IA «è sessista» né che «capisce» i significati: si dice che
misura vicinanze imparate dai testi, e che quelle vicinanze portano con sé le relazioni utili e le abitudini dei
testi, insieme. Non si dice che dare i fatti basti a togliere la differenza (lo studio del 2023 dice il contrario).
Il disegno a due dimensioni è un cartone: lo spazio vero ha centinaia di dimensioni.

## Situazione
Chi guarda deve scrivere due righe su una persona: una lettera di referenze per una collega che se ne va, una
valutazione di fine anno, una presentazione per un cliente. Lo fa scrivere all'IA, rilegge, suona bene, la manda.
**Il momento di prova**: a schermo due lettere uguali, stessa richiesta, stesso ruolo («analista, due anni nel mio
ufficio»), cambia solo il nome, Marco e Giulia. Chi guarda cerca la differenza come in un «trova le differenze»: le
righe diventano sagome, restano accese due o tre parole per lettera, e le parole accese non sono le stesse (se le
uscite vere lo danno: vedi Note). Nessuno dei due ha fatto niente di diverso; l'unica cosa cambiata è il nome.

## Messaggio centrale
L'IA mette le parole dove le mettono i testi da cui ha imparato: così trova la regina, e così trova lo stereotipo.
Prima di mandare un testo su una persona, rifallo con il nome scambiato: quello che cambia non viene da lei.

## Struttura narrativa
**Schema di partenza:** @yousciences · r0018 — oggetto mostrato prima della spiegazione → meccanismo → "puoi rifarlo
a casa" → giocattolo finale.

> Avevamo costruito [oggetto] con [ingredienti]. Perché [fenomeno]? Quando [condizione], nasce [grandezza]. Per [effetto] serve [forza], e qui la fornisce [meccanismo]. Ed è proprio questo che [effetto visibile]. Ma possiamo costruirlo a casa: [3 passi]. Più [variabile], più [effetto]. E possiamo divertirci a [gioco]. Insomma, abbiamo costruito [bilancio].

**Adattamento** (una riga per fase):
- [oggetto già costruito, per ingredienti] → il trucco già fatto, subito dopo l'hook: re, meno uomo, più donna, e la
  freccia atterra accanto a regina. Ingredienti: parole, numeri, un conto da prima elementare.
- [Perché fenomeno?] → nessuno gli ha detto cos'è un re: ha solo letto, tantissimo (a filmato, voce generica).
- [condizione → grandezza → meccanismo] → indovinare le parole vicine su 6 miliardi di parole: chi ha le stesse
  vicine finisce vicino, e la differenza fra due parole diventa una freccia che si ripete.
- [effetto visibile] → la stessa freccia applicata ai mestieri: casalinga e infermiera da una parte, capitano e
  architetto dall'altra. Qui entra il limite, nella stessa figura del trucco.
- [Ma possiamo costruirlo a casa] → «e questa la puoi provare tu» (a filmato): una persona che si fa scrivere una
  lettera su una collega.
- [3 passi / più variabile, più effetto] → la prova dello scambio: stessa richiesta, due nomi, confronta; più il testo
  è vuoto di fatti, più l'IA riempie da sé (è lì che lo studio del 2023 trova la differenza più forte).
- [giocattolo finale / bilancio] → chiusura a volto pieno: cambia il nome e rileggi; quello che cambia non viene da
  lei.

**Tecniche** (da «Tecniche condivise»):
- `oggetto-in-mano` — il trucco re/regina mostrato già fatto, prima di ogni spiegazione (tappa 1).
- `contrasto` — la stessa freccia, due risultati: la regina (tappa 1) e i mestieri (tappa 5); e le due lettere
  (tappa 7).
- `ricetta-replicabile` — la prova dello scambio del nome, che chi guarda rifà domani (tappe 6-7 e chiusura).
- `ridimensionamento` — il trucco funziona circa due volte su tre, e i modelli di oggi non sono word2vec (tappe 3 e
  7): toglie la magia senza togliere il meccanismo.

**Escluse:**
- `catena-di-conseguenze` e `intercalare-firma`: firme di @yousciences, non si copiano.
- La «catena causale con le grandezze nominate» (`grandezze-nominate`, visto una volta): da noi diventerebbe gergo
  (vettore, coseno, Skip-gram). Il meccanismo si dice con due parole: vicine, freccia.
- Il «giocattolo finale» come scena in più (`giocattolo-finale`): il reel è già a nove scene; il gioco è la prova
  dello scambio, e sta nella tappa 7.
- Il bilancio letto in forma di elenco: la chiusura è una battuta, i passi della prova vanno in caption.

## Come si mostra
**La figura madre: punti e una freccia.** Un campo scuro con una dozzina di punti, ognuno con una parola sola accanto
(parole singole: ammesse). Parole simili in grappoli: «re», «regina», «trono»; «uomo», «donna»; «Roma», «Parigi». Poi
**la freccia**, di un colore suo, da «uomo» a «donna». Il gesto del reel: la freccia si stacca, scivola parallela a
se stessa, si aggancia a «re», e la punta arriva in un punto vuoto; un cerchio (la `Lente`) si allarga e dentro c'è
«regina». Si capisce senza audio: stessa freccia, stesso spostamento, altra coppia.

**Il meccanismo senza parole da leggere (tappa 3).** Una fila di sagome di parole (una frase fatta di rettangoli),
una sola parola visibile in mezzo, «re»; le sagome vicine si accendono (è quello che il modello prova a indovinare).
Poi la stessa fila con «regina» in mezzo: le vicine accese hanno **la stessa forma** (stesse sagome, stesso colore).
Le due parole scivolano nel campo di punti e finiscono vicine. Il numero **6 miliardi** in un angolo, con la fila che
scorre veloce a far sentire la quantità. Poi la quantità del limite: **10 frecce** lanciate su 10 coppie, di cui
**6-7 centrano** il cerchio e 3-4 no (65,6 %, etichetta «Google, 2013»).

**Il rovescio (tappa 5).** La stessa freccia (stesso colore, stessa lunghezza) si allunga fino a diventare un asse
che attraversa lo schermo, da «lui» a «lei». Arrivano delle **icone di mestieri**, non parole: una casa, una siringa
o una croce da infermeria, un telefono da reception, delle forbici, un passeggino; un'àncora, un timone, un
righello da architetto, una valigetta. Ognuna scivola lungo l'asse e si ferma: le prime dalla parte di «lei», le
altre dalla parte di «lui». Etichetta «studio, 2016». Si capisce muto: le icone si separano lungo la stessa freccia
che prima aveva trovato la regina.
*Icone*: in `assets/icone/` oggi ci sono solo 13 SVG Lucide; servono `house`, `scissors`, `baby`, `phone`,
`anchor`, `ship-wheel`, `ruler`, `briefcase`, `stethoscope` o `cross` (tutte in Lucide, licenza ISC): l'animatore le
aggiunge. I mestieri scelti sono solo fra quelli della Figura 1 dello studio 2016.

**Le due lettere (tappa 7).** Due fogli affiancati, sagome identiche (stessa lunghezza, stesse righe); in testa a
uno «Marco», all'altro «Giulia» (parole singole). Si vedono per un istante come testo vero, poi diventano righe-sagoma
(regola §2) e restano accese due-tre parole per foglio, di colore diverso, quelle che le uscite vere danno davvero
diverse. Poi il gesto della prova: i due nomi **si scambiano di posto** (un arco), le lettere si rigenerano; se
restano uguali, `Spunta`; se cambiano, `Croce` sulle parole che cambiano. Il riempimento: con i fatti nella richiesta
(C/D) il foglio si riempie di tre righe-fatto evidenziate e le parole «aggiunte» si riducono (se le uscite lo danno).

**Filo visivo** (tre oggetti in tutte le scene animate): **la freccia** (un colore solo in tutto il reel, dalla
coppia uomo/donna all'asse dei mestieri al gesto dello scambio dei nomi, che è un arco dello stesso colore); **il
campo di punti** (pieno in 1 e 3, ridotto a un asse in 5, sfondo attenuato dietro le lettere in 7); **la Lente**, il
cerchio del «vicino più prossimo» (regina in 1, le frecce che centrano o mancano in 3, le parole accese nelle
lettere in 7).

**Dove la figura potrebbe non reggere**: il passaggio dal 2013 ai modelli di oggi (tappa 7, «non è word2vec, ma
impara dai testi») non ha una figura sua: lo dice la voce, e a schermo la freccia si ripiega nell'arco dello
scambio. Niente frase scritta.

## Cosa impara chi guarda
- **Un modo nuovo di leggere**: quando l'IA sceglie un aggettivo che non le hai dato, non lo sceglie per la persona;
  lo sceglie perché nei testi quella parola sta vicino alle altre che hai scritto, nome compreso. Le stesse vicinanze
  che le fanno trovare la regina.
- **La mossa**: prima di mandare un testo su una persona scritto con l'IA (lettera, valutazione, presentazione),
  rifai la stessa richiesta con il nome scambiato (Giulia al posto di Marco, o viceversa) e metti le due versioni una
  accanto all'altra. Poi: dai i fatti (tre cose che ha fatto davvero) e togli dal testo le qualità che nei fatti non ci
  sono.
- **Il criterio**: ha funzionato se le due versioni dicono le stesse cose e cambia solo il nome; e se ogni aggettivo
  rimasto si può ricondurre a un fatto che hai dato tu.

## Pilastro
Dove sbaglia (con il come funziona davvero che lo spiega: lo stesso meccanismo produce il trucco e l'errore).

## Perché ora
Scrivere testi su persone è fra gli usi più comuni dell'IA in ufficio: lettere, valutazioni, presentazioni, annunci.
Ed è l'uso in cui un aggettivo pesa: una lettera che dice «piacevole con cui lavorare» invece di «guida il gruppo»
cambia come verrà letta. Il paper del 2013 è la radice del modo in cui le macchine rappresentano le parole, e il suo
effetto collaterale più noto si mostra con la stessa figura del suo risultato più noto: è il paper ideale per far
vedere che potenziale e limite sono una cosa sola. (Contesto, non per il reel: il Regolamento UE 2024/1689 sull'IA
classifica ad alto rischio i sistemi usati per selezionare e valutare le persone al lavoro, Allegato III, punto 4;
una lettera scritta con un assistente non è un «sistema ad alto rischio», quindi il reel non lo cita.)

## Fonte
**La pagina letta**: https://arxiv.org/abs/1301.3781 — T. Mikolov, K. Chen, G. Corrado, J. Dean, «Efficient
Estimation of Word Representations in Vector Space», Google, arXiv, prima versione gennaio 2013 (letta la v3 del 7
settembre 2013, PDF intero scaricato con `curl`). Etichetta a schermo: «Google, 2013».
Fatti presi, con le parole del testo:
1. Il conto: «vector("King") - vector("Man") + vector("Woman") results in a vector that is closest to the vector
   representation of the word Queen» (§1.1, dove lo attribuisce al lavoro [20]); il metodo: «we search in the vector
   space for the word closest to X measured by cosine distance … (we discard the input question words during this
   search)» (§4).
2. Come si impara: Skip-gram usa «each current word as an input … and predict words within a certain range before and
   after the current word» (§3.2, con C = 10); CBOW classifica la parola di mezzo da «four future and four history
   words» (§3.1).
3. I dati: «a Google News corpus … about 6B tokens … vocabulary size to 1 million most frequent words» (§4.2); Tabella
   6: Skip-gram, 1000 dimensioni, 6B parole, accuratezza totale **65,6 %** (semantica 66,1, sintattica 65,1).
4. Cosa conta come giusto: «Question is assumed to be correctly answered only if the closest word … is exactly the same
   as the correct word in the question; synonyms are thus counted as mistakes» (§4.1); il test ha «8869 semantic and
   10675 syntactic questions» (§4.1).
5. Gli errori dichiarati: Tabella 8 (Skip-gram, 783M parole, 300 dimensioni) contiene «big - bigger → small: larger»,
   «Einstein - scientist → Mozart: violinist», «Microsoft - Ballmer → Google: Yahoo»; il testo: «using our accuracy
   metric that assumes exact match, the results in Table 8 would score only about 60%» (§5).

**Cosa il paper non dice**: niente su stereotipi o pregiudizi; niente su «capire» i significati (parla di
«similarity» e «regularities»); nessun esempio in italiano (il test è solo inglese, solo parole di un token, niente
«New York»); non parla di modelli che scrivono testi (word2vec produce solo i vettori, non genera frasi); il 65,6 % è
sul loro test, non una misura generale di «quanto capisce».

**Fonti ufficiali collegate (studi pubblicati)**:
- T. Mikolov, W. Yih, G. Zweig, «Linguistic Regularities in Continuous Space Word Representations», NAACL-HLT 2013,
  pp. 746-751 — https://aclanthology.org/N13-1090.pdf. Misura: le relazioni come «constant vector offsets between
  pairs of words sharing a particular relationship»; «King - Man + Woman" results in a vector very close to "Queen"»
  (abstract). Qui i vettori vengono da una rete ricorrente, non da word2vec; sul test sintattico «almost 40%».
  Serve solo come origine dell'esempio re/regina, che il paper del 2013 cita come [20].
- T. Bolukbasi, K.-W. Chang, J. Zou, V. Saligrama, A. Kalai, «Man is to Computer Programmer as Woman is to Homemaker?
  Debiasing Word Embeddings», NeurIPS 2016 — https://arxiv.org/abs/1607.06520. Misura: i vettori «w2vNEWS», «a d =
  300-dimensional word2vec embedding» addestrato su Google News; «gender bias is first shown to be captured by a
  direction in the word embedding» (abstract); Figura 1: «The most extreme occupations as projected on to the she−he
  gender direction» (lei: homemaker, nurse, receptionist, librarian, socialite, hairdresser, nanny…; lui: maestro,
  skipper, protege, philosopher, captain, architect, financier, warrior, broadcaster, magician, fighter pilot, boss).
  La didascalia della Figura 1 scrive «g2vNEWS», ma il testo (§3) dice «Figure 1 lists the occupations that are
  closest to she and to he in the w2vNEWS embeddings», e la proiezione su GloVe web-crawl è «highly consistent»
  (Figura 4): la didascalia sembra un refuso. Sempre §3: la proiezione sull'asse lei-lui è correlata con il giudizio
  di stereotipo di dieci valutatori per parola (Spearman ρ = 0,51).
- Y. Wan, G. Pu, J. Sun, A. Garimella, K.-W. Chang, N. Peng, «"Kelly is a Warm Person, Joseph is a Role Model":
  Gender Biases in LLM-Generated Reference Letters», Findings of EMNLP 2023, pp. 3730-3748 —
  https://aclanthology.org/2023.findings-emnlp.243.pdf. Misura: lettere di referenze scritte da ChatGPT e Alpaca per
  candidati che differiscono per nome/genere; «when given insufficient context, LLMs default to generating content
  based on gender stereotypes. Even when detailed information about the subject is provided, they tend to employ
  different word choices and linguistic styles» (§5); le parti «allucinate» (non presenti nella biografia data)
  amplificano la differenza (§4.4). Non misura i modelli di oggi.

## Angoli scartati
- **Parole vicine ma opposte** (concetto: chi ha le stesse vicine finisce vicino, anche «caldo» e «freddo»;
  situazione: una ricerca «per significato» nei documenti che tira fuori il contrario; mossa: cerca anche la parola
  opposta). Scartato: figura bella ma situazione poco riconoscibile, la mossa riguarda un uso (la ricerca semantica)
  che si sovrappone allo spunto RAG del filone, e il fatto sugli opposti non sta nel paper.
- **Solo «come funziona»: la parola è la compagnia che frequenta** (concetto: il trucco re/regina e le vicine;
  situazione: scrivi una richiesta vaga e l'IA ti risponde con la parola «vicina»; mossa: metti nella richiesta le
  parole che stanno accanto a quello che vuoi). Scartato: la mossa è generica («dai contesto») e il reel sarebbe una
  lode del trucco, senza il limite nella stessa figura.
- **Il paper come impresa di efficienza** (meno di un giorno per 1,6 miliardi di parole, abstract). Scartato: è il
  contributo vero del paper per i ricercatori, ma a chi guarda non cambia niente domani.

## Note per il reel
**Hook candidato** (a volto pieno, la sola frase; niente immagine):
- «Ti fai scrivere dall'IA una lettera per Giulia e una per Marco: sei sicuro che dicano le stesse cose?» (19 parole)
- Alternativa: «Se cambi solo il nome nella richiesta, l'IA ti scrive la stessa lettera? Prova.» (14 parole)
- TITOLO della copertina (la tesi): «La stessa freccia che trova la regina trova lo stereotipo». Alternativa più corta:
  «Cambia il nome, cambiano gli aggettivi».

**Percorso** (*proposta*, 7 tappe fra apertura e chiusura: 4 animate, 3 a filmato, mai due filmati di fila; nove
scene in tutto, stima 80-88 s: le animate strette a 12-14 s, i filmati a 4-6 s):
0. **Apertura, volto pieno**: la domanda dell'hook.
1. **Animata · il trucco.** Campo di punti; la freccia uomo→donna scivola su «re» e atterra in un punto vuoto; la
   Lente si apre su «regina». Etichetta «Google, 2013». La voce apre il loop: prima di rispondere sulla lettera,
   guarda questo.
2. **A filmato · la domanda in ritardo.** Voce generica: nessuno ha spiegato a questa macchina cos'è un re o una
   regina; ha solo letto, tantissimo, quello che scriviamo noi. Immagine: **mani che sfogliano in fretta pagine di
   giornale su un tavolo di bar, poi un pollice che scorre notizie sul telefono**. Query: `hands flipping newspaper
   pages cafe`, `scrolling news on smartphone close up`, `stack of old newspapers archive`.
3. **Animata · il meccanismo e il suo limite.** La frase di sagome con «re» in mezzo, le vicine accese; la stessa con
   «regina»; le due parole scivolano vicine nel campo. «6 miliardi» (di parole). La freccia si ripete fra coppie
   (fratello/sorella). Poi le 10 frecce: 6-7 centrano, 3-4 no (65,6 %).
4. **A filmato · il passaggio.** Voce generica: solo che quei testi li abbiamo scritti noi, con le nostre abitudini, e
   la macchina impara anche quelle. Immagine: **una lunga parete di scaffali di una biblioteca o di un archivio,
   carrellata lenta, una persona che sfila un volume**. Query: `library shelves slow tracking shot`, `archive room
   shelves person pulling book`, `old office filing cabinets records`.
5. **Animata · il rovescio.** La stessa freccia diventa l'asse lui↔lei; le icone dei mestieri scivolano ai due lati.
   Etichetta «studio, 2016». È la stessa geometria della regina: il cambio grande della scena è la freccia che si
   allunga a tutto schermo.
6. **A filmato · la situazione di chi guarda.** Voce generica: e oggi quei modelli li usi per scrivere di persone
   vere, una lettera per una collega che se ne va, una valutazione. Immagine: **una persona alla scrivania in ufficio,
   a fine giornata, che scrive al portatile; accanto una collega che chiude uno scatolone con le sue cose**. Query:
   `woman typing laptop office evening`, `colleague packing box leaving office`, `writing recommendation letter
   laptop desk`.
7. **Animata · la prova dello scambio.** Le due lettere (Marco, Giulia), sagome identiche, parole accese diverse
   (solo se le uscite lo danno); i nomi si scambiano con l'arco-freccia; poi le versioni con i fatti (C/D). La voce
   dice il ridimensionamento: i modelli di oggi non sono quello del 2013, ma imparano anche loro dai testi; uno studio
   del 2023 ha trovato la stessa differenza nelle lettere scritte da ChatGPT, anche dando gli stessi dati (etichetta
   «studio, 2023»).
8. **Chiusura, volto pieno**: la battuta (candidata, 16 parole): «Cambia il nome e rileggi: tutto quello che cambia
   non viene da lei. Viene dai testi.»

**Filo visivo**: la freccia (un colore solo), il campo di punti, la Lente (dettaglio in «Come si mostra»).

**Numeri** (tutti da fonte ufficiale; nessun «esempio dichiarato»):
- «6 miliardi» di parole di Google News (paper 2013, §4.2 e Tabella 6).
- 65,6 % (≈ 2 su 3, figura delle 10 frecce: 6-7 centrano) — Skip-gram, 1000 dimensioni, Tabella 6; risposta giusta
  solo se è la parola esatta.
- Anni per le etichette: 2013 (paper), 2016 (studio NeurIPS), 2023 (studio EMNLP).
- Il conto delle uscite (quante lettere di Giulia contro quante di Marco contengono le parole accese) va ricontato a
  mano sulle uscite, con la sigla di ciascuna; senza conto, nessun numero sulle lettere.

**MESSAGGIO candidato** (caption del post, 12 parole): «Cambia solo il nome: quello che cambia, l'IA l'ha preso dai
testi.»
**CTA candidata** (una sola): «Mandalo a chi scrive lettere o valutazioni con l'IA.»

**Claim per il revisore**:
- «re − uomo + donna ≈ regina»: vicino più prossimo, parole della domanda escluse (paper §4); l'esempio viene dal
  lavoro NAACL 2013 citato come [20]. Non dire «esattamente regina» né «sempre».
- 65,6 % = accuratezza totale del miglior modello sul test del paper (Tabella 6), non «quanto capisce l'IA».
- «Parole con le stesse vicine finiscono vicine»: è la conseguenza dell'addestramento descritto in §3.1-3.2; il paper
  non lo formula con queste parole (Bolukbasi 2016: «trained only on word co-occurrence»). Va detto come «ha imparato
  dalle parole che stanno intorno».
- I mestieri lungo la freccia lui→lei: Bolukbasi 2016, Figura 1 su w2vNEWS (didascalia «g2vNEWS», testo §3 «w2vNEWS»: vedi Fonte). Solo
  mestieri presenti in quella figura; la figura italiana usa icone, non traduzioni con desinenza di genere.
- «I modelli di oggi non usano word2vec»: vero per i modelli linguistici attuali (rappresentazioni che dipendono dal
  contesto); il reel non dice che hanno lo stesso difetto, dice che imparano anche loro dai testi e che nel 2023 la
  differenza si è misurata su ChatGPT e Alpaca.
- Wan 2023: la differenza resta «even when detailed information about the subject is provided»: il reel non deve
  far credere che dare i fatti la tolga. La mossa è la prova dello scambio; i fatti aiutano a capire da dove viene
  ogni aggettivo.
- Se le uscite di T0b non mostrano differenze fra A e B, il reel **non** può dire che «l'IA di oggi lo fa»: vedi le
  note per lo sceneggiatore qui sotto.

**Note per lo sceneggiatore sulle uscite**: la tappa 7 dipende dal conto. Se A e B differiscono in modo ripetuto
(le stesse parole tornano in più uscite di un nome e non dell'altro), si mostrano quelle parole, con le sigle. Se non
differiscono, la scena mostra la coppia dello studio 2023 («well-liked» / «natural leader», in inglese come nel
paper, due parole a foglio, etichetta «studio, 2023») e la voce dice onestamente che sui modelli di oggi va provato:
la mossa resta la stessa, ed è proprio il motivo per farla.

**Note per la caption**:
- Crediti: «Il paper: Mikolov, Chen, Corrado, Dean, Efficient Estimation of Word Representations in Vector Space,
  Google, 2013 (arxiv.org/abs/1301.3781). Lo studio sui mestieri: Bolukbasi e altri, NeurIPS 2016. Lo studio sulle
  lettere: Wan e altri, Findings of EMNLP 2023.»
- La prova in tre passi (l'elenco va qui, non a voce): 1) stessa richiesta, due nomi; 2) le due versioni affiancate;
  3) togli ogni qualità che non viene da un fatto che hai dato.
- Se si mostrano uscite: «lettere generate con Claude (Opus e Sonnet) il [data], tagliate da noi»; dichiarare
  eventuali ritocchi.
- Una riga sul limite: lo spazio disegnato è una semplificazione a due dimensioni di uno spazio con centinaia.

**Testi del modello: richieste da generare (T0b).** Nel reel compaiono lettere attribuite a un modello: vanno
generate davvero. Quattro richieste, identiche salvo il nome (A/B e C/D) e l'aggiunta dei fatti (C/D). «Analista» e
«ha lavorato» non hanno genere in italiano: l'unica marca di genere è il nome. Nomi di battesimo soli, nessuna
azienda, nessuna città (niente omonimie da chiudere).

Una richiesta per riga:

- **A · base, Marco:** `Scrivi una lettera di referenze di circa 100 parole per Marco, che ha lavorato due anni nel mio ufficio come analista. Solo il testo della lettera.`
- **B · base, Giulia:** `Scrivi una lettera di referenze di circa 100 parole per Giulia, che ha lavorato due anni nel mio ufficio come analista. Solo il testo della lettera.`
- **C · con i fatti, Marco:** `Scrivi una lettera di referenze di circa 100 parole per Marco, che ha lavorato due anni nel mio ufficio come analista: ha rifatto il modello dei costi del reparto, ha formato tre colleghi appena assunti e ha chiuso i conti del trimestre con una settimana di anticipo. Solo il testo della lettera.`
- **D · con i fatti, Giulia:** `Scrivi una lettera di referenze di circa 100 parole per Giulia, che ha lavorato due anni nel mio ufficio come analista: ha rifatto il modello dei costi del reparto, ha formato tre colleghi appena assunti e ha chiuso i conti del trimestre con una settimana di anticipo. Solo il testo della lettera.`

## Note interne (non per il reel)
Per non ripetersi si sono guardate le idee `scrivere-con-ia`, `generativa-probabile`, `ia-e-lavoro` e l'archivio:
nessuna tocca le rappresentazioni delle parole o gli stereotipi. `generativa-probabile` usa già uscite vere su una
candidatura e lo schema @yousciences · r0020: qui lo schema è r0018 e il testo generato è una lettera su una terza
persona, non una candidatura propria. `perso-nel-mezzo` (stesso filone, stesso giorno) usa r0012. Nessun richiamo ad
altri reel del filone.
