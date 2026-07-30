import type { Formula, TagId } from '../data/types'
import { formulas, getChapter } from '../data/catalog'

/** Banglish / English / Bangla aliases for better recall. */
const ALIASES: Record<string, string[]> = {
  lorentz: ['লরেঞ্জ', 'লরেঞ্জ বল', 'lorentz force'],
  biot: ['বায়োট', 'সাভার্ট', 'biot-savart'],
  savart: ['বায়োট', 'সাভার্ট'],
  solenoid: ['সোলেনয়েড'],
  toroid: ['টরয়েড'],
  ammeter: ['অ্যামিটার', 'এমিটার'],
  voltmeter: ['ভোল্টমিটার'],
  shunt: ['শাণ্ট', 'শান্ট'],
  flux: ['ফ্লাক্স'],
  hall: ['হল', 'হল বিভব'],
  cyclotron: ['সাইক্লোট্রন'],
  force: ['বল'],
  field: ['ক্ষেত্র', 'চৌম্বক ক্ষেত্র', 'তড়িৎক্ষেত্র'],
  earth: ['ভূ-চৌম্বক', 'বিনতি'],
  dip: ['বিনতি'],
  torque: ['টর্ক', 'ভ্রামক'],
  moment: ['ভ্রামক', 'মোমেন্ট', 'ডাইপোল'],
  wire: ['তার', 'পরিবাহী'],
  loop: ['লুপ', 'কুণ্ডলী', 'কুন্ডলী'],
  radius: ['ব্যাসার্ধ'],
  freq: ['কম্পাঙ্ক', 'frequency'],
  frequency: ['কম্পাঙ্ক'],
  important: ['গুরুত্বপূর্ণ', 'সর্বোচ্চ'],
  top: ['সর্বোচ্চ', '3-star'],
  ohm: ['ওহম', 'ওমের'],
  kirchhoff: ['কির্চফ', 'kirchoff'],
  wheatstone: ['হুইটস্টোন', 'হুইটস্টোন ব্রিজ'],
  potentiometer: ['পটেনশিওমিটার'],
  capacitor: ['ধারক', 'ক্যাপাসিটর'],
  dielectric: ['পরাবৈদ্যুতিক'],
  gauss: ['গাউস'],
  coulomb: ['কুলাম'],
  snell: ['স্নেল'],
  lens: ['লেন্স'],
  mirror: ['দর্পণ', 'আয়না'],
  prism: ['প্রিজম'],
  young: ['ইয়ং', 'ইয়ংস', 'ydse'],
  ydse: ['ইয়ং', 'দ্বি-স্লিট', 'young'],
  diffraction: ['অপবর্তন'],
  interference: ['ব্যতিচার'],
  photoelectric: ['ফটোইলেকট্রিক', 'আলোকতড়িৎ'],
  debroglie: ['ডি-ব্রগলি', 'দি ব্রগলি', 'de broglie'],
  bohr: ['বোর'],
  rydberg: ['রিডবার্গ'],
  radioactivity: ['তেজস্ক্রিয়', 'অর্ধায়ু', 'half life'],
  half: ['অর্ধায়ু', 'half-life', 't1/2'],
  carnot: ['কার্নো'],
  entropy: ['এনট্রপি'],
  bernoulli: ['বার্নোলি'],
  stokes: ['স্টোকস'],
  youngmodulus: ['ইয়ং গুণাঙ্ক'],
  shm: ['সরল ছন্দিত', 'শম', 'simple harmonic'],
  pendulum: ['দোলক'],
  doppler: ['ডপলার'],
  kepler: ['কেপলার'],
  escape: ['পালানোর বেগ', 'মুক্তিবেগ'],
  satellite: ['উপগ্রহ'],
  elevator: ['লিফট', 'লিফ্ট'],
  friction: ['ঘর্ষণ'],
  projectile: ['প্রক্ষিপ্ত', 'প্রজেক্টাইল'],
  momentum: ['ভরবেগ'],
  impulse: ['আবেগ'],
  work: ['কাজ'],
  energy: ['শক্তি'],
  power: ['ক্ষমতা'],
  // Chemistry (expanded)
  mole: ['মোল', 'অ্যাভোগাড্রো', 'avogadro'],
  ph: ['পিএইচ', 'হাইড্রোজেন', 'পিএইচ মান'],
  buffer: ['বাফার', 'henderson', 'হেন্ডারসন'],
  henderson: ['বাফার', 'হেন্ডারসন', 'hasselbalch'],
  organic: ['জৈব', 'অর্গানিক'],
  nernst: ['নার্নস্ট'],
  faraday: ['ফ্যারাডে', 'ফ্যারাডের'],
  colligative: ['সম্মিল', 'অসমোটিক', 'রাউল'],
  haber: ['হ্যাবার', 'অ্যামোনিয়া'],
  lechatelier: ['লা শাতেলিয়ে', 'le chatelier', 'লেশাটেলিয়ে', 'chatelier'],
  arrhenius: ['আরেনিয়াস', 'সক্রিয়ন'],
  hess: ['হেস', 'hess law'],
  ksp: ['দ্রাব্যতা', 'solubility', 'কেএসপি'],
  raoult: ['রাউল', 'রাউল্ট'],
  henry: ['হেনরি', 'henry'],
  sn1: ['এসএন১', 'sn1', 'নিউক্লিওফিলিক'],
  sn2: ['এসএন২', 'sn2'],
  vsepr: ['ভেস্পর', 'vsepr', 'আণবিক আকৃতি'],
  hybridization: ['হাইব্রিডাইজেশন', 'সংকরণ'],
  kohlrausch: ['কোলরাউশ', 'কোলরাউস'],
  markovnikov: ['মার্কোভনিকভ', 'মার্কফনিকভ'],
  grignard: ['গ্রিনইয়ার্ড', 'grignard'],
  ostwald: ['অস্টওয়াল্ড'],
  solvay: ['সলভে'],
  contact: ['কন্টাক্ট', 'সালফিউরিক'],
  titration: ['টাইট্রেশন', 'আয়তনমিতি'],
  normality: ['নরম্যালিটি', 'নরমাল'],
  molarity: ['মোলারিটি', 'মোলালিটি'],
  gibbs: ['গিবস', 'মুক্ত শক্তি'],
  nernstcell: ['কোশ বিভব'],
  cfse: ['সিএফএসই', 'ক্রিস্টাল ফিল্ড'],
  huckel: ['হুকেল', 'অ্যারোমেটিক', 'aromatic'],
  saponification: ['সাবান', 'স্যপোনিফিকেশন'],
  beer: ['বিয়ার', 'ল্যামবার্ট', 'absorbance'],
  chromatography: ['ক্রোমাটোগ্রাফি', 'rf'],
  // Math
  matrix: ['ম্যাট্রিক্স', 'নির্ণায়ক'],
  determinant: ['নির্ণায়ক', 'ডিটারমিন্যান্ট'],
  probability: ['সম্ভাব্যতা', 'বেইজ'],
  binomial: ['দ্বিপদী'],
  parabola: ['পরাবৃত্ত'],
  ellipse: ['উপবৃত্ত'],
  hyperbola: ['অধিবৃত্ত'],
  integral: ['যোগজ', 'ইন্টিগ্রাল'],
  derivative: ['অন্তরক', 'ডিফারেনশিয়াল'],
  sequence: ['অনুক্রম', 'ধারা', 'সমান্তর'],
  permutation: ['ক্রমবিন্যাস', 'সমাবেশ'],
  physics: ['পদার্থ', 'পদার্থবিজ্ঞান'],
  chemistry: ['রসায়ন'],
  math: ['গণিত', 'উচ্চতর গণিত'],
}

function normalize(input: string): string {
  return input
    .toLowerCase()
    .normalize('NFKC')
    .replace(/[।.!?,;:()[\]{}'"`]/g, ' ')
    .replace(/[-_/]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

function tokenize(query: string): string[] {
  const q = normalize(query)
  if (!q) return []
  return q.split(' ').filter((t) => t.length > 0)
}

function expandToken(token: string): string[] {
  const out = new Set<string>([token])
  const short = token.length < 3
  for (const [key, aliases] of Object.entries(ALIASES)) {
    const keyHit = short
      ? token === key || key.startsWith(token)
      : token === key || token.includes(key) || key.includes(token)
    if (keyHit) {
      out.add(key)
      for (const a of aliases) out.add(normalize(a))
    }
    for (const a of aliases) {
      const na = normalize(a)
      const aliasHit = short
        ? token === na || na.startsWith(token)
        : token === na || token.includes(na) || na.includes(token)
      if (aliasHit) {
        out.add(key)
        out.add(na)
      }
    }
  }
  return [...out]
}

interface SearchDoc {
  formula: Formula
  id: string
  title: string
  summary: string
  latex: string
  full: string
}

function buildDoc(formula: Formula): SearchDoc {
  const chapter = getChapter(formula.chapter)
  const parts = [
    formula.id,
    formula.title,
    formula.titleBn,
    formula.summary,
    formula.latex,
    formula.chapter,
    chapter?.name,
    chapter?.nameBn,
    ...(formula.tags ?? []),
    ...(formula.symbols ?? []).flatMap((s) => [s.symbol, s.meaning, s.unit]),
    formula.derivation?.lead,
    formula.memorize?.trick,
    ...(formula.memorize?.steps ?? []),
    ...(formula.questions ?? []).flatMap((q) => [q.question, q.examType]),
  ]
  return {
    formula,
    id: normalize(formula.id),
    title: normalize(`${formula.title} ${formula.titleBn}`),
    summary: normalize(formula.summary),
    latex: normalize(formula.latex),
    full: normalize(parts.filter(Boolean).join(' · ')),
  }
}

/** Precomputed once — avoids rebuilding haystacks on every keystroke. */
const SEARCH_INDEX: SearchDoc[] = formulas.map(buildDoc)
const DOC_BY_ID = new Map(SEARCH_INDEX.map((d) => [d.formula.id, d]))

function passesTag(formula: Formula, activeTag?: TagId | null): boolean {
  if (!activeTag) return true
  const imp = formula.importance ?? 2
  if (activeTag === '3-star') return imp === 3
  if (activeTag === '2-star') return imp === 2
  if (activeTag === '1-star') return imp === 1
  return formula.tags.includes(activeTag)
}

function starMatch(q: string, imp: number): boolean | null {
  // Avoid hijacking bare "1"/"2"/"3" / "*" as importance filters
  if (q === '3 star' || q === '3star' || q === '***' || q === '৩★') return imp === 3
  if (q === '2 star' || q === '2star' || q === '**' || q === '২★') return imp === 2
  if (q === '1 star' || q === '1star' || q === '১★') return imp === 1
  return null
}

function scoreDoc(doc: SearchDoc, tokens: string[]): number {
  if (!tokens.length) return 1
  let score = 0

  for (const token of tokens) {
    const variants = expandToken(token)
    let best = 0
    for (const v of variants) {
      if (!v) continue
      if (doc.id === v || doc.title === v) best = Math.max(best, 120)
      else if (doc.id.includes(v)) best = Math.max(best, 95)
      else if (doc.title.startsWith(v) || doc.title.includes(` ${v}`)) best = Math.max(best, 88)
      else if (doc.title.includes(v)) best = Math.max(best, 72)
      else if (doc.summary.includes(v)) best = Math.max(best, 48)
      else if (doc.latex.includes(v)) best = Math.max(best, 40)
      else if (doc.full.includes(v)) best = Math.max(best, 28)
    }
    if (best === 0) return 0
    score += best
  }

  score += (doc.formula.importance ?? 2) * 2
  score += Math.max(0, 24 - doc.formula.title.length / 4)
  return score
}

/** Compatibility helper used across the app. */
export function matchFormula(
  formula: Formula,
  query: string,
  activeTag?: TagId | null,
): boolean {
  if (!passesTag(formula, activeTag)) return false
  const tokens = tokenize(query)
  if (!tokens.length) return true

  const q = normalize(query)
  const imp = formula.importance ?? 2
  const star = starMatch(q, imp)
  if (star !== null) return star

  const doc = DOC_BY_ID.get(formula.id) ?? buildDoc(formula)
  return scoreDoc(doc, tokens) > 0
}

export interface RankedFormula {
  formula: Formula
  score: number
}

/** Ranked search — use for menus and home hits. */
export function searchFormulas(
  list: Formula[],
  query: string,
  activeTag?: TagId | null,
  limit = 40,
): RankedFormula[] {
  const tokens = tokenize(query)
  const q = normalize(query)
  const allow = new Set(list.map((f) => f.id))

  const docs = SEARCH_INDEX.filter((d) => {
    if (!allow.has(d.formula.id)) return false
    if (!passesTag(d.formula, activeTag)) return false
    if (!tokens.length) return true
    const star = starMatch(q, d.formula.importance ?? 2)
    if (star !== null) return star
    return scoreDoc(d, tokens) > 0
  })

  if (!tokens.length) {
    return docs.slice(0, limit).map((d) => ({ formula: d.formula, score: 1 }))
  }

  return docs
    .map((d) => ({ formula: d.formula, score: scoreDoc(d, tokens) }))
    .sort((a, b) => b.score - a.score || a.formula.title.localeCompare(b.formula.title))
    .slice(0, limit)
}

/** Quick suggestion chips — balanced across subjects. */
export const SEARCH_SUGGESTIONS = [
  'lorentz',
  'Nernst',
  'Ksp',
  'matrix',
  'কার্নো',
  'SN1',
  'Bernoulli',
  'pH',
  'হুকেল',
  'Hess',
] as const
