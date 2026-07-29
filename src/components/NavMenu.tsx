import {
  useEffect,
  useId,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
} from 'react'
import { createPortal } from 'react-dom'
import { Link, useSearchParams } from 'react-router-dom'
import {
  chapters,
  defaultChapterId,
  formulas,
  formulasForChapter,
  getChapter,
  subjectsList,
} from '../data/catalog'
import { useFocusTrap } from '../hooks/useFocusTrap'
import { matchFormula } from '../utils/search'
import { readSafeInsets, viewportBox } from '../utils/safeArea'

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
  const fabRef = useRef<HTMLButtonElement>(null)
  const panelRef = useRef<HTMLElement>(null)
  const [pos, setPos] = useState({ top: 56, left: 8 })
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

  const placePanel = () => {
    const btn = rootRef.current
    if (!btn) return
    const r = btn.getBoundingClientRect()
    const safe = readSafeInsets()
    const vp = viewportBox()
    const marginX = Math.max(8, safe.left, safe.right)
    const marginY = Math.max(8, safe.top)
    const marginBottom = Math.max(8, safe.bottom + 8)
    const width = Math.min(320, vp.width - marginX * 2)
    const panelH = panelRef.current?.offsetHeight || 320
    let left = Math.min(
      Math.max(vp.offsetLeft + marginX, r.left),
      vp.offsetLeft + vp.width - width - marginX,
    )
    let top = r.bottom + 8
    if (top + panelH > vp.offsetTop + vp.height - marginBottom) {
      top = Math.max(
        vp.offsetTop + marginY,
        vp.offsetTop + vp.height - panelH - marginBottom,
      )
    }
    setPos({ top, left })
  }

  useLayoutEffect(() => {
    if (!open) return
    placePanel()
    const id = window.requestAnimationFrame(placePanel)
    return () => window.cancelAnimationFrame(id)
  }, [open, query, list.length])

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false)
    }
    const onReposition = () => placePanel()
    const vv = window.visualViewport
    window.addEventListener('keydown', onKey)
    window.addEventListener('resize', onReposition)
    window.addEventListener('scroll', onReposition, true)
    vv?.addEventListener('resize', onReposition)
    vv?.addEventListener('scroll', onReposition)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.removeEventListener('resize', onReposition)
      window.removeEventListener('scroll', onReposition, true)
      vv?.removeEventListener('resize', onReposition)
      vv?.removeEventListener('scroll', onReposition)
    }
  }, [open])

  useFocusTrap(open, panelRef, fabRef)

  const chapter = params.get('chapter') || chapterId
  const activeChapter = getChapter(chapterId || defaultChapterId)
  const activeSubject =
    subjectsList.find((s) => s.id === activeChapter?.subjectId) ?? subjectsList[0]

  const close = () => setOpen(false)

  const panel = open ? (
    <>
      <button
        type="button"
        className="overlay-backdrop"
        aria-label="Close navigation"
        tabIndex={-1}
        onClick={close}
      />
      <nav
        id={panelId}
        ref={panelRef}
        className="nav-panel"
        role="dialog"
        aria-modal="true"
        aria-label="Book navigation"
        style={{ top: pos.top, left: pos.left }}
      >
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
          {q ? (
            <button
              type="button"
              className="nav-search-clear"
              aria-label="Clear search"
              onClick={() => onQueryChange('')}
            >
              ×
            </button>
          ) : null}
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
    </>
  ) : null

  return (
    <div className={`nav-root${floating ? ' is-floating' : ' is-inline'}`} ref={rootRef}>
      <button
        ref={fabRef}
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

      {panel ? createPortal(panel, document.body) : null}
    </div>
  )
}
