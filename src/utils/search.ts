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
  important: ['গুরুত্বপূর্ণ', 'সর্বোচ্চ'],
  top: ['সর্বোচ্চ', '3-star'],
}

export function matchFormula(
  formula: Formula,
  query: string,
  activeTag?: TagId | null
): boolean {
  const imp = formula.importance ?? 2

  // Tag filter
  if (activeTag) {
    if (activeTag === '3-star' && imp !== 3) return false
    if (activeTag === '2-star' && imp !== 2) return false
    if (activeTag === '1-star' && imp !== 1) return false
    if (
      !activeTag.endsWith('-star') &&
      !formula.tags.includes(activeTag)
    ) {
      return false
    }
  }

  const q = query.trim().toLowerCase()
  if (!q) return true

  // Direct star search (e.g. "3", "3 star", "3star", "***")
  if (q === '3' || q === '3 star' || q === '3star' || q === '***') {
    return imp === 3
  }
  if (q === '2' || q === '2 star' || q === '2star' || q === '**') {
    return imp === 2
  }
  if (q === '1' || q === '1 star' || q === '1star' || q === '*') {
    return imp === 1
  }

  // Text search in fields
  const inTitleEn = formula.title.toLowerCase().includes(q)
  const inTitleBn = formula.titleBn.toLowerCase().includes(q)
  const inSummary = formula.summary.toLowerCase().includes(q)
  const inLatex = formula.latex.toLowerCase().includes(q)
  const inId = formula.id.toLowerCase().includes(q)

  // Tags match
  const inTags = formula.tags.some((t) => t.toLowerCase().includes(q))

  // Symbol meanings match
  const inSymbols = formula.symbols?.some(
    (s) =>
      s.meaning.toLowerCase().includes(q) ||
      s.symbol.toLowerCase().includes(q) ||
      s.unit.toLowerCase().includes(q)
  )

  if (inTitleEn || inTitleBn || inSummary || inLatex || inId || inTags || inSymbols) {
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
