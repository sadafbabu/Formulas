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

export interface Formula {
  id: string
  title: string
  titleBn: string
  latex: string
  summary: string
  tags: TagId[]
  chapter: string
  importance?: 1 | 2 | 3 // 1 to 3 grey stars (3 being highest / most important)
  subjects: string[]
  related: string[]
  symbols: SymbolInfo[]
  derivation: Derivation
}

export interface ChapterMeta {
  id: string
  slug: string
  name: string
  nameBn: string
  order: number
}

export interface SubjectMeta {
  id: string
  slug: string
  name: string
  nameBn: string
  order: number
}

export interface BookPage {
  pageNumber: number
  formulas: Formula[]
}
