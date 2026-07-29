import type { ReactNode } from 'react'
import { tags } from '../data/catalog'
import type { TagId } from '../data/types'

interface TopBarProps {
  activeTag: TagId | null
  onTagChange: (tag: TagId | null) => void
  matchCount: number
  totalCount: number
  menuSlot: ReactNode
  viewMode: 'home' | 'book'
  onGoHome: () => void
}

export function TopBar({
  activeTag,
  onTagChange,
  matchCount,
  totalCount,
  menuSlot,
  viewMode,
  onGoHome,
}: TopBarProps) {
  return (
    <header className="top-bar">
      <div className="top-bar-left">
        <button
          type="button"
          className={`home-nav-btn${viewMode === 'home' ? ' is-active' : ''}`}
          onClick={onGoHome}
          title="সকল বিষয় ও অধ্যায়ের ওভারভিউ ড্যাশবোর্ড"
          aria-label="ওভারভিউতে ফিরে যান"
          aria-current={viewMode === 'home' ? 'page' : undefined}
        >
          <svg
            className="home-icon"
            viewBox="0 0 24 24"
            width="15"
            height="15"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
            <polyline points="9 22 9 12 15 12 15 22" />
          </svg>
          <span>ওভারভিউ</span>
        </button>
        {menuSlot}
      </div>

      {viewMode === 'book' && (
        <div className="top-bar-tags" role="toolbar" aria-label="Filter by exam tag">
          <button
            type="button"
            className={`top-tag${!activeTag ? ' is-active' : ''}`}
            onClick={() => onTagChange(null)}
            aria-pressed={!activeTag}
          >
            All
          </button>
          {tags.map((tag) => (
            <button
              key={tag.id}
              type="button"
              className={`top-tag${activeTag === tag.id ? ' is-active' : ''}`}
              onClick={() => onTagChange(tag.id)}
              title={tag.labelBn}
              aria-pressed={activeTag === tag.id}
            >
              {tag.label}
            </button>
          ))}
        </div>
      )}

      {viewMode === 'book' && (
        <div className="top-bar-count" aria-live="polite">
          {matchCount === totalCount ? `${totalCount}` : `${matchCount}/${totalCount}`}
        </div>
      )}
    </header>
  )
}
