import type { Formula, TagId } from '../data/types'
import { DeriveHint } from './DeriveHint'
import { Katex } from './Katex'
import { QuestionHint } from './QuestionHint'
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
  // Determine grey star importance tag (3-star highest, 2-star, 1-star)
  const imp = formula.importance ?? 2
  const importanceTag: TagId =
    imp === 3 ? '3-star' : imp === 2 ? '2-star' : '1-star'

  // Filter out any older star tags from formula.tags to avoid duplicates
  const examTags = formula.tags.filter((t) => !t.endsWith('-star'))

  // Clean ordered display tags: exam tags first, followed by single grey star tag
  const displayTags: TagId[] = [...examTags, importanceTag]

  return (
    <article
      className="formula"
      style={{ animationDelay: `${30 + index * 30}ms` }}
    >
      <div className="formula-main">
        <div className="formula-latex-col">
          <Katex latex={formula.latex} display />
        </div>

        <div className="formula-text-col">
          <header className="formula-head">
            <h2 className="formula-title">
              <span className="formula-title-bn">{formula.titleBn}</span>
              <span className="formula-title-en">{formula.title}</span>
            </h2>
            <div className="formula-actions">
              <QuestionHint formula={formula} />
              <SymbolHint formula={formula} />
              <DeriveHint formula={formula} />
            </div>
          </header>
          <p className="formula-summary">{formula.summary}</p>
          <div className="formula-meta">
            {displayTags.map((tag) => (
              <TagChip key={tag} id={tag} active={activeTag === tag} />
            ))}
          </div>
        </div>
      </div>
    </article>
  )
}
