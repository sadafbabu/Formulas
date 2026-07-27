import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import {
  buildPages,
  defaultChapterId,
  formulasForChapter,
  getChapter,
} from '../data/catalog'
import type { TagId } from '../data/types'
import { A5Page } from './A5Page'

interface SpreadViewerProps {
  activeTag?: TagId | null
  query?: string
  chapterId?: string
}

function isInteractive(target: EventTarget | null): boolean {
  if (!(target instanceof Element)) return false
  return Boolean(
    target.closest(
      'a, button, input, textarea, select, label, .hint-wrap, .hint-popover, .tag, .nav-root',
    ),
  )
}

export function SpreadViewer({
  activeTag,
  query = '',
  chapterId = defaultChapterId,
}: SpreadViewerProps) {
  const chapter = getChapter(chapterId) ?? getChapter(defaultChapterId)!

  const { pages, emptyFilter } = useMemo(() => {
    const q = query.trim().toLowerCase()
    const source = formulasForChapter(chapterId)
    const filtered = source.filter((f) => {
      const tagOk = !activeTag || f.tags.includes(activeTag)
      if (!tagOk) return false
      if (!q) return true
      return (
        f.title.toLowerCase().includes(q) ||
        f.titleBn.includes(query.trim()) ||
        f.summary.toLowerCase().includes(q) ||
        f.latex.toLowerCase().includes(q)
      )
    })
    const hasFilter = Boolean(activeTag || q)
    if (!filtered.length && hasFilter) {
      return { pages: [], emptyFilter: true }
    }
    return {
      pages: buildPages(filtered.length ? filtered : source),
      emptyFilter: false,
    }
  }, [activeTag, query, chapterId])

  // Unified logical page index (works for both desktop spreads & mobile)
  const [pageIndex, setPageIndex] = useState(0)
  const [dir, setDir] = useState<'next' | 'prev' | 'none'>('none')
  const [animKey, setAnimKey] = useState(0)
  const animLock = useRef(false)

  useEffect(() => {
    setPageIndex(0)
    setDir('none')
    setAnimKey((k) => k + 1)
  }, [activeTag, query, chapterId])

  const maxPage = Math.max(0, pages.length - 1)
  const safePage = Math.min(pageIndex, maxPage)
  const maxSpread = Math.max(0, Math.ceil(pages.length / 2) - 1)
  const safeSpread = Math.min(Math.floor(safePage / 2), maxSpread)
  const left = pages[safeSpread * 2]
  const right = pages[safeSpread * 2 + 1]
  const singleWide = Boolean(left && !right)
  const mobilePage = pages[safePage]
  const progress =
    pages.length <= 1 ? 1 : (safeSpread + 1) / (maxSpread + 1)

  const goPrev = useCallback(() => {
    if (animLock.current) return
    setPageIndex((i) => {
      if (i <= 0) return i
      // desktop: jump by 2 (spread), mobile CSS hides spread — still OK to step 1
      const step = window.matchMedia('(max-width: 820px)').matches ? 1 : 2
      const next = Math.max(0, i - step)
      if (next === i) return i
      animLock.current = true
      setDir('prev')
      setAnimKey((k) => k + 1)
      window.setTimeout(() => {
        animLock.current = false
      }, 360)
      return next
    })
  }, [])

  const goNext = useCallback(() => {
    if (animLock.current) return
    setPageIndex((i) => {
      const step = window.matchMedia('(max-width: 820px)').matches ? 1 : 2
      const next = Math.min(maxPage, i + step)
      // snap to even index on desktop for clean spreads
      const desktop = !window.matchMedia('(max-width: 820px)').matches
      const snapped = desktop ? next - (next % 2) : next
      const target = Math.min(maxPage, snapped)
      if (target === i) return i
      animLock.current = true
      setDir('next')
      setAnimKey((k) => k + 1)
      window.setTimeout(() => {
        animLock.current = false
      }, 360)
      return target
    })
  }, [maxPage])

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
        e.preventDefault()
        goPrev()
      }
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
        e.preventDefault()
        goNext()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [goPrev, goNext])

  const onEdgeClick = (side: 'left' | 'right', e: { target: EventTarget | null }) => {
    if (isInteractive(e.target)) return
    if (side === 'left') goPrev()
    else goNext()
  }

  const slideClass =
    dir === 'prev' ? 'is-from-left' : dir === 'next' ? 'is-from-right' : 'is-enter'

  if (emptyFilter) {
    return (
      <div className="spread-stage">
        <div className="empty-filter">
          <p>কোনো সূত্র মেলেনি</p>
          <span>আর একটা tag/search try করো</span>
        </div>
      </div>
    )
  }

  return (
    <div className="spread-stage">
      <div
        key={`desk-${animKey}`}
        className={`slide-deck ${slideClass}${singleWide ? ' is-single-wide' : ''}`}
        aria-label="Presentation slide"
      >
        {/* Edge hit zones — avoids accidental flips on content */}
        <button
          type="button"
          className="edge-zone is-left"
          aria-label="Previous page"
          disabled={safeSpread <= 0}
          onClick={(e) => onEdgeClick('left', e)}
        />
        <button
          type="button"
          className="edge-zone is-right"
          aria-label="Next page"
          disabled={safeSpread >= maxSpread}
          onClick={(e) => onEdgeClick('right', e)}
        />

        <div className="spread">
          {left && (
            <div className={`page-hit is-left${singleWide ? ' is-wide' : ''}`}>
              <A5Page
                page={left}
                chapter={chapter}
                side={singleWide ? 'single' : 'left'}
                activeTag={activeTag}
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
              />
            </div>
          )}
        </div>

        <div className="deck-chrome">
          <div className="progress-track" aria-hidden="true">
            <div
              className="progress-fill"
              style={{ width: `${progress * 100}%` }}
            />
          </div>
          <div className="page-indicator" aria-live="polite">
            <span>{safeSpread + 1}</span>
            <span className="page-indicator-sep">/</span>
            <span>{maxSpread + 1}</span>
          </div>
        </div>
      </div>

      <div key={`mob-${animKey}`} className={`mobile-pager ${slideClass}`}>
        <button
          type="button"
          className="edge-zone is-left"
          aria-label="Previous page"
          disabled={safePage <= 0}
          onClick={(e) => onEdgeClick('left', e)}
        />
        <button
          type="button"
          className="edge-zone is-right"
          aria-label="Next page"
          disabled={safePage >= maxPage}
          onClick={(e) => onEdgeClick('right', e)}
        />
        {mobilePage && (
          <div className="page-hit is-single">
            <A5Page
              page={mobilePage}
              chapter={chapter}
              side="single"
              activeTag={activeTag}
            />
          </div>
        )}
        <div className="deck-chrome">
          <div className="progress-track" aria-hidden="true">
            <div
              className="progress-fill"
              style={{
                width: `${((safePage + 1) / pages.length) * 100}%`,
              }}
            />
          </div>
          <div className="page-indicator" aria-live="polite">
            <span>{safePage + 1}</span>
            <span className="page-indicator-sep">/</span>
            <span>{pages.length}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
