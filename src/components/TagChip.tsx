import { Link } from 'react-router-dom'
import { getTag } from '../data/catalog'
import type { TagId } from '../data/types'

interface TagChipProps {
  id: TagId
  active?: boolean
}

export function TagChip({ id, active }: TagChipProps) {
  const tag = getTag(id)
  if (!tag) return null

  return (
    <Link
      to={`/?tag=${tag.id}`}
      className={`tag${active ? ' is-active' : ''}`}
      title={tag.labelBn}
    >
      {tag.label}
    </Link>
  )
}
