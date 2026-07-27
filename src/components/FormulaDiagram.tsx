interface FormulaDiagramProps {
  id: string
}

export function FormulaDiagram({ id }: FormulaDiagramProps) {
  switch (id) {
    case 'biot-savart':
    case 'wire-field':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Straight wire field">
          <title>Straight Wire Magnetic Field (ঋজু তারের চৌম্বক ক্ষেত্র)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <line x1="100" y1="10" x2="100" y2="100" stroke="#ef4444" strokeWidth="4.5" strokeLinecap="round" />
          <path d="M 100 24 L 100 12 L 94 20 M 100 12 L 106 20" stroke="#ef4444" strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          <text x="112" y="22" fill="#ef4444" fontSize="12" fontWeight="800">I (প্রবাহ)</text>
          <ellipse cx="100" cy="60" rx="42" ry="18" fill="none" stroke="#38bdf8" strokeWidth="2" strokeDasharray="5 3" opacity="0.65" />
          <ellipse cx="100" cy="60" rx="72" ry="30" fill="none" stroke="#38bdf8" strokeWidth="2.2" />
          <path d="M 172 60 L 172 50 L 166 56" stroke="#38bdf8" strokeWidth="3" fill="none" strokeLinecap="round" strokeLinejoin="round" />
          <text x="135" y="92" fill="#38bdf8" fontSize="12" fontWeight="800">B (ক্ষেত্র)</text>
          <line x1="100" y1="60" x2="172" y2="60" stroke="#f59e0b" strokeWidth="2" strokeDasharray="3 2" />
          <circle cx="172" cy="60" r="3" fill="#f59e0b" />
          <text x="130" y="54" fill="#f59e0b" fontSize="11" fontWeight="700">r (দূরত্ব)</text>
        </svg>
      )

    case 'straight-wire-finite':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Finite wire field">
          <title>Finite Wire Magnetic Field (সসীম তারের চৌম্বক ক্ষেত্র)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <line x1="60" y1="20" x2="60" y2="90" stroke="#ef4444" strokeWidth="4" />
          <circle cx="140" cy="55" r="4" fill="#38bdf8" />
          <line x1="60" y1="55" x2="140" y2="55" stroke="#f59e0b" strokeWidth="2" strokeDasharray="3 2" />
          <line x1="60" y1="20" x2="140" y2="55" stroke="#a855f7" strokeWidth="1.8" />
          <line x1="60" y1="90" x2="140" y2="55" stroke="#a855f7" strokeWidth="1.8" />
          <text x="75" y="38" fill="#a855f7" fontSize="10" fontWeight="700">ϕ₁</text>
          <text x="75" y="80" fill="#a855f7" fontSize="10" fontWeight="700">ϕ₂</text>
          <text x="90" y="50" fill="#f59e0b" fontSize="11" fontWeight="700">r</text>
          <text x="145" y="59" fill="#38bdf8" fontSize="12" fontWeight="800">B</text>
        </svg>
      )

    case 'loop-center':
    case 'loop-axis':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Circular coil field">
          <title>Circular Coil Axis (কুণ্ডলীর অক্ষীয় ক্ষেত্র)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <ellipse cx="60" cy="55" rx="24" ry="42" fill="none" stroke="#e2e8f0" strokeWidth="3.5" />
          <path d="M 60 97 L 66 93 L 60 88" stroke="#ef4444" strokeWidth="2.8" fill="none" strokeLinecap="round" />
          <text x="46" y="104" fill="#ef4444" fontSize="11" fontWeight="800">I</text>
          <line x1="60" y1="55" x2="60" y2="13" stroke="#f59e0b" strokeWidth="2.2" />
          <circle cx="60" cy="13" r="3" fill="#f59e0b" />
          <text x="66" y="32" fill="#f59e0b" fontSize="11" fontWeight="700">a (ব্যাসার্ধ)</text>
          <line x1="15" y1="55" x2="185" y2="55" stroke="#64748b" strokeWidth="1.5" strokeDasharray="4 3" />
          <line x1="60" y1="55" x2="168" y2="55" stroke="#38bdf8" strokeWidth="3" />
          <path d="M 168 55 L 157 49 M 168 55 L 157 61" stroke="#38bdf8" strokeWidth="3" fill="none" strokeLinecap="round" />
          <text x="160" y="44" fill="#38bdf8" fontSize="13" fontWeight="800">B</text>
          <text x="105" y="70" fill="#94a3b8" fontSize="11" fontWeight="600">x (অক্ষীয় দূরত্ব)</text>
        </svg>
      )

    case 'arc-center':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Circular Arc field">
          <title>Circular Arc Center (বৃত্তাকার চাপের কেন্দ্র)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <path d="M 60 90 A 45 45 0 0 1 140 90" fill="none" stroke="#e2e8f0" strokeWidth="3.5" />
          <circle cx="100" cy="50" r="4" fill="#38bdf8" />
          <line x1="100" y1="50" x2="60" y2="90" stroke="#f59e0b" strokeWidth="2" strokeDasharray="3 2" />
          <line x1="100" y1="50" x2="140" y2="90" stroke="#f59e0b" strokeWidth="2" strokeDasharray="3 2" />
          <path d="M 85 65 A 20 20 0 0 1 115 65" fill="none" stroke="#a855f7" strokeWidth="2" />
          <text x="96" y="76" fill="#a855f7" fontSize="11" fontWeight="800">θ</text>
          <text x="70" y="62" fill="#f59e0b" fontSize="10" fontWeight="700">r</text>
          <text x="95" y="42" fill="#38bdf8" fontSize="12" fontWeight="800">B</text>
        </svg>
      )

    case 'solenoid':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Solenoid field">
          <title>Solenoid (সোলেনয়েড)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <path d="M 20 35 Q 35 12 50 35 Q 65 58 80 35 Q 95 12 110 35 Q 125 58 140 35 Q 155 12 170 35" fill="none" stroke="#e2e8f0" strokeWidth="3.2" strokeLinecap="round" />
          <line x1="15" y1="60" x2="180" y2="60" stroke="#38bdf8" strokeWidth="2.5" />
          <path d="M 180 60 L 168 54 M 180 60 L 168 66" stroke="#38bdf8" strokeWidth="2.5" fill="none" />
          <text x="165" y="48" fill="#38bdf8" fontSize="12" fontWeight="800">B</text>
          <text x="35" y="98" fill="#ef4444" fontSize="11" fontWeight="700">B = μ₀nI (সুষম অভ্যন্তরীণ ক্ষেত্র)</text>
        </svg>
      )

    case 'toroid':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Toroid field">
          <title>Toroid (টরয়েড)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <circle cx="100" cy="55" r="42" fill="none" stroke="#e2e8f0" strokeWidth="3" />
          <circle cx="100" cy="55" r="24" fill="none" stroke="#e2e8f0" strokeWidth="2.5" />
          <circle cx="100" cy="55" r="33" fill="none" stroke="#38bdf8" strokeWidth="2.2" strokeDasharray="6 3" />
          <path d="M 100 22 L 106 25 L 100 28" stroke="#38bdf8" strokeWidth="2.5" fill="none" strokeLinecap="round" />
          <text x="110" y="20" fill="#38bdf8" fontSize="11" fontWeight="800">B (আবদ্ধ)</text>
          <text x="35" y="100" fill="#ef4444" fontSize="10" fontWeight="700">B = μ₀NI / 2πr</text>
        </svg>
      )

    case 'lorentz':
    case 'force-on-wire':
    case 'parallel-wires':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Lorentz force">
          <title>Lorentz Force (লরেঞ্জ বল)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          {[30, 85, 140, 175].map((x) =>
            [25, 65, 95].map((y) => (
              <g key={`${x}-${y}`} stroke="#38bdf8" strokeWidth="1.5" opacity="0.35">
                <line x1={x - 4} y1={y - 4} x2={x + 4} y2={y + 4} />
                <line x1={x + 4} y1={y - 4} x2={x - 4} y2={y + 4} />
              </g>
            ))
          )}
          <path d="M 20 85 Q 95 85 125 25" fill="none" stroke="#a855f7" strokeWidth="3" />
          <circle cx="86" cy="68" r="8.5" fill="#a855f7" stroke="#ffffff" strokeWidth="1.8" />
          <text x="82" y="72" fill="#ffffff" fontSize="11" fontWeight="800">+</text>
          <line x1="86" y1="68" x2="130" y2="54" stroke="#38bdf8" strokeWidth="2.5" />
          <path d="M 130 54 L 120 53 M 130 54 L 123 61" stroke="#38bdf8" strokeWidth="2.5" fill="none" />
          <text x="135" y="52" fill="#38bdf8" fontSize="11" fontWeight="800">v (বেগ)</text>
          <line x1="86" y1="68" x2="60" y2="34" stroke="#ef4444" strokeWidth="3" />
          <path d="M 60 34 L 69 38 M 60 34 L 63 45" stroke="#ef4444" strokeWidth="3" fill="none" strokeLinecap="round" />
          <text x="38" y="28" fill="#ef4444" fontSize="12" fontWeight="800">F_m (লরেঞ্জ বল)</text>
        </svg>
      )

    case 'cyclotron-radius':
    case 'cyclotron-freq':
    case 'moving-charge-energy':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Cyclotron orbit">
          <title>Cyclotron Orbit (সাইক্লোট্রন ঘূর্ণন পথ)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <circle cx="100" cy="55" r="36" fill="none" stroke="#a855f7" strokeWidth="2.8" strokeDasharray="6 3" />
          <circle cx="100" cy="55" r="4" fill="#38bdf8" />
          <line x1="100" y1="55" x2="136" y2="55" stroke="#f59e0b" strokeWidth="2.5" />
          <path d="M 136 55 L 126 50 M 136 55 L 126 60" stroke="#f59e0b" strokeWidth="2.5" fill="none" />
          <text x="110" y="48" fill="#f59e0b" fontSize="12" fontWeight="800">r</text>
          <line x1="136" y1="55" x2="136" y2="16" stroke="#ef4444" strokeWidth="2.5" />
          <path d="M 136 16 L 130 25 M 136 16 L 142 25" stroke="#ef4444" strokeWidth="2.5" fill="none" />
          <text x="144" y="26" fill="#ef4444" fontSize="12" fontWeight="800">v</text>
          <text x="25" y="100" fill="#94a3b8" fontSize="11" fontWeight="700">r = mv / qB</text>
        </svg>
      )

    case 'velocity-selector':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Velocity Selector">
          <title>Velocity Selector (বেগ নির্বাচক)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <line x1="15" y1="55" x2="185" y2="55" stroke="#22c55e" strokeWidth="3" />
          <path d="M 185 55 L 175 50 M 185 55 L 175 60" stroke="#22c55e" strokeWidth="3" fill="none" />
          <line x1="100" y1="55" x2="100" y2="15" stroke="#ef4444" strokeWidth="2.5" />
          <text x="105" y="25" fill="#ef4444" fontSize="11" fontWeight="800">F_e = qE</text>
          <line x1="100" y1="55" x2="100" y2="95" stroke="#38bdf8" strokeWidth="2.5" />
          <text x="105" y="90" fill="#38bdf8" fontSize="11" fontWeight="800">F_m = qvB</text>
          <text x="20" y="45" fill="#22c55e" fontSize="12" fontWeight="800">v = E / B</text>
        </svg>
      )

    case 'galvanometer-ammeter':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Ammeter shunt">
          <title>Ammeter Shunt (অ্যামিটার শাণ্ট)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <line x1="15" y1="55" x2="45" y2="55" stroke="#e2e8f0" strokeWidth="3" />
          <line x1="155" y1="55" x2="185" y2="55" stroke="#e2e8f0" strokeWidth="3" />
          <path d="M 45 55 L 45 28 L 70 28" stroke="#e2e8f0" strokeWidth="2.2" fill="none" />
          <path d="M 130 28 L 155 28 L 155 55" stroke="#e2e8f0" strokeWidth="2.2" fill="none" />
          <circle cx="100" cy="28" r="18" fill="#1e293b" stroke="#38bdf8" strokeWidth="3" />
          <text x="94" y="34" fill="#38bdf8" fontSize="15" fontWeight="800">G</text>
          <path d="M 45 55 L 45 82 L 70 82" stroke="#e2e8f0" strokeWidth="2.2" fill="none" />
          <path d="M 130 82 L 155 82 L 155 55" stroke="#e2e8f0" strokeWidth="2.2" fill="none" />
          <rect x="70" y="72" width="60" height="20" rx="4" fill="#1e293b" stroke="#ef4444" strokeWidth="3" />
          <text x="82" y="86" fill="#ef4444" fontSize="12" fontWeight="800">Shunt S</text>
          <text x="18" y="44" fill="#e2e8f0" fontSize="11" fontWeight="700">I</text>
        </svg>
      )

    case 'galvanometer-voltmeter':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Voltmeter">
          <title>Voltmeter Circuit (ভোল্টমিটার)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <line x1="15" y1="48" x2="45" y2="48" stroke="#e2e8f0" strokeWidth="3" />
          <line x1="90" y1="48" x2="115" y2="48" stroke="#e2e8f0" strokeWidth="3" />
          <line x1="170" y1="48" x2="185" y2="48" stroke="#e2e8f0" strokeWidth="3" />
          <circle cx="68" cy="48" r="18" fill="#1e293b" stroke="#38bdf8" strokeWidth="3" />
          <text x="62" y="54" fill="#38bdf8" fontSize="15" fontWeight="800">G</text>
          <rect x="115" y="37" width="55" height="22" rx="4" fill="#1e293b" stroke="#f59e0b" strokeWidth="3" />
          <text x="126" y="52" fill="#f59e0b" fontSize="12" fontWeight="800">উচ্চ R</text>
          <path d="M 25 76 L 25 82 L 175 82 L 175 76" stroke="#94a3b8" strokeWidth="1.8" fill="none" />
          <text x="82" y="98" fill="#94a3b8" fontSize="11" fontWeight="800">মোট বিভব V</text>
        </svg>
      )

    case 'tangent-galvanometer':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Tangent Galvanometer">
          <title>Tangent Galvanometer (ট্যানজেন্ট গ্যালভানোমিটার)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <circle cx="100" cy="55" r="38" fill="none" stroke="#e2e8f0" strokeWidth="3.5" />
          <line x1="100" y1="17" x2="100" y2="93" stroke="#38bdf8" strokeWidth="2.5" strokeDasharray="3 2" />
          <line x1="62" y1="55" x2="138" y2="55" stroke="#ef4444" strokeWidth="2.5" strokeDasharray="3 2" />
          <line x1="100" y1="55" x2="130" y2="25" stroke="#a855f7" strokeWidth="3" />
          <path d="M 130 25 L 122 28 M 130 25 L 127 33" stroke="#a855f7" strokeWidth="3" fill="none" />
          <text x="110" y="42" fill="#f59e0b" fontSize="11" fontWeight="800">θ</text>
          <text x="14" y="98" fill="#38bdf8" fontSize="11" fontWeight="700">I = K tanθ</text>
        </svg>
      )

    case 'earth-magnetism':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Earth magnetism">
          <title>Earth Magnetism (ভূ-চৌম্বক উপাংশ)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <line x1="35" y1="25" x2="175" y2="25" stroke="#64748b" strokeWidth="1.8" strokeDasharray="3 2" />
          <line x1="35" y1="25" x2="35" y2="90" stroke="#64748b" strokeWidth="1.8" strokeDasharray="3 2" />
          <line x1="35" y1="25" x2="150" y2="78" stroke="#a855f7" strokeWidth="3.2" />
          <path d="M 150 78 L 138 72 M 150 78 L 142 83" stroke="#a855f7" strokeWidth="3.2" fill="none" strokeLinecap="round" />
          <text x="156" y="84" fill="#a855f7" fontSize="13" fontWeight="800">B</text>
          <line x1="35" y1="25" x2="150" y2="25" stroke="#38bdf8" strokeWidth="2.8" />
          <text x="85" y="18" fill="#38bdf8" fontSize="12" fontWeight="800">B_H (অনুভূমিক)</text>
          <line x1="35" y1="25" x2="35" y2="78" stroke="#ef4444" strokeWidth="2.8" />
          <text x="5" y="55" fill="#ef4444" fontSize="11" fontWeight="800">B_V</text>
          <text x="72" y="42" fill="#f59e0b" fontSize="12" fontWeight="800">δ (বিনতি)</text>
        </svg>
      )

    case 'bar-magnet-field':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Bar magnet">
          <title>Bar Magnet Field (দণ্ড চুম্বক ক্ষেত্র)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <rect x="50" y="42" width="50" height="26" fill="#ef4444" rx="2" />
          <rect x="100" y="42" width="50" height="26" fill="#38bdf8" rx="2" />
          <text x="68" y="60" fill="#ffffff" fontSize="13" fontWeight="800">N</text>
          <text x="120" y="60" fill="#ffffff" fontSize="13" fontWeight="800">S</text>
          <path d="M 40 40 Q 100 10 160 40" fill="none" stroke="#a855f7" strokeWidth="2.2" />
          <path d="M 40 70 Q 100 100 160 70" fill="none" stroke="#a855f7" strokeWidth="2.2" />
          <text x="25" y="100" fill="#f59e0b" fontSize="11" fontWeight="700">M = 2l × m</text>
        </svg>
      )

    case 'magnetic-moment':
    case 'torque-loop':
    case 'magnetic-work':
    case 'magnetic-potential-energy':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Magnetic Moment and Torque">
          <title>Magnetic Dipole & Torque (চৌম্বক দ্বিমেৰু ও টর্ক)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <polygon points="50,75 110,75 140,45 80,45" fill="rgba(56, 189, 248, 0.15)" stroke="#38bdf8" strokeWidth="2.5" />
          <text x="88" y="64" fill="#38bdf8" fontSize="11" fontWeight="700">Area A</text>
          <path d="M 125 60 L 132 53 L 124 50" stroke="#ef4444" strokeWidth="2.5" fill="none" strokeLinecap="round" />
          <text x="135" y="65" fill="#ef4444" fontSize="11" fontWeight="800">I</text>
          <line x1="95" y1="60" x2="95" y2="14" stroke="#a855f7" strokeWidth="3" />
          <path d="M 95 14 L 89 24 M 95 14 L 101 24" stroke="#a855f7" strokeWidth="3" fill="none" strokeLinecap="round" />
          <text x="104" y="24" fill="#a855f7" fontSize="13" fontWeight="800">M = NIA</text>
          <text x="15" y="100" fill="#f59e0b" fontSize="11" fontWeight="700">τ = M × B (টর্ক)</text>
        </svg>
      )

    case 'amperes-law':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Ampere Law">
          <title>Ampere's Law (অ্যাম্পিয়ারের সার্কিটাল সূত্র)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <line x1="75" y1="15" x2="75" y2="95" stroke="#ef4444" strokeWidth="3" />
          <circle cx="75" cy="55" r="4" fill="#ef4444" />
          <text x="60" y="30" fill="#ef4444" fontSize="11" fontWeight="800">I₁</text>
          <line x1="125" y1="15" x2="125" y2="95" stroke="#ef4444" strokeWidth="3" />
          <circle cx="125" cy="55" r="4" fill="#ef4444" />
          <text x="132" y="30" fill="#ef4444" fontSize="11" fontWeight="800">I₂</text>
          <ellipse cx="100" cy="55" r="55" ry="32" fill="none" stroke="#38bdf8" strokeWidth="2.8" strokeDasharray="6 3" />
          <circle cx="155" cy="55" r="3" fill="#f59e0b" />
          <line x1="155" y1="55" x2="155" y2="25" stroke="#f59e0b" strokeWidth="2.5" />
          <text x="162" y="30" fill="#f59e0b" fontSize="11" fontWeight="800">dl</text>
          <text x="35" y="100" fill="#38bdf8" fontSize="11" fontWeight="700">∮ B·dl = μ₀ I_enc</text>
        </svg>
      )

    case 'magnetic-flux':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Magnetic Flux">
          <title>Magnetic Flux (চৌম্বক ফ্লাক্স)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <polygon points="40,80 110,80 145,50 75,50" fill="rgba(56, 189, 248, 0.18)" stroke="#38bdf8" strokeWidth="2.5" />
          <text x="85" y="70" fill="#38bdf8" fontSize="11" fontWeight="700">Area A</text>
          <line x1="92" y1="65" x2="92" y2="20" stroke="#e2e8f0" strokeWidth="2" strokeDasharray="3 2" />
          <text x="80" y="18" fill="#e2e8f0" fontSize="11" fontWeight="700">n (অভিলম্ব)</text>
          {[55, 92, 130].map((x, i) => (
            <g key={i}>
              <line x1={x} y1="95" x2={x + 25} y2="15" stroke="#ef4444" strokeWidth="2.5" />
            </g>
          ))}
          <text x="160" y="24" fill="#ef4444" fontSize="12" fontWeight="800">B</text>
          <text x="25" y="102" fill="#22c55e" fontSize="11" fontWeight="700">Φ_B = B·A cosθ</text>
        </svg>
      )

    case 'hall-effect':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Hall Effect">
          <title>Hall Effect (হল প্রভাব)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <polygon points="35,65 135,65 165,40 65,40" fill="rgba(30, 41, 59, 0.9)" stroke="#e2e8f0" strokeWidth="2" />
          <polygon points="35,65 135,65 135,85 35,85" fill="rgba(15, 23, 42, 0.9)" stroke="#e2e8f0" strokeWidth="2" />
          <line x1="100" y1="95" x2="100" y2="10" stroke="#38bdf8" strokeWidth="3" />
          <text x="108" y="18" fill="#38bdf8" fontSize="12" fontWeight="800">B</text>
          <line x1="10" y1="52" x2="45" y2="52" stroke="#ef4444" strokeWidth="3" />
          <text x="12" y="44" fill="#ef4444" fontSize="11" fontWeight="800">I</text>
          <text x="12" y="98" fill="#f59e0b" fontSize="11" fontWeight="700">V_H = IB / nqd</text>
        </svg>
      )

    case 'magnetic-intensity':
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Magnetic Intensity">
          <title>Magnetic Intensity & Induction (চৌম্বক তীব্রতা ও আবেশ)</title>
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <rect x="40" y="30" width="120" height="50" rx="6" fill="rgba(51, 65, 85, 0.6)" stroke="#e2e8f0" strokeWidth="2" />
          <text x="75" y="58" fill="#e2e8f0" fontSize="11" fontWeight="700">পদার্থ (μ_r)</text>
          <line x1="15" y1="70" x2="185" y2="70" stroke="#38bdf8" strokeWidth="2.8" />
          <text x="165" y="62" fill="#38bdf8" fontSize="12" fontWeight="800">B = μH</text>
          <text x="35" y="98" fill="#22c55e" fontSize="11" fontWeight="700">μ_r = 1 + χ_m</text>
        </svg>
      )

    default:
      return (
        <svg viewBox="0 0 200 110" className="formula-diagram-svg" aria-label="Physics Diagram">
          <rect x="0" y="0" width="200" height="110" fill="#0f172a" rx="8" />
          <circle cx="100" cy="55" r="30" fill="none" stroke="#38bdf8" strokeWidth="2.5" strokeDasharray="4 2" />
          <text x="68" y="58" fill="#e2e8f0" fontSize="12" fontWeight="700">Formulas</text>
        </svg>
      )
  }
}
