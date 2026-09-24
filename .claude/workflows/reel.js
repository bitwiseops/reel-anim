export const meta = {
  name: 'reel',
  description: "Da uno spunto, un'idea o una sceneggiatura fino all'anteprima --prova su cui registrare",
  whenToUse: "Corsa completa della pipeline dei reel senza fermate intermedie. args = percorso in contenuti/spunti/, contenuti/idee/ o contenuti/sceneggiature/",
  phases: [
    { title: 'Idea', detail: "ideatore sullo spunto (saltata se si parte da un'idea o da una sceneggiatura)" },
    { title: 'Copione', detail: 'il parlato da un modello esterno (reel copione, catena di [copione]), se l\'idea non ce l\'ha già', model: 'haiku' },
    { title: 'Sceneggiatura', detail: "uscite vere se servono, sceneggiatore sul copione; poi valida a 0 errori e l'idea passa a sceneggiata" },
    { title: 'Fonti', detail: 'un verificatore-fonte per fonte, in parallelo', model: 'sonnet' },
    { title: 'Revisione', detail: 'revisore-tecnico con le schede delle fonti: con un ❌ la corsa si ferma' },
    { title: 'Filmati', detail: 'broll: marca le scene (in serie), poi cerca e mette in fila; la metà più debole va a immagini (Meshy); tutto in parallelo con l\'animazione', model: 'sonnet' },
    { title: 'Animazione', detail: 'animatore: .py, anima --json a zero avvisi e zero controlli' },
    { title: 'Fotogrammi', detail: 'monta --prova, poi un controllore-fotogrammi per scena animata, in parallelo; al massimo due rimandi', model: 'sonnet' },
    { title: 'Rapporto', detail: 'VOCE per scena, durate, avvisi, fotogrammi, prossimo passo', model: 'sonnet' },
  ],
}

// Ogni tappa chiude con lo stesso schema: i controlli fra le tappe sono confronti, non giudizi.
const ESITO = {
  type: 'object',
  required: ['stato', 'file', 'errori', 'avvisi', 'bloccato', 'motivo'],
  properties: {
    stato: { type: 'string', description: 'stato del file dopo la tappa (stato: nel frontmatter, o **Stato:** di un\'idea)' },
    file: { type: 'string', description: 'percorso del file prodotto o aggiornato, relativo alla radice del repo' },
    errori: { type: 'integer' },
    avvisi: { type: 'integer' },
    bloccato: { type: 'boolean' },
    motivo: { type: 'string', description: 'perché si è bloccato, oppure note per il presentatore' },
  },
}
const FONTI = {
  type: 'object',
  required: ['fonti'],
  properties: {
    fonti: {
      type: 'array',
      items: {
        type: 'object',
        required: ['url', 'claim'],
        properties: {
          url: { type: 'string', description: 'URL della fonte (o titolo esatto, se manca il link)' },
          claim: { type: 'array', items: { type: 'string' }, description: 'i claim del reel che poggiano su questa fonte, alla lettera' },
        },
      },
    },
  },
}
const SCENE = {
  type: 'object',
  required: ['scene'],
  properties: { scene: { type: 'array', items: { type: 'integer' }, description: 'numeri delle scene ANIMATE (con un video in ~/Library/Caches/reel-anim/<slug>/_scene/ e una classe Manim)' } },
}
const vuoto = (motivo) => ({ stato: '', file: '', errori: 0, avvisi: 0, bloccato: true, motivo })

// Un agente che non c'è nel registro (creato in questa sessione) o che muore non fa crollare la corsa: la ferma.
async function tappa(fase, prompt, agentType, extra) {
  try {
    const r = await agent(prompt, { agentType, phase: fase, label: `${fase} · ${agentType}`, schema: ESITO, ...(extra || {}) })
    return r || vuoto(`${agentType}: agente saltato o terminato senza risposta`)
  } catch (e) {
    return vuoto(`${agentType}: ${e && e.message ? e.message : String(e)}`)
  }
}
const ferma = (fase, r) => { log(`fermata a ${fase}: ${r.motivo}`); return { fermato_a: fase, ...r } }
// Le tappe che lanciano un comando e ne riportano l'esito non hanno bisogno del modello forte.
const COMANDO = { model: 'haiku', effort: 'low' }

const partenza = String(args || '').trim()
if (!partenza) return ferma('avvio', vuoto("manca args: il percorso di uno spunto, di un'idea o di una sceneggiatura"))
let idea = partenza
let file = partenza
let noteSceneggiatore = ''

if (partenza.includes('contenuti/spunti/')) {
  phase('Idea')
  const r = await tappa('Idea', `Spunto: ${partenza}. Scrivi l'idea in contenuti/idee/ e porta lo spunto a stato: ideato con idea: nel frontmatter. Nel campo file il percorso dell'idea.`, 'ideatore')
  if (r.bloccato || !r.file.includes('contenuti/idee/')) return ferma('idea', r)
  idea = r.file
  log(`idea: ${idea}`)
}

if (!partenza.includes('contenuti/sceneggiature/')) {
  phase('Sceneggiatura')
  // T0b, T0c, T1 di pipeline.md
  const u = await tappa('Sceneggiatura',
    `Tappa T0b di .claude/commands/pipeline.md su ${idea}. Se l'idea ha già la riga \`**Uscite:**\`, o se \`uv run reel uscite ${idea} --prova-a-secco\` ` +
    `dice che non ci sono richieste da generare, non fare niente: bloccato = false, motivo = "nessuna uscita da generare". ` +
    `Altrimenti lancia \`uv run reel uscite ${idea}\` e riporta in motivo il percorso del file e le uscite segnalate «da ricontrollare». ` +
    `bloccato = true solo se il comando fallisce. stato = "idea", file = ${idea}, errori = 0, avvisi = numero di uscite da ricontrollare.`,
    'general-purpose', COMANDO)
  if (u.bloccato) return ferma('uscite', u)
  phase('Copione')
  const cp = await tappa('Copione',
    `Tappa T0c di .claude/commands/pipeline.md su ${idea}. Se l'idea ha già la riga \`**Copione:**\` e il file esiste, non fare niente: bloccato = false, motivo = "copione già scritto: <percorso>". ` +
    `Altrimenti lancia \`uv run reel copione ${idea} --prova-a-secco > /dev/null\` (riporta in motivo il saldo e i modelli che si salterebbero), poi \`uv run reel copione ${idea}\` UNA volta sola (costa punti Poe: mai rilanciarlo). ` +
    `In motivo: il percorso del copione, il modello che l'ha scritto, gli anelli saltati o falliti. avvisi = numero di righe ⚠. bloccato = true solo se il comando fallisce. stato = "copione", file = il percorso del copione.`,
    'general-purpose', COMANDO)
  if (cp.bloccato) return ferma('copione', cp)
  log(`copione: ${cp.motivo}`)
  let s = await tappa('Sceneggiatura', `Idea: ${idea}. La VOCE è il copione indicato da **Copione:** nell'idea: prendilo alla lettera e scrivi la sceneggiatura in contenuti/sceneggiature/ finché \`uv run reel valida\` non ha errori. Non toccare il file idea.`, 'sceneggiatore')
  if (s.bloccato || !s.file.includes('contenuti/sceneggiature/')) return ferma('sceneggiatura', s)
  let c = null
  for (let giro = 1; giro <= 3; giro++) {
    c = await tappa('Sceneggiatura',
      `Esegui \`uv run reel valida ${s.file}\` senza modificare la sceneggiatura e metti in errori e avvisi i conteggi, in motivo le righe di errore. ` +
      `Solo se gli errori sono 0: con Edit porta ${idea} a \`**Stato:** sceneggiata\` e aggiungi \`**Sceneggiatura:** ${s.file}\` sotto la riga dello stato (se c'è già, non duplicarla). ` +
      `stato = "sceneggiatura", file = ${s.file}, bloccato = false.`,
      'general-purpose', COMANDO)
    if (c.bloccato || c.errori === 0 || giro === 3) break
    s = await tappa('Sceneggiatura', `Correggi ${s.file}: \`uv run reel valida\` dà ancora errori:\n${c.motivo}\nRiscrivi lo stesso file, niente duplicati.`, 'sceneggiatore')
    if (s.bloccato) return ferma('sceneggiatura', s)
  }
  if (c.bloccato || c.errori > 0) return ferma('valida', c)
  file = s.file
  noteSceneggiatore = `${s.motivo} · copione: ${cp.motivo}`
  log(`sceneggiatura: ${file} (${c.avvisi} avvisi)`)
}

// T2
phase('Fonti')
let schede = ''
const elenco = await agent(
  `Leggi ${file} e il file idea indicato da \`idea:\` nel frontmatter. Se il frontmatter è già stato: rivisto o animato, restituisci fonti = []. ` +
  `Altrimenti elenca le FONTI ESTERNE su cui poggiano numeri e fatti del reel (sezione ## Fonte e «claim per il revisore» dell'idea, Note di produzione della sceneggiatura) ` +
  `e per ciascuna i claim del reel che le sono attribuiti, alla lettera (VOCE, numeri a schermo, FIGURA:). Solo fonti con un URL o un titolo preciso; nessuna fonte → fonti = [].`,
  { agentType: 'general-purpose', model: 'sonnet', effort: 'low', phase: 'Fonti', label: 'Fonti · elenco', schema: FONTI })
const fonti = (elenco && elenco.fonti) || []
if (fonti.length) {
  const esiti = await parallel(fonti.map((f, i) => () =>
    agent(`Fonte: ${f.url}\nClaim che il reel le attribuisce:\n- ${f.claim.join('\n- ')}\nSceneggiatura (per il contesto): ${file}`,
      { agentType: 'verificatore-fonte', phase: 'Fonti', label: `Fonte ${i + 1} · ${f.url.slice(0, 50)}` })))
  schede = esiti.filter(Boolean).join('\n\n')
  log(`fonti verificate: ${esiti.filter(Boolean).length} su ${fonti.length}`)
}

phase('Revisione')
const rv = await tappa('Revisione',
  `Rivedi ${file}. Se il frontmatter è già stato: rivisto (o animato) e la Revisione tecnica dice APPROVATO, non rifarla: restituisci lo stato com'è.` +
  (schede ? `\n\nSchede dei verificatore-fonte (parti da queste; riapri tu solo le fonti dubbie o decisive):\n\n${schede}` : ''),
  'revisore-tecnico')
if (rv.bloccato || !['rivisto', 'animato'].includes(rv.stato)) return ferma('revisione', rv)

// T2b primo tempo
phase('Filmati')
const marca = await tappa('Filmati',
  `Modalità: marca. Sceneggiatura: ${file}. Se le scene a filmato sono già [broll] nel file e l'equilibrio torna, non rifare niente e dillo.`, 'broll')
if (marca.bloccato || marca.errori > 0) return ferma('filmati (marca)', marca)

// (T2b secondo tempo → T2c) ∥ T3: la scelta dei filmati è provvisoria
const [fl0, an0] = await parallel([
  async () => {
    const b = await tappa('Filmati', `Modalità: scegli, scelta PROVVISORIA (--tutto). Sceneggiatura: ${file}. ` +
      `Metti in fila le scene a filmato per quanto convince il miglior filmato e scrivi in motivo «scene per Meshy: N, M» (la metà più debole): per quelle non scegliere né rendere niente.`, 'broll')
    if (b.bloccato || b.errori > 0) return b
    const im = await tappa('Filmati', `Sceneggiatura: ${file}. Rapporto di broll (le scene per Meshy sono lì): ${b.motivo}`, 'immagini')
    return { ...im, motivo: `${b.motivo} · immagini: ${im.motivo}`, bloccato: im.bloccato, errori: b.errori + im.errori }
  },
  () => tappa('Animazione',
    `Anima ${file} fino a \`uv run reel anima ${file} --json\` con 0 avvisi di tempo e 0 controlli, e porta il frontmatter a stato: animato. ` +
    `I filmati delle scene [broll] si stanno rendendo in parallelo: se \`monta --prova --anteprima\` fallisce solo perché un filmato manca, non è un tuo errore (dillo in motivo): il montaggio lo rifà il coordinatore.`,
    'animatore'),
])
const fl = fl0 || vuoto('broll: nessuna risposta')
let an = an0 || vuoto('animatore: nessuna risposta')
if (fl.bloccato || fl.errori > 0) return ferma('filmati (scegli)', fl)
if (an.bloccato || an.stato !== 'animato') return ferma('animazione', an)

// T3b e T4
phase('Fotogrammi')
const MONTA = `Esegui \`uv run broll piano ${file}\` e, se una scena è tornata a «scelto», \`uv run broll rendi <slug>\`; ` +
  `poi \`uv run reel monta ${file} --prova --anteprima\`. Non modificare nessun file a mano. errori/avvisi = i conteggi del montaggio ` +
  `(da contenuti/render/<slug>/report.json), motivo = durata del reel e righe di errore, bloccato = true se il montaggio fallisce. stato = "animato", file = ${file}.`
let mt = await tappa('Fotogrammi', MONTA, 'general-purpose', COMANDO)
if (mt.bloccato) return ferma('montaggio', mt)
const sc = await agent(
  `Leggi ${file} e contenuti/render/<slug>/report.json (lo slug è nel frontmatter): elenca i numeri delle scene ANIMATE, cioè non [broll], non a volto pieno (apertura e chiusura), con un video in ~/Library/Caches/reel-anim/<slug>/_scene/NN.mp4 (il campo «video» di report.json).`,
  { agentType: 'general-purpose', ...COMANDO, phase: 'Fotogrammi', label: 'Fotogrammi · scene', schema: SCENE })
const scene = (sc && sc.scene) || []
let difetti = ''
for (let rimando = 0; rimando <= 2 && scene.length; rimando++) {
  const occhi = await parallel(scene.map((n) => () =>
    agent(`Sceneggiatura: ${file}. Scena: ${n}.`, { agentType: 'controllore-fotogrammi', phase: 'Fotogrammi', label: `Scena ${n} · giro ${rimando + 1}`, schema: ESITO })))
  const gravi = occhi.filter(Boolean).filter((o) => o.errori > 0 && !o.bloccato)
  difetti = occhi.filter(Boolean).filter((o) => o.errori > 0 || o.avvisi > 0).map((o) => o.motivo).join('\n\n')
  log(`controllo fotogrammi, giro ${rimando + 1}: ${gravi.length} scene con difetti gravi su ${scene.length}`)
  if (!gravi.length || rimando === 2) break
  an = await tappa('Animazione',
    `Rimando dei controllore-fotogrammi su ${file}: correggi i difetti GRAVI qui sotto (scena, beat, istante), rilancia \`anima --json\` sulle scene toccate fino a 0 avvisi e 0 controlli, ` +
    `e riguarda quei passaggi con \`uv run reel strisce ${file} --scena N --sorgente anima\`. Non toccare le scene senza difetti.\n\n${gravi.map((o) => o.motivo).join('\n\n')}`,
    'animatore')
  if (an.bloccato) return ferma('animazione (rimando)', an)
  mt = await tappa('Fotogrammi', MONTA, 'general-purpose', COMANDO)
  if (mt.bloccato) return ferma('montaggio', mt)
}

phase('Rapporto')
const rapporto = await agent(
  `Scrivi il report unico per il presentatore sul reel ${file}, seguendo la sezione «Report della FERMATA 3» di .claude/commands/pipeline.md. ` +
  `Leggi la sceneggiatura, l'idea collegata e contenuti/render/<slug>/report.json (lo slug è nel frontmatter). ` +
  `Note dello sceneggiatore (titolo alternativo, frasi del copione segnalate, scostamenti; e il modello che ha scritto il copione): ${noteSceneggiatore || 'nessuna'}. ` +
  `Revisione: ${rv.motivo || 'nessuna nota'}. Filmati: equilibrio e scene marcate: ${marca.motivo || '—'}; scelte PROVVISORIE, da mettere in testa ai punti da confermare: ${fl.motivo || 'nessuna scena a filmato'}. ` +
  `Animazione: ${an.motivo || 'nessuna nota'} (${an.errori} controlli, ${an.avvisi} avvisi di tempo). Montaggio: ${mt.motivo || '—'}. ` +
  `Difetti dei controllore-fotogrammi rimasti dopo i rimandi: ${difetti || 'nessuno'}.`,
  { agentType: 'general-purpose', model: 'sonnet', effort: 'low', phase: 'Rapporto', label: 'Rapporto' })
return { completato: true, file, rapporto }
