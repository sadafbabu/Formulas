/** Wrap bare Bangla (and similar prose) so KaTeX does not smash it in math mode. */
export function prepareMixedTex(input: string): string {
  if (!/[\u0980-\u09FF]/.test(input)) return input
  if (!hasBareBangla(input)) return input

  return input.replace(
    /([\u0980-\u09FF][^\u0980-\u09FF\\{}]*[\u0980-\u09FF]|[\u0980-\u09FF]+)/g,
    (match, _g, offset: number, whole: string) => {
      if (isInsideTextCommand(whole, offset)) return match
      return `\\text{${match}}`
    },
  )
}

function hasBareBangla(input: string): boolean {
  let i = 0
  while (i < input.length) {
    if (input.startsWith('\\text{', i)) {
      const start = i + 6
      let depth = 1
      let j = start
      while (j < input.length && depth > 0) {
        if (input[j] === '{') depth++
        else if (input[j] === '}') depth--
        j++
      }
      i = j
      continue
    }
    const code = input.charCodeAt(i)
    if (code >= 0x0980 && code <= 0x09ff) return true
    i++
  }
  return false
}

function isInsideTextCommand(input: string, offset: number): boolean {
  const before = input.slice(0, offset)
  const open = before.lastIndexOf('\\text{')
  if (open < 0) return false
  const from = open + 6
  let depth = 1
  for (let j = from; j < input.length; j++) {
    if (input[j] === '{') depth++
    else if (input[j] === '}') {
      depth--
      if (depth === 0) return offset >= from && offset < j
    }
  }
  return offset >= from
}

/** Map common unicode / shorthand symbols into KaTeX-safe forms. */
export function toLatexSymbol(raw: string): string {
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
  return (
    map[raw] ??
    raw
      .replace(/₀/g, '_{0}')
      .replace(/₁/g, '_{1}')
      .replace(/₂/g, '_{2}')
      .replace(/₃/g, '_{3}')
  )
}
