import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  buildPages,
  defaultChapterId,
  formulas,
  formulasForChapter,
  getChapter,
} from '../data/catalog'
import type { TagId } from '../data/types'
import { useLayoutMode } from '../hooks/useLayoutMode'
import { matchFormula } from '../utils/search'
import { A5Page } from './A5Page'

interface SpreadViewerProps {
  activeTag?: TagId | null
  query?: string
  chapterId?: string
  page?: number
  onPageChange?: (page: number) => void
  onClearQuery?: () => void
  onClearTag?: () => void
}

export function SpreadViewer({
  activeTag,
  query = '',
  chapterId = defaultChapterId,
  page = 1,
  onPageChange,
  onClearQuery,
  onClearTag,
}: SpreadViewerProps) {
  const mode = useLayoutMode()
  const chapter = getChapter(chapterId) ?? getChapter(defaultChapterId)!

  // One page at a time on every viewport — full width so latex stays readable.
  const perPage = mode === 'desktop' ? 5 : mode === 'tablet' ? 4 : 3

  const { pages, emptyFilter } = useMemo(() => {
    const source = formulasForChapter(chapterId)
    const filtered = source.filter((f) => matchFormula(f, query, activeTag))
    if (!filtered.length) {
      return { pages: [], emptyFilter: true }
    }
    return { pages: buildPages(filtered, perPage), emptyFilter: false }
  }, [activeTag, query, chapterId, perPage])

  const globalMatchCount = useMemo(() => {
    if (!query.trim()) return 0
    return formulas.filter((f) => matchFormula(f, query, null)).length
  }, [query])

  const [pageIndex, setPageIndex] = useState(0)
  const [dir, setDir] = useState<'next' | 'prev' | 'none'>('none')
  const [animKey, setAnimKey] = useState(0)
  const animLock = useRef(false)
  const pagerRef = useRef<HTMLDivElement>(null)
  const touchStart = useRef<{ x: number; y: number } | null>(null)

  useEffect(() => {
    setPageIndex(0)
    setDir('none')
    setAnimKey((k) => k + 1)
  }, [activeTag, query, chapterId, mode])

  useEffect(() => {
    if (emptyFilter || !pages.length) return
    const desired = Math.min(Math.max(0, page - 1), pages.length - 1)
    setPageIndex((current) => (current === desired ? current : desired))
  }, [page, pages.length, emptyFilter])

  const maxPage = Math.max(0, pages.length - 1)
  const safePage = Math.min(pageIndex, maxPage)
  const currentPage = pages[safePage]

  useEffect(() => {
    if (!onPageChange || emptyFilter) return
    const oneBased = safePage + 1
    if (oneBased === page) return
    onPageChange(oneBased)
  }, [safePage, page, onPageChange, emptyFilter])

  const progress = pages.length <= 1 ? 1 : (safePage + 1) / pages.length

  const goPrev = useCallback(() => {
    if (animLock.current) return
    setPageIndex((i) => {
      if (i <= 0) return i
      const next = i - 1
      animLock.current = true
      setDir('prev')
      setAnimKey((k) => k + 1)
      window.setTimeout(() => {
        animLock.current = false
      }, 320)
      return next
    })
  }, [])

  const goNext = useCallback(() => {
    if (animLock.current) return
    setPageIndex((i) => {
      if (i >= maxPage) return i
      const next = i + 1
      animLock.current = true
      setDir('next')
      setAnimKey((k) => k + 1)
      window.setTimeout(() => {
        animLock.current = false
      }, 320)
      return next
    })
  }, [maxPage])

  useEffect(() => {
    const el = pagerRef.current
    if (!el) return

    const skipSwipe = (target: EventTarget | null) => {
      const node = target as HTMLElement | null
      return Boolean(
        node?.closest(
          'a, button, .formula-latex-col, .formula-latex, .nav-panel, .hint-popover, input, textarea, [role="dialog"], [role="button"]',
        ),
      )
    }

    const onTouchStart = (e: TouchEvent) => {
      if (skipSwipe(e.target)) {
        touchStart.current = null
        return
      }
      const t = e.touches[0]
      touchStart.current = { x: t.clientX, y: t.clientY }
    }

    const onTouchEnd = (e: TouchEvent) => {
      if (!touchStart.current) return
      const t = e.changedTouches[0]
      const dx = t.clientX - touchStart.current.x
      const dy = t.clientY - touchStart.current.y
      touchStart.current = null
      if (Math.abs(dx) < 56 || Math.abs(dx) < Math.abs(dy) * 1.35) return
      if (dx < 0) goNext()
      else goPrev()
    }

    const onTouchCancel = () => {
      touchStart.current = null
    }

    el.addEventListener('touchstart', onTouchStart, { passive: true })
    el.addEventListener('touchend', onTouchEnd, { passive: true })
    el.addEventListener('touchcancel', onTouchCancel, { passive: true })
    return () => {
      el.removeEventListener('touchstart', onTouchStart)
      el.removeEventListener('touchend', onTouchEnd)
      el.removeEventListener('touchcancel', onTouchCancel)
    }
  }, [goNext, goPrev])

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null
      if (
        target?.closest(
          'input, textarea, select, button, a, [contenteditable="true"], [role="dialog"], [role="button"], [role="menuitem"]',
        )
      ) {
        return
      }
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault()
        goPrev()
      }
      if (e.key === 'ArrowRight' || e.key === 'PageDown') {
        e.preventDefault()
        goNext()
      }
      if (e.key === ' ' || e.key === 'Spacebar') {
        const bodies = document.querySelectorAll('.spread-stage .page-body')
        for (const node of bodies) {
          const el = node as HTMLElement
          if (el.scrollHeight > el.clientHeight + 2) {
            const remaining = el.scrollHeight - el.scrollTop - el.clientHeight
            if (remaining > 4) return
          }
        }
        e.preventDefault()
        goNext()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [goPrev, goNext])

  const slideClass =
    dir === 'prev' ? 'is-from-left' : dir === 'next' ? 'is-from-right' : 'is-enter'

  const atStart = safePage <= 0
  const atEnd = safePage >= maxPage

  if (emptyFilter) {
    const hasQuery = query.trim().length > 0
    const hasTag = Boolean(activeTag)
    const emptyTitle = hasQuery
      ? 'এই অধ্যায়ে খোঁজে কোনো সূত্র মিলেনি'
      : hasTag
        ? 'এই tag-এ কোনো সূত্র নেই'
        : 'এই অধ্যায়ে সূত্র নেই'
    const emptyHint = hasQuery
      ? globalMatchCount > 0
        ? `অন্য অধ্যায়ে ${globalMatchCount} মিল আছে — মেনু থেকে খুলুন, বা সার্চ মুছুন`
        : 'অন্য কীওয়ার্ড দিয়ে খুঁজুন বা সার্চ খালি করুন'
      : hasTag
        ? 'উপর থেকে All বা অন্য tag বেছে নিন'
        : 'মেনু থেকে অন্য অধ্যায় খুলুন'
    return (
      <div className={`spread-stage mode-${mode}`}>
        <div className="empty-filter">
          <p>{emptyTitle}</p>
          <span>{emptyHint}</span>
          <div className="empty-filter-actions">
            {hasQuery && onClearQuery ? (
              <button type="button" className="empty-action" onClick={onClearQuery}>
                সার্চ মুছুন
              </button>
            ) : null}
            {hasTag && onClearTag ? (
              <button type="button" className="empty-action" onClick={onClearTag}>
                Tag মুছুন
              </button>
            ) : null}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className={`spread-stage mode-${mode}`}>
      <div
        key={`page-${animKey}`}
        ref={pagerRef}
        className={`single-pager ${slideClass}`}
        aria-label="Book page"
      >
        <button
          type="button"
          className="edge-zone is-left"
          aria-label="Previous edge"
          disabled={atStart}
          onClick={goPrev}
        />
        <button
          type="button"
          className="edge-zone is-right"
          aria-label="Next edge"
          disabled={atEnd}
          onClick={goNext}
        />

        {currentPage && (
          <div className="page-hit is-single">
            <A5Page
              page={currentPage}
              chapter={chapter}
              side="single"
              activeTag={activeTag}
              perPage={perPage}
            />
          </div>
        )}

        <div className="deck-chrome">
          <div className="progress-track" aria-hidden="true">
            <div className="progress-fill" style={{ width: `${progress * 100}%` }} />
          </div>
          <div className="page-nav-row">
            <button
              type="button"
              className="page-turn"
              aria-label="Previous page"
              disabled={atStart}
              onClick={goPrev}
            >
              ‹
            </button>
            <div className="page-indicator" aria-live="polite">
              <span>{String(safePage + 1).padStart(2, '0')}</span>
              <span className="page-indicator-sep">/</span>
              <span>{String(pages.length).padStart(2, '0')}</span>
            </div>
            <button
              type="button"
              className="page-turn"
              aria-label="Next page"
              disabled={atEnd}
              onClick={goNext}
            >
              ›
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
