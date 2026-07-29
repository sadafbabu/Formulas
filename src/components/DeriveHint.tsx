import { Link, useSearchParams } from 'react-router-dom'
import type { Formula } from '../data/types'
import { HintPopover } from './HintPopover'
import { Katex } from './Katex'
import { MathOrText } from './MathOrText'

interface DeriveHintProps {
  formula: Formula
}

export function DeriveHint({ formula }: DeriveHintProps) {
  const first = formula.derivation.steps[0]
  const [params] = useSearchParams()
  const chapter = params.get('chapter') || formula.chapter
  const detailTo = `/formula/${formula.id}?chapter=${encodeURIComponent(chapter)}`

  return (
    <HintPopover
      label={`${formula.titleBn} — কীভাবে এলো`}
      title="কেভাবে এলো"
      icon={
        <svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true">
          <path
            fill="currentColor"
            d="M8 1.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13zM7.25 5a.75.75 0 1 1 1.5 0 .75.75 0 0 1-1.5 0zM7 7.25h1.5V12H7V7.25z"
          />
        </svg>
      }
    >
      <MathOrText
        text={formula.derivation.lead}
        as="p"
        className="derive-popover-lead"
      />
      {first && (
        <div className="derive-popover-step">
          <span>{first.title}</span>
          <Katex latex={first.latex} />
        </div>
      )}
      <Link
        className="derive-popover-link"
        to={detailTo}
        onClick={(e) => e.stopPropagation()}
      >
        পুরো derivation →
      </Link>
    </HintPopover>
  )
}
