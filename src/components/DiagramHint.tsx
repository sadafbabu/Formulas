import { FormulaDiagram } from './FormulaDiagram'
import { HintPopover } from './HintPopover'

interface DiagramHintProps {
  formulaId: string
  titleBn: string
}

export function DiagramHint({ formulaId, titleBn }: DiagramHintProps) {
  return (
    <HintPopover
      label="চিত্র দেখুন"
      title={`চিত্র ডায়াগ্রাম: ${titleBn}`}
      icon={
        <svg
          viewBox="0 0 24 24"
          width="15"
          height="15"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
          <circle cx="8.5" cy="8.5" r="1.5" />
          <polyline points="21 15 16 10 5 21" />
        </svg>
      }
      wide
    >
      <div className="diagram-popover-content">
        <FormulaDiagram id={formulaId} />
      </div>
    </HintPopover>
  )
}
