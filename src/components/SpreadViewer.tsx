import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  buildPages,
  defaultChapterId,
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
  onClearQuery?: () => void
  onClearTag?: () => void
}

const PAGE_ANIM_MS = 450

export function SpreadViewer({
  activeTag,
  query = '',
  chapterId = defaultChapterId,
  onClearQuery,
  onClearTag,
}: SpreadViewerProps) {
  const mode = useLayoutMode()
  const isSpread = mode === 'desktop'
  const chapter = getChapter(chapterId) ?? getChapter(defaultChapterId)!

  // Compact on phones — 3 dense cards; tablet 4; desktop spread 5.
  const perPage = mode === 'desktop' ? 5 : mode === 'tablet' ? 4 : 3

  const { pages, emptyFilter } = useMemo(() => {
    const source = formulasForChapter(chapterId)
    const filtered = source.filter((f) => matchFormula(f, query, activeTag))
    if (!filtered.length) {
      return { pages: [], emptyFilter: true }
    }
    return { pages: buildPages(filtered, perPage), emptyFilter: false }
  }, [activeTag, query, chapterId, perPage])

  const [pageIndex, setPageIndex] = useState(0)
  const [dir, setDir] = useState<'next' | 'prev' | 'none'>('none')
  const [animKey, setAnimKey] = useState(0)
  const animLock = useRef(false)
  const pagerHostRef = useRef<HTMLDivElement>(null)
  const touchStart = useRef<{ x: number; y: number } | null>(null)
  const prevPerPage = useRef(perPage)

  // Reset only when filters/chapter change — not on rotate/breakpoint.
  useEffect(() => {
    setPageIndex(0)
    setDir('none')
    setAnimKey((k) => k + 1)
  }, [activeTag, query, chapterId])

  // When density changes (mobile↔tablet↔desktop), keep approximate place in the book.
  useEffect(() => {
    if (prevPerPage.current === perPage) return
    const oldPer = prevPerPage.current
    prevPerPage.current = perPage
    setPageIndex((i) => {
      const formulaOffset = i * oldPer
      return Math.floor(formulaOffset / perPage)
    })
    setDir('none')
  }, [perPage])

  const maxPage = Math.max(0, pages.length - 1)
  const safePage = Math.min(pageIndex, maxPage)
  const maxSpread = Math.max(0, Math.ceil(pages.length / 2) - 1)
  const safeSpread = Math.min(Math.floor(safePage / 2), maxSpread)
  const left = pages[safeSpread * 2]
  const right = pages[safeSpread * 2 + 1]
  const singleWide = Boolean(left && !right)
  const mobilePage = pages[safePage]

  useEffect(() => {
    if (pageIndex > maxPage) setPageIndex(maxPage)
  }, [pageIndex, maxPage])

  const progress = isSpread
    ? pages.length <= 1
      ? 1
      : (safeSpread + 1) / (maxSpread + 1)
    : pages.length <= 1
      ? 1
      : (safePage + 1) / pages.length

  const goPrev = useCallback(() => {
    if (animLock.current) return
    setPageIndex((i) => {
      if (i <= 0) return i
      const step = isSpread ? 2 : 1
      let next = Math.max(0, i - step)
      if (isSpread) next = next - (next % 2)
      if (next === i) return i
      animLock.current = true
      setDir('prev')
      setAnimKey((k) => k + 1)
      window.setTimeout(() => {
        animLock.current = false
      }, PAGE_ANIM_MS)
      return next
    })
  }, [isSpread])

  const goNext = useCallback(() => {
    if (animLock.current) return
    setPageIndex((i) => {
      const step = isSpread ? 2 : 1
      let next = Math.min(maxPage, i + step)
      if (isSpread) next = next - (next % 2)
      next = Math.min(maxPage, next)
      if (next === i) return i
      animLock.current = true
      setDir('next')
      setAnimKey((k) => k + 1)
      window.setTimeout(() => {
        animLock.current = false
      }, PAGE_ANIM_MS)
      return next
    })
  }, [isSpread, maxPage])

  // Listeners on a stable host so remounting the slide does not kill swipe.
  useEffect(() => {
    if (isSpread) return
    const el = pagerHostRef.current
    if (!el) return

    const skipSwipe = (target: EventTarget | null) => {
      const node = target as HTMLElement | null
      return Boolean(
        node?.closest(
          '.formula-latex-col, .formula-latex, .formula-actions, .hint-wrap, .hint-popover, .overlay-backdrop, .nav-panel, .deck-chrome, .formula-meta, a, input, textarea, button',
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
      if (Math.abs(dx) < 80) return
      if (Math.abs(dy) > 28 && Math.abs(dx) < Math.abs(dy) * 2.2) return
      if (Math.abs(dx) < Math.abs(dy) * 2) return
      if (dx < 0) goNext()
      else goPrev()
    }

    el.addEventListener('touchstart', onTouchStart, { passive: true })
    el.addEventListener('touchend', onTouchEnd, { passive: true })
    return () => {
      el.removeEventListener('touchstart', onTouchStart)
      el.removeEventListener('touchend', onTouchEnd)
    }
  }, [isSpread, goNext, goPrev])

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null
      if (
        target?.closest(
          'input, textarea, select, [contenteditable="true"], [role="dialog"]',
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
          const body = node as HTMLElement
          if (body.scrollHeight > body.clientHeight + 2) return
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

  const atStart = isSpread ? safeSpread <= 0 : safePage <= 0
  const atEnd = isSpread ? safeSpread >= maxSpread : safePage >= maxPage

  if (emptyFilter) {
    const hasQuery = query.trim().length > 0
    const hasTag = Boolean(activeTag)
    const emptyTitle = hasQuery
      ? 'খোঁজে কোনো সূত্র মিলেনি'
      : hasTag
        ? 'এই tag-এ কোনো সূত্র নেই'
        : 'এই অধ্যায়ে সূত্র নেই'
    const emptyHint = hasQuery
      ? 'অন্য কীওয়ার্ড দিয়ে খুঁজুন বা সার্চ খালি করুন'
      : hasTag
        ? 'উপর থেকে All বা অন্য tag বেছে নিন'
        : 'মেনু থেকে অন্য অধ্যায় খুলুন'
    return (
      <div className={`spread-stage mode-${mode}`}>
        <div className="empty-filter">
          <p>{emptyTitle}</p>
          <span>{emptyHint}</span>
          {hasQuery && onClearQuery ? (
            <button
              type="button"
              className="empty-filter-action"
              onClick={onClearQuery}
            >
              সার্চ মুছুন
            </button>
          ) : null}
          {hasTag && !hasQuery && onClearTag ? (
            <button
              type="button"
              className="empty-filter-action"
              onClick={onClearTag}
            >
              সব tag দেখুন
            </button>
          ) : null}
        </div>
      </div>
    )
  }

  return (
    <div className={`spread-stage mode-${mode}`}>
      {isSpread ? (
        <div
          key={`desk-${animKey}`}
          className={`slide-deck ${slideClass}${singleWide ? ' is-single-wide' : ''}`}
          aria-label="Book spread"
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

          <div className="spread">
            {left && (
              <div className={`page-hit is-left${singleWide ? ' is-wide' : ''}`}>
                <A5Page
                  page={left}
                  chapter={chapter}
                  side={singleWide ? 'single' : 'left'}
                  activeTag={activeTag}
                  perPage={perPage}
                />
              </div>
            )}
            {right && (
              <div className="page-hit is-right">
                <A5Page
                  page={right}
                  chapter={chapter}
                  side="right"
                  activeTag={activeTag}
                  perPage={perPage}
                />
              </div>
            )}
          </div>

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
                <span>
                  {right
                    ? `${String(left.pageNumber).padStart(2, '0')}–${String(right.pageNumber).padStart(2, '0')}`
                    : `${String(left.pageNumber).padStart(2, '0')}`}
                </span>
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
      ) : (
        <div
          ref={pagerHostRef}
          className="mobile-pager"
          aria-label="Book page"
        >
          <div key={animKey} className={`mobile-pager-slide ${slideClass}`}>
            {mobilePage && (
              <div className="page-hit is-single">
                <A5Page
                  page={mobilePage}
                  chapter={chapter}
                  side="single"
                  activeTag={activeTag}
                  perPage={perPage}
                  animateFormulas={dir === 'none'}
                />
              </div>
            )}
          </div>
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
      )}
    </div>
  )
}
