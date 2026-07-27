import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { Katex } from '../components/Katex'
import { NavMenu } from '../components/NavMenu'
import { TagChip } from '../components/TagChip'
import { getFormula } from '../data/catalog'

export function FormulaDetailPage() {
  const { id } = useParams()
  const formula = id ? getFormula(id) : undefined
  const [query, setQuery] = useState('')

  if (!formula) {
    return (
      <div className="book-shell detail-shell">
        <NavMenu query={query} onQueryChange={setQuery} />
        <main className="detail-scroll">
          <article className="detail">
            <Link className="detail-back" to="/">
              ← বইয়ে ফিরে যান
            </Link>
            <h1>সূত্র পাওয়া যায়নি</h1>
          </article>
        </main>
      </div>
    )
  }

  const { derivation } = formula

  return (
    <div className="book-shell detail-shell">
      <NavMenu query={query} onQueryChange={setQuery} />
      <main className="detail-scroll">
        <article className="detail">
          <Link className="detail-back" to="/">
            ← বইয়ে ফিরে যান
          </Link>

          <h1>{formula.title}</h1>
          <p className="subtitle">{formula.titleBn}</p>

          <div className="formula-meta">
            {formula.tags.map((tag) => (
              <TagChip key={tag} id={tag} />
            ))}
          </div>

          <div className="detail-hero-latex">
            <Katex latex={formula.latex} display />
          </div>

          <p className="detail-lead">{derivation.lead}</p>

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
