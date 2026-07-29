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
    const pad = 10
    const width = panel?.offsetWidth || (wide ? 300 : 260)
    const height = panel?.offsetHeight || 180
    const maxLeft = Math.max(pad, window.innerWidth - width - pad)
    const left = Math.min(Math.max(pad, r.right - width), maxLeft)
    let top = r.bottom + 8
    if (top + height > window.innerHeight - pad) {
      top = Math.max(pad, r.top - height - 8)
    }
    // Keep within viewport even if panel is taller than the screen
    const maxTop = Math.max(pad, window.innerHeight - Math.min(height, window.innerHeight - pad * 2) - pad)
    top = Math.min(top, maxTop)
    setPos({ top, left })
  }, [wide])

  useLayoutEffect(() => {
    if (open) place()
  }, [open, place, children])

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
