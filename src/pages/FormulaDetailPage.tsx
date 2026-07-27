import { useState } from 'react'
import { Link, useParams, useSearchParams } from 'react-router-dom'
import { Katex } from '../components/Katex'
import { NavMenu } from '../components/NavMenu'
import { TagChip } from '../components/TagChip'
import { defaultChapterId, getFormula } from '../data/catalog'

export function FormulaDetailPage() {
  const { id } = useParams()
  const formula = id ? getFormula(id) : undefined
  const [query, setQuery] = useState('')
  const [params, setParams] = useSearchParams()
  const chapterId =
    params.get('chapter') || formula?.chapter || defaultChapterId

  const setChapterId = (nextId: string) => {
    const next = new URLSearchParams(params)
    next.set('chapter', nextId)
    setParams(next, { replace: true })
  }

  const backTo = `/?chapter=${encodeURIComponent(chapterId)}`

  if (!formula) {
    return (
      <div className="book-shell detail-shell">
        <NavMenu
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

  return (
    <div className="book-shell detail-shell">
      <NavMenu
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
              <TagChip key={tag} id={tag} />
            ))}
          </div>

          <div className="detail-hero-latex">
            <Katex latex={formula.latex} display />
          </div>

          <p className="detail-lead">{derivation.lead}</p>

          {symbols?.length > 0 && (
            <aside className="assumptions symbol-box">
              <h4>চিহ্ন · একক · মান</h4>
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
                      <td>{s.symbol}</td>
                      <td>{s.meaning}</td>
                      <td>{s.unit}</td>
                      <td>{s.value ?? '—'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </aside>
          )}

          {derivation.steps.map((step, i) => (
            <section className="step" key={step.title}>
              <span className="step-index">Step {i + 1}</span>
              <h3>{step.title}</h3>
              <div className="formula-latex">
                <Katex latex={step.latex} display />
              </div>
              <p>{step.note}</p>
            </section>
          ))}

          <aside className="assumptions">
            <h4>ধরে নেওয়া</h4>
            <ul>
              {derivation.assumptions.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </aside>
        </article>
      </main>
    </div>
  )
}
