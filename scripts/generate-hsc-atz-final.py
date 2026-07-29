#!/usr/bin/env python3
"""A–Z HSC/admission gap fill: missing high-yield formulas + tag fixes."""

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
    tags = (
        ["hsc", "eng-admission", "varsity", star]
        if subject == "math"
        else ["hsc", "eng-admission", "medical", "varsity", star]
    )
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
            {"symbol": "—", "meaning": "প্রধান চলকসমূহ সূত্রে দ্রষ্টব্য", "unit": "—"}
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
                "question": f"{title_bn} এর মূল সূত্র/নীতিটি লেখো।",
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


def fix_missing_hsc_tags() -> int:
    n = 0
    for p in ROOT.glob("*/chapters/*/formulas/*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        tags = list(data.get("tags") or [])
        if "hsc" in tags:
            continue
        # keep exam tags first
        tags = ["hsc", *[t for t in tags if t != "hsc"]]
        data["tags"] = tags
        p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        n += 1
    return n


# —— Chemistry: atomic structure & periodic properties ——
ATOMIC = [
    make(id="aufbau-principle", chapter="qualitative-chem", title="Aufbau Principle", title_bn="আউফবাউ নীতি", summary="fill lowest energy first", latex="\\text{electrons fill orbitals in order of increasing energy (}n+\\ell\\text{ rule)}", subject="chemistry", order=210, trick="n+ℓ ছোট আগে; সমান হলে ছোট n আগে।", importance=3),
    make(id="hund-rule", chapter="qualitative-chem", title="Hund's Rule", title_bn="হান্ডের নিয়ম", summary="maximize unpaired spins", latex="\\text{degenerate orbitals: maximize unpaired electrons with parallel spin}", subject="chemistry", order=220, trick="একই শক্তির অরবিটালে আগে একক ইলেকট্রন।", importance=3),
    make(id="pauli-exclusion", chapter="qualitative-chem", title="Pauli Exclusion Principle", title_bn="পাউলির বর্জন নীতি", summary="unique quantum set", latex="\\text{no two electrons in an atom share all four quantum numbers}", subject="chemistry", order=230, trick="এক অরবিটালে সর্বোচ্চ ২ ইলেকট্রন, বিপরীত স্পিন।", importance=3),
    make(id="ionization-energy-trend", chapter="qualitative-chem", title="Ionization Energy Trend", title_bn="আয়নন শক্তির প্রবণতা", summary="IE across/down", latex="\\mathrm{IE}\\uparrow\\text{ across period};\\quad \\mathrm{IE}\\downarrow\\text{ down group}", subject="chemistry", order=240, trick="নিষ্ক্রিয় গ্যাসে IE সর্বোচ্চ; ক্ষার ধাতুতে কম।", importance=3),
    make(id="electron-affinity-trend", chapter="qualitative-chem", title="Electron Affinity Trend", title_bn="ইলেকট্রন আসক্তির প্রবণতা", summary="EA trends", latex="\\mathrm{EA}\\text{ generally increases across a period (more negative)}", subject="chemistry", order=250, trick="হ্যালোজেনে EA সবচেয়ে ঋণাত্মক।", importance=2),
    make(id="electronegativity-pauling", chapter="qualitative-chem", title="Pauling Electronegativity", title_bn="পলিং তড়িৎঋণাত্মকতা", summary="χ trends", latex="\\chi\\uparrow\\text{ across period};\\ \\chi\\downarrow\\text{ down group};\\ \\chi_{\\mathrm{F}}\\text{ highest}", subject="chemistry", order=260, trick="F > O > N/Cl — মুখস্থ ক্রম।", importance=3),
    make(id="atomic-radius-trend", chapter="qualitative-chem", title="Atomic Radius Trend", title_bn="পারমাণবিক ব্যাসার্ধের প্রবণতা", summary="radius across/down", latex="r\\downarrow\\text{ across period};\\quad r\\uparrow\\text{ down group}", subject="chemistry", order=270, trick="বামে→ডানে ছোট; উপরে→নিচে বড়।", importance=3),
]

ORGANIC_EXTRA = [
    make(id="anti-markovnikov-rule", chapter="organic-chem", title="Anti-Markovnikov Addition", title_bn="অ্যান্টি-মার্কোভনিকভ যোজন", summary="HBr + peroxide", latex="\\mathrm{RCH=CH_2}+\\mathrm{HBr}\\xrightarrow{\\mathrm{ROOR}}\\mathrm{RCH_2CH_2Br}", subject="chemistry", order=230, trick="পারক্সাইডে HBr অ্যান্টি-মার্কোভনিকভ।", importance=3),
    make(id="elimination-e1", chapter="organic-chem", title="E1 Elimination", title_bn="E1 বিলোপন", summary="unimolecular elimination", latex="\\text{E1: two-step, carbocation intermediate, rate}=k[\\mathrm{RX}]", subject="chemistry", order=240, trick="E1 ≈ SN1 পরিবেশ; দ্বিবন্ধন তৈরি।", importance=2),
    make(id="redox-half-reaction", chapter="organic-chem", title="Organic Redox Idea", title_bn="জৈব জারণ–বিজারণ ধারণা", summary="gain/loss of H/O", latex="\\text{oxidation: gain O / lose H};\\quad \\text{reduction: gain H / lose O}", subject="chemistry", order=250, trick="অ্যালকোহল→অ্যালডিহাইড→অ্যাসিড = জারণ।", importance=2),
    make(id="amino-acid-zwitterion", chapter="organic-chem", title="Amino Acid Zwitterion", title_bn="অ্যামিনো অ্যাসিড জুইটারআয়ন", summary="⁺H₃N–CHR–COO⁻", latex="\\mathrm{H_2N{-}CHR{-}COOH}\\rightleftharpoons \\mathrm{^{+}H_3N{-}CHR{-}COO^{-}}", subject="chemistry", order=260, trick="আইসোইলেকট্রিক বিন্দুতে জুইটারআয়ন।", importance=2),
    make(id="glucose-open-cyclic", chapter="organic-chem", title="Glucose Open ↔ Cyclic", title_bn="গ্লুকোজ মুক্ত ও চক্রাকার রূপ", summary="pyranose/furanose", latex="\\text{open-chain aldehyde}\\rightleftharpoons \\text{cyclic hemiacetal (pyranose)}", subject="chemistry", order=270, trick="D-গ্লুকোজ মূলত পাইরানোজ।", importance=2),
    make(id="peptide-bond", chapter="organic-chem", title="Peptide Bond", title_bn="পেপটাইড বন্ধন", summary="amide link", latex="\\mathrm{{-CO{-}NH{-}}}\\ \\text{(peptide/amide bond)}", subject="chemistry", order=280, trick="অ্যামিনো অ্যাসিড জোড়ায় –CONH–।", importance=2),
]

INDUSTRIAL_METAL = [
    make(id="froth-flotation", chapter="industrial-chemistry", title="Froth Flotation", title_bn="ফেন ভাসান পদ্ধতি", summary="sulphide ore concentration", latex="\\text{sulphide ore particles attach to froth; gangue sinks}", subject="chemistry", order=110, trick="সালফাইড আকরিক নির্বাচনী ভাসান।", importance=2),
    make(id="zone-refining", chapter="industrial-chemistry", title="Zone Refining", title_bn="জোন পরিশোধন", summary="ultrapure semiconductors", latex="\\text{impurities concentrate in molten zone and are swept away}", subject="chemistry", order=120, trick="Si/Ge অতি বিশুদ্ধ করতে ব্যবহৃত।", importance=2),
    make(id="electrolytic-refining", chapter="industrial-chemistry", title="Electrolytic Refining", title_bn="তড়িৎ পরিশোধন", summary="anode mud", latex="\\text{impure metal anode}\\\\rightarrow\\text{pure metal cathode}", subject="chemistry", order=130, trick="Cu পরিশোধনে অ্যানোড মাডে Au/Ag।", importance=2),
]

# —— Physics extras ——
PHYS = [
    make(id="ampere-force-parallel-wires", chapter="magnetic-current", title="Force Between Parallel Currents", title_bn="সমান্তরাল তারের বল", summary="F/L = μ₀ I₁I₂/(2πd)", latex="\\frac{F}{L}=\\frac{\\mu_0 I_1 I_2}{2\\pi d}", subject="physics", order=200, trick="সমদিক = আকর্ষণ; বিপরীত = বিকর্ষণ।", importance=3),
    make(id="moving-coil-galvanometer", chapter="magnetic-current", title="Moving Coil Galvanometer", title_bn="চল কুণ্ডলী গ্যালভানোমিটার", summary="NIAB = kθ", latex="NIAB=k\\theta\\quad\\Rightarrow\\quad I\\propto\\theta", subject="physics", order=210, trick="বিচ্যুতি প্রবাহের সমানুপাতিক।", importance=2),
    make(id="pair-production", chapter="modern-physics", title="Pair Production", title_bn="জোড় উৎপাদন", summary="γ → e⁻ + e⁺", latex="\\gamma\\to e^-+e^+\\quad(E_\\gamma\\ge 1.022\\,\\mathrm{MeV})", subject="physics", order=170, trick="ন্যূনতম ১.০২২ MeV ফোটন শক্তি।", importance=2),
    make(id="logic-nand-nor", chapter="semiconductor", title="NAND & NOR Gates", title_bn="NAND ও NOR গেট", summary="universal gates", latex="\\mathrm{NAND}=\\overline{A\\cdot B},\\quad \\mathrm{NOR}=\\overline{A+B}", subject="physics", order=120, trick="NAND/NOR দিয়ে সব গেট বানানো যায়।", importance=3),
    make(id="logic-xor-gate", chapter="semiconductor", title="XOR Gate", title_bn="XOR গেট", summary="A⊕B", latex="A\\oplus B=A\\overline{B}+\\overline{A}B", subject="physics", order=130, trick="একই হলে ০; ভিন্ন হলে ১।", importance=2),
]

# —— Math extras ——
MATH = [
    make(id="mathematical-induction", chapter="sequences-series", title="Mathematical Induction", title_bn="গাণিতিক আরোহ পদ্ধতি", summary="base + inductive step", latex="P(1)\\text{ true and }P(k)\\Rightarrow P(k+1)\\Rightarrow P(n)\\ \\forall n\\in\\mathbb{N}", subject="math", order=110, trick="ভিত্তি ধাপ + আরোহ ধাপ দুটোই লাগে।", importance=3),
    make(id="rolle-theorem", chapter="calculus", title="Rolle's Theorem", title_bn="রোলের উপপাদ্য", summary="f(a)=f(b) ⇒ f'(c)=0", latex="f(a)=f(b)\\Rightarrow \\exists c\\in(a,b):\\ f'(c)=0", subject="math", order=180, trick="মধ্যমান উপপাদ্যের বিশেষ রূপ।", importance=2),
    make(id="separable-differential-eq", chapter="calculus", title="Separable Differential Equation", title_bn="বিভাজ্য অন্তরক সমীকরণ", summary="dy/dx = g(x)h(y)", latex="\\frac{dy}{dx}=g(x)h(y)\\Rightarrow \\int\\frac{dy}{h(y)}=\\int g(x)\\,dx", subject="math", order=190, trick="x ও y আলাদা করে যোগজ নাও।", importance=3),
    make(id="cauchy-schwarz", chapter="sequences-series", title="Cauchy–Schwarz Inequality", title_bn="কোশি–শ্বারজ অসমতা", summary="(Σa²)(Σb²)≥(Σab)²", latex="\\Big(\\sum a_i^2\\Big)\\Big(\\sum b_i^2\\Big)\\ge\\Big(\\sum a_i b_i\\Big)^2", subject="math", order=120, trick="সমানতা যখন a ও b সমানুপাতিক।", importance=2),
    make(id="angle-bisector-theorem", chapter="straight-lines", title="Angle Bisector Theorem", title_bn="কোণ সমদ্বিখণ্ডক উপপাদ্য", summary="divides opposite side", latex="\\frac{BD}{DC}=\\frac{AB}{AC}", subject="math", order=170, trick="সমদ্বিখণ্ডক বিপরীত বাহুকে বাহুর অনুপাতে ভাগ করে।", importance=2),
    make(id="height-distance-trig", chapter="trigonometric-equations", title="Heights & Distances", title_bn="উচ্চতা ও দূরত্ব", summary="tanθ = h/d", latex="\\tan\\theta=\\frac{h}{d},\\quad \\sin\\theta=\\frac{h}{l}", subject="math", order=210, trick="উন্নয়ন/অবনমন কোণে tan ব্যবহার করো।", importance=3),
    make(id="sine-rule-explicit", chapter="trigonometric-equations", title="Law of Sines", title_bn="সাইন সূত্র", summary="a/sinA = 2R", latex="\\frac{a}{\\sin A}=\\frac{b}{\\sin B}=\\frac{c}{\\sin C}=2R", subject="math", order=220, trick="২R = পরিবৃত্ত ব্যাস।", importance=3),
    make(id="cosine-rule-explicit", chapter="trigonometric-equations", title="Law of Cosines", title_bn="কসাইন সূত্র", summary="c²=a²+b²−2ab cosC", latex="c^2=a^2+b^2-2ab\\cos C", subject="math", order=230, trick="কোণ জানা থাকলে তৃতীয় বাহু।", importance=3),
    make(id="inverse-trig-derivative", chapter="differentiation", title="Derivative of arcsin/arctan", title_bn="arcsin/arctan এর অন্তরক", summary="1/√(1−x²), 1/(1+x²)", latex="\\frac{d}{dx}\\arcsin x=\\frac{1}{\\sqrt{1-x^2}},\\quad \\frac{d}{dx}\\arctan x=\\frac{1}{1+x^2}", subject="math", order=130, trick="√(1−x²) ও (1+x²) মুখস্থ রাখো।", importance=3),
]


def main() -> None:
    fixed = fix_missing_hsc_tags()
    groups = [
        ("chemistry", "qualitative-chem", ATOMIC),
        ("chemistry", "organic-chem", ORGANIC_EXTRA),
        ("chemistry", "industrial-chemistry", INDUSTRIAL_METAL),
        ("physics", "magnetic-current", PHYS[:2]),
        ("physics", "modern-physics", PHYS[2:3]),
        ("physics", "semiconductor", PHYS[3:]),
        ("math", "sequences-series", [MATH[0], MATH[3]]),
        ("math", "calculus", [MATH[1], MATH[2]]),
        ("math", "straight-lines", [MATH[4]]),
        ("math", "trigonometric-equations", MATH[5:8]),
        ("math", "differentiation", MATH[8:]),
    ]
    n = 0
    for subject, chapter, items in groups:
        for f in items:
            if f is None:
                continue
            write_formula(subject, chapter, f)
            n += 1
    print(f"Fixed hsc tags on {fixed} files; wrote {n} new formulas")


if __name__ == "__main__":
    main()
