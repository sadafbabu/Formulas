export type TagId =
  | 'hsc'
  | 'eng-admission'
  | 'medical'
  | 'varsity'
  | 'general'
  | 'olympic'
  | '3-star'
  | '2-star'
  | '1-star'

export interface Tag {
  id: TagId
  label: string
  labelBn: string
  category?: 'exam' | 'importance' | 'chapter'
}

export interface DerivationStep {
  title: string
  latex: string
  note: string
}

export interface Derivation {
  lead: string
  steps: DerivationStep[]
  assumptions: string[]
}

/** Symbol legend: meaning, unit, optional constant/value */
export interface SymbolInfo {
  symbol: string
  meaning: string
  unit: string
  value?: string
}

export interface QuestionItem {
  examType: string
  question: string
  answer: string
}

/** Memorization aid: a mnemonic/trick plus optional ordered steps to recall the formula */
export interface MemorizeItem {
  trick: string
  steps?: string[]
}

export type PaperId = '1st-paper' | '2nd-paper'
export type SubjectId = 'physics' | 'chemistry' | 'math'

export interface Formula {
  id: string
  title: string
  titleBn: string
  latex: string
  summary: string
  tags: TagId[]
  chapter: string
  paper?: PaperId
  importance?: 1 | 2 | 3 // 1 to 3 grey stars (3 being highest / most important)
  subjects: string[]
  related: string[]
  symbols: SymbolInfo[]
  derivation: Derivation
  questions?: QuestionItem[]
  memorize?: MemorizeItem
}

export interface ChapterMeta {
  id: string
  slug: string
  name: string
  nameBn: string
  subjectId: SubjectId
  paperId: PaperId
  order: number
  formulaCount?: number
  isReady?: boolean
}

export interface SubjectMeta {
  id: SubjectId
  slug: string
  name: string
  nameBn: string
  icon: string
  color: string
  order: number
}

export interface PaperMeta {
  id: PaperId
  name: string
  nameBn: string
}

export interface BookPage {
  pageNumber: number
  formulas: Formula[]
}
