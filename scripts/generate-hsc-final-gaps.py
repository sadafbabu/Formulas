#!/usr/bin/env python3
"""Final HSC gap fill: integration, nuclear chem, extra high-yield formulas."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "subjects"
EXISTING = {p.stem for p in ROOT.glob("*/chapters/*/formulas/*.json")}


def make(*, id, chapter, title, title_bn, summary, latex, importance=2, order=10, trick="", subject="math"):
    if id in EXISTING:
        raise SystemExit(f"duplicate id: {id}")
    star = f"{importance}-star"
    if subject == "math":
        tags = ["hsc", "eng-admission", "varsity", star]
    else:
        tags = ["hsc", "eng-admission", "medical", "varsity", star]
    return {
        "id": id,
        "chapter": chapter,
        "title": title,
        "titleBn": title_bn,
        "summary": summary,
        "latex": latex,
        "tags": tags,
        "importance": importance,
        "order": order,
        "symbols": [{"symbol": "—", "meaning": "প্রধান চলকসমূহ সূত্রে দ্রষ্টব্য", "unit": "—"}],
        "derivation": {
            "lead": summary,
            "steps": [{"title": "মূল সূত্র", "latex": latex, "note": "HSC ও ভর্তি পরীক্ষায় সরাসরি প্রয়োগযোগ্য রূপ।"}],
            "assumptions": [],
        },
        "questions": [{"examType": "HSC / Admission", "question": f"{title_bn} এর মূল সূত্রটি লেখো।", "answer": latex}],
        "memorize": {"trick": trick, "steps": []},
        "subjects": [subject],
        "related": [],
    }


def write_formula(subject, chapter, data):
    out = ROOT / subject / "chapters" / chapter / "formulas"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{data['id']}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    EXISTING.add(data["id"])


def write_meta(subject, chapter, meta):
    out = ROOT / subject / "chapters" / chapter
    out.mkdir(parents=True, exist_ok=True)
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


INTEGRATION = [
    make(id="integral-xn", chapter="integration", title="Power Integral", title_bn="ঘাতের যোগজ", summary="∫xⁿ dx", latex="\\int x^n\\,dx=\\frac{x^{n+1}}{n+1}+C\\quad(n\\ne-1)", order=10, trick="ঘাত এক বাড়াও, নতুন ঘাত দিয়ে ভাগ।", importance=3),
    make(id="integral-1x", chapter="integration", title="∫ dx/x", title_bn="১/x এর যোগজ", summary="ln|x|", latex="\\int\\frac{1}{x}\\,dx=\\ln|x|+C", order=20, trick="n=−1 ব্যতিক্রম → ln|x|।", importance=3),
    make(id="integral-ex", chapter="integration", title="∫ eˣ dx", title_bn="eˣ এর যোগজ", summary="eˣ", latex="\\int e^x\\,dx=e^x+C,\\quad \\int a^x\\,dx=\\frac{a^x}{\\ln a}+C", order=30, trick="eˣ নিজের যোগজ; aˣ ভাগ ln a।", importance=3),
    make(id="integral-trig-basic", chapter="integration", title="Basic Trig Integrals", title_bn="মৌলিক ত্রিকোণমিতিক যোগজ", summary="sin, cos, sec²", latex="\\int\\sin x= -\\cos x,\\ \\int\\cos x=\\sin x,\\ \\int\\sec^2 x=\\tan x", order=40, trick="অন্তরকের উল্টো দিক মনে রাখো।", importance=3),
    make(id="integral-substitution-basic", chapter="integration", title="Substitution Method", title_bn="প্রতিস্থাপন পদ্ধতি", summary="u=g(x)", latex="\\int f(g(x))g'(x)\\,dx=\\int f(u)\\,du", order=50, trick="ভিতরের অন্তরক দেখলেই u ধরো।", importance=3),
    make(id="integral-by-parts-ilate", chapter="integration", title="Integration by Parts", title_bn="অংশীয় যোগজীকরণ", summary="∫u dv", latex="\\int u\\,dv=uv-\\int v\\,du", order=60, trick="LIATE: Log → Inverse → Algebraic → Trig → Exp।", importance=3),
    make(id="definite-integral-properties", chapter="integration", title="Definite Integral Properties", title_bn="নির্দিষ্ট যোগজের ধর্ম", summary="bounds swap", latex="\\int_a^b f=-\\int_b^a f,\\quad \\int_a^a f=0,\\quad \\int_a^b f=\\int_a^c f+\\int_c^b f", order=70, trick="সীমা উল্টালে ঋণাত্মক; মাঝের বিন্দু ভাঙা যায়।", importance=2),
    make(id="integral-even-odd", chapter="integration", title="Even–Odd Integrals", title_bn="জোড়–বিজোড় যোগজ", summary="symmetric limits", latex="\\int_{-a}^{a}f_{\\text{even}}=2\\int_0^a f,\\quad \\int_{-a}^{a}f_{\\text{odd}}=0", order=80, trick="বিজোড় ফাংশন সমমিত সীমায় শূন্য।", importance=2),
    make(id="area-under-curve", chapter="integration", title="Area Under Curve", title_bn="বক্ররেখার নিচের ক্ষেত্রফল", summary="A=∫y dx", latex="A=\\int_a^b y\\,dx=\\int_a^b f(x)\\,dx", order=90, trick="x-অক্ষের উপরের ক্ষেত্র ধনাত্মক।", importance=3),
    make(id="volume-disk-method", chapter="integration", title="Volume Disk Method", title_bn="চাকতি পদ্ধতিতে আয়তন", summary="π∫y² dx", latex="V=\\pi\\int_a^b [f(x)]^2\\,dx", order=100, trick="x-অক্ষ ঘুরিয়ে চাকতি; πr² এর যোগজ।", importance=2),
]

NUCLEAR = [
    make(id="radioactive-decay-law-chem", chapter="nuclear-chemistry", title="Radioactive Decay Law", title_bn="তেজস্ক্রিয় ক্ষয় সূত্র", summary="N=N₀e^(−λt)", latex="N=N_0 e^{-\\lambda t},\\quad A=\\lambda N", order=10, trick="A = λN; সক্রিয়তা ক্ষয়ের হার।", subject="chemistry", importance=3),
    make(id="half-life-chem", chapter="nuclear-chemistry", title="Half-Life", title_bn="অর্ধায়ু", summary="t½=ln2/λ", latex="t_{1/2}=\\frac{\\ln 2}{\\lambda}=\\frac{0.693}{\\lambda}", order=20, trick="অর্ধায়ু = ০.৬৯৩/λ — মুখস্থ।", subject="chemistry", importance=3),
    make(id="carbon-dating", chapter="nuclear-chemistry", title="Carbon Dating", title_bn="কার্বন ডেটিং", summary="¹⁴C age", latex="t=\\frac{t_{1/2}}{0.693}\\ln\\frac{N_0}{N}", order=30, trick="জীবিত বস্তুতে ¹⁴C/¹²C স্থির; মৃত্যুর পর ক্ষয়।", subject="chemistry", importance=2),
    make(id="binding-energy-per-nucleon", chapter="nuclear-chemistry", title="Binding Energy per Nucleon", title_bn="প্রতি নিউক্লিয়নে বন্ধন শক্তি", summary="BE/A", latex="\\text{BE/nucleon}=\\frac{[Zm_H+(A-Z)m_n-M]c^2}{A}", order=40, trick="BE/A বেশি = স্থিতিশীল নিউক্লিয়াস; Fe কাছাকাছি সর্বোচ্চ।", subject="chemistry", importance=2),
    make(id="alpha-beta-gamma-decay", chapter="nuclear-chemistry", title="α β γ Decay", title_bn="α β γ ক্ষয়", summary="emission changes", latex="\\alpha:\\,A\\!-\\!4,Z\\!-\\!2;\\quad \\beta^-:\\,Z\\!+\\!1;\\quad \\gamma:\\ \\text{no }A,Z\\text{ change}", order=50, trick="α = He নিউক্লিয়াস; β⁻ = নিউট্রন→প্রোটন; γ = শুধু শক্তি।", subject="chemistry", importance=3),
    make(id="nuclear-fission-fusion", chapter="nuclear-chemistry", title="Fission & Fusion", title_bn="বিভাজন ও সংযোজন", summary="heavy split / light join", latex="\\text{fission: heavy}\\to\\text{lighter}+\\text{energy};\\ \\text{fusion: light}\\to\\text{heavier}", order=60, trick="বিভাজন ইউরেনিয়াম; সংযোজন সূর্যের শক্তি।", subject="chemistry", importance=2),
]

TRIG_EXTRA = [
    make(id="sin2a-cos2a", chapter="trigonometric-equations", title="Double Angle Formulas", title_bn="দ্বিগুণ কোণ সূত্র", summary="sin2A, cos2A", latex="\\sin2A=2\\sin A\\cos A,\\quad \\cos2A=\\cos^2A-\\sin^2A=2\\cos^2A-1=1-2\\sin^2A", order=180, trick="cos2A-এর তিন রূপ — sin/cos একা থাকলে কাজে লাগে।", importance=3),
    make(id="tan2a-formula", chapter="trigonometric-equations", title="tan 2A", title_bn="tan ২A", summary="2tanA/(1−tan²A)", latex="\\tan2A=\\frac{2\\tan A}{1-\\tan^2 A}", order=190, trick="ভাজকে ১−tan²A; শূন্য হলে অসংজ্ঞাত।", importance=2),
    make(id="sin3a-cos3a", chapter="trigonometric-equations", title="Triple Angle", title_bn="ত্রিগুণ কোণ", summary="sin3A, cos3A", latex="\\sin3A=3\\sin A-4\\sin^3 A,\\quad \\cos3A=4\\cos^3 A-3\\cos A", order=200, trick="sin3A: 3s−4s³; cos3A: 4c³−3c।", importance=2),
]

STATICS_EXTRA = [
    make(id="friction-limiting", chapter="math-statics", title="Limiting Friction", title_bn="সীমিত ঘর্ষণ", summary="F=μR", latex="F=\\mu R,\\quad \\tan\\lambda=\\mu", order=70, trick="λ = ঘর্ষণ কোণ; ঢালে μ = tan α।", importance=3),
    make(id="inclined-plane-force", chapter="math-statics", title="Force on Inclined Plane", title_bn="ঢালু তলে বল", summary="mg sinθ, mg cosθ", latex="F_{\\parallel}=mg\\sin\\theta,\\quad N=mg\\cos\\theta", order=80, trick="সমান্তরাল = mg sinθ; লম্ব = mg cosθ।", importance=3),
]

DYN_EXTRA = [
    make(id="newton-second-math", chapter="math-dynamics", title="Newton's Second Law", title_bn="নিউটনের দ্বিতীয় সূত্র", summary="F=ma", latex="F=ma=\\frac{dp}{dt}", order=70, trick="গণিতের গতিবিদ্যায় F=ma দিয়ে সমীকরণ গঠন।", importance=3),
    make(id="work-energy-math", chapter="math-dynamics", title="Work–Energy Theorem", title_bn="কাজ–শক্তি উপপাদ্য", summary="W=ΔKE", latex="W=\\frac12 m(v^2-u^2)", order=80, trick="মোট কাজ = গতিশক্তির পরিবর্তন।", importance=2),
]

PHYS_EXTRA = [
    make(id="heat-capacity-specific", chapter="thermodynamics", title="Specific Heat Capacity", title_bn="আপেক্ষিক তাপ", summary="Q=mcΔT", latex="Q=mc\\Delta T,\\quad c=\\frac{Q}{m\\Delta T}", order=140, trick="c = একক ভরে ১° তাপমাত্রা বাড়াতে প্রয়োজনীয় তাপ।", subject="physics", importance=3),
    make(id="latent-heat", chapter="thermodynamics", title="Latent Heat", title_bn="সুপ্ত তাপ", summary="Q=mL", latex="Q=mL", order=150, trick="তাপমাত্রা না বাড়িয়ে দশা পরিবর্তনের তাপ।", subject="physics", importance=2),
    make(id="mirror-magnification", chapter="geometric-optics", title="Magnification", title_bn="বিবর্ধন", summary="m=h'/h=−v/u", latex="m=\\frac{h'}{h}=-\\frac{v}{u}", order=150, trick="ঋণাত্মক m = উল্টো প্রতিবিম্ব।", subject="physics", importance=2),
    make(id="snell-critical-combo", chapter="geometric-optics", title="Relative Refractive Index", title_bn="আপেক্ষিক প্রতিসরাঙ্ক", summary="μ21=μ2/μ1", latex="{}_{1}\\mu_{2}=\\frac{\\mu_2}{\\mu_1}=\\frac{v_1}{v_2}", order=160, trick="আলো দ্রুত মাধ্যম থেকে ধীর মাধ্যমে → μ>1।", subject="physics", importance=2),
]

CHEM_EXTRA = [
    make(id="hess-law", chapter="chemical-equilibrium", title="Hess's Law", title_bn="হেসের সূত্র", summary="ΔH path independent", latex="\\Delta H=\\sum \\Delta H_{\\text{steps}}", order=180, trick="মোট এনথ্যালপি পরিবর্তন পথ-নির্ভর নয়।", subject="chemistry", importance=3),
    make(id="ka-kb-relation", chapter="chemical-equilibrium", title="Ka × Kb = Kw", title_bn="Ka·Kb=Kw", summary="conjugate pair", latex="K_a\\cdot K_b=K_w=10^{-14}\\ (25^\\circ\\mathrm{C})", order=190, trick="কনজুগেট জোড়ায় Ka×Kb=Kw।", subject="chemistry", importance=2),
    make(id="electrochemical-cell-notation", chapter="electrochemistry", title="Cell Notation", title_bn="কোষ প্রতীক", summary="anode|anode||cathode|cathode", latex="\\text{Zn}|\\text{Zn}^{2+}\\|\\text{Cu}^{2+}|\\text{Cu}", order=140, trick="বামে জারণ (অ্যানোড); ডানে বিজারণ (ক্যাথোড)।", subject="chemistry", importance=2),
]

def main():
    write_meta("math", "integration", {"id": "integration", "slug": "integration", "name": "Integration", "nameBn": "যোগজীকরণ", "order": 9})
    write_meta("chemistry", "nuclear-chemistry", {"id": "nuclear-chemistry", "slug": "nuclear-chemistry", "name": "Nuclear Chemistry", "nameBn": "নিউক্লীয় রসায়ন", "order": 8})
    n = 0
    for f in INTEGRATION:
        write_formula("math", "integration", f); n += 1
    for f in NUCLEAR:
        write_formula("chemistry", "nuclear-chemistry", f); n += 1
    for group in (TRIG_EXTRA, STATICS_EXTRA, DYN_EXTRA, PHYS_EXTRA, CHEM_EXTRA):
        for f in group:
            write_formula(f["subjects"][0], f["chapter"], f); n += 1
    print(f"Wrote {n} more formulas")

if __name__ == "__main__":
    main()
