#!/usr/bin/env python3
"""Enrich thin HSC chapters + add high-yield missing topics in one pass."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "subjects"
EXISTING = {p.stem for p in ROOT.glob("*/chapters/*/formulas/*.json")}


def make(
    *,
    id: str,
    chapter: str,
    title: str,
    title_bn: str,
    summary: str,
    latex: str,
    subject: str,
    importance: int = 2,
    order: int = 10,
    trick: str = "",
) -> dict | None:
    if id in EXISTING:
        return None
    star = f"{importance}-star"
    if subject == "math":
        tags = ["hsc", "eng-admission", "varsity", star]
    elif subject == "chemistry":
        tags = ["hsc", "eng-admission", "medical", "varsity", star]
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
        "symbols": [
            {
                "symbol": "—",
                "meaning": "প্রধান চলকসমূহ সূত্রে দ্রষ্টব্য",
                "unit": "—",
            }
        ],
        "derivation": {
            "lead": trick or summary,
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
        "memorize": {"trick": trick or summary, "steps": []},
        "subjects": [subject],
        "related": [],
    }


def write_formula(subject: str, chapter: str, data: dict) -> None:
    out = ROOT / subject / "chapters" / chapter / "formulas"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{data['id']}.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    EXISTING.add(data["id"])


def write_meta(subject: str, chapter: str, meta: dict) -> None:
    out = ROOT / subject / "chapters" / chapter
    out.mkdir(parents=True, exist_ok=True)
    (out / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


# —— New chapters ——
SURFACE = [
    make(id="adsorption-physisorption-chemisorption", chapter="surface-chemistry", title="Physisorption vs Chemisorption", title_bn="ভৌত ও রাসায়নিক অধিশোষণ", summary="ΔH, layer, reversible", latex="\\text{physisorption: }|\\Delta H|\\sim 20\\!-\\!40\\,\\mathrm{kJ/mol};\\ \\text{chemisorption: }|\\Delta H|\\sim 80\\!-\\!240\\,\\mathrm{kJ/mol}", subject="chemistry", order=10, trick="ভৌত = বহুস্তর, উল্টানো যায়; রাসায়নিক = একস্তর, শক্তিশালী।", importance=3),
    make(id="freundlich-adsorption", chapter="surface-chemistry", title="Freundlich Isotherm", title_bn="ফ্রয়েন্ডলিচ সমতাপরেখা", summary="x/m = k P^(1/n)", latex="\\frac{x}{m}=k P^{1/n}\\quad(n>1)", subject="chemistry", order=20, trick="log(x/m)=log k+(1/n)log P — সরলরেখার ঢাল ১/n।", importance=3),
    make(id="langmuir-adsorption", chapter="surface-chemistry", title="Langmuir Isotherm", title_bn="ল্যাংমুইর সমতাপরেখা", summary="θ = KP/(1+KP)", latex="\\theta=\\frac{KP}{1+KP},\\quad \\frac{P}{x/m}=\\frac{1}{k_1k_2}+\\frac{P}{k_1}", subject="chemistry", order=30, trick="একস্তর অধিশোষণ; উচ্চ P-তে θ→1।", importance=2),
    make(id="catalyst-types", chapter="surface-chemistry", title="Homogeneous & Heterogeneous Catalysis", title_bn="সম ও অসম সংঘটক", summary="same/different phase", latex="\\text{homogeneous: same phase};\\quad \\text{heterogeneous: different phase}", subject="chemistry", order=40, trick="Fe Haber প্রক্রিয়ায় অসম; ইনভার্টেজ সম সংঘটক।", importance=2),
    make(id="colloid-tyndall", chapter="surface-chemistry", title="Tyndall Effect", title_bn="টিনডাল প্রভাব", summary="light scattering", latex="\\text{colloidal particles scatter light}\\Rightarrow\\text{Tyndall cone}", subject="chemistry", order=50, trick="সমাধান করে না; কলয়েড করে — পথ দেখা যায়।", importance=2),
    make(id="brownian-motion-colloid", chapter="surface-chemistry", title="Brownian Motion", title_bn="ব্রাউনীয় গতি", summary="zigzag particle motion", latex="\\text{continuous random motion of colloidal particles}", subject="chemistry", order=60, trick="কলয়েড স্থিতিশীলতার প্রমাণ — কণা থেমে যায় না।", importance=2),
    make(id="emulsion-types", chapter="surface-chemistry", title="Emulsion Types", title_bn="ইমালশনের প্রকার", summary="O/W and W/O", latex="\\text{O/W (oil in water)},\\quad \\text{W/O (water in oil)}", subject="chemistry", order=70, trick="দুধ = O/W; মাখন = W/O।", importance=2),
    make(id="cmc-micelle", chapter="surface-chemistry", title="CMC & Micelle", title_bn="CMC ও মাইকেল", summary="critical micelle concentration", latex="\\text{CMC = concentration where micelles form}", subject="chemistry", order=80, trick="সাবানের পরিষ্কার ক্ষমতা CMC-এর উপরে কার্যকর।", importance=2),
]

LOG_EXP = [
    make(id="log-product-quotient", chapter="logarithms-exponents", title="Log Product & Quotient", title_bn="লগ গুণ ও ভাগ", summary="log(ab), log(a/b)", latex="\\log_c(ab)=\\log_c a+\\log_c b,\\quad \\log_c\\frac{a}{b}=\\log_c a-\\log_c b", subject="math", order=10, trick="গুণ → যোগ; ভাগ → বিয়োগ।", importance=3),
    make(id="log-power-rule", chapter="logarithms-exponents", title="Log Power Rule", title_bn="লগ ঘাত সূত্র", summary="log(a^n)=n log a", latex="\\log_c(a^n)=n\\log_c a", subject="math", order=20, trick="ঘাত সামনে এসে গুণক হয়।", importance=3),
    make(id="change-of-base", chapter="logarithms-exponents", title="Change of Base", title_bn="ভিত্তি পরিবর্তন", summary="log_b a = log_k a / log_k b", latex="\\log_b a=\\frac{\\log_k a}{\\log_k b}=\\frac{1}{\\log_a b}", subject="math", order=30, trick="ক্যালকুলেটরে ln বা log₁₀ দিয়ে যেকোনো ভিত্তি।", importance=3),
    make(id="log-identity-ab", chapter="logarithms-exponents", title="log_b a · log_a b = 1", title_bn="বিপরীত লগ গুণফল", summary="reciprocal logs", latex="\\log_b a\\cdot\\log_a b=1", subject="math", order=40, trick="একটি জানলে অন্যটি উল্টো।", importance=2),
    make(id="exponential-laws", chapter="logarithms-exponents", title="Laws of Exponents", title_bn="ঘাতের সূত্রাবলি", summary="a^m a^n, (a^m)^n", latex="a^m a^n=a^{m+n},\\quad (a^m)^n=a^{mn},\\quad \\frac{a^m}{a^n}=a^{m-n}", subject="math", order=50, trick="গুণে ঘাত যোগ; ঘাতের ঘাত গুণ।", importance=3),
    make(id="exp-log-inverse", chapter="logarithms-exponents", title="Exp–Log Inverse", title_bn="ঘাত–লগ বিপরীত", summary="a^{log_a x}=x", latex="a^{\\log_a x}=x\\ (x>0),\\quad \\log_a(a^x)=x", subject="math", order=60, trick="একই ভিত্তিতে একে অন্যের উল্টো।", importance=3),
    make(id="natural-common-log", chapter="logarithms-exponents", title="ln and log₁₀", title_bn="ln ও সাধারণ লগ", summary="ln = log_e", latex="\\ln x=\\log_e x,\\quad \\log_{10}x=\\frac{\\ln x}{\\ln 10}", subject="math", order=70, trick="প্রাকৃতিক লগ ভিত্তি e≈2.718।", importance=2),
    make(id="log-equation-basic", chapter="logarithms-exponents", title="Basic Log Equation", title_bn="মৌলিক লগ সমীকরণ", summary="log_b a = c ⇒ a=b^c", latex="\\log_b a=c\\iff a=b^c\\quad(a>0,b>0,b\\ne1)", subject="math", order=80, trick="লগ সমীকরণ → ঘাত আকারে লেখো।", importance=3),
]

VECTOR_ALG = [
    make(id="vector-magnitude-unit", chapter="vector-algebra", title="Magnitude & Unit Vector", title_bn="মান ও একক ভেক্টর", summary="|a|, â", latex="|\\vec a|=\\sqrt{a_x^2+a_y^2+a_z^2},\\quad \\hat a=\\frac{\\vec a}{|\\vec a|}", subject="math", order=10, trick="একক ভেক্টর = ভেক্টর ÷ মান।", importance=3),
    make(id="vector-dot-product-math", chapter="vector-algebra", title="Dot Product", title_bn="অন্তঃগুণফল", summary="a·b = |a||b|cosθ", latex="\\vec a\\cdot\\vec b=|\\vec a||\\vec b|\\cos\\theta=a_xb_x+a_yb_y+a_zb_z", subject="math", order=20, trick="লম্ব হলে ডট = ০; সমান্তরালে ±|a||b|।", importance=3),
    make(id="vector-cross-product-math", chapter="vector-algebra", title="Cross Product", title_bn="বহির্গুণফল", summary="a×b", latex="\\vec a\\times\\vec b=|\\vec a||\\vec b|\\sin\\theta\\,\\hat n=\\begin{vmatrix}\\hat i&\\hat j&\\hat k\\\\a_x&a_y&a_z\\\\b_x&b_y&b_z\\end{vmatrix}", subject="math", order=30, trick="ডানহস্ত নিয়ম; সমান্তরালে ক্রস = ০।", importance=3),
    make(id="vector-scalar-triple-math", chapter="vector-algebra", title="Scalar Triple Product", title_bn="স্কালার ত্রিগুণফল", summary="[a b c]", latex="[\\vec a\\,\\vec b\\,\\vec c]=\\vec a\\cdot(\\vec b\\times\\vec c)=\\begin{vmatrix}a_x&a_y&a_z\\\\b_x&b_y&b_z\\\\c_x&c_y&c_z\\end{vmatrix}", subject="math", order=40, trick="আয়তন = |[a b c]|; সমতলীয় হলে ০।", importance=2),
    make(id="vector-projection-formula", chapter="vector-algebra", title="Projection of a on b", title_bn="a-এর b-এর উপর অভিক্ষেপ", summary="proj_b a", latex="\\mathrm{proj}_{\\vec b}\\vec a=\\frac{\\vec a\\cdot\\vec b}{|\\vec b|^2}\\vec b,\\quad \\mathrm{comp}_{\\vec b}\\vec a=\\frac{\\vec a\\cdot\\vec b}{|\\vec b|}", subject="math", order=50, trick="অভিক্ষেপ ভেক্টর; কম্পোনেন্ট স্কেলার।", importance=2),
    make(id="vector-section-formula", chapter="vector-algebra", title="Section Formula", title_bn="অনুপাত বিভাজন", summary="internal division", latex="\\vec r=\\frac{m\\vec b+n\\vec a}{m+n}\\quad(\\text{internal }m:n)", subject="math", order=60, trick="m:n অভ্যন্তরে — ওজনিত গড়।", importance=2),
    make(id="vector-angle-between", chapter="vector-algebra", title="Angle Between Vectors", title_bn="দুই ভেক্টরের কোণ", summary="cosθ = (a·b)/(|a||b|)", latex="\\cos\\theta=\\frac{\\vec a\\cdot\\vec b}{|\\vec a||\\vec b|}", subject="math", order=70, trick="কোণ বের করতে ডট ব্যবহার করো।", importance=3),
    make(id="vector-area-parallelogram", chapter="vector-algebra", title="Area of Parallelogram", title_bn="সামান্তরিকের ক্ষেত্রফল", summary="|a×b|", latex="A=|\\vec a\\times\\vec b|", subject="math", order=80, trick="ক্রসের মান = সামান্তরিক ক্ষেত্রফল।", importance=2),
]

# —— Enrich thin / high-yield existing chapters ——
INDUSTRIAL = [
    make(id="haber-ammonia-conditions", chapter="industrial-chemistry", title="Haber Optimum Conditions", title_bn="হেবার অনুকূল শর্ত", summary="pressure temperature catalyst", latex="P\\sim 200\\!-\\!300\\,\\mathrm{atm},\\ T\\sim 400\\!-\\!450^\\circ\\mathrm{C},\\ \\mathrm{Fe\\ catalyst}", subject="chemistry", order=50, trick="উচ্চ চাপ + মধ্যম তাপ + Fe সংঘটক।", importance=3),
    make(id="contact-process-v2o5", chapter="industrial-chemistry", title="Contact Process Key Step", title_bn="কন্টাক্ট মূল ধাপ", summary="SO₂→SO₃ with V₂O₅", latex="2\\mathrm{SO_2}+\\mathrm{O_2}\\rightleftharpoons 2\\mathrm{SO_3}\\ (\\mathrm{V_2O_5})", subject="chemistry", order=60, trick="V₂O₅ সংঘটক; ওলিয়াম হয়ে H₂SO₄।", importance=3),
    make(id="solvay-nahco3-step", chapter="industrial-chemistry", title="Solvay Bicarbonate Step", title_bn="সলভে বাইকার্বোনেট ধাপ", summary="NaHCO₃ precipitation", latex="\\mathrm{NaCl}+\\mathrm{NH_3}+\\mathrm{CO_2}+\\mathrm{H_2O}\\to\\mathrm{NaHCO_3}\\downarrow+\\mathrm{NH_4Cl}", subject="chemistry", order=70, trick="NaHCO₃ তাপে Na₂CO₃ দেয়।", importance=2),
    make(id="ostwald-nh3-oxidation", chapter="industrial-chemistry", title="Ostwald NH₃ Oxidation", title_bn="অস্টওয়াল্ড NH₃ জারণ", summary="NH₃→NO", latex="4\\mathrm{NH_3}+5\\mathrm{O_2}\\xrightarrow{\\mathrm{Pt}}4\\mathrm{NO}+6\\mathrm{H_2O}", subject="chemistry", order=80, trick="অ্যামোনিয়া জারণ → নাইট্রিক অ্যাসিড।", importance=2),
    make(id="glass-composition", chapter="industrial-chemistry", title="Soda-Lime Glass", title_bn="সোডা-লাইম কাচ", summary="Na₂O·CaO·6SiO₂", latex="\\mathrm{Na_2O\\cdot CaO\\cdot 6SiO_2}", subject="chemistry", order=90, trick="সাধারণ কাচ = সোডা + চুন + বালি।", importance=1),
    make(id="cement-composition", chapter="industrial-chemistry", title="Portland Cement", title_bn="পোর্টল্যান্ড সিমেন্ট", summary="CaO, SiO₂, Al₂O₃", latex="\\text{main: }\\mathrm{CaO},\\mathrm{SiO_2},\\mathrm{Al_2O_3},\\mathrm{Fe_2O_3}", subject="chemistry", order=100, trick="জলযোগে সেটিং — হাইড্রেশন।", importance=1),
]

SOLID = [
    make(id="packing-efficiency-fcc", chapter="solid-state-chemistry", title="FCC Packing Efficiency", title_bn="FCC প্যাকিং দক্ষতা", summary="74%", latex="\\text{PE}=\\frac{4\\times\\tfrac43\\pi r^3}{a^3}\\times100\\%=74\\%\\quad(a=2\\sqrt2\\,r)", subject="chemistry", order=60, trick="FCC/HCP সর্বোচ্চ ৭৪%।", importance=3),
    make(id="packing-efficiency-bcc", chapter="solid-state-chemistry", title="BCC Packing Efficiency", title_bn="BCC প্যাকিং দক্ষতা", summary="68%", latex="\\text{PE}=68\\%\\quad(a\\sqrt3=4r)", subject="chemistry", order=70, trick="BCC-তে body diagonal = 4r।", importance=2),
    make(id="density-crystal", chapter="solid-state-chemistry", title="Crystal Density", title_bn="স্ফটিক ঘনত্ব", summary="ρ = ZM/(N_A a³)", latex="\\rho=\\frac{ZM}{N_A a^3}", subject="chemistry", order=80, trick="Z = একক কোষে কণা সংখ্যা।", importance=3),
    make(id="bragg-law-chem", chapter="solid-state-chemistry", title="Bragg's Law", title_bn="ব্র্যাগের সূত্র", summary="nλ=2d sinθ", latex="n\\lambda=2d\\sin\\theta", subject="chemistry", order=90, trick="X-ray দিয়ে d নির্ণয়।", importance=2),
    make(id="schottky-frenkel", chapter="solid-state-chemistry", title="Schottky & Frenkel Defects", title_bn="শটকি ও ফ্রেনকেল ত্রুটি", summary="vacancy / interstitial", latex="\\text{Schottky: cation+anion vacancy};\\ \\text{Frenkel: ion displaced to interstitial}", subject="chemistry", order=100, trick="শটকি ঘনত্ব কমায়; ফ্রেনকেল ঘনত্ব একই রাখে।", importance=2),
]

COORD = [
    make(id="werner-valency-types", chapter="coordination-chemistry", title="Werner Primary & Secondary Valency", title_bn="ওয়ার্নার প্রাথমিক ও মাধ্যমিক যোজনী", summary="oxidation vs coordination", latex="\\text{primary = oxidation number};\\quad \\text{secondary = coordination number}", subject="chemistry", order=60, trick="প্রাথমিক আয়নীয়; মাধ্যমিক দিকনির্দেশক।", importance=2),
    make(id="coordination-number-geometry", chapter="coordination-chemistry", title="CN and Geometry", title_bn="সমন্বয় সংখ্যা ও জ্যামিতি", summary="CN 2,4,6", latex="\\mathrm{CN}=2\\to\\text{linear};\\ 4\\to\\text{tetrahedral/square planar};\\ 6\\to\\text{octahedral}", subject="chemistry", order=70, trick="CN=৬ সাধারণত অষ্টতলক।", importance=3),
    make(id="efs-crystal-field-split", chapter="coordination-chemistry", title="Crystal Field Splitting", title_bn="স্ফটিক ক্ষেত্র বিভাজন", summary="Δ_o / Δ_t", latex="\\Delta_o\\ (\\text{octahedral}),\\quad \\Delta_t=\\tfrac45\\Delta_o\\ (\\text{approx. for tetrahedral})", subject="chemistry", order=80, trick="বড় Δ → নিম্ন স্পিন; ছোট Δ → উচ্চ স্পিন।", importance=2),
    make(id="spectrochemical-series", chapter="coordination-chemistry", title="Spectrochemical Series", title_bn="বর্ণালি রাসায়নিক শ্রেণি", summary="ligand field strength", latex="\\mathrm{I^-}<\\mathrm{Br^-}<\\mathrm{Cl^-}<\\mathrm{F^-}<\\mathrm{OH^-}<\\mathrm{H_2O}<\\mathrm{NH_3}<\\mathrm{en}<\\mathrm{CN^-}", subject="chemistry", order=90, trick="CN⁻ শক্তিশালী ক্ষেত্র লিগ্যান্ড।", importance=2),
    make(id="chelate-effect", chapter="coordination-chemistry", title="Chelate Effect", title_bn="কিলেট প্রভাব", summary="polydentate stability", latex="\\text{chelate complexes more stable than similar non-chelates}", subject="chemistry", order=100, trick="এন্ট্রপি বাড়ে বলে কিলেট স্থিতিশীল।", importance=2),
]

ASTRONOMY = [
    make(id="stellar-parallax-pc", chapter="astronomy", title="Stellar Parallax Distance", title_bn="প্যারালাক্স দূরত্ব", summary="d=1/p", latex="d(\\mathrm{pc})=\\frac{1}{p('')} ", subject="physics", order=70, trick="প্যারালাক্স সেকেন্ডে → পারসেক দূরত্ব।", importance=3),
    make(id="absolute-apparent-magnitude", chapter="astronomy", title="Distance Modulus", title_bn="দূরত্ব মডুলাস", summary="m−M=5log(d/10)", latex="m-M=5\\log_{10}\\frac{d}{10}\\quad(d\\text{ in pc})", subject="physics", order=80, trick="m=আপাত, M=পরম মান।", importance=2),
    make(id="hubble-recession-law", chapter="astronomy", title="Hubble's Law", title_bn="হাবলের সূত্র", summary="v=H₀d", latex="v=H_0 d", subject="physics", order=90, trick="মহাবিশ্ব সম্প্রসারণের প্রমাণ।", importance=3),
    make(id="planetary-escape-speed", chapter="astronomy", title="Escape Velocity", title_bn="পলায়ন বেগ", summary="√(2GM/R)", latex="v_e=\\sqrt{\\frac{2GM}{R}}", subject="physics", order=100, trick="পৃথিবীতে ≈১১.২ km/s।", importance=2),
]

NUCLEAR_EXTRA = [
    make(id="mean-life-chem", chapter="nuclear-chemistry", title="Mean Life", title_bn="গড় আয়ু", summary="τ=1/λ", latex="\\tau=\\frac{1}{\\lambda}=\\frac{t_{1/2}}{0.693}", subject="chemistry", order=70, trick="গড় আয়ু > অর্ধায়ু।", importance=2),
    make(id="activity-becquerel", chapter="nuclear-chemistry", title="Activity Units", title_bn="সক্রিয়তার একক", summary="Bq and Ci", latex="1\\,\\mathrm{Bq}=1\\,\\mathrm{s^{-1}},\\quad 1\\,\\mathrm{Ci}=3.7\\times10^{10}\\,\\mathrm{Bq}", subject="chemistry", order=80, trick="SI একক বেকেরেল।", importance=2),
    make(id="mass-energy-chem", chapter="nuclear-chemistry", title="Mass–Energy Equivalence", title_bn="ভর–শক্তি সমতুল্যতা", summary="E=mc²", latex="E=(\\Delta m)c^2", subject="chemistry", order=90, trick="ভর ক্ষতি → শক্তি নির্গত।", importance=3),
    make(id="neutron-proton-ratio", chapter="nuclear-chemistry", title="n/p Stability", title_bn="n/p স্থিতিশীলতা", summary="band of stability", latex="\\text{stable }n/p\\approx1\\ (\\text{light})\\to\\approx1.5\\ (\\text{heavy})", subject="chemistry", order=100, trick="ভারী নিউক্লিয়াসে নিউট্রন বেশি লাগে।", importance=2),
]

ENV = [
    make(id="bod-cod-definitions", chapter="environmental-chemistry", title="BOD & COD", title_bn="BOD ও COD", summary="oxygen demand", latex="\\mathrm{BOD}=\\text{O}_2\\text{ used by microbes};\\quad \\mathrm{COD}=\\text{chemical O}_2\\text{ demand}", subject="chemistry", order=70, trick="BOD বেশি = পানি দূষিত।", importance=3),
    make(id="major-greenhouse-gases", chapter="environmental-chemistry", title="Greenhouse Gases", title_bn="গ্রিনহাউস গ্যাস", summary="CO₂, CH₄, N₂O, O₃", latex="\\mathrm{CO_2},\\mathrm{CH_4},\\mathrm{N_2O},\\mathrm{O_3},\\mathrm{CFCs}", subject="chemistry", order=80, trick="CH₄ CO₂-এর চেয়ে শক্তিশালী গ্রিনহাউস গ্যাস।", importance=2),
    make(id="ozone-depletion-cfcs", chapter="environmental-chemistry", title="Ozone Depletion by CFC", title_bn="CFC দ্বারা ওজোন ক্ষয়", summary="Cl radical chain", latex="\\mathrm{CF_2Cl_2}\\xrightarrow{uv}\\mathrm{Cl^\\bullet},\\quad \\mathrm{Cl^\\bullet}+\\mathrm{O_3}\\to\\mathrm{ClO^\\bullet}+\\mathrm{O_2}", subject="chemistry", order=90, trick="এক Cl পরমাণু হাজার ওজোন ভাঙতে পারে।", importance=3),
    make(id="acid-rain-formation", chapter="environmental-chemistry", title="Acid Rain", title_bn="অ্যাসিড বৃষ্টি", summary="SO₂, NOₓ → acids", latex="\\mathrm{SO_2}+\\mathrm{H_2O}\\to\\mathrm{H_2SO_3};\\quad \\mathrm{NO_2}+\\mathrm{H_2O}\\to\\mathrm{HNO_3}", subject="chemistry", order=100, trick="pH < ৫.৬ হলে অ্যাসিড বৃষ্টি।", importance=2),
]

LP = [
    make(id="lp-objective-z", chapter="linear-programming", title="Objective Function", title_bn="উদ্দেশ্য ফাংশন", summary="Z = ax+by", latex="Z=ax+by\\ (\\text{maximize/minimize})", subject="math", order=50, trick="কোণবিন্দুতে চরম মান পাওয়া যায়।", importance=3),
    make(id="lp-feasible-set", chapter="linear-programming", title="Feasible Region", title_bn="সম্ভাব্য অঞ্চল", summary="intersection of half-planes", latex="\\text{feasible region = intersection of all constraints}", subject="math", order=60, trick="বন্ধ ও সীমাবদ্ধ হলে সমাধান নিশ্চিত।", importance=2),
    make(id="lp-corner-optimum", chapter="linear-programming", title="Corner Point Theorem", title_bn="কোণবিন্দু উপপাদ্য", summary="optimum at vertex", latex="\\text{optimal }Z\\text{ occurs at a corner of the feasible region}", subject="math", order=70, trick="সব কোণে Z হিসাব করে বড়/ছোট নাও।", importance=3),
    make(id="lp-graphical-steps", chapter="linear-programming", title="Graphical Method Steps", title_bn="লেখচিত্র পদ্ধতির ধাপ", summary="draw → shade → evaluate", latex="\\text{1) lines 2) shade 3) corners 4) evaluate }Z", subject="math", order=80, trick="দুই চলকের LP গ্রাফে সহজ।", importance=2),
]

PERM = [
    make(id="permutation-npr", chapter="permutation-combination", title="ⁿPᵣ", title_bn="ক্রমবিন্যাস ⁿPᵣ", summary="n!/(n−r)!", latex="{}^{n}P_{r}=\\frac{n!}{(n-r)!}", subject="math", order=80, trick="ক্রম গুরুত্বপূর্ণ।", importance=3),
    make(id="combination-ncr", chapter="permutation-combination", title="ⁿCᵣ", title_bn="সমাবেশ ⁿCᵣ", summary="n!/(r!(n−r)!)", latex="{}^{n}C_{r}=\\frac{n!}{r!(n-r)!}={}^{n}P_{r}/r!", subject="math", order=90, trick="ক্রম গুরুত্বহীন; ⁿCᵣ=ⁿCₙ₋ᵣ।", importance=3),
    make(id="circular-arrangement", chapter="permutation-combination", title="Circular Permutation", title_bn="বৃত্তাকার ক্রমবিন্যাস", summary="(n−1)!", latex="P_{\\circ}=(n-1)!", subject="math", order=100, trick="ঘূর্ণন একই ধরলে (n−1)!।", importance=2),
    make(id="permutation-with-repetition", chapter="permutation-combination", title="Permutations with Repetition", title_bn="পুনরাবৃত্তিসহ ক্রমবিন্যাস", summary="n!/(n₁!n₂!…)", latex="\\frac{n!}{n_1!n_2!\\cdots n_k!}", subject="math", order=110, trick="একই অক্ষরের পুনরাবৃত্তি ভাজকে যায়।", importance=2),
    make(id="combination-sum-identity", chapter="permutation-combination", title="Pascal Identity", title_bn="প্যাসকেল সমতা", summary="ⁿCᵣ + ⁿCᵣ₋₁ = ⁿ⁺¹Cᵣ", latex="{}^{n}C_{r}+{}^{n}C_{r-1}={}^{n+1}C_{r}", subject="math", order=120, trick="দ্বিপদী সহগের ত্রিভুজ নিয়ম।", importance=2),
]

MATRIX = [
    make(id="matrix-multiplication-cond", chapter="matrix-determinant", title="Matrix Multiplication Condition", title_bn="ম্যাট্রিক্স গুণের শর্ত", summary="(m×n)(n×p)", latex="A_{m\\times n}B_{n\\times p}=C_{m\\times p}", subject="math", order=90, trick="মধ্যের দুই মাত্রা সমান হতে হবে।", importance=3),
    make(id="det-2x2-formula", chapter="matrix-determinant", title="2×2 Determinant", title_bn="২×২ নির্ণায়ক", summary="ad−bc", latex="\\begin{vmatrix}a&b\\\\c&d\\end{vmatrix}=ad-bc", subject="math", order=100, trick="২×২: প্রধান−অপ্রধান কর্ণ।", importance=3),
    make(id="inverse-matrix-adj", chapter="matrix-determinant", title="Inverse via Adjoint", title_bn="সহযোগী দিয়ে বিপরীত", summary="A⁻¹ = (1/|A|) adj A", latex="A^{-1}=\\frac{1}{|A|}\\mathrm{adj}\\,A\\quad(|A|\\ne0)", subject="math", order=110, trick="|A|=০ হলে বিপরীত নেই।", importance=3),
    make(id="cramer-rule-system", chapter="matrix-determinant", title="Cramer's Rule", title_bn="ক্রেমারের সূত্র", summary="x=Δx/Δ", latex="x_i=\\frac{\\Delta_i}{\\Delta}\\quad(\\Delta\\ne0)", subject="math", order=120, trick="প্রতি চলকের জন্য স্তম্ভ বদলাও।", importance=2),
]

CIRCULAR = [
    make(id="v-omega-r", chapter="circular-motion", title="v = ωr", title_bn="রৈখিক ও কৌণিক বেগ", summary="v=ωr", latex="v=\\omega r,\\quad a_t=\\alpha r", subject="physics", order=90, trick="একই r-এ ω বাড়লে v বাড়ে।", importance=3),
    make(id="centripetal-force-mv2r", chapter="circular-motion", title="Centripetal Force", title_bn="কেন্দ্রমুখী বল", summary="mv²/r", latex="F_c=\\frac{mv^2}{r}=m\\omega^2 r", subject="physics", order=100, trick="দিক কেন্দ্রের দিকে; কাজ করে না।", importance=3),
    make(id="banking-of-road", chapter="circular-motion", title="Banking of Road", title_bn="রাস্তার ঢালকরণ", summary="tanθ=v²/(rg)", latex="\\tan\\theta=\\frac{v^2}{rg}\\quad(\\text{no friction})", subject="physics", order=110, trick="বেশি গতি = বেশি ঢাল।", importance=3),
    make(id="vertical-circle-limits", chapter="circular-motion", title="Vertical Circle Extremes", title_bn="উল্লম্ব বৃত্তের চরম", summary="top/bottom", latex="v_{\\top}\\ge\\sqrt{gr},\\quad v_{\\bot}=\\sqrt{u^2-4gr}\\ (\\text{string})", subject="physics", order=120, trick="শীর্ষে ন্যূনতম √(gr)।", importance=2),
]

AC_EXTRA = [
    make(id="ac-impedance", chapter="induction-ac", title="AC Impedance", title_bn="প্রতিবন্ধকতা", summary="Z=√(R²+(X_L−X_C)²)", latex="Z=\\sqrt{R^2+(X_L-X_C)^2},\\quad X_L=\\omega L,\\ X_C=1/(\\omega C)", subject="physics", order=140, trick="অনুরণনে X_L=X_C → Z=R।", importance=3),
    make(id="ac-power-factor", chapter="induction-ac", title="Power Factor", title_bn="ক্ষমতা গুণাঙ্ক", summary="cosφ = R/Z", latex="\\cos\\phi=\\frac{R}{Z},\\quad P_{\\mathrm{avg}}=V_{\\mathrm{rms}}I_{\\mathrm{rms}}\\cos\\phi", subject="physics", order=150, trick="খাঁটি রোধে cosφ=১।", importance=3),
    make(id="lc-resonance-freq", chapter="induction-ac", title="LC Resonance Frequency", title_bn="LC অনুরণন কম্পাঙ্ক", summary="f₀=1/(2π√LC)", latex="f_0=\\frac{1}{2\\pi\\sqrt{LC}}", subject="physics", order=160, trick="রেডিও টিউনিং-এর সূত্র।", importance=3),
    make(id="ideal-transformer-ratio", chapter="induction-ac", title="Transformer Equation", title_bn="ট্রান্সফরমার সমীকরণ", summary="Vs/Vp = Ns/Np", latex="\\frac{V_s}{V_p}=\\frac{N_s}{N_p}=\\frac{I_p}{I_s}", subject="physics", order=170, trick="স্টেপ-আপ: Ns>Np।", importance=2),
]

MODERN_EXTRA = [
    make(id="einstein-photoelectric", chapter="modern-physics", title="Einstein Photoelectric Equation", title_bn="আইনস্টাইনের ফটোইলেকট্রিক সমীকরণ", summary="K_max=hf−φ", latex="K_{\\max}=hf-\\phi=h(f-f_0)", subject="physics", order=140, trick="কাট-অফ f₀=φ/h।", importance=3),
    make(id="stopping-potential", chapter="modern-physics", title="Stopping Potential", title_bn="রোধ বিভব", summary="eV₀=K_max", latex="eV_0=K_{\\max}=hf-\\phi", subject="physics", order=150, trick="V₀ দিয়ে K_max মাপা যায়।", importance=2),
    make(id="bohr-frequency-condition", chapter="modern-physics", title="Bohr Frequency Condition", title_bn="বোরের কম্পাঙ্ক শর্ত", summary="hf=E₂−E₁", latex="hf=E_2-E_1", subject="physics", order=160, trick="শক্তি পার্থক্য = ফোটন শক্তি।", importance=3),
]

FLUID_HEAT = [
    make(id="continuity-fluid", chapter="properties-of-matter", title="Equation of Continuity", title_bn="ধারাবাহিকতার সমীকরণ", summary="A₁v₁=A₂v₂", latex="A_1v_1=A_2v_2", subject="physics", order=130, trick="সরু স্থানে বেগ বেশি।", importance=3),
    make(id="torricelli-theorem", chapter="properties-of-matter", title="Torricelli's Theorem", title_bn="টরিসেলির উপপাদ্য", summary="v=√(2gh)", latex="v=\\sqrt{2gh}", subject="physics", order=140, trick="ট্যাঙ্কের ছিদ্রে বেগ = √(2gh)।", importance=2),
    make(id="newton-cooling", chapter="thermodynamics", title="Newton's Law of Cooling", title_bn="নিউটনের শীতলীকরণ সূত্র", summary="dT/dt ∝ (T−T₀)", latex="\\frac{dT}{dt}=-k(T-T_0)", subject="physics", order=160, trick="তাপমাত্রা পার্থক্যের সমানুপাতিক হারে ঠান্ডা।", importance=2),
    make(id="thermal-conduction-rate", chapter="thermodynamics", title="Heat Conduction Rate", title_bn="তাপ পরিবহন হার", summary="dQ/dt = κAΔT/L", latex="\\frac{dQ}{dt}=\\kappa A\\frac{\\Delta T}{L}", subject="physics", order=170, trick="κ বড় = ভালো পরিবাহী।", importance=2),
]

KINETICS_EXTRA = [
    make(id="first-order-half-life", chapter="chemical-equilibrium", title="First-Order Half-Life", title_bn="প্রথম ক্রমের অর্ধায়ু", summary="t½=0.693/k", latex="t_{1/2}=\\frac{0.693}{k}\\quad(\\text{1st order})", subject="chemistry", order=200, trick="ঘনত্ব-নির্ভর নয় — তেজস্ক্রিয় ক্ষয়ের মতো।", importance=3),
    make(id="integrated-first-order", chapter="chemical-equilibrium", title="Integrated First-Order Rate", title_bn="সমাকলিত প্রথম ক্রম", summary="ln([A]₀/[A])=kt", latex="\\ln\\frac{[A]_0}{[A]}=kt\\quad\\text{or}\\quad [A]=[A]_0 e^{-kt}", subject="chemistry", order=210, trick="ln[A] বনাম t সরলরেখা।", importance=3),
    make(id="activation-energy-arrhenius-plot", chapter="chemical-equilibrium", title="Arrhenius Plot", title_bn="আরেনিয়াস প্লট", summary="ln k vs 1/T", latex="\\ln k=\\ln A-\\frac{E_a}{RT}", subject="chemistry", order=220, trick="ঢাল = −E_a/R।", importance=2),
]

MATH_EXTRA = [
    make(id="limit-standard-sinx", chapter="differentiation", title="Standard Limit sin x / x", title_bn="প্রমিত সীমা sinx/x", summary="→1 as x→0", latex="\\lim_{x\\to0}\\frac{\\sin x}{x}=1", subject="math", order=110, trick="রেডিয়ানে সত্য; ডিগ্রিতে নয়।", importance=3),
    make(id="lhopital-rule", chapter="differentiation", title="L'Hôpital's Rule", title_bn="ল'হোপিটালের নিয়ম", summary="0/0 or ∞/∞", latex="\\lim\\frac{f}{g}=\\lim\\frac{f'}{g'}\\quad(\\tfrac00\\text{ or }\\tfrac{\\infty}{\\infty})", subject="math", order=120, trick="অনির্ণেয় আকারে অন্তরক নাও।", importance=2),
    make(id="mean-value-theorem", chapter="calculus", title="Mean Value Theorem", title_bn="মধ্যমান উপপাদ্য", summary="f'(c)=(f(b)−f(a))/(b−a)", latex="f'(c)=\\frac{f(b)-f(a)}{b-a}", subject="math", order=170, trick="কোনো c-তে স্পর্শক জ্যা-এর সমান্তরাল।", importance=2),
    make(id="fundamental-theorem-calculus", chapter="integration", title="Fundamental Theorem of Calculus", title_bn="ক্যালকুলাসের মৌলিক উপপাদ্য", summary="d/dx ∫_a^x f = f(x)", latex="\\frac{d}{dx}\\int_a^x f(t)\\,dt=f(x)", subject="math", order=110, trick="যোগজের অন্তরক = মূল ফাংশন।", importance=3),
]


def main() -> None:
    write_meta(
        "chemistry",
        "surface-chemistry",
        {
            "id": "surface-chemistry",
            "slug": "surface-chemistry",
            "name": "Surface Chemistry",
            "nameBn": "পৃষ্ঠ রসায়ন",
            "order": 9,
        },
    )
    write_meta(
        "math",
        "logarithms-exponents",
        {
            "id": "logarithms-exponents",
            "slug": "logarithms-exponents",
            "name": "Logarithms & Exponents",
            "nameBn": "লগারিদম ও ঘাত",
            "order": 6,
        },
    )
    write_meta(
        "math",
        "vector-algebra",
        {
            "id": "vector-algebra",
            "slug": "vector-algebra",
            "name": "Vector Algebra",
            "nameBn": "ভেক্টর বীজগণিত",
            "order": 2,
        },
    )

    groups = [
        ("chemistry", "surface-chemistry", SURFACE),
        ("math", "logarithms-exponents", LOG_EXP),
        ("math", "vector-algebra", VECTOR_ALG),
        ("chemistry", "industrial-chemistry", INDUSTRIAL),
        ("chemistry", "solid-state-chemistry", SOLID),
        ("chemistry", "coordination-chemistry", COORD),
        ("physics", "astronomy", ASTRONOMY),
        ("chemistry", "nuclear-chemistry", NUCLEAR_EXTRA),
        ("chemistry", "environmental-chemistry", ENV),
        ("math", "linear-programming", LP),
        ("math", "permutation-combination", PERM),
        ("math", "matrix-determinant", MATRIX),
        ("physics", "circular-motion", CIRCULAR),
        ("physics", "induction-ac", AC_EXTRA),
        ("physics", "modern-physics", MODERN_EXTRA),
        ("physics", "properties-of-matter", FLUID_HEAT[:2]),
        ("physics", "thermodynamics", FLUID_HEAT[2:]),
        ("chemistry", "chemical-equilibrium", KINETICS_EXTRA),
        ("math", "differentiation", MATH_EXTRA[:2]),
        ("math", "calculus", MATH_EXTRA[2:3]),
        ("math", "integration", MATH_EXTRA[3:]),
    ]

    n = 0
    for subject, chapter, items in groups:
        for f in items:
            if f is None:
                continue
            write_formula(subject, chapter, f)
            n += 1
    print(f"Wrote {n} formulas across {len(groups)} groups")


if __name__ == "__main__":
    main()
