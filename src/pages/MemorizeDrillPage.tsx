import { useEffect, useMemo, useState } from 'react'
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
import { bookReturnPath } from '../utils/bookLinks'
import {
  buildDrillQueue,
  filterDrillFormulas,
  loadMemorizeProgress,
  markFormulaSeen,
  type MemorizeProgress,
} from '../utils/memorizeSession'

const validTagIds = new Set(tags.map((t) => t.id))

export function MemorizeDrillPage() {
  const [params, setParams] = useSearchParams()
  const [query, setQuery] = useState('')
  const [progress, setProgress] = useState<MemorizeProgress>(() =>
    loadMemorizeProgress(),
  )
  const [revealed, setRevealed] = useState(false)
  const [index, setIndex] = useState(0)
  const [sessionKnown, setSessionKnown] = useState(0)
  const [sessionAgain, setSessionAgain] = useState(0)
  const [done, setDone] = useState(false)

  const rawChapter = params.get('chapter')
  const chapterId =
    rawChapter && getChapter(rawChapter) ? rawChapter : defaultChapterId
  const rawTag = params.get('tag')
  const activeTag =
    rawTag && validTagIds.has(rawTag as TagId) ? (rawTag as TagId) : null
  const rawImp = params.get('importance')
  const importance: 1 | 2 | 3 | null =
    rawImp === '1' || rawImp === '2' || rawImp === '3'
      ? (Number(rawImp) as 1 | 2 | 3)
      : 3

  const pool = useMemo(
    () =>
      filterDrillFormulas(formulas, {
        chapter: chapterId,
        tag: activeTag,
        importance,
      }),
    [chapterId, activeTag, importance],
  )

  const [queue, setQueue] = useState(() => buildDrillQueue(pool, progress))

  useEffect(() => {
    const prog = loadMemorizeProgress()
    setProgress(prog)
    setQueue(buildDrillQueue(pool, prog))
    setIndex(0)
    setRevealed(false)
    setDone(pool.length === 0)
    setSessionKnown(0)
    setSessionAgain(0)
  }, [pool])

  const current = !done && queue.length > 0 ? queue[index] : undefined
  const chapterMeta = getChapter(chapterId)
  const remaining = Math.max(0, queue.length - index)

  const setChapterId = (id: string) => {
    const next = new URLSearchParams(params)
    next.set('chapter', id)
    setParams(next, { replace: true })
  }

  const setImportance = (value: 1 | 2 | 3 | null) => {
    const next = new URLSearchParams(params)
    if (value == null) next.delete('importance')
    else next.set('importance', String(value))
    setParams(next, { replace: true })
  }

  const setTag = (tag: TagId | null) => {
    const next = new URLSearchParams(params)
    if (tag) next.set('tag', tag)
    else next.delete('tag')
    setParams(next, { replace: true })
  }

  const advance = (known: boolean) => {
    if (!current) return
    setProgress((prev) => markFormulaSeen(prev, current.id, known))
    if (known) setSessionKnown((n) => n + 1)
    else setSessionAgain((n) => n + 1)

    if (known) {
      if (index + 1 >= queue.length) {
        setDone(true)
        setRevealed(false)
        return
      }
      setIndex((i) => i + 1)
      setRevealed(false)
      return
    }

    // Again: move card to end of remaining queue
    setQueue((prev) => {
      const copy = [...prev]
      const [card] = copy.splice(index, 1)
      copy.push(card)
      return copy
    })
    setRevealed(false)
    // index stays pointing at the next card that slid into place;
    // if this was the last item, wrap to same index (now the reshuffled one)
    if (index >= queue.length - 1) {
      // only one card left — keep drilling it
      setIndex(0)
    }
  }

  const backTo = bookReturnPath({
    chapter: chapterId,
    tag: activeTag,
    query: params.get('q'),
  })

  const examTags = tags.filter((t) => t.category !== 'importance')

  return (
    <div className="book-shell detail-shell memorize-shell">
      <NavMenu
        floating
        query={query}
        onQueryChange={setQuery}
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
              {importance ? ` · ${importance}★` : ''}
              {activeTag ? ` · ${activeTag}` : ''}
              {pool.length ? ` · ${pool.length} সূত্র` : ''}
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

          {pool.length === 0 ? (
            <div className="memorize-empty">
              <p>এই ফিল্টারে কোনো সূত্র নেই। অধ্যায় বা ট্যাগ বদলে দেখো।</p>
              <Link className="memorize-btn memorize-btn-primary" to={backTo}>
                বইয়ে যাও
              </Link>
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
                  onClick={() => {
                    setQueue(buildDrillQueue(pool, loadMemorizeProgress()))
                    setProgress(loadMemorizeProgress())
                    setIndex(0)
                    setSessionKnown(0)
                    setSessionAgain(0)
                    setDone(false)
                    setRevealed(false)
                  }}
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
                  {current.memorize?.steps && current.memorize.steps.length > 0 ? (
                    <ol className="memorize-card-steps">
                      {current.memorize.steps.map((step, i) => (
                        <li key={`${step}-${i}`}>{step}</li>
                      ))}
                    </ol>
                  ) : null}
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
          ) : null}
        </div>
      </main>
    </div>
  )
}
