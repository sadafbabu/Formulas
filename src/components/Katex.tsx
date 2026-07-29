import katex from 'katex'
import 'katex/dist/contrib/mhchem.mjs'
import { useMemo } from 'react'

interface KatexProps {
  latex: string
  display?: boolean
  className?: string
}

const cache = new Map<string, string>()

function renderLatex(latex: string, display: boolean): string {
  const key = `${display ? 'd' : 'i'}:${latex}`
  const hit = cache.get(key)
  if (hit !== undefined) return hit
  let html: string
  try {
    html = katex.renderToString(latex, {
      throwOnError: false,
      displayMode: display,
      strict: 'ignore',
    })
  } catch {
    html = latex
  }
  // Bound memory on long sessions — drop oldest when large.
  if (cache.size > 800) {
    const first = cache.keys().next().value
    if (first !== undefined) cache.delete(first)
  }
  cache.set(key, html)
  return html
}

export function Katex({ latex, display = false, className }: KatexProps) {
  const html = useMemo(() => renderLatex(latex, display), [latex, display])

  return (
    <span
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  )
}
