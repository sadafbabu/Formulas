import { Katex } from './Katex'
import { looksLikeTex, prepareMixedTex } from '../utils/mathText'

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

  if (!looksLikeTex(trimmed)) {
    return <Tag className={className}>{trimmed}</Tag>
  }

  return (
    <Tag className={className}>
      <Katex latex={prepareMixedTex(trimmed)} display={display} />
    </Tag>
  )
}
