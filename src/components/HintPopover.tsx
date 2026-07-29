import {
  useCallback,
  useEffect,
  useId,
  useLayoutEffect,
  useRef,
  useState,
  type ReactNode,
} from 'react'
import { createPortal } from 'react-dom'

interface HintPopoverProps {
  label: string
  title: string
  icon: ReactNode
  children: ReactNode
  wide?: boolean
}

const FOCUSABLE =
  'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'

export function HintPopover({
  label,
  title,
  icon,
  children,
  wide,
}: HintPopoverProps) {
  const [open, setOpen] = useState(false)
  const tipId = useId()
  const titleId = useId()
  const rootRef = useRef<HTMLDivElement>(null)
  const triggerRef = useRef<HTMLButtonElement>(null)
  const panelRef = useRef<HTMLDivElement>(null)
  const closeRef = useRef<HTMLButtonElement>(null)
  const [pos, setPos] = useState({ top: 0, left: 0 })

  const place = useCallback(() => {
    const btn = rootRef.current
    const panel = panelRef.current
    if (!btn) return
    const r = btn.getBoundingClientRect()
    const width =
      panel?.offsetWidth ||
      (wide ? Math.min(448, window.innerWidth - 16) : 260)
    const height = panel?.offsetHeight || 180
    let left = Math.min(
      Math.max(8, r.right - width),
      window.innerWidth - width - 8,
    )
    let top = r.bottom + 8
    if (top + height > window.innerHeight - 8) {
      top = Math.max(8, r.top - height - 8)
    }
    if (height > window.innerHeight - 16) {
      top = 8
    }
    setPos({ top, left })
  }, [wide])

  useLayoutEffect(() => {
    if (!open) return
    place()
    const id = window.requestAnimationFrame(() => {
      place()
      window.requestAnimationFrame(place)
    })
    return () => window.cancelAnimationFrame(id)
  }, [open, children, place])

  useEffect(() => {
    if (!open) return
    const previouslyFocused = document.activeElement as HTMLElement | null
    closeRef.current?.focus()

    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        e.preventDefault()
        setOpen(false)
        return
      }
      if (e.key !== 'Tab' || !panelRef.current) return
      const nodes = [
        ...panelRef.current.querySelectorAll<HTMLElement>(FOCUSABLE),
      ].filter((el) => !el.hasAttribute('disabled') && el.tabIndex !== -1)
      if (!nodes.length) {
        e.preventDefault()
        return
      }
      const first = nodes[0]
      const last = nodes[nodes.length - 1]
      const active = document.activeElement as HTMLElement | null
      if (e.shiftKey && active === first) {
        e.preventDefault()
        last.focus()
      } else if (!e.shiftKey && active === last) {
        e.preventDefault()
        first.focus()
      }
    }

    const onPointer = (e: MouseEvent | TouchEvent) => {
      const t = e.target as Node
      if (rootRef.current?.contains(t)) return
      if (panelRef.current?.contains(t)) return
      setOpen(false)
    }
    const onScroll = () => place()
    window.addEventListener('keydown', onKey)
    window.addEventListener('mousedown', onPointer)
    window.addEventListener('touchstart', onPointer)
    window.addEventListener('resize', onScroll)
    window.addEventListener('scroll', onScroll, true)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.removeEventListener('mousedown', onPointer)
      window.removeEventListener('touchstart', onPointer)
      window.removeEventListener('resize', onScroll)
      window.removeEventListener('scroll', onScroll, true)
      previouslyFocused?.focus?.()
    }
  }, [open, place])

  return (
    <div className="hint-wrap" ref={rootRef}>
      <button
        ref={triggerRef}
        type="button"
        className="hint-btn"
        aria-label={label}
        aria-expanded={open}
        aria-controls={tipId}
        aria-haspopup="dialog"
        title={title}
        onClick={(e) => {
          e.stopPropagation()
          setOpen((v) => !v)
        }}
      >
        {icon}
      </button>

      {open &&
        createPortal(
          <div
            id={tipId}
            ref={panelRef}
            className={`hint-popover${wide ? ' is-wide' : ''}`}
            role="dialog"
            aria-modal="true"
            aria-labelledby={titleId}
            style={{ top: pos.top, left: pos.left }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="hint-popover-head">
              <p id={titleId} className="hint-popover-title">
                {title}
              </p>
              <button
                ref={closeRef}
                type="button"
                className="hint-popover-close"
                aria-label="বন্ধ করুন"
                onClick={() => setOpen(false)}
              >
                ×
              </button>
            </div>
            {children}
          </div>,
          document.body,
        )}
    </div>
  )
}
