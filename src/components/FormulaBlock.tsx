import type { Formula, TagId } from '../data/types'
import { DeriveHint } from './DeriveHint'
import { Katex } from './Katex'
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
      style={{ animationDelay: `${80 + index * 70}ms` }}
    >
      <div className="formula-title-row">
        <h2 className="formula-title">
          {formula.title}
          <span className="formula-title-bn">{formula.titleBn}</span>
        </h2>
        <DeriveHint formula={formula} />
      </div>

      <div className="formula-latex">
        <Katex latex={formula.latex} display />
      </div>

      <p className="formula-summary">{formula.summary}</p>

      <div className="formula-meta">
        {formula.tags.map((tag) => (
          <TagChip key={tag} id={tag} active={activeTag === tag} />
        ))}
      </div>
    </article>
  )
}
