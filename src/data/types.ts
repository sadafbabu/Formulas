export type TagId =
  | 'hsc'
  | 'eng-admission'
  | 'medical'
  | 'varsity'
  | 'general'
  | 'olympic'

export interface Tag {
  id: TagId
  label: string
  labelBn: string
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
