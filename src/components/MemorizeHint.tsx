import { Link, useSearchParams } from 'react-router-dom'
import type { Formula } from '../data/types'
import { memorizePath } from '../utils/bookLinks'
import { HintPopover } from './HintPopover'

interface MemorizeHintProps {
  formula: Formula
}

export function MemorizeHint({ formula }: MemorizeHintProps) {
  const memo = formula.memorize
  const [params] = useSearchParams()
  if (!memo) return null

  const drillTo = memorizePath({
    chapter: formula.chapter,
    tag: params.get('tag'),
    importance: (formula.importance as 1 | 2 | 3) ?? 3,
  })

  return (
    <HintPopover
      label={`${formula.titleBn} — মুখস্থ করার উপায়`}
      title="মুখস্থ · মনে রাখার কৌশল"
      icon={
        <svg
          viewBox="0 0 24 24"
          width="14"
          height="14"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <path d="M9.5 2A2.5 2.5 0 0 0 7 4.5v15A2.5 2.5 0 0 0 9.5 22h5A2.5 2.5 0 0 0 17 19.5v-15A2.5 2.5 0 0 0 14.5 2h-5z" />
          <line x1="7" y1="6" x2="17" y2="6" />
          <line x1="7" y1="18" x2="17" y2="18" />
          <path d="M11 10h2M11 13h2" />
        </svg>
      }
      wide
    >
      <div className="memorize-popover-content">
        <p className="memorize-kicker">মনে রাখার কৌশল</p>
        <p className="memorize-trick">{memo.trick}</p>
        {memo.steps && memo.steps.length > 0 && (
          <ol className="memorize-steps">
            {memo.steps.map((s, i) => (
              <li key={i}>{s}</li>
            ))}
          </ol>
        )}
        <Link className="memorize-hint-drill" to={drillTo}>
          মুখস্থ ড্রিল →
        </Link>
      </div>
    </HintPopover>
  )
}
