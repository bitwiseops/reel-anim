# Comprare una scheda per l'IA conviene solo se la usi tanto

**Data:** 2026-09-22
**Tipo:** pillola
**Fonte:** testo (contenuti/spunti/2026-09-22-gpu-comprare-o-affittare.md)
**Stato:** sceneggiata
**Copione:** contenuti/copioni/2026-09-22-gpu-comprare-o-affittare.md
**Sceneggiatura:** contenuti/sceneggiature/2026-09-22-gpu-comprare-o-affittare.md

Reel a sé stante, fuori dal filone dei paper. Nessun personaggio, nessuna azienda inventata, nessun nome proprio nella
situazione: non c'è omonimia da chiudere. **Nessun testo attribuito a un modello: la tappa T0b si salta.** La tesi è
del presentatore (il testo incollato, §3 e §5): la tengo, la completo, e marco come *proposta* quello che aggiungo.
Tutti i numeri del testo erano senza link: ho rifatto il conto da capo con i numeri che ho trovato su fonti ufficiali
(listino del fornitore, ARERA, BCE, scheda tecnica NVIDIA, TrendForce), letti da me il 2026-09-22. **Il prezzo
d'acquisto della scheda non ha una fonte ufficiale** (lo fanno i negozi e il mercato dell'usato): entra come
**esempio dichiarato**, arrotondato, e il reel lo dice.

**Pubblico scelto** (decisione mia, in `--tutto`): **chi ha pensato di far girare un modello di IA sul proprio
computer** (sviluppatori, chi fa ricerca, studenti, chi vuole un assistente in casa per tenersi i dati), cioè chi
almeno una volta ha guardato il prezzo di una scheda video «per l'IA». È una nicchia, ma è quella a cui la domanda
serve davvero, e cresce: i modelli aperti da far girare in locale sono diventati un tema comune. Il ragionamento però
arriva anche a chi non compra niente, perché la figura è quella di ogni «compro o noleggio?» (l'auto e il car sharing):
chi guarda impara a leggere un prezzo come **costo per ora d'uso**, non come cifra sul cartellino. Per questo l'angolo
regge per i nostri reel e non chiudo NEEDS_CONTEXT.

## Concetto AI illustrato
**Far girare l'IA costa in ore di scheda video. Se la affitti, ogni ora costa uguale; se la compri, ogni ora costa
meno quanto più la usi. Le due cose si incrociano a una soglia di ore al mese: sotto conviene affittare, sopra
comprare.**

Il meccanismo, senza semplificare in falso:
- **Affitto: costo orario piatto.** Un servizio di noleggio ti fa pagare un tanto all'ora la scheda (con processore e
  memoria del computer che la ospita), a qualunque uso. Su RunPod, il 22 settembre 2026, una RTX 3090 (24 GB di
  memoria video) costa **0,50 $/h** nella parte «Secure Cloud» (centri dati del fornitore) e **0,22 $/h** nella parte
  «Community Cloud» (macchine di privati collegate al servizio). Al cambio BCE del 21 settembre 2026 (1 € = 1,1490 $):
  **0,435 €/h** e **0,191 €/h** tasse escluse (termini di servizio RunPod: «Fees do not include any Sales Tax»); per un
  privato in Italia si aggiunge l'IVA al 22 %: **0,531 €/h** e **0,234 €/h**, la stessa base (tasse incluse) della
  corrente e del prezzo della macchina.
- **Acquisto: costo orario che scende.** Il prezzo della macchina è una spesa fissa; divisa sui mesi in cui la usi
  (36, tre anni, come nel testo del presentatore) diventa una quota mensile, e divisa per le ore che la fai lavorare in
  un mese diventa un costo per ora: `quota / ore`. È una curva che scende (un'iperbole): a 20 ore al mese ogni ora
  costa tanto, a 300 poco. A questa si somma **la corrente**, che invece è un costo per ora fisso: la scheda assorbe
  fino a 350 W (scheda tecnica NVIDIA), il computer intero sotto carico diciamo **0,5 kW** (esempio dichiarato), e la
  tariffa di riferimento ARERA dal 1° luglio 2026 è **31,63 centesimi al kWh** tasse incluse: **0,158 €/h**. La curva
  dell'acquisto non scende mai sotto questa riga: anche con la scheda pagata, ogni ora costa la corrente.
- **La soglia.** Si cerca il numero di ore al mese `H` in cui le due spese si pareggiano:
  `affitto × H = quota mensile + corrente × H`, quindi `H = quota mensile / (affitto − corrente)`.

**Il calcolo, con i numeri verificati** (esempio dichiarato: 1.500 € fra scheda usata e resto del computer; è la
somma del testo del presentatore, 1.250 + 250, che non ho potuto verificare su fonti ufficiali):
- quota mensile = 1.500 € / 36 mesi = **41,67 €/mese**
- corrente = 0,5 kW × 0,3163 €/kWh = **0,158 €/h**
- affitto (Secure Cloud) = 0,50 $ / 1,1490 × 1,22 (IVA) = **0,531 €/h**
- H = 41,67 / (0,531 − 0,158) = 41,67 / 0,373 = 111,8, detta **centodieci ore al mese**, cioè **quasi quattro ore al
  giorno (3,7), tutti i giorni**.
- Verifica: a 110 ore, l'acquisto costa 41,67/110 + 0,158 = 0,537 €/h, quanto l'affitto.

Quanto si sposta la soglia (per il revisore e per la caption, non tutti per il reel):
- scheda + computer a 1.000 € → **75 h/mese** (2,5 h al giorno); a 2.000 € → **circa 150 h/mese** (5 h al giorno);
- se dopo tre anni rivendi la macchina a metà prezzo (ipotesi, nessuna fonte), la spesa netta è 750 € → **56 h/mese**:
  il valore di rivendita pesa quanto il prezzo d'acquisto, e il testo del presentatore ha ragione a dirlo;
- **se affitti al prezzo più basso** (Community, 0,22 $/h + IVA = 0,234 €/h), la differenza con la corrente è 0,076 €/h
  e la soglia diventa 41,67 / 0,076 = **circa 550 ore al mese**, oltre diciotto ore al giorno su un mese di 720-744.
  **L'incrocio c'è, ma lontanissimo**: a quel prezzo, con questi numeri e senza rivendita, comprare conviene solo
  tenendo la scheda accesa quasi giorno e notte. È un risultato forte ma fragile (i privati sono meno affidabili, e basta una rivendita per
  cambiarlo): va detto con la cautela.

**La soglia del testo (83 ore) non si ritrova.** Le 83 ore tornano togliendo la corrente (41,67 / 0,50 ≈ 83). Con
la corrente e l'IVA al 22 % sull'affitto (revisione del 2026-09-22, approvata dal presentatore) il numero giusto è
**110**: 41,67 / (0,531 − 0,158) = 111,7, quasi quattro ore al giorno. Nella caption si dice che è un esempio e che
ognuno lo rifà con i suoi prezzi.

**Il tetto che nessuna ora compra.** Prima del conto c'è una domanda di sì o no: il modello che vuoi far girare entra
nella memoria della scheda? Una scheda da 24 GB non diventa una da 80 GB a forza di ore; se il modello non ci sta, il
confronto non esiste e si affitta (o si sceglie un modello più piccolo). È il primo passo della mossa del presentatore.

**Perché le schede costano care proprio adesso** (contesto, scena di apertura del meccanismo): la memoria. TrendForce
(3 luglio 2026) scrive che i produttori spostano capacità verso i server per l'IA, che l'offerta di memoria grafica
resta «constrained» e che i prezzi GDDR6/7 salgono con quelli della DRAM; e (30 luglio 2026) che l'offerta di DRAM
resterà tesa nel 2027 e che i nuovi impianti non daranno contributi sostanziali prima del 2028. Il reel ne ricava solo
questo: la memoria delle schede serve ai centri dati dell'IA, e il sollievo non è dietro l'angolo. **Niente prezzi di
listino delle schede** (nessuna fonte ufficiale letta: quelle di TrendForce sulle RTX 50 sono notizie «reportedly»,
non ricerche sue).

## Situazione
*Proposta.* Vuoi far girare un modello di IA sul tuo computer: per tenerti i dati, per non pagare un abbonamento, per
provare. Apri gli annunci, trovi una scheda video da 24 GB usata, e il prezzo è più alto di quanto ricordavi. Ti
chiedi se comprarla. La domanda che ti fai è «quanto costa?»; quella giusta è «quante ore la farò lavorare?».

Il momento di prova per chi guarda (*proposta*): prima che compaia la soglia, il presentatore gli chiede di fare il
suo conto a mente: «quante ore al mese la terresti accesa a lavorare, davvero? Non quante ci stai al computer: quante
la fai girare». Chi guarda di solito si dà un numero generoso; la figura gli mostra che serve una media di quasi
quattro ore al giorno, tutti i giorni, per tre anni.

A schermo la situazione diventa oggetti, non battute: una scheda video (sagoma), un mucchio di monete che è il suo
prezzo, un orologio o un contatore delle ore del mese, un grafico con una riga piatta e una curva.

## Messaggio centrale
Una scheda comprata costa meno a ogni ora che la usi, una affittata costa sempre uguale. Prima di comprarla conta le
ore: con i prezzi di oggi, sotto le quattro ore al giorno conviene affittare.

## Struttura narrativa
**Schema di partenza:** @ingegneria.italia · r0039 — allarme di mercato con i numeri → tre cause in elenco →
ricaduta su chi guarda → domanda-pivot che porta dentro lo stabilimento → processo in tappe → ritorno al problema
iniziale → firma.

> Negli ultimi mesi in [settore] c'è qualcosa che sta correndo più veloce di tutto: [costo]. Il motivo è [materia prima], o meglio [termine tecnico], che è [spiegazione in una riga]. In [periodo] il prezzo è salito del [numero]. Il punto è che [causa 1]. Tradotto: [versione semplice]. Ma c'è anche [causa 2]. E poi c'è un vincolo [di altra natura]: [causa 3]. Per noi questo si traduce in [ricaduta]. Quindi la domanda è: [alternativa possibile]? Siamo in [luogo]. Qui [oggetto] non viene [buttato], viene [rigenerato]. Si parte da [tappa 1]… [tappe]. E come dicevamo all'inizio, [la soluzione risponde al problema d'apertura]. [Firma].

Perché questo. È lo schema del corpus che parte da **un prezzo che sale per colpa di una materia prima** e lo
trasforma, con una sola domanda, in **«allora devi proprio comprarlo?»**: esattamente la mossa del nostro reel (le
schede care per la memoria → la domanda comprare o affittare → il conto a tappe). Le tecniche portanti
(`domanda-pivot`, `numeri-come-prova`, `struttura-ad-anello`, `cautela`) stanno in «Tecniche condivise». Nessuna delle
altre idee in `contenuti/idee/` usa r0039 (usate: r0040, r0018, r0020, r0045, r0037, r0012).

**Adattamento** (una riga per fase):
- [Negli ultimi mesi c'è qualcosa che corre più veloce di tutto: il costo] → l'apertura a volto pieno è la domanda di
  chi guarda (vuoi l'IA in casa, quante ore la userai?); il prezzo che corre arriva subito dopo, sul filmato degli
  annunci: le schede costano più di quanto ricordavi.
- [Il motivo è la materia prima, o meglio il termine tecnico] → la memoria: quella che serve alle schede la
  prendono i centri dati dell'IA. Una causa sola, fatta vedere, non tre.
- [In (periodo) il prezzo è salito del (numero)] → niente percentuale sulle schede (nessuna fonte ufficiale): il numero
  è la data, «non prima del 2028» (TrendForce, 2026), per dire che aspettare non risolve.
- [Per noi questo si traduce in (ricaduta)] → una frase: per chi vuole l'IA in casa, la scheda è la spesa grossa.
- [Quindi la domanda è: (alternativa possibile)?] → la domanda-pivot: «ma devi proprio comprarla?». L'alternativa è
  affittarla a ore.
- [Siamo in (luogo). Qui (oggetto) non viene buttato, viene rigenerato] → invece dello stabilimento, l'analogia che
  tutti conoscono, sul filmato: l'auto tua e l'auto a noleggio. L'auto tua costa meno a ogni viaggio che fai, quella a
  noleggio costa uguale.
- [Si parte da (tappa 1)… (tappe)] → il conto a tappe, animato: la riga piatta dell'affitto, il mucchio del prezzo
  diviso in mesi e poi in ore, la corrente, l'incrocio a 110 ore.
- [E come dicevamo all'inizio, (la soluzione risponde al problema d'apertura)] → anello sulla domanda d'apertura: la
  mossa è rispondere davvero a «quante ore?», e la chiusura riprende la domanda dell'hook ribaltandola (non quanto
  costa: quante ore).

**Tecniche** (da «Tecniche condivise»):
- `domanda-pivot`: «devi proprio comprarla?» fra il prezzo che corre (scena 3) e l'analogia (scena 4).
- `numeri-come-prova`: la soglia si guadagna con il conto fatto vedere, un numero per beat (0,53 · 42 · 0,16 · 110).
- `analogia`: l'auto tua e l'auto a noleggio (scena 4, a filmato), detta come somiglianza del meccanismo di costo.
- `struttura-ad-anello`: l'hook chiede «quante ore?», la chiusura dice che quella è la domanda giusta.
- `cautela`: il conto non tiene la rivendita né le ore buttate sul noleggio; con i prezzi più bassi dei privati
  l'incrocio scivola lontanissimo (scena 6 e caption).

**Escluse:**
- `elenco` delle tre cause (r0039 ne ha tre: concentrazione, strategia, vincolo fisico): qui una causa sola, la
  memoria; le altre del testo (seconda generazione di schede spostata, prezzi medi) non hanno fonte ufficiale letta.
  Nessun elenco a camera; le tre verifiche del §5 del testo vanno in caption.
- `presenza-sul-luogo` («siamo nello stabilimento…»): non abbiamo un luogo; la sostituisce l'analogia filmata.
- `sponsor-integrato` e `firma-di-chiusura` («anche questa è ingegneria»): firme di un solo account, non si copiano.
  Nominiamo un fornitore solo come fonte del numero: nessuna promozione (lo diciamo in caption).
- Lunghezza: r0039 dura 160 s. Qui otto scene e obiettivo ≤ 70 s; se serve tagliare, la scena 3 perde il beat sul
  2028 e la scena 6 si riduce a una frase.

## Tappe del parlato
<!-- aggiunta il 2026-09-23 dal brief della prova alla cieca (contenuti/prove-parlato/gpu-comprare-o-affittare/brief.md),
per provare `uv run reel copione`: la sceneggiatura attuale non è stata rifatta da qui -->
1. (apertura) Una domanda a chi sta pensando di comprare una scheda video per l'IA in casa: quante ore la userà davvero?
2. (filmato: uno sul divano che scorre annunci) Le schede oggi costano più di quanto ci si ricordava.
3. (animazione) C'entra la memoria: i produttori la danno prima all'IA e per le schede ne resta poca; le fabbriche
   nuove, secondo le previsioni (TrendForce), conteranno solo dal 2028. Domanda-ponte: devi proprio comprarla?
4. (filmato: una che prende un'auto a noleggio) Analogia: la macchina tua costa meno a viaggio più la usi, a noleggio
   costa sempre uguale.
5. (animazione, grafico) A noleggio: circa mezzo euro l'ora (0,53 € con IVA), sempre. Comprata: esempio 1.500 euro
   fra scheda e computer, divisi su tre anni; ogni rata mensile si divide per le ore d'uso, quindi più la usi meno costa
   l'ora.
6. (animazione) A casa la corrente la paghi tu a ogni ora; con questi prezzi le due curve si incrociano a circa 110 ore
   al mese, cioè quasi quattro ore al giorno, tutti i giorni.
7. (filmato: uno che aspetta davanti al portatile) Il conto non dice tutto: a noleggio paghi anche le ore in cui
   aspetti; quella tua la puoi rivendere.
8. (animazione) La mossa: prima guarda se il modello che vuoi entra nella memoria della scheda, se no la affitti; se
   entra, affittala un mese e leggi in fattura quante ore hai pagato; sotto le 110, comprarla ti costava di più.
9. (chiusura) La domanda non è quanto costa la scheda, è quante ore la farai lavorare davvero. Battuta finale.

## Come si mostra
*Il reel si guarda muto: le caption col parlato sono in fondo, a schermo non c'è niente da leggere. Qui la figura che
regge il concetto senza parole.*

**La figura madre: un grafico con una riga piatta e una curva che scende, e un mucchio di monete che si sbriciola in
ore.** In orizzontale le ore al mese (da 0 a 300), in verticale quanto costa un'ora. Una sola scheda video (sagoma)
torna in tutte le scene animate.

- **Scena 3 — la memoria che se ne va (una quantità, un gesto).** Un mucchio di chip di memoria (rettangolini) al
  centro. Quasi tutti scivolano verso una grande sagoma di armadio server a sinistra; pochi arrivano alla scheda video a
  destra, che resta mezza vuota. Poi una linea del tempo che corre in avanti e si ferma contro una sbarra: «2028».
  Etichetta piccola: «TrendForce, 2026». Si capisce senza leggere: la memoria va altrove, e per un po' sarà così.
- **Scena 5 — il conto che si vede (prima una riga, poi una curva, poi l'incrocio).**
  1. La riga dell'affitto: piatta, all'altezza «0,53 €» (un'ora a noleggio, IVA inclusa), con una piccola nuvola accanto.
  2. Il prezzo della macchina: un mucchio di monete «1.500 €» accanto alla scheda. Il mucchio si divide in 36 fette
     (i mesi di tre anni); una fetta, «42 €», resta in mano.
  3. La fetta si sbriciola sulle ore del mese: con poche ore (20) ogni ora è un pezzo grosso e il punto sta in alto
     sul grafico; con 50, più basso; con 110, all'altezza della riga dell'affitto; con 300, sotto. La curva si
     disegna unendo i punti.
  4. Sotto a tutto, una riga tratteggiata: la corrente, «0,16 €». La curva le si avvicina e non la passa mai.
  5. L'incrocio si accende: «110 h», e accanto un orologio di un giorno che si riempie per 3,7 ore: quasi quattro ore
     al giorno. Etichette piccole: «RunPod + IVA, set. 2026» sotto la riga dell'affitto, «500 W · ARERA» sotto la
     corrente.
  A sinistra dell'incrocio l'area si colora (affitta), a destra l'altra (compra): la regola si legge senza parole.
- **Scena 7 — la mossa (due gesti, prima/dopo).** Primo gesto: un blocco (il modello) scende nella scheda; in una
  versione ci sta e si incastra, nell'altra sborda e la scheda si spegne (il blocco va verso la nuvola). Etichetta
  sulla scheda: «24 GB». Secondo gesto: il contatore delle ore del mese si riempie fino a una tacca a «110»; si ferma
  sotto la tacca → la freccia va alla nuvola (affitta); la supera → la freccia va alla scheda (compra). Poi il
  criterio: una ricevuta del mese di noleggio (sagoma, righe grigie) da cui si accende un solo numero, le ore pagate,
  che vola sul contatore.

**Mossa wow candidata** (*proposta*, facoltativa, scena 5 o 6): la seconda riga dell'affitto, quella dei privati a
«0,23 €», scende sul grafico e si ferma appena sopra la corrente; il grafico si allarga fino a «720 h» (un mese
intero, giorno e notte) e la curva la tocca solo verso «550 h», oltre diciotto ore al giorno. È l'unico momento in cui la figura rovescia l'intuizione
(«se la usi tanto conviene comprare» diventa «a certi prezzi, quasi mai»); va accompagnato dalla cautela (vedi claim).

Le tre scene a filmato (gli annunci, l'auto a noleggio, le ore buttate) sono in «Note per il reel», con le query.

## Cosa impara chi guarda
- **Un modo nuovo di leggere**: il prezzo di una scheda per l'IA non è un costo, è un costo **diviso per le ore** che
  la farai lavorare. Affittare e comprare non si confrontano sul cartellino ma sull'ora: una riga piatta contro una
  curva che scende, e dove si incrociano c'è la tua risposta.
- **La mossa, per domani** (del presentatore, §5 del testo; le prime due verifiche nel reel, la terza in caption):
  1. il modello che vuoi usare entra nella memoria della scheda? Se no, affitti;
  2. quante ore al mese la faresti lavorare davvero? Se sei sotto la soglia (con i prezzi di oggi, circa 110, quasi
     quattro ore al giorno), affitti.
- **Il criterio per capire se ha funzionato** (*proposta*, un gesto di chi guarda): **prima di comprare, affitta per un
  mese e, a fine mese, leggi sulla fattura del noleggio quante ore hai pagato davvero.** Se il numero è sotto la
  soglia, comprare ti sarebbe costato di più; se è sopra, hai la prova che conviene comprare. Rifai il conto con il
  prezzo della scheda che hai trovato tu (quota mensile diviso la differenza fra affitto orario e corrente).

## Pilastro
Cosa può fare per te (e dove costa: il limite di memoria e le ore buttate sono nella stessa idea).

## Perché ora
La memoria delle schede video serve ai centri dati dell'IA: TrendForce, a luglio 2026, scrive che l'offerta resta tesa
per tutto il 2027 e che gli impianti nuovi daranno contributi sostanziali solo dal 2028. Intanto far girare un modello
in casa è diventato una cosa che si fa (modelli aperti, programmi che li installano con un clic), e la tentazione di
comprare una scheda arriva proprio quando le schede costano di più. Il noleggio a ore, dall'altra parte, costa pochi
decimi di euro. È il momento in cui la domanda «compro o affitto?» ha soldi veri in gioco.

## Fonte
**Lo spunto è testo del presentatore** (incollato il 2026-09-22, senza link). La tesi (le due curve e la soglia, §3) e
la mossa (le tre verifiche, §5) sono sue. I numeri li ho ricercati uno per uno; quelli che entrano vengono da qui, tutti
**consultati il 2026-09-22**:

- **RunPod, pagina «GPU Cloud Pricing»** (listino ufficiale del fornitore, «Updated September 13, 2026»):
  https://www.runpod.io/pricing. Letta anche nell'HTML grezzo (dati strutturati della pagina). Misura: prezzo
  on-demand per ora di un «pod» con una GPU. Fatti: «On-demand RTX 3090 cloud GPU rental on Runpod. Community Cloud
  $0.22/hr, Secure Cloud $0.50/hr.» (24 GB VRAM, 125 GB RAM, 16 vCPU nella tabella Secure); RTX 4090 $0.34 / $0.74;
  RTX 5090 (32 GB) $0.69 / $0.99; H100 PCIe (80 GB) $1.99 / $2.89. Nel reel entra solo la 3090 (0,50 $, e 0,22 $ se si
  usa la mossa wow).
- **ARERA, comunicato «Elettricità: Maggior Tutela +4,6% nel III trimestre 2026 per i clienti vulnerabili»**, Milano,
  25 giugno 2026: https://www.arera.it/fileadmin/allegati/com_stampa/26/Aggiornamento_Maggior_Tutela_III_trimestre_2026.pdf
  (letto il PDF). Fatto: «Dal 1° luglio 2026, il prezzo di riferimento dell'energia elettrica per il cliente tipo sarà
  di 31,63 centesimi di euro per kilowattora, tasse incluse». Misura: **cliente tipo vulnerabile in Maggior Tutela**,
  2.000 kWh/anno, 3 kW (nota 1 del comunicato); non è la tariffa di chi sta sul mercato libero.
- **BCE, tassi di cambio di riferimento dell'euro**, 21 settembre 2026: 1 € = 1,1490 USD.
  https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml
- **NVIDIA, scheda tecnica GeForce RTX 3090** (Founders Edition): «Graphics Card Power (W) 350», «Required System
  Power (W) 750», memoria «24 GB GDDR6X».
  https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090-3090ti/. Misura: potenza della scheda e
  alimentatore consigliato, **non** il consumo del computer; lo 0,5 kW del conto è un esempio dichiarato (350 W di
  scheda più il resto).
- **TrendForce, «Diverging Memory Market Outlook in 2027 as DRAM Supply Remains Tight While NAND Flash Supply
  Conditions Ease»**, 30 luglio 2026: https://www.trendforce.com/presscenter/news/20260730-13158.html. Fatti: «construction
  schedules, equipment installation, and raw material preparation will delay meaningful production ramp-ups until the
  second half of 2027. Given the semiconductor manufacturing cycle, substantial output contributions are not expected
  to materialize until 2028.» e «These factors will constrain overall DRAM bit supply growth in 2027, keeping market
  supply tight.» Misura: offerta di DRAM (tutta, non solo delle schede video).
- **TrendForce, «AI Server Demand Continues to Support Memory Prices in 3Q26…»**, 3 luglio 2026:
  https://www.trendforce.com/presscenter/news/20260703-13134.html. Fatto: «Memory suppliers have also been flexibly
  reallocating production capacity toward other mainstream products, which has kept graphics DRAM supply constrained
  and allowed GDDR6/7 prices to rise alongside broader DRAM pricing trends.» Misura: prezzi contrattuali della
  memoria, non i prezzi al pubblico delle schede.

**Cosa non entra, e perché.** I prezzi delle schede nuove e usate (4090, 3090, 5090, il +84 % in Europa) vengono da
listini di negozi e non hanno fonte ufficiale: al loro posto un prezzo d'esempio dichiarato. La mediana H100 «su 54
provider», il trend +7 %, le forchette degli hyperscaler, OVHcloud e Scaleway: non servono alla figura (il reel parla
di una scheda da 24 GB) e non li ho verificati. Lo spostamento al 2028 della prossima generazione NVIDIA e AMD: l'ho
trovato solo in notizie riportate («reportedly»), non in una ricerca ufficiale; non entra. Il 20-40 % in più degli host
non verificati: nessuna fonte trovata; non entra (resta la cautela a parole, senza numero).

## Angoli scartati
- **«Aspettare non è una strategia»** (la carenza di memoria fino al 2028, §1 del testo). Vero e con fonte, ma è una
  notizia di mercato con una mossa sola («compra adesso») che il reel non può sostenere senza prezzi ufficiali delle
  schede, e che spingerebbe a comprare: il contrario della prudenza del conto. Resta come contesto nella scena 3.
- **«Nessuna ora trasforma 24 GB in 80»** (il tetto di memoria, §4). Chiaro e visivo (il blocco che non entra), ma
  da solo dice solo «certe cose non le fai in casa». Diventa il primo gesto della mossa.
- **«Salire di fascia peggiora la soglia»** (3090 contro 5090, §3). Interessante, ma servono i prezzi d'acquisto di
  due schede, che non hanno fonte ufficiale; e due curve in più affollano il grafico. In caption, se il presentatore
  lo vuole, come ragionamento senza numeri.
- **«Il valore di rivendita decide»** (§3). È la variabile che sposta di più la soglia (da 110 a 56 ore con una
  rivendita a metà), ma il valore futuro di una scheda usata è una scommessa, non un dato: nel reel una frase di
  cautela, in caption il conto.
- **«Accesso istituzionale: tempo di coda contro denaro»** (terza verifica del §5). Vale per chi fa ricerca (in Italia,
  per esempio, i bandi ISCRA del CINECA), non per il pubblico largo: in caption.

## Note per il reel
**Hook candidato** (la sola frase, detta da lui a tutto schermo, nessuna immagine):
- «Stai pensando di comprarti una scheda video per far girare l'IA in casa? Quante ore al mese la userai, davvero?»
  (20 parole)
- Alternativa: «Vuoi l'IA sul tuo computer e stai guardando le schede video? Prima dimmi quante ore la farai lavorare.» (18)
- **TITOLO della copertina** (la tesi): «Comprare una scheda per l'IA conviene solo se la usi tanto». Alternative:
  «Scheda per l'IA: comprarla o affittarla? Conta le ore»; «Quattro ore al giorno: sotto, affitta».

**Percorso** (*proposta*, otto scene; sei in mezzo: tre animate e tre a filmato, alternate, nessuna coppia di filmati;
la VOCE la scrive lo sceneggiatore):
1. **Apertura, volto pieno**: l'hook.
2. **A filmato · la situazione.** Voce generica: la voglia di avere l'IA sul proprio computer, i dati che restano
   tuoi, niente abbonamento; apri gli annunci e le schede costano più di quanto ricordavi. Immagine: **una persona
   seduta sul divano, di sera, scorre annunci sul telefono con foto di schede video, si ferma e alza le sopracciglia**;
   oppure **due mani che tolgono una scheda video dalla scatola**. Query: `person scrolling online marketplace on
   phone at night`, `hands unboxing graphics card`, `man looking at computer parts prices on laptop`.
3. **Animata · il perché del prezzo.** I chip di memoria che vanno quasi tutti all'armadio server, la scheda mezza
   vuota; la linea del tempo che si ferma a «2028» («TrendForce, 2026»). Chiude con la domanda-pivot: devi proprio
   comprarla? (numero: solo 2028).
4. **A filmato · l'analogia.** Voce generica: è come l'auto; quella tua costa meno a ogni viaggio che fai, quella a
   noleggio costa uguale ogni volta; se la usi poco, conviene la seconda. Immagine: **una persona in strada sblocca
   con il telefono un'auto a noleggio parcheggiata, sale e parte**; in alternativa **un'auto ferma sotto casa, coperta
   di foglie**. Query: `person unlocking car sharing car with smartphone`, `woman getting into rental car city
   street`, `parked car covered in leaves`.
5. **Animata · il conto e la soglia.** Riga piatta dell'affitto (0,53 €), il mucchio da 1.500 € in 36 fette (42 €), la
   fetta sbriciolata in ore, la curva, la corrente (0,16 €), l'incrocio a 110 h, l'orologio che si riempie per quasi
   quattro ore. Qui stanno tutti i numeri. Un beat per numero; non più di cinque beat.
6. **A filmato · la cautela.** Voce generica: il conto non dice tutto; sul noleggio paghi anche le ore in cui sistemi,
   aspetti, sbagli; in casa quelle ore costano solo la corrente; e se poi la scheda la rivendi, comprare conviene
   prima; però ci sono servizi a noleggio che costano così poco che comprare non conviene quasi mai. (Niente numeri
   qui: se il presentatore vuole la riga dei privati, va nella scena 5 o nella 7 come figura.) Immagine: **una persona
   davanti al portatile, di notte, che aspetta con il mento sulla mano mentre una barra di avanzamento va avanti
   piano**; oppure **un tassametro / un parchimetro che scorre**. Query: `developer waiting in front of laptop at
   night`, `person bored waiting for computer to finish`, `taxi meter running close up`.
7. **Animata · la mossa.** Il blocco-modello che entra o sborda dalla scheda («24 GB»); il contatore delle ore del
   mese con la tacca a 110, la freccia verso la nuvola o verso la scheda; la ricevuta del mese di noleggio da cui si
   accende il numero delle ore pagate (il criterio).
8. **Chiusura, volto pieno**: la battuta.

Obiettivo ≤ 70 s, circa 170-180 parole di VOCE. La scena più densa è la 5: se sfora, il passaggio «1.500 → 36 fette →
42 €» si fa in un beat solo (il mucchio si divide e resta la fetta).

**Filo visivo** (tre oggetti che tornano in tutte le scene animate; niente testo denso):
- **La scheda video** (sagoma, sempre a destra): mezza vuota in scena 3, accanto al mucchio di monete in scena 5,
  contenitore del blocco-modello in scena 7.
- **La nuvola del noleggio** (icona, sempre a sinistra o in alto): assente in scena 3, sulla riga piatta in scena 5,
  destinazione della freccia «affitta» in scena 7.
- **Il contatore delle ore** (un orologio o una barra che si riempie): l'orologio del giorno in scena 5, il contatore
  del mese con la tacca in scena 7; in scena 3 è la linea del tempo verso il 2028.
Ogni scena animata ha il suo cambio grande: i chip che scivolano via (3), il mucchio che si sbriciola e la curva (5),
il blocco che sborda e la freccia che sceglie (7).

**Numeri.** In VOCE al massimo tre: «circa mezzo euro l'ora» a noleggio, «centodieci ore al mese», «quasi quattro ore al
giorno». Tutti gli altri solo a schermo, arrotondati: 0,53 € (affitto, RunPod Secure Cloud RTX 3090, 0,50 $ tasse
escluse al cambio BCE, più IVA al 22 %), 1.500 € (**esempio dichiarato**, detto come tale: «mettiamo millecinquecento euro fra scheda e computer»), 36
mesi (scelta del conto, tre anni), 42 € al mese, 0,16 € l'ora di corrente (0,5 kW esempio × 31,63 c€/kWh ARERA), 110
h, 24 GB (scheda tecnica NVIDIA), 2028 (TrendForce). Il 110 va sempre detto come risultato **di questo esempio**.

**Chi si nomina nel reel.** A schermo, piccole, le etichette che reggono i numeri: «TrendForce, 2026», «RunPod + IVA,
set. 2026», «500 W · ARERA». Nessun nome a voce. Nessuna idea viene da un post o da un articolo non ufficiale: la tesi è del
presentatore.

**MESSAGGIO candidato** (per la caption del post, ≤ 12 parole):
- «Prima di comprare la scheda per l'IA, conta le ore.» (10)
- Alternative: «Affitto: ogni ora uguale. Acquisto: più la usi, meno costa.» (10); «Sotto le quattro ore al giorno, affitta.» (7)

**Chiusura a battuta** (*proposta*, ≤ 18 parole di VOCE, sceglie lo sceneggiatore): «Non chiederti quanto costa la
scheda. Chiediti quante ore la farai lavorare.» (13) Seconda direzione, ad anello con l'hook: «La domanda non è
quanto costa. È quante ore: il resto è una divisione.» (15)

**CTA** (una): «Mandalo a chi sta per comprarsi una scheda video per l'IA.» Alternativa: «Salvalo per quando ti viene
voglia di comprarla.»

**Claim per il revisore** (con le formule prudenti)
- **La soglia di 110 ore** è il risultato di un esempio: 1.500 € (non verificato, esempio dichiarato), 36 mesi, 0,5 kW
  (esempio), 31,63 c€/kWh (ARERA, cliente tipo vulnerabile in Maggior Tutela), 0,50 $/h (RunPod Secure Cloud, RTX
  3090, 22/09/2026, tasse escluse) + IVA 22 %, 1,1490 $/€ (BCE, 21/09/2026). Formula: «con questi prezzi», «in questo
  esempio», mai «la soglia è 110 ore» in assoluto. Conto: 41,67 / (0,531 − 0,158) = 111,7 (era 150 senza IVA, ❌ 3
  della prima revisione).
- **Lo scarto con il testo del presentatore**: le sue 83 ore tornano togliendo la corrente (41,67 / 0,50 ≈ 83). Chiuso.
- **La tariffa ARERA** non è «la tariffa di casa» di tutti: è il prezzo di riferimento del cliente tipo vulnerabile in
  Maggior Tutela. Formula: «una tariffa di casa tipica, circa 30 centesimi al kWh». Mai «la bolletta di tutti».
- **Il prezzo RunPod** non comprende lo spazio disco (si paga a parte: da verificare sulla stessa pagina) ed è per
  una GPU con processore e memoria inclusi; è il listino del 13 settembre 2026 e cambia. Etichetta con mese e anno.
- **Il 2028 di TrendForce** riguarda l'offerta di **DRAM** in generale (i contributi sostanziali dei nuovi impianti),
  non il prezzo delle schede video. Formula: «la memoria resterà scarsa per tutto il 2027, i nuovi impianti pesano dal
  2028». Il legame con le schede video è nel comunicato del 3 luglio 2026 (memoria grafica «constrained», prezzi
  GDDR6/7 in salita). Mai «le schede costeranno care fino al 2028».
- **La riga dei privati (0,23 €/h con IVA) che incrocia solo verso 550 ore**, se usata: vale senza rivendita e con
  1.500 €; i privati del
  «Community Cloud» sono meno affidabili (formula: «servizi più economici, ma meno affidabili»). Mai «comprare non
  conviene mai».
- **«Le ore buttate sul noleggio»** e **la rivendita** si dicono senza numeri: nessuna fonte ufficiale.
- **24 GB** è la memoria della RTX 3090 (scheda tecnica NVIDIA). Nel gesto della scena 7 il blocco che «non entra» è
  generico: non nominare un modello preciso e la sua dimensione senza fonte.
- **L'analogia dell'auto**: somiglianza del meccanismo di costo (spesa fissa divisa per l'uso contro tariffa a
  consumo), non un confronto di prezzi.

**Note per la caption**
- La tesi e le tre verifiche sono del presentatore; il conto è rifatto con numeri verificati al 22 settembre 2026.
- Il conto per intero, per chi vuole rifarlo con i suoi prezzi: soglia (ore al mese) = (prezzo della macchina ÷ mesi
  di uso) ÷ (affitto orario − consumo in kW × prezzo del kWh). Esempio: (1.500 ÷ 36) ÷ (0,531 − 0,5 × 0,316) ≈ 110,
  con l'affitto IVA inclusa.
- Le tre verifiche in elenco (solo in caption): 1) il modello entra nella memoria della scheda (24-32 GB)? se no,
  affitti; 2) le ore al mese superano la soglia calcolata sui tuoi prezzi? se sono molto sotto, affitti; 3) hai un
  accesso istituzionale (per chi fa ricerca, in Italia per esempio i bandi ISCRA del CINECA)? allora il confronto è
  tempo di coda contro denaro.
- Come si sposta la soglia: macchina a 1.000 € → 75 ore; a 2.000 € → 150 ore; rivenduta a metà dopo tre anni → 56
  ore; noleggio dei privati a 0,22 $/h più IVA → circa 550 ore, oltre diciotto al giorno. Con partita IVA l'IVA si
  toglie da tutte le voci e la soglia resta vicina a 110 (circa 117 con la corrente al 10 %).
- Fonti: RunPod pricing (13/09/2026), ARERA comunicato del 25/06/2026, BCE cambio del 21/09/2026, scheda tecnica NVIDIA
  RTX 3090, TrendForce 03/07/2026 e 30/07/2026 (link in «Fonte»). Nessuna sponsorizzazione: RunPod è citato solo come
  listino pubblico di riferimento, e i prezzi cambiano.
