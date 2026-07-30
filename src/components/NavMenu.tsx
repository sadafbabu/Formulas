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
import { formulaDetailPath, memorizePath } from '../utils/bookLinks'
import {
  SEARCH_SUGGESTIONS,
  matchFormula,
  searchFormulas,
} from '../utils/search'

interface NavMenuProps {
  query: string
  onQueryChange: (value: string) => void
  chapterId: string
  onChapterChange: (id: string) => void
  floating?: boolean
  openSignal?: number
}

const RESULT_LIMIT = 50

export function NavMenu({
  query,
  onQueryChange,
  chapterId,
  onChapterChange,
  floating = false,
  openSignal = 0,
}: NavMenuProps) {
  const [open, setOpen] = useState(false)
  const [draftQuery, setDraftQuery] = useState(query)
  const [params] = useSearchParams()
  const panelId = useId()
  const rootRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const isCoarsePointer =
    typeof window !== 'undefined' &&
    window.matchMedia('(pointer: coarse)').matches
  const q = query.trim()

  useEffect(() => {
    setDraftQuery(query)
  }, [query])

  useEffect(() => {
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current)
    }
  }, [])

  const commitQuery = (value: string, immediate = false) => {
    setDraftQuery(value)
    if (debounceRef.current) clearTimeout(debounceRef.current)
    if (immediate || !value.trim()) {
      onQueryChange(value)
      return
    }
    debounceRef.current = setTimeout(() => onQueryChange(value), 160)
  }

  useEffect(() => {
    if (openSignal > 0) {
      setOpen(true)
      window.setTimeout(() => inputRef.current?.focus(), 30)
    }
  }, [openSignal])

  const chapterList = useMemo(() => {
    return formulasForChapter(chapterId || defaultChapterId).filter((f) =>
      matchFormula(f, query, null),
    )
  }, [chapterId, query])

  const rankedGlobal = useMemo(() => {
    if (!q) return []
    return searchFormulas(formulas, query, null, RESULT_LIMIT)
  }, [q, query])

  const globalMatchTotal = useMemo(() => {
    if (!q) return 0
    return formulas.filter((f) => matchFormula(f, query, null)).length
  }, [q, query])

  const chaptersBySubject = useMemo(() => {
    return subjectsList.map((subject) => ({
      subject,
      chapters: chapters.filter((ch) => ch.subjectId === subject.id),
    }))
  }, [])

  const filteredChapterNav = useMemo(() => {
    if (!q) return chaptersBySubject
    const nq = q.toLowerCase()
    return chaptersBySubject
      .map(({ subject, chapters: subjectChapters }) => ({
        subject,
        chapters: subjectChapters.filter((ch) => {
          const hay = `${ch.name} ${ch.nameBn} ${ch.id}`.toLowerCase()
          if (hay.includes(nq)) return true
          return formulas.some(
            (f) => f.chapter === ch.id && matchFormula(f, query, null),
          )
        }),
      }))
      .filter((g) => g.chapters.length > 0)
  }, [chaptersBySubject, q, query])

  const searchingAll = Boolean(q && rankedGlobal.length > 0)
  const list = q
    ? rankedGlobal.map((r) => r.formula)
    : chapterList
  const resultLabel = (() => {
    if (!q) return `এই অধ্যায়ের সূত্র (${list.length})`
    if (searchingAll) {
      if (globalMatchTotal > RESULT_LIMIT) {
        return `সেরা মিল (প্রথম ${RESULT_LIMIT} / ${globalMatchTotal})`
      }
      return `সেরা মিল (${globalMatchTotal})`
    }
    return `কোনো সূত্র মিলেনি`
  })()

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

  const activeChapter = getChapter(chapterId || defaultChapterId)
  const activeSubject =
    subjectsList.find((s) => s.id === activeChapter?.subjectId) ?? subjectsList[0]

  return (
    <div className={`nav-root${floating ? ' is-floating' : ' is-inline'}`} ref={rootRef}>
      <button
        type="button"
        className={`nav-fab${open ? ' is-open' : ''}`}
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
          <div className="nav-panel-head">
            <div>
              <div className="nav-brand">Formulas</div>
              <p className="nav-subject-line">
                {activeSubject.nameBn} · {activeChapter?.nameBn ?? activeSubject.name}
              </p>
            </div>
            <button
              type="button"
              className="nav-panel-close"
              aria-label="মেনু বন্ধ"
              onClick={() => setOpen(false)}
            >
              ×
            </button>
          </div>

          <label className="nav-search">
            <span aria-hidden="true">⌕</span>
            <input
              ref={inputRef}
              value={draftQuery}
              onChange={(e) => commitQuery(e.target.value)}
              onBlur={() => commitQuery(draftQuery, true)}
              placeholder="নাম, চিহ্ন, অধ্যায়, Banglish…"
              aria-label="সূত্র খুঁজুন"
              autoFocus={!isCoarsePointer}
              enterKeyHint="search"
              autoComplete="off"
              autoCorrect="off"
              spellCheck={false}
            />
            {draftQuery.trim() ? (
              <button
                type="button"
                className="nav-search-clear"
                aria-label="সার্চ মুছুন"
                onClick={() => {
                  commitQuery('', true)
                  inputRef.current?.focus()
                }}
              >
                ×
              </button>
            ) : null}
          </label>

          {!q ? (
            <div className="nav-suggest">
              <Link
                className="nav-memorize-link"
                to={memorizePath({
                  chapter: chapterId,
                  tag: params.get('tag'),
                  importance: 3,
                })}
                onClick={() => setOpen(false)}
              >
                মুখস্থ ড্রিল
                <span>৩★ ফ্ল্যাশকার্ড</span>
              </Link>
              <span className="nav-suggest-label">দ্রুত খোঁজ</span>
              <div className="nav-suggest-row">
                {SEARCH_SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    type="button"
                    className="nav-suggest-chip"
                    onClick={() => commitQuery(s, true)}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : null}

          {filteredChapterNav.map(({ subject, chapters: subjectChapters }) => (
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

          <p className="nav-section">{resultLabel}</p>
          <ul className="nav-formula-list">
            {list.length === 0 ? (
              <li className="nav-empty">
                কোনো সূত্র মিলেনি — অন্য কীওয়ার্ড বা Banglish চেষ্টা করুন
              </li>
            ) : (
              list.map((f) => {
                const chMeta = getChapter(f.chapter)
                return (
                  <li key={f.id}>
                    <Link
                      to={formulaDetailPath(f.id, {
                        chapter: f.chapter || chapterId,
                        tag: params.get('tag'),
                        query: q || null,
                        page: params.get('page'),
                      })}
                      onClick={() => setOpen(false)}
                    >
                      <span className="nav-formula-title">{f.titleBn}</span>
                      <span className="nav-formula-sub">
                        {f.title}
                        {searchingAll && chMeta ? ` · ${chMeta.nameBn}` : ''}
                      </span>
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
