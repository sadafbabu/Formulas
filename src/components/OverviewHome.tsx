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
      {/* Hero Header */}
      <header className="overview-hero">
        <div className="hero-badge">HSC & Admission Formula Hub</div>
        <h1 className="hero-title">
          পদার্থবিজ্ঞান, রসায়ন ও উচ্চতর গণিত <br />
          <span className="hero-highlight">১ম ও ২য় পত্রের অধ্যায়ভিত্তিক অল সূত্রাবলী</span>
        </h1>
        <p className="hero-subtitle">
          এইচএসসি বোর্ড পরীক্ষা ও বুয়েট/মেডিকেল/ভার্সিটি ক-ইউনিট ভর্তি পরীক্ষার জন্য ১০০% সিলেবাসভিত্তিক পূর্ণাঙ্গ সূত্রের ডিজিটাল হ্যান্ডবুক।
        </p>

        {/* Filter Controls */}
        <div className="overview-filters">
          <div className="filter-group">
            <span className="filter-label">বিষয় (Subject):</span>
            <button
              type="button"
              className={`filter-tab${selectedSubject === 'all' ? ' is-active' : ''}`}
              onClick={() => setSelectedSubject('all')}
            >
              সব বিষয়
            </button>
            {subjectsList.map((s) => (
              <button
                key={s.id}
                type="button"
                className={`filter-tab${selectedSubject === s.id ? ' is-active' : ''}`}
                onClick={() => setSelectedSubject(s.id)}
              >
                {s.icon} {s.nameBn}
              </button>
            ))}
          </div>

          <div className="filter-group">
            <span className="filter-label">পত্র (Paper):</span>
            <button
              type="button"
              className={`filter-tab${selectedPaper === 'all' ? ' is-active' : ''}`}
              onClick={() => setSelectedPaper('all')}
            >
              উভয় পত্র
            </button>
            {papers.map((p) => (
              <button
                key={p.id}
                type="button"
                className={`filter-tab${selectedPaper === p.id ? ' is-active' : ''}`}
                onClick={() => setSelectedPaper(p.id)}
              >
                {p.nameBn}
              </button>
            ))}
          </div>
        </div>
      </header>

      {/* Chapters Grid */}
      <section className="overview-grid">
        {filteredChapters.map((ch) => {
          const subj = subjectsList.find((s) => s.id === ch.subjectId)
          const paper = papers.find((p) => p.id === ch.paperId)

          return (
            <article
              key={ch.id}
              className={`chapter-card${ch.isReady ? ' is-ready' : ' is-locked'}`}
              onClick={() => ch.isReady && onSelectChapter(ch.id)}
            >
              <div className="card-top">
                <span className="card-badge" style={{ borderColor: subj?.color }}>
                  {subj?.icon} {subj?.nameBn} — {paper?.nameBn}
                </span>
                <span className={`status-pill${ch.isReady ? ' is-live' : ''}`}>
                  {ch.isReady ? `⚡ ${ch.formulaCount}টি সূত্র Ready` : 'শীঘ্রই আসছে'}
                </span>
              </div>

              <h3 className="chapter-title-bn">{ch.nameBn}</h3>
              <p className="chapter-title-en">{ch.name}</p>

              <div className="card-footer">
                <span className="chapter-order">অধ্যায় ০{ch.order}</span>
                <button
                  type="button"
                  className="open-btn"
                  disabled={!ch.isReady}
                >
                  {ch.isReady ? '📖 সূত্র দেখুন' : 'প্রস্তুত হচ্ছে'}
                </button>
              </div>
            </article>
          )
        })}
      </section>
    </div>
  )
}
