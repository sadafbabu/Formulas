import { useEffect, type RefObject } from 'react'

const FOCUSABLE =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'

/**
 * Trap Tab focus inside `containerRef` while `active`, restore focus on cleanup.
 */
export function useFocusTrap(
  active: boolean,
  containerRef: RefObject<HTMLElement | null>,
  restoreRef?: RefObject<HTMLElement | null>,
) {
  useEffect(() => {
    if (!active) return
    const container = containerRef.current
    if (!container) return

    const previouslyFocused =
      (document.activeElement as HTMLElement | null) ?? null
    const restoreTarget = restoreRef?.current ?? previouslyFocused

    const focusables = () =>
      Array.from(container.querySelectorAll<HTMLElement>(FOCUSABLE)).filter(
        (el) => {
          if (el.hasAttribute('disabled')) return false
          if (el.getAttribute('aria-hidden') === 'true') return false
          if (el.tabIndex === -1 && el.tagName !== 'A') {
            // Allow explicitly focusable dialog shells, skip other tabindex=-1.
            if (!el.hasAttribute('tabindex')) return false
          }
          const style = window.getComputedStyle(el)
          if (style.display === 'none' || style.visibility === 'hidden') return false
          return el.getClientRects().length > 0
        },
      )

    // Defer so portal content is painted.
    const focusFirst = window.requestAnimationFrame(() => {
      const nodes = focusables()
      const preferred =
        container.querySelector<HTMLElement>('input, textarea, [autofocus]') ||
        nodes[0]
      preferred?.focus()
    })

    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return
      const nodes = focusables()
      if (!nodes.length) {
        e.preventDefault()
        return
      }
      const first = nodes[0]
      const last = nodes[nodes.length - 1]
      const current = document.activeElement as HTMLElement | null
      if (e.shiftKey) {
        if (current === first || !container.contains(current)) {
          e.preventDefault()
          last.focus()
        }
      } else if (current === last) {
        e.preventDefault()
        first.focus()
      }
    }

    document.addEventListener('keydown', onKeyDown)
    return () => {
      window.cancelAnimationFrame(focusFirst)
      document.removeEventListener('keydown', onKeyDown)
      if (restoreTarget && typeof restoreTarget.focus === 'function') {
        restoreTarget.focus()
      }
    }
  }, [active, containerRef, restoreRef])
}
