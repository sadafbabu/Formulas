import { useEffect, useMemo, useRef, useState } from 'react'
import { buildPages, formulas, subject } from '../data/catalog'
import type { TagId } from '../data/types'
import { A5Page } from './A5Page'

interface SpreadViewerProps {
  activeTag?: TagId | null
  query?: string
}

function isInteractive(target: EventTarget | null): boolean {
  if (!(target instanceof Element)) return false
  return Boolean(
    target.closest(
      'a, button, input, textarea, select, label, .derive-hint, .tag, .nav-root',
    ),
  )
}

export function SpreadViewer({ activeTag, query = '' }: SpreadViewerProps) {
  const pages = useMemo(() => {
    const q = query.trim().toLowerCase()
    const filtered = formulas.filter((f) => {
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
    return buildPages(filtered.length ? filtered : formulas)
  }, [activeTag, query])

  const [spreadIndex, setSpreadIndex] = useState(0)
  const [mobileIndex, setMobileIndex] = useState(0)
  const [dir, setDir] = useState<'next' | 'prev' | 'none'>('none')
  const [animKey, setAnimKey] = useState(0)
  const animLock = useRef(false)

  useEffect(() => {
    setSpreadIndex(0)
    setMobileIndex(0)
    setDir('none')
    setAnimKey((k) => k + 1)
  }, [activeTag, query])

  const maxSpread = Math.max(0, Math.ceil(pages.length / 2) - 1)
  const safeSpread = Math.min(spreadIndex, maxSpread)
  const left = pages[safeSpread * 2]
  const right = pages[safeSpread * 2 + 1]
  const singleWide = Boolean(left && !right)

  const safeMobile = Math.min(mobileIndex, pages.length - 1)
  const mobilePage = pages[safeMobile]
  const progress = maxSpread === 0 ? 1 : (safeSpread + 1) / (maxSpread + 1)

  const goPrev = () => {
    if (animLock.current) return
    const canDesk = spreadIndex > 0
    const canMob = mobileIndex > 0
    if (!canDesk && !canMob) return
    animLock.current = true
    setDir('prev')
    setAnimKey((k) => k + 1)
    if (canDesk) setSpreadIndex((i) => i - 1)
    if (canMob) setMobileIndex((i) => i - 1)
    window.setTimeout(() => {
      animLock.current = false
    }, 400)
  }

  const goNext = () => {
    if (animLock.current) return
    const canDesk = spreadIndex < maxSpread
    const canMob = mobileIndex < pages.length - 1
    if (!canDesk && !canMob) return
    animLock.current = true
    setDir('next')
    setAnimKey((k) => k + 1)
    if (canDesk) setSpreadIndex((i) => i + 1)
    if (canMob) setMobileIndex((i) => i + 1)
    window.setTimeout(() => {
      animLock.current = false
    }, 400)
  }

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
  })

  const onPageClick = (
    side: 'left' | 'right' | 'single',
    e: {
      target: EventTarget | null
      currentTarget: EventTarget
      clientX: number
    },
  ) => {
    if (isInteractive(e.target)) return
    if (side === 'left') goPrev()
    else if (side === 'right') goNext()
    else {
      const el = e.currentTarget as HTMLElement
      const rect = el.getBoundingClientRect()
      const x = e.clientX - rect.left
      if (x < rect.width / 2) goPrev()
      else goNext()
    }
  }

  const slideClass =
    dir === 'prev' ? 'is-from-left' : dir === 'next' ? 'is-from-right' : 'is-enter'

  return (
    <div className="spread-stage">
      <div
        key={`desk-${animKey}`}
        className={`slide-deck ${slideClass}${singleWide ? ' is-single-wide' : ''}`}
        aria-label="Presentation slide"
      >
        <div className="spread">
          {left && (
            <div
              className={`page-hit is-left${singleWide ? ' is-wide' : ''}${safeSpread <= 0 ? ' is-edge' : ''}`}
              onClick={(e) =>
                onPageClick(singleWide ? 'single' : 'left', e)
              }
            >
              <A5Page
                page={left}
                subject={subject}
                side={singleWide ? 'single' : 'left'}
                activeTag={activeTag}
                dense={!singleWide}
              />
            </div>
          )}
          {right && (
            <div
              className={`page-hit is-right${safeSpread >= maxSpread ? ' is-edge' : ''}`}
              onClick={(e) => onPageClick('right', e)}
            >
              <A5Page
                page={right}
                subject={subject}
                side="right"
                activeTag={activeTag}
                dense
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
        {mobilePage && (
          <div
            className="page-hit is-single"
            onClick={(e) => onPageClick('single', e)}
          >
            <A5Page
              page={mobilePage}
              subject={subject}
              side="single"
              activeTag={activeTag}
              dense
            />
          </div>
        )}
        <div className="deck-chrome">
          <div className="progress-track" aria-hidden="true">
            <div
              className="progress-fill"
              style={{
                width: `${((safeMobile + 1) / pages.length) * 100}%`,
              }}
            />
          </div>
          <div className="page-indicator" aria-live="polite">
            <span>{safeMobile + 1}</span>
            <span className="page-indicator-sep">/</span>
            <span>{pages.length}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
