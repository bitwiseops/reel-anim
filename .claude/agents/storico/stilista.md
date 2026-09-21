# Storico delle lezioni · stilista

Copia integrale della sezione «Lezioni dalle sessioni» di `.claude/agents/stilista.md` com'era il 2026-09-21, prima del
riordino in «Regole in vigore». **Gli agenti non caricano questo file**: è la cronaca (chi ha detto cosa, su quale
reel, cosa è stato superato e da cosa). Le lezioni nuove si aggiungono in fondo, con la data, quando serve ricordare
il *perché* di una regola; la regola stessa vive nell'agente.

## Dove è finita ogni lezione (riordino del 2026-09-21)
| Lezione | Oggi |
|---|---|
| 09-15 · niente righe `- Nota:`, le note stanno nelle Analisi | in vigore · «Leggere il corpus» |
| 09-15 · 11 reel su 14 da due account | in vigore · «Contare» |
| 09-15 · contraddizioni con i limiti nel rapporto e non nella guida | **corretta il 09-19** · «Cosa deve dare la guida»: nel rapporto e, in breve, nella guida |
| 09-16 · `**Note:**`, code allucinate, ricontare da zero, citazioni vecchie, dirette | in vigore · «Leggere il corpus», «Contare» |
| 09-16 · «non hai la shell: il verdetto lo conferma il coordinatore» | **superata** il 09-21: lo stilista ha `Bash` e lancia `reel stile` da sé |
| 09-19 · la guida deve dare l'orecchio, firme di un account, controesempi, terne | in vigore · «Cosa deve dare la guida», «Contare» |
| 09-19 · il passo non si stima a mano («chiedi al coordinatore») | in vigore, **corretta** · «Contare»: lo lancia lui |
| 09-19 · prima occorrenza di «Reel letti:» / «Letto il:» | in vigore · «Cosa deve dare la guida» |

Aggiunto il 2026-09-21: passo 0 di «Come lavori» (schede dei reel dal workflow `stile`). Stesso giorno, dopo la
verifica di conservazione: passo 4 allineato alla lezione del 09-19 (rapporto **e** guida), passo 5 con le tredici
sezioni della guida vera, blocco «cosa cambia per te» (regole editoriali §3, §4, §8).

## Lezioni dalle sessioni
- **2026-09-15, prima guida su 14 reel**: nell'export di reelkit non ci sono righe `- Nota:` (le note stanno dentro
  le Analisi, e riguardano spesso gli errori di Whisper). 11 reel su 14 venivano da due account: una regola «7 su 14»
  può riflettere soprattutto loro, dillo accanto alla regola. Le contraddizioni con i limiti del repo (hook senza
  «tu», frasi corte con il verbo contate come titoli, chiusure oltre 18 parole, reel oltre 90 s) sono andate nel
  rapporto e non nella guida: è la strada giusta, la decisione resta al presentatore.
- **2026-09-16, guida rifatta su 30 reel**: le `**Note:**` in fondo alle Analisi dicono quali trascrizioni escludere
  (r0034 inaffidabile) e dove tagliare le code allucinate (r0018, r0020). Allargando il corpus alcune regole sono
  scese sotto la metà (il fatto in apertura, l'«io» come reazione): si ricontano da zero, non si aggiornano i numeri
  vecchi. Le citazioni vecchie si ricontrollano parola per parola (una CTA era attribuita al reel sbagliato). Gli
  estratti da dirette (r0027-r0029, r0035) sono i migliori per il parlato naturale, ma vanno segnalati come tali.
  Non hai la shell: il verdetto di `reel stile` lo conferma il coordinatore.
- **2026-09-19, guida rifatta su 40 reel dopo «la voce narrante deve risultare più umana e naturale»** (seconda
  volta che il presentatore lo dice): le regole astratte non bastano, la guida deve dare l'orecchio. Servono una
  sezione quasi solo di citazioni raggruppate per mossa («Come suona il parlato vero»), una di tic dello scritto con
  esempi in negativo costruiti e dichiarati tali, mai attribuiti al corpus, e 5-8 id da leggere per intero, di
  account diversi, con il perché (lo sceneggiatore ora legge le trascrizioni intere). Accanto a ogni mossa vanno reel
  **e account**: una mossa di un solo account è una firma e sta in una sezione a parte, come in `pattern.md`. Un
  account nuovo può rovesciare un «mai»: con @gabrysolution sono entrati nel corpus le frasi nominali in fila,
  l'antitesi in coppia e la terna finale, cioè proprio i tic che il presentatore rifiuta: un reel del corpus può
  valere da controesempio, e va detto. Le terne vanno distinte: l'enumerazione di cose (35 su 40, spesso di 2, 4 o 6
  membri) è parlato, la terna messa per il ritmo no. Le citazioni con un errore di Whisper dentro si scartano; nomi e
  cifre non valgono mai come dati. **Il passo non si stima a mano**: non hai la shell, quindi chiedi al coordinatore
  l'uscita di `uv run reel stile --trascrizioni` (la stima a occhio ha sbagliato tre account su dodici). `reel stile`
  legge la **prima** occorrenza di «Reel letti:» e «Letto il:»: fuori dalla sezione Corpus quelle due stringhe non si
  scrivono. Le contraddizioni con i limiti del repo stanno anche nella guida, in breve, con «decisa» o «aperta».
