import tagsJson from '../../content/tags.json'
import physicsMeta from '../../content/subjects/physics/meta.json'

import type {
  BookPage,
  ChapterMeta,
  Formula,
  PaperMeta,
  SubjectMeta,
  Tag,
  TagId,
} from './types'

export const tags = tagsJson as Tag[]
export const subject: SubjectMeta = physicsMeta as SubjectMeta

export const papers: PaperMeta[] = [
  { id: '1st-paper', name: '1st Paper', nameBn: '১ম পত্র' },
  { id: '2nd-paper', name: '2nd Paper', nameBn: '২য় পত্র' },
]

export const subjectsList: SubjectMeta[] = [
  { id: 'physics', slug: 'physics', name: 'Physics', nameBn: 'পদার্থবিজ্ঞান', icon: '', color: '#ffffff', order: 1 },
  { id: 'chemistry', slug: 'chemistry', name: 'Chemistry', nameBn: 'রসায়ন', icon: '', color: '#ffffff', order: 2 },
  { id: 'math', slug: 'math', name: 'Higher Math', nameBn: 'উচ্চতর গণিত', icon: '', color: '#ffffff', order: 3 },
]

/** Chapter metadata. `formulaCount` is derived from the content files, never hand-written. */
const chapterList: Omit<ChapterMeta, 'formulaCount' | 'isReady'>[] = [
  // Physics 1st Paper (NCTB order)
  { id: 'measurement', slug: 'measurement', name: 'Physical World & Measurement', nameBn: 'ভৌত জগত ও পরিমাপ', subjectId: 'physics', paperId: '1st-paper', order: 1 },
  { id: 'vector', slug: 'vector', name: 'Vector', nameBn: 'ভেক্টর', subjectId: 'physics', paperId: '1st-paper', order: 2 },
  { id: 'motion-kinematics', slug: 'motion-kinematics', name: 'Motion & Kinematics', nameBn: 'গতিবিদ্যা', subjectId: 'physics', paperId: '1st-paper', order: 3 },
  { id: 'dynamics', slug: 'dynamics', name: 'Newtonian Mechanics', nameBn: 'নিউটনীয় বলবিদ্যা', subjectId: 'physics', paperId: '1st-paper', order: 4 },
  { id: 'work-energy', slug: 'work-energy', name: 'Work, Energy & Power', nameBn: 'কাজ, ক্ষমতা ও শক্তি', subjectId: 'physics', paperId: '1st-paper', order: 5 },
  { id: 'circular-motion', slug: 'circular-motion', name: 'Circular Motion', nameBn: 'বৃত্তাকার গতি', subjectId: 'physics', paperId: '1st-paper', order: 6 },
  { id: 'gravitation', slug: 'gravitation', name: 'Gravitation & Gravity', nameBn: 'মহাকর্ষ ও অভিকর্ষ', subjectId: 'physics', paperId: '1st-paper', order: 7 },
  { id: 'properties-of-matter', slug: 'properties-of-matter', name: 'Properties of Matter', nameBn: 'পদার্থের গুণাবলি', subjectId: 'physics', paperId: '1st-paper', order: 8 },
  { id: 'periodic-motion', slug: 'periodic-motion', name: 'Periodic Motion & SHM', nameBn: 'পর্যায়বৃত্ত গতি', subjectId: 'physics', paperId: '1st-paper', order: 9 },
  { id: 'waves', slug: 'waves', name: 'Waves', nameBn: 'তরঙ্গ', subjectId: 'physics', paperId: '1st-paper', order: 10 },
  { id: 'ideal-gas', slug: 'ideal-gas', name: 'Ideal Gas & Kinetic Theory', nameBn: 'আদর্শ গ্যাস ও গতিতত্ত্ব', subjectId: 'physics', paperId: '1st-paper', order: 11 },

  // Physics 2nd Paper
  { id: 'thermodynamics', slug: 'thermodynamics', name: 'Thermodynamics', nameBn: 'তাপগতিবিদ্যা', subjectId: 'physics', paperId: '2nd-paper', order: 1 },
  { id: 'static-electricity', slug: 'static-electricity', name: 'Static Electricity', nameBn: 'স্থির তড়িৎ', subjectId: 'physics', paperId: '2nd-paper', order: 2 },
  { id: 'current-electricity', slug: 'current-electricity', name: 'Current Electricity', nameBn: 'চল তড়িৎ', subjectId: 'physics', paperId: '2nd-paper', order: 3 },
  { id: 'magnetic-current', slug: 'magnetic-current', name: 'Magnetic Effects of Current & Magnetism', nameBn: 'তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব', subjectId: 'physics', paperId: '2nd-paper', order: 4 },
  { id: 'induction-ac', slug: 'induction-ac', name: 'Electromagnetic Induction & AC', nameBn: 'তড়িচ্চৌম্বক আবেশ ও পর্যায়বৃত্ত প্রবাহ', subjectId: 'physics', paperId: '2nd-paper', order: 5 },
  { id: 'geometric-optics', slug: 'geometric-optics', name: 'Geometric Optics', nameBn: 'জ্যামিতিক আলোকবিজ্ঞান', subjectId: 'physics', paperId: '2nd-paper', order: 6 },
  { id: 'wave-optics', slug: 'wave-optics', name: 'Wave Optics', nameBn: 'ভৌত আলোকবিজ্ঞান', subjectId: 'physics', paperId: '2nd-paper', order: 7 },
  { id: 'modern-physics', slug: 'modern-physics', name: 'Modern Physics', nameBn: 'আধুনিক পদার্থবিজ্ঞানের সূচনা', subjectId: 'physics', paperId: '2nd-paper', order: 8 },
  { id: 'semiconductor', slug: 'semiconductor', name: 'Semiconductor & Electronics', nameBn: 'সেমিকন্ডাক্টর ও ইলেকট্রনিক্স', subjectId: 'physics', paperId: '2nd-paper', order: 10 },
  { id: 'astronomy', slug: 'astronomy', name: 'Astronomy & Astrophysics', nameBn: 'জ্যোতির্বিজ্ঞান', subjectId: 'physics', paperId: '2nd-paper', order: 11 },

  // Chemistry 1st Paper
  { id: 'qualitative-chem', slug: 'qualitative-chem', name: 'Qualitative Chemistry', nameBn: 'গুণগত রসায়ন', subjectId: 'chemistry', paperId: '1st-paper', order: 2 },
  { id: 'chemical-bonding', slug: 'chemical-bonding', name: 'Chemical Bonding & Structure', nameBn: 'পর্যায়বৃত্ত ধর্ম ও রাসায়নিক বন্ধন', subjectId: 'chemistry', paperId: '1st-paper', order: 3 },
  { id: 'chemical-equilibrium', slug: 'chemical-equilibrium', name: 'Chemical Equilibrium & Kinetics', nameBn: 'রাসায়নিক পরিবর্তন ও সাম্যাবস্থা', subjectId: 'chemistry', paperId: '1st-paper', order: 4 },
  { id: 'solid-state-chemistry', slug: 'solid-state-chemistry', name: 'Solid State Chemistry', nameBn: 'কঠিন অবস্থা', subjectId: 'chemistry', paperId: '1st-paper', order: 5 },

  // Chemistry 2nd Paper
  { id: 'environmental-chemistry', slug: 'environmental-chemistry', name: 'Environmental Chemistry', nameBn: 'পরিবেশ রসায়ন', subjectId: 'chemistry', paperId: '2nd-paper', order: 1 },
  { id: 'organic-chem', slug: 'organic-chem', name: 'Organic Chemistry', nameBn: 'জৈব রসায়ন', subjectId: 'chemistry', paperId: '2nd-paper', order: 2 },
  { id: 'quantitative-chem', slug: 'quantitative-chem', name: 'Quantitative Chemistry', nameBn: 'পরিমাণগত রসায়ন', subjectId: 'chemistry', paperId: '2nd-paper', order: 3 },
  { id: 'colligative-properties', slug: 'colligative-properties', name: 'Colligative Properties', nameBn: 'সম্মিল গুণ', subjectId: 'chemistry', paperId: '2nd-paper', order: 4 },
  { id: 'electrochemistry', slug: 'electrochemistry', name: 'Electrochemistry', nameBn: 'তড়িৎ রসায়ন', subjectId: 'chemistry', paperId: '2nd-paper', order: 5 },
  { id: 'coordination-chemistry', slug: 'coordination-chemistry', name: 'Coordination Chemistry', nameBn: 'সমন্বয় রসায়ন', subjectId: 'chemistry', paperId: '2nd-paper', order: 6 },
  { id: 'industrial-chemistry', slug: 'industrial-chemistry', name: 'Industrial Chemistry', nameBn: 'শিল্প রসায়ন', subjectId: 'chemistry', paperId: '2nd-paper', order: 7 },
  { id: 'nuclear-chemistry', slug: 'nuclear-chemistry', name: 'Nuclear Chemistry', nameBn: 'নিউক্লীয় রসায়ন', subjectId: 'chemistry', paperId: '2nd-paper', order: 8 },

  // Higher Math 1st Paper
  { id: 'sets-functions', slug: 'sets-functions', name: 'Sets & Functions', nameBn: 'সেট ও ফাংশন', subjectId: 'math', paperId: '1st-paper', order: 1 },
  { id: 'matrix-determinant', slug: 'matrix-determinant', name: 'Matrices & Determinants', nameBn: 'ম্যাট্রিক্স ও নির্ণায়ক', subjectId: 'math', paperId: '1st-paper', order: 2 },
  { id: 'straight-lines', slug: 'straight-lines', name: 'Straight Lines', nameBn: 'সরলরেখা', subjectId: 'math', paperId: '1st-paper', order: 3 },
  { id: 'circle-geometry', slug: 'circle-geometry', name: 'Circle', nameBn: 'বৃত্ত', subjectId: 'math', paperId: '1st-paper', order: 4 },
  { id: 'sequences-series', slug: 'sequences-series', name: 'Sequences & Series', nameBn: 'অনুক্রম ও ধারা', subjectId: 'math', paperId: '1st-paper', order: 5 },
  { id: 'differentiation', slug: 'differentiation', name: 'Differentiation', nameBn: 'অন্তরীকরণ', subjectId: 'math', paperId: '1st-paper', order: 8 },
  { id: 'integration', slug: 'integration', name: 'Integration', nameBn: 'যোগজীকরণ', subjectId: 'math', paperId: '1st-paper', order: 9 },
  { id: 'calculus', slug: 'calculus', name: 'Calculus Applications', nameBn: 'ক্যালকুলাস প্রয়োগ', subjectId: 'math', paperId: '1st-paper', order: 10 },
  { id: 'math-statics', slug: 'math-statics', name: 'Statics (Math)', nameBn: 'স্থিতিবিদ্যা (গণিত)', subjectId: 'math', paperId: '1st-paper', order: 11 },
  { id: 'math-dynamics', slug: 'math-dynamics', name: 'Dynamics (Math)', nameBn: 'গতিবিদ্যা (গণিত)', subjectId: 'math', paperId: '1st-paper', order: 12 },

  // Higher Math 2nd Paper
  { id: 'complex-numbers', slug: 'complex-numbers', name: 'Complex Numbers', nameBn: 'জটিল সংখ্যা', subjectId: 'math', paperId: '2nd-paper', order: 3 },
  { id: 'polynomials', slug: 'polynomials', name: 'Polynomials & Equations', nameBn: 'বহুপদী ও বহুপদী সমীকরণ', subjectId: 'math', paperId: '2nd-paper', order: 4 },
  { id: 'binomial-theorem', slug: 'binomial-theorem', name: 'Binomial Theorem', nameBn: 'দ্বিপদী উপপাদ্য', subjectId: 'math', paperId: '2nd-paper', order: 5 },
  { id: 'permutation-combination', slug: 'permutation-combination', name: 'Permutations & Combinations', nameBn: 'ক্রমবিন্যাস ও সমাবেশ', subjectId: 'math', paperId: '2nd-paper', order: 6 },
  { id: 'trigonometric-equations', slug: 'trigonometric-equations', name: 'Trigonometric Equations', nameBn: 'ত্রিকোণমিতিক সমীকরণ', subjectId: 'math', paperId: '2nd-paper', order: 7 },
  { id: 'conic-sections', slug: 'conic-sections', name: 'Conic Sections', nameBn: 'কোনিক অংশ', subjectId: 'math', paperId: '2nd-paper', order: 8 },
  { id: 'probability', slug: 'probability', name: 'Probability', nameBn: 'সম্ভাব্যতা', subjectId: 'math', paperId: '2nd-paper', order: 9 },
  { id: 'coordinate-geometry-3d', slug: 'coordinate-geometry-3d', name: '3D Coordinate Geometry', nameBn: 'ত্রিমাত্রিক স্থানাঙ্ক জ্যামিতি', subjectId: 'math', paperId: '2nd-paper', order: 10 },
  { id: 'linear-programming', slug: 'linear-programming', name: 'Linear Programming', nameBn: 'রৈখিক প্রোগ্রামিং', subjectId: 'math', paperId: '2nd-paper', order: 11 },
]

/**
 * Every formula ships as a JSON file under content/subjects/<subject>/chapters/<chapter>/formulas/.
 * Loading them by glob means a new file is live the moment it is added — it can never be
 * silently left out of the book, and per-chapter counts can never drift out of date.
 */
const formulaModules = import.meta.glob<Formula>(
  '../../content/subjects/*/chapters/*/formulas/*.json',
  { eager: true, import: 'default' },
)

export const formulas: Formula[] = Object.values(formulaModules).sort((a, b) => {
  const ao = a.order ?? Number.MAX_SAFE_INTEGER
  const bo = b.order ?? Number.MAX_SAFE_INTEGER
  if (ao !== bo) return ao - bo
  return a.id.localeCompare(b.id)
})

const countByChapter = formulas.reduce<Record<string, number>>((acc, f) => {
  acc[f.chapter] = (acc[f.chapter] ?? 0) + 1
  return acc
}, {})

export const allChapters: ChapterMeta[] = chapterList.map((ch) => ({
  ...ch,
  formulaCount: countByChapter[ch.id] ?? 0,
  isReady: (countByChapter[ch.id] ?? 0) > 0,
}))

const paperOrder: Record<string, number> = { '1st-paper': 0, '2nd-paper': 1 }
const subjectOrder = new Map(subjectsList.map((s, i) => [s.id, i]))

export const chapters: ChapterMeta[] = [...allChapters].sort(
  (a, b) =>
    (subjectOrder.get(a.subjectId) ?? 0) - (subjectOrder.get(b.subjectId) ?? 0) ||
    paperOrder[a.paperId] - paperOrder[b.paperId] ||
    a.order - b.order,
)

export const defaultChapterId = 'magnetic-current'

const tagMap = new Map(tags.map((t) => [t.id, t]))
const chapterMap = new Map(allChapters.map((c) => [c.id, c]))

export function getTag(id: TagId): Tag | undefined {
  return tagMap.get(id)
}

export function getChapter(id: string): ChapterMeta | undefined {
  return chapterMap.get(id)
}

export function getFormula(id: string): Formula | undefined {
  return formulas.find((f) => f.id === id)
}

export function formulasForChapter(chapterId: string = defaultChapterId): Formula[] {
  return formulas.filter((f) => f.chapter === chapterId)
}

/** Compact pack — perPage varies by layout mode */
export function buildPages(items: Formula[], perPage = 7): BookPage[] {
  const pages: BookPage[] = []
  for (let i = 0; i < items.length; i += perPage) {
    pages.push({
      pageNumber: pages.length + 1,
      formulas: items.slice(i, i + perPage),
    })
  }
  return pages
}

export const samplePages = buildPages(formulasForChapter())
