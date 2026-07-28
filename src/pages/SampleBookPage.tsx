import { useMemo, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { NavMenu } from '../components/NavMenu'
import { OverviewHome } from '../components/OverviewHome'
import { SpreadViewer } from '../components/SpreadViewer'
import { TopBar } from '../components/TopBar'
import {
  defaultChapterId,
  formulasForChapter,
} from '../data/catalog'
import type { TagId } from '../data/types'
import { matchFormula } from '../utils/search'

export function SampleBookPage() {
  const [params, setParams] = useSearchParams()
  const activeTag = (params.get('tag') as TagId | null) ?? null
  const chapterId = params.get('chapter') || defaultChapterId
  const viewMode: 'home' | 'book' =
    params.get('view') === 'book' ? 'book' : 'home'
  const [query, setQuery] = useState('')

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
