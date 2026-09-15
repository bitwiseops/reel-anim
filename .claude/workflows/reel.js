export const meta = {
  name: 'reel',
  description: "Da uno spunto, un'idea o una sceneggiatura fino all'anteprima --prova su cui registrare",
  whenToUse: "Corsa completa della pipeline dei reel senza fermate intermedie. args = percorso in contenuti/spunti/, contenuti/idee/ o contenuti/sceneggiature/",
  phases: [
    { title: 'Idea', detail: "ideatore sullo spunto (saltata se si parte da un'idea o da una sceneggiatura)" },
    { title: 'Sceneggiatura', detail: "sceneggiatore; poi valida a 0 errori e l'idea passa a sceneggiata" },
    { title: 'Revisione', detail: 'revisore-tecnico: con un ❌ la corsa si ferma' },
    { title: 'Animazione', detail: 'animatore: .py, anima --json, fotogrammi, monta --prova --anteprima' },
    { title: 'Rapporto', detail: 'VOCE per scena, durate, avvisi, fotogrammi, prossimo passo' },
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
  let s = await tappa('Sceneggiatura', `Idea: ${idea}. Scrivi la sceneggiatura in contenuti/sceneggiature/ finché \`uv run reel valida\` non ha errori. Non toccare il file idea.`, 'sceneggiatore')
  if (s.bloccato || !s.file.includes('contenuti/sceneggiature/')) return ferma('sceneggiatura', s)
  let c = null
  for (let giro = 1; giro <= 3; giro++) {
    c = await tappa('Sceneggiatura',
      `Esegui \`uv run reel valida ${s.file}\` senza modificare la sceneggiatura e metti in errori e avvisi i conteggi, in motivo le righe di errore. ` +
      `Solo se gli errori sono 0: con Edit porta ${idea} a \`**Stato:** sceneggiata\` e aggiungi \`**Sceneggiatura:** ${s.file}\` sotto la riga dello stato (se c'è già, non duplicarla). ` +
      `stato = "sceneggiatura", file = ${s.file}, bloccato = false.`,
      'general-purpose', { effort: 'low' })
    if (c.bloccato || c.errori === 0 || giro === 3) break
    s = await tappa('Sceneggiatura', `Correggi ${s.file}: \`uv run reel valida\` dà ancora errori:\n${c.motivo}\nRiscrivi lo stesso file, niente duplicati.`, 'sceneggiatore')
    if (s.bloccato) return ferma('sceneggiatura', s)
  }
  if (c.bloccato || c.errori > 0) return ferma('valida', c)
  file = s.file
  noteSceneggiatore = s.motivo
  log(`sceneggiatura: ${file} (${c.avvisi} avvisi)`)
}

phase('Revisione')
const rv = await tappa('Revisione', `Rivedi ${file}. Se il frontmatter è già stato: rivisto (o animato) e la Revisione tecnica dice APPROVATO, non rifarla: restituisci lo stato com'è.`, 'revisore-tecnico')
if (rv.bloccato || !['rivisto', 'animato'].includes(rv.stato)) return ferma('revisione', rv)

phase('Animazione')
const an = await tappa('Animazione', `Anima ${file} fino a \`uv run reel monta ${file} --prova --anteprima\` con 0 avvisi di tempo e 0 controlli, e porta il frontmatter a stato: animato.`, 'animatore')
if (an.bloccato || an.stato !== 'animato') return ferma('animazione', an)

phase('Rapporto')
const rapporto = await agent(
  `Scrivi il report unico per il presentatore sul reel ${file}, seguendo la sezione «Report della FERMATA 3» di .claude/commands/pipeline.md. ` +
  `Leggi la sceneggiatura, l'idea collegata e contenuti/render/<slug>/report.json (lo slug è nel frontmatter). ` +
  `Note dello sceneggiatore (titolo alternativo, frasi incerte): ${noteSceneggiatore || 'nessuna'}. ` +
  `Revisione: ${rv.motivo || 'nessuna nota'}. Animazione: ${an.motivo || 'nessuna nota'} (${an.errori} controlli, ${an.avvisi} avvisi di tempo).`,
  { agentType: 'general-purpose', effort: 'low', phase: 'Rapporto', label: 'Rapporto' })
return { completato: true, file, rapporto }
