import { useEffect, useState } from 'react'

export type LayoutMode = 'mobile' | 'tablet' | 'desktop'

function readMode(): LayoutMode {
  if (typeof window === 'undefined') return 'desktop'
  const w = window.innerWidth
  if (w < 700) return 'mobile'
  if (w < 1100) return 'tablet'
  return 'desktop'
}

/** mobile <700 · tablet 700–1099 · desktop ≥1100 */
export function useLayoutMode(): LayoutMode {
  const [mode, setMode] = useState<LayoutMode>(readMode)

  useEffect(() => {
    const onResize = () => setMode(readMode())
    window.addEventListener('resize', onResize)
    return () => window.removeEventListener('resize', onResize)
  }, [])

  return mode
}
