import { useState } from 'react'
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { Katex } from '../components/Katex'
import { MathOrText } from '../components/MathOrText'
import { NavMenu } from '../components/NavMenu'
import { TagChip } from '../components/TagChip'
import { defaultChapterId, getChapter, getFormula } from '../data/catalog'
import { bookReturnPath, formulaDetailPath } from '../utils/bookLinks'
import { stripDollarMath, toLatexSymbol } from '../utils/mathText'

export function FormulaDetailPage() {
  const { id } = useParams()
  const formula = id ? getFormula(id) : undefined
  const [query, setQuery] = useState('')
  const [params] = useSearchParams()
  const navigate = useNavigate()
  const chapterId =
    params.get('chapter') || formula?.chapter || defaultChapterId

  const setChapterId = (nextId: string) => {
    navigate(`/?chapter=${encodeURIComponent(nextId)}&view=book`)
  }

  const backTo = bookReturnPath({
    chapter: chapterId,
    tag: params.get('tag'),
    query: params.get('q'),
    page: params.get('page'),
  })

  if (!formula) {
    return (
      <div className="book-shell detail-shell">
        <NavMenu
          floating
          query={query}
          onQueryChange={setQuery}
          chapterId={chapterId}
          onChapterChange={setChapterId}
        />
        <main className="detail-scroll">
          <article className="detail">
            <Link className="detail-back" to={backTo}>
              ← বইয়ে ফিরে যান
            </Link>
            <h1>সূত্র পাওয়া যায়নি</h1>
          </article>
        </main>
      </div>
    )
  }

  const { derivation, symbols } = formula
  const assumptions = (
    Array.isArray(derivation.assumptions) ? derivation.assumptions : []
  )
    .map((item) => stripDollarMath(item).trim())
    .filter(Boolean)
  const steps = Array.isArray(derivation.steps) ? derivation.steps : []
  const questions = (formula.questions ?? []).filter(
    (q) => q.question?.trim() && q.answer?.trim(),
  )
  const related = (formula.related ?? [])
    .map((rid) => getFormula(rid))
    .filter(Boolean)

  return (
    <div className="book-shell detail-shell">
      <NavMenu
        floating
        query={query}
        onQueryChange={setQuery}
        chapterId={chapterId}
        onChapterChange={setChapterId}
      />
      <main className="detail-scroll">
        <article className="detail">
          <Link className="detail-back" to={backTo}>
            ← বইয়ে ফিরে যান
          </Link>

          <h1>{formula.titleBn}</h1>
          <p className="subtitle">{formula.title}</p>

          <div className="formula-meta">
            {formula.tags.map((tag) => (
              <TagChip key={tag} id={tag} chapterId={formula.chapter} />
            ))}
          </div>

          <div className="detail-hero-latex">
            <Katex latex={formula.latex} display />
          </div>

          <MathOrText
            text={derivation.lead}
            as="p"
            className="detail-lead"
          />

          {symbols?.length > 0 && (
            <aside className="assumptions symbol-box">
              <h4>চিহ্ন · একক · মান</h4>
              <div className="symbol-table-wrap">
                <table className="symbol-table detail-symbol-table">
                  <thead>
                    <tr>
                      <th>চিহ্ন</th>
                      <th>অর্থ</th>
                      <th>একক</th>
                      <th>মান</th>
                    </tr>
                  </thead>
                  <tbody>
                    {symbols.map((s) => (
                      <tr key={`${s.symbol}-${s.meaning}`}>
                        <td>
                          <Katex latex={toLatexSymbol(s.symbol)} />
                        </td>
                        <td>{s.meaning}</td>
                        <td>{s.unit}</td>
                        <td>{s.value ?? '—'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </aside>
          )}

          {steps.map((step, i) => (
            <section className="step" key={`${step.title}-${i}`}>
              <span className="step-index">Step {i + 1}</span>
              <h3>{step.title}</h3>
              <div className="formula-latex">
                <Katex latex={step.latex} display />
              </div>
              <MathOrText text={step.note} as="p" />
            </section>
          ))}

          {assumptions.length > 0 && (
            <aside className="assumptions">
              <h4>ধরে নেওয়া</h4>
              <ul>
                {assumptions.map((item) => (
                  <li key={item}>
                    <MathOrText text={item} />
                  </li>
                ))}
              </ul>
            </aside>
          )}

          {formula.memorize?.trick ? (
            <aside className="assumptions detail-memorize">
              <h4>মুখস্থ · মনে রাখার কৌশল</h4>
              <p className="memorize-trick">{formula.memorize.trick}</p>
              {formula.memorize.steps && formula.memorize.steps.length > 0 ? (
                <ol className="memorize-steps">
                  {formula.memorize.steps.map((s, i) => (
                    <li key={`${s}-${i}`}>{s}</li>
                  ))}
                </ol>
              ) : null}
            </aside>
          ) : null}

          {questions.length > 0 && (
            <section className="detail-questions">
              <h4>নমুনা প্রশ্ন ও সমাধান</h4>
              {questions.map((q, i) => (
                <div className="detail-question-card" key={`${q.examType}-${i}`}>
                  <span className="question-exam-tag">{q.examType}</span>
                  <div className="question-problem">
                    <strong>প্রশ্ন:</strong>
                    <MathOrText text={q.question} as="p" className="question-copy" />
                  </div>
                  <div className="question-solution">
                    <strong>সমাধান:</strong>
                    <MathOrText
                      text={q.answer}
                      display
                      as="div"
                      className="question-solution-text"
                    />
                  </div>
                </div>
              ))}
            </section>
          )}

          {related.length > 0 && (
            <aside className="detail-related">
              <h4>সম্পর্কিত সূত্র</h4>
              <ul>
                {related.map((f) => {
                  if (!f) return null
                  const ch = getChapter(f.chapter)
                  return (
                    <li key={f.id}>
                      <Link
                        to={formulaDetailPath(f.id, {
                          chapter: f.chapter,
                          tag: params.get('tag'),
                          query: params.get('q'),
                        })}
                      >
                        {f.titleBn}
                        {ch ? <span>{ch.nameBn}</span> : null}
                      </Link>
                    </li>
                  )
                })}
              </ul>
            </aside>
          )}
        </article>
      </main>
    </div>
  )
}
