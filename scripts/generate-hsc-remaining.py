#!/usr/bin/env python3
"""Add remaining NCTB HSC syllabus chapters and formulas."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "subjects"
EXISTING = {
    p.stem
    for p in ROOT.glob("*/chapters/*/formulas/*.json")
}


def make(
    *,
    id: str,
    chapter: str,
    title: str,
    title_bn: str,
    summary: str,
    latex: str,
    importance: int = 2,
    order: int,
    trick: str,
    subject: str = "math",
    tags: list[str] | None = None,
):
    if id in EXISTING:
        raise SystemExit(f"duplicate id: {id}")
    star = f"{importance}-star"
    base_tags = tags or ["hsc", "eng-admission", "varsity", star]
    if subject == "chemistry" and "medical" not in base_tags:
        base_tags = ["hsc", "eng-admission", "medical", "varsity", star]
    if subject == "physics" and "medical" not in base_tags:
        base_tags = ["hsc", "eng-admission", "medical", "varsity", star]
    if star not in base_tags:
        base_tags = [t for t in base_tags if not t.endswith("-star")] + [star]
    return {
        "id": id,
        "chapter": chapter,
        "title": title,
        "titleBn": title_bn,
        "summary": summary,
        "latex": latex,
        "tags": base_tags,
        "importance": importance,
        "order": order,
        "symbols": [{"symbol": "—", "meaning": "প্রধান চলকসমূহ সূত্রে দ্রষ্টব্য", "unit": "—"}],
        "derivation": {
            "lead": summary,
            "steps": [
                {
                    "title": "মূল সূত্র",
                    "latex": latex,
                    "note": "HSC ও ভর্তি পরীক্ষায় সরাসরি প্রয়োগযোগ্য রূপ।",
                }
            ],
            "assumptions": [],
        },
        "questions": [
            {
                "examType": "HSC / Admission",
                "question": f"{title_bn} এর মূল সূত্রটি লেখো।",
                "answer": latex,
            }
        ],
        "memorize": {"trick": trick, "steps": []},
        "subjects": [subject],
        "related": [],
    }


def write_formula(subject: str, chapter: str, data: dict):
    out = ROOT / subject / "chapters" / chapter / "formulas"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{data['id']}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    EXISTING.add(data["id"])


def write_meta(subject: str, chapter: str, meta: dict):
    out = ROOT / subject / "chapters" / chapter
    out.mkdir(parents=True, exist_ok=True)
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ── Physics: Measurement ─────────────────────────────────────────────
MEASUREMENT = [
    make(id="dimensional-formula", chapter="measurement", title="Dimensional Formula", title_bn="মাত্রিক সূত্র", summary="[M^a L^b T^c]", latex="[Q]=\\mathrm{M}^{a}\\mathrm{L}^{b}\\mathrm{T}^{c}", order=10, trick="প্রতিটি ভৌত রাশিকে M, L, T-এর ঘাত দিয়ে লেখো।", subject="physics", importance=3),
    make(id="dimensional-homogeneity", chapter="measurement", title="Principle of Homogeneity", title_bn="মাত্রিক সমসত্ত্বতার নীতি", summary="প্রতিটি পদ একই মাত্রা", latex="[\\text{LHS}]=[\\text{RHS}]\\quad\\text{(each term)}", order=20, trick="যোগ/বিয়োগ শুধু একই মাত্রার রাশিতে; সমীকরণ যাচাইয়ে ব্যবহার।", subject="physics", importance=3),
    make(id="percentage-error", chapter="measurement", title="Percentage Error", title_bn="শতকরা ত্রুটি", summary="Δx/x × 100%", latex="\\delta x\\%=\\frac{\\Delta x}{x}\\times 100\\%", order=30, trick="আপেক্ষিক ত্রুটি × 100 = শতকরা ত্রুটি।", subject="physics", importance=3),
    make(id="error-propagation-product", chapter="measurement", title="Error in Product/Quotient", title_bn="গুণ/ভাগে ত্রুটি", summary="যোগ আপেক্ষিক ত্রুটি", latex="\\frac{\\Delta z}{z}=\\frac{\\Delta x}{x}+\\frac{\\Delta y}{y}\\quad(z=xy\\text{ বা }x/y)", order=40, trick="গুণ বা ভাগে আপেক্ষিক ত্রুটি যোগ হয়।", subject="physics", importance=2),
    make(id="error-propagation-power", chapter="measurement", title="Error in Power", title_bn="ঘাতে ত্রুটি", summary="n× relative error", latex="\\frac{\\Delta z}{z}=|n|\\frac{\\Delta x}{x}\\quad(z=x^n)", order=50, trick="ঘাত n হলে আপেক্ষিক ত্রুটি n গুণ।", subject="physics", importance=2),
    make(id="significant-figures-rule", chapter="measurement", title="Significant Figures", title_bn="সার্থক অঙ্ক", summary="নির্ভুল অঙ্ক গণনা", latex="\\text{s.f. = all certain digits + first uncertain digit}", order=60, trick="গুণে ফল = কম s.f. ওয়ালার মতো; যোগে দশমিক স্থান মেলাও।", subject="physics", importance=2),
    make(id="least-count-vernier", chapter="measurement", title="Vernier Least Count", title_bn="ভার্নিয়ার লঘিষ্ঠ পাঠ", summary="LC = 1 MSD − 1 VSD", latex="\\mathrm{LC}=1\\,\\mathrm{MSD}-1\\,\\mathrm{VSD}=\\frac{1\\,\\mathrm{MSD}}{n}", order=70, trick="n ভাগে ভাগ করলে LC = MSD/n।", subject="physics", importance=2),
    make(id="screw-gauge-least-count", chapter="measurement", title="Screw Gauge Least Count", title_bn="স্ক্রু গেজ লঘিষ্ঠ পাঠ", summary="pitch/divisions", latex="\\mathrm{LC}=\\frac{\\text{pitch}}{\\text{circular scale divisions}}", order=80, trick="Pitch = এক পূর্ণ ঘূর্ণনে অগ্রগতি; LC = pitch/CSD।", subject="physics", importance=2),
    make(id="si-base-units", chapter="measurement", title="SI Base Units", title_bn="SI মৌলিক একক", summary="৭টি মৌলিক একক", latex="\\mathrm{m},\\ \\mathrm{kg},\\ \\mathrm{s},\\ \\mathrm{A},\\ \\mathrm{K},\\ \\mathrm{mol},\\ \\mathrm{cd}", order=90, trick="দৈর্ঘ্য–ভর–সময়–বিদ্যুৎ–তাপমাত্রা–মোল–ক্যান্ডেলা।", subject="physics", importance=2),
    make(id="absolute-relative-error", chapter="measurement", title="Absolute & Relative Error", title_bn="পরম ও আপেক্ষিক ত্রুটি", summary="Δx এবং Δx/x", latex="\\Delta x=|x_{\\text{meas}}-x_{\\text{true}}|,\\quad \\frac{\\Delta x}{x}", order=100, trick="পরম = পার্থক্য; আপেক্ষিক = পরম/মান।", subject="physics", importance=2),
]

# ── Physics: Motion / Kinematics ──────────────────────────────────────
MOTION = [
    make(id="displacement-velocity-accel", chapter="motion-kinematics", title="v and a Definitions", title_bn="বেগ ও ত্বরণের সংজ্ঞা", summary="v=dx/dt, a=dv/dt", latex="\\vec v=\\frac{d\\vec r}{dt},\\quad \\vec a=\\frac{d\\vec v}{dt}", order=10, trick="সরণের অন্তরক = বেগ; বেগের অন্তরক = ত্বরণ।", subject="physics", importance=3),
    make(id="average-instantaneous-velocity", chapter="motion-kinematics", title="Average & Instantaneous Velocity", title_bn="গড় ও তাৎক্ষণিক বেগ", summary="Δx/Δt vs dx/dt", latex="v_{\\text{avg}}=\\frac{\\Delta x}{\\Delta t},\\quad v=\\lim_{\\Delta t\\to0}\\frac{\\Delta x}{\\Delta t}", order=20, trick="গড় = মোট সরণ/সময়; তাৎক্ষণিক = সীমা।", subject="physics", importance=2),
    make(id="kinematic-equation-v", chapter="motion-kinematics", title="v = u + at", title_bn="প্রথম গতি সমীকরণ", summary="v=u+at", latex="v=u+at", order=30, trick="সমান ত্বরণে চূড়ান্ত বেগ = প্রাথমিক + at।", subject="physics", importance=3),
    make(id="kinematic-equation-s", chapter="motion-kinematics", title="s = ut + ½at²", title_bn="দ্বিতীয় গতি সমীকরণ", summary="s=ut+½at²", latex="s=ut+\\tfrac12 at^2", order=40, trick="সরণ = ut + ½at²; a=0 হলে s=ut।", subject="physics", importance=3),
    make(id="kinematic-equation-v2", chapter="motion-kinematics", title="v² = u² + 2as", title_bn="তৃতীয় গতি সমীকরণ", summary="v²=u²+2as", latex="v^2=u^2+2as", order=50, trick="সময় ছাড়া সমীকরণ; v²−u²=2as।", subject="physics", importance=3),
    make(id="kinematic-nth-second", chapter="motion-kinematics", title="Distance in nth Second", title_bn="n-তম সেকেন্ডে সরণ", summary="s_n", latex="s_n=u+\\tfrac12 a(2n-1)", order=60, trick="n-তম সেকেন্ড = u + a(2n−1)/2।", subject="physics", importance=2),
    make(id="relative-velocity-1d", chapter="motion-kinematics", title="Relative Velocity 1D", title_bn="আপেক্ষিক বেগ (১D)", summary="vAB=vA−vB", latex="\\vec v_{AB}=\\vec v_A-\\vec v_B", order=70, trick="A এর সাপেক্ষে B = vA − vB।", subject="physics", importance=2),
    make(id="rain-man-relative", chapter="motion-kinematics", title="Rain–Man Relative Velocity", title_bn="বৃষ্টি–মানুষ আপেক্ষিক বেগ", summary="umbrella tilt", latex="\\tan\\theta=\\frac{v_m}{v_r}\\quad(\\vec v_{rm}=\\vec v_r-\\vec v_m)", order=80, trick="ছাতা কাত = আপেক্ষিক বৃষ্টির দিক।", subject="physics", importance=2),
    make(id="river-boat-crossing", chapter="motion-kinematics", title="River Boat Crossing", title_bn="নদী পারাপার", summary="shortest path / time", latex="t=\\frac{d}{\\sqrt{v_b^2-v_r^2}}\\ (\\perp),\\quad t_{\\min}=\\frac{d}{v_b}", order=90, trick="লম্ব পথ: drift কাটতে কাত; কম সময়ে সোজা তীরের দিকে।", subject="physics", importance=2),
    make(id="graph-slope-area", chapter="motion-kinematics", title="Motion Graphs", title_bn="গতি লেখচিত্র", summary="slope & area", latex="v=\\text{slope of }x\\text{–}t;\\quad a=\\text{slope of }v\\text{–}t;\\quad s=\\text{area under }v\\text{–}t", order=100, trick="x–t ঢাল=v; v–t ঢাল=a; v–t ক্ষেত্রফল=s।", subject="physics", importance=3),
]

# ── Physics: Circular Motion ──────────────────────────────────────────
CIRCULAR = [
    make(id="angular-linear-relation", chapter="circular-motion", title="v = ωr", title_bn="রৈখিক–কৌণিক সম্পর্ক", summary="v=ωr", latex="v=\\omega r,\\quad a_t=\\alpha r", order=10, trick="রৈখিক বেগ = ω×r; স্পর্শক ত্বরণ = αr।", subject="physics", importance=3),
    make(id="centripetal-acceleration", chapter="circular-motion", title="Centripetal Acceleration", title_bn="কেন্দ্রমুখী ত্বরণ", summary="a=v²/r", latex="a_c=\\frac{v^2}{r}=\\omega^2 r", order=20, trick="দিক কেন্দ্রের দিকে; মান v²/r বা ω²r।", subject="physics", importance=3),
    make(id="period-frequency-circular", chapter="circular-motion", title="Period & Frequency", title_bn="পর্যায়কাল ও কম্পাঙ্ক", summary="T=2π/ω", latex="T=\\frac{2\\pi}{\\omega}=\\frac{1}{f},\\quad \\omega=2\\pi f", order=30, trick="ω = 2πf; T = 1/f।", subject="physics", importance=2),
    make(id="banking-of-road-ideal", chapter="circular-motion", title="Ideal Banking Angle", title_bn="আদর্শ ব্যাংকিং কোণ", summary="tanθ=v²/rg", latex="\\tan\\theta=\\frac{v^2}{rg}", order=40, trick="ঘর্ষণ ছাড়া; v² = rg tanθ।", subject="physics", importance=3),
    make(id="vertical-circle-tension", chapter="circular-motion", title="Vertical Circle", title_bn="উল্লম্ব বৃত্ত", summary="শীর্ষে/নিচে টান", latex="T_{\\text{bottom}}-mg=\\frac{mv^2}{r},\\quad T_{\\text{top}}+mg=\\frac{mv^2}{r}", order=50, trick="নিচে T−mg; উপরে T+mg; ন্যূনতম শীর্ষ বেগ √(gr)।", subject="physics", importance=3),
    make(id="vertical-circle-min-speed", chapter="circular-motion", title="Min Speed at Top", title_bn="শীর্ষে ন্যূনতম বেগ", summary="v=√(gr)", latex="v_{\\text{top,min}}=\\sqrt{gr},\\quad v_{\\text{bottom,min}}=\\sqrt{5gr}", order=60, trick="শীর্ষ √(gr); নিচে √(5gr) — শক্তি সংরক্ষণ।", subject="physics", importance=3),
    make(id="conical-pendulum", chapter="circular-motion", title="Conical Pendulum", title_bn="শঙ্কু দোলক", summary="T=2π√(L cosθ/g)", latex="T=2\\pi\\sqrt{\\frac{L\\cos\\theta}{g}},\\quad \\tan\\theta=\\frac{v^2}{rg}", order=70, trick="উল্লম্ব উপাংশ ভারসাম্য; অনুভূমিক = কেন্দ্রমুখী।", subject="physics", importance=2),
    make(id="death-well-loop", chapter="circular-motion", title="Loop-the-Loop", title_bn="লুপ দিয়ে ঘূর্ণন", summary="height 5r/2", latex="h_{\\min}=\\frac{5r}{2}\\quad\\text{(from bottom of loop)}", order=80, trick="লুপ সম্পূর্ণ করতে উচ্চতা ≥ 5r/2।", subject="physics", importance=2),
]

# ── Physics: Waves ────────────────────────────────────────────────────
WAVES = [
    make(id="wave-speed-string", chapter="waves", title="Wave Speed on String", title_bn="তারের তরঙ্গ বেগ", summary="v=√(T/μ)", latex="v=\\sqrt{\\frac{T}{\\mu}}", order=10, trick="টান বাড়লে বেগ বাড়ে; μ = ভর/দৈর্ঘ্য।", subject="physics", importance=3),
    make(id="wave-v-f-lambda", chapter="waves", title="v = fλ", title_bn="তরঙ্গ বেগ সূত্র", summary="v=fλ", latex="v=f\\lambda", order=20, trick="বেগ = কম্পাঙ্ক × তরঙ্গদৈর্ঘ্য — সব তরঙ্গে।", subject="physics", importance=3),
    make(id="transverse-wave-equation", chapter="waves", title="Progressive Wave Equation", title_bn="অগ্রগামী তরঙ্গ সমীকরণ", summary="y=A sin(ωt−kx)", latex="y=A\\sin(\\omega t-kx),\\quad k=\\frac{2\\pi}{\\lambda}", order=30, trick="ωt−kx ডানদিকে; ωt+kx বামদিকে।", subject="physics", importance=3),
    make(id="superposition-principle-wave", chapter="waves", title="Superposition Principle", title_bn="অধিরোপণ নীতি", summary="y=y1+y2", latex="y=y_1+y_2", order=40, trick="দুই তরঙ্গ একই স্থানে → সরণ যোগ।", subject="physics", importance=2),
    make(id="phase-path-difference", chapter="waves", title="Phase & Path Difference", title_bn="কলারূপ ও পথ পার্থক্য", summary="Δφ=2π/λ · Δx", latex="\\Delta\\phi=\\frac{2\\pi}{\\lambda}\\Delta x", order=50, trick="এক λ = 2π কলা; Δx দিয়ে Δφ।", subject="physics", importance=2),
    make(id="intensity-amplitude-wave", chapter="waves", title="Intensity ∝ A²", title_bn="তীব্রতা ও প্রশস্ততা", summary="I∝A²", latex="I\\propto A^2,\\quad I\\propto \\frac{1}{r^2}\\ (\\text{point source})", order=60, trick="প্রশস্ততা দ্বিগুণ → তীব্রতা চারগুণ; বিন্দু উৎসে 1/r²।", subject="physics", importance=2),
    make(id="echo-formula", chapter="waves", title="Echo", title_bn="প্রতিধ্বনি", summary="2d=vt", latex="2d=vt\\quad\\Rightarrow\\quad d=\\frac{vt}{2}", order=70, trick="যাওয়া+ফেরা = 2d; d = vt/2।", subject="physics", importance=2),
    make(id="doppler-effect-general", chapter="waves", title="Doppler Effect", title_bn="ডপলার প্রভাব", summary="f'=f(v±vo)/(v±vs)", latex="f'=f\\,\\frac{v\\pm v_o}{v\\pm v_s}", order=80, trick="পর্যবেক্ষক কাছে +; উৎস কাছে হলে ভাজকে − (কম্পন বাড়ে)।", subject="physics", importance=3),
    make(id="beats-frequency", chapter="waves", title="Beat Frequency", title_bn="কম্পনসংখ্যা পার্থক্য (বিট)", summary="|f1−f2|", latex="f_{\\text{beat}}=|f_1-f_2|", order=90, trick="প্রতি সেকেন্ডে বিট = দুই কম্পাঙ্কের পার্থক্য।", subject="physics", importance=2),
    make(id="organ-pipe-closed", chapter="waves", title="Closed Organ Pipe", title_bn="বন্ধ অর্গান পাইপ", summary="λ/4, 3λ/4…", latex="f_n=(2n-1)\\frac{v}{4L},\\quad n=1,2,3,\\ldots", order=100, trick="শুধু বিজোড় গুণিতক; মূল সুর v/4L।", subject="physics", importance=3),
    make(id="organ-pipe-open", chapter="waves", title="Open Organ Pipe", title_bn="মুক্ত অর্গান পাইপ", summary="λ/2, λ…", latex="f_n=n\\frac{v}{2L},\\quad n=1,2,3,\\ldots", order=110, trick="সব গুণিতক; মূল সুর v/2L।", subject="physics", importance=3),
]

# ── Physics: Astronomy ────────────────────────────────────────────────
ASTRONOMY = [
    make(id="parallax-distance", chapter="astronomy", title="Parallax Distance", title_bn="লম্বন দূরত্ব", summary="d=b/θ", latex="d=\\frac{b}{\\theta}\\quad(\\theta\\text{ in rad})", order=10, trick="ছোট কোণে চাপ ≈ জ্যা; নক্ষত্র দূরত্ব মাপার ভিত্তি।", subject="physics", importance=2),
    make(id="light-year-au", chapter="astronomy", title="Light Year & AU", title_bn="আলোকবর্ষ ও AU", summary="1 ly, 1 AU", latex="1\\,\\mathrm{ly}=9.46\\times10^{15}\\,\\mathrm{m},\\quad 1\\,\\mathrm{AU}=1.496\\times10^{11}\\,\\mathrm{m}", order=20, trick="AU = পৃথিবী–সূর্য গড় দূরত্ব; ly = আলোর ১ বছরের পথ।", subject="physics", importance=2),
    make(id="hubble-law", chapter="astronomy", title="Hubble's Law", title_bn="হাবলের সূত্র", summary="v=H₀d", latex="v=H_0 d", order=30, trick="দূরত্ব বাড়লে মহাবিশ্ব সম্প্রসারণ বেগ বাড়ে।", subject="physics", importance=2),
    make(id="solar-luminosity-flux", chapter="astronomy", title="Solar Constant / Flux", title_bn="সৌর ধ্রুবক", summary="S=L/(4πr²)", latex="S=\\frac{L}{4\\pi r^2}", order=40, trick="উজ্জ্বলতা L; পৃথিবীতে ফ্লাক্স 1/r² হারে কমে।", subject="physics", importance=2),
    make(id="magnitude-scale", chapter="astronomy", title="Apparent Magnitude", title_bn="আপাত মান", summary="m1−m2", latex="m_1-m_2=-2.5\\log_{10}\\frac{I_1}{I_2}", order=50, trick="৫ মান পার্থক্য = ১০০ গুণ তীব্রতা।", subject="physics", importance=1),
    make(id="escape-velocity-planet", chapter="astronomy", title="Planetary Escape Speed", title_bn="গ্রহ থেকে মুক্তি বেগ", summary="√(2GM/R)", latex="v_e=\\sqrt{\\frac{2GM}{R}}", order=60, trick="পৃথিবী ≈ 11.2 km/s; কৃষ্ণগহ্বরের event horizon সংজ্ঞায়।", subject="physics", importance=2),
]

# ── Chemistry: Environmental ──────────────────────────────────────────
ENV = [
    make(id="greenhouse-gases", chapter="environmental-chemistry", title="Greenhouse Gases", title_bn="গ্রিনহাউস গ্যাস", summary="CO₂, CH₄, N₂O, CFC", latex="\\ce{CO2},\\ \\ce{CH4},\\ \\ce{N2O},\\ \\ce{O3},\\ \\text{CFCs}", order=10, trick="IR শোষণ করে পৃথিবী গরম রাখে — CO₂ প্রধান।", subject="chemistry", importance=2),
    make(id="ozone-depletion", chapter="environmental-chemistry", title="Ozone Depletion", title_bn="ওজোন ক্ষয়", summary="CFC + O₃", latex="\\ce{CF2Cl2 ->[h\\nu] Cl*}\\ ;\\ \\ce{Cl* + O3 -> ClO* + O2}", order=20, trick="Cl· মুক্ত মূলক ওজোন ভাঙে; এক Cl হাজার ওজোন নষ্ট করতে পারে।", subject="chemistry", importance=2),
    make(id="acid-rain", chapter="environmental-chemistry", title="Acid Rain", title_bn="অম্ল বৃষ্টি", summary="pH < 5.6", latex="\\ce{SO2 + H2O -> H2SO3};\\quad \\ce{NO2 + H2O -> HNO3}", order=30, trick="SO₂/NO₂ → অম্ল; pH ৫.৬-এর নিচে = অম্ল বৃষ্টি।", subject="chemistry", importance=2),
    make(id="bod-cod", chapter="environmental-chemistry", title="BOD & COD", title_bn="BOD ও COD", summary="oxygen demand", latex="\\text{BOD}=\\text{O}_2\\text{ used by microbes (5 days)};\\quad \\text{COD}=\\text{chemical O}_2\\text{ demand}", order=40, trick="BOD বেশি = জল দূষিত; COD সবসময় ≥ BOD।", subject="chemistry", importance=2),
    make(id="smog-photochemical", chapter="environmental-chemistry", title="Photochemical Smog", title_bn="আলোকরাসায়নিক ধোঁয়াশা", summary="NOx + VOC + sunlight", latex="\\ce{NO2 ->[h\\nu] NO + O*}\\ ;\\ \\ce{O* + O2 -> O3}", order=50, trick="রৌদ্র + যানবাহন দূষণ → O₃, PAN; লস অ্যাঞ্জেলেস টাইপ।", subject="chemistry", importance=1),
    make(id="green-chemistry-principles", chapter="environmental-chemistry", title="Green Chemistry Idea", title_bn="সবুজ রসায়ন", summary="atom economy", latex="\\text{Atom economy}=\\frac{\\text{mass of desired product}}{\\text{mass of all reactants}}\\times100\\%", order=60, trick="কম বর্জ্য, উচ্চ atom economy = সবুজ প্রক্রিয়া।", subject="chemistry", importance=2),
]

# ── Chemistry: Quantitative ───────────────────────────────────────────
QUANT = [
    make(id="mole-concept-basic", chapter="quantitative-chem", title="Mole Concept", title_bn="মোল ধারণা", summary="n=N/NA=m/M", latex="n=\\frac{N}{N_A}=\\frac{m}{M}=\\frac{V}{22.4\\,\\mathrm{L}}\\ (\\text{STP gas})", order=10, trick="১ মোল = ৬.০২২×১০²³ কণা = M গ্রাম = STP-তে ২২.৪ L গ্যাস।", subject="chemistry", importance=3),
    make(id="molarity-molality", chapter="quantitative-chem", title="Molarity & Molality", title_bn="মোলারিটি ও মোলালিটি", summary="M vs m", latex="M=\\frac{n_{\\text{solute}}}{V_{\\text{L}}},\\quad m=\\frac{n_{\\text{solute}}}{w_{\\text{kg solvent}}}", order=20, trick="M = মোল/লিটার দ্রবণ; m = মোল/কেজি দ্রাবক (তাপমাত্রা-নির্ভর নয়)।", subject="chemistry", importance=3),
    make(id="normality-relation", chapter="quantitative-chem", title="Normality", title_bn="নরমালিটি", summary="N=M×n-factor", latex="N=M\\times n_{\\text{factor}},\\quad N_1V_1=N_2V_2", order=30, trick="অম্ল/ক্ষারের n-factor = H⁺/OH⁻ সংখ্যা; টাইট্রেশনে N₁V₁=N₂V₂।", subject="chemistry", importance=3),
    make(id="percentage-composition", chapter="quantitative-chem", title="Percentage Composition", title_bn="শতকরা সংযুক্তি", summary="% element", latex="\\%=\\frac{\\text{mass of element in formula}}{\\text{molar mass}}\\times100", order=40, trick="যৌগে মৌলের ভর অনুপাত × ১০০।", subject="chemistry", importance=2),
    make(id="stoichiometry-mass", chapter="quantitative-chem", title="Stoichiometric Mass Relation", title_bn="stoichiometry ভর সম্পর্ক", summary="mole ratio", latex="\\frac{m_A}{aM_A}=\\frac{m_B}{bM_B}\\quad(aA\\to bB)", order=50, trick="সমীকরণের মোল অনুপাত দিয়ে ভর বের করো।", subject="chemistry", importance=3),
    make(id="limiting-reagent-calc", chapter="quantitative-chem", title="Limiting Reagent Calc", title_bn="সীমিত বিকারক গণনা", summary="smallest mole/coeff", latex="\\text{limiting}=\\min\\left(\\frac{n_i}{\\nu_i}\\right)", order=60, trick="প্রতিটি বিকারকের n/গুণাঙ্ক; সবচেয়ে ছোট = limiting।", subject="chemistry", importance=3),
    make(id="ppm-ppb", chapter="quantitative-chem", title="ppm & ppb", title_bn="ppm ও ppb", summary="parts per million", latex="\\mathrm{ppm}=\\frac{\\text{mass solute}}{\\text{mass solution}}\\times10^6", order=70, trick="জল দূষণ/অশোধনে ppm; ১ ppm ≈ ১ mg/L জলে।", subject="chemistry", importance=2),
    make(id="gas-stoichiometry-volume", chapter="quantitative-chem", title="Gas Volume Stoichiometry", title_bn="গ্যাস আয়তন stoichiometry", summary="Avogadro volume ratio", latex="\\frac{V_A}{V_B}=\\frac{a}{b}\\quad(\\text{same }T,P)", order=80, trick="একই T,P-তে গ্যাসের আয়তন অনুপাত = মোল অনুপাত।", subject="chemistry", importance=2),
]

# ── Math: Sequences & Series ──────────────────────────────────────────
SEQ = [
    make(id="ap-nth-term", chapter="sequences-series", title="AP nth Term", title_bn="সমান্তর ধারার n-তম পদ", summary="a+(n−1)d", latex="a_n=a+(n-1)d", order=10, trick="প্রথম পদ a, সাধারণ অন্তর d।", importance=3),
    make(id="ap-sum", chapter="sequences-series", title="Sum of AP", title_bn="সমান্তর ধারার যোগফল", summary="n/2[2a+(n−1)d]", latex="S_n=\\frac{n}{2}[2a+(n-1)d]=\\frac{n}{2}(a+l)", order=20, trick="S = n/2 × (প্রথম+শেষ)।", importance=3),
    make(id="gp-nth-term", chapter="sequences-series", title="GP nth Term", title_bn="গুণোত্তর ধারার n-তম পদ", summary="ar^(n−1)", latex="a_n=ar^{n-1}", order=30, trick="প্রথম a, সাধারণ অনুপাত r।", importance=3),
    make(id="gp-sum-finite", chapter="sequences-series", title="Sum of Finite GP", title_bn="সসীম গুণোত্তর যোগফল", summary="a(rⁿ−1)/(r−1)", latex="S_n=a\\frac{r^n-1}{r-1}\\ (r\\ne1)", order=40, trick="r≠1; r=1 হলে S=na।", importance=3),
    make(id="gp-sum-infinite", chapter="sequences-series", title="Infinite GP Sum", title_bn="অসীম গুণোত্তর যোগফল", summary="a/(1−r)", latex="S_\\infty=\\frac{a}{1-r}\\quad(|r|<1)", order=50, trick="|r|<1 হলেই অসীম যোগফল আছে।", importance=3),
    make(id="hp-relation", chapter="sequences-series", title="Harmonic Progression", title_bn="হারমোনিক ধারা", summary="1/a_n is AP", latex="a,b,c\\text{ in HP}\\iff \\frac{1}{a},\\frac{1}{b},\\frac{1}{c}\\text{ in AP}", order=60, trick="HP-এর ব্যস্তক AP — এই ট্রিকই যথেষ্ট।", importance=2),
    make(id="am-gm-hm", chapter="sequences-series", title="AM–GM–HM Inequality", title_bn="AM–GM–HM অসমতা", summary="AM≥GM≥HM", latex="\\frac{a+b}{2}\\ge\\sqrt{ab}\\ge\\frac{2ab}{a+b}", order=70, trick="সমানতা কেবল a=b-তে; ভর্তিতে খুব কাজে লাগে।", importance=3),
    make(id="agp-sum", chapter="sequences-series", title="Arithmetico-Geometric Series", title_bn="সমান্তর-গুণোত্তর ধারা", summary="Σ n rⁿ", latex="S=a+(a+d)r+(a+2d)r^2+\\cdots", order=80, trick="S − rS করে GP বের করো।", importance=2),
    make(id="sum-natural-squares-cubes", chapter="sequences-series", title="Σn, Σn², Σn³", title_bn="প্রাকৃতিক সংখ্যার ঘাতের যোগ", summary="n(n+1)/2 ইত্যাদি", latex="\\sum n=\\frac{n(n+1)}{2},\\ \\sum n^2=\\frac{n(n+1)(2n+1)}{6},\\ \\sum n^3=\\left(\\frac{n(n+1)}{2}\\right)^2", order=90, trick="Σn³ = (Σn)² — মনে রাখার সহজ সম্পর্ক।", importance=3),
    make(id="arithmetic-mean-insert", chapter="sequences-series", title="Inserting AMs", title_bn="সমান্তর মধ্যক নিবেশ", summary="n AMs between a,b", latex="d=\\frac{b-a}{n+1}", order=100, trick="a ও b-এর মাঝে nটি AM → অন্তর (b−a)/(n+1)।", importance=2),
]

# ── Math: Circle Geometry ─────────────────────────────────────────────
CIRCLE = [
    make(id="circle-general-equation", chapter="circle-geometry", title="General Circle Equation", title_bn="বৃত্তের সাধারণ সমীকরণ", summary="x²+y²+2gx+2fy+c=0", latex="x^2+y^2+2gx+2fy+c=0,\\quad \\text{centre }(-g,-f),\\ r=\\sqrt{g^2+f^2-c}", order=10, trick="কেন্দ্র (−g,−f); r²=g²+f²−c>0 চাই।", importance=3),
    make(id="circle-center-radius", chapter="circle-geometry", title="Centre-Radius Form", title_bn="কেন্দ্র–ব্যাসার্ধ রূপ", summary="(x−h)²+(y−k)²=r²", latex="(x-h)^2+(y-k)^2=r^2", order=20, trick="কেন্দ্র (h,k), ব্যাসার্ধ r — সবচেয়ে সোজা রূপ।", importance=3),
    make(id="circle-diameter-form", chapter="circle-geometry", title="Equation with Diameter", title_bn="ব্যাস দিয়ে বৃত্ত", summary="endpoints form", latex="(x-x_1)(x-x_2)+(y-y_1)(y-y_2)=0", order=30, trick="ব্যাসের দুই প্রান্ত জানা থাকলেই সমীকরণ।", importance=2),
    make(id="tangent-circle-point", chapter="circle-geometry", title="Tangent at Point on Circle", title_bn="বৃত্তের বিন্দুতে স্পর্শক", summary="xx1+yy1=r²", latex="xx_1+yy_1=r^2\\quad(x^2+y^2=r^2)", order=40, trick="T=0 পদ্ধতি; কেন্দ্রে xx₁+yy₁=r²।", importance=3),
    make(id="tangent-from-external", chapter="circle-geometry", title="Tangent from External Point", title_bn="বহিঃস্থ বিন্দু থেকে স্পর্শক", summary="length √(S1)", latex="L=\\sqrt{S_1}=\\sqrt{x_1^2+y_1^2-r^2}", order=50, trick="স্পর্শকের দৈর্ঘ্য = √(power of point)।", importance=2),
    make(id="chord-of-contact", chapter="circle-geometry", title="Chord of Contact", title_bn="স্পর্শকদ্বয়ের জ্যা", summary="xx1+yy1=r²", latex="xx_1+yy_1=r^2\\quad\\text{(from }(x_1,y_1)\\text{)}", order=60, trick="বহিঃস্থ বিন্দু থেকে দুই স্পর্শকের সংযোগ জ্যা = chord of contact।", importance=2),
    make(id="power-of-point", chapter="circle-geometry", title="Power of a Point", title_bn="বিন্দুর ক্ষমতা", summary="PA·PB=PT²", latex="PA\\cdot PB=PT^2=\\text{power}", order=70, trick="ছেদকারী জ্যা বা স্পর্শক — পাওয়ার সমান।", importance=2),
    make(id="radical-axis", chapter="circle-geometry", title="Radical Axis", title_bn="মূলদ অক্ষ", summary="S1−S2=0", latex="S_1-S_2=0", order=80, trick="দুই বৃত্তের সমীকরণ বিয়োগ = radical axis (সরলরেখা)।", importance=2),
    make(id="common-chord-circles", chapter="circle-geometry", title="Common Chord", title_bn="সাধারণ জ্যা", summary="S1−S2=0", latex="S_1-S_2=0\\quad(\\text{intersecting circles})", order=90, trick="ছেদকারী বৃত্তে radical axis = সাধারণ জ্যা।", importance=2),
    make(id="condition-orthogonality-circles", chapter="circle-geometry", title="Orthogonal Circles", title_bn="লম্ববৃত্ত", summary="2g1g2+2f1f2=c1+c2", latex="2g_1g_2+2f_1f_2=c_1+c_2", order=100, trick="ছেদকোণ ৯০° → d² = r₁²+r₂²।", importance=2),
]

# ── Math: Differentiation (dedicated HSC chapter feel) ────────────────
DIFF = [
    make(id="derivative-definition", chapter="differentiation", title="Derivative Definition", title_bn="অন্তরকের সংজ্ঞা", summary="lim h→0", latex="f'(x)=\\lim_{h\\to0}\\frac{f(x+h)-f(x)}{h}", order=10, trick="ঢালের সীমা = অন্তরক।", importance=3),
    make(id="derivative-xn", chapter="differentiation", title="Power Rule", title_bn="ঘাত নিয়ম", summary="nxⁿ⁻¹", latex="\\frac{d}{dx}x^n=nx^{n-1}", order=20, trick="ঘাত সামনে এনে এক কমাও।", importance=3),
    make(id="derivative-trig", chapter="differentiation", title="Trig Derivatives", title_bn="ত্রিকোণমিতিক অন্তরক", summary="sin, cos, tan", latex="(\\sin x)'=\\cos x,\\ (\\cos x)'=-\\sin x,\\ (\\tan x)'=\\sec^2 x", order=30, trick="sin→cos; cos→−sin; tan→sec²।", importance=3),
    make(id="derivative-exp-log", chapter="differentiation", title="Exp & Log Derivatives", title_bn="সূচক ও লগ অন্তরক", summary="eˣ, ln x", latex="(e^x)'=e^x,\\quad (\\ln x)'=\\frac{1}{x},\\quad (a^x)'=a^x\\ln a", order=40, trick="eˣ নিজের অন্তরক; ln-এর অন্তরক ১/x।", importance=3),
    make(id="chain-rule-diff", chapter="differentiation", title="Chain Rule", title_bn="শৃঙ্খল নিয়ম", summary="dy/dx=(dy/du)(du/dx)", latex="\\frac{dy}{dx}=\\frac{dy}{du}\\cdot\\frac{du}{dx}", order=50, trick="বাইরের অন্তরক × ভিতরের অন্তরক।", importance=3),
    make(id="product-rule-diff", chapter="differentiation", title="Product Rule", title_bn="গুণ নিয়ম", summary="uv'+vu'", latex="(uv)'=u'v+uv'", order=60, trick="প্রথম×দ্বিতীয়′ + দ্বিতীয়×প্রথম′।", importance=3),
    make(id="quotient-rule-diff", chapter="differentiation", title="Quotient Rule", title_bn="ভাগ নিয়ম", summary="(vu'−uv')/v²", latex="\\left(\\frac{u}{v}\\right)'=\\frac{u'v-uv'}{v^2}", order=70, trick="নিচের বর্গ ভাজক; উপরে vu′−uv′।", importance=3),
    make(id="implicit-diff", chapter="differentiation", title="Implicit Differentiation", title_bn="অন্তর্নিহিত অন্তরীকরণ", summary="F(x,y)=0", latex="\\frac{dy}{dx}=-\\frac{F_x}{F_y}", order=80, trick="দুই পাশে d/dx; y′ আলাদা করো।", importance=2),
    make(id="parametric-diff", chapter="differentiation", title="Parametric Differentiation", title_bn="প্যারামিতিক অন্তরীকরণ", summary="dy/dx=(dy/dt)/(dx/dt)", latex="\\frac{dy}{dx}=\\frac{dy/dt}{dx/dt}", order=90, trick="t বাদ না দিয়েই ঢাল।", importance=2),
    make(id="second-derivative", chapter="differentiation", title="Second Derivative", title_bn="দ্বিতীয় অন্তরক", summary="d²y/dx²", latex="\\frac{d^2y}{dx^2}=\\frac{d}{dx}\\left(\\frac{dy}{dx}\\right)", order=100, trick="বাঁক/উত্তলতা ও maxima-minima পরীক্ষায়।", importance=2),
]

# ── Expansions for existing chapters ──────────────────────────────────
EXPAND = [
    # properties of matter
    make(id="excess-pressure-bubble", chapter="properties-of-matter", title="Excess Pressure in Bubble", title_bn="বুদবুদে অতিরিক্ত চাপ", summary="4T/r soap, 2T/r air", latex="\\Delta P_{\\text{soap}}=\\frac{4T}{r},\\quad \\Delta P_{\\text{air bubble}}=\\frac{2T}{r}", order=110, trick="সাবান বুদবুদ দুই তল → 4T/r; বায়ু বুদবুদ এক তল → 2T/r।", subject="physics", importance=3),
    make(id="hookes-law-stress-strain", chapter="properties-of-matter", title="Hooke's Law", title_bn="হুকের সূত্র", summary="stress∝strain", latex="\\frac{F}{A}=Y\\frac{\\Delta L}{L}", order=120, trick="স্থিতিস্থাপক সীমায় stress = Y × strain।", subject="physics", importance=3),
    # static electricity
    make(id="gauss-law", chapter="static-electricity", title="Gauss's Law", title_bn="গসের সূত্র", summary="∮E·dA=Q/ε₀", latex="\\oint\\vec E\\cdot d\\vec A=\\frac{Q_{\\text{encl}}}{\\varepsilon_0}", order=130, trick="বদ্ধ তলে মোট ফ্লাক্স = ভিতরের চার্জ/ε₀।", subject="physics", importance=3),
    make(id="field-infinite-sheet", chapter="static-electricity", title="Field of Infinite Sheet", title_bn="অসীম পাতের ক্ষেত্র", summary="E=σ/2ε₀", latex="E=\\frac{\\sigma}{2\\varepsilon_0}", order=140, trick="অসীম চার্জিত পাত; দূরত্ব-নির্ভর নয়।", subject="physics", importance=2),
    # geometric optics
    make(id="critical-angle", chapter="geometric-optics", title="Critical Angle", title_bn="ক্রান্তি কোণ", summary="sin c = 1/μ", latex="\\sin c=\\frac{1}{\\mu}=\\frac{\\mu_r}{\\mu_d}", order=130, trick="ঘন→হালকা; c-এর বেশি = সম্পূর্ণ অভ্যন্তরীণ প্রতিফলন।", subject="physics", importance=3),
    make(id="lens-formula", chapter="geometric-optics", title="Thin Lens Formula", title_bn="পাতলা লেন্স সূত্র", summary="1/v−1/u=1/f", latex="\\frac{1}{v}-\\frac{1}{u}=\\frac{1}{f}", order=140, trick="দর্পণে +; লেন্সে − চিহ্ন প্রথা মেনে চলো।", subject="physics", importance=3),
    # thermodynamics
    make(id="thermal-expansion-linear", chapter="thermodynamics", title="Linear Expansion", title_bn="রৈখিক প্রসারণ", summary="ΔL=αLΔT", latex="\\Delta L=\\alpha L\\Delta T,\\quad \\gamma=3\\alpha", order=130, trick="γ = 3α; আয়তন প্রসারণ তিনগুণ রৈখিক।", subject="physics", importance=2),
    # organic
    make(id="hoffmann-bromamide", chapter="organic-chem", title="Hoffmann Bromamide", title_bn="হফম্যান ব্রোমামাইড", summary="amide → amine (−1C)", latex="\\ce{RCONH2 + Br2 + 4KOH -> RNH2 + K2CO3 + 2KBr + 2H2O}", order=210, trick="অ্যামাইড থেকে ১ কার্বন কম প্রাথমিক অ্যামিন।", subject="chemistry", importance=2),
    make(id="williamson-ether", chapter="organic-chem", title="Williamson Ether Synthesis", title_bn="উইলিয়ামসন ইথার সংশ্লেষণ", summary="RONa + R'X", latex="\\ce{RONa + R'X -> ROR' + NaX}", order=220, trick="অ্যালকক্সাইড + অ্যালকাইল হ্যালাইড → ইথার।", subject="chemistry", importance=2),
    # equilibrium
    make(id="ph-strong-acid", chapter="chemical-equilibrium", title="pH of Strong Acid", title_bn="সবল অম্লের pH", summary="pH=−log[H+]", latex="\\mathrm{pH}=-\\log_{10}[\\mathrm{H}^+],\\quad \\mathrm{pOH}=-\\log_{10}[\\mathrm{OH}^-]", order=170, trick="সবল অম্লে [H⁺]=molarity; pH+pOH=14 (২৫°C)।", subject="chemistry", importance=3),
    # work-energy
    make(id="work-by-constant-force", chapter="work-energy", title="Work by Constant Force", title_bn="ধ্রুব বলের কাজ", summary="W=F·s", latex="W=\\vec F\\cdot\\vec s=Fs\\cos\\theta", order=110, trick="θ=৯০° হলে কাজ শূন্য; বিপরীত হলে ঋণাত্মক।", subject="physics", importance=3),
    # gravitation
    make(id="acceleration-due-to-gravity", chapter="gravitation", title="g = GM/R²", title_bn="অভিকর্ষজ ত্বরণ", summary="g=GM/R²", latex="g=\\frac{GM}{R^2}", order=110, trick="পৃথিবী পৃষ্ঠে g; উচ্চতায় g' = g(1−2h/R)।", subject="physics", importance=3),
    # matrix
    make(id="matrix-transpose-properties", chapter="matrix-determinant", title="Transpose Properties", title_bn="ট্রান্সপোজ ধর্ম", summary="(AB)ᵀ=BᵀAᵀ", latex="(AB)^T=B^TA^T,\\quad (A^T)^T=A", order=80, trick="গুণের ট্রান্সপোজে ক্রম উল্টো।", importance=2),
    make(id="determinant-3x3-expansion", chapter="matrix-determinant", title="3×3 Determinant Expansion", title_bn="৩×৩ নির্ণায়ক প্রসারণ", summary="cofactor expansion", latex="|A|=a_{11}C_{11}+a_{12}C_{12}+a_{13}C_{13}", order=90, trick="এক সারি বরাবর সহগুণক দিয়ে প্রসারণ।", importance=3),
    # binomial
    make(id="binomial-general-term-position", chapter="binomial-theorem", title="General Term Position", title_bn="সাধারণ পদের অবস্থান", summary="T_{r+1}", latex="T_{r+1}=\\binom{n}{r}a^{n-r}b^r", order=140, trick="(r+1)-তম পদ; r=0 থেকে শুরু।", importance=2),
    # complex
    make(id="complex-conjugate-modulus", chapter="complex-numbers", title="z·z̄ = |z|²", title_bn="মডুলাস ও কনজুগেট", summary="zz̄=|z|²", latex="z\\bar z=|z|^2", order=140, trick="ভাগ করার সময় ভাজককে কনজুগেট দিয়ে গুণ।", importance=3),
    # probability
    make(id="poisson-approx-hint", chapter="probability", title="Poisson Approximation Hint", title_bn="পোয়াসোঁ আনুমানিক", summary="λ=np", latex="P(X=k)\\approx e^{-\\lambda}\\frac{\\lambda^k}{k!},\\quad \\lambda=np", order=150, trick="n বড়, p ছোট হলে binomial → Poisson।", importance=1),
    # sets
    make(id="n-union-three-sets", chapter="sets-functions", title="Inclusion–Exclusion (3 sets)", title_bn="তিন সেটের অন্তর্ভুক্তি–বর্জন", summary="|A∪B∪C|", latex="|A\\cup B\\cup C|=|A|+|B|+|C|-|A\\cap B|-|B\\cap C|-|C\\cap A|+|A\\cap B\\cap C|", order=110, trick="যোগ − জোড় ছেদ + তিনের ছেদ।", importance=2),
    # conic
    make(id="parabola-reflection-property", chapter="conic-sections", title="Parabola Reflection Property", title_bn="পরাবৃত্তের প্রতিফলন ধর্ম", summary="focus-directrix path", latex="\\text{ray }\\parallel\\text{ axis reflects through focus}", order=190, trick="অক্ষের সমান্তরাল রশ্মি ফোকাস দিয়ে যায় — স্যাটেলাইট ডিশ।", importance=1),
    # semiconductor
    make(id="led-principle", chapter="semiconductor", title="LED Principle", title_bn="LED নীতি", summary="recombination photon", latex="E_g=\\frac{hc}{\\lambda}", order=110, trick="ব্যান্ড গ্যাপ = ফোটন শক্তি; রঙ Eg দিয়ে নির্ধারিত।", subject="physics", importance=2),
    # induction
    make(id="eddy-current-loss", chapter="induction-ac", title="Eddy Current", title_bn="এডি কারেন্ট", summary="laminated core", latex="P_{\\text{eddy}}\\propto B^2f^2t^2", order=130, trick="পাতলা স্তরে কোর কাটো → এডি লস কমে।", subject="physics", importance=1),
    # current
    make(id="shunt-multiplier", chapter="current-electricity", title="Shunt & Multiplier", title_bn="শাণ্ট ও মাল্টিপ্লায়ার", summary="Ammeter/Voltmeter", latex="S=\\frac{I_g G}{I-I_g},\\quad R=\\frac{V}{I_g}-G", order=140, trick="অ্যামিটারে সমান্তরাল শাণ্ট; ভোল্টমিটারে সিরিজ রোধ।", subject="physics", importance=2),
]


CHAPTERS = [
    ("physics", "measurement", {"id": "measurement", "slug": "measurement", "name": "Physical World & Measurement", "nameBn": "ভৌত জগত ও পরিমাপ", "order": 1}, MEASUREMENT),
    ("physics", "motion-kinematics", {"id": "motion-kinematics", "slug": "motion-kinematics", "name": "Motion & Kinematics", "nameBn": "গতিবিদ্যা", "order": 3}, MOTION),
    ("physics", "circular-motion", {"id": "circular-motion", "slug": "circular-motion", "name": "Circular Motion", "nameBn": "বৃত্তাকার গতি", "order": 6}, CIRCULAR),
    ("physics", "waves", {"id": "waves", "slug": "waves", "name": "Waves", "nameBn": "তরঙ্গ", "order": 9}, WAVES),
    ("physics", "astronomy", {"id": "astronomy", "slug": "astronomy", "name": "Astronomy & Astrophysics", "nameBn": "জ্যোতির্বিজ্ঞান", "order": 11}, ASTRONOMY),
    ("chemistry", "environmental-chemistry", {"id": "environmental-chemistry", "slug": "environmental-chemistry", "name": "Environmental Chemistry", "nameBn": "পরিবেশ রসায়ন", "order": 1}, ENV),
    ("chemistry", "quantitative-chem", {"id": "quantitative-chem", "slug": "quantitative-chem", "name": "Quantitative Chemistry", "nameBn": "পরিমাণগত রসায়ন", "order": 1}, QUANT),
    ("math", "sequences-series", {"id": "sequences-series", "slug": "sequences-series", "name": "Sequences & Series", "nameBn": "অনুক্রম ও ধারা", "order": 4}, SEQ),
    ("math", "circle-geometry", {"id": "circle-geometry", "slug": "circle-geometry", "name": "Circle", "nameBn": "বৃত্ত", "order": 4}, CIRCLE),
    ("math", "differentiation", {"id": "differentiation", "slug": "differentiation", "name": "Differentiation", "nameBn": "অন্তরীকরণ", "order": 8}, DIFF),
]


def main():
    n = 0
    for subject, chapter, meta, formulas in CHAPTERS:
        write_meta(subject, chapter, meta)
        for f in formulas:
            write_formula(subject, chapter, f)
            n += 1
    for f in EXPAND:
        write_formula(f["subjects"][0], f["chapter"], f)
        n += 1
    print(f"Wrote {n} formulas across {len(CHAPTERS)} new chapters + expansions")


if __name__ == "__main__":
    main()
