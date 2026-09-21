export const meta = {
  name: 'stile',
  description: 'Rifà docs/stile-parlato.md dal corpus di reelkit: schede dei reel in parallelo, poi lo stilista compone la guida',
  whenToUse: "Quando `uv run reel stile` dice che la guida manca o è da rifare. args (facoltativo) = numero massimo di reel da leggere (default 40, i più recenti)",
  phases: [
    { title: 'Corpus', detail: 'uv run reel stile: percorso del corpus, id dei reel, passo per account', model: 'haiku' },
    { title: 'Schede', detail: 'lotti di 8 reel annotati in parallelo: si osserva e si conta, non si interpreta', model: 'sonnet' },
    { title: 'Guida', detail: 'stilista: compone docs/stile-parlato.md dalle schede e ricontrolla le citazioni' },
  ],
}

const CORPUS = {
  type: 'object',
  required: ['corpus', 'reel', 'passo'],
  properties: {
    corpus: { type: 'string', description: "percorso assoluto dell'export.md di reelkit" },
    reel: { type: 'array', items: { type: 'string' }, description: 'id dei reel del corpus (r00NN), dal più recente' },
    passo: { type: 'string', description: "l'uscita di `uv run reel stile --trascrizioni`, così com'è" },
  },
}
const SCHEDE = {
  type: 'object',
  required: ['schede'],
  properties: {
    schede: {
      type: 'array',
      items: {
        type: 'object',
        required: ['id', 'account', 'attacco', 'connettivi', 'lunghezze', 'chiusura'],
        properties: {
          id: { type: 'string' },
          account: { type: 'string' },
          durata: { type: 'string' },
          tipo: { type: 'string', description: 'reel scritto | estratto da una diretta | altro' },
          affidabile: { type: 'boolean', description: 'false se le **Note:** dicono che la trascrizione è inaffidabile' },
          note_whisper: { type: 'string', description: 'errori di Whisper e code allucinate segnalati nelle **Note:** (dove tagliare)' },
          attacco: { type: 'string', description: 'le prime 10 parole, alla lettera' },
          connettivi: { type: 'array', items: { type: 'string' }, description: 'i connettivi che tornano, con il conteggio («quindi ×4»)' },
          lunghezze: { type: 'array', items: { type: 'integer' }, description: 'parole di 10 frasi a campione' },
          riprese: { type: 'array', items: { type: 'string' }, description: 'parole dette due volte di fila, soggetto ripreso in coda: alla lettera' },
          domande: { type: 'array', items: { type: 'string' }, description: 'domande a chi guarda o a se stesso, alla lettera' },
          chiusura: { type: 'string', description: 'le ultime due frasi, alla lettera' },
          non_fa: { type: 'array', items: { type: 'string' }, description: 'elenchi, titoli in fila, sigle, «oggi parliamo di», antitesi in coppia, terne per il ritmo: cosa c\'è e cosa no' },
          citazioni: { type: 'array', items: { type: 'string' }, description: '1-3 frasi testuali che suonano parlato vero, SENZA errori di Whisper dentro' },
          analisi: { type: 'string', description: "cosa il presentatore vuole imparare da questo reel, dall'**Analisi**, in due righe" },
        },
      },
    },
  },
}

phase('Corpus')
const massimo = Number(args) > 0 ? Number(args) : 40
const c = await agent(
  `Nel repo: lancia \`uv run reel stile\` e \`uv run reel stile --trascrizioni\`. Dal primo prendi il percorso del corpus (export.md di reelkit); ` +
  `nel corpus i reel sono i titoli \`### <id> · <durata>\` sotto \`## <account>\`: elenca tutti gli id con \`grep -n '^### ' <corpus>\`, ordinati dal più recente (id più alto). ` +
  `In passo metti l'uscita del secondo comando così com'è.`,
  { agentType: 'general-purpose', model: 'haiku', effort: 'low', phase: 'Corpus', label: 'Corpus', schema: CORPUS })
if (!c || !c.reel || !c.reel.length) return { completato: false, motivo: 'corpus vuoto o assente: lo stilista scrive la guida provvisoria, lancialo a mano' }
const reel = c.reel.slice(0, massimo)
if (c.reel.length > massimo) log(`corpus di ${c.reel.length} reel: letti i ${massimo} più recenti, esclusi ${c.reel.slice(massimo).join(', ')}`)

phase('Schede')
const lotti = []
for (let i = 0; i < reel.length; i += 8) lotti.push(reel.slice(i, i + 8))
const esiti = await parallel(lotti.map((lotto, i) => () =>
  agent(
    `Corpus: ${c.corpus} (export di reelkit: per ogni reel \`### <id> · <durata>\`, \`- URL:\`, **Trascrizione** di Whisper, **Analisi** del presentatore con le **Note:** in fondo). ` +
    `Compila una scheda per ciascuno di questi reel: ${lotto.join(', ')}. Leggi PRIMA le **Note:** (dicono quali trascrizioni sono inaffidabili e dove tagliare le code allucinate), poi la trascrizione. ` +
    `Osserva e conta, non interpretare: tutto ciò che citi è alla lettera, mai ritoccato. Punteggiatura e maiuscole sono di Whisper, non dell'autore: guarda le parole, l'ordine, le ripetizioni. ` +
    `Nomi propri e cifre non valgono come dati. Una citazione con un errore di Whisper dentro si scarta.`,
    { agentType: 'general-purpose', model: 'sonnet', phase: 'Schede', label: `Schede · lotto ${i + 1} (${lotto[0]}…)`, schema: SCHEDE })))
const schede = esiti.filter(Boolean).flatMap((e) => e.schede)
const mancanti = reel.filter((id) => !schede.some((s) => s.id === id))
if (mancanti.length) log(`senza scheda: ${mancanti.join(', ')} (lo stilista li legge dal corpus)`)

phase('Guida')
const guida = await agent(
  `Rifai docs/stile-parlato.md. Il coordinatore ti passa le schede dei reel (${schede.length} su ${reel.length}): conta su queste, e riapri il corpus (${c.corpus}) solo per ` +
  `ricontrollare parola per parola le citazioni che metti nella guida e per i reel senza scheda (${mancanti.join(', ') || 'nessuno'}). ` +
  `Passo per account (uscita di \`uv run reel stile --trascrizioni\`):\n${c.passo}\n\nSchede:\n${JSON.stringify(schede)}`,
  { agentType: 'stilista', phase: 'Guida', label: 'Guida · stilista' })
return { completato: true, reel_letti: reel.length, schede: schede.length, senza_scheda: mancanti, rapporto: guida }
