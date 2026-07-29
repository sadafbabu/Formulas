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

  const next = new URLSearchParams(params)
  next.set('tag', tag.id)
  next.set('view', 'book')
  if (!next.get('chapter')) {
    // keep existing chapter if any; book view still needs one from SampleBookPage default
  }

  return (
    <Link
      to={`/?${next.toString()}`}
      className={`tag${active ? ' is-active' : ''}`}
      title={`${tag.labelBn} — শুধু এই tag`}
      onClick={(e) => e.stopPropagation()}
    >
      {tag.label}
    </Link>
  )
}
