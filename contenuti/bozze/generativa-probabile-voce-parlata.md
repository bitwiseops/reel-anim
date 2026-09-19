# generativa-probabile — proposta di VOCE più parlata

Proposta del 2026-09-19, dopo la nota del presentatore davanti all'anteprima: «la voce narrante deve risultare più
umana e naturale». **È solo una proposta da leggere ad alta voce**: la sceneggiatura
`contenuti/sceneggiature/2026-09-15-generativa-probabile.md` (stato: animato) non è stata toccata, e nemmeno
`contenuti/animazioni/generativa-probabile.py`.

Vincoli rispettati: stesso numero di righe VOCE per scena, ogni riga dice la stessa cosa nello stesso ordine, le
parole che l'animazione accende restano nella loro riga, nessun fatto e nessun numero nuovo, i testi del modello
(A1 nella scena 1, C4 nella scena 5) identici parola per parola.

## Cosa ho ascoltato

Trascrizioni lette per intero (`uv run reel stile --trascrizioni --lingua it`), otto reel di sei account:

| id | account | durata | passo |
|---|---|---|---|
| r0037 | @marcocamisanicalzolari | 98 s | 3,3 parole/s (è il reel da cui viene lo schema dell'idea) |
| r0041 | @ingegneria.italia | 74 s | 2,8 |
| r0036 | @ifarmsrlai | 55 s | 2,9 |
| r0014 | @gianluigiballarani | 100 s | 3,1 |
| r0024 | @inregola.it | 78 s | 2,5 |
| r0025 | @inregola.it | 98 s | 2,6 |
| r0001 | @simorizzo_ai | 87 s | 2,5 |
| r0048 | @gabrysolution | 66 s | 3,4 |

Più `docs/stile-parlato.md`. Dalle trascrizioni ho preso il passo, non le frasi.

**Tre mosse del parlato che ho usato**

1. **«Non è che…, è che…»: la correzione detta in una frase sola, al posto dell'antitesi in due frasi gemelle.**
   Da r0048: «E prima di giudicarmi lasciami spiegare perché non è che nessuno mi volesse bene. Ero io.» (e r0037
   assolve con un inciso, non con una frase a specchio: «non hanno sbagliato in realtà a usare l'intelligenza
   artificiale. Capita a tutti, no?»). Usata nella scena 4, righe 1-2.
2. **La frase che si appoggia a quella di prima: il connettivo in testa risponde alla scena precedente**, così una
   scena non ricomincia da capo. Da r0025: «Ed è qui che viene il bello. Perché quel passaporto italiano che hai in
   mano ti dà un vantaggio…»; da r0024: «Ma aspetta, perché la parte più assurda deve ancora arrivare.» Usata
   all'inizio della scena 3 («Perché lei scrive…» risponde a «non basta chiederglielo») e della scena 5 («Allora
   togli…» risponde a «non le hai ancora detto niente»).
3. **La cosa ripresa in coda, o indicata con «questo» e «lì», e l'inciso detto quasi a parte.** Da r0001: «ne è
   stato risolto solamente uno di questi problemi» e «che ci ha impiegato ben sette anni e che tra l'altro, una
   volta vinto, ha rifiutato…»; da r0024: «Breaking Bad una cosa ce l'ha insegnata.» Usata in «Finiscila tu, questa
   frase» (scena 1), «finisce lì, accanto a…» (scena 2), «e due, tra l'altro, con la stessa frase» (scena 4),
   «Eccola, una mail che parla di te» (scena 6).

In più, dalla guida: la parola chiave che torna («colloquio» ridetta nella scena 2; nel corpus 30 reel su 30) e
l'ultimo membro della terna più forte («e non sa nemmeno perché…», scena 3).

Cosa ho tolto, seguendo la lezione del 2026-09-19: la coppia «Non sbagli a… / Sbagli se…», la metafora «Cambia il
vestito», l'ellissi da epigramma «probabile, ma probabile dopo…». Intercalari aggiunti in tutto il reel: due («tra
l'altro», «nemmeno»); «Guarda,» della scena 3 è uscito per far posto a «Perché».

---

## Scena 1 [hook] — 20 → 20 parole

| # | VOCE di oggi | p | VOCE proposta | p |
|---|---|---|---|---|
| 1 | Ti fai scrivere la candidatura dall'IA? Finisci tu la frase. | 10 | Ti fai scrivere la candidatura dall'IA? Finiscila tu, questa frase. | 10 |
| 2 | Allego il mio curriculum e resto a disposizione per un… | 10 | *(invariata: è il testo di A1, un cartellino a parola)* | 10 |

Monologo: «Ti fai scrivere la candidatura dall'IA? Finiscila tu, questa frase. Allego il mio curriculum e resto a
disposizione per un…»

Cosa cambia: «questa frase» in coda indica quello che sta per scriversi a schermo; l'imperativo con il clitico e la
ripresa è come lo si dice a voce («finiscila tu, questa»), quello di oggi è un'istruzione scritta. Stesse 10 parole.

## Scena 2 — 44 → 46 parole

| # | VOCE di oggi | p | VOCE proposta | p |
|---|---|---|---|---|
| 1 | Colloquio, vero? Hai fatto un po' quello che fa lei. | 10 | *(invariata)* | 10 |
| 2 | Io gliel'ho chiesta dieci volte, e c'era in ==tutte e dieci==. | 11 | Io gliel'ho chiesta dieci volte, e colloquio c'era in ==tutte e dieci==. | 12 |
| 3 | E la tua mail finisce accanto a quelle degli altri. | 10 | E la tua mail finisce lì, accanto a quelle degli altri. | 11 |
| 4 | E una mail che parla di te? Si può, ma non basta chiederlo. | 13 | E una mail che parla di te? Si può, ma non basta chiederglielo. | 13 |

Monologo: «Colloquio, vero? Hai fatto un po' quello che fa lei. Io gliel'ho chiesta dieci volte, e colloquio c'era in
tutte e dieci. E la tua mail finisce lì, accanto a quelle degli altri. E una mail che parla di te? Si può, ma non
basta chiederglielo.»

Cosa cambia: «c'era» aveva il soggetto sottinteso (chi ascolta senza guardare non sa cosa c'era): ridire
«colloquio» è quello che fa chi parla, e cade sul colpo dei quattro «colloquio» a schermo; «lì» indica la pila;
«chiederglielo» è la forma detta («chiederlo» a chi?). Era già la scena più vicina al parlato: la tocco poco.

## Scena 3 — 41 → 42 parole

| # | VOCE di oggi | p | VOCE proposta | p |
|---|---|---|---|---|
| 1 | Guarda, lei scrive una parola alla volta, e ne prende una delle più ==probabili==. | 14 | Perché lei scrive una parola alla volta, e ne prende una delle più ==probabili==. | 14 |
| 2 | Per questo la mail viene fluente, ma se non gliel'hai detto, non sa da quanti anni lavori, | 17 | Per questo la mail viene fluente. Ma se non gliel'hai detto, non sa da quanti anni lavori, | 17 |
| 3 | non sa dove, e non sa perché vuoi proprio loro. | 10 | non sa dove, e non sa nemmeno perché vuoi proprio loro. | 11 |

Monologo: «Perché lei scrive una parola alla volta, e ne prende una delle più probabili. Per questo la mail viene
fluente. Ma se non gliel'hai detto, non sa da quanti anni lavori, non sa dove, e non sa nemmeno perché vuoi proprio
loro.»

Cosa cambia: la scena non riparte con un «Guarda,» ma risponde alla domanda lasciata aperta un attimo prima («non
basta chiederglielo» — «Perché lei scrive…»); il punto dopo «fluente» fa una frase corta e poi una lunga (oggi è una
sola frase di 27 parole su due righe) e mette «Per questo» solo su «fluente», come chiedeva il revisore al punto 13;
«nemmeno» rompe la terna a specchio e carica l'ultimo membro. Il testo della correzione ❌ 14 («se non gliel'hai
detto») resta alla lettera.

## Scena 4 — 45 → 49 parole

| # | VOCE di oggi | p | VOCE proposta | p |
|---|---|---|---|---|
| 1 | Non sbagli a fartela scrivere, ci mancherebbe. | 7 | Non è che sbagli a fartela scrivere, ci mancherebbe, | 9 |
| 2 | Sbagli se pensi che basti «sii originale». | 7 | è che non basta dirle «sii originale». | 7 |
| 3 | Io l'ho fatto, e una mail su due comincia con un ==divano==, | 12 | *(invariata)* | 12 |
| 4 | e due con la stessa frase. | 6 | e due, tra l'altro, con la stessa frase. | 8 |
| 5 | Cambia il vestito, ma del tuo lavoro non le hai ancora detto niente. | 13 | L'inizio è cambiato, ma del tuo lavoro non le hai ancora detto niente. | 13 |

Monologo: «Non è che sbagli a fartela scrivere, ci mancherebbe, è che non basta dirle «sii originale». Io l'ho fatto,
e una mail su due comincia con un divano, e due, tra l'altro, con la stessa frase. L'inizio è cambiato, ma del tuo
lavoro non le hai ancora detto niente.»

Cosa cambia: è la scena che la lezione del 2026-09-19 indica per nome. Le due frasi gemelle «Non sbagli… / Sbagli
se…» diventano una frase sola su due beat («non è che…, è che…»), che è come ci si corregge parlando; «sbagli se
pensi che basti» diventa «non basta», che è la stessa taratura del revisore (insufficiente, non inutile) e la stessa
parola del MESSAGGIO; «tra l'altro» fa dire la riga 4 «quasi a parte», come già chiedeva la nota per il presentatore;
la metafora «Cambia il vestito» diventa la cosa che si vede («L'inizio è cambiato»): è un claim più stretto di
quello approvato al punto 22, non più largo. «dirle» prepara «dille un fatto vero» della scena 5.

## Scena 5 — 33 → 34 parole

| # | VOCE di oggi | p | VOCE proposta | p |
|---|---|---|---|---|
| 1 | Togli «sii originale» e dille un fatto vero che sai solo tu. | 12 | Allora togli «sii originale» e dille un fatto vero che sai solo tu. | 13 |
| 2 | Tipo che hai portato una newsletter a duemilacento iscritti. | 9 | *(invariata)* | 9 |
| 3 | Ora scrive: in un anno ho portato gli iscritti da trecento a… | 12 | *(invariata: è il testo di C4, un cartellino a parola)* | 12 |

Monologo: «Allora togli «sii originale» e dille un fatto vero che sai solo tu. Tipo che hai portato una newsletter a
duemilacento iscritti. Ora scrive: in un anno ho portato gli iscritti da trecento a…»

Cosa cambia: solo «Allora», che lega la mossa al «non le hai ancora detto niente» di un attimo prima; oggi la scena
parte con un imperativo a freddo. Il resto era già parlato («Tipo che…»).

## Scena 6 — 27 → 29 parole

| # | VOCE di oggi | p | VOCE proposta | p |
|---|---|---|---|---|
| 1 | Duemilacento, vero? | 2 | *(invariata)* | 2 |
| 2 | È ancora una parola probabile, ma probabile ==dopo il tuo numero==. | 11 | È ancora una parola probabile, ma stavolta è probabile ==dopo il tuo numero==. | 13 |
| 3 | Ecco una mail che parla di te, e il numero ce l'hai messo tu. | 14 | Eccola, una mail che parla di te, e il numero ce l'hai messo tu. | 14 |

Monologo: «Duemilacento, vero? È ancora una parola probabile, ma stavolta è probabile dopo il tuo numero. Eccola, una
mail che parla di te, e il numero ce l'hai messo tu.»

Cosa cambia: «probabile, ma probabile dopo…» era un'ellissi da scritto (la seconda metà senza verbo); con «stavolta
è» diventa una frase che si dice, e la ripetizione di «probabile» resta (è il tag `formula-ripetuta`). «Eccola, una
mail…» è la ripresa in coda: risponde alla domanda «E una mail che parla di te?» della scena 2 con la stessa forma.

## Scena 7 [chiusura] — 16 → 16 parole

| # | VOCE di oggi | p | VOCE proposta | p |
|---|---|---|---|---|
| 1 | La prima era scritta bene. | 5 | *(invariata)* | 5 |
| 2 | Solo che poteva firmarla chiunque. | 5 | *(invariata)* | 5 |
| 3 | Questa la puoi firmare solo tu. | 6 | *(invariata)* | 6 |

Cosa cambia: niente. È la battuta finale, l'unico posto dove l'aforisma è voluto (§5, punto 3), ha già «Solo che» e
«Questa la puoi», che sono forme parlate, e ogni frase regge un passaggio da ≥ 0,9 s. Una sola variante possibile,
se al presentatore suona secca: «La prima era scritta bene, per carità.» (+2, chiusura a 18 parole, il massimo: il
14 settembre una chiusura lunga l'ha già fatta accorciare, quindi non la propongo).

---

## Prova dell'orecchio

Ho messo ogni monologo accanto a una trascrizione e ho guardato lunghezze, simmetrie e frasi che chiudono.

- **Scena 1** contro r0024 («Hai mai visto Breaking Bad? Bene, è ambientata in New Mexico.»): domanda al «tu» e
  subito una frase corta che la usa. Regge.
- **Scena 2** contro r0014 («E allora la studentessa gli ha chiesto… e si è offerta…»): tre frasi su quattro
  cominciano con «E», come lì; lunghezze 2-8-12-11-7-6. Regge. Resta scritto «Colloquio, vero?» (vedi sotto).
- **Scena 3** contro r0037 («Ma non sapeva niente di quella montagna. Un modello non guarda il sentiero, non sente il
  caldo e non sa che…»): frase corta (6 parole) e poi la terna lunga (22), con l'ultimo membro diverso. Oggi era
  14 + 27.
- **Scena 4** contro r0048 («non è che nessuno mi volesse bene. Ero io. Ogni decisione la prendevo da sola…»):
  lunghezze 16-20-13, nessuna frase gemella. Oggi erano 7-7-18-13, con le prime due a specchio.
- **Scena 5** contro r0025 («Quindi fai la pratica e ti ritrovi con…», «Beh, tanto per cominciare…»): imperativo
  preceduto dal connettivo, poi l'esempio. Regge.
- **Scena 6** contro r0025 («È legale? Certo che sì. Semplicemente nessuno te l'aveva detto.»): domanda corta,
  risposta, frase che chiude sul «tu». Regge; la più scritta resta la riga 1.
- **Scena 7**: battuta finale, confrontata con la chiusa di r0014 («ma adesso gli esseri umani stanno imparando a
  scrivere peggio, pur di non sembrare…»): lì la battuta è una frase lunga, da noi sono tre corte. È una scelta
  (chiusura a battuta, `docs/linguaggio-reel.md`), non un residuo.

## Verifica

Copia fuori da `contenuti/`:
`/private/tmp/claude-501/-Users-bitwise-Projects-reel-anim/eb386097-51f2-458f-a3f0-12b83aa22de4/scratchpad/voce/2026-09-15-generativa-probabile.md`
(le 14 righe sostituite con `sostituisci.py`, nella stessa cartella; ogni riga di partenza trovata una volta sola).

| | originale | copia con la VOCE proposta |
|---|---|---|
| `uv run reel valida` | [OK] 0 errori, 0 avvisi | [OK] 0 errori, 0 avvisi |
| avvisi di linguaggio (frasi da titolo, «X, sì. Y, no.», due punti come snodo) | 0 | 0 |
| parole di voce | 226 | 236 |
| per scena | 20/44/41/45/33/27/16 | 20/46/42/49/34/29/16 |
| durata stimata | 86 s (86,3) | 90 s (89,9): **+4,2 %**, sotto il 10 % e sotto il limite di 90 |

236 è il tetto: con 237 parole la stima passa i 90 s e `valida` avvisa. Con la voce di prova l'anteprima di oggi dura
73,6 s; in proporzione la proposta sta intorno ai 77 s.

**Gli avvisi di linguaggio erano già zero prima**: `valida` non vede quello che il presentatore ha sentito (frasi
gemelle, metafora, ellissi). Il controllo automatico qui non distingue le due versioni; le distingue solo la lettura
ad alta voce.

### Cosa deve sapere l'animatore (se la proposta passa)

Gli inizi dei beat restano una riga = un beat, quindi i brief valgono tutti. Ma
`contenuti/animazioni/generativa-probabile.py` aggancia gli accenti **all'indice della parola dentro la riga**
(`self.tempi(i)[k]`), non alla parola: dove una riga guadagna parole prima dell'ancora, l'indice va spostato. Sono sei
numeri; tutte le attese hanno già il tetto `min(…, self.limite(i) − x)`, quindi senza ritocco niente si rompe, l'accento
cade solo una o due parole prima.

| Scena · riga | Ancora | Indice oggi | Indice nuovo |
|---|---|---|---|
| 2 · riga 2 | fine dell'ingresso dei frammenti / «tutte e dieci» | `t1[7]` / `t1[8]` | `t1[8]` / `t1[9]` |
| 2 · riga 3 | «accanto» | `t2[5]` | `t2[6]` |
| 3 · riga 3 | «perché» | `t2[6]` | `t2[7]` |
| 4 · riga 1 | «ci mancherebbe» | `t0[5]` | `t0[7]` |
| 5 · riga 1 | «sii originale» / «un fatto vero» | `t0[1]` / `t0[5]` | `t0[2]` / `t0[6]` |
| 6 · riga 2 | «dopo il tuo numero» | `t1[7]` | `t1[9]` |

Invariati tutti gli altri indici (controllati uno per uno: scena 1 «candidatura» 4 e «Finiscila» 6; scena 2 riga 1 e
riga 4; scena 3 righe 1 e 2; scena 4 righe 2, 3 e 5; scena 5 righe 2 e 3; scena 6 riga 3). Le scene 2-6 vanno
comunque rigenerate con `anima`, perché la voce di prova cambia durata.

Per il revisore, se si applica: nessun fatto nuovo, ma tre giunture da rileggere — «Perché lei scrive…» (scena 3:
lega «non basta chiederglielo» al meccanismo, è la tesi del reel ma oggi il nesso non è detto), «è che non basta
dirle» al posto di «sbagli se pensi che basti» (scena 4: cade il secondo «sbagli» dello schema
`assolvere-prima-di-accusare`, resta l'assoluzione), «L'inizio è cambiato» al posto di «Cambia il vestito» (più
stretto del claim approvato al punto 22).

## Dove NON sono riuscito a migliorare senza rompere un vincolo

Sono le righe dove per suonare più dette servirebbe ritoccare anche l'animazione.

- **Scena 2 riga 1 «Colloquio, vero?» e scena 6 riga 1 «Duemilacento, vero?»**: sono le due righe più «da copione»
  del reel (la parola nuda, poi «vero?», due volte). Ma il punch «COLLOQUIO» parte al fotogramma 0 della scena 2 e
  «2.100» occupa da solo gli 1,8 s della riga: la parola deve restare in testa e la riga non può allungarsi. Per
  dirle in modo più sciolto («Hai detto colloquio, vero?», «E qui hai pensato duemilacento, no?») bisogna spostare
  il punch di qualche decimo: lavoro dell'animatore.
- **Scena 1 riga 2 e scena 5 riga 3**: testi del modello (A1 e C4), un cartellino a parola: non si toccano per
  regola. «Ora scrive:» è l'unica parte nostra, ma i cartellini partono da `t2[2]`: anche solo «E adesso lei scrive:»
  sposta dieci ancore.
- **Scena 5 riga 2 «Tipo che hai portato una newsletter a duemilacento iscritti.»**: cinque ancore sulla riga
  (`t1[0]`, «portato», «newsletter», «duemilacento», «iscritti») perché il fatto si scrive nella carta insieme alla
  voce. È già parlata; ogni parola in più sposta la scrittura.
- **Scena 3 righe 2-3, la terna «non sa… non sa… non sa»**: è il punto più recitato che resta. Tre segnaposto si
  accendono uno per membro e il testo della riga 2 è la correzione ❌ 14 alla lettera, quindi ho potuto solo
  spezzare la frase e aggiungere «nemmeno». Detta davvero sarebbe più sbilanciata («…non sa da quanti anni lavori,
  né dove, e soprattutto non sa perché…»), ma «né dove» toglie il secondo «non sa» su cui si accende «[azienda/e]»
  e sposta il confine fra i due beat.
- **Scena 4 riga 3 «Io l'ho fatto, e una mail su due comincia con un divano,»**: invariata. La versione che direi
  al bar è «Io ci ho provato, e una mail su due mi comincia con un divano,» (+2), ma la scena 4 è a 49 parole su 50
  e il reel a 236 su 236. Qui il vincolo è la durata, non l'animazione: servirebbe togliere un beat alla scena (la
  riga 4, che le note di produzione indicano già come prima candidata al taglio) e quindi rifare l'animazione.
- **Scena 7**: lasciata com'è per scelta (vedi sopra).

### Varianti più larghe, se il presentatore accetta di superare i 90 s stimati

Ognuna è indipendente; tutte insieme fanno 241 parole, circa 92 s stimati (un avviso di `valida`, +6,6 % sull'originale).

| Scena · riga | Variante | Costo |
|---|---|---|
| 2 · riga 1 | Colloquio, vero? Hai fatto un po' quello che fa lei, l'IA. | +1 (chi è «lei» lo si sente, senza lo schermo) |
| 3 · riga 2 | …fluente. Ma se non gliel'hai detto tu, non sa da quanti anni lavori, | +1 (ritocca il testo della correzione ❌ 14) |
| 4 · riga 3 | Io ci ho provato, e una mail su due mi comincia con un ==divano==, | +2 (scena 4 a 51: sopra il limite, va tolto «tra l'altro») |
| 5 · riga 1 | Allora togli «sii originale» e dille un fatto vero, uno che sai solo tu. | +1 |

## Frasi di cui sono meno sicuro

- «Non è che sbagli a fartela scrivere, ci mancherebbe, / è che non basta dirle «sii originale».»: a voce funziona
  solo se le due righe si dicono di fila senza scendere di tono su «ci mancherebbe» (la riga 1 finisce con la
  virgola apposta). Se il presentatore fa pausa fra i due beat, meglio la forma chiusa: «…ci mancherebbe. / Il guaio
  è pensare che basti «sii originale».» (9 + 8, una parola in più).
- «Perché lei scrive una parola alla volta…»: regge nella presa unica; se la scena 3 viene registrata da sola
  (`--da-scena 3`) comincia con un «Perché» appeso, e va detta ripartendo dalla fine della scena 2.
- «e colloquio c'era in tutte e dieci»: la parola senza articolo è giusta a voce (si cita la parola), sul karaoke
  può sembrare un refuso.

---

# Parte 2 — struttura con i filmati

Proposta su carta del 2026-09-19 (seconda richiesta del coordinatore): il presentatore ha visto che `reel-9x16.mp4`
non ha nessuna clip e le vuole. Come nella Parte 1, **niente è stato toccato**: né la sceneggiatura animata, né
`contenuti/animazioni/`, né `tools/`. Ho riletto le due lezioni del 2026-09-19 in `.claude/agents/sceneggiatore.md`
(apertura con hook a filmato; scene a filmato) e `docs/sceneggiatura.md` §2 (`[broll]` e «L'hook a filmato»).

**Consiglio la versione a 9 scene** (hook a filmato + una scena d'attenzione a filmato a metà). Quella a 8 scene
(solo l'hook a filmato) è scritta in breve più sotto. La VOCE è quella della Parte 1, con i tagli dichiarati qui.

## Le scelte, in breve

- **L'hook nuovo pone una domanda, non un fatto**: «La candidatura te l'ha scritta l'IA, e adesso aspetti. Ma quella
  mail parla di te?» (15 parole). Ho scartato la strada «mandi candidature e non ti risponde nessuno»: direbbe che
  una mail scritta dall'IA riceve meno risposte, e questo il revisore non l'ha mai visto né c'è una fonte
  (la nota al punto 9 della revisione dice proprio che il reel non lo afferma). «E adesso aspetti» è
  l'esperienza riconosciuta, e la clip la mostra; la domanda «parla di te?» è già il filo del reel (etichetta «parla
  di te?», scena 8 «Eccola, una mail che parla di te»), quindi l'hook apre a voce il loop che oggi si apre solo a
  metà.
- **La scena d'attenzione è «E la tua mail finisce lì, accanto a quelle degli altri», non «Non è che sbagli…»**.
  La prima è la posta in gioco e non ha niente da disegnare (oggi, su quel beat, l'animazione fa solo due copie
  grigie a ventaglio); «lì» ora indica la pila che si vede nella clip. La seconda, nella Parte 1, è la prima metà di
  una frase sola su due beat («Non è che sbagli…, / è che non basta dirle…»): uno stacco filmato→animazione la
  spezzerebbe a metà, e su quel beat c'è da disegnare (la carta «richiesta» che si accende senza barrature).
- **La scena d'attenzione va allargata di una frase**: da sola sono 11 parole (4,7 s) e lascia «E una mail che parla
  di te?» senza casa. La domanda chiude la scena a filmato (18 parole, ~7 s), la risposta «Si può, ma non basta
  chiederglielo.» apre la scena animata dopo: lo stacco cade fra domanda e risposta, che è dove uno stacco si regge.
- **Il gioco «finiscila tu» non ripete più l'hook**: «Guarda questa candidatura. L'ultima frase finiscila tu.» (il
  «questo» su quello che si vede, r0020 nella guida; «l'ultima frase» dice quello che l'animazione fa, cioè
  scorrere fino in fondo).

## Dove ho tagliato (la Parte 1 era a 236 parole su 236)

Con 9 scene il tetto scende a **231 parole** (ogni scena costa 0,8 s di stima). Hook nuovo +15, quindi −20 altrove:

| Taglio | Parole | Perché proprio questo |
|---|---|---|
| Scena «sii originale»: tolta la riga «e due, tra l'altro, con la stessa frase.» | −8 | è la prima candidata al taglio già nelle Note di produzione («il conto resta in caption»); la scena passa da 5 a 4 beat |
| Scena «colloquio»: tolto «Hai fatto un po' quello che fa lei.» | −8 | seconda candidata nelle stesse note, ed è il claim ⚠️ 6 del revisore; resta «Colloquio, vero?» da solo, come «Duemilacento, vero?» |
| Vecchio hook: «Ti fai scrivere la candidatura dall'IA? Finiscila tu, questa frase.» → «Guarda questa candidatura. L'ultima frase finiscila tu.» | −3 | la domanda la fa già l'hook nuovo |
| Meccanismo: tolto «nemmeno» | −1 | si torna al testo approvato |

Cosa si perde davvero: **«tra l'altro»** (una delle tre mosse della Parte 1 esce con la sua riga) e **il ponte «hai
fatto quello che fa lei»** fra la prova e il meccanismo. Il ponte lo porta ancora l'immagine: nella scena 5
«colloquio» sta in testa alla colonna e vola nel cursore. Se il presentatore preferisce sforare i 90 s stimati, è la
prima frase da rimettere (+8 parole, ~93 s: un avviso).

## Versione a 9 scene (consigliata)

Le scene a filmato sono scritte `[spiegazione]`/`[hook]` con brief filmabile e senza `TESTO:`: `[broll]` e
`SCHERMO:` li mette `broll scrivi` quando i file esistono.

### Scena 1 [hook] — a filmato · nuova · 15 parole
```
TITOLO: Generativa non vuol dire creativa
VOCE: La candidatura te l'ha scritta l'IA, e adesso aspetti. Ma quella mail parla di te?
ANIMAZIONE: Una ragazza al portatile sul tavolo di casa, di sera, preme invio e resta a fissare la posta in attesa di una risposta, il telefono fermo vicino alla mano.
```
Rispetto a oggi: non esiste. Il TITOLO resta quello di oggi ma vive solo in copertina (`fotogrammi.titola` lo scrive
sopra un fotogramma della clip); niente `RIQUADRO: no`, niente `TESTO:`, il brief non nomina il titolo.

### Scena 2 [spiegazione] — animata · è l'hook di oggi · 17 parole
```
VOCE: Guarda questa candidatura. L'ultima frase finiscila tu.
VOCE: Allego il mio curriculum e resto a disposizione per un…
ANIMAZIONE: Si arriva da uno stacco sul filmato, quindi al primo fotogramma è già tutto in scena, senza ingressi: la carta «richiesta» con «Scrivi la mail per candidarmi a questo annuncio.» e, agganciata sotto e attenuata, la carta «annuncio · inventato» con «Acme Arredi» acceso; più giù la mail con «Oggetto: Candidatura per la posizione di addetto marketing» e «Gentile responsabile della selezione,». Su «candidatura» la carta «richiesta» si accende con un bordo accento. GRANDE: viaggio su «L'ultima frase»: la carta si compatta in alto, la mail sale e il corpo scorre veloce e attenuato (righe grigie) fino in fondo.
ANIMAZIONE: (come oggi) l'ultima riga si scrive un cartellino alla volta con la voce, fino a «un»; il cursore lampeggia fino alla fine.
```
Rispetto a oggi: via il titolo dal fotogramma 0 e il suo rimpicciolirsi; via `RIQUADRO: no` (il presentatore è nel
riquadro dall'hook, e «finiscila tu» detto a camera vale di più). La riga 2 è il testo di A1, identica.

### Scena 3 [spiegazione] — animata · prima metà della scena 2 di oggi · 14 parole
```
VOCE: Colloquio, vero?
VOCE: Io gliel'ho chiesta dieci volte, e colloquio c'era in ==tutte e dieci==.
ANIMAZIONE: (come oggi) GRANDE: punch «COLLOQUIO», poi la parola rientra al posto del cursore.
ANIMAZIONE: (come oggi) la mail si riduce a sinistra, entrano i quattro frammenti A2, A4, A6, A9 e «10 su 10». I frammenti restano in scena fino allo stacco, con un ultimo secondo fermo.
TESTO: 10 su 10
```
Rispetto a oggi: esce il colpo di scala su «quello che fa lei» (la frase non c'è più); i frammenti non escono in
alto, perché il loro beat d'uscita è diventato il filmato: **restano fermi fino allo stacco**, che è anche un ultimo
fotogramma più leggibile di oggi.

### Scena 4 [spiegazione] — a filmato · il beat 3 della scena 2 di oggi, allargato · 18 parole
```
VOCE: E la tua mail finisce lì, accanto a quelle degli altri.
VOCE: E una mail che parla di te?
ANIMAZIONE: Una pila di curriculum stampati su una scrivania d'ufficio; le mani di un selezionatore li sfogliano uno dopo l'altro con lo stesso gesto, senza scartarne nessuno.
```
Rispetto a oggi: **le due copie grigie a ventaglio spariscono dal Manim** (le sostituisce la pila vera). Il motivo
delle sagome grigie resta nella chiusura (la moltiplicazione), che ora fa rima con la pila della clip invece che con
le due copie. «Senza scartarne nessuno» è nel brief apposta: una clip con un curriculum buttato via direbbe «ti
scartano», che il reel non afferma.

### Scena 5 [spiegazione] — animata · scena 3 di oggi, con in testa il beat 4 della scena 2 · 47 parole
```
VOCE: Si può, ma non basta chiederglielo.
VOCE: Perché lei scrive una parola alla volta, e ne prende una delle più ==probabili==.
VOCE: Per questo la mail viene fluente. Ma se non gliel'hai detto, non sa da quanti anni lavori,
VOCE: non sa dove, e non sa perché vuoi proprio loro.
ANIMAZIONE: Si arriva da uno stacco sul filmato: al primo fotogramma la mail è già intera al centro con «colloquio.» acceso, e la carta «richiesta» compatta in alto. Su «Si può» entra in alto, piccola, l'etichetta «parla di te?» con il punto di domanda in accento, che resta in scena attenuata fino alla scena 8; su «non basta» il punto di domanda si attenua.
ANIMAZIONE: (come il beat 1 di oggi) colonna delle candidate, GRANDE: zoom, «colloquio» vola nel cursore.
ANIMAZIONE: (come il beat 2 di oggi) «fluente», «[numero]» acceso.
ANIMAZIONE: (come il beat 3 di oggi) gli altri due segnaposto, «non gliel'hai detto».
TESTO: parla di te?
TESTO: fluente
TESTO: non gliel'hai detto
```
Rispetto a oggi: un beat in più in testa (l'etichetta del loop, che oggi entra a fine scena 2). Così «Perché lei
scrive…» risponde a una frase detta nella stessa scena, e il dubbio della Parte 1 («Perché» appeso se la scena si
registra da sola) cade. 47 parole, ~18 s: è la scena più lunga, sotto i 19 s.

### Scena 6 [spiegazione] — animata · scena 4 di oggi, 4 beat invece di 5 · 41 parole
```
VOCE: Non è che sbagli a fartela scrivere, ci mancherebbe,
VOCE: è che non basta dirle «sii originale».
VOCE: Io l'ho fatto, e una mail su due comincia con un ==divano==.
VOCE: L'inizio è cambiato, ma del tuo lavoro non le hai ancora detto niente.
TESTO: 5 su 10
TESTO: non gliel'hai detto
```
Brief come oggi meno il beat «stessa frase». Rispetto a oggi: escono il terzo frammento (B3), il riquadro accento
sulle due righe identiche e il `TESTO: stessa frase`. Il fatto (B2 e B3 aprono con la stessa frase) **passa in
caption**, dove la revisione lo ha già messo («due Opus cominciano con la stessa frase»): non sparisce in silenzio,
ma dalla VOCE e dallo schermo sì. Da dire al revisore.

### Scene 7, 8, 9 — le scene 5, 6, 7 di oggi con la VOCE della Parte 1
Solo rinumerate. Nei brief i rimandi diventano «stesso gesto della scena 2», «la colonna della scena 5»,
«l'etichetta della scena 5», «fino alla scena 8». 34, 29 e 16 parole.

## Tabella per l'animatore: scena di oggi → scena nuova

| Oggi | Nuova | Classe | Cosa va fatto |
|---|---|---|---|
| — | 1 [hook] filmato | nessuna | niente Manim: clip + riquadro. La copertina non è più l'ultimo fotogramma di `Scena01` |
| 1 [hook] | 2 [spiegazione] | `Scena01` → `Scena02` | **da rifare in parte**: fotogramma 0 senza titolo e già pieno; il riquadro ora c'è, quindi l'area contenuto è quella corta (oggi è quella alta dell'hook): reimpaginare carta + mail. Ancore beat 0: «candidatura» `t0[4]` → `t0[2]`, viaggio `t0[6]` → `t0[3]`. Il beat 0 è più corto (7 parole, ~3 s): bordo e viaggio da 1,2 s ci stanno, ma stretti |
| 2, beat 0-1 | 3 | `Scena02` → `Scena03` | beat 0 ridotto a «Colloquio, vero?» (~1,8 s, come «Duemilacento, vero?»): via il colpo su «quello che fa lei», il rientro della parola nella mail può finire nei primi decimi del beat 1. Beat 1: ancore `t1[7]`/`t1[8]` → `t1[8]`/`t1[9]` (Parte 1); **i frammenti non escono**, ultimo secondo fermo |
| 2, beat 2 | 4 filmato | nessuna | **buttato**: le due copie grigie a ventaglio |
| 2, beat 3 | 5, beat 0 | dentro `Scena05` | **spostato**: mail intera già a fotogramma 0 (si arriva da uno stacco), etichetta «parla di te?» su `t0[0]`, il «?» si attenua su «non» `t0[3]` |
| 3 | 5, beat 1-3 | `Scena03` → `Scena05` | i tre beat slittano di uno (`tempi(0..2)` → `tempi(1..3)`), indici dentro le righe invariati («nemmeno» non c'è più: «perché» resta `t[6]`) |
| 4 | 6 | `Scena04` → `Scena06` | **via il beat 3** (B3, riquadro, «stessa frase»); il beat 4 diventa beat 3 (`tempi(4)` → `tempi(3)`, indici invariati); ancora «ci mancherebbe» `t0[5]` → `t0[7]` (Parte 1). Il beat del divano ora finisce con il punto: serve un fermo pulito su B2 + due frammenti + «5 su 10» |
| 5 | 7 | `Scena05` → `Scena07` | rinumerata; ancore `t0[1]`/`t0[5]` → `t0[2]`/`t0[6]` (Parte 1) |
| 6 | 8 | `Scena06` → `Scena08` | rinumerata; ancora `t1[7]` → `t1[9]` (Parte 1) |
| 7 | 9 | `Scena07` → `Scena09` | rinumerata, invariata |

In più: gli stati che una scena eredita dalla precedente vanno ricontrollati ai due stacchi (2→3 resta in
continuità; 3→4→5 no: la scena 5 deve ricostruire da sé mail intera e carta compatta). Le clip registrate non
esistono ancora, quindi niente `contenuti/media/` da rinumerare; `contenuti/render/generativa-probabile/` va rifatto
da capo (i `report*.json` hanno la numerazione vecchia).

## Verifica

Copia: `…/scratchpad/voce/struttura/2026-09-15-generativa-probabile.md` (scene complete, brief interi).

```
uv run reel valida <copia>
[AVVISO]  9 scene: il formato tipico è 6-8
[OK con avvisi] reel stimato 90s · 9 scene (1 hook, 7 spiegazione, 1 chiusura) · 231 parole di voce
   1:hook 15p ~6s · 2: 17p ~7s · 3: 14p ~6s · 4: 18p ~7s · 5: 47p ~18s · 6: 41p ~15s · 7: 34p ~13s · 8: 29p ~11s · 9:chius 16p ~7s
```
0 errori; l'unico avviso è quello fisso delle 9 scene (il coordinatore ne ammette 9); nessun avviso di durata
(89,7 s) né di linguaggio. 231 è il tetto: una parola in più e scatta l'avviso dei 90 s.

```
uv run --project broll broll piano <copia>
generativa-probabile · 9 scene · 2 a filmato
  ▣ scena 1 [hook] · filmato · «ragazza portatile tavolo casa sera»
  ▣ scena 4 [spiegazione] · filmato · «pila curriculum stampati scrivania ufficio»
  ◻ scene 2, 3, 5, 6, 7, 8, 9 · animazione
```
Il piano propone a filmato proprio l'hook e la scena 4, e nessun'altra. Le due query descrivono un'immagine già al
primo tentativo (la query sono le prime cinque parole piene del brief: per questo i due brief cominciano dal
soggetto e dal luogo). Perché le altre restano animate: la 2 è attaccata all'hook (mai due di fila), le altre
nominano una quantità o una figura («10 su 10», colonna, «5 su 10», «300», «2.100»).

**Attenzione, il comando ha scritto un file nel repo**: `contenuti/broll/generativa-probabile/piano.json` (nuovo,
non tracciato). È una proposta e si rifà, ma così com'è **non va usato**: `sorgente` punta alla copia nello
scratchpad, e le durate «(report)» vengono da `contenuti/render/generativa-probabile/report.json`, che ha la
numerazione vecchia (dà 15,0 s alla scena 4, che ne dura ~7). Va rifatto con `broll piano` sulla sceneggiatura vera,
dopo che la struttura è stata applicata e rimontata.

## Versione a 8 scene (solo l'apertura a filmato), in breve

Scena 1 hook a filmato e scena 2 come sopra; la scena 3 è la scena 2 di oggi quasi intera («Colloquio, vero?» /
«Io gliel'ho chiesta…» / «E la tua mail finisce lì, accanto a quelle degli altri.» / «E una mail che parla di te? Si
può, ma non basta chiederglielo.», 38 parole, con le copie grigie e l'etichetta come oggi); le altre scalano di uno.
Stessi tagli (il tetto a 8 scene è 234: «nemmeno» può restare). Verificata sulla copia
`…/scratchpad/voce/struttura/otto/`: `[OK]` 0 errori, 0 avvisi, 89 s, 232 parole (15/17/38/42/41/34/29/16).

Perché non la consiglio: costa gli stessi tagli alla VOCE e dà **una sola clip, nei primi 6 secondi, e poi 83 s di
sola animazione**: l'alternanza che il presentatore ha chiesto non si vede. Ha un solo vantaggio, meno lavoro per
l'animatore (la scena 2 di oggi non si spezza, si rifà solo il vecchio hook). Con 9 scene la seconda clip cade a
~19 s, dopo tre scene, nel punto in cui il reel dice la posta in gioco. Resta vero anche con 9 che **dalla scena 5
in poi (~70 s) è tutto animato**: ogni scena lì ha un meccanismo o un numero, e una terza clip chiederebbe una
decima scena.

## Per il revisore, se si applica

Nessun fatto o numero nuovo. Da rileggere:
- l'hook nuovo: è una domanda, ma «e adesso aspetti» + una clip di attesa non deve diventare «non ti rispondono
  perché l'ha scritta l'IA» (il brief chiede attesa, non un rifiuto);
- la clip della scena 4: selezionatore e pila rendono concreto «accanto a quelle degli altri»; il brief esclude lo
  scarto. Resta il ⚠️ 9: non si dice che gli altri usano l'IA né che chi legge se ne accorge;
- «stessa frase» esce da VOCE e schermo e resta solo in caption; «hai fatto un po' quello che fa lei» (⚠️ 6) esce
  del tutto;
- «Guarda questa candidatura»: non dice più chi l'ha scritta; lo dicono la carta «richiesta» a schermo e, una scena
  dopo, «Io gliel'ho chiesta dieci volte».

## Frasi di cui sono meno sicuro (Parte 2)

- «La candidatura te l'ha scritta l'IA, e adesso aspetti.»: dà per fatto che chi guarda l'abbia già mandata; chi non
  l'ha fatto potrebbe non sentirsi chiamato. Alternativa al presente, stesse 15 parole: «La candidatura te la scrive
  l'IA, la mandi, e aspetti. Ma quella mail parla di te?».
- «Guarda questa candidatura. L'ultima frase finiscila tu.»: «finiscila» dopo «l'ultima frase» è la ripresa col
  clitico della Parte 1; se al presentatore inciampa, «L'ultima frase finiscila tu» regge anche da sola.
- «E una mail che parla di te?» in coda alla scena a filmato: ripete quasi alla lettera la domanda dell'hook («Ma
  quella mail parla di te?»). È voluto (il loop), ma a 19 s di distanza può suonare come un doppione: si sente solo
  leggendolo ad alta voce.
- «Colloquio, vero?» da solo su una riga: era già la riga più da copione, e ora non ha più la frase che la
  ammorbidiva.

TITOLO alternativo per la copertina (ora che vive solo lì e deve fermare la griglia): «La candidatura che può
firmare chiunque» (6 parole; riprende la battuta finale, già approvata per la prima mail).
