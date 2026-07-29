/** Read CSS env() safe-area insets in CSS pixels (fallback 0). */
export function readSafeInsets() {
  if (typeof window === 'undefined' || typeof getComputedStyle === 'undefined') {
    return { top: 0, right: 0, bottom: 0, left: 0 }
  }
  const probe = document.createElement('div')
  probe.style.cssText =
    'position:fixed;top:0;left:0;visibility:hidden;pointer-events:none;' +
    'padding-top:env(safe-area-inset-top,0px);' +
    'padding-right:env(safe-area-inset-right,0px);' +
    'padding-bottom:env(safe-area-inset-bottom,0px);' +
    'padding-left:env(safe-area-inset-left,0px);'
  document.body.appendChild(probe)
  const cs = getComputedStyle(probe)
  const top = Number.parseFloat(cs.paddingTop) || 0
  const right = Number.parseFloat(cs.paddingRight) || 0
  const bottom = Number.parseFloat(cs.paddingBottom) || 0
  const left = Number.parseFloat(cs.paddingLeft) || 0
  probe.remove()
  return { top, right, bottom, left }
}

export function viewportBox() {
  const vv = window.visualViewport
  if (vv) {
    return {
      width: vv.width,
      height: vv.height,
      offsetTop: vv.offsetTop,
      offsetLeft: vv.offsetLeft,
    }
  }
  return {
    width: window.innerWidth,
    height: window.innerHeight,
    offsetTop: 0,
    offsetLeft: 0,
  }
}
