import { useEffect, useRef, type ReactNode } from 'react'
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
  query?: string
  onQueryChange?: (value: string) => void
  onOpenMenuSearch?: () => void
}

export function TopBar({
  activeTag,
  onTagChange,
  matchCount,
  totalCount,
  menuSlot,
  viewMode,
  onGoHome,
  query = '',
  onQueryChange,
  onOpenMenuSearch,
}: TopBarProps) {
  const tagsRef = useRef<HTMLDivElement>(null)
  const searchRef = useRef<HTMLInputElement>(null)

  const examTags = tags.filter((t) => t.category !== 'importance')
  const starTags = tags.filter((t) => t.category === 'importance')

  useEffect(() => {
    if (viewMode !== 'book' || !tagsRef.current) return
    const active = tagsRef.current.querySelector<HTMLElement>('.top-tag.is-active')
    active?.scrollIntoView({
      inline: 'center',
      block: 'nearest',
      behavior: 'smooth',
    })
  }, [activeTag, viewMode])

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null
      if (target?.closest('input, textarea, select, [contenteditable="true"]')) return
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey)) {
        e.preventDefault()
        searchRef.current?.focus()
        onOpenMenuSearch?.()
      }
      if (e.key === '/' && !e.metaKey && !e.ctrlKey && !e.altKey) {
        e.preventDefault()
        searchRef.current?.focus()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onOpenMenuSearch])

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

      {onQueryChange ? (
        <label className="top-bar-search">
          <span className="top-bar-search-icon" aria-hidden="true">
            ⌕
          </span>
          <input
            ref={searchRef}
            value={query}
            onChange={(e) => onQueryChange(e.target.value)}
            placeholder={
              viewMode === 'home' ? 'সূত্র বা অধ্যায় খুঁজুন…' : 'এই বইয়ে সূত্র খুঁজুন…'
            }
            aria-label="সূত্র খুঁজুন"
          />
          {query.trim() ? (
            <button
              type="button"
              className="top-bar-search-clear"
              aria-label="সার্চ মুছুন"
              onClick={() => onQueryChange('')}
            >
              ×
            </button>
          ) : (
            <kbd className="top-bar-search-kbd" title="Keyboard shortcut">
              /
            </kbd>
          )}
        </label>
      ) : null}

      {viewMode === 'book' && (
        <div
          ref={tagsRef}
          className="top-bar-tags"
          role="toolbar"
          aria-label="Filter by exam tag"
        >
          <button
            type="button"
            className={`top-tag${!activeTag ? ' is-active' : ''}`}
            onClick={() => onTagChange(null)}
            aria-pressed={!activeTag}
          >
            All
          </button>
          {examTags.map((tag) => (
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
          <span className="top-tag-sep" aria-hidden="true" />
          {starTags.map((tag) => (
            <button
              key={tag.id}
              type="button"
              className={`top-tag is-star${activeTag === tag.id ? ' is-active' : ''}`}
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
          <span className="top-bar-count-pill">
            {matchCount === totalCount
              ? `${totalCount}`
              : `${matchCount}/${totalCount}`}
          </span>
        </div>
      )}
    </header>
  )
}
