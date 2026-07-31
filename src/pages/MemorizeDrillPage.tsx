import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Katex } from '../components/Katex'
import { NavMenu } from '../components/NavMenu'
import {
  chapters,
  defaultChapterId,
  formulas,
  getChapter,
  tags,
} from '../data/catalog'
import type { TagId } from '../data/types'
import { bookReturnPath, formulaDetailPath } from '../utils/bookLinks'
import {
  buildDrillQueue,
  filterDrillFormulas,
  isStarTag,
  loadMemorizeProgress,
  markFormulaSeen,
  type MemorizeProgress,
} from '../utils/memorizeSession'

const examTagIds = new Set(
  tags.filter((t) => t.category !== 'importance').map((t) => t.id),
)

export function MemorizeDrillPage() {
  const [params, setParams] = useSearchParams()
  const [query, setQuery] = useState(() => params.get('q') ?? '')
  const [progress, setProgress] = useState<MemorizeProgress>(() =>
    loadMemorizeProgress(),
  )
  const [revealed, setRevealed] = useState(false)
  const [index, setIndex] = useState(0)
  const [sessionKnown, setSessionKnown] = useState(0)
  const [sessionAgain, setSessionAgain] = useState(0)
  const [done, setDone] = useState(false)
  const advancingRef = useRef(false)
  const advanceRef = useRef<(known: boolean) => void>(() => {})

  const rawChapter = params.get('chapter')
  const chapterId =
    rawChapter && getChapter(rawChapter) ? rawChapter : defaultChapterId

  // Star tags in URL become importance, never exam filters
  const rawTag = params.get('tag')
  const activeTag: TagId | null =
    rawTag && examTagIds.has(rawTag as TagId) ? (rawTag as TagId) : null

  const rawImp = params.get('importance')
  // Missing importance = all levels (null). Only 1/2/3 are filters.
  // First-entry default (3) is set by memorizePath when linking in.
  const importance: 1 | 2 | 3 | null =
    rawImp === '1' || rawImp === '2' || rawImp === '3'
      ? (Number(rawImp) as 1 | 2 | 3)
      : null

  const unknownOnly = params.get('unknown') === '1'
  const startId = params.get('start')

  // Migrate accidental star tags out of `tag`
  useEffect(() => {
    if (!rawTag || !isStarTag(rawTag)) return
    const next = new URLSearchParams(params)
    next.delete('tag')
    if (!next.get('importance')) {
      next.set('importance', rawTag[0])
    }
    setParams(next, { replace: true })
  }, [rawTag, params, setParams])

  // Normalize invalid chapter ids in the URL (same as book page).
  useEffect(() => {
    if (!rawChapter || getChapter(rawChapter)) return
    const next = new URLSearchParams(params)
    next.set('chapter', defaultChapterId)
    setParams(next, { replace: true })
  }, [rawChapter, params, setParams])

  const pool = useMemo(
    () =>
      filterDrillFormulas(formulas, {
        chapter: chapterId,
        tag: activeTag,
        importance,
      }),
    [chapterId, activeTag, importance],
  )

  const [queue, setQueue] = useState<typeof pool>([])

  useEffect(() => {
    const prog = loadMemorizeProgress()
    setProgress(prog)
    const filtered = unknownOnly
      ? pool.filter((f) => !prog[f.id]?.known)
      : pool
    setQueue(buildDrillQueue(filtered, prog, unknownOnly, startId))
    setIndex(0)
    setRevealed(false)
    setDone(filtered.length === 0)
    setSessionKnown(0)
    setSessionAgain(0)
  }, [pool, unknownOnly, startId])

  const visibleCount = unknownOnly
    ? pool.filter((f) => !progress[f.id]?.known).length
    : pool.length

  const current = !done && queue.length > 0 ? queue[index] : undefined
  const chapterMeta = getChapter(chapterId)
  const remaining = Math.max(0, queue.length - index)

  const patchParams = (mutate: (next: URLSearchParams) => void) => {
    const next = new URLSearchParams(params)
    mutate(next)
    setParams(next, { replace: true })
  }

  const setQuerySynced = (value: string) => {
    setQuery(value)
    patchParams((next) => {
      const trimmed = value.trim()
      if (trimmed) next.set('q', trimmed)
      else next.delete('q')
    })
  }

  const setChapterId = (id: string) => {
    patchParams((next) => next.set('chapter', id))
  }

  const setImportance = (value: 1 | 2 | 3 | null) => {
    patchParams((next) => {
      if (value == null) next.delete('importance')
      else next.set('importance', String(value))
    })
  }

  const setTag = (tag: TagId | null) => {
    patchParams((next) => {
      if (tag) next.set('tag', tag)
      else next.delete('tag')
    })
  }

  const setUnknownOnly = (value: boolean) => {
    patchParams((next) => {
      if (value) next.set('unknown', '1')
      else next.delete('unknown')
    })
  }

  const advance = (known: boolean) => {
    if (!current || advancingRef.current) return
    advancingRef.current = true
    setProgress((prev) => markFormulaSeen(prev, current.id, known))
    if (known) setSessionKnown((n) => n + 1)
    else setSessionAgain((n) => n + 1)

    if (known) {
      if (index + 1 >= queue.length) {
        setDone(true)
        setRevealed(false)
        window.setTimeout(() => {
          advancingRef.current = false
        }, 0)
        return
      }
      setIndex((i) => i + 1)
      setRevealed(false)
      window.setTimeout(() => {
        advancingRef.current = false
      }, 0)
      return
    }

    // Again: move current card to the end. Index stays so the next card slides in.
    // If it was the last card, wrap to 0 (otherwise we'd re-show the same card).
    const atEnd = index >= queue.length - 1
    setQueue((prev) => {
      if (prev.length <= 1) return prev
      const copy = [...prev]
      const [card] = copy.splice(index, 1)
      copy.push(card)
      return copy
    })
    setRevealed(false)
    if (atEnd) setIndex(0)
    window.setTimeout(() => {
      advancingRef.current = false
    }, 0)
  }
  advanceRef.current = advance

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement | null
      if (target?.closest('input, textarea, select, [contenteditable="true"]')) {
        return
      }
      if (done || visibleCount === 0) return

      if (!revealed && (e.key === ' ' || e.key === 'Enter')) {
        e.preventDefault()
        setRevealed(true)
        return
      }
      if (!revealed) return
      if (e.key === '1' || e.key === 'a' || e.key === 'A') {
        e.preventDefault()
        advanceRef.current(false)
      } else if (e.key === '2' || e.key === 'k' || e.key === 'K') {
        e.preventDefault()
        advanceRef.current(true)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [done, visibleCount, revealed])

  const backTo = bookReturnPath({
    chapter: chapterId,
    tag: activeTag,
    query: params.get('q') ?? query,
  })

  const examTags = tags.filter((t) => t.category !== 'importance')

  const restart = () => {
    const prog = loadMemorizeProgress()
    setProgress(prog)
    const filtered = unknownOnly
      ? pool.filter((f) => !prog[f.id]?.known)
      : pool
    setQueue(buildDrillQueue(filtered, prog, unknownOnly, startId))
    setIndex(0)
    setSessionKnown(0)
    setSessionAgain(0)
    setDone(filtered.length === 0)
    setRevealed(false)
  }

  return (
    <div className="book-shell detail-shell memorize-shell">
      <NavMenu
        floating
        query={query}
        onQueryChange={setQuerySynced}
        chapterId={chapterId}
        onChapterChange={setChapterId}
      />

      <main className="memorize-scroll">
        <div className="memorize-panel">
          <div className="memorize-toolbar">
            <Link className="detail-back" to={backTo}>
              ← বইয়ে ফিরে যান
            </Link>
            <h1 className="memorize-title">মুখস্থ ড্রিল</h1>
            <p className="memorize-sub">
              {chapterMeta?.nameBn ?? 'অধ্যায়'}
              {importance ? ` · ${importance}★` : ' · সব ★'}
              {activeTag ? ` · ${activeTag}` : ''}
              {unknownOnly ? ' · শুধু অজানা' : ''}
              {visibleCount ? ` · ${visibleCount} সূত্র` : ''}
            </p>
            <p className="memorize-keys">
              কীবোর্ড: Space দেখাও · 1/A আবার · 2/K জানি
            </p>
          </div>

          <div className="memorize-filters">
            <label className="memorize-filter">
              <span>অধ্যায়</span>
              <select
                value={chapterId}
                onChange={(e) => setChapterId(e.target.value)}
              >
                {chapters.map((ch) => (
                  <option key={ch.id} value={ch.id}>
                    {ch.nameBn}
                  </option>
                ))}
              </select>
            </label>
            <label className="memorize-filter">
              <span>গুরুত্ব</span>
              <select
                value={importance ?? ''}
                onChange={(e) => {
                  const v = e.target.value
                  setImportance(v ? (Number(v) as 1 | 2 | 3) : null)
                }}
              >
                <option value="3">৩★</option>
                <option value="2">২★</option>
                <option value="1">১★</option>
                <option value="">সব</option>
              </select>
            </label>
            <label className="memorize-filter">
              <span>ট্যাগ</span>
              <select
                value={activeTag ?? ''}
                onChange={(e) =>
                  setTag((e.target.value || null) as TagId | null)
                }
              >
                <option value="">সব</option>
                {examTags.map((t) => (
                  <option key={t.id} value={t.id}>
                    {t.labelBn}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <label className="memorize-unknown-toggle">
            <input
              type="checkbox"
              checked={unknownOnly}
              onChange={(e) => setUnknownOnly(e.target.checked)}
            />
            শুধু অজানা / নতুন সূত্র
          </label>

          {visibleCount === 0 ? (
            <div className="memorize-empty">
              <p>
                {unknownOnly
                  ? 'এই ফিল্টারে অজানা সূত্র নেই — সব জানা হয়ে গেছে, অথবা ফিল্টার বদলাও।'
                  : 'এই ফিল্টারে কোনো সূত্র নেই। অধ্যায় বা ট্যাগ বদলে দেখো।'}
              </p>
              <div className="memorize-actions">
                {unknownOnly ? (
                  <button
                    type="button"
                    className="memorize-btn memorize-btn-primary"
                    onClick={() => setUnknownOnly(false)}
                  >
                    সব সূত্র দেখাও
                  </button>
                ) : null}
                <Link className="memorize-btn memorize-btn-primary" to={backTo}>
                  বইয়ে যাও
                </Link>
              </div>
            </div>
          ) : done ? (
            <div className="memorize-done">
              <h2>সেশন শেষ</h2>
              <p>
                জানি: <strong>{sessionKnown}</strong> · আবার:{' '}
                <strong>{sessionAgain}</strong>
              </p>
              <div className="memorize-actions">
                <button
                  type="button"
                  className="memorize-btn memorize-btn-primary"
                  onClick={restart}
                >
                  আবার শুরু
                </button>
                <Link className="memorize-btn" to={backTo}>
                  বইয়ে ফিরে যান
                </Link>
              </div>
            </div>
          ) : current ? (
            <section className="memorize-card" aria-live="polite">
              <div className="memorize-card-meta">
                <span>
                  {index + 1} / {queue.length}
                </span>
                <span>বাকি ~{remaining}</span>
              </div>
              <h2 className="memorize-card-title">{current.titleBn}</h2>
              <p className="memorize-card-en">{current.title}</p>

              {!revealed ? (
                <button
                  type="button"
                  className="memorize-reveal"
                  onClick={() => setRevealed(true)}
                >
                  সূত্র দেখাও
                </button>
              ) : (
                <div className="memorize-reveal-body">
                  <div className="memorize-latex">
                    <Katex latex={current.latex} display />
                  </div>
                  {current.memorize?.trick ? (
                    <p className="memorize-card-trick">{current.memorize.trick}</p>
                  ) : null}
                  {current.memorize?.steps &&
                  current.memorize.steps.length > 0 ? (
                    <ol className="memorize-card-steps">
                      {current.memorize.steps.map((step, i) => (
                        <li key={`${step}-${i}`}>{step}</li>
                      ))}
                    </ol>
                  ) : null}
                  <Link
                    className="memorize-detail-link"
                    to={formulaDetailPath(current.id, {
                      chapter: current.chapter,
                      tag: activeTag,
                      query: params.get('q') ?? query,
                    })}
                  >
                    বিস্তারিত দেখুন →
                  </Link>
                  <div className="memorize-actions">
                    <button
                      type="button"
                      className="memorize-btn memorize-btn-again"
                      onClick={() => advance(false)}
                    >
                      আবার
                    </button>
                    <button
                      type="button"
                      className="memorize-btn memorize-btn-primary"
                      onClick={() => advance(true)}
                    >
                      জানি
                    </button>
                  </div>
                </div>
              )}
            </section>
          ) : (
            <div className="memorize-empty">
              <p>কার্ড লোড হচ্ছে না — আবার শুরু করো।</p>
              <button
                type="button"
                className="memorize-btn memorize-btn-primary"
                onClick={restart}
              >
                আবার শুরু
              </button>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
