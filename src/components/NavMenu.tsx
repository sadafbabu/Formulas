import { useEffect, useId, useMemo, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import {
  chapters,
  defaultChapterId,
  formulas,
  formulasForChapter,
  getChapter,
  subjectsList,
} from '../data/catalog'
import { matchFormula } from '../utils/search'

interface NavMenuProps {
  query: string
  onQueryChange: (value: string) => void
  chapterId: string
  onChapterChange: (id: string) => void
  /** When false, only render the fab+panel (menu lives inside TopBar) */
  floating?: boolean
}

export function NavMenu({
  query,
  onQueryChange,
  chapterId,
  onChapterChange,
  floating = false,
}: NavMenuProps) {
  const [open, setOpen] = useState(false)
  const [params] = useSearchParams()
  const panelId = useId()
  const rootRef = useRef<HTMLDivElement>(null)
  const isCoarsePointer =
    typeof window !== 'undefined' &&
    window.matchMedia('(pointer: coarse)').matches
  const q = query.trim()

  const chapterList = useMemo(() => {
    return formulasForChapter(chapterId || defaultChapterId).filter((f) =>
      matchFormula(f, query, null),
    )
  }, [chapterId, query])

  const globalList = useMemo(() => {
    if (!q) return []
    return formulas.filter((f) => matchFormula(f, query, null)).slice(0, 40)
  }, [q, query])

  const chaptersBySubject = useMemo(() => {
    return subjectsList.map((subject) => ({
      subject,
      chapters: chapters.filter((ch) => ch.subjectId === subject.id),
    }))
  }, [])

  const list = q ? (globalList.length ? globalList : chapterList) : chapterList
  const searchingAll = Boolean(q && globalList.length > 0)

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false)
    }
    const onPointer = (e: Event) => {
      if (!rootRef.current?.contains(e.target as Node)) setOpen(false)
    }
    window.addEventListener('keydown', onKey)
    window.addEventListener('mousedown', onPointer)
    window.addEventListener('touchstart', onPointer)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.removeEventListener('mousedown', onPointer)
      window.removeEventListener('touchstart', onPointer)
    }
  }, [open])

  const chapter = params.get('chapter') || chapterId
  const activeChapter = getChapter(chapterId || defaultChapterId)
  const activeSubject =
    subjectsList.find((s) => s.id === activeChapter?.subjectId) ?? subjectsList[0]

  return (
    <div className={`nav-root${floating ? ' is-floating' : ' is-inline'}`} ref={rootRef}>
      <button
        type="button"
        className="nav-fab"
        aria-label="Open navigation"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen((v) => !v)}
      >
        <span className="nav-fab-bars" aria-hidden="true">
          <i />
          <i />
          <i />
        </span>
      </button>

      {open && (
        <nav id={panelId} className="nav-panel" aria-label="Book navigation">
          <div className="nav-brand">Formulas</div>
          <p className="nav-subject-line">
            {activeSubject.nameBn} · {activeSubject.name}
          </p>

          <label className="nav-search">
            <span aria-hidden="true">⌕</span>
            <input
              value={query}
              onChange={(e) => onQueryChange(e.target.value)}
              placeholder="সূত্র খুঁজুন…"
              aria-label="সূত্র খুঁজুন"
              autoFocus={!isCoarsePointer}
            />
          </label>

          {chaptersBySubject.map(({ subject, chapters: subjectChapters }) => (
            <div key={subject.id} className="nav-subject-group">
              <p className="nav-section">
                {subject.nameBn}
                <span className="nav-section-en"> · {subject.name}</span>
              </p>
              {subjectChapters.map((ch) => (
                <button
                  key={ch.id}
                  type="button"
                  className={`nav-link${chapterId === ch.id ? ' is-active' : ''}`}
                  onClick={() => {
                    onChapterChange(ch.id)
                    setOpen(false)
                  }}
                >
                  {ch.nameBn}
                  <span>{ch.formulaCount}</span>
                </button>
              ))}
            </div>
          ))}

          <p className="nav-section">
            {searchingAll ? 'সব অধ্যায়ে মিল' : 'সূত্র'} ({list.length}
            {q ? ' মিল' : ''})
          </p>
          <ul className="nav-formula-list">
            {list.length === 0 ? (
              <li className="nav-empty">কোনো সূত্র মিলেনি</li>
            ) : (
              list.map((f) => {
                const chMeta = getChapter(f.chapter)
                return (
                  <li key={f.id}>
                    <Link
                      to={`/formula/${f.id}?chapter=${encodeURIComponent(f.chapter || chapter)}`}
                      onClick={() => setOpen(false)}
                    >
                      {f.titleBn}
                      {searchingAll && chMeta ? (
                        <span className="nav-formula-chapter">{chMeta.nameBn}</span>
                      ) : null}
                    </Link>
                  </li>
                )
              })
            )}
          </ul>
        </nav>
      )}
    </div>
  )
}
