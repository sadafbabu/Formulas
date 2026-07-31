/** Preserve book context when jumping to a formula detail page. */
export function formulaDetailPath(
  formulaId: string,
  opts: {
    chapter: string
    tag?: string | null
    query?: string | null
    page?: string | number | null
  },
): string {
  const p = new URLSearchParams()
  p.set('chapter', opts.chapter)
  if (opts.tag) p.set('tag', opts.tag)
  const q = opts.query?.trim()
  if (q) p.set('q', q)
  if (opts.page != null && opts.page !== '' && Number(opts.page) > 1) {
    p.set('page', String(opts.page))
  }
  return `/formula/${formulaId}?${p.toString()}`
}

/** Build the book URL to return to from a detail page. */
export function bookReturnPath(opts: {
  chapter: string
  tag?: string | null
  query?: string | null
  page?: string | number | null
}): string {
  const p = new URLSearchParams()
  p.set('chapter', opts.chapter)
  p.set('view', 'book')
  if (opts.tag) p.set('tag', opts.tag)
  const q = opts.query?.trim()
  if (q) p.set('q', q)
  if (opts.page != null && opts.page !== '' && Number(opts.page) > 1) {
    p.set('page', String(opts.page))
  }
  return `/?${p.toString()}`
}

/**
 * Memorize drill URL.
 * Star tags (`1-star`/`2-star`/`3-star`) map to `importance`, not `tag`.
 * Pass `importance: null` explicitly for “all levels” (omit param) —
 * this wins even when `tag` is a star.
 * Omit `importance` to default to 3★ on first entry (or the star tag’s level).
 * Pass `startId` to pin that formula to the front of the drill queue.
 */
export function memorizePath(opts: {
  chapter?: string | null
  tag?: string | null
  importance?: 1 | 2 | 3 | null
  unknownOnly?: boolean
  startId?: string | null
}): string {
  const p = new URLSearchParams()
  if (opts.chapter) p.set('chapter', opts.chapter)

  const tag = opts.tag
  const isStar = tag === '1-star' || tag === '2-star' || tag === '3-star'

  if (opts.importance === null) {
    // all levels — leave importance unset (even if tag was a star)
  } else if (opts.importance != null) {
    p.set('importance', String(opts.importance))
  } else if (isStar) {
    p.set('importance', tag[0])
  } else {
    p.set('importance', '3')
  }

  if (tag && !isStar) p.set('tag', tag)

  if (opts.unknownOnly) p.set('unknown', '1')
  if (opts.startId) p.set('start', opts.startId)
  const qs = p.toString()
  return qs ? `/memorize?${qs}` : '/memorize'
}
