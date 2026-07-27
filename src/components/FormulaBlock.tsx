import type { Formula, TagId } from '../data/types'
import { DeriveHint } from './DeriveHint'
import { Katex } from './Katex'
import { TagChip } from './TagChip'

interface FormulaBlockProps {
  formula: Formula
  activeTag?: TagId | null
  index?: number
  hero?: boolean
}

export function FormulaBlock({
  formula,
  activeTag,
  index = 0,
  hero = false,
}: FormulaBlockProps) {
  return (
    <article
      className={`formula${hero ? ' is-hero' : ''}`}
      style={{ animationDelay: `${50 + index * 50}ms` }}
    >
      <header className="formula-head">
        <h2 className="formula-title">
          <span className="formula-title-en">{formula.title}</span>
          <span className="formula-title-bn">{formula.titleBn}</span>
        </h2>
        <DeriveHint formula={formula} />
      </header>

      <div className="formula-latex">
        <Katex latex={formula.latex} display />
      </div>

      <footer className="formula-foot">
        <p className="formula-summary">{formula.summary}</p>
        <div className="formula-meta">
          {formula.tags.map((tag) => (
            <TagChip key={tag} id={tag} active={activeTag === tag} />
          ))}
        </div>
      </footer>
    </article>
  )
}
