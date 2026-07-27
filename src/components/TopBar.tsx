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
        >
          🏠 ওভারভিউ (Home)
        </button>
        {viewMode === 'book' && menuSlot}
      </div>

      {viewMode === 'book' && (
        <div className="top-bar-tags" role="toolbar" aria-label="Filter by exam tag">
          <button
            type="button"
            className={`top-tag${!activeTag ? ' is-active' : ''}`}
            onClick={() => onTagChange(null)}
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
            >
              {tag.label}
            </button>
          ))}
        </div>
      )}

      {viewMode === 'book' && (
        <div className="top-bar-count" aria-live="polite">
          {activeTag ? `${matchCount}/${totalCount}` : `${totalCount}`}
        </div>
      )}
    </header>
  )
}
