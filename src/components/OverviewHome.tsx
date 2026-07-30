import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  allChapters,
  formulas,
  getChapter,
  papers,
  subjectsList,
} from '../data/catalog'
import type { PaperId, SubjectId } from '../data/types'
import { formulaDetailPath } from '../utils/bookLinks'
import { SEARCH_SUGGESTIONS, matchFormula, searchFormulas } from '../utils/search'

interface OverviewHomeProps {
  onSelectChapter: (chapterId: string) => void
  query?: string
  onQueryChange?: (value: string) => void
}

export function OverviewHome({
  onSelectChapter,
  query = '',
  onQueryChange,
}: OverviewHomeProps) {
  const [selectedSubject, setSelectedSubject] = useState<SubjectId | 'all'>('all')
  const [selectedPaper, setSelectedPaper] = useState<PaperId | 'all'>('all')
  const q = query.trim()

  const filteredChapters = allChapters.filter((ch) => {
    if (selectedSubject !== 'all' && ch.subjectId !== selectedSubject) return false
    if (selectedPaper !== 'all' && ch.paperId !== selectedPaper) return false
    if (!q) return true
    const hay = `${ch.name} ${ch.nameBn} ${ch.id}`.toLowerCase()
    if (hay.includes(q.toLowerCase())) return true
    return formulas.some(
      (f) => f.chapter === ch.id && matchFormula(f, query, null),
    )
  })

  const formulaHits = useMemo(() => {
    if (!q) return []
    return searchFormulas(formulas, query, null, 24).map((r) => r.formula)
  }, [q, query])

  const formulaHitTotal = useMemo(() => {
    if (!q) return 0
    return formulas.filter((f) => matchFormula(f, query, null)).length
  }, [q, query])

  return (
    <div className="overview-scroll">
      <div className="overview-container">
      <header className="overview-hero">
        <span className="hero-subhead">FORMULA HUB — HSC & ADMISSION</span>
        <h1 className="hero-title">সকল বিষয়ের অধ্যায়ভিত্তিক সূত্রাবলী</h1>
        <p className="hero-subtitle">
          এইচএসসি বোর্ড এবং বুয়েট, মেডিকেল ও ভার্সিটি ক-ইউনিট ভর্তি পরীক্ষার জন্য প্রস্তুতকৃত ডিজিটাল ফর্মুলা বুক।
        </p>

        <Link
          className="overview-memorize-cta"
          to="/memorize?importance=3"
        >
          মুখস্থ ড্রিল শুরু করো
          <span>৩★ ফ্ল্যাশকার্ড · জানি / আবার</span>
        </Link>

        {onQueryChange ? (
          <label className="overview-search">
            <span aria-hidden="true">⌕</span>
            <input
              value={query}
              onChange={(e) => onQueryChange(e.target.value)}
              placeholder="উদাহরণ: lorentz, কার্নো, YDSE, লিফট…"
              aria-label="সূত্র বা অধ্যায় খুঁজুন"
            />
            {q ? (
              <button
                type="button"
                className="overview-search-clear"
                aria-label="সার্চ মুছুন"
                onClick={() => onQueryChange('')}
              >
                ×
              </button>
            ) : null}
          </label>
        ) : null}

        {onQueryChange && !q ? (
          <div className="overview-suggest-row" aria-label="দ্রুত খোঁজ">
            {SEARCH_SUGGESTIONS.map((s) => (
              <button
                key={s}
                type="button"
                className="overview-suggest-chip"
                onClick={() => onQueryChange(s)}
              >
                {s}
              </button>
            ))}
          </div>
        ) : null}

        <div className="overview-filters">
          <div className="filter-group" role="group" aria-label="বিষয়">
            <button
              type="button"
              className={`filter-tab${selectedSubject === 'all' ? ' is-active' : ''}`}
              aria-pressed={selectedSubject === 'all'}
              onClick={() => setSelectedSubject('all')}
            >
              সব বিষয়
            </button>
            {subjectsList.map((s) => (
              <button
                key={s.id}
                type="button"
                className={`filter-tab${selectedSubject === s.id ? ' is-active' : ''}`}
                aria-pressed={selectedSubject === s.id}
                onClick={() => setSelectedSubject(s.id)}
              >
                {s.nameBn}
              </button>
            ))}
          </div>

          <div className="filter-divider" />

          <div className="filter-group" role="group" aria-label="পত্র">
            <button
              type="button"
              className={`filter-tab${selectedPaper === 'all' ? ' is-active' : ''}`}
              aria-pressed={selectedPaper === 'all'}
              onClick={() => setSelectedPaper('all')}
            >
              সব পত্র
            </button>
            {papers.map((p) => (
              <button
                key={p.id}
                type="button"
                className={`filter-tab${selectedPaper === p.id ? ' is-active' : ''}`}
                aria-pressed={selectedPaper === p.id}
                onClick={() => setSelectedPaper(p.id)}
              >
                {p.nameBn}
              </button>
            ))}
          </div>
        </div>
      </header>

      {q && formulaHits.length > 0 ? (
        <section className="overview-hits" aria-label="সূত্র মিল">
          <h2 className="overview-hits-title">
            সূত্র মিল
            <span>
              {formulaHitTotal > formulaHits.length
                ? ` · প্রথম ${formulaHits.length} / ${formulaHitTotal}`
                : ` · ${formulaHitTotal}`}
            </span>
          </h2>
          <ul className="overview-hits-list">
            {formulaHits.map((f) => {
              const ch = getChapter(f.chapter)
              return (
                <li key={f.id}>
                  <Link
                    to={formulaDetailPath(f.id, {
                      chapter: f.chapter,
                      query: q,
                    })}
                  >
                    <span className="overview-hit-title">{f.titleBn}</span>
                    {ch ? (
                      <span className="overview-hit-chapter">{ch.nameBn}</span>
                    ) : null}
                  </Link>
                </li>
              )
            })}
          </ul>
        </section>
      ) : null}

      <section className="overview-grid">
        {filteredChapters.length === 0 ? (
          <div className="overview-empty">
            <p>{q ? 'এই খোঁজে কোনো অধ্যায় মিলেনি' : 'এই ফিল্টারে কোনো অধ্যায় নেই'}</p>
            <button
              type="button"
              className="filter-tab is-active"
              onClick={() => {
                setSelectedSubject('all')
                setSelectedPaper('all')
                onQueryChange?.('')
              }}
            >
              সব ফিল্টার মুছুন
            </button>
          </div>
        ) : (
          filteredChapters.map((ch) => {
            const subj = subjectsList.find((s) => s.id === ch.subjectId)
            const paper = papers.find((p) => p.id === ch.paperId)

            return (
              <article
                key={ch.id}
                className={`chapter-card${ch.isReady ? ' is-ready' : ' is-locked'}`}
                role={ch.isReady ? 'button' : undefined}
                tabIndex={ch.isReady ? 0 : undefined}
                aria-label={
                  ch.isReady
                    ? `${ch.nameBn} অধ্যায় খুলুন`
                    : `${ch.nameBn} — শীঘ্রই আসছে`
                }
                onClick={() => ch.isReady && onSelectChapter(ch.id)}
                onKeyDown={(e) => {
                  if (!ch.isReady) return
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault()
                    onSelectChapter(ch.id)
                  }
                }}
              >
                <div className="card-top">
                  <span className="card-badge">
                    {subj?.nameBn} · {paper?.nameBn}
                  </span>
                  <span className={`status-pill${ch.isReady ? ' is-live' : ''}`}>
                    {ch.isReady ? `${ch.formulaCount} সূত্র` : 'শীঘ্রই আসছে'}
                  </span>
                </div>

                <h3 className="chapter-title-bn">{ch.nameBn}</h3>
                <p className="chapter-title-en">{ch.name}</p>

                <div className="card-footer">
                  <span className="chapter-order">
                    CHAPTER {String(ch.order).padStart(2, '0')}
                  </span>
                  <span className="open-link">
                    {ch.isReady ? 'বই খুলুন →' : 'প্রস্তুত হচ্ছে'}
                  </span>
                </div>
              </article>
            )
          })
        )}
      </section>
      </div>
    </div>
  )
}
