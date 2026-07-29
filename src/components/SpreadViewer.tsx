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
}

export function SpreadViewer({
  activeTag,
  query = '',
  chapterId = defaultChapterId,
}: SpreadViewerProps) {
  const mode = useLayoutMode()
  const isSpread = mode === 'desktop'
  const chapter = getChapter(chapterId) ?? getChapter(defaultChapterId)!

  const perPage = mode === 'desktop' ? 7 : mode === 'tablet' ? 6 : 5

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

  useEffect(() => {
    setPageIndex(0)
    setDir('none')
    setAnimKey((k) => k + 1)
  }, [activeTag, query, chapterId, mode])

  const maxPage = Math.max(0, pages.length - 1)
  const safePage = Math.min(pageIndex, maxPage)
  const maxSpread = Math.max(0, Math.ceil(pages.length / 2) - 1)
  const safeSpread = Math.min(Math.floor(safePage / 2), maxSpread)
  const left = pages[safeSpread * 2]
  const right = pages[safeSpread * 2 + 1]
  const singleWide = Boolean(left && !right)
  const mobilePage = pages[safePage]

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
      }, 320)
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
      }, 320)
      return next
    })
  }, [isSpread, maxPage])

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

  const slideClass =
    dir === 'prev' ? 'is-from-left' : dir === 'next' ? 'is-from-right' : 'is-enter'

  const atStart = isSpread ? safeSpread <= 0 : safePage <= 0
  const atEnd = isSpread ? safeSpread >= maxSpread : safePage >= maxPage

  if (emptyFilter) {
    const hasQuery = query.trim().length > 0
    const message = hasQuery
      ? 'এই খোঁজায় কোনো সূত্র মেলেনি'
      : activeTag
        ? 'এই tag-এ কোনো সূত্র নেই'
        : 'এই অধ্যায়ে কোনো সূত্র নেই'
    const hint = hasQuery
      ? 'অন্য শব্দ দিয়ে খুঁজে দেখো'
      : activeTag
        ? 'উপর থেকে All বা অন্য tag বেছে নাও'
        : 'অন্য অধ্যায় বেছে নাও'
    return (
      <div className={`spread-stage mode-${mode}`}>
        <div className="empty-filter">
          <p>{message}</p>
          <span>{hint}</span>
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
            aria-label="Previous"
            disabled={atStart}
            onClick={goPrev}
          />
          <button
            type="button"
            className="edge-zone is-right"
            aria-label="Next"
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
            <div className="page-indicator" aria-live="polite">
              <span>
                {right
                  ? `${String(left.pageNumber).padStart(2, '0')}–${String(right.pageNumber).padStart(2, '0')}`
                  : `${String(left.pageNumber).padStart(2, '0')}`}
              </span>
              <span className="page-indicator-sep">/</span>
              <span>{String(pages.length).padStart(2, '0')}</span>
            </div>
          </div>
        </div>
      ) : (
        <div
          key={`single-${animKey}`}
          className={`mobile-pager ${slideClass}`}
          aria-label="Book page"
        >
          <button
            type="button"
            className="edge-zone is-left"
            aria-label="Previous"
            disabled={atStart}
            onClick={goPrev}
          />
          <button
            type="button"
            className="edge-zone is-right"
            aria-label="Next"
            disabled={atEnd}
            onClick={goNext}
          />
          {mobilePage && (
            <div className="page-hit is-single">
              <A5Page
                page={mobilePage}
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
            <div className="page-indicator" aria-live="polite">
              <span>{String(safePage + 1).padStart(2, '0')}</span>
              <span className="page-indicator-sep">/</span>
              <span>{String(pages.length).padStart(2, '0')}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
