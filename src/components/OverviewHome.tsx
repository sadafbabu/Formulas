import { useState } from 'react'
import { allChapters, papers, subjectsList } from '../data/catalog'
import type { PaperId, SubjectId } from '../data/types'

interface OverviewHomeProps {
  onSelectChapter: (chapterId: string) => void
}

export function OverviewHome({ onSelectChapter }: OverviewHomeProps) {
  const [selectedSubject, setSelectedSubject] = useState<SubjectId | 'all'>('all')
  const [selectedPaper, setSelectedPaper] = useState<PaperId | 'all'>('all')

  const filteredChapters = allChapters.filter((ch) => {
    if (selectedSubject !== 'all' && ch.subjectId !== selectedSubject) return false
    if (selectedPaper !== 'all' && ch.paperId !== selectedPaper) return false
    return true
  })

  return (
    <div className="overview-container">
      {/* Hero Header - Strict Monochrome Minimalist */}
      <header className="overview-hero">
        <span className="hero-subhead">FORMULA HUB — HSC & ADMISSION</span>
        <h1 className="hero-title">সকল বিষয়ের অধ্যায়ভিত্তিক সূত্রাবলী</h1>
        <p className="hero-subtitle">
          এইচএসসি বোর্ড এবং বুয়েট, মেডিকেল ও ভার্সিটি ক-ইউনিট ভর্তি পরীক্ষার জন্য প্রস্তুতকৃত ডিজিটাল ফর্মুলা বুক।
        </p>

        {/* Minimalist Filter Bar */}
        <div className="overview-filters">
          <div className="filter-group">
            {subjectsList.map((s) => (
              <button
                key={s.id}
                type="button"
                className={`filter-tab${selectedSubject === s.id ? ' is-active' : ''}`}
                onClick={() => setSelectedSubject(selectedSubject === s.id ? 'all' : s.id)}
              >
                {s.nameBn}
              </button>
            ))}
          </div>

          <div className="filter-divider" />

          <div className="filter-group">
            {papers.map((p) => (
              <button
                key={p.id}
                type="button"
                className={`filter-tab${selectedPaper === p.id ? ' is-active' : ''}`}
                onClick={() => setSelectedPaper(selectedPaper === p.id ? 'all' : p.id)}
              >
                {p.nameBn}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Minimalist Chapters Grid */}
      <section className="overview-grid">
        {filteredChapters.length === 0 ? (
          <div className="overview-empty">
            <p>এই ফিল্টারে কোনো অধ্যায় নেই</p>
            <button
              type="button"
              className="filter-tab is-active"
              onClick={() => {
                setSelectedSubject('all')
                setSelectedPaper('all')
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
  )
}
