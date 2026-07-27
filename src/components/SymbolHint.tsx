import { useId, useState } from 'react'
import type { Formula } from '../data/types'
import { Katex } from './Katex'

interface SymbolHintProps {
  formula: Formula
}

export function SymbolHint({ formula }: SymbolHintProps) {
  const [open, setOpen] = useState(false)
  const tipId = useId()
  const symbols = formula.symbols ?? []

  if (!symbols.length) return null

  return (
    <div
      className="hint-wrap symbol-hint"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
      onFocus={() => setOpen(true)}
      onBlur={() => setOpen(false)}
    >
      <button
        type="button"
        className="hint-btn"
        aria-label={`${formula.titleBn} — চিহ্ন ও একক`}
        aria-describedby={open ? tipId : undefined}
        title="চিহ্ন · একক · মান"
      >
        <svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true">
          <path
            fill="currentColor"
            d="M3.2 3.2h3.1v1.3H5.1v7h1.2v1.3H3.2v-1.3h1.2v-7H3.2V3.2zm6.2 0h3.4l-2.2 9.6h-1.5L11.6 4.5H9.4V3.2z"
          />
        </svg>
      </button>

      {open && (
        <div id={tipId} className="hint-popover symbol-popover" role="tooltip">
          <p className="hint-popover-title">চিহ্ন · একক · মান</p>
          <table className="symbol-table">
            <thead>
              <tr>
                <th>চিহ্ন</th>
                <th>অর্থ</th>
                <th>একক</th>
                <th>মান</th>
              </tr>
            </thead>
            <tbody>
              {symbols.map((s) => (
                <tr key={`${s.symbol}-${s.meaning}`}>
                  <td className="symbol-cell">
                    <Katex latex={toLatexSymbol(s.symbol)} />
                  </td>
                  <td>{s.meaning}</td>
                  <td>{s.unit}</td>
                  <td>{s.value ?? '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

/** Best-effort: plain symbols → KaTeX-friendly */
function toLatexSymbol(raw: string): string {
  const map: Record<string, string> = {
    'μ₀': '\\mu_{0}',
    'I₁, I₂': 'I_{1}, I_{2}',
    'F/ℓ': 'F/\\ell',
    'I_encl': 'I_{\\mathrm{encl}}',
    '∮ B·dl': '\\oint B\\cdot dl',
    'dB': 'dB',
    'ℓ': '\\ell',
    'θ': '\\theta',
    'τ': '\\tau',
  }
  return map[raw] ?? raw.replace(/₀/g, '_{0}').replace(/₁/g, '_{1}').replace(/₂/g, '_{2}')
}
