import type { BookPage, ChapterMeta, TagId } from '../data/types'
import { FormulaBlock } from './FormulaBlock'

interface A5PageProps {
  page: BookPage
  chapter: ChapterMeta
  side?: 'left' | 'right' | 'single'
  activeTag?: TagId | null
  /** Expected formulas per full page — sparse pages pack to the top */
  perPage?: number
}

export function A5Page({
  page,
  chapter,
  side = 'single',
  activeTag,
  perPage = 7,
}: A5PageProps) {
  const sideClass =
    side === 'left' ? 'is-left' : side === 'right' ? 'is-right' : 'is-single'
  const sparse = page.formulas.length < perPage

  return (
    <section
      className={`a5-page ${sideClass}${sparse ? ' is-sparse' : ''}`}
      aria-label={`পৃষ্ঠা ${page.pageNumber}`}
    >
      <header className="page-header">
        <div className="page-header-main">
          <span className="page-chapter">{chapter.nameBn}</span>
          <span className="page-subject">{chapter.name}</span>
        </div>
        <span className="page-num-badge">
          {String(page.pageNumber).padStart(2, '0')}
        </span>
      </header>

      <div className="page-body">
        {page.formulas.map((formula, i) => (
          <FormulaBlock
            key={formula.id}
            formula={formula}
            activeTag={activeTag}
            index={i}
          />
        ))}
      </div>
    </section>
  )
}
