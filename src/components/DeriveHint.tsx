import { useId, useState } from 'react'
import { Link } from 'react-router-dom'
import type { Formula } from '../data/types'
import { Katex } from './Katex'

interface DeriveHintProps {
  formula: Formula
}

export function DeriveHint({ formula }: DeriveHintProps) {
  const [open, setOpen] = useState(false)
  const tipId = useId()
  const first = formula.derivation.steps[0]

  return (
    <div
      className="derive-hint"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      onFocus={() => setOpen(true)}
      onBlur={() => setOpen(false)}
    >
      <button
        type="button"
        className="derive-btn"
        aria-label={`${formula.titleBn} — কীভাবে এলো`}
        aria-describedby={open ? tipId : undefined}
      >
        <svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true">
          <path
            fill="currentColor"
            d="M8 1.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13zM7.25 5a.75.75 0 1 1 1.5 0 .75.75 0 0 1-1.5 0zM7 7.25h1.5V12H7V7.25z"
          />
        </svg>
      </button>

      {open && (
        <div id={tipId} className="derive-popover" role="tooltip">
          <p className="derive-popover-lead">{formula.derivation.lead}</p>
          {first && (
            <div className="derive-popover-step">
              <span>{first.title}</span>
              <Katex latex={first.latex} />
            </div>
          )}
          <Link
            className="derive-popover-link"
            to={`/formula/${formula.id}`}
            onClick={(e) => e.stopPropagation()}
          >
            পুরো derivation →
          </Link>
        </div>
      )}
    </div>
  )
}
