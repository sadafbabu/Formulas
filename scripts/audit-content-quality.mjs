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
}

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

  const questions = data.questions || []
  if (
    questions.length === 0 ||
    questions.some(
      (q) =>
        /সূত্রটি লেখো|ইঙ্গিত:/.test(q.question || '') ||
        (q.question || '').trim().length < 12,
    )
  ) {
    stats.templateQuestions.push(rel)
  }

  const der = data.derivation || {}
  const derSteps = der.steps || []
  if (derSteps.length < 2 || ((der.lead || '').trim().length < 30 && derSteps.length <= 1)) {
    stats.weakDerivation.push(rel)
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

const report = {
  total: stats.total,
  weakMemorize: { count: stats.weakMemorize.length, byImportance: byImp(stats.weakMemorize), bySubject: bySubj(stats.weakMemorize) },
  stubSummary: { count: stats.stubSummary.length, byImportance: byImp(stats.stubSummary) },
  stubSymbols: { count: stats.stubSymbols.length, byImportance: byImp(stats.stubSymbols) },
  templateQuestions: { count: stats.templateQuestions.length, byImportance: byImp(stats.templateQuestions) },
  weakDerivation: { count: stats.weakDerivation.length, byImportance: byImp(stats.weakDerivation) },
}

if (process.argv.includes('--json')) {
  console.log(JSON.stringify({ ...report, weakMemorizeIds: stats.weakMemorize }, null, 2))
} else {
  console.log('Content quality audit')
  console.log(JSON.stringify(report, null, 2))
}
