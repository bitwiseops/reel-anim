---
fonte: testo
data: 2026-09-24
stato: ideato
idea: contenuti/idee/2026-09-24-gpu-comprare-affittare.md
---

# Comprare una GPU o affittarla nel cloud, per far girare modelli di IA open source

Chi vuole far girare in proprio un modello aperto (per privacy, per provare, per lavoro) si chiede se convenga
comprare una scheda o affittarla a ore. Il presentatore vuole **fonti indipendenti, il trend e un'opinione sopra**.

## I dati (settembre 2026)

**Comprare costa di più di quanto dica il listino, e non scenderà presto**
- NVIDIA, pagina della GeForce RTX 5090: 32 GB di GDDR7; prezzo di listino della Founders Edition in Italia
  2.389 €. https://www.nvidia.com/en-us/geforce/graphics-cards/50-series/rtx-5090/ (listino da verificare sulla
  pagina italiana)
- Prezzi di mercato in Italia (Trovaprezzi, idealo): le 5090 dei partner fra circa 4.400 e 6.000 €; la Founders
  Edition quasi introvabile. https://www.trovaprezzi.it/prezzo_schede-grafiche_nvidia_geforce_rtx_5090.aspx
  (comparatore, non fonte ufficiale: vale come «prezzo del giorno», da citare con la data)
- Il perché: le memorie vanno ai data center dell'IA. Micron, commento ai risultati del terzo trimestre fiscale 2026:
  la memoria HBM del 2026 è venduta con contratti pluriennali, l'offerta va ai clienti dei data center e frena PC e
  telefoni, e le nuove fabbriche non daranno volumi significativi prima dell'anno fiscale 2028.
  https://investors.micron.com/static-files/631b1a32-5537-46ae-8f40-82e42fc79dfe

**Affittare costa poco e si paga al secondo**
- RunPod, listino al 13/09/2026 (USD, per ora, fatturato al secondo): RTX 4090 24 GB 0,34 $ (community) / 0,74 $
  (secure); RTX 5090 32 GB 0,69 / 0,99 $; RTX 3090 0,22 / 0,50 $; H100 80 GB da 1,99 $. https://www.runpod.io/pricing
- Da verificare: se i prezzi sono al netto dell'IVA (per un privato in Italia si aggiunge il 22%) e il cambio.

**Tenerla accesa a casa ha un costo**
- ARERA, prezzo di riferimento per il cliente vulnerabile in maggior tutela dal 1° luglio 2026: 31,63 centesimi per
  kWh, tasse incluse (aggiornamento di ottobre in uscita a fine settembre).
  https://www.arera.it/comunicati-stampa/dettaglio/elettricita-maggior-tutela-81-nel-ii-trimestre-2026per-i-clienti-vulnerabili
- NVIDIA: potenza della scheda da prendere dalla pagina tecnica (la 5090 è dichiarata intorno ai 575 W).

**I modelli aperti chiedono meno memoria**
- OpenAI, scheda di gpt-oss-20b su Hugging Face: modello aperto che gira con 16 GB di memoria (pesi a 4 bit).
  https://huggingface.co/openai/gpt-oss-20b

## Il trend che si vede
Il prezzo per comprare sale (memorie contese dai data center, nessun sollievo prima del 2028), quello per affittare
resta basso e si paga solo quando la usi, e i modelli aperti buoni stanno in meno memoria. Figura: due curve che si
allontanano, e una soglia di ore al mese sotto la quale affittare vince.

## Un'opinione da costruirci sopra (proposta: la sceglie il presentatore alla fermata 1)
«Per quasi tutti oggi conviene affittare: comprare ha senso solo se la scheda lavora molte ore, tutti i giorni, o se
i dati non possono uscire da casa.» Mossa per chi guarda: contare le proprie ore al mese prima di comprare, e
provare il modello in affitto per una sera.
Potenziale e limite nella stessa idea: il cloud costa poco ma i dati escono da casa; la scheda costa tanto ma resta
tua (e si rivende).

## Cautele per il revisore
- Il punto di pareggio va calcolato con numeri della stessa data, IVA ed elettricità comprese, e dichiarato come
  esempio (ore al mese), non come regola.
- Prezzo di listino contro prezzo di mercato: dire quale si usa.
- Il resto del PC (alimentatore, processore, memoria) non è nel prezzo della scheda.
- «Affittare» su RunPod community cloud vuol dire macchine di terzi: dirlo se si parla di privacy.
