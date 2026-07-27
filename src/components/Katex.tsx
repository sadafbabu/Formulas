import katex from 'katex'

interface KatexProps {
  latex: string
  display?: boolean
  className?: string
}

export function Katex({ latex, display = false, className }: KatexProps) {
  let html = ''
  try {
    html = katex.renderToString(latex, {
      throwOnError: false,
      displayMode: display,
      strict: 'ignore',
    })
  } catch {
    html = latex
  }

  return (
    <span
      className={className}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  )
}
