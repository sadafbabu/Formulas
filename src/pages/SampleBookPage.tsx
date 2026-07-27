import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { NavMenu } from '../components/NavMenu'
import { SpreadViewer } from '../components/SpreadViewer'
import { defaultChapterId } from '../data/catalog'
import type { TagId } from '../data/types'

export function SampleBookPage() {
  const [params] = useSearchParams()
  const activeTag = (params.get('tag') as TagId | null) ?? null
  const [query, setQuery] = useState('')
  const [chapterId, setChapterId] = useState(defaultChapterId)

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
