import { useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { SpreadViewer } from '../components/SpreadViewer'
import { formulas, tags } from '../data/catalog'
import type { TagId } from '../data/types'

export function SampleBookPage() {
  const [params, setParams] = useSearchParams()
  const activeTag = (params.get('tag') as TagId | null) ?? null
  const [query, setQuery] = useState('')

  const matchCount = useMemo(() => {
    const q = query.trim().toLowerCase()
    return formulas.filter((f) => {
      const tagOk = !activeTag || f.tags.includes(activeTag)
      if (!tagOk) return false
      if (!q) return true
      return (
        f.title.toLowerCase().includes(q) ||
        f.titleBn.includes(q) ||
        f.summary.toLowerCase().includes(q)
      )
    }).length
  }, [activeTag, query])

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          Formulas<span>.</span>
        </div>

        <label className="search">
          <span aria-hidden="true">⌕</span>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="সূত্র খুঁজুন…"
            aria-label="Search formulas"
          />
        </label>

        <div className="topbar-meta">
          <span>
            {activeTag
              ? tags.find((t) => t.id === activeTag)?.label
              : 'All tags'}
            {query ? ` · ${matchCount} hits` : ''}
          </span>
          {activeTag && (
            <button
              type="button"
              className="btn-ghost"
              onClick={() => setParams({})}
            >
              Clear tag
            </button>
          )}
        </div>
      </header>

      <main className="main">
        <p className="sample-note">
          এটি <strong>average template page</strong> — বাকি সব page এই
          কাঠামোতেই যাবে: A5 spread (PC) / এক page (mobile), ট্যাগ, আর{' '}
          <strong>বিস্তারিত →</strong> derivation link। Black theme।
        </p>

        <SpreadViewer activeTag={activeTag} query={query} />
      </main>
    </div>
  )
}
