/** True when a string should render via KaTeX (not as plain prose). */
export function looksLikeTex(input: string): boolean {
  const t = input.trim()
  if (!t) return false
  if (/\\[a-zA-Z]/.test(t)) return true
  if (/[_^]/.test(t)) return true
  // Compact ASCII equations: PV=nRT, y=mx+c, Q=mL
  if (
    /^[\x20-\x7E]+$/.test(t) &&
    /=/.test(t) &&
    /[A-Za-z]/.test(t) &&
    t.length <= 160 &&
    (t.match(/\s/g) ?? []).length <= 10
  ) {
    if (/^(The|This|When|If|For|In|A |An )\b/i.test(t)) return false
    if (
      /\b(is|are|was|were|the|and|with|from|that|which)\b/i.test(t) &&
      t.split(/\s+/).length > 6
    ) {
      return false
    }
    return true
  }
  return false
}

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
  return (
    map[raw] ??
    raw
      .replace(/\$/g, '')
      .replace(/₀/g, '_{0}')
      .replace(/₁/g, '_{1}')
      .replace(/₂/g, '_{2}')
      .replace(/₃/g, '_{3}')
  )
}

/** Strip leftover `$...$` delimiters from prose fields. */
export function stripDollarMath(input: string): string {
  return input.replace(/\$([^$]*)\$/g, '$1').replace(/\$/g, '')
}
