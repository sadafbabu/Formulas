import { useState } from 'react'

interface CopyLatexBtnProps {
  latex: string
}

export function CopyLatexBtn({ latex }: CopyLatexBtnProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = (e: React.MouseEvent) => {
    e.stopPropagation()
    navigator.clipboard.writeText(latex)
    setCopied(true)
    setTimeout(() => setCopied(false), 1800)
  }

  return (
    <div className="hint-wrap">
      <button
        type="button"
        className={`hint-btn${copied ? ' is-copied' : ''}`}
        aria-label="Copy LaTeX code"
        title={copied ? 'কপি হয়েছে!' : 'LaTeX কোড কপি করুন'}
        onClick={handleCopy}
      >
        {copied ? (
          <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="#22c55e" strokeWidth="2.5" strokeLinecap="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
        ) : (
          <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
          </svg>
        )}
      </button>
    </div>
  )
}
