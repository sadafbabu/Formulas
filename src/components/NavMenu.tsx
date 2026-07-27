import { useEffect, useId, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import {
  chapters,
  defaultChapterId,
  formulasForChapter,
  subject,
  tags,
} from '../data/catalog'
import type { TagId } from '../data/types'

interface NavMenuProps {
  query: string
  onQueryChange: (value: string) => void
  chapterId: string
  onChapterChange: (id: string) => void
}

export function NavMenu({
  query,
  onQueryChange,
  chapterId,
  onChapterChange,
}: NavMenuProps) {
  const [open, setOpen] = useState(false)
  const [params, setParams] = useSearchParams()
  const activeTag = params.get('tag') as TagId | null
  const panelId = useId()
  const rootRef = useRef<HTMLDivElement>(null)
  const list = formulasForChapter(chapterId || defaultChapterId)

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false)
    }
    const onPointer = (e: MouseEvent) => {
      if (!rootRef.current?.contains(e.target as Node)) setOpen(false)
    }
    window.addEventListener('keydown', onKey)
    window.addEventListener('mousedown', onPointer)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.removeEventListener('mousedown', onPointer)
    }
  }, [open])

  return (
    <div className="nav-root" ref={rootRef}>
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
            {subject.nameBn} · {subject.name}
          </p>

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
          {chapters.map((ch) => (
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

          <p className="nav-section">Tags</p>
          <div className="nav-tags">
            <button
              type="button"
              className={`nav-tag${!activeTag ? ' is-active' : ''}`}
              onClick={() => {
                setParams({})
                setOpen(false)
              }}
            >
              All
            </button>
            {tags.map((tag) => (
              <button
                key={tag.id}
                type="button"
                className={`nav-tag${activeTag === tag.id ? ' is-active' : ''}`}
                onClick={() => {
                  setParams({ tag: tag.id })
                  setOpen(false)
                }}
              >
                {tag.label}
              </button>
            ))}
          </div>

          <p className="nav-section">সূত্র ({list.length})</p>
          <ul className="nav-formula-list">
            {list.map((f) => (
              <li key={f.id}>
                <Link to={`/formula/${f.id}`} onClick={() => setOpen(false)}>
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
