import type { Formula } from '../data/types'
import { toLatexSymbol } from '../utils/mathText'
import { HintPopover } from './HintPopover'
import { Katex } from './Katex'
import { MathOrText } from './MathOrText'

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
          <path
            fill="currentColor"
            d="M3 3.2h10v1.35H5.7L10.2 8 5.7 11.45H13V12.8H3v-1.05L7.7 8 3 4.25V3.2z"
          />
        </svg>
      }
    >
      <div className="symbol-table-wrap">
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
                <td>
                  <MathOrText text={s.meaning} />
                </td>
                <td>{s.unit}</td>
                <td>{s.value ?? '—'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </HintPopover>
  )
}
