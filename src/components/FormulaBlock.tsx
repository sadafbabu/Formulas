import { Link, useSearchParams } from 'react-router-dom'
import type { Formula, TagId } from '../data/types'
import { formulaDetailPath } from '../utils/bookLinks'
import { DeriveHint } from './DeriveHint'
import { Katex } from './Katex'
import { MathOrText } from './MathOrText'
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
  const detailTo = formulaDetailPath(formula.id, {
    chapter,
    tag: params.get('tag'),
    query: params.get('q'),
    page: params.get('page'),
  })

  const imp = formula.importance ?? 2
  const importanceTag: TagId =
    imp === 3 ? '3-star' : imp === 2 ? '2-star' : '1-star'

  const examTags = formula.tags.filter((t) => !t.endsWith('-star'))
  const displayTags: TagId[] = [...examTags, importanceTag]

  return (
    <article
      className="formula"
      style={{ animationDelay: `${30 + index * 30}ms` }}
    >
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

      <Link
        to={detailTo}
        className="formula-latex-link"
        title="বিস্তারিত দেখুন"
        onClick={(e) => {
          // Avoid accidental navigation while selecting / inspecting KaTeX.
          if (window.getSelection()?.toString()) {
            e.preventDefault()
          }
        }}
      >
        <div className="formula-latex-col">
          <div className="formula-latex">
            <Katex latex={formula.latex} display />
          </div>
        </div>
      </Link>

      <div className="formula-foot">
        <MathOrText
          text={formula.summary}
          as="p"
          className="formula-summary"
        />
        <div className="formula-meta">
          {displayTags.map((tag) => (
            <TagChip key={tag} id={tag} active={activeTag === tag} chapterId={formula.chapter} />
          ))}
        </div>
      </div>
    </article>
  )
}
