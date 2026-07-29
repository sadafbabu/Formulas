import { useEffect, useState } from 'react'

export type LayoutMode = 'mobile' | 'tablet' | 'desktop'

function readMode(): LayoutMode {
  if (typeof window === 'undefined') return 'desktop'
  // Keep in sync with CSS @media (max-width: 699px) and desktop spread ≥1100.
  if (window.matchMedia('(max-width: 699px)').matches) return 'mobile'
  if (window.matchMedia('(max-width: 1099px)').matches) return 'tablet'
  return 'desktop'
}

/** mobile ≤699 · tablet 700–1099 · desktop ≥1100 */
export function useLayoutMode(): LayoutMode {
  const [mode, setMode] = useState<LayoutMode>(readMode)

  useEffect(() => {
    const mobileMq = window.matchMedia('(max-width: 699px)')
    const tabletMq = window.matchMedia('(max-width: 1099px)')
    const onChange = () => setMode(readMode())
    mobileMq.addEventListener('change', onChange)
    tabletMq.addEventListener('change', onChange)
    onChange()
    return () => {
      mobileMq.removeEventListener('change', onChange)
      tabletMq.removeEventListener('change', onChange)
    }
  }, [])

  return mode
}
