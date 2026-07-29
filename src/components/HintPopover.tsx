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
import { useFocusTrap } from '../hooks/useFocusTrap'
import { readSafeInsets, viewportBox } from '../utils/safeArea'

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
  const btnRef = useRef<HTMLButtonElement>(null)
  const panelRef = useRef<HTMLDivElement>(null)
  const [pos, setPos] = useState({ top: 0, left: 0 })

  const place = useCallback(() => {
    const btn = rootRef.current
    const panel = panelRef.current
    if (!btn) return
    const r = btn.getBoundingClientRect()
    const safe = readSafeInsets()
    const vp = viewportBox()
    const mobile = window.matchMedia('(max-width: 699px)').matches
    const gap = 8
    const marginX = Math.max(8, safe.left, safe.right) + 4
    const marginBottom = Math.max(12, safe.bottom + 8)
    const marginTop = Math.max(8, safe.top + 4)

    const maxWidth = vp.width - marginX * 2
    const width = mobile
      ? Math.min(maxWidth, wide ? 420 : 320)
      : panel?.offsetWidth || Math.min(wide ? 448 : 260, maxWidth)
    const height = panel?.offsetHeight || 180

    let left: number
    let top: number

    if (mobile) {
      left = vp.offsetLeft + Math.max(marginX, (vp.width - width) / 2)
      top = Math.max(
        vp.offsetTop + marginTop,
        Math.min(r.bottom + gap, vp.offsetTop + vp.height - height - marginBottom),
      )
      if (top + height > vp.offsetTop + vp.height - marginBottom) {
        top = Math.max(
          vp.offsetTop + marginTop,
          vp.offsetTop + vp.height - height - marginBottom,
        )
      }
    } else {
      left = Math.min(
        Math.max(vp.offsetLeft + marginX, r.right - width),
        vp.offsetLeft + vp.width - width - marginX,
      )
      top = r.bottom + gap
      if (top + height > vp.offsetTop + vp.height - marginBottom) {
        top = Math.max(vp.offsetTop + marginTop, r.top - height - gap)
      }
    }

    if (height > vp.height - marginTop - marginBottom) {
      top = vp.offsetTop + marginTop
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
    const onScroll = () => place()
    const vv = window.visualViewport
    window.addEventListener('keydown', onKey)
    window.addEventListener('resize', onScroll)
    window.addEventListener('scroll', onScroll, true)
    vv?.addEventListener('resize', onScroll)
    vv?.addEventListener('scroll', onScroll)
    return () => {
      window.removeEventListener('keydown', onKey)
      window.removeEventListener('resize', onScroll)
      window.removeEventListener('scroll', onScroll, true)
      vv?.removeEventListener('resize', onScroll)
      vv?.removeEventListener('scroll', onScroll)
    }
  }, [open, place])

  useFocusTrap(open, panelRef, btnRef)

  const close = () => setOpen(false)

  return (
    <div className="hint-wrap" ref={rootRef}>
      <button
        ref={btnRef}
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
          <>
            <button
              type="button"
              className="overlay-backdrop"
              aria-label="Close hint"
              tabIndex={-1}
              onClick={close}
            />
            <div
              id={tipId}
              ref={panelRef}
              className={`hint-popover${wide ? ' is-wide' : ''}`}
              role="dialog"
              aria-modal="true"
              aria-label={title}
              tabIndex={-1}
              style={{ top: pos.top, left: pos.left }}
              onClick={(e) => e.stopPropagation()}
            >
              <p className="hint-popover-title">{title}</p>
              {children}
            </div>
          </>,
          document.body,
        )}
    </div>
  )
}
