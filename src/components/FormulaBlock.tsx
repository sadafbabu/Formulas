import type { Formula, TagId } from '../data/types'
import { DeriveHint } from './DeriveHint'
import { Katex } from './Katex'
import { SymbolHint } from './SymbolHint'
import { TagChip } from './TagChip'

interface FormulaBlockProps {
  formula: Formula
  activeTag?: TagId | null
  index?: number
}

export function FormulaBlock({
  formula,
  activeTag,
  index = 0,
}: FormulaBlockProps) {
  return (
    <article
      className="formula"
      style={{ animationDelay: `${30 + index * 30}ms` }}
    >
      <div className="formula-main">
        <div className="formula-latex">
          <Katex latex={formula.latex} display />
        </div>
        <div className="formula-text">
          <header className="formula-head">
            <h2 className="formula-title">
              <span className="formula-title-bn">{formula.titleBn}</span>
              <span className="formula-title-en">{formula.title}</span>
            </h2>
            <div className="formula-actions">
              <SymbolHint formula={formula} />
              <DeriveHint formula={formula} />
            </div>
          </header>
          <p className="formula-summary">{formula.summary}</p>
          <div className="formula-meta">
            {formula.tags.map((tag) => (
              <TagChip key={tag} id={tag} active={activeTag === tag} />
            ))}
          </div>
        </div>
      </div>
    </article>
  )
}
