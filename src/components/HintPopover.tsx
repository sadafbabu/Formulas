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

export function HintPopover({
  label,
  title,
  icon,
  children,
  wide,
}: HintPopoverProps) {
  const [open, setOpen] = useState(false)
  const tipId = useId()
  const rootRef = useRef<HTMLDivElement>(null)
  const panelRef = useRef<HTMLDivElement>(null)
  const [pos, setPos] = useState({ top: 0, left: 0 })

  const place = useCallback(() => {
    const btn = rootRef.current
    const panel = panelRef.current
    if (!btn) return
    const r = btn.getBoundingClientRect()
    const mobile = window.innerWidth < 700
    const width = mobile
      ? Math.min(window.innerWidth - 16, wide ? 420 : 320)
      : panel?.offsetWidth || (wide ? Math.min(448, window.innerWidth - 16) : 260)
    const height = panel?.offsetHeight || 180
    let left: number
    let top: number

    if (mobile) {
      // Centered sheet — reliable on small screens / notches.
      left = Math.max(8, (window.innerWidth - width) / 2)
      top = Math.max(8, Math.min(r.bottom + 8, window.innerHeight - height - 12))
      if (top + height > window.innerHeight - 8) {
        top = Math.max(8, window.innerHeight - height - 12)
      }
    } else {
      left = Math.min(
        Math.max(8, r.right - width),
        window.innerWidth - width - 8,
      )
      top = r.bottom + 8
      if (top + height > window.innerHeight - 8) {
        top = Math.max(8, r.top - height - 8)
      }
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
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false)
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
    }
  }, [open, place])

  return (
    <div className="hint-wrap" ref={rootRef}>
      <button
        type="button"
        className="hint-btn"
        aria-label={label}
        aria-expanded={open}
        aria-controls={tipId}
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
            aria-label={title}
            style={{ top: pos.top, left: pos.left }}
            onClick={(e) => e.stopPropagation()}
          >
            <p className="hint-popover-title">{title}</p>
            {children}
          </div>,
          document.body,
        )}
    </div>
  )
}
