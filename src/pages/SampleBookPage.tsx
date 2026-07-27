import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { NavMenu } from '../components/NavMenu'
import { SpreadViewer } from '../components/SpreadViewer'
import { defaultChapterId } from '../data/catalog'
import type { TagId } from '../data/types'

export function SampleBookPage() {
  const [params, setParams] = useSearchParams()
  const activeTag = (params.get('tag') as TagId | null) ?? null
  const chapterId = params.get('chapter') || defaultChapterId
  const [query, setQuery] = useState('')

  const setChapterId = (id: string) => {
    const next = new URLSearchParams(params)
    next.set('chapter', id)
    setParams(next, { replace: true })
  }

  return (
    <div className="book-shell">
      <NavMenu
        query={query}
        onQueryChange={setQuery}
        chapterId={chapterId}
        onChapterChange={setChapterId}
      />
      <SpreadViewer
        activeTag={activeTag}
        query={query}
        chapterId={chapterId}
      />
    </div>
  )
}
