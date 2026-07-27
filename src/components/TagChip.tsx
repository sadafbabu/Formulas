import { Link, useSearchParams } from 'react-router-dom'
import { getTag } from '../data/catalog'
import type { TagId } from '../data/types'

interface TagChipProps {
  id: TagId
  active?: boolean
}

export function TagChip({ id, active }: TagChipProps) {
  const tag = getTag(id)
  const [params] = useSearchParams()
  if (!tag) return null

  const next = new URLSearchParams()
  const chapter = params.get('chapter')
  if (chapter) next.set('chapter', chapter)
  next.set('tag', tag.id)

  return (
    <Link
      to={`/?${next.toString()}`}
      className={`tag${active ? ' is-active' : ''}`}
      title={tag.labelBn}
      onClick={(e) => e.stopPropagation()}
    >
      {tag.label}
    </Link>
  )
}
