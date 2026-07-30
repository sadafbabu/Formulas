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

/** Memorize drill session URL with optional chapter/tag/importance filters. */
export function memorizePath(opts: {
  chapter?: string | null
  tag?: string | null
  importance?: 1 | 2 | 3 | null
}): string {
  const p = new URLSearchParams()
  if (opts.chapter) p.set('chapter', opts.chapter)
  if (opts.tag) p.set('tag', opts.tag)
  if (opts.importance != null) p.set('importance', String(opts.importance))
  const qs = p.toString()
  return qs ? `/memorize?${qs}` : '/memorize'
}
