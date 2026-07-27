import { useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { NavMenu } from '../components/NavMenu'
import { SpreadViewer } from '../components/SpreadViewer'
import type { TagId } from '../data/types'

export function SampleBookPage() {
  const [params] = useSearchParams()
  const activeTag = (params.get('tag') as TagId | null) ?? null
  const [query, setQuery] = useState('')

  return (
    <div className="book-shell">
      <NavMenu query={query} onQueryChange={setQuery} />
      <SpreadViewer activeTag={activeTag} query={query} />
    </div>
  )
}
