import type { CSSProperties } from 'react'
import type { BookPage, SubjectMeta, TagId } from '../data/types'
import { FormulaBlock } from './FormulaBlock'

interface A5PageProps {
  page: BookPage
  subject: SubjectMeta
  side?: 'left' | 'right' | 'single'
  activeTag?: TagId | null
  dense?: boolean
}

export function A5Page({
  page,
  subject,
  side = 'single',
  activeTag,
  dense = true,
}: A5PageProps) {
  const sideClass =
    side === 'left' ? 'is-left' : side === 'right' ? 'is-right' : 'is-single'
  const count = page.formulas.length

  return (
    <section
      className={`a5-page ${sideClass}${dense ? ' is-dense' : ' is-hero'}`}
      aria-label={`Page ${page.pageNumber}`}
      style={{ '--formula-count': count } as CSSProperties}
    >
      <header className="page-header">
        <div className="page-header-main">
          <span className="page-chapter">{subject.chapter}</span>
          <span className="page-subject">
            {subject.nameBn} · {subject.name}
          </span>
        </div>
        <span className="page-num-badge">
          {String(page.pageNumber).padStart(2, '0')}
        </span>
      </header>

      <div className={`page-body count-${count}`}>
        {page.formulas.map((formula, i) => (
          <FormulaBlock
            key={formula.id}
            formula={formula}
            activeTag={activeTag}
            index={i}
            hero={count === 1}
          />
        ))}
      </div>

      <footer className="page-footer">
        <span className="page-brand">Formulas</span>
        <span className="page-hint">
          {side === 'left' ? '← prev' : side === 'right' ? 'next →' : 'tap sides'}
        </span>
      </footer>
    </section>
  )
}
