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

export function filterDrillFormulas(
  all: Formula[],
  opts: {
    chapter?: string | null
    tag?: TagId | null
    importance?: 1 | 2 | 3 | null
  },
): Formula[] {
  return all.filter((f) => {
    if (opts.chapter && f.chapter !== opts.chapter) return false
    if (opts.tag && !f.tags.includes(opts.tag)) return false
    if (opts.importance != null && (f.importance ?? 2) !== opts.importance) {
      return false
    }
    return true
  })
}

/** Build a practice queue: unknown first, then unreviewed, then known last. */
export function buildDrillQueue(
  formulas: Formula[],
  progress: MemorizeProgress,
): Formula[] {
  const unknown: Formula[] = []
  const fresh: Formula[] = []
  const known: Formula[] = []
  for (const f of formulas) {
    const entry = progress[f.id]
    if (!entry) fresh.push(f)
    else if (entry.known) known.push(f)
    else unknown.push(f)
  }
  return [...unknown, ...fresh, ...known]
}
