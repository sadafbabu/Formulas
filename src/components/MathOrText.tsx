import { Katex } from './Katex'
import { prepareMixedTex } from '../utils/mathText'

interface MathOrTextProps {
  text: string
  display?: boolean
  className?: string
  as?: 'span' | 'p' | 'div'
}

/** Render plain prose as text; mixed/TeX strings via KaTeX with Bangla wrapped in \\text{}. */
export function MathOrText({
  text,
  display = false,
  className,
  as: Tag = 'span',
}: MathOrTextProps) {
  const trimmed = text.trim()
  if (!trimmed) return null

  if (!/\\[a-zA-Z]/.test(trimmed)) {
    return <Tag className={className}>{trimmed}</Tag>
  }

  return (
    <Tag className={className}>
      <Katex latex={prepareMixedTex(trimmed)} display={display} />
    </Tag>
  )
}
