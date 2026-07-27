interface FormulaDiagramProps {
  id: string
}

export function FormulaDiagram({ id }: FormulaDiagramProps) {
  switch (id) {
    case 'biot-savart':
    case 'wire-field':
      return (
        <svg
          viewBox="0 0 180 95"
          className="formula-diagram"
          aria-label="Straight wire magnetic field diagram"
        >
          <title>Straight Wire Magnetic Field (ঋজু তারের চৌম্বক ক্ষেত্র)</title>
          {/* Wire */}
          <line x1="90" y1="8" x2="90" y2="88" stroke="#ef4444" strokeWidth="4" strokeLinecap="round" />
          {/* Current Arrow */}
          <path d="M 90 22 L 90 12 L 85 18 M 90 12 L 95 18" stroke="#ef4444" strokeWidth="2.5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          <text x="100" y="20" fill="#ef4444" fontSize="11" fontWeight="700">I (তড়িৎপ্রবাহ)</text>

          {/* Magnetic Field Circles */}
          <ellipse cx="90" cy="50" rx="38" ry="16" fill="none" stroke="#38bdf8" strokeWidth="1.8" strokeDasharray="4 2" opacity="0.6" />
          <ellipse cx="90" cy="50" rx="65" ry="26" fill="none" stroke="#38bdf8" strokeWidth="2" />
          
          {/* B Arrow */}
          <path d="M 155 50 L 155 42 L 150 47" stroke="#38bdf8" strokeWidth="2.5" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          <text x="120" y="76" fill="#38bdf8" fontSize="11" fontWeight="700">B (চৌম্বক ক্ষেত্র)</text>

          {/* Distance r */}
          <line x1="90" y1="50" x2="155" y2="50" stroke="#f59e0b" strokeWidth="1.5" strokeDasharray="3 2" />
          <text x="118" y="44" fill="#f59e0b" fontSize="10" fontWeight="600">r</text>
        </svg>
      )

    case 'loop-center':
    case 'loop-axis':
      return (
        <svg
          viewBox="0 0 180 95"
          className="formula-diagram"
          aria-label="Circular coil magnetic field diagram"
        >
          <title>Circular Coil Axis (কুণ্ডলীর অক্ষীয় ক্ষেত্র)</title>
          {/* Loop Ellipse */}
          <ellipse cx="55" cy="48" rx="22" ry="38" fill="none" stroke="#e2e8f0" strokeWidth="3" />
          <path d="M 55 86 L 60 83 L 55 79" stroke="#ef4444" strokeWidth="2.5" fill="none" strokeLinecap="round" />
          <text x="42" y="92" fill="#ef4444" fontSize="10" fontWeight="700">I</text>

          {/* Radius a */}
          <line x1="55" y1="48" x2="55" y2="10" stroke="#f59e0b" strokeWidth="2" />
          <text x="60" y="28" fill="#f59e0b" fontSize="10" fontWeight="700">a (ব্যাসার্ধ)</text>

          {/* Axis line */}
          <line x1="15" y1="48" x2="165" y2="48" stroke="#64748b" strokeWidth="1.5" strokeDasharray="4 3" />

          {/* Magnetic Field Vector B */}
          <line x1="55" y1="48" x2="150" y2="48" stroke="#38bdf8" strokeWidth="2.8" />
          <path d="M 150 48 L 140 43 M 150 48 L 140 53" stroke="#38bdf8" strokeWidth="2.8" fill="none" strokeLinecap="round" />
          <text x="145" y="40" fill="#38bdf8" fontSize="12" fontWeight="700">B</text>

          <text x="95" y="62" fill="#94a3b8" fontSize="10">x (দূরত্ব)</text>
        </svg>
      )

    case 'solenoid':
    case 'toroid':
      return (
        <svg
          viewBox="0 0 180 95"
          className="formula-diagram"
          aria-label="Solenoid magnetic field diagram"
        >
          <title>Solenoid (সোলেনয়েড)</title>
          {/* Helical Coil */}
          <path
            d="M 20 30 Q 32 10 44 30 Q 56 50 68 30 Q 80 10 92 30 Q 104 50 116 30 Q 128 10 140 30 Q 152 50 164 30"
            fill="none"
            stroke="#e2e8f0"
            strokeWidth="3"
            strokeLinecap="round"
          />
          {/* Uniform Field B Lines Inside */}
          <line x1="15" y1="52" x2="160" y2="52" stroke="#38bdf8" strokeWidth="2.2" />
          <path d="M 160 52 L 150 47 M 160 52 L 150 57" stroke="#38bdf8" strokeWidth="2.2" fill="none" />

          <line x1="15" y1="64" x2="160" y2="64" stroke="#38bdf8" strokeWidth="2.2" opacity="0.8" />
          <path d="M 160 64 L 150 59 M 160 64 L 150 69" stroke="#38bdf8" strokeWidth="2.2" fill="none" opacity="0.8" />

          <text x="162" y="60" fill="#38bdf8" fontSize="11" fontWeight="700">B</text>
          <text x="35" y="86" fill="#ef4444" fontSize="10" fontWeight="700">B = μ₀nI (সুষম ক্ষেত্র)</text>
        </svg>
      )

    case 'lorentz':
    case 'force-on-wire':
    case 'parallel-wires':
      return (
        <svg
          viewBox="0 0 180 95"
          className="formula-diagram"
          aria-label="Lorentz force diagram"
        >
          <title>Lorentz Force (লরেঞ্জ বল)</title>
          {/* Inward Magnetic Field Crosses B */}
          {[25, 75, 125, 160].map((x) =>
            [22, 58].map((y) => (
              <g key={`${x}-${y}`} stroke="#38bdf8" strokeWidth="1.5" opacity="0.35">
                <line x1={x - 4} y1={y - 4} x2={x + 4} y2={y + 4} />
                <line x1={x + 4} y1={y - 4} x2={x - 4} y2={y + 4} />
              </g>
            ))
          )}
          {/* Curved trajectory */}
          <path d="M 20 75 Q 85 75 110 25" fill="none" stroke="#a855f7" strokeWidth="2.8" />
          {/* Charge Particle */}
          <circle cx="78" cy="60" r="7.5" fill="#a855f7" stroke="#ffffff" strokeWidth="1.5" />
          <text x="74" y="64" fill="#ffffff" fontSize="10" fontWeight="800">+</text>
          
          {/* Velocity v Arrow */}
          <line x1="78" y1="60" x2="115" y2="48" stroke="#38bdf8" strokeWidth="2" />
          <path d="M 115 48 L 107 47 M 115 48 L 109 54" stroke="#38bdf8" strokeWidth="2" fill="none" />
          <text x="118" y="46" fill="#38bdf8" fontSize="10" fontWeight="700">v (বেগ)</text>

          {/* Force F Arrow */}
          <line x1="78" y1="60" x2="55" y2="30" stroke="#ef4444" strokeWidth="2.5" />
          <path d="M 55 30 L 63 34 M 55 30 L 57 40" stroke="#ef4444" strokeWidth="2.5" fill="none" strokeLinecap="round" />
          <text x="35" y="26" fill="#ef4444" fontSize="11" fontWeight="800">F_m (বল)</text>
        </svg>
      )

    case 'cyclotron-radius':
    case 'cyclotron-freq':
    case 'moving-charge-energy':
      return (
        <svg
          viewBox="0 0 180 95"
          className="formula-diagram"
          aria-label="Cyclotron orbit diagram"
        >
          <title>Cyclotron Orbit (সাইক্লোট্রন ঘূর্ণন পথ)</title>
          {/* Circular Orbit */}
          <circle cx="90" cy="48" r="32" fill="none" stroke="#a855f7" strokeWidth="2.5" strokeDasharray="5 3" />
          <circle cx="90" cy="48" r="3.5" fill="#38bdf8" />
          
          {/* Radius Arrow */}
          <line x1="90" y1="48" x2="122" y2="48" stroke="#f59e0b" strokeWidth="2.2" />
          <path d="M 122 48 L 114 44 M 122 48 L 114 52" stroke="#f59e0b" strokeWidth="2.2" fill="none" />
          <text x="100" y="43" fill="#f59e0b" fontSize="11" fontWeight="700">r (ব্যাসার্ধ)</text>

          {/* Velocity Vector Tangent */}
          <line x1="122" y1="48" x2="122" y2="14" stroke="#ef4444" strokeWidth="2.2" />
          <path d="M 122 14 L 117 22 M 122 14 L 127 22" stroke="#ef4444" strokeWidth="2.2" fill="none" />
          <text x="130" y="22" fill="#ef4444" fontSize="11" fontWeight="700">v</text>

          <text x="25" y="88" fill="#94a3b8" fontSize="10" fontWeight="600">r = mv / qB</text>
        </svg>
      )

    case 'galvanometer-ammeter':
      return (
        <svg
          viewBox="0 0 180 95"
          className="formula-diagram"
          aria-label="Ammeter shunt circuit diagram"
        >
          <title>Ammeter Shunt Circuit (অ্যামিটার শাণ্ট বর্তনী)</title>
          {/* Main wire */}
          <line x1="10" y1="48" x2="40" y2="48" stroke="#e2e8f0" strokeWidth="2.5" />
          <line x1="140" y1="48" x2="170" y2="48" stroke="#e2e8f0" strokeWidth="2.5" />
          
          {/* Branch Top (Galvanometer G) */}
          <path d="M 40 48 L 40 24 L 62 24" stroke="#e2e8f0" strokeWidth="2" fill="none" />
          <path d="M 118 24 L 140 24 L 140 48" stroke="#e2e8f0" strokeWidth="2" fill="none" />
          <circle cx="90" cy="24" r="16" fill="#1e293b" stroke="#38bdf8" strokeWidth="2.5" />
          <text x="84" y="30" fill="#38bdf8" fontSize="14" fontWeight="800">G</text>
          <text x="45" y="18" fill="#38bdf8" fontSize="10" fontWeight="700">Ig</text>

          {/* Branch Bottom (Shunt S) */}
          <path d="M 40 48 L 40 72 L 62 72" stroke="#e2e8f0" strokeWidth="2" fill="none" />
          <path d="M 118 72 L 140 72 L 140 48" stroke="#e2e8f0" strokeWidth="2" fill="none" />
          <rect x="62" y="63" width="56" height="18" rx="4" fill="#1e293b" stroke="#ef4444" strokeWidth="2.5" />
          <text x="73" y="76" fill="#ef4444" fontSize="11" fontWeight="800">Shunt S</text>

          <text x="14" y="38" fill="#e2e8f0" fontSize="10" fontWeight="700">I (মোট)</text>
        </svg>
      )

    case 'galvanometer-voltmeter':
      return (
        <svg
          viewBox="0 0 180 95"
          className="formula-diagram"
          aria-label="Voltmeter series resistance circuit diagram"
        >
          <title>Voltmeter Circuit (ভোল্টমিটার বর্তনী)</title>
          {/* Series wire */}
          <line x1="10" y1="42" x2="40" y2="42" stroke="#e2e8f0" strokeWidth="2.5" />
          <line x1="80" y1="42" x2="105" y2="42" stroke="#e2e8f0" strokeWidth="2.5" />
          <line x1="155" y1="42" x2="170" y2="42" stroke="#e2e8f0" strokeWidth="2.5" />

          {/* Galvanometer G */}
          <circle cx="60" cy="42" r="16" fill="#1e293b" stroke="#38bdf8" strokeWidth="2.5" />
          <text x="54" y="48" fill="#38bdf8" fontSize="14" fontWeight="800">G</text>

          {/* Series High Resistance R */}
          <rect x="105" y="32" width="50" height="20" rx="4" fill="#1e293b" stroke="#f59e0b" strokeWidth="2.5" />
          <text x="115" y="46" fill="#f59e0b" fontSize="11" fontWeight="800">উচ্চ R</text>

          {/* Voltage Bracket */}
          <path d="M 20 68 L 20 74 L 160 74 L 160 68" stroke="#94a3b8" strokeWidth="1.5" fill="none" />
          <text x="75" y="88" fill="#94a3b8" fontSize="10" fontWeight="700">মোট বিভব V</text>
        </svg>
      )

    case 'earth-magnetism':
      return (
        <svg
          viewBox="0 0 180 95"
          className="formula-diagram"
          aria-label="Earth magnetism components diagram"
        >
          <title>Earth Magnetism (ভূ-চৌম্বক উপাংশ)</title>
          {/* Axis lines */}
          <line x1="30" y1="20" x2="155" y2="20" stroke="#64748b" strokeWidth="1.5" strokeDasharray="3 2" />
          <line x1="30" y1="20" x2="30" y2="78" stroke="#64748b" strokeWidth="1.5" strokeDasharray="3 2" />

          {/* Total Field B Vector */}
          <line x1="30" y1="20" x2="135" y2="68" stroke="#a855f7" strokeWidth="3" />
          <path d="M 135 68 L 125 63 M 135 68 L 128 73" stroke="#a855f7" strokeWidth="3" fill="none" strokeLinecap="round" />
          <text x="142" y="74" fill="#a855f7" fontSize="12" fontWeight="800">B (মোট)</text>

          {/* Horizontal Component BH */}
          <line x1="30" y1="20" x2="135" y2="20" stroke="#38bdf8" strokeWidth="2.5" />
          <path d="M 135 20 L 127 16 M 135 20 L 127 24" stroke="#38bdf8" strokeWidth="2.5" fill="none" />
          <text x="75" y="14" fill="#38bdf8" fontSize="11" fontWeight="700">B_H (অনুভূমিক)</text>

          {/* Vertical Component BV */}
          <line x1="30" y1="20" x2="30" y2="68" stroke="#ef4444" strokeWidth="2.5" />
          <path d="M 30 68 L 26 60 M 30 68 L 34 60" stroke="#ef4444" strokeWidth="2.5" fill="none" />
          <text x="5" y="48" fill="#ef4444" fontSize="10" fontWeight="700">B_V</text>

          {/* Dip angle delta */}
          <path d="M 60 20 A 30 30 0 0 1 54 31" fill="none" stroke="#f59e0b" strokeWidth="2" />
          <text x="64" y="34" fill="#f59e0b" fontSize="11" fontWeight="800">δ (বিনতি)</text>
        </svg>
      )

    default:
      return null
  }
}
