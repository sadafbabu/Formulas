import { Link, useSearchParams } from 'react-router-dom'
import { getTag } from '../data/catalog'
import type { TagId } from '../data/types'

interface TagChipProps {
  id: TagId
  active?: boolean
  /** Prefer this chapter when filtering from a formula context */
  chapterId?: string
}

export function TagChip({ id, active, chapterId }: TagChipProps) {
  const tag = getTag(id)
  const [params] = useSearchParams()
  if (!tag) return null

  const next = new URLSearchParams(params)
  next.set('tag', tag.id)
  next.set('view', 'book')
  // Always start a tag filter on page 1 (don't keep a stale book page).
  next.delete('page')
  const chapter = chapterId || params.get('chapter')
  if (chapter) next.set('chapter', chapter)

  return (
    <Link
      to={`/?${next.toString()}`}
      className={`tag${active ? ' is-active' : ''}`}
      title={`${tag.labelBn} — শুধু এই ট্যাগ`}
      onClick={(e) => e.stopPropagation()}
    >
      {tag.label}
    </Link>
  )
}
