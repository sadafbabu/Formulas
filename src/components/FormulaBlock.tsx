import { Link, useSearchParams } from 'react-router-dom'
import type { Formula, TagId } from '../data/types'
import { DeriveHint } from './DeriveHint'
import { Katex } from './Katex'
import { MemorizeHint } from './MemorizeHint'
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
  const [params] = useSearchParams()
  const chapter = params.get('chapter') || formula.chapter
  const detailTo = `/formula/${formula.id}?chapter=${encodeURIComponent(chapter)}`

  // Determine grey star importance tag (3-star highest, 2-star, 1-star)
  const imp = formula.importance ?? 2
  const importanceTag: TagId =
    imp === 3 ? '3-star' : imp === 2 ? '2-star' : '1-star'

  // Filter out any older star tags from formula.tags to avoid duplicates
  const examTags = formula.tags.filter((t) => !t.endsWith('-star'))

  // Exam tags first (cap at 2 for compact rows), then grey star importance.
  const displayTags: TagId[] = [...examTags.slice(0, 2), importanceTag]

  return (
    <article
      className="formula"
      style={{ animationDelay: `${20 + index * 20}ms` }}
    >
      <div className="formula-main">
        <div className="formula-latex-col">
          <Link to={detailTo} className="formula-latex-link" title="বিস্তারিত দেখুন">
            <div className="formula-latex">
              <Katex latex={formula.latex} display />
            </div>
          </Link>
        </div>

        <div className="formula-text-col">
          <header className="formula-head">
            <h2 className="formula-title">
              <Link to={detailTo} className="formula-title-link">
                <span className="formula-title-bn">{formula.titleBn}</span>
                <span className="formula-title-en">{formula.title}</span>
              </Link>
            </h2>
            <div className="formula-actions">
              <QuestionHint formula={formula} />
              <SymbolHint formula={formula} />
              <DeriveHint formula={formula} />
              <MemorizeHint formula={formula} />
            </div>
          </header>
          <p className="formula-summary">{formula.summary}</p>
          <div className="formula-meta">
            {displayTags.map((tag) => (
              <TagChip
                key={tag}
                id={tag}
                active={activeTag === tag}
                chapterId={formula.chapter}
              />
            ))}
          </div>
        </div>
      </div>
    </article>
  )
}
