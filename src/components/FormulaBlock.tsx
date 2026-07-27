import { Link } from 'react-router-dom'
import type { Formula, TagId } from '../data/types'
import { Katex } from './Katex'
import { TagChip } from './TagChip'

interface FormulaBlockProps {
  formula: Formula
  activeTag?: TagId | null
}

export function FormulaBlock({ formula, activeTag }: FormulaBlockProps) {
  return (
    <article className="formula">
      <div className="formula-title-row">
        <h2 className="formula-title">
          {formula.title}
          <span className="formula-title-bn"> · {formula.titleBn}</span>
        </h2>
      </div>

      <div className="formula-latex">
        <Katex latex={formula.latex} display />
      </div>

      <p className="formula-summary">{formula.summary}</p>

      <div className="formula-meta">
        {formula.tags.map((tag) => (
          <TagChip key={tag} id={tag} active={activeTag === tag} />
        ))}
        <Link className="derive-link" to={`/formula/${formula.id}`}>
          বিস্তারিত →
        </Link>
      </div>
    </article>
  )
}
