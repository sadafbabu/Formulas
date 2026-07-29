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
  const rawTag = params.get('tag')
  const activeTag =
    rawTag && validTagIds.has(rawTag as TagId) ? (rawTag as TagId) : null
  const rawChapter = params.get('chapter')
  const chapterId =
    rawChapter && getChapter(rawChapter) ? rawChapter : defaultChapterId
  const viewMode: 'home' | 'book' =
    params.get('view') === 'book' ? 'book' : 'home'
  const [query, setQuery] = useState('')

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

  const setChapterId = (id: string) => {
    const next = new URLSearchParams(params)
    next.set('chapter', id)
    next.set('view', 'book')
    setParams(next, { replace: true })
  }

  const setTag = (tag: TagId | null) => {
    const next = new URLSearchParams(params)
    if (tag) next.set('tag', tag)
    else next.delete('tag')
    if (!next.get('chapter')) next.set('chapter', chapterId)
    next.set('view', 'book')
    setParams(next, { replace: true })
  }

  const handleGoHome = () => {
    const next = new URLSearchParams(params)
    next.set('view', 'home')
    setParams(next, { replace: true })
  }

  return (
    <div className="book-shell has-topbar">
      <TopBar
        activeTag={activeTag}
        onTagChange={setTag}
        matchCount={matchCount}
        totalCount={all.length}
        viewMode={viewMode}
        onGoHome={handleGoHome}
        menuSlot={
          <NavMenu
            query={query}
            onQueryChange={setQuery}
            chapterId={chapterId}
            onChapterChange={setChapterId}
          />
        }
      />

      {viewMode === 'home' ? (
        <OverviewHome onSelectChapter={setChapterId} />
      ) : (
        <SpreadViewer
          activeTag={activeTag}
          query={query}
          chapterId={chapterId}
        />
      )}
    </div>
  )
}
