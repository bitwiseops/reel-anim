---
fonte: testo
data: 2026-09-24
stato: ideato
idea: contenuti/idee/2026-09-24-dove-finiscono-chat.md
---

# Dove finiscono le tue chat: come i provider usano i dati, e quando conviene un'IA in casa

Chi scrive a ChatGPT o a Claude non sa cosa succede a quello che scrive: se ci addestrano i modelli, per quanto
lo tengono, chi può ottenerlo. Il reel spiega **come vengono usati i dati** dai provider (esempi: OpenAI e
Anthropic) e **se conviene un modello in casa**. Il presentatore vuole **fonti indipendenti, il trend e
un'opinione sopra**.

## I dati (fonti ufficiali)

**Cosa dicono i provider**
- Anthropic, *Updates to Consumer Terms and Privacy Policy* (agosto 2025): per Claude Free, Pro e Max l'utente
  sceglie se le chat servono ad addestrare i modelli; se accetta, i dati si conservano **5 anni**, altrimenti resta
  la conservazione di **30 giorni**. La scelta si cambia nelle impostazioni; le chat cancellate non entrano
  nell'addestramento futuro. https://www.anthropic.com/news/updates-to-our-consumer-terms
  Anthropic Privacy Center, quanto a lungo conserva i dati:
  https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data
- OpenAI, *Data controls in ChatGPT*: per i piani personali l'opzione «Migliora il modello per tutti» decide se le
  chat addestrano i modelli; le chat temporanee non addestrano ma si conservano fino a 30 giorni per sicurezza.
  https://help.openai.com/en/articles/7730893-data-controls-faq
  OpenAI, per aziende e API: di default non addestra su input e output di ChatGPT Team, Enterprise e API; i log di
  controllo degli abusi si tengono fino a 30 giorni; la conservazione zero solo con accordi Enterprise.
  https://developers.openai.com/api/docs/guides/your-data
  https://openai.com/policies/how-your-data-is-used-to-improve-model-performance/

**Cosa dicono le autorità e i tribunali (indipendenti dai provider)**
- Garante privacy, comunicato del 20/12/2024: sanzione di 15 milioni a OpenAI e campagna informativa di sei mesi;
  contestati fra l'altro la mancanza di una base giuridica per usare dati personali nell'addestramento e la
  trasparenza verso gli utenti. https://www.garanteprivacy.it/home/docweb/-/docweb-display/docweb/10085432
- Tribunale di Roma, sentenza del 18/03/2026: annulla la sanzione **per competenza** (da febbraio 2024 OpenAI ha
  sede in Irlanda, decide l'autorità irlandese), **senza entrare nel merito** delle violazioni. Fonte da trovare in
  forma ufficiale (testo della sentenza o comunicato); intanto ANSA del 20/03/2026:
  https://www.ansa.it/canale_tecnologia/notizie/tecnologia/2026/03/20/tribunale-roma-annulla-multa-da-15-milioni-di-euro-del-garante-privacy-a-openai_6560fadd-4099-451e-99a0-7fcbc9a285c1.html
- Causa New York Times contro OpenAI (tribunale federale di New York): nel 2025 un ordine di conservazione ha
  obbligato OpenAI a tenere anche le chat che gli utenti avevano cancellato; l'ordine è stato tolto per il futuro il
  9/10/2025, ma quelle già conservate restano. Fonte da trovare in forma ufficiale (l'ordinanza, o la pagina di
  OpenAI sulle richieste del NYT).

**L'alternativa in casa**
- Un modello aperto gira anche su un computer di casa: la scheda di gpt-oss-20b (OpenAI) dice che sta in 16 GB di
  memoria. https://huggingface.co/openai/gpt-oss-20b — con un modello in casa le chat non escono dal computer.

## Il trend che si vede
Le chat sono diventate materia prima: i provider chiedono di usarle per addestrare (con conservazioni che vanno da
30 giorni a 5 anni), le autorità contestano e i tribunali possono ordinare di conservarle anche dopo che le hai
cancellate. Nello stesso tempo i modelli aperti sono diventati abbastanza piccoli da stare in casa.

## Un'opinione da costruirci sopra (proposta: la sceglie il presentatore alla fermata 1)
«Non serve scappare dal cloud: serve sapere quale interruttore hai toccato. Per le cose di tutti i giorni basta
spegnere l'addestramento; per quello che non diresti a un estraneo, un modello in casa.»
Mossa per chi guarda: aprire adesso le impostazioni della propria IA e controllare quell'interruttore.
Potenziale e limite: il cloud è più capace e comodo, l'IA in casa è più riservata ma meno potente e costa.

## Cautele per il revisore
- Le policy cambiano: citare la data della pagina letta; controllare le impostazioni attuali di entrambi i provider.
- Nessuna frase che presenti un provider come peggiore dell'altro senza un fatto: le regole di default sono diverse
  per piani personali, aziende e API, e vanno dette per quello che sono.
- Il caso del Garante è chiuso senza esame del merito: non dire «OpenAI ha violato la privacy» come fatto accertato.
- «Le chat non escono dal computer» vale se il programma che fa girare il modello non manda dati fuori: dirlo
  in modo preciso.
- Tema vicino a comprare o affittare una GPU: il reel deve stare in piedi da solo (regole editoriali §6), senza
  entrare nei costi dell'hardware.
