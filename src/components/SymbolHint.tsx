import type { Formula } from '../data/types'
import { HintPopover } from './HintPopover'
import { Katex } from './Katex'

interface SymbolHintProps {
  formula: Formula
}

export function SymbolHint({ formula }: SymbolHintProps) {
  const symbols = formula.symbols ?? []
  if (!symbols.length) return null

  return (
    <HintPopover
      label={`${formula.titleBn} — চিহ্ন ও একক`}
      title="চিহ্ন · একক · মান"
      wide
      icon={
        <svg viewBox="0 0 16 16" width="13" height="13" aria-hidden="true">
          {/* clear "Σ" mark */}
          <path
            fill="currentColor"
            d="M3 3.2h10v1.35H5.7L10.2 8 5.7 11.45H13V12.8H3v-1.05L7.7 8 3 4.25V3.2z"
          />
        </svg>
      }
    >
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
    </HintPopover>
  )
}

function toLatexSymbol(raw: string): string {
  const map: Record<string, string> = {
    'μ₀': '\\mu_{0}',
    'I₁, I₂': 'I_{1}, I_{2}',
    'F/ℓ': 'F/\\ell',
    'I_encl': 'I_{\\mathrm{encl}}',
    '∮ B·dl': '\\oint B\\cdot dl',
    dB: 'dB',
    ℓ: '\\ell',
    θ: '\\theta',
    τ: '\\tau',
  }
  if (map[raw]) return map[raw]

  const subs: Record<string, string> = {
    '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4',
    '₅': '5', '₆': '6', '₇': '7', '₈': '8', '₉': '9',
  }
  const sups: Record<string, string> = {
    '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
    '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9',
  }
  return raw
    .replace(/[₀-₉]/g, (c) => `_{${subs[c] ?? ''}}`)
    .replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹]/g, (c) => `^{${sups[c] ?? ''}}`)
}
