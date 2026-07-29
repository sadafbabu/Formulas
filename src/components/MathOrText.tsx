import { Katex } from './Katex'
import { prepareMixedTex, splitProseAndMath } from '../utils/mathText'

interface MathOrTextProps {
  text: string
  display?: boolean
  className?: string
  as?: 'span' | 'p' | 'div'
}

/** Render plain prose as text; delimited or bare TeX via KaTeX. */
export function MathOrText({
  text,
  display = false,
  className,
  as: Tag = 'span',
}: MathOrTextProps) {
  const trimmed = text.trim()
  if (!trimmed) return null

  const parts = splitProseAndMath(trimmed)
  const hasMathPart = parts.some((p) => p.type === 'math')

  if (hasMathPart) {
    return (
      <Tag className={className}>
        {parts.map((part, i) =>
          part.type === 'text' ? (
            <span key={i}>{part.value}</span>
          ) : (
            <Katex key={i} latex={prepareMixedTex(part.value)} />
          ),
        )}
      </Tag>
    )
  }

  if (!/\\[a-zA-Z]/.test(trimmed)) {
    return <Tag className={className}>{trimmed}</Tag>
  }

  return (
    <Tag className={className}>
      <Katex latex={prepareMixedTex(trimmed)} display={display} />
    </Tag>
  )
}
