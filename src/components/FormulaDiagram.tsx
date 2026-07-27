interface FormulaDiagramProps {
  id: string
}

export function FormulaDiagram({ id }: FormulaDiagramProps) {
  switch (id) {
    case 'biot-savart':
    case 'wire-field':
      return (
        <svg
          viewBox="0 0 160 80"
          className="formula-diagram"
          aria-hidden="true"
        >
          {/* Wire */}
          <line x1="80" y1="5" x2="80" y2="75" stroke="#ef4444" strokeWidth="3.5" strokeDasharray="none" strokeLinecap="round" />
          <path d="M 80 18 L 80 10 L 76 16 M 80 10 L 84 16" stroke="#ef4444" strokeWidth="2.5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          <text x="88" y="18" fill="#ef4444" fontSize="10" fontWeight="700">I</text>
          
          {/* Magnetic Field Concentric Ellipses */}
          <ellipse cx="80" cy="40" rx="35" ry="14" fill="none" stroke="#60a5fa" strokeWidth="1.8" strokeDasharray="3 2" opacity="0.6" />
          <ellipse cx="80" cy="40" rx="55" ry="22" fill="none" stroke="#60a5fa" strokeWidth="1.8" strokeDasharray="none" />
          
          {/* B Vector arrow */}
          <path d="M 135 40 L 135 34 L 131 38" stroke="#60a5fa" strokeWidth="2" fill="none" strokeLinecap="round" />
          <text x="140" y="38" fill="#60a5fa" fontSize="11" fontWeight="700">B</text>

          {/* Right Hand Rule Hand Indicator */}
          <circle cx="80" cy="40" r="3" fill="#60a5fa" />
          <text x="5" y="72" fill="#94a3b8" fontSize="8">Right-hand Rule</text>
        </svg>
      )

    case 'loop-center':
    case 'loop-axis':
      return (
        <svg
          viewBox="0 0 160 80"
          className="formula-diagram"
          aria-hidden="true"
        >
          {/* Loop Ellipse */}
          <ellipse cx="60" cy="40" rx="22" ry="32" fill="none" stroke="#e2e8f0" strokeWidth="2.5" />
          {/* Current direction */}
          <path d="M 60 72 L 64 70 L 60 66" stroke="#ef4444" strokeWidth="2" fill="none" strokeLinecap="round" />
          <text x="48" y="78" fill="#ef4444" fontSize="10" fontWeight="700">I</text>

          {/* Axis line */}
          <line x1="20" y1="40" x2="145" y2="40" stroke="#475569" strokeWidth="1.5" strokeDasharray="4 3" />

          {/* B Vector on Axis */}
          <line x1="60" y1="40" x2="135" y2="40" stroke="#60a5fa" strokeWidth="2.5" />
          <path d="M 135 40 L 127 36 M 135 40 L 127 44" stroke="#60a5fa" strokeWidth="2.5" fill="none" strokeLinecap="round" />
          <text x="138" y="36" fill="#60a5fa" fontSize="11" fontWeight="700">B</text>
          
          {/* Radius & Distance */}
          <line x1="60" y1="40" x2="60" y2="8" stroke="#38bdf8" strokeWidth="1.5" />
          <text x="64" y="24" fill="#38bdf8" fontSize="9">a</text>
          <text x="95" y="52" fill="#94a3b8" fontSize="9">x</text>
        </svg>
      )

    case 'solenoid':
    case 'toroid':
      return (
        <svg
          viewBox="0 0 160 80"
          className="formula-diagram"
          aria-hidden="true"
        >
          {/* Coils */}
          <path
            d="M 20 25 Q 30 10 40 25 Q 50 40 60 25 Q 70 10 80 25 Q 90 40 100 25 Q 110 10 120 25 Q 130 40 140 25"
            fill="none"
            stroke="#e2e8f0"
            strokeWidth="2.5"
            strokeLinecap="round"
          />
          {/* Internal B Lines */}
          <line x1="15" y1="45" x2="145" y2="45" stroke="#60a5fa" strokeWidth="2" />
          <path d="M 145 45 L 137 41 M 145 45 L 137 49" stroke="#60a5fa" strokeWidth="2" fill="none" />

          <line x1="15" y1="55" x2="145" y2="55" stroke="#60a5fa" strokeWidth="2" opacity="0.75" />
          <path d="M 145 55 L 137 51 M 145 55 L 137 59" stroke="#60a5fa" strokeWidth="2" fill="none" opacity="0.75" />

          <text x="148" y="52" fill="#60a5fa" fontSize="10" fontWeight="700">B</text>
          <text x="20" y="72" fill="#ef4444" fontSize="9" fontWeight="600">B = μ₀nI</text>
        </svg>
      )

    case 'lorentz':
    case 'force-on-wire':
    case 'parallel-wires':
      return (
        <svg
          viewBox="0 0 160 80"
          className="formula-diagram"
          aria-hidden="true"
        >
          {/* Uniform B Field Inward crosses */}
          {[30, 70, 110, 140].map((x) =>
            [20, 50].map((y) => (
              <g key={`${x}-${y}`} stroke="#60a5fa" strokeWidth="1.2" opacity="0.4">
                <line x1={x - 4} y1={y - 4} x2={x + 4} y2={y + 4} />
                <line x1={x + 4} y1={y - 4} x2={x - 4} y2={y + 4} />
              </g>
            ))
          )}
          {/* Particle trajectory curve */}
          <path d="M 20 60 Q 70 60 90 20" fill="none" stroke="#38bdf8" strokeWidth="2.5" strokeDasharray="none" />
          {/* Charge particle */}
          <circle cx="65" cy="48" r="6" fill="#a855f7" />
          <text x="62" y="51" fill="#ffffff" fontSize="8" fontWeight="700">+</text>
          
          {/* Force Vector Arrow */}
          <line x1="65" y1="48" x2="45" y2="28" stroke="#ef4444" strokeWidth="2.2" />
          <path d="M 45 28 L 51 31 M 45 28 L 47 35" stroke="#ef4444" strokeWidth="2" fill="none" />
          <text x="32" y="24" fill="#ef4444" fontSize="10" fontWeight="700">F_m</text>
        </svg>
      )

    case 'cyclotron-radius':
    case 'cyclotron-freq':
    case 'moving-charge-energy':
      return (
        <svg
          viewBox="0 0 160 80"
          className="formula-diagram"
          aria-hidden="true"
        >
          {/* Circular Orbit */}
          <circle cx="80" cy="40" r="28" fill="none" stroke="#38bdf8" strokeWidth="2" strokeDasharray="4 3" />
          <circle cx="80" cy="40" r="3" fill="#60a5fa" />
          
          {/* Radius Arrow */}
          <line x1="80" y1="40" x2="108" y2="40" stroke="#f59e0b" strokeWidth="2" />
          <path d="M 108 40 L 102 37 M 108 40 L 102 43" stroke="#f59e0b" strokeWidth="2" />
          <text x="90" y="35" fill="#f59e0b" fontSize="10" fontWeight="700">r</text>

          {/* Velocity Vector */}
          <line x1="108" y1="40" x2="108" y2="12" stroke="#ef4444" strokeWidth="2" />
          <path d="M 108 12 L 105 18 M 108 12 L 111 18" stroke="#ef4444" strokeWidth="2" fill="none" />
          <text x="114" y="20" fill="#ef4444" fontSize="10" fontWeight="700">v</text>

          <text x="10" y="74" fill="#94a3b8" fontSize="8">r = mv / qB</text>
        </svg>
      )

    case 'galvanometer-ammeter':
      return (
        <svg
          viewBox="0 0 160 80"
          className="formula-diagram"
          aria-hidden="true"
        >
          {/* Main wire */}
          <line x1="10" y1="40" x2="35" y2="40" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="125" y1="40" x2="150" y2="40" stroke="#e2e8f0" strokeWidth="2" />
          
          {/* Branch Top (Galvanometer G) */}
          <line x1="35" y1="40" x2="35" y2="20" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="125" y1="40" x2="125" y2="20" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="35" y1="20" x2="60" y2="20" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="100" y1="20" x2="125" y2="20" stroke="#e2e8f0" strokeWidth="2" />
          
          <circle cx="80" cy="20" r="14" fill="#1e293b" stroke="#38bdf8" strokeWidth="2" />
          <text x="75" y="24" fill="#38bdf8" fontSize="12" fontWeight="700">G</text>

          {/* Branch Bottom (Shunt S) */}
          <line x1="35" y1="40" x2="35" y2="60" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="125" y1="40" x2="125" y2="60" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="35" y1="60" x2="60" y2="60" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="100" y1="60" x2="125" y2="60" stroke="#e2e8f0" strokeWidth="2" />
          
          <rect x="60" y="53" width="40" height="14" rx="3" fill="#1e293b" stroke="#ef4444" strokeWidth="2" />
          <text x="76" y="64" fill="#ef4444" fontSize="10" fontWeight="700">S</text>

          {/* Current labels */}
          <text x="12" y="32" fill="#e2e8f0" fontSize="9">I</text>
          <text x="42" y="15" fill="#38bdf8" fontSize="8">Ig</text>
        </svg>
      )

    case 'galvanometer-voltmeter':
      return (
        <svg
          viewBox="0 0 160 80"
          className="formula-diagram"
          aria-hidden="true"
        >
          {/* Main Series wire */}
          <line x1="10" y1="40" x2="45" y2="40" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="75" y1="40" x2="100" y2="40" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="140" y1="40" x2="150" y2="40" stroke="#e2e8f0" strokeWidth="2" />

          {/* Galvanometer G */}
          <circle cx="60" cy="40" r="15" fill="#1e293b" stroke="#38bdf8" strokeWidth="2" />
          <text x="55" y="44" fill="#38bdf8" fontSize="12" fontWeight="700">G</text>

          {/* Series High Resistance R */}
          <rect x="100" y="32" width="40" height="16" rx="3" fill="#1e293b" stroke="#f59e0b" strokeWidth="2" />
          <text x="116" y="44" fill="#f59e0b" fontSize="11" fontWeight="700">R</text>

          {/* Voltage V Label */}
          <path d="M 20 62 L 20 66 L 140 66 L 140 62" stroke="#94a3b8" strokeWidth="1.2" fill="none" />
          <text x="75" y="76" fill="#94a3b8" fontSize="9" fontWeight="600">Total V</text>
        </svg>
      )

    case 'earth-magnetism':
      return (
        <svg
          viewBox="0 0 160 80"
          className="formula-diagram"
          aria-hidden="true"
        >
          {/* Coordinate Axes */}
          <line x1="30" y1="20" x2="140" y2="20" stroke="#475569" strokeWidth="1.5" strokeDasharray="3 2" />
          <line x1="30" y1="20" x2="30" y2="70" stroke="#475569" strokeWidth="1.5" strokeDasharray="3 2" />

          {/* Vector B Total */}
          <line x1="30" y1="20" x2="120" y2="60" stroke="#a855f7" strokeWidth="2.5" />
          <path d="M 120 60 L 112 55 M 120 60 L 114 65" stroke="#a855f7" strokeWidth="2.5" fill="none" />
          <text x="126" y="65" fill="#a855f7" fontSize="11" fontWeight="700">B</text>

          {/* Component BH */}
          <line x1="30" y1="20" x2="120" y2="20" stroke="#60a5fa" strokeWidth="2" />
          <path d="M 120 20 L 114 17 M 120 20 L 114 23" stroke="#60a5fa" strokeWidth="2" />
          <text x="70" y="15" fill="#60a5fa" fontSize="10" fontWeight="700">B_H</text>

          {/* Component BV */}
          <line x1="30" y1="20" x2="30" y2="60" stroke="#ef4444" strokeWidth="2" />
          <path d="M 30 60 L 27 54 M 30 60 L 33 54" stroke="#ef4444" strokeWidth="2" />
          <text x="12" y="45" fill="#ef4444" fontSize="10" fontWeight="700">B_V</text>

          {/* Dip Angle delta */}
          <path d="M 55 20 A 25 25 0 0 1 50 29" fill="none" stroke="#f59e0b" strokeWidth="1.8" />
          <text x="58" y="32" fill="#f59e0b" fontSize="10" fontWeight="700">δ</text>
        </svg>
      )

    default:
      return null
  }
}
