import type { BookPage, SubjectMeta, TagId } from '../data/types'
import { FormulaBlock } from './FormulaBlock'

interface A5PageProps {
  page: BookPage
  subject: SubjectMeta
  side?: 'left' | 'right' | 'single'
  activeTag?: TagId | null
}

export function A5Page({ page, subject, side = 'single', activeTag }: A5PageProps) {
  const sideClass =
    side === 'left' ? 'is-left' : side === 'right' ? 'is-right' : ''

  return (
    <section className={`a5-page ${sideClass}`} aria-label={`Page ${page.pageNumber}`}>
      <header className="page-header">
        <span className="page-chapter">{subject.chapter}</span>
        <span className="page-subject">
          {subject.nameBn} · {subject.name}
        </span>
      </header>

      <div className="page-body">
        {page.formulas.map((formula) => (
          <FormulaBlock
            key={formula.id}
            formula={formula}
            activeTag={activeTag}
          />
        ))}
      </div>

      <footer className="page-footer">
        <span>Formulas</span>
        <span>{page.pageNumber}</span>
      </footer>
    </section>
  )
}
