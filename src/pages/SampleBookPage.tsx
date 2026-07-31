import { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { NavMenu } from '../components/NavMenu'
import { OverviewHome } from '../components/OverviewHome'
import { SpreadViewer } from '../components/SpreadViewer'
import { TopBar } from '../components/TopBar'
import {
  defaultChapterId,
  formulasForChapter,
  getChapter,
  tags,
} from '../data/catalog'
import type { TagId } from '../data/types'
import { matchFormula } from '../utils/search'

const validTagIds = new Set(tags.map((t) => t.id))

export function SampleBookPage() {
  const [params, setParams] = useSearchParams()
  const [menuOpenSignal, setMenuOpenSignal] = useState(0)
  const rawTag = params.get('tag')
  const activeTag =
    rawTag && validTagIds.has(rawTag as TagId) ? (rawTag as TagId) : null
  const rawChapter = params.get('chapter')
  const chapterId =
    rawChapter && getChapter(rawChapter) ? rawChapter : defaultChapterId
  const viewMode: 'home' | 'book' =
    params.get('view') === 'book' ? 'book' : 'home'
  const query = params.get('q') ?? ''
  const pageParam = Math.max(1, Number(params.get('page') || '1') || 1)

  useEffect(() => {
    const next = new URLSearchParams(params)
    let dirty = false
    if (rawTag && !validTagIds.has(rawTag as TagId)) {
      next.delete('tag')
      dirty = true
    }
    if (rawChapter && !getChapter(rawChapter)) {
      next.set('chapter', defaultChapterId)
      dirty = true
    }
    if (dirty) setParams(next, { replace: true })
  }, [params, rawTag, rawChapter, setParams])

  const all = formulasForChapter(chapterId)
  const matchCount = useMemo(() => {
    return all.filter((f) => matchFormula(f, query, activeTag)).length
  }, [all, activeTag, query])

  const setQuery = (value: string, replace = true) => {
    const next = new URLSearchParams(params)
    const trimmed = value.trimStart()
    if (trimmed) next.set('q', trimmed)
    else next.delete('q')
    next.delete('page')
    setParams(next, { replace })
  }

  const setChapterId = (id: string, options?: { clearFilters?: boolean }) => {
    const next = new URLSearchParams(params)
    next.set('chapter', id)
    next.set('view', 'book')
    next.delete('page')
    if (options?.clearFilters) {
      next.delete('tag')
      next.delete('q')
    }
    setParams(next)
  }

  const setTag = (tag: TagId | null) => {
    const next = new URLSearchParams(params)
    if (tag) next.set('tag', tag)
    else next.delete('tag')
    if (!next.get('chapter')) next.set('chapter', chapterId)
    next.set('view', 'book')
    next.delete('page')
    setParams(next)
  }

  const setPage = (page: number) => {
    const next = new URLSearchParams(params)
    if (page <= 1) next.delete('page')
    else next.set('page', String(page))
    setParams(next, { replace: true })
  }

  const handleGoHome = () => {
    const next = new URLSearchParams(params)
    next.set('view', 'home')
    next.delete('tag')
    next.delete('page')
    setParams(next)
  }

  const clearQuery = () => setQuery('', false)
  const clearTag = () => setTag(null)

  return (
    <div className={`book-shell has-topbar${viewMode === 'home' ? ' is-home' : ''}`}>
      <TopBar
        activeTag={activeTag}
        onTagChange={setTag}
        matchCount={matchCount}
        totalCount={all.length}
        viewMode={viewMode}
        onGoHome={handleGoHome}
        query={query}
        onQueryChange={setQuery}
        onOpenMenuSearch={() => setMenuOpenSignal((n) => n + 1)}
        chapterId={chapterId}
        menuSlot={
          <NavMenu
            query={query}
            onQueryChange={setQuery}
            chapterId={chapterId}
            onChapterChange={(id) => setChapterId(id)}
            openSignal={menuOpenSignal}
          />
        }
      />

      {viewMode === 'home' ? (
        <OverviewHome
          query={query}
          onQueryChange={setQuery}
          onSelectChapter={(id) => setChapterId(id, { clearFilters: true })}
        />
      ) : (
        <SpreadViewer
          key={`${chapterId}::${activeTag ?? ''}::${query}`}
          activeTag={activeTag}
          query={query}
          chapterId={chapterId}
          page={pageParam}
          onPageChange={setPage}
          onClearQuery={clearQuery}
          onClearTag={clearTag}
        />
      )}
    </div>
  )
}
