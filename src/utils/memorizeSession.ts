import type { Formula, TagId } from '../data/types'

const STORAGE_KEY = 'memorize-progress-v1'

export type MemorizeProgressEntry = {
  known: boolean
  seen: number
  updatedAt: number
}

export type MemorizeProgress = Record<string, MemorizeProgressEntry>

export function loadMemorizeProgress(): MemorizeProgress {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return {}
    const parsed = JSON.parse(raw) as MemorizeProgress
    return parsed && typeof parsed === 'object' ? parsed : {}
  } catch {
    return {}
  }
}

export function saveMemorizeProgress(progress: MemorizeProgress): void {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress))
  } catch {
    // ignore quota / private mode
  }
}

/** Wipe all memorize progress (known/seen flags). */
export function clearMemorizeProgress(): MemorizeProgress {
  try {
    localStorage.removeItem(STORAGE_KEY)
  } catch {
    // ignore
  }
  return {}
}

export function markFormulaSeen(
  progress: MemorizeProgress,
  id: string,
  known: boolean,
): MemorizeProgress {
  const prev = progress[id]
  const next: MemorizeProgress = {
    ...progress,
    [id]: {
      known,
      seen: (prev?.seen ?? 0) + 1,
      updatedAt: Date.now(),
    },
  }
  saveMemorizeProgress(next)
  return next
}

/** Map book star tags to numeric importance; ignore non-star tags. */
export function importanceFromTag(
  tag: string | null | undefined,
): 1 | 2 | 3 | null {
  if (tag === '1-star') return 1
  if (tag === '2-star') return 2
  if (tag === '3-star') return 3
  return null
}

export function isStarTag(tag: string | null | undefined): boolean {
  return tag === '1-star' || tag === '2-star' || tag === '3-star'
}

export function filterDrillFormulas(
  all: Formula[],
  opts: {
    chapter?: string | null
    tag?: TagId | null
    importance?: 1 | 2 | 3 | null
    unknownOnly?: boolean
    progress?: MemorizeProgress
  },
): Formula[] {
  const examTag =
    opts.tag && !isStarTag(opts.tag) ? opts.tag : null
  return all.filter((f) => {
    if (opts.chapter && f.chapter !== opts.chapter) return false
    if (examTag && !f.tags.includes(examTag)) return false
    if (opts.importance != null && (f.importance ?? 2) !== opts.importance) {
      return false
    }
    if (opts.unknownOnly && opts.progress) {
      const entry = opts.progress[f.id]
      if (entry?.known) return false
    }
    return true
  })
}

/** Build a practice queue: unknown first, then unreviewed, then known last. */
export function buildDrillQueue(
  list: Formula[],
  progress: MemorizeProgress,
  unknownOnly = false,
  startId?: string | null,
): Formula[] {
  const unknown: Formula[] = []
  const fresh: Formula[] = []
  const known: Formula[] = []
  for (const f of list) {
    const entry = progress[f.id]
    if (!entry) fresh.push(f)
    else if (entry.known) known.push(f)
    else unknown.push(f)
  }
  const base = unknownOnly ? [...unknown, ...fresh] : [...unknown, ...fresh, ...known]
  if (!startId) return base
  const idx = base.findIndex((f) => f.id === startId)
  if (idx <= 0) return base
  const pinned = base[idx]
  return [pinned, ...base.slice(0, idx), ...base.slice(idx + 1)]
}
