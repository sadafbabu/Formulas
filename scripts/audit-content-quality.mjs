#!/usr/bin/env node
/**
 * Audit formula content quality (memorize, summary, symbols, questions).
 * Usage: node scripts/audit-content-quality.mjs [--json]
 */
import fs from 'node:fs'
import path from 'node:path'

const root = path.join(process.cwd(), 'content', 'subjects')
const files = []

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const target = path.join(dir, entry.name)
    if (entry.isDirectory()) walk(target)
    else if (target.includes(`${path.sep}formulas${path.sep}`) && target.endsWith('.json')) {
      files.push(target)
    }
  }
}

walk(root)

const stats = {
  total: 0,
  weakMemorize: [],
  stubSummary: [],
  stubSymbols: [],
  templateQuestions: [],
  weakDerivation: [],
  autoMemorizeSteps: [],
  relatedRashiSymbols: [],
  oldTemplateQuestions: [],
  dupDerivationLatex: [],
  softEchoMemorize: [],
  softQuestions: [],
  echoSummaryTrickLead: [],
  junkSymbols: [],
}

const OPERATOR_SYMBOLS = new Set([
  'sum', 'prod', 'int', 'rightarrow', 'leftarrow', 'xrightarrow',
  'rightleftharpoons', 'cdot', 'times', 'main:',
])

for (const file of files) {
  const data = JSON.parse(fs.readFileSync(file, 'utf8'))
  const subject = path.relative(root, file).split(path.sep)[0]
  const rel = { id: data.id, subject, importance: data.importance ?? 2, chapter: data.chapter }
  stats.total++

  const mem = data.memorize || {}
  const trick = (mem.trick || '').trim()
  const steps = mem.steps || []
  if (!trick || steps.length < 2 || trick.length < 30) {
    stats.weakMemorize.push(rel)
  }
  const stepJoined = steps.join(' | ')
  if (
    steps.some((s) => String(s).startsWith('সূত্র:')) ||
    stepJoined.includes('চিহ্ন মনে রাখো') ||
    steps.some((s) => String(s).startsWith('কী কাজে লাগে:'))
  ) {
    stats.autoMemorizeSteps.push(rel)
  }
  if (
    steps.some((s) => /^(মনে রাখো —|চিহ্ন চেক:|কাজ:|প্রয়োগ:|পরীক্ষায়:)/.test(String(s)))
  ) {
    stats.softEchoMemorize.push(rel)
  }

  const summary = (data.summary || '').trim()
  if (summary.length < 24 || /^=|^[A-Za-z\\{}_^0-9Δλπσ≈∝\s+\-−]+$/.test(summary)) {
    stats.stubSummary.push(rel)
  }

  const symbols = data.symbols || []
  if (
    symbols.length === 0 ||
    symbols.some(
      (s) =>
        String(s.symbol || '').includes(',') ||
        s.unit === 'সূত্রানুযায়ী' ||
        (symbols.length === 1 && String(s.meaning || '').length < 8),
    )
  ) {
    stats.stubSymbols.push(rel)
  }
  if (symbols.some((s) => String(s.meaning || '').includes('সম্পর্কিত রাশি'))) {
    stats.relatedRashiSymbols.push(rel)
  }
  if (
    symbols.some((s) => {
      const sym = String(s.symbol || '').replace(/^\\/, '').replace(/[_^].*$/, '')
      const meaning = String(s.meaning || '')
      return (
        OPERATOR_SYMBOLS.has(sym) ||
        meaning.includes('(সূত্রের রাশি)') ||
        /\s/.test(String(s.symbol || '')) && String(s.symbol || '').length > 18
      )
    })
  ) {
    stats.junkSymbols.push(rel)
  }

  const questions = data.questions || []
  if (
    questions.length === 0 ||
    questions.some(
      (q) =>
        /সূত্রটি লেখো\.\s*\(ইঙ্গিত:/.test(q.question || '') ||
        (/ইঙ্গিত:/.test(q.question || '') && (q.question || '').length < 80) ||
        (q.question || '').trim().length < 12,
    )
  ) {
    stats.templateQuestions.push(rel)
  }
  if (
    questions.some(
      (q) =>
        (q.question || '').includes('কখন ব্যবহার করবে?') ||
        (q.question || '').trim().endsWith('মূল সম্পর্ক কী?'),
    )
  ) {
    stats.oldTemplateQuestions.push(rel)
  }
  if (
    questions.some((q) =>
      /লিখো এবং একটি ব্যবহার|দিয়ে কী নির্ণয়|মূল সূত্র কী\? এক লাইনে|সংক্ষেপে কী কাজে লাগে/.test(
        q.question || '',
      ),
    )
  ) {
    stats.softQuestions.push(rel)
  }

  const der = data.derivation || {}
  const derSteps = der.steps || []
  if (derSteps.length < 2 || ((der.lead || '').trim().length < 30 && derSteps.length <= 1)) {
    stats.weakDerivation.push(rel)
  }
  if (
    derSteps.length >= 2 &&
    (derSteps[0].latex || '') === (derSteps[1].latex || '')
  ) {
    stats.dupDerivationLatex.push(rel)
  }

  const lead = (der.lead || '').trim()
  if (summary && trick && lead && summary === trick && trick === lead) {
    stats.echoSummaryTrickLead.push(rel)
  }
}

const byImp = (list) => {
  const c = { 1: 0, 2: 0, 3: 0 }
  for (const x of list) c[x.importance] = (c[x.importance] || 0) + 1
  return c
}

const bySubj = (list) => {
  const c = {}
  for (const x of list) c[x.subject] = (c[x.subject] || 0) + 1
  return c
}

const bucket = (list) => ({
  count: list.length,
  byImportance: byImp(list),
  bySubject: bySubj(list),
})

const report = {
  total: stats.total,
  weakMemorize: bucket(stats.weakMemorize),
  stubSummary: bucket(stats.stubSummary),
  stubSymbols: bucket(stats.stubSymbols),
  templateQuestions: bucket(stats.templateQuestions),
  weakDerivation: bucket(stats.weakDerivation),
  templates: {
    autoMemorizeSteps: bucket(stats.autoMemorizeSteps),
    relatedRashiSymbols: bucket(stats.relatedRashiSymbols),
    oldTemplateQuestions: bucket(stats.oldTemplateQuestions),
    dupDerivationLatex: bucket(stats.dupDerivationLatex),
    softEchoMemorize: bucket(stats.softEchoMemorize),
    softQuestions: bucket(stats.softQuestions),
    echoSummaryTrickLead: bucket(stats.echoSummaryTrickLead),
    junkSymbols: bucket(stats.junkSymbols),
  },
}

if (process.argv.includes('--json')) {
  console.log(JSON.stringify({ ...report, weakMemorizeIds: stats.weakMemorize }, null, 2))
} else {
  console.log('Content quality audit')
  console.log(JSON.stringify(report, null, 2))
}
