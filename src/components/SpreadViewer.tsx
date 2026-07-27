import { useEffect, useMemo, useState } from 'react'
import { buildPages, formulas, subject } from '../data/catalog'
import type { TagId } from '../data/types'
import { A5Page } from './A5Page'

interface SpreadViewerProps {
  activeTag?: TagId | null
  query?: string
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

  return (
    <div className="spread-stage">
      <div className="spread" aria-label="Book spread">
        {left && (
          <A5Page
            page={left}
            subject={subject}
            side="left"
            activeTag={activeTag}
          />
        )}
        {right && (
          <A5Page
            page={right}
            subject={subject}
            side="right"
            activeTag={activeTag}
          />
        )}
      </div>

      <div className="mobile-pager">
        {mobilePage && (
          <A5Page
            page={mobilePage}
            subject={subject}
            side="single"
            activeTag={activeTag}
          />
        )}
      </div>

      <div className="spread-controls">
        <button
          type="button"
          className="btn-ghost"
          disabled={safeSpread <= 0 && safeMobile <= 0}
          onClick={() => {
            setSpreadIndex((i) => Math.max(0, i - 1))
            setMobileIndex((i) => Math.max(0, i - 1))
          }}
        >
          ← Prev
        </button>
        <span>
          Spread {safeSpread + 1} / {maxSpread + 1}
          <span aria-hidden="true"> · </span>
          Page {safeMobile + 1}/{pages.length}
        </span>
        <button
          type="button"
          className="btn-ghost"
          disabled={
            safeSpread >= maxSpread && safeMobile >= pages.length - 1
          }
          onClick={() => {
            setSpreadIndex((i) => Math.min(maxSpread, i + 1))
            setMobileIndex((i) => Math.min(pages.length - 1, i + 1))
          }}
        >
          Next →
        </button>
      </div>
    </div>
  )
}
