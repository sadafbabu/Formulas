import { useEffect, useId, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import {
  allChapters,
  defaultChapterId,
  formulasForChapter,
  getChapter,
  subjectsList,
} from '../data/catalog'

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
  const activeChapterId = chapterId || defaultChapterId
  const list = formulasForChapter(activeChapterId)
  const activeChapter = getChapter(activeChapterId)
  const activeSubject = subjectsList.find(
    (s) => s.id === activeChapter?.subjectId,
  )

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false)
    }
    const onPointer = (e: MouseEvent | TouchEvent) => {
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

  const chapter = params.get('chapter')

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
          {activeSubject && (
            <p className="nav-subject-line">
              {activeSubject.nameBn} · {activeSubject.name}
            </p>
          )}

          <label className="nav-search">
            <span aria-hidden="true">⌕</span>
            <input
              value={query}
              onChange={(e) => onQueryChange(e.target.value)}
              placeholder="সূত্র খুঁজুন…"
              autoFocus
            />
          </label>

          <p className="nav-section">অধ্যায়</p>
          {allChapters.map((ch) => (
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
              <span>{ch.name}</span>
            </button>
          ))}

          <p className="nav-section">সূত্র ({list.length})</p>
          <ul className="nav-formula-list">
            {list.map((f) => (
              <li key={f.id}>
                <Link
                  to={`/formula/${f.id}${chapter ? `?chapter=${chapter}` : ''}`}
                  onClick={() => setOpen(false)}
                >
                  {f.titleBn}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  )
}
