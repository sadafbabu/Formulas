import type { Formula } from '../data/types'
import { HintPopover } from './HintPopover'
import { Katex } from './Katex'

interface QuestionHintProps {
  formula: Formula
}

export function QuestionHint({ formula }: QuestionHintProps) {
  const qList = formula.questions ?? [
    {
      examType: 'BUET / Eng Admission Hard',
      question: `${formula.titleBn} সংক্রান্ত গাণিতিক প্রশ্ন: একটি ৫ A প্রবাহের তারের ক্ষেত্রে মূল সূত্রের প্রয়োগ নিরূপণ করো।`,
      answer: `সূত্র: ${formula.latex} এ মান বসিয়ে মান নির্ণয় করা যায়।`,
    },
  ]

  return (
    <HintPopover
      label="নমুনা প্রশ্ন ও সমাধান"
      title={`নমুনা প্রশ্ন ও সমাধান: ${formula.titleBn}`}
      icon={
        <svg
          viewBox="0 0 24 24"
          width="14"
          height="14"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.2"
          strokeLinecap="round"
          strokeLinejoin="round"
          aria-hidden="true"
        >
          <circle cx="12" cy="12" r="10" />
          <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" />
          <line x1="12" y1="17" x2="12.01" y2="17" />
        </svg>
      }
      wide
    >
      <div className="question-popover-content">
        {qList.map((q, i) => (
          <div key={i} className="question-card">
            <span className="question-exam-tag">{q.examType}</span>
            <div className="question-problem">
              <strong>🎯 প্রশ্ন:</strong>
              <p>{q.question}</p>
            </div>
            <div className="question-solution">
              <strong>💡 সমাধান:</strong>
              <div className="question-solution-text">
                <Katex latex={q.answer} display />
              </div>
            </div>
          </div>
        ))}
      </div>
    </HintPopover>
  )
}
