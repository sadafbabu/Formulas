import fs from 'node:fs'
import path from 'node:path'
import katex from 'katex'
import 'katex/dist/contrib/mhchem.mjs'

const root = path.join(process.cwd(), 'content', 'subjects')
const tagPath = path.join(process.cwd(), 'content', 'tags.json')
const validTags = new Set(JSON.parse(fs.readFileSync(tagPath, 'utf8')).map((tag) => tag.id))
const files = []
const errors = []

function walk(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const target = path.join(directory, entry.name)
    if (entry.isDirectory()) walk(target)
    else if (target.includes(`${path.sep}formulas${path.sep}`) && target.endsWith('.json')) {
      files.push(target)
    }
  }
}

function fail(file, message) {
  errors.push(`${path.relative(process.cwd(), file)}: ${message}`)
}

function isRecord(value) {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function render(file, label, latex) {
  if (typeof latex !== 'string' || !latex.trim()) {
    fail(file, `${label} must be a non-empty string`)
    return 0
  }
  try {
    katex.renderToString(latex, { throwOnError: true, strict: 'ignore' })
    return 1
  } catch (error) {
    fail(file, `${label} does not render: ${error.message}`)
    return 0
  }
}

walk(root)

const formulas = []
for (const file of files) {
  try {
    formulas.push({ file, data: JSON.parse(fs.readFileSync(file, 'utf8')) })
  } catch (error) {
    fail(file, `invalid JSON: ${error.message}`)
  }
}

const idFiles = new Map()
const ordersByChapter = new Map()
let rendered = 0

for (const { file, data } of formulas) {
  const relative = path.relative(root, file).split(path.sep)
  const subject = relative[0]
  const chapter = relative[2]
  const filenameId = path.basename(file, '.json')

  for (const key of ['id', 'title', 'titleBn', 'summary', 'latex', 'chapter']) {
    if (typeof data[key] !== 'string' || !data[key].trim()) {
      fail(file, `${key} must be a non-empty string`)
    }
  }
  for (const key of ['tags', 'subjects', 'related', 'symbols']) {
    if (!Array.isArray(data[key])) fail(file, `${key} must be an array`)
  }
  if (!isRecord(data.derivation)) fail(file, 'derivation must be an object')
  if (!isRecord(data.memorize) || typeof data.memorize.trick !== 'string' || !data.memorize.trick.trim()) {
    fail(file, 'memorize.trick must be a non-empty string')
  }
  if (![1, 2, 3].includes(data.importance)) fail(file, 'importance must be 1, 2, or 3')
  if (!Number.isFinite(data.order)) fail(file, 'order must be a number')

  if (data.id !== filenameId) fail(file, `id "${data.id}" does not match filename "${filenameId}"`)
  if (data.chapter !== chapter) fail(file, `chapter "${data.chapter}" does not match path "${chapter}"`)
  if (JSON.stringify(data.subjects) !== JSON.stringify([subject])) {
    fail(file, `subjects must be exactly ["${subject}"]`)
  }
  if (subject === 'math' && data.tags?.includes('medical')) {
    fail(file, 'Higher Math formulas cannot use the medical admission tag')
  }

  const starTags = data.tags?.filter((tag) => tag.endsWith('-star')) ?? []
  if (JSON.stringify(starTags) !== JSON.stringify([`${data.importance}-star`])) {
    fail(file, `importance ${data.importance} must have exactly the ${data.importance}-star tag`)
  }
  for (const tag of data.tags ?? []) {
    if (!validTags.has(tag)) fail(file, `unknown tag "${tag}"`)
  }

  if (isRecord(data.derivation)) {
    if (!Array.isArray(data.derivation.steps) || data.derivation.steps.length === 0) {
      fail(file, 'derivation.steps must be a non-empty array')
    }
    if (!Array.isArray(data.derivation.assumptions)) {
      fail(file, 'derivation.assumptions must be an array')
    }
  }
  if (!Array.isArray(data.symbols) || data.symbols.length === 0) {
    fail(file, 'symbols must be a non-empty array')
  }

  idFiles.set(data.id, [...(idFiles.get(data.id) ?? []), file])
  const chapterOrders = ordersByChapter.get(chapter) ?? new Map()
  chapterOrders.set(data.order, [...(chapterOrders.get(data.order) ?? []), data.id])
  ordersByChapter.set(chapter, chapterOrders)

  rendered += render(file, 'latex', data.latex)
  for (const [index, step] of (data.derivation?.steps ?? []).entries()) {
    rendered += render(file, `derivation.steps[${index}].latex`, step.latex)
  }
  for (const [index, question] of (data.questions ?? []).entries()) {
    rendered += render(file, `questions[${index}].answer`, question.answer)
  }
}

for (const [id, matches] of idFiles) {
  if (matches.length > 1) {
    for (const file of matches) fail(file, `duplicate formula id "${id}"`)
  }
}

const allIds = new Set(idFiles.keys())
for (const { file, data } of formulas) {
  for (const relatedId of data.related ?? []) {
    if (!allIds.has(relatedId)) fail(file, `related id "${relatedId}" does not exist`)
    if (relatedId === data.id) fail(file, 'formula cannot relate to itself')
  }
}

const catalogPath = path.join(process.cwd(), 'src', 'data', 'catalog.ts')
const catalogSource = fs.readFileSync(catalogPath, 'utf8')
const catalogChapterIds = new Set(
  [...catalogSource.matchAll(/\{\s*id:\s*'([^']+)'/g)].map((m) => m[1]),
)
for (const { file, data } of formulas) {
  if (!catalogChapterIds.has(data.chapter)) {
    fail(file, `chapter "${data.chapter}" is missing from src/data/catalog.ts chapterList`)
  }
}

for (const [chapter, orderMap] of ordersByChapter) {
  for (const [order, ids] of orderMap) {
    if (ids.length > 1) {
      for (const id of ids) {
        const file = idFiles.get(id)?.[0] ?? chapter
        fail(file, `chapter order ${order} is shared by: ${ids.join(', ')}`)
      }
    }
  }
}

if (errors.length) {
  console.error(`Content validation failed with ${errors.length} problem(s):`)
  for (const error of errors) console.error(`- ${error}`)
  process.exit(1)
}

console.log(
  `Content valid: ${formulas.length} JSON files, ${allIds.size} unique IDs, ${rendered} KaTeX/mhchem expressions`,
)
