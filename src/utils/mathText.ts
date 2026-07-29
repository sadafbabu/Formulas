/** Wrap bare Bangla prose so KaTeX does not smash it in math mode. */
export function prepareMixedTex(input: string): string {
  if (!/[\u0980-\u09FF]/.test(input)) return input
  if (!hasBareBangla(input)) return input

  let out = ''
  let i = 0
  while (i < input.length) {
    if (input[i] === '\\') {
      const end = consumeTexCommand(input, i)
      out += input.slice(i, end)
      i = end
      continue
    }

    let j = i
    while (j < input.length && input[j] !== '\\') j++
    const prose = input.slice(i, j)
    if (/[\u0980-\u09FF]/.test(prose)) {
      out += `\\text{${prose}}`
    } else {
      out += prose
    }
    i = j
  }
  return out
}

/** Consume a TeX command starting at `\\`, including following `{...}` groups. */
function consumeTexCommand(input: string, start: number): number {
  let i = start + 1
  if (i >= input.length) return input.length

  if (/[a-zA-Z]/.test(input[i])) {
    while (i < input.length && /[a-zA-Z]/.test(input[i])) i++
    if (i < input.length && input[i] === '*') i++
  } else {
    i++
  }

  while (i < input.length && input[i] === '{') {
    let depth = 1
    i++
    while (i < input.length && depth > 0) {
      if (input[i] === '{') depth++
      else if (input[i] === '}') depth--
      i++
    }
  }
  return i
}

function hasBareBangla(input: string): boolean {
  let i = 0
  while (i < input.length) {
    if (input[i] === '\\') {
      i = consumeTexCommand(input, i)
      continue
    }
    const code = input.charCodeAt(i)
    if (code >= 0x0980 && code <= 0x09ff) return true
    i++
  }
  return false
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
  if (map[raw]) return map[raw]

  const subs: Record<string, string> = {
    '₀': '0',
    '₁': '1',
    '₂': '2',
    '₃': '3',
    '₄': '4',
    '₅': '5',
    '₆': '6',
    '₇': '7',
    '₈': '8',
    '₉': '9',
  }
  const sups: Record<string, string> = {
    '⁰': '0',
    '¹': '1',
    '²': '2',
    '³': '3',
    '⁴': '4',
    '⁵': '5',
    '⁶': '6',
    '⁷': '7',
    '⁸': '8',
    '⁹': '9',
  }
  return raw
    .replace(/\$/g, '')
    .replace(/[₀-₉]/g, (c) => `_{${subs[c] ?? ''}}`)
    .replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹]/g, (c) => `^{${sups[c] ?? ''}}`)
}

/** Strip leftover `$...$` delimiters from prose fields. */
export function stripDollarMath(input: string): string {
  return input.replace(/\$([^$]*)\$/g, '$1').replace(/\$/g, '')
}
