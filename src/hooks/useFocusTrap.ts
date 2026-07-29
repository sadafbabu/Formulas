import { useEffect, type RefObject } from 'react'

const FOCUSABLE =
  'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'

interface FocusTrapOptions {
  /** When false, skip autofocusing inputs (avoids mobile keyboard jump). */
  focusInput?: boolean
}

/**
 * Trap Tab focus inside `containerRef` while `active`, restore focus on cleanup.
 */
export function useFocusTrap(
  active: boolean,
  containerRef: RefObject<HTMLElement | null>,
  restoreRef?: RefObject<HTMLElement | null>,
  options: FocusTrapOptions = {},
) {
  const { focusInput = true } = options

  useEffect(() => {
    if (!active) return
    const container = containerRef.current
    if (!container) return

    const previouslyFocused =
      (document.activeElement as HTMLElement | null) ?? null
    const restoreTarget = restoreRef?.current ?? previouslyFocused

    const focusables = () => {
      const nodes = Array.from(
        container.querySelectorAll<HTMLElement>(FOCUSABLE),
      ).filter((el) => {
        if (el.hasAttribute('disabled')) return false
        if (el.getAttribute('aria-hidden') === 'true') return false
        const style = window.getComputedStyle(el)
        if (style.display === 'none' || style.visibility === 'hidden') return false
        return el.getClientRects().length > 0
      })
      // Dialog shell itself is a last-resort focus target.
      if (
        !nodes.length &&
        container.tabIndex >= -1 &&
        container.getClientRects().length > 0
      ) {
        return [container]
      }
      return nodes
    }

    const focusFirst = window.requestAnimationFrame(() => {
      const nodes = focusables()
      let preferred: HTMLElement | null = null
      if (focusInput) {
        preferred =
          container.querySelector<HTMLElement>('input, textarea, [autofocus]') ||
          nodes[0] ||
          null
      } else {
        preferred =
          nodes.find((n) => n.tagName !== 'INPUT' && n.tagName !== 'TEXTAREA') ||
          container
      }
      preferred?.focus()
    })

    const onKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return
      const nodes = focusables()
      if (!nodes.length) {
        e.preventDefault()
        container.focus()
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
      } else if (current === last || current === container) {
        e.preventDefault()
        first.focus()
      }
    }

    document.addEventListener('keydown', onKeyDown)
    return () => {
      window.cancelAnimationFrame(focusFirst)
      document.removeEventListener('keydown', onKeyDown)
      if (
        restoreTarget &&
        document.contains(restoreTarget) &&
        typeof restoreTarget.focus === 'function'
      ) {
        restoreTarget.focus()
      }
    }
  }, [active, containerRef, restoreRef, focusInput])
}
