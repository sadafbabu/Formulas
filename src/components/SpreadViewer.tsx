import { useEffect, useMemo, useState } from 'react'
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

  useEffect(() => {
    setSpreadIndex(0)
    setMobileIndex(0)
  }, [activeTag, query])

  const maxSpread = Math.max(0, Math.ceil(pages.length / 2) - 1)
  const safeSpread = Math.min(spreadIndex, maxSpread)
  const left = pages[safeSpread * 2]
  const right = pages[safeSpread * 2 + 1]

  const safeMobile = Math.min(mobileIndex, pages.length - 1)
  const mobilePage = pages[safeMobile]

  const goPrev = () => {
    setSpreadIndex((i) => Math.max(0, i - 1))
    setMobileIndex((i) => Math.max(0, i - 1))
  }

  const goNext = () => {
    setSpreadIndex((i) => Math.min(maxSpread, i + 1))
    setMobileIndex((i) => Math.min(pages.length - 1, i + 1))
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
    e: { target: EventTarget | null; currentTarget: EventTarget; clientX: number },
  ) => {
    if (isInteractive(e.target)) return
    if (side === 'left') goPrev()
    else if (side === 'right') goNext()
    else {
      // mobile: left half prev, right half next
      const el = e.currentTarget as HTMLElement
      const rect = el.getBoundingClientRect()
      const x = e.clientX - rect.left
      if (x < rect.width / 2) goPrev()
      else goNext()
    }
  }

  return (
    <div className="spread-stage">
      <div className="spread" aria-label="Book spread">
        {left && (
          <div
            className={`page-hit is-left${safeSpread <= 0 ? ' is-edge' : ''}`}
            onClick={(e) => onPageClick('left', e)}
          >
            <A5Page
              page={left}
              subject={subject}
              side="left"
              activeTag={activeTag}
            />
          </div>
        )}
        {right ? (
          <div
            className={`page-hit is-right${safeSpread >= maxSpread ? ' is-edge' : ''}`}
            onClick={(e) => onPageClick('right', e)}
          >
            <A5Page
              page={right}
              subject={subject}
              side="right"
              activeTag={activeTag}
            />
          </div>
        ) : (
          <div className="page-hit is-right is-blank" aria-hidden="true" />
        )}
      </div>

      <div className="mobile-pager">
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
            />
          </div>
        )}
      </div>

      <div className="page-indicator" aria-live="polite">
        {safeSpread + 1}/{maxSpread + 1}
      </div>
    </div>
  )
}
