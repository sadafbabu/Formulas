#!/usr/bin/env python3
"""Bulk-generate remaining HSC/admission formula JSON files."""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "subjects"


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
    question: str | None = None,
    answer: str | None = None,
    tags: list[str] | None = None,
    related: list[str] | None = None,
    subject: str = "math",
):
    star = f"{importance}-star"
    base_tags = tags or ["hsc", "eng-admission", "varsity", star]
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
                "question": question or f"{title_bn} এর মূল সূত্রটি লেখো।",
                "answer": answer or latex,
            }
        ],
        "memorize": {"trick": trick, "steps": []},
        "subjects": [subject],
        "related": related or [],
    }


def write_formula(subject: str, chapter: str, data: dict):
    out_dir = ROOT / subject / "chapters" / chapter / "formulas"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{data['id']}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def write_meta(subject: str, chapter: str, meta: dict):
    out_dir = ROOT / subject / "chapters" / chapter
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
        f.write("\n")


# ── Math: Conic Sections ──────────────────────────────────────────────
CONIC_META = {
    "id": "conic-sections",
    "slug": "conic-sections",
    "name": "Conic Sections",
    "nameBn": "কোনিক অংশ",
    "order": 8,
}
CONIC = [
    make(id="parabola-standard", chapter="conic-sections", title="Standard Parabola", title_bn="মানক পরাবৃত্ত", summary="y²=4ax", latex="y^2=4ax", order=10, trick="a>0 হলে x-অক্ষের দিকে; ফোকাস (a,0), ডাইরেক্ট্রিক্স x=−a।", importance=3),
    make(id="parabola-focus-directrix", chapter="conic-sections", title="Parabola Focus & Directrix", title_bn="পরাবৃত্তের ফোকাস ও ডাইরেক্ট্রিক্স", summary="ফোকাস ও ডাইরেক্ট্রিক্স", latex="\\text{Focus }(a,0),\\ \\text{Directrix }x=-a\\ \\text{for }y^2=4ax", order=20, trick="4a = ল্যাটাস রেক্টামের দৈর্ঘ্য; ফোকাস থেকে যেকোনো বিন্দু = ডাইরেক্ট্রিক্সের দূরত্ব।", importance=2),
    make(id="parabola-latus-rectum", chapter="conic-sections", title="Latus Rectum of Parabola", title_bn="পরাবৃত্তের ল্যাটাস রেক্টাম", summary="ল্যাটাস রেক্টাম", latex="\\text{LR}=4a", order=30, trick="LR = 4a — পরাবৃত্তে সবচেয়ে বেশি ব্যবহৃত সংখ্যা।", importance=2),
    make(id="parabola-parametric", chapter="conic-sections", title="Parametric Parabola", title_bn="পরামিতিক পরাবৃত্ত", summary="x=at², y=2at", latex="x=at^2,\\quad y=2at", order=40, trick="t = tan(θ/2) ধরে স্পর্শরেখা সহজ।", importance=2),
    make(id="parabola-tangent", chapter="conic-sections", title="Tangent to Parabola", title_bn="পরাবৃত্তের স্পর্শরেখা", summary="y²=4ax-এ স্পর্শরেখা", latex="yy_1=2a(x+x_1)", order=50, trick="'yy₁ = 2a(x+x₁)' — y²=4ax-এর স্পর্শ সূত্র; T≡0 পদ্ধতি মনে রাখো।", importance=3),
    make(id="ellipse-standard", chapter="conic-sections", title="Standard Ellipse", title_bn="মানক উপবৃত্ত", summary="x²/a²+y²/b²=1", latex="\\frac{x^2}{a^2}+\\frac{y^2}{b^2}=1\\quad(a>b)", order=60, trick="a = বৃহত্তর অর্ধ-অক্ষ; c²=a²−b²; ইকসেন্ট্রিসিটি e=c/a<1।", importance=3),
    make(id="ellipse-foci", chapter="conic-sections", title="Ellipse Foci", title_bn="উপবৃত্তের ফোকাস", summary="ফোকাস (±c,0)", latex="c^2=a^2-b^2,\\ \\text{Foci }(\\pm c,0)", order=70, trick="PF₁+PF₂=2a — উপবৃত্তের সংজ্ঞা; e=c/a।", importance=2),
    make(id="ellipse-eccentricity", chapter="conic-sections", title="Ellipse Eccentricity", title_bn="উপবৃত্তের উপকেন্দ্রতা", summary="e=c/a", latex="e=\\frac{c}{a}=\\sqrt{1-\\frac{b^2}{a^2}}", order=80, trick="0<e<1 উপবৃত্ত; e→0 বৃত্ত; e→1 পাতলা উপবৃত্ত।", importance=2),
    make(id="ellipse-latus-rectum", chapter="conic-sections", title="Ellipse Latus Rectum", title_bn="উপবৃত্তের ল্যাটাস রেক্টাম", summary="LR=2b²/a", latex="\\text{LR}=\\frac{2b^2}{a}", order=90, trick="উপবৃত্তে LR = 2b²/a; পরাবৃত্তে 4a — মিশে যাবে না!", importance=2),
    make(id="ellipse-tangent", chapter="conic-sections", title="Tangent to Ellipse", title_bn="উপবৃত্তের স্পর্শরেখা", summary="স্পর্শ সূত্র", latex="\\frac{xx_1}{a^2}+\\frac{yy_1}{b^2}=1", order=100, trick="x²/a²+y²/b²=1-এ T≡0 দিয়ে স্পর্শ।", importance=2),
    make(id="hyperbola-standard", chapter="conic-sections", title="Standard Hyperbola", title_bn="মানক অধিবৃত্ত", summary="x²/a²−y²/b²=1", latex="\\frac{x^2}{a^2}-\\frac{y^2}{b^2}=1", order=110, trick="c²=a²+b² (উপবৃত্তের উল্টো); e>1; শাখা x=±(b/a)y।", importance=3),
    make(id="hyperbola-foci", chapter="conic-sections", title="Hyperbola Foci", title_bn="অধিবৃত্তের ফোকাস", summary="ফোকাস (±c,0)", latex="c^2=a^2+b^2,\\ \\text{Foci }(\\pm c,0)", order=120, trick="|PF₁−PF₂|=2a — অধিবৃত্ত সংজ্ঞা।", importance=2),
    make(id="hyperbola-asymptotes", chapter="conic-sections", title="Hyperbola Asymptotes", title_bn="অধিবৃত্তের লঘুগামী", summary="y=±(b/a)x", latex="y=\\pm\\frac{b}{a}x", order=130, trick="লঘুগামী x²/a²−y²/b²=0; কেন্দ্রে মিলে।", importance=2),
    make(id="hyperbola-eccentricity", chapter="conic-sections", title="Hyperbola Eccentricity", title_bn="অধিবৃত্তের উপকেন্দ্রতা", summary="e=c/a>1", latex="e=\\frac{c}{a}=\\sqrt{1+\\frac{b^2}{a^2}}>1", order=140, trick="e>1 অধিবৃত্ত; e=1 পরাবৃত্ত; e<1 উপবৃত্ত।", importance=2),
    make(id="hyperbola-rectangular", chapter="conic-sections", title="Rectangular Hyperbola", title_bn="সমকোণী অধিবৃত্ত", summary="xy=c²", latex="xy=c^2,\\quad e=\\sqrt{2}", order=150, trick="xy=c²-এ লঘুগামী y=±x; e=√2 স্থির।", importance=2),
    make(id="hyperbola-tangent", chapter="conic-sections", title="Tangent to Hyperbola", title_bn="অধিবৃত্তের স্পর্শরেখা", summary="স্পর্শ সূত্র", latex="\\frac{xx_1}{a^2}-\\frac{yy_1}{b^2}=1", order=160, trick="উপবৃত্তে +, অধিবৃত্তে − — মাঝের চিহ্নই পার্থক্য।", importance=2),
    make(id="conic-general-second-degree", chapter="conic-sections", title="General Second Degree", title_bn="সাধারণ দ্বিঘাত সমীকরণ", summary="Ax²+Bxy+Cy²+...=0", latex="Ax^2+Bxy+Cy^2+Dx+Ey+F=0", order=170, trick="B²−4AC দিয়ে কোনিক চেনা: <0 উপবৃত্ত, =0 পরাবৃত্ত, >0 অধিবৃত্ত।", importance=2),
    make(id="conic-discriminant-type", chapter="conic-sections", title="Conic Discriminant", title_bn="কোনিক পৃথককারী", summary="B²−4AC", latex="\\Delta=B^2-4AC\\begin{cases}<0 & \\text{ellipse}\\\\=0 & \\text{parabola}\\\\>0 & \\text{hyperbola}\\end{cases}", order=180, trick="Δ=B²−4AC — HSC-তে কোনিক শনাক্তকরণের মূল চাবি।", importance=3),
]

# ── Math: Probability ───────────────────────────────────────────────
PROB_META = {
    "id": "probability",
    "slug": "probability",
    "name": "Probability",
    "nameBn": "সম্ভাব্যতা",
    "order": 9,
}
PROB = [
    make(id="classical-probability", chapter="probability", title="Classical Probability", title_bn="ধ্রুবক সম্ভাব্যতা", summary="P(E)=favourable/total", latex="P(E)=\\frac{n(E)}{n(S)}", order=10, trick="সমান সম্ভাব্য নমুনা বিন্দু ধরে; 0≤P(E)≤1।", importance=3),
    make(id="complement-probability", chapter="probability", title="Complement Rule", title_bn="পরিপূরক নিয়ম", summary="P(E')=1−P(E)", latex="P(E')=1-P(E)", order=20, trick="'ঘটবে না' = 1 − 'ঘটবে' — সবচেয়ে দ্রুত পদ্ধতি।", importance=3),
    make(id="addition-rule-probability", chapter="probability", title="Addition Rule", title_bn="যোগ নিয়ম", summary="P(A∪B)", latex="P(A\\cup B)=P(A)+P(B)-P(A\\cap B)", order=30, trick="মিলিত = A+B−AB; পরস্পর বর্জন হলে AB=0।", importance=3),
    make(id="mutually-exclusive-probability", chapter="probability", title="Mutually Exclusive Events", title_bn="পরস্পর বর্জন ঘটনা", summary="P(A∩B)=0", latex="P(A\\cap B)=0\\Rightarrow P(A\\cup B)=P(A)+P(B)", order=40, trick="একসাথে ঘটতে পারে না → সরাসরি যোগ।", importance=2),
    make(id="conditional-probability", chapter="probability", title="Conditional Probability", title_bn="শর্তাধীন সম্ভাব্যতা", summary="P(A|B)", latex="P(A|B)=\\frac{P(A\\cap B)}{P(B)}", order=50, trick="B ঘটেছে ধরে A-এর সম্ভাব্যতা; ভajra = P(A∩B)/P(B)。", importance=3),
    make(id="multiplication-rule-probability", chapter="probability", title="Multiplication Rule", title_bn="গুণ নিয়ম", summary="P(A∩B)", latex="P(A\\cap B)=P(A)\\,P(B|A)=P(B)\\,P(A|B)", order=60, trick="ক্রমিক ঘটনায় গুণ; স্বাধীন হলে P(B|A)=P(B)。", importance=3),
    make(id="independent-events-probability", chapter="probability", title="Independent Events", title_bn="স্বাধীন ঘটনা", summary="P(A∩B)=P(A)P(B)", latex="P(A\\cap B)=P(A)P(B)", order=70, trick="একটির ঘটনা অন্যটিকে প্রভাবিত করে না → গুণ।", importance=3),
    make(id="bayes-theorem", chapter="probability", title="Bayes' Theorem", title_bn="বেইজের উপপাদ্য", summary="পosterior সম্ভাব্যতা", latex="P(A|B)=\\frac{P(B|A)P(A)}{P(B)}", order=80, trick="P(B|A)P(A)/P(B) — উল্টো শর্তাধীন সম্ভাব্যতা।", importance=3),
    make(id="total-probability-theorem", chapter="probability", title="Total Probability", title_bn="মোট সম্ভাব্যতা উপপাদ্য", summary="P(B)=ΣP(Aᵢ)P(B|Aᵢ)", latex="P(B)=\\sum_i P(A_i)P(B|A_i)", order=90, trick="বিভাজিত নমুনা ক্ষেত্র; Bayes-এর সাথে জোড়া।", importance=2),
    make(id="binomial-probability", chapter="probability", title="Binomial Probability", title_bn="দ্বিপদী সম্ভাব্যতা", summary="nCr p^r q^(n−r)", latex="P(X=r)=\\binom{n}{r}p^r(1-p)^{n-r}", order=100, trick="n বার স্বাধীন trial; সফল r বার; q=1−p。", importance=3),
    make(id="binomial-mean-variance", chapter="probability", title="Binomial Mean & Variance", title_bn="দ্বিপদী গড় ও বিচ্যুতি", summary="μ=np, σ²=npq", latex="\\mu=np,\\quad \\sigma^2=np(1-p)", order=110, trick="গড়=np; বিচ্যুতি=npq — সূত্র মুখস্থ।", importance=2),
    make(id="geometric-probability", chapter="probability", title="Geometric Probability", title_bn="জ্যামিতিক সম্ভাব্যতা", summary="অঞ্চলের অনুপাত", latex="P=\\frac{\\text{favourable length/area}}{\\text{total length/area}}", order=120, trick="এক সমান সম্ভাব্য বিন্দু → দৈর্ঘ্য/ক্ষেত্রফল অনুপাত。", importance=1),
    make(id="permutation-probability", chapter="probability", title="Permutation in Probability", title_bn="ক্রমবিন্যাসে সম্ভাব্যতা", summary="n!/(n−r)!", latex="P=\\frac{\\text{favourable permutations}}{n!}", order=130, trick="ক্রম গুরুত্বপূর্ণ হলে nCr নয় nPr。", importance=2),
    make(id="expected-value", chapter="probability", title="Expected Value", title_bn="প্রত্যাশিত মান", summary="E(X)=ΣxP(x)", latex="E(X)=\\sum x\\,P(x)", order=140, trick="গড় = Σ(মান × সম্ভাব্যতা); MCQ-তে দ্রুত।", importance=2),
]

# ── Math: 3D Coordinate Geometry ────────────────────────────────────
COORD3D_META = {
    "id": "coordinate-geometry-3d",
    "slug": "coordinate-geometry-3d",
    "name": "3D Coordinate Geometry",
    "nameBn": "ত্রিমাত্রিক স্থানাঙ্ক জ্যামিতি",
    "order": 10,
}
COORD3D = [
    make(id="distance-3d", chapter="coordinate-geometry-3d", title="Distance in 3D", title_bn="ত্রিমাত্রিক দূরত্ব", summary="দুই বিন্দুর দূরত্ব", latex="d=\\sqrt{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}", order=10, trick="2D-এর √(Δx²+Δy²)-এ z যোগ — একই ধরন।", importance=3),
    make(id="section-formula-3d", chapter="coordinate-geometry-3d", title="Section Formula 3D", title_bn="অংশন সূত্র (৩D)", summary="m:n অনুপাতে", latex="\\left(\\frac{mx_2+nx_1}{m+n},\\frac{my_2+ny_1}{m+n},\\frac{mz_2+nz_1}{m+n}\\right)", order=20, trick="2D section formula-এ z যোগ করলেই হয়。", importance=2),
    make(id="direction-cosines", chapter="coordinate-geometry-3d", title="Direction Cosines", title_bn="দিক্‌কোসাইন", summary="l²+m²+n²=1", latex="l^2+m^2+n^2=1", order=30, trick="দিক্‌কোসাইনের বর্গের যোগফল = 1 — সবসময়।", importance=3),
    make(id="direction-ratios", chapter="coordinate-geometry-3d", title="Direction Ratios", title_bn="দিক্‌অনুপাত", summary="a,b,c", latex="\\frac{l}{a}=\\frac{m}{b}=\\frac{n}{c}", order=40, trick="DR (a,b,c) → DC l=a/√(a²+b²+c²)।", importance=2),
    make(id="angle-between-lines-3d", chapter="coordinate-geometry-3d", title="Angle Between Lines 3D", title_bn="৩D-এ রেখার মধ্যবর্তী কোণ", summary="cosθ=|l₁l₂+m₁m₂+n₁n₂|", latex="\\cos\\theta=|l_1l_2+m_1m_2+n_1n_2|", order=50, trick="DC-এর dot product; DR দিয়ে সহজ।", importance=2),
    make(id="line-equation-3d-vector", chapter="coordinate-geometry-3d", title="Line Vector Form", title_bn="রেখার ভেক্টর রূপ", summary="r=a+λb", latex="\\vec r=\\vec a+\\lambda\\vec b", order=60, trick="a = বিন্দু, b = দিক্‌ভেক্টর; λ = প্যারামিটার。", importance=2),
    make(id="line-equation-3d-cartesian", chapter="coordinate-geometry-3d", title="Line Cartesian Form", title_bn="রেখার কার্টেসীয় রূপ", summary="(x−x₁)/a=...", latex="\\frac{x-x_1}{a}=\\frac{y-y_1}{b}=\\frac{z-z_1}{c}", order=70, trick="DR (a,b,c) এবং বিন্দু (x₁,y₁,z₁)。", importance=3),
    make(id="shortest-distance-skew-lines", chapter="coordinate-geometry-3d", title="Skew Lines Distance", title_bn="অসন্মিল রেখার লম্ব দূরত্ব", summary="দুই অসন্মিল রেখা", latex="d=\\frac{|(\\vec b_1\\times\\vec b_2)\\cdot(\\vec a_2-\\vec a_1)|}{|\\vec b_1\\times\\vec b_2|}", order=80, trick="cross × dot; পরস্পর ছেদ করে না → skew。", importance=2),
    make(id="plane-normal-form", chapter="coordinate-geometry-3d", title="Plane Normal Form", title_bn="সমতলের লম্ব রূপ", summary="lx+my+nz=p", latex="lx+my+nPz=p", order=90, trick="স্বাভাবিক ভেক্টর (l,m,n); মূল থেকে দূর p。", importance=2),
    make(id="plane-general-form", chapter="coordinate-geometry-3d", title="Plane General Form", title_bn="সমতলের সাধারণ রূপ", summary="Ax+By+Cz+D=0", latex="Ax+By+Cz+D=0", order=100, trick="স্বাভাবিক (A,B,C); D দিয়ে অবস্থান নির্ধারণ。", importance=3),
    make(id="angle-between-planes", chapter="coordinate-geometry-3d", title="Angle Between Planes", title_bn="সমতলের মধ্যবর্তী কোণ", summary="cosθ", latex="\\cos\\theta=\\frac{|A_1A_2+B_1B_2+C_1C_2|}{\\sqrt{A_1^2+B_1^2+C_1^2}\\sqrt{A_2^2+B_2^2+C_2^2}}", order=110, trick="স্বাভাবিক ভেক্টরের dot product。", importance=2),
    make(id="sphere-equation", chapter="coordinate-geometry-3d", title="Sphere Equation", title_bn="গোলকের সমীকরণ", summary="(x−a)²+...", latex="(x-a)^2+(y-b)^2+(z-c)^2=r^2", order=120, trick="কেন্দ্র (a,b,c), ব্যাসার্ধ r; 2D বৃত্তের 3D সংস্করণ。", importance=3),
]

# Fix typo in plane-normal-form
COORD3D[8]["latex"] = "lx+my+nz=p"

# ── Math: Sets & Functions ────────────────────────────────────────────
SETS_META = {
    "id": "sets-functions",
    "slug": "sets-functions",
    "name": "Sets & Functions",
    "nameBn": "সেট ও ফাংশন",
    "order": 1,
}
SETS = [
    make(id="set-union", chapter="sets-functions", title="Set Union", title_bn="সেটের যোগ", summary="A∪B", latex="A\\cup B=\\{x:x\\in A\\text{ or }x\\in B\\}", order=10, trick="∪ = union = যোগ; Venn-এ দুই বৃত্ত মিল।", importance=2),
    make(id="set-intersection", chapter="sets-functions", title="Set Intersection", title_bn="সেটের ছেদ", summary="A∩B", latex="A\\cap B=\\{x:x\\in A\\text{ and }x\\in B\\}", order=20, trick="∩ = intersection = ছেদ; common elements。", importance=2),
    make(id="set-complement", chapter="sets-functions", title="Set Complement", title_bn="পরিপূরক সেট", summary="A'", latex="A'=U\\setminus A", order=30, trick="Universal set-এ যা A-তে নেই = A'。", importance=2),
    make(id="set-difference", chapter="sets-functions", title="Set Difference", title_bn="সেটের পার্থক্য", summary="A−B", latex="A\\setminus B=\\{x:x\\in A,\\ x\\notin B\\}", order=40, trick="A-তে আছে কিন্তু B-তে নেই。", importance=2),
    make(id="de-morgan-sets", chapter="sets-functions", title="De Morgan's Laws (Sets)", title_bn="ডি মরগানের সূত্র (সেট)", summary="(A∪B)'=(A'∩B')", latex="(A\\cup B)'=A'\\cap B'\\quad;(A\\cap B)'=A'\\cup B'", order=50, trick="Union↔Intersection উল্টো; complement বাইরে।", importance=2),
    make(id="cartesian-product", chapter="sets-functions", title="Cartesian Product", title_bn="কার্তesian গুণফল", summary="A×B", latex="A\\times B=\\{(a,b):a\\in A,\\ b\\in B\\}", order=60, trick="|A×B|=|A|·|B|; ordered pair。", importance=2),
    make(id="function-definition", chapter="sets-functions", title="Function Definition", title_bn="ফাংশনের সংজ্ঞা", summary="f:A→B", latex="f:A\\to B,\\quad \\forall a\\in A\\ \\exists!\\ b\\in B\\text{ s.t. }f(a)=b", order=70, trick="প্রতিটি input-এ exactly এক output — MCQ-তে function test。", importance=2),
    make(id="function-composition", chapter="sets-functions", title="Function Composition", title_bn="ফাংশনের সংযোজন", summary="(f∘g)(x)", latex="(f\\circ g)(x)=f(g(x))", order=80, trick="g আগে, f পরে; fog ≠ gof সাধারণত。", importance=3),
    make(id="inverse-function", chapter="sets-functions", title="Inverse Function", title_bn=" বিপরীত ফাংশন", summary="f⁻¹", latex="f^{-1}(f(x))=x\\quad\\text{and}\\quad f(f^{-1}(y))=y", order=90, trick="f⁻¹ exists iff f one-to-one; graph = mirror y=x。", importance=2),
    make(id="even-odd-function", chapter="sets-functions", title="Even & Odd Functions", title_bn="জোড় ও বিজোড় ফাংশন", summary="f(−x)", latex="f(-x)=f(x)\\text{ (even)};\\quad f(-x)=-f(x)\\text{ (odd)}", order=100, trick="Even → y-axis symmetry; Odd → origin symmetry。", importance=2),
]

# Fix title typo
SETS[8]["titleBn"] = "বিপরীত ফাংশন"

# ── Math: Statics ─────────────────────────────────────────────────────
STATICS_META = {
    "id": "math-statics",
    "slug": "math-statics",
    "name": "Statics (Math)",
    "nameBn": "স্থিতিবিদ্যা (গণিত)",
    "order": 10,
}
STATICS = [
    make(id="equilibrium-forces", chapter="math-statics", title="Equilibrium of Forces", title_bn="বলের সাম্যাবস্থা", summary="ΣF=0", latex="\\sum F_x=0,\\quad \\sum F_y=0", order=10, trick="সাম্য = x ও y-তে বলের যোগফল শূন্য。", importance=3),
    make(id="triangle-of-forces", chapter="math-statics", title="Triangle of Forces", title_bn="বলের ত্রিভুজ", summary="Lami's theorem", latex="\\frac{F_1}{\\sin\\alpha}=\\frac{F_2}{\\sin\\beta}=\\frac{F_3}{\\sin\\gamma}", order=20, trick="তিন বল সাম্য → Lami: F/sin( opposite angle )。", importance=3),
    make(id="lami-theorem", chapter="math-statics", title="Lami's Theorem", title_bn="লামির উপপাদ্য", summary="তিন বল সাম্য", latex="\\frac{P}{\\sin\\alpha}=\\frac{Q}{\\sin\\beta}=\\frac{R}{\\sin\\gamma}", order=30, trick="প্রতিটি বল বিপরীত কোণের sin-এ ভাগ。", importance=3),
    make(id="moment-of-force", chapter="math-statics", title="Moment of Force", title_bn="বলের ভ্রাম", summary="τ=Fd", latex="\\tau=F\\,d\\,\\sin\\theta", order=40, trick="τ = F × ⊥ distance; d⊥ = d sinθ。", importance=2),
    make(id="couple-moment", chapter="math-statics", title="Couple Moment", title_bn="দম্পতি বলের ভ্রাম", summary="M=Fd", latex="M=F\\,d", order=50, trick="দুই সমান বিপরীত বল; moment = F×distance between。", importance=2),
    make(id="parallel-forces-resultant", chapter="math-statics", title="Resultant of Parallel Forces", title_bn="সমান্তরাল বলের লব্ধি", summary="R=ΣF", latex="R=\\sum F_i,\\quad \\bar{x}=\\frac{\\sum F_i x_i}{\\sum F_i}", order=60, trick="লব্ধি = যোগ; moment arm দিয়ে অবস্থান。", importance=2),
]

# ── Math: Dynamics (projectile) ───────────────────────────────────────
DYNAMICS_META = {
    "id": "math-dynamics",
    "slug": "math-dynamics",
    "name": "Dynamics (Math)",
    "nameBn": "গতিবিদ্যা (গণিত)",
    "order": 11,
}
DYNAMICS = [
    make(id="projectile-range", chapter="math-dynamics", title="Projectile Range", title_bn="ক্ষিপ্ত বস্তুর পালা", summary="R=u²sin2θ/g", latex="R=\\frac{u^2\\sin 2\\theta}{g}", order=10, trick="45°-এ max range; R=u²sin2θ/g — HSC favorite。", importance=3),
    make(id="projectile-max-height", chapter="math-dynamics", title="Maximum Height", title_bn="সর্বোচ্চ উচ্চতা", summary="H=u²sin²θ/2g", latex="H=\\frac{u^2\\sin^2\\theta}{2g}", order=20, trick="শুধু vertical component u sinθ; H=v²/2g。", importance=3),
    make(id="projectile-time-of-flight", chapter="math-dynamics", title="Time of Flight", title_bn="উড্ডয়নকাল", summary="T=2u sinθ/g", latex="T=\\frac{2u\\sin\\theta}{g}", order=30, trick="উঠা + নামা = 2u sinθ/g。", importance=3),
    make(id="projectile-equation-path", chapter="math-dynamics", title="Projectile Path", title_bn="ক্ষিপ্ত পথের সমীকরণ", summary="y=x tanθ−...", latex="y=x\\tan\\theta-\\frac{gx^2}{2u^2\\cos^2\\theta}", order=40, trick="x elim করে parabolic path; g/2u²cos²θ coefficient。", importance=2),
    make(id="projectile-velocity-components", chapter="math-dynamics", title="Velocity Components", title_bn="বেগের উপাদিসমূহ", summary="u cosθ, u sinθ", latex="v_x=u\\cos\\theta,\\quad v_y=u\\sin\\theta-gt", order=50, trick="Horizontal = constant; vertical = u sinθ − gt。", importance=2),
    make(id="projectile-range-max-angle", chapter="math-dynamics", title="Max Range Angle", title_bn="সর্বোচ্চ পালার কোণ", summary="θ=45°", latex="R_{\\max}=\\frac{u^2}{g}\\quad\\text{at }\\theta=45^\\circ", order=60, trick="sin2θ max at 45°; same level থেকে ছোড়লে。", importance=2),
]

# ── Math: Linear Programming ──────────────────────────────────────────
LP_META = {
    "id": "linear-programming",
    "slug": "linear-programming",
    "name": "Linear Programming",
    "nameBn": "রৈখিক প্রোগ্রামিং",
    "order": 11,
}
LP = [
    make(id="lp-objective-function", chapter="linear-programming", title="Objective Function", title_bn="উদ্দেশ্য ফাংশন", summary="Z=ax+by", latex="Z=ax+by", order=10, trick="Maximize বা Minimize করতে হবে Z = ax+by。", importance=2),
    make(id="lp-feasible-region", chapter="linear-programming", title="Feasible Region", title_bn="সম্ভাব্য অঞ্চল", summary="constraints-এর ছেদ", latex="\\text{Feasible region = intersection of constraint half-planes}", order=20, trick="সব constraint একসাথে plot → bounded/unbounded region。", importance=2),
    make(id="lp-corner-point", chapter="linear-programming", title="Corner Point Method", title_bn="কোণ বিন্দু পদ্ধতি", summary="vertices-এ Z মান", latex="Z_{\\max/\\min}\\text{ at a corner point of feasible region}", order=30, trick="Optimum ALWAYS at corner — graph-এ vertex-গুলোতে Z বসাও。", importance=3),
    make(id="lp-constraint-inequality", chapter="linear-programming", title="Constraint Inequality", title_bn="সীমাবদ্ধতা অসমতা", summary="ax+by≤c", latex="ax+by\\le c", order=40, trick="≤ → origin side feasible (coefficients positive হলে)。", importance=2),
]

# ── Chemistry: Colligative Properties ─────────────────────────────────
COLLIG_META = {
    "id": "colligative-properties",
    "slug": "colligative-properties",
    "name": "Colligative Properties",
    "nameBn": "সম্মিল গুণ",
    "order": 3,
}
COLLIG = [
    make(id="relative-lowering-vapour-pressure", chapter="colligative-properties", title="Relative Lowering of V.P.", title_bn="বাষ্পচাপের আপেক্ষিক হ্রাস", summary="(P°−P)/P°", latex="\\frac{P^\\circ-P}{P^\\circ}=x_B=\\frac{n_B}{n_A+n_B}", order=10, trick="ΔP/P° = mole fraction of solute; Raoult's law base。", subject="chemistry", importance=3),
    make(id="elevation-boiling-point", chapter="colligative-properties", title="Elevation of Boiling Point", title_bn="স্ফুটনাঙ্কের উচ্চায়ন", summary="ΔTb=Kbm", latex="\\Delta T_b=K_b m", order=20, trick="ΔTb = Kb × molality; Ebullioscopic constant。", subject="chemistry", importance=3),
    make(id="depression-freezing-point", chapter="colligative-properties", title="Depression of Freezing Point", title_bn="স্থাযোগাঙ্কের অবনমন", summary="ΔTf=Kfm", latex="\\Delta T_f=K_f m", order=30, trick="ΔTf = Kf × m; Cryoscopic constant。", subject="chemistry", importance=3),
    make(id="osmotic-pressure", chapter="colligative-properties", title="Osmotic Pressure", title_bn="প্রস্বেদ চাপ", summary="π=CRT", latex="\\pi=CRT=MRT", order=40, trick="π = CRT — dilute solution; van't Hoff factor i multiply。", subject="chemistry", importance=3),
    make(id="vant-hoff-factor", chapter="colligative-properties", title="van't Hoff Factor", title_bn="ভ্যান't হফ গুণক", summary="i=observed/calculated", latex="i=\\frac{\\text{observed colligative property}}{\\text{calculated (no dissociation)}}", order=50, trick="Electrolyte-এ i>1; association-এ i<1。", subject="chemistry", importance=2),
    make(id="raoult-law", chapter="colligative-properties", title="Raoult's Law", title_bn="রাউলের সূত্র", summary="P=PA°xA", latex="P=P_A^\\circ x_A+P_B^\\circ x_B", order=60, trick="Ideal solution: P = Σ Pi° xi; vapor pressure lowering。", subject="chemistry", importance=3),
    make(id="colligative-molecular-mass", chapter="colligative-properties", title="Molar Mass from Colligative", title_bn="সম্মিল গুণ থেকে mol ভর", summary="M from ΔTb or π", latex="M=\\frac{K_b w_B}{\\Delta T_b w_A}", order=70, trick="ΔTb বা π দিয়ে molar mass — HSC numerical favorite。", subject="chemistry", importance=2),
]

# ── Chemistry: Solid State ────────────────────────────────────────────
SOLID_META = {
    "id": "solid-state-chemistry",
    "slug": "solid-state-chemistry",
    "name": "Solid State Chemistry",
    "nameBn": "কঠিন অবস্থা",
    "order": 5,
}
SOLID = [
    make(id="unit-cell-atoms", chapter="solid-state-chemistry", title="Atoms per Unit Cell", title_bn="একক কোষে পরমাণু", summary="Z=?", latex="Z=\\text{contribution from all corner/face/edge atoms}", order=10, trick="Corner=1/8, Face=1/2, Edge=1/4, Body=1 — add up。", subject="chemistry", importance=3),
    make(id="packing-efficiency", chapter="solid-state-chemistry", title="Packing Efficiency", title_bn="প্যাকিং দক্ষতা", summary="volume occupied", latex="\\text{PE}=\\frac{\\text{volume of atoms}}{\\text{volume of unit cell}}\\times100\\%", order=20, trick="SC=52%, BCC=68%, FCC/HCP=74% — memorize。", subject="chemistry", importance=2),
    make(id="density-unit-cell", chapter="solid-state-chemistry", title="Density from Unit Cell", title_bn="একক কোষ থেকে ঘনত্ব", summary="d=ZM/Na³", latex="d=\\frac{ZM}{N_A a^3}", order=30, trick="Z=atoms/cell, M=molar mass, a=edge length。", subject="chemistry", importance=3),
    make(id="bragg-equation", chapter="solid-state-chemistry", title="Bragg's Equation", title_bn="ব্র্যাগের সমীকরণ", summary="nλ=2d sinθ", latex="n\\lambda=2d\\sin\\theta", order=40, trick="X-ray diffraction; n=order, d=interplanar spacing。", subject="chemistry", importance=2),
    make(id="schottky-defect", chapter="solid-state-chemistry", title="Schottky Defect", title_bn="শটকি ত্রুটি", summary="cation+anion vacancy", latex="\\text{Schottky: equal cation and anion vacancies}", order=50, trick="Ionic solid-এ দুই vacancy; density decreases。", subject="chemistry", importance=1),
]

# ── Chemistry: Coordination Chemistry ─────────────────────────────────
COORD_META = {
    "id": "coordination-chemistry",
    "slug": "coordination-chemistry",
    "name": "Coordination Chemistry",
    "nameBn": "সমন্বয় রসায়ন",
    "order": 5,
}
COORD = [
    make(id="coordination-number", chapter="coordination-chemistry", title="Coordination Number", title_bn="সমন্বয় সংখ্যা", summary="CN=?", latex="\\text{CN}=\\text{number of donor atoms bonded to central metal}", order=10, trick="Ligand donor atoms count; common CN=4,6。", subject="chemistry", importance=2),
    make(id="effective-atomic-number", chapter="coordination-chemistry", title="Effective Atomic Number", title_bn="কার্যকর পরমাণু সংখ্যা", summary="EAN rule", latex="\\text{EAN}=Z-\\text{oxidation state}+2\\times\\text{CN}", order=20, trick="EAN ≈ next noble gas (18 or 36) → stable complex。", subject="chemistry", importance=2),
    make(id="werner-primary-secondary", chapter="coordination-chemistry", title="Werner's Theory", title_bn="ভার্নারের তত্ত্ব", summary="primary+secondary valence", latex="\\text{Primary valence = ionizable; Secondary = non-ionizable}", order=30, trick="Primary = oxidation state; Secondary = coordination。", subject="chemistry", importance=2),
    make(id="crystal-field-splitting", chapter="coordination-chemistry", title="Crystal Field Splitting", title_bn="ক্রিস্টাল ক্ষেত্র বিভাজন", summary="Δ₀", latex="\\Delta_0=\\text{energy gap between }e_g\\text{ and }t_{2g}", order=40, trick="Octahedral: eg vs t2g; color from d-d transition。", subject="chemistry", importance=2),
    make(id="magnetic-moment-spin-only", chapter="coordination-chemistry", title="Spin-Only Magnetic Moment", title_bn="স্পিন-মাত্র চৌম্বক মুহূর্ত", summary="μ=√n(n+2) BM", latex="\\mu=\\sqrt{n(n+2)}\\ \\text{BM}", order=50, trick="n=unpaired electrons; √n(n+2) BM formula。", subject="chemistry", importance=3),
]

# ── Chemistry: Industrial Chemistry ───────────────────────────────────
IND_META = {
    "id": "industrial-chemistry",
    "slug": "industrial-chemistry",
    "name": "Industrial Chemistry",
    "nameBn": "শিল্প রসায়ন",
    "order": 6,
}
IND = [
    make(id="haber-process", chapter="industrial-chemistry", title="Haber Process", title_bn="হ্যাবার পদ্ধতি", summary="N₂+3H₂⇌2NH₃", latex="\\ce{N2 + 3H2 <=> 2NH3};\\quad \\Delta H=-92\\ \\text{kJ/mol}", order=10, trick="450°C, 200 atm, Fe catalyst; exothermic → low T favors product。", subject="chemistry", importance=3),
    make(id="contact-process", chapter="industrial-chemistry", title="Contact Process", title_bn="কন্টাক্ট পদ্ধতি", summary="SO₂→SO₃→H₂SO₄", latex="\\ce{2SO2 + O2 <=> 2SO3};\\quad \\ce{SO3 + H2SO4 -> H2S2O7 -> 2H2SO4}", order=20, trick="V₂O₅ catalyst; oleum intermediate H₂S₂O₇。", subject="chemistry", importance=2),
    make(id="ostwald-process", chapter="industrial-chemistry", title="Ostwald Process", title_bn="অস্টওয়াল্ড পদ্ধতি", summary="NH₃→HNO₃", latex="\\ce{4NH3 + 5O2 -> 4NO + 6H2O};\\quad \\ce{NO -> NO2 -> HNO3}", order=30, trick="Ammonia oxidation → NO → NO₂ → HNO₃; Pt catalyst。", subject="chemistry", importance=2),
    make(id="solvay-process", chapter="industrial-chemistry", title="Solvay Process", title_bn="সলভে পদ্ধতি", summary="Na₂CO₃ production", latex="\\ce{2NaCl + CaCO3 -> Na2CO3 + CaCl2}", order=40, trick="NH₃ + CO₂ + brine → NaHCO₃ → Na₂CO₃; byproduct CaCl₂。", subject="chemistry", importance=2),
]

# ── Expansions to existing chapters ───────────────────────────────────
EXPANSIONS = [
    # matrix-determinant
    make(id="matrix-inverse-formula", chapter="matrix-determinant", title="Matrix Inverse", title_bn="ম্যাট্রিক্সের বিপরীত", summary="A⁻¹=adj(A)/|A|", latex="A^{-1}=\\frac{\\operatorname{adj}(A)}{|A|}", order=50, trick="adj(A)/|A|; |A|≠0 হলে inverse exists。", importance=3),
    make(id="cramers-rule", chapter="matrix-determinant", title="Cramer's Rule", title_bn="ক্রেমারের নিয়ম", summary="x=Δx/Δ", latex="x=\\frac{\\Delta_x}{\\Delta},\\quad y=\\frac{\\Delta_y}{\\Delta}", order=60, trick="Δ=main determinant; Δx = x-column replace。", importance=2),
    make(id="determinant-properties", chapter="matrix-determinant", title="Determinant Properties", title_bn="নির্ণায়কের ধর্ম", summary="row interchange", latex="|A^T|=|A|;\\quad |AB|=|A||B|", order=70, trick="Row swap → sign change; two equal rows → det=0。", importance=2),
    # permutation-combination
    make(id="circular-permutation", chapter="permutation-combination", title="Circular Permutation", title_bn="বৃত্তাকার ক্রম", summary="(n−1)!", latex="P_{\\text{circular}}=(n-1)!", order=50, trick="Linear n! → Circular (n−1)!; one fixed point。", importance=2),
    make(id="combination-formula", chapter="permutation-combination", title="Combination Formula", title_bn="সমাবেশ সূত্র", summary="nCr", latex="\\binom{n}{r}=\\frac{n!}{r!(n-r)!}", order=60, trick="nCr = nPr/r!; order doesn't matter。", importance=3),
    make(id="permutation-formula", chapter="permutation-combination", title="Permutation Formula", title_bn="ক্রমবিন্যাস সূত্র", summary="nPr", latex="P(n,r)=\\frac{n!}{(n-r)!}", order=70, trick="Order matters → nPr; n!/(n−r)!。", importance=3),
    make(id="combination-identities", chapter="permutation-combination", title="Combination Identities", title_bn="সমাবেশ পরিচয়", summary="nC0+nC1+...", latex="\\binom{n}{0}+\\binom{n}{1}+\\cdots+\\binom{n}{n}=2^n", order=80, trick="Binomial row sum = 2^n; Pascal's triangle。", importance=2),
    # straight-lines
    make(id="slope-intercept-form", chapter="straight-lines", title="Slope-Intercept Form", title_bn="ঢাল-ছেদ রূপ", summary="y=mx+c", latex="y=mx+c", order=140, trick="m=slope, c=y-intercept; quick graphing。", importance=2),
    make(id="point-slope-form", chapter="straight-lines", title="Point-Slope Form", title_bn="বিন্দু-ঢাল রূপ", summary="y−y₁=m(x−x₁)", latex="y-y_1=m(x-x_1)", order=150, trick="One point + slope → line equation。", importance=2),
    make(id="normal-form-line", chapter="straight-lines", title="Normal Form of Line", title_bn="রেখার লম্ব রূপ", summary="x cosα+y sinα=p", latex="x\\cos\\alpha+y\\sin\\alpha=p", order=160, trick="p = perpendicular from origin; α = angle with x-axis。", importance=2),
    # calculus
    make(id="integration-by-parts", chapter="calculus", title="Integration by Parts", title_bn="অংশীয় যোগজীকরণ", summary="∫u dv", latex="\\int u\\,dv=uv-\\int v\\,du", order=160, trick="LIATE: Log, Inverse, Algebraic, Trig, Exp — choose u。", importance=3),
    make(id="partial-fractions", chapter="calculus", title="Partial Fractions", title_bn="আংশিক ভগ্নাংশ", summary="decompose rational", latex="\\frac{P(x)}{Q(x)}=\\sum\\frac{A_i}{(x-a_i)^{n_i}}", order=170, trick="Denominator factor → A/(x−a) terms; then integrate。", importance=2),
    make(id="trapezoidal-rule", chapter="calculus", title="Trapezoidal Rule", title_bn="টrapezoidal নিয়ম", summary="numerical integration", latex="\\int_a^b f(x)\\,dx\\approx\\frac{h}{2}[y_0+2(y_1+\\cdots+y_{n-1})+y_n]", order=180, trick="h=(b−a)/n; end points once, middle twice。", importance=1),
    # trigonometric-equations
    make(id="general-solution-sin", chapter="trigonometric-equations", title="General Solution sinθ=k", title_bn="sinθ=k-এর সাধারণ সমাধান", summary="θ=nπ+(−1)ⁿα", latex="\\theta=n\\pi+(-1)^n\\alpha,\\quad \\sin\\alpha=k", order=150, trick="Principal α first; then nπ+(−1)ⁿα pattern。", importance=3),
    make(id="general-solution-cos", chapter="trigonometric-equations", title="General Solution cosθ=k", title_bn="cosθ=k-এর সাধারণ সমাধান", summary="θ=2nπ±α", latex="\\theta=2n\\pi\\pm\\alpha,\\quad \\cos\\alpha=k", order=160, trick="±α symmetry; 2nπ period for cos。", importance=3),
    make(id="general-solution-tan", chapter="trigonometric-equations", title="General Solution tanθ=k", title_bn="tanθ=k-এর সাধারণ সমাধান", summary="θ=nπ+α", latex="\\theta=n\\pi+\\alpha,\\quad \\tan\\alpha=k", order=170, trick="Period π (not 2π) for tan; simpler than sin/cos。", importance=2),
    # physics properties-of-matter
    make(id="hydrostatic-pressure", chapter="properties-of-matter", title="Hydrostatic Pressure", title_bn="স্থিতিস্থাপক চাপ", summary="P=hρg", latex="P=h\\rho g", order=90, trick="P = hρg; depth increases → pressure increases。", subject="physics", importance=3),
    make(id="pascals-law", chapter="properties-of-matter", title="Pascal's Law", title_bn="প্যাসকেলের সূত্র", summary="pressure transmitted", latex="\\frac{F_1}{A_1}=\\frac{F_2}{A_2}", order=100, trick="Hydraulic lift: small force × large distance = large force × small distance。", subject="physics", importance=2),
    # physics thermodynamics
    make(id="stefan-boltzmann-law", chapter="thermodynamics", title="Stefan-Boltzmann Law", title_bn="স্টিফান-বোল্টজম্যান সূত্র", summary="P=σAT⁴", latex="P=\\sigma A T^4", order=120, trick="Radiated power ∝ T⁴; σ=5.67×10⁻⁸ W/m²K⁴。", subject="physics", importance=2),
    # physics current-electricity
    make(id="rc-charging", chapter="current-electricity", title="RC Charging", title_bn="RC চarging", summary="q=Q(1−e^(−t/RC))", latex="q=Q(1-e^{-t/RC}),\\quad Q=CV", order=130, trick="τ=RC time constant; 63% charge at t=τ。", subject="physics", importance=2),
    # physics wave-optics
    make(id="thin-film-interference", chapter="wave-optics", title="Thin Film Interference", title_bn="অপাতল স্তরে ব্যতিচার", summary="2nt=(m+½)λ", latex="2nt=\\left(m+\\tfrac{1}{2}\\right)\\lambda", order=110, trick="Phase reversal at one surface → half wavelength path difference。", subject="physics", importance=2),
    # chemistry qualitative
    make(id="gas-density-formula", chapter="qualitative-chem", title="Gas Density", title_bn="গ্যাসের ঘনত্ব", summary="d=PM/RT", latex="d=\\frac{PM}{RT}", order=170, trick="From PV=nRT → d=PM/RT; compare molar masses at same P,T。", subject="chemistry", importance=2),
    make(id="iodoform-test", chapter="qualitative-chem", title="Iodoform Test", title_bn="আয়োডোফর্ম পরীক্ষা", summary="CH₃CO− group", latex="\\ce{CH3CO-R + 3I2 + 4NaOH -> CHI3 + RCOONa + 3NaI + 2H2O}", order=180, trick="Methyl ketone or CH₃CH(OH)− → yellow CHI₃ precipitate。", subject="chemistry", importance=2),
    # chemistry organic
    make(id="fehling-test", chapter="organic-chem", title="Fehling's Test", title_bn="ফেলিং পরীক্ষা", summary="aldehyde detection", latex="\\ce{RCHO + 2Cu(OH)2 -> RCOOH + Cu2O + 2H2O}", order=190, trick="Aldehyde → red Cu₂O precipitate; ketone negative。", subject="chemistry", importance=2),
    make(id="tollens-test", chapter="organic-chem", title="Tollens' Test", title_bn="টollen's পরীক্ষা", summary="silver mirror", latex="\\ce{RCHO + 2Ag(NH3)2+ + 3OH- -> RCOO- + 2Ag + 4NH3 + 2H2O}", order=200, trick="Aldehyde → silver mirror; distinguishes from ketone。", subject="chemistry", importance=2),
]

CHAPTERS = [
    ("math", "conic-sections", CONIC_META, CONIC),
    ("math", "probability", PROB_META, PROB),
    ("math", "coordinate-geometry-3d", COORD3D_META, COORD3D),
    ("math", "sets-functions", SETS_META, SETS),
    ("math", "math-statics", STATICS_META, STATICS),
    ("math", "math-dynamics", DYNAMICS_META, DYNAMICS),
    ("math", "linear-programming", LP_META, LP),
    ("chemistry", "colligative-properties", COLLIG_META, COLLIG),
    ("chemistry", "solid-state-chemistry", SOLID_META, SOLID),
    ("chemistry", "coordination-chemistry", COORD_META, COORD),
    ("chemistry", "industrial-chemistry", IND_META, IND),
]

def main():
    count = 0
    for subject, chapter, meta, formulas in CHAPTERS:
        write_meta(subject, chapter, meta)
        for f in formulas:
            write_formula(subject, chapter, f)
            count += 1

    for f in EXPANSIONS:
        subject = f["subjects"][0]
        write_formula(subject, f["chapter"], f)
        count += 1

    print(f"Wrote {count} formula files")


if __name__ == "__main__":
    main()
