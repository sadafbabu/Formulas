import type { Formula, TagId } from '../data/types'

/** Common Banglish to English/Bangla search term aliases */
const ALIASES: Record<string, string[]> = {
  lorentz: ['লরেঞ্জ', 'লরেঞ্জ বল'],
  biot: ['বায়োট', 'সাভার্ট', 'biot-savart'],
  savart: ['বায়োট', 'সাভার্ট'],
  solenoid: ['সোলেনয়েড'],
  toroid: ['টরয়েড'],
  ammeter: ['অ্যামিটার', 'এমিটার'],
  voltmeter: ['ভোল্টমিটার'],
  shunt: ['শাণ্ট', 'শান্ট'],
  flux: ['ফ্লাক্স'],
  hall: ['হল', 'হল বিভব'],
  cyclotron: ['সাইক্লোট্রন'],
  force: ['বল', 'force'],
  field: ['ক্ষেত্র', 'চৌম্বক ক্ষেত্র'],
  earth: ['ভূ-চৌম্বক', 'বিনতি'],
  dip: ['বিনতি', 'কোণ'],
  torque: ['টর্ক'],
  moment: ['ভ্রামক', 'মোমেন্ট'],
  wire: ['তার', 'পরিবাহী'],
  loop: ['লুপ', 'কুন্ডলী'],
  radius: ['ব্যাসার্ধ'],
  freq: ['কম্পাঙ্ক'],
  star: ['স্টার'],
}

export function matchFormula(
  formula: Formula,
  query: string,
  activeTag?: TagId | null
): boolean {
  // Tag filter
  if (activeTag) {
    if (activeTag === '3-star' && formula.importance !== 3) return false
    if (activeTag === '2-star' && formula.importance !== 2) return false
    if (activeTag === '1-star' && formula.importance !== 1) return false
    if (!formula.tags.includes(activeTag) && formula.importance !== (activeTag === '3-star' ? 3 : activeTag === '2-star' ? 2 : activeTag === '1-star' ? 1 : null)) {
      return false
    }
  }

  const q = query.trim().toLowerCase()
  if (!q) return true

  // Direct term matches
  const inTitleEn = formula.title.toLowerCase().includes(q)
  const inTitleBn = formula.titleBn.toLowerCase().includes(q)
  const inSummary = formula.summary.toLowerCase().includes(q)
  const inLatex = formula.latex.toLowerCase().includes(q)
  const inId = formula.id.toLowerCase().includes(q)

  // Symbol meanings match
  const inSymbols = formula.symbols?.some(
    (s) =>
      s.meaning.toLowerCase().includes(q) ||
      s.symbol.toLowerCase().includes(q) ||
      s.unit.toLowerCase().includes(q)
  )

  if (inTitleEn || inTitleBn || inSummary || inLatex || inId || inSymbols) {
    return true
  }

  // Alias expansion for Banglish terms
  for (const [key, aliasList] of Object.entries(ALIASES)) {
    if (q.includes(key)) {
      for (const alias of aliasList) {
        if (
          formula.titleBn.toLowerCase().includes(alias) ||
          formula.summary.toLowerCase().includes(alias) ||
          formula.title.toLowerCase().includes(alias)
        ) {
          return true
        }
      }
    }
  }

  return false
}
