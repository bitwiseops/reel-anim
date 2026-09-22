---
fonte: testo
data: 2026-09-22
stato: ideato
idea: contenuti/idee/2026-09-22-gpu-comprare-o-affittare.md
---

**Comprare una GPU o affittarla a ore?** Testo incollato dal presentatore il 2026-09-22 (qui sotto, integrale). Chiude
su un «modello interattivo pubblicato sopra» che non è allegato: il reel non ci rimanda.

Note per l'ideatore:
- **I numeri del testo non hanno link**: nessuno entra nel reel così com'è. Ognuno va ritrovato su una fonte ufficiale
  (`docs/regole-editoriali.md` §5): le pagine dei prezzi dei fornitori (RunPod, Vast.ai, AWS, GCP, Azure, OVHcloud,
  Scaleway), i comunicati di TrendForce, ARERA per la tariffa elettrica. I prezzi dell'hardware nuovo e usato sono i più
  fragili: cambiano ogni settimana e vengono da listini di negozi. Se non trovi una fonte ufficiale, al numero preciso
  preferisci l'ordine di grandezza detto come tale.
- **Il cuore che si può animare** è il §3: il costo orario dell'affitto è una retta piatta, quello dell'acquisto è una
  curva che scende con le ore (capitale diviso ore, più la corrente), e le due si incrociano a una soglia (circa 83 ore
  al mese nell'esempio della 3090 usata). La soglia va **ricalcolata** con i numeri che verifichi, e il calcolo va
  scritto nell'idea.
- **La mossa per chi guarda** è il §5: tre verifiche in ordine (il modello entra in 24-32 GB? le ore superano la soglia?
  c'è un accesso istituzionale?).
- **Il pubblico**: chi usa l'IA ogni giorno non compra GPU. Decidi a chi parla il reel (chi fa ricerca o sviluppo,
  chi fa girare modelli in locale) e dillo nell'idea, oppure trova l'angolo che tocca anche chi non lo fa. Se l'angolo
  non regge per il pubblico dei reel, chiudi NEEDS_CONTEXT.
- Fuori dal filone «paper dirompenti»: vale il regime attuale (reel muto con caption, figura che regge da sola, registri
  a metà, estremi a volto pieno, reel a sé stante).

---

## Comprare una GPU o affittarla a ore?

**Premessa.** La domanda non ha una risposta assoluta, e chi la dà probabilmente sta descrivendo il proprio caso d'uso più che un principio generale. Quello che segue è il materiale per rispondere al proprio.

### 1. Il mercato dell'hardware, settembre 2026

Le schede da 24 GB costano oggi ben oltre il listino originale. La RTX 4090 si trova nuova a $2.755–3.449 contro un MSRP di $1.599, e usata a $2.350–2.500; la RTX 3090 sta a $1.369–1.535 nuova e $1.095–1.181 usata. Sulla 5090 la dinamica è più marcata: in Europa il prezzo medio è passato da circa €2.230 a metà luglio 2025 a €4.100, quasi +84% in dodici mesi.

La causa non è la domanda di gaming ma la carenza di memorie. TrendForce prevede che l'offerta DRAM resti tesa per tutto il 2027, con i nuovi impianti che non danno contributi produttivi sostanziali prima del 2028. Sul fronte GPU la carenza sta spostando al 2028 la prossima generazione Nvidia e AMD, senza finestre di sollievo nel 2027. Aspettare, quindi, non è una strategia.

### 2. Il mercato dell'affitto

Qui la forbice è enorme. Sul segmento consumer il pavimento è RunPod Community a $0,34/h per una RTX 4090, con Vast.ai nella stessa fascia. Sulla fascia datacenter, la mediana on-demand per una H100 su 54 provider è $3,36/h, con il minimo in stock a $1,35 e un trend a +7% negli ultimi 90 giorni. Gli hyperscaler stanno molto sopra: AWS ~$3,90–6,88, GCP ~$3,00–10,98, Azure ~$6,98–12,29 a seconda della configurazione.

L'opzione europea costa un sovrapprezzo contenuto: OVHcloud espone la H100 PCIe a €2,80/h da Gravelines, Scaleway ha L4 a $0,90/h, L40S a $1,68/h e H100 a $3,32–3,61/h, con posizionamento SecNumCloud su Parigi e Varsavia.

### 3. Il meccanismo economico

L'affitto ha costo orario piatto: paghi uguale a dieci o a cinquecento ore. L'acquisto ha un costo orario iperbolico — capitale fisso diviso ore effettive, più l'elettricità (in Italia la tariffa domestica con oneri e imposte è 0,3163 €/kWh nel terzo trimestre 2026).

Le due curve si incrociano a una soglia oraria. Con una 3090 usata a €1.250, €250 di sistema, 500 W, cloud a $0,51/h e orizzonte 36 mesi, **la soglia è circa 83 ore al mese** — meno di tre ore al giorno. Sotto, vince l'affitto; sopra, l'acquisto, e a pieno regime di migliaia di euro.

Due effetti controintuitivi:

Salire di fascia peggiora la soglia. Dalla 3090 alla 5090 il prezzo d'acquisto più che triplica, ma la tariffa cloud corrispondente solo raddoppia. Il rapporto è oggi più favorevole sull'usato Ampere che sul nuovo.

Il valore residuo è la variabile dominante. In un mercato in salita una scheda usata si deprezza pochissimo, e l'acquisto si avvicina a un prestito garantito più che a una spesa.

### 4. Quello che i numeri non catturano

- **I dati.** Terabyte di archivi satellitari si spostano male verso il cloud, e il costo non compare in nessuna tariffa oraria.
- **Le ore improduttive.** Sul cloud paghi anche mentre installi, debugghi e guardi una loss divergere. In locale quel tempo costa solo corrente.
- **L'affidabilità.** Gli host non verificati dei marketplace arrivano a costare il 20–40% sopra il prezzo di listino una volta contati riavvii e downtime.
- **Il tetto di VRAM.** Nessun numero di ore trasforma una 3090 in una H100 da 80 GB.

### 5. Come rispondere alla domanda

La decisione si riduce a tre verifiche, in ordine:

1. Il modello entra in 24–32 GB? Se no, il confronto non esiste: si affitta.
2. Le ore mensili previste superano la soglia calcolata sui propri prezzi? Se sono molto sotto, si affitta.
3. Esiste un accesso istituzionale? Allora il vero confronto non è denaro contro denaro, ma tempo di coda contro denaro — ed è un calcolo diverso.

Il modello interattivo pubblicato sopra permette di sostituire i propri numeri a quelli di default e vedere dove si sposta la soglia.
