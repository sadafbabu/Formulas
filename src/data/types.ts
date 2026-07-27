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

export interface Formula {
  id: string
  title: string
  titleBn: string
  latex: string
  summary: string
  tags: TagId[]
  subjects: string[]
  related: string[]
  derivation: Derivation
}

export interface SubjectMeta {
  id: string
  slug: string
  name: string
  nameBn: string
  order: number
  chapter: string
}

export interface BookPage {
  pageNumber: number
  formulas: Formula[]
}
