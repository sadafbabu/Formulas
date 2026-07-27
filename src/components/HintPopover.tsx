import {
  useEffect,
  useId,
  useRef,
  useState,
  type ReactNode,
} from 'react'

interface HintPopoverProps {
  label: string
  title: string
  icon: ReactNode
  children: ReactNode
  wide?: boolean
}

/** Click/tap + hover popover that portals-like escapes overflow via fixed position */
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

  const place = () => {
    const btn = rootRef.current
    if (!btn) return
    const r = btn.getBoundingClientRect()
    const width = wide ? 300 : 280
    const left = Math.min(
      Math.max(8, r.right - width),
      window.innerWidth - width - 8,
    )
    const top = Math.min(r.bottom + 6, window.innerHeight - 12)
    setPos({ top, left })
  }

  useEffect(() => {
    if (!open) return
    place()
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setOpen(false)
    }
    const onPointer = (e: MouseEvent) => {
      if (!rootRef.current?.contains(e.target as Node)) setOpen(false)
    }
    const onScroll = () => place()
    window.addEventListener('keydown', onKey)
    window.addEventListener('mousedown', onPointer)
    window.addEventListener('resize', onScroll)
    window.addEventListener('scroll', onScroll, true)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.removeEventListener('mousedown', onPointer)
      window.removeEventListener('resize', onScroll)
      window.removeEventListener('scroll', onScroll, true)
    }
  }, [open, wide])

  return (
    <div
      className="hint-wrap"
      ref={rootRef}
      onMouseEnter={() => {
        if (window.matchMedia('(hover: hover)').matches) {
          place()
          setOpen(true)
        }
      }}
      onMouseLeave={() => {
        if (window.matchMedia('(hover: hover)').matches) setOpen(false)
      }}
    >
      <button
        type="button"
        className="hint-btn"
        aria-label={label}
        aria-expanded={open}
        aria-controls={tipId}
        title={title}
        onClick={(e) => {
          e.stopPropagation()
          place()
          setOpen((v) => !v)
        }}
      >
        {icon}
      </button>

      {open && (
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
        </div>
      )}
    </div>
  )
}
