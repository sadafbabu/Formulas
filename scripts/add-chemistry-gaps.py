#!/usr/bin/env python3
"""Add high-yield missing HSC/admission Chemistry formulas."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "subjects" / "chemistry"
ALL_IDS = {
    p.stem
    for p in (Path(__file__).resolve().parent.parent / "content" / "subjects").glob(
        "*/chapters/*/formulas/*.json"
    )
}


def tags(importance: int = 2) -> list[str]:
    return ["hsc", "eng-admission", "medical", "varsity", f"{importance}-star"]


def formula(
    *,
    id: str,
    chapter: str,
    title: str,
    title_bn: str,
    summary: str,
    latex: str,
    symbols: list[dict],
    lead: str,
    steps: list[dict],
    assumptions: list[str],
    questions: list[dict],
    trick: str,
    memorize_steps: list[str] | None = None,
    related: list[str] | None = None,
    importance: int = 2,
    order: int = 200,
) -> dict:
    if id in ALL_IDS:
        raise SystemExit(f"duplicate id: {id}")
    return {
        "id": id,
        "chapter": chapter,
        "title": title,
        "titleBn": title_bn,
        "summary": summary,
        "latex": latex,
        "tags": tags(importance),
        "importance": importance,
        "order": order,
        "symbols": symbols,
        "derivation": {"lead": lead, "steps": steps, "assumptions": assumptions},
        "questions": questions,
        "memorize": {"trick": trick, "steps": memorize_steps or []},
        "subjects": ["chemistry"],
        "related": [r for r in (related or []) if r in ALL_IDS and r != id],
    }


def write(data: dict) -> None:
    out = ROOT / "chapters" / data["chapter"] / "formulas"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{data['id']}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    ALL_IDS.add(data["id"])
    print(f"+ {data['chapter']}/{data['id']}")


NEW = [
    formula(
        id="henrys-law",
        chapter="colligative-properties",
        title="Henry's Law",
        title_bn="হেনরির সূত্র",
        summary="গ্যাসের দ্রাব্যতা চাপের সমানুপাতিক: P = K_H · x",
        latex=r"P=K_H\,x\quad(\text{বা }C=K_H P)",
        symbols=[
            {"symbol": "P", "meaning": "গ্যাসের আংশিক চাপ", "unit": "atm / Pa"},
            {"symbol": "x", "meaning": "দ্রাবণে মোল ভগ্নাংশ", "unit": "—"},
            {"symbol": "K_H", "meaning": "হেনরি ধ্রুবক", "unit": "atm"},
            {"symbol": "C", "meaning": "ঘনমাত্রা রূপ", "unit": "mol/L"},
        ],
        lead="ধ্রুব তাপমাত্রায় দ্রবীভূত গ্যাসের মোল ভগ্নাংশ আংশিক চাপের সমানুপাতিক।",
        steps=[
            {"title": "সূত্র", "latex": r"P=K_H x", "note": "চাপ বাড়লে দ্রাব্যতা বাড়ে (সোডা)।"},
            {"title": "তাপমাত্রা", "latex": r"T\uparrow\Rightarrow K_H\uparrow\Rightarrow\text{দ্রাব্যতা}\downarrow", "note": "গরম পানিতে কম অক্সিজেন।"},
        ],
        assumptions=["আদর্শ তরল–গ্যাস দ্রবণ; নিম্ন চাপ"],
        questions=[
            {
                "examType": "HSC",
                "question": "হেনরির সূত্র অনুযায়ী চাপ দ্বিগুণ হলে দ্রাব্যতা কী হয়?",
                "answer": r"\text{দ্রাব্যতা দ্বিগুণ}",
            }
        ],
        trick="সোডা বোতল: চাপ↑ → CO₂ বেশি দ্রবীভূত; খুললে চাপ↓ → বুদবুদ।",
        memorize_steps=["P = K_H x", "গরমে গ্যাস কম দ্রবে"],
        related=["raoult-law", "osmotic-pressure"],
        importance=3,
        order=80,
    ),
    formula(
        id="ph-weak-acid",
        chapter="chemical-equilibrium",
        title="pH of Weak Acid",
        title_bn="দুর্বল অ্যাসিডের pH",
        summary="[H⁺]≈√(K_a c); pH = −½ log(K_a c)",
        latex=r"[\mathrm{H}^+]=\sqrt{K_a c},\quad\mathrm{pH}=-\tfrac12\log(K_a c)",
        symbols=[
            {"symbol": "K_a", "meaning": "অ্যাসিড বিয়োজন ধ্রুবক", "unit": "—"},
            {"symbol": "c", "meaning": "আদি ঘনমাত্রা", "unit": "mol/L"},
            {"symbol": r"[\mathrm{H}^+]", "meaning": "হাইড্রোজেন আয়ন ঘনমাত্রা", "unit": "mol/L"},
        ],
        lead="HA ⇌ H⁺ + A⁻; α≪1 হলে K_a ≈ cα² → [H⁺]=√(K_a c)।",
        steps=[
            {"title": "আসন্নতা", "latex": r"K_a=\dfrac{c\alpha^2}{1-\alpha}\approx c\alpha^2", "note": "α≪1।"},
            {"title": "pH", "latex": r"[\mathrm{H}^+]=\sqrt{K_a c},\ \mathrm{pH}=-\log[\mathrm{H}^+]", "note": "শক্তিশালী অ্যাসিডে [H⁺]=c।"},
        ],
        assumptions=["α≪1; একপ্রোটিক অ্যাসিড; ২৫°C"],
        questions=[
            {
                "examType": "Admission",
                "question": "K_a=10⁻⁵, c=0.1 M। pH?",
                "answer": r"[\mathrm{H}^+]=\sqrt{10^{-6}}=10^{-3};\ \mathrm{pH}=3",
            }
        ],
        trick="দুর্বল অ্যাসিড: √(K_a×c) — শক্তিশালীতে সোজা c।",
        memorize_steps=["[H⁺]=√(K_a c)", "pH=−log[H⁺]"],
        related=["buffer-henderson", "ka-kb-relation"],
        importance=3,
        order=290,
    ),
    formula(
        id="solubility-from-ksp",
        chapter="chemical-equilibrium",
        title="Solubility from Ksp",
        title_bn="Ksp থেকে দ্রাব্যতা",
        summary="AB: s=√Ksp; AB₂: s=∛(Ksp/4)",
        latex=r"AB:\ s=\sqrt{K_{sp}};\quad AB_2:\ s=\sqrt[3]{K_{sp}/4}",
        symbols=[
            {"symbol": "K_{sp}", "meaning": "দ্রাব্যতা গুণফল", "unit": "—"},
            {"symbol": "s", "meaning": "মোলার দ্রাব্যতা", "unit": "mol/L"},
        ],
        lead="সম্পৃক্ত দ্রবণে আয়ন ঘনমাত্রা থেকে Ksp; s বের করা ভর্তির ফেভারিট।",
        steps=[
            {"title": "AB প্রকার", "latex": r"K_{sp}=s\cdot s=s^2\Rightarrow s=\sqrt{K_{sp}}", "note": "AgCl, BaSO₄।"},
            {"title": "AB₂ প্রকার", "latex": r"K_{sp}=(s)(2s)^2=4s^3\Rightarrow s=\sqrt[3]{K_{sp}/4}", "note": "CaF₂, Mg(OH)₂।"},
        ],
        assumptions=["শুধুমাত্র পানিতে; কোনো জটিল আয়ন নেই"],
        questions=[
            {
                "examType": "HSC",
                "question": "AgCl-এর Ksp=10⁻¹⁰। s কত?",
                "answer": r"s=10^{-5}\,\mathrm{mol/L}",
            }
        ],
        trick="AB → √Ksp; AB₂ → ∛(Ksp/4)। চার্জ গুণে ভুলো না।",
        memorize_steps=["AB: s²=Ksp", "AB₂: 4s³=Ksp"],
        related=["precipitation-ksp", "common-ion-effect"],
        importance=3,
        order=300,
    ),
    formula(
        id="precipitation-ksp",
        chapter="chemical-equilibrium",
        title="Precipitation Condition (Ksp)",
        title_bn="অধঃক্ষেপণের শর্ত (Ksp)",
        summary="Q > Ksp হলে অধঃক্ষেপ; Q < Ksp দ্রবণ অসম্পৃক্ত",
        latex=r"Q>K_{sp}\Rightarrow\text{অধঃক্ষেপ};\quad Q<K_{sp}\Rightarrow\text{দ্রবীভূত}",
        symbols=[
            {"symbol": "Q", "meaning": "আয়নিক গুণফল (reaction quotient)", "unit": "—"},
            {"symbol": "K_{sp}", "meaning": "দ্রাব্যতা গুণফল", "unit": "—"},
        ],
        lead="মিশ্রণের পর তাত্ক্ষণিক আয়ন গুণফল Q তুলনা করো Ksp-এর সাথে।",
        steps=[
            {"title": "শর্ত", "latex": r"Q=\prod[\mathrm{ion}]^{n}", "note": "Q>Ksp → অধঃক্ষেপ শুরু।"},
            {"title": "সাম্য", "latex": r"Q=K_{sp}", "note": "সম্পৃক্ত দ্রবণ।"},
        ],
        assumptions=["২৫°C; আয়নিক শক্তি নগণ্য"],
        questions=[
            {
                "examType": "Admission",
                "question": "Q < Ksp হলে কী হবে?",
                "answer": r"\text{অধঃক্ষেপ হবে না (অসম্পৃক্ত)}",
            }
        ],
        trick="Q বড় = অধঃক্ষেপ; Q ছোট = এখনও দ্রবীভূত।",
        memorize_steps=["Q>Ksp → precipitate", "Q<Ksp → dissolve"],
        related=["solubility-from-ksp", "common-ion-effect"],
        importance=3,
        order=310,
    ),
    formula(
        id="common-ion-effect",
        chapter="chemical-equilibrium",
        title="Common Ion Effect",
        title_bn="উভয়-আয়ন প্রভাব",
        summary="উভয় আয়ন যোগে দুর্বল ইলেকট্রোলাইটের বিয়োজন কমে",
        latex=r"HA\rightleftharpoons H^++A^-;\quad [A^-]_{\mathrm{extra}}\uparrow\Rightarrow\alpha\downarrow",
        symbols=[
            {"symbol": "\\alpha", "meaning": "বিয়োজন মাত্রা", "unit": "—"},
            {"symbol": "K_a", "meaning": "বিয়োজন ধ্রুবক", "unit": "—"},
        ],
        lead="Le Chatelier: উভয় আয়ন বাড়লে সাম্য বামে সরে — দ্রাব্যতা/বিয়োজন কমে।",
        steps=[
            {"title": "দুর্বল অ্যাসিড", "latex": r"K_a=\dfrac{[\mathrm{H}^+][A^-]}{[HA]}", "note": "লবণ থেকে A⁻ যোগ → [H⁺] কমে।"},
            {"title": "দ্রাব্যতা", "latex": r"AgCl(s)\rightleftharpoons Ag^++Cl^-", "note": "NaCl যোগে Cl⁻↑ → AgCl কম দ্রবে।"},
        ],
        assumptions=["তাপমাত্রা ধ্রুব"],
        questions=[
            {
                "examType": "HSC",
                "question": "CH₃COOH-এ CH₃COONa যোগ করলে pH কী হয়?",
                "answer": r"\mathrm{pH}\uparrow\ (\text{বাফার / উভয়-আয়ন})",
            }
        ],
        trick="একই আয়ন যোগ = বিয়োজন/দ্রাব্যতা কমে — বাফার ও ধোয়ার রসায়নের চাবিকাঠি।",
        memorize_steps=["উভয় আয়ন → সাম্য বামে", "দ্রাব্যতা কমে"],
        related=["le-chatelier", "buffer-henderson", "solubility-from-ksp"],
        importance=3,
        order=320,
    ),
    formula(
        id="clausius-clapeyron",
        chapter="chemical-equilibrium",
        title="Clausius–Clapeyron Equation",
        title_bn="ক্লসিয়াস–ক্ল্যাপেইরন সমীকরণ",
        summary="বাষ্পচাপ–তাপমাত্রা: ln(P₂/P₁)=−(ΔH_v/R)(1/T₂−1/T₁)",
        latex=r"\ln\dfrac{P_2}{P_1}=-\dfrac{\Delta H_v}{R}\left(\dfrac{1}{T_2}-\dfrac{1}{T_1}\right)",
        symbols=[
            {"symbol": "P_1, P_2", "meaning": "দুই তাপমাত্রায় বাষ্পচাপ", "unit": "Pa"},
            {"symbol": "\\Delta H_v", "meaning": "বাষ্পীভবন এনথ্যালপি", "unit": "J/mol"},
            {"symbol": "T", "meaning": "পরম তাপমাত্রা", "unit": "K"},
        ],
        lead="তরল–বাষ্প সাম্যে চাপের তাপমাত্রা নির্ভরতা।",
        steps=[
            {"title": "দ্বি-বিন্দু রূপ", "latex": r"\ln(P_2/P_1)=-\dfrac{\Delta H_v}{R}(1/T_2-1/T_1)", "note": "T↑ → P↑।"},
        ],
        assumptions=["ΔH_v তাপমাত্রায় প্রায় ধ্রুব; আদর্শ বাষ্প"],
        questions=[
            {
                "examType": "Admission",
                "question": "তাপমাত্রা বাড়লে তরলের বাষ্পচাপ কী হয়?",
                "answer": r"P\uparrow",
            }
        ],
        trick="গরম করলে বাষ্পচাপ বাড়ে — ln P বনাম 1/T সরলরেখা, ঢাল −ΔH/R।",
        memorize_steps=["ln(P₂/P₁) = −(ΔH/R)(1/T₂−1/T₁)"],
        related=["van-t-hoff", "hess-law"],
        importance=2,
        order=330,
    ),
    formula(
        id="kirchhoff-enthalpy",
        chapter="chemical-equilibrium",
        title="Kirchhoff's Law (Enthalpy)",
        title_bn="কির্চফের সূত্র (এনথ্যালপি)",
        summary="ΔH(T₂)=ΔH(T₁)+ΔC_p (T₂−T₁)",
        latex=r"\Delta H(T_2)=\Delta H(T_1)+\Delta C_p(T_2-T_1)",
        symbols=[
            {"symbol": "\\Delta H", "meaning": "বিক্রিয়ার এনথ্যালপি পরিবর্তন", "unit": "J/mol"},
            {"symbol": "\\Delta C_p", "meaning": "উৎপাদ − বিক্রিয়াকের তাপধারণক্ষমতা", "unit": "J/(mol·K)"},
        ],
        lead="তাপমাত্রা বদলালে ΔH-এর সংশোধন — ΔC_p দিয়ে।",
        steps=[
            {"title": "সূত্র", "latex": r"\Delta H_2=\Delta H_1+\Delta C_p\Delta T", "note": "ΔC_p=ΣC_p(prod)−ΣC_p(react)।"},
        ],
        assumptions=["ΔC_p ধ্রুব; কোনো দশা পরিবর্তন নেই"],
        questions=[
            {
                "examType": "HSC",
                "question": "ΔC_p=0 হলে ΔH-এর তাপমাত্রা নির্ভরতা?",
                "answer": r"\Delta H\ \text{তাপমাত্রায় স্বাধীন}",
            }
        ],
        trick="ΔH বদলাতে চাইলে ΔC_p×ΔT যোগ করো।",
        memorize_steps=["ΔH₂ = ΔH₁ + ΔC_p ΔT"],
        related=["hess-law", "gibbs-helmholtz"],
        importance=2,
        order=340,
    ),
    formula(
        id="gibbs-helmholtz",
        chapter="chemical-equilibrium",
        title="Gibbs Free Energy Relation",
        title_bn="গিবসের মুক্ত শক্তি",
        summary="ΔG = ΔH − TΔS; ΔG° = −RT ln K",
        latex=r"\Delta G=\Delta H-T\Delta S,\quad \Delta G^\circ=-RT\ln K",
        symbols=[
            {"symbol": "\\Delta G", "meaning": "গিবস মুক্ত শক্তি পরিবর্তন", "unit": "J/mol"},
            {"symbol": "\\Delta H, \\Delta S", "meaning": "এনথ্যালপি ও এনট্রপি পরিবর্তন", "unit": "J/mol, J/(mol·K)"},
            {"symbol": "K", "meaning": "সাম্য ধ্রুবক", "unit": "—"},
        ],
        lead="স্বতঃস্ফূর্ততা: ΔG<0। সাম্যে ΔG=0 এবং K-এর সাথে যুক্ত।",
        steps=[
            {"title": "স্বতঃস্ফূর্ততা", "latex": r"\Delta G<0\Rightarrow\text{স্বতঃস্ফূর্ত}", "note": "ΔG>0 অস্বতঃস্ফূর্ত।"},
            {"title": "K সম্পর্ক", "latex": r"\Delta G^\circ=-RT\ln K", "note": "বড় K → ঋণাত্মক ΔG°।"},
        ],
        assumptions=["ধ্রুব T,P"],
        questions=[
            {
                "examType": "Admission",
                "question": "ΔG° ঋণাত্মক হলে K কেমন?",
                "answer": r"K>1",
            }
        ],
        trick="ΔG=ΔH−TΔS; ΔG°=−RT ln K — পরীক্ষার জোড়া সূত্র।",
        memorize_steps=["ΔG<0 = চলে", "ΔG°=−RT ln K"],
        related=["van-t-hoff", "hess-law"],
        importance=3,
        order=350,
    ),
    formula(
        id="half-life-second-order",
        chapter="chemical-equilibrium",
        title="Half-Life of Second-Order Reaction",
        title_bn="দ্বিতীয় ক্রমের অর্ধায়ু",
        summary="t₁/₂ = 1/(k[A]₀) — আদি ঘনমাত্রার উপর নির্ভর করে",
        latex=r"t_{1/2}=\dfrac{1}{k[A]_0}\quad(2\text{nd order, }2A\to\text{prod})",
        symbols=[
            {"symbol": "k", "meaning": "হার ধ্রুবক", "unit": "L/(mol·s)"},
            {"symbol": "[A]_0", "meaning": "আদি ঘনমাত্রা", "unit": "mol/L"},
            {"symbol": "t_{1/2}", "meaning": "অর্ধায়ু", "unit": "s"},
        ],
        lead="প্রথম ক্রমে t½ ধ্রুব; দ্বিতীয় ক্রমে [A]₀ বাড়লে t½ কমে।",
        steps=[
            {"title": "সূত্র", "latex": r"t_{1/2}=1/(k[A]_0)", "note": "শূন্য ক্রমে t½∝[A]₀।"},
        ],
        assumptions=["একক বিক্রিয়ক দ্বিতীয় ক্রম"],
        questions=[
            {
                "examType": "HSC",
                "question": "[A]₀ দ্বিগুণ হলে দ্বিতীয় ক্রমের t½?",
                "answer": r"t_{1/2}\ \text{অর্ধেক}",
            }
        ],
        trick="2nd order: t½ = 1/(k[A]₀) — ঘনমাত্রা↑ অর্ধায়ু↓।",
        memorize_steps=["1st: t½=ln2/k", "2nd: t½=1/(k[A]₀)"],
        related=["first-order-half-life", "activation-energy-arrhenius-plot"],
        importance=3,
        order=360,
    ),
    formula(
        id="collision-frequency-theory",
        chapter="chemical-equilibrium",
        title="Collision Theory Rate Constant",
        title_bn="সংঘর্ষ তত্ত্ব ও হার ধ্রুবক",
        summary="k = P Z e^(−E_a/RT)",
        latex=r"k=PZ\,e^{-E_a/RT}",
        symbols=[
            {"symbol": "P", "meaning": "স্টিয়ারিক গুণাঙ্ক", "unit": "—"},
            {"symbol": "Z", "meaning": "সংঘর্ষ কম্পাঙ্ক", "unit": "s⁻¹ বা L/(mol·s)"},
            {"symbol": "E_a", "meaning": "সক্রিয়ন শক্তি", "unit": "J/mol"},
        ],
        lead="কার্যকর সংঘর্ষ = সঠিক দিক (P) × যথেষ্ট শক্তি (e^(−Ea/RT))।",
        steps=[
            {"title": "সূত্র", "latex": r"k=PZe^{-E_a/RT}", "note": "Arrhenius-এর সাথে মিল: A≈PZ।"},
        ],
        assumptions=["গ্যাস দশা; দ্বিআণবিক"],
        questions=[
            {
                "examType": "HSC",
                "question": "E_a বাড়লে k কী হয়?",
                "answer": r"k\downarrow",
            }
        ],
        trick="হার = সংঘর্ষ × দিক × e^(−Ea/RT)।",
        memorize_steps=["k=PZ e^(−Ea/RT)", "A≈PZ"],
        related=["activation-energy-arrhenius-plot", "half-life-second-order"],
        importance=2,
        order=370,
    ),
    formula(
        id="cell-emf-series",
        chapter="electrochemistry",
        title="Standard Cell EMF from Series",
        title_bn="তড়িৎ রাসায়নিক শ্রেণি থেকে কোশ EMF",
        summary="E°_cell = E°_cathode − E°_anode = E°_red + E°_ox",
        latex=r"E^\circ_{\mathrm{cell}}=E^\circ_{\mathrm{cathode}}-E^\circ_{\mathrm{anode}}",
        symbols=[
            {"symbol": r"E^\circ_{\mathrm{cathode}}", "meaning": "বিজারণ বিভব (ধনাত্মক তড়িদ)", "unit": "V"},
            {"symbol": r"E^\circ_{\mathrm{anode}}", "meaning": "অ্যানোডের বিজারণ বিভব", "unit": "V"},
        ],
        lead="উচ্চতর বিজারণ বিভব = ক্যাথোড; নিম্নতর = অ্যানোড।",
        steps=[
            {"title": "সূত্র", "latex": r"E^\circ_{\mathrm{cell}}=E^\circ_R-E^\circ_L", "note": "ডান–বাম তড়িদের বিজারণ বিভব।"},
            {"title": "চিহ্ন", "latex": r"E^\circ>0\Rightarrow\text{গ্যালভানিক স্বতঃস্ফূর্ত}", "note": "ΔG°=−nFE°।"},
        ],
        assumptions=["প্রমাণ অবস্থা; জলীয় আয়ন"],
        questions=[
            {
                "examType": "HSC",
                "question": "Zn (−0.76 V) ও Cu (+0.34 V)। E°_cell?",
                "answer": r"E^\circ=0.34-(-0.76)=1.10\,\mathrm{V}",
            }
        ],
        trick="ক্যাথোড − অ্যানোড (দুটোই reduction বিভব)। Cu ডানে থাকলে ধনাত্মক।",
        memorize_steps=["E°_cell = E°_c − E°_a", "বড় E° = ক্যাথোড"],
        related=["nernst-equation", "galvanic-cell"],
        importance=3,
        order=150,
    ),
    formula(
        id="faraday-first-law",
        chapter="electrochemistry",
        title="Faraday's First Law of Electrolysis",
        title_bn="ফ্যারাডের প্রথম সূত্র",
        summary="মুক্ত পদার্থের ভর m = ZIt = (E/F)It",
        latex=r"m=ZIt=\dfrac{E}{F}It=\dfrac{M}{nF}It",
        symbols=[
            {"symbol": "m", "meaning": "জমা/মুক্ত ভর", "unit": "g"},
            {"symbol": "I, t", "meaning": "প্রবাহ ও সময়", "unit": "A, s"},
            {"symbol": "E", "meaning": "রাসায়নিক তুল্যাঙ্ক", "unit": "g/eq"},
            {"symbol": "F", "meaning": "ফ্যারাডে ধ্রুবক ≈96500", "unit": "C/mol"},
        ],
        lead="প্রবাহিত চার্জের সমানুপাতে তড়িদদ্রব্য মুক্ত হয়।",
        steps=[
            {"title": "সূত্র", "latex": r"m=ZIt,\quad Z=E/F", "note": "Q=It।"},
            {"title": "মোল রূপ", "latex": r"m=\dfrac{MIt}{nF}", "note": "n = ইলেকট্রন সংখ্যা।"},
        ],
        assumptions=["১০০% কারেন্ট দক্ষতা"],
        questions=[
            {
                "examType": "HSC",
                "question": "I দ্বিগুণ, t একই হলে m কী হয়?",
                "answer": r"m\ \text{দ্বিগুণ}",
            }
        ],
        trick="m∝Q=It — বেশি চার্জ, বেশি জমা।",
        memorize_steps=["m=ZIt", "Z=E/F=M/(nF)"],
        related=["faraday-laws", "nernst-equation"],
        importance=3,
        order=160,
    ),
    formula(
        id="beer-lambert",
        chapter="quantitative-chem",
        title="Beer–Lambert Law",
        title_bn="বিয়ার–ল্যামবার্ট সূত্র",
        summary="A = ε c l — শোষণ ঘনমাত্রার সমানুপাতিক",
        latex=r"A=\varepsilon\,c\,l=\log_{10}(I_0/I)",
        symbols=[
            {"symbol": "A", "meaning": "শোষণ (absorbance)", "unit": "—"},
            {"symbol": "\\varepsilon", "meaning": "মোলার শোষণ গুণাঙ্ক", "unit": "L/(mol·cm)"},
            {"symbol": "c", "meaning": "ঘনমাত্রা", "unit": "mol/L"},
            {"symbol": "l", "meaning": "পথ দৈর্ঘ্য", "unit": "cm"},
        ],
        lead="রঙিন দ্রবণের ঘনমাত্রা বর্ণালীমাপক দিয়ে মাপা যায়।",
        steps=[
            {"title": "সূত্র", "latex": r"A=\varepsilon c l", "note": "A বনাম c সরলরেখা (পাতলা দ্রবণ)।"},
        ],
        assumptions=["একবর্ণী আলো; পাতলা দ্রবণ; কোনো স্ক্যাটারিং নেই"],
        questions=[
            {
                "examType": "Admission",
                "question": "c দ্বিগুণ হলে A কী হয় (ল্যামবার্ট–বিয়ার)?",
                "answer": r"A\ \text{দ্বিগুণ}",
            }
        ],
        trick="A=εcl — ঘনমাত্রা মাপার সূত্র।",
        memorize_steps=["A=εcl", "A=log(I₀/I)"],
        related=["molarity-definition", "percentage-yield"],
        importance=2,
        order=90,
    ),
    formula(
        id="percentage-yield",
        chapter="quantitative-chem",
        title="Percentage Yield",
        title_bn="শতকরা উৎপাদন",
        summary="% yield = (actual / theoretical) × 100",
        latex=r"\%\ \mathrm{yield}=\dfrac{\text{actual mass}}{\text{theoretical mass}}\times 100",
        symbols=[
            {"symbol": "\\text{actual}", "meaning": "পরীক্ষায় পাওয়া ভর", "unit": "g"},
            {"symbol": "\\text{theoretical}", "meaning": "সীমায়ক থেকে হিসাবকৃত ভর", "unit": "g"},
        ],
        lead="সীমায়ক বিক্রিয়ক দিয়ে তাত্ত্বিক উৎপাদন বের করে তুলনা।",
        steps=[
            {"title": "সূত্র", "latex": r"\%\mathrm{yield}=\dfrac{m_{\mathrm{act}}}{m_{\mathrm{theo}}}\times100", "note": "সবসময় ≤100% (আদর্শ)।"},
        ],
        assumptions=["সঠিক সীমায়ক শনাক্ত"],
        questions=[
            {
                "examType": "HSC",
                "question": "তাত্ত্বিক 10 g, পাওয়া 8 g। % yield?",
                "answer": r"80\%",
            }
        ],
        trick="% yield = যা পেয়েছ / যা পাওয়ার কথা × 100।",
        memorize_steps=["সীমায়ক → theoretical", "actual/theo × 100"],
        related=["limiting-reagent-calc", "atom-economy"],
        importance=3,
        order=100,
    ),
    formula(
        id="atom-economy",
        chapter="quantitative-chem",
        title="Atom Economy",
        title_bn="পরমাণু মিতব্যয়িতা",
        summary="% atom economy = (কাঙ্ক্ষিত উৎপাদনের মোলার ভর / মোট বিক্রিয়কের মোলার ভর) × 100",
        latex=r"\%\ \mathrm{AE}=\dfrac{M_{\mathrm{desired}}}{\sum M_{\mathrm{reactants}}}\times100",
        symbols=[
            {"symbol": "M_{\mathrm{desired}}", "meaning": "কাঙ্ক্ষিত উৎপাদনের মোলার ভর", "unit": "g/mol"},
            {"symbol": "\\sum M_{\mathrm{reactants}}", "meaning": "সব বিক্রিয়কের মোট মোলার ভর", "unit": "g/mol"},
        ],
        lead="সবুজ রসায়ন: কতটা পরমাণু কাজে লাগে, কতটা বর্জ্য।",
        steps=[
            {"title": "সূত্র", "latex": r"\%\mathrm{AE}=\dfrac{M_{\mathrm{product}}}{\sum M_{\mathrm{reactants}}}\times100", "note": "যোগ বিক্রিয়ায় AE≈100%।"},
        ],
        assumptions=["stoichiometric সহগ ১:১ ধরে মোলার ভর যোগ"],
        questions=[
            {
                "examType": "HSC",
                "question": "যোগ বিক্রিয়ায় atom economy সাধারণত কেমন?",
                "answer": r"\approx 100\%",
            }
        ],
        trick="কাঙ্ক্ষিত / মোট বিক্রিয়ক × 100 — বর্জ্য কম = AE বেশি।",
        memorize_steps=["AE = desired MM / total reactant MM"],
        related=["percentage-yield", "limiting-reagent-calc"],
        importance=2,
        order=110,
    ),
    formula(
        id="cfse-octahedral",
        chapter="coordination-chemistry",
        title="CFSE for Octahedral Complex",
        title_bn="অষ্টতলকীয় জটিলের CFSE",
        summary="CFSE = (−0.4 n_t2g + 0.6 n_eg) Δ_o",
        latex=r"\mathrm{CFSE}=(-0.4\,n_{t_{2g}}+0.6\,n_{e_g})\Delta_o",
        symbols=[
            {"symbol": "n_{t_{2g}}, n_{e_g}", "meaning": "দুই সেটে ইলেকট্রন সংখ্যা", "unit": "—"},
            {"symbol": "\\Delta_o", "meaning": "অষ্টতলকীয় বিভাজন শক্তি", "unit": "cm⁻¹ / kJ·mol⁻¹"},
        ],
        lead="t₂g নিচু (−0.4Δ_o), e_g উঁচু (+0.6Δ_o) প্রতি ইলেকট্রনে।",
        steps=[
            {"title": "সূত্র", "latex": r"\mathrm{CFSE}=(-0.4n_{t_{2g}}+0.6n_{e_g})\Delta_o", "note": "জোড় শক্তি P আলাদা যোগ হয়।"},
            {"title": "উদাহরণ d³", "latex": r"t_{2g}^3\Rightarrow\mathrm{CFSE}=-1.2\Delta_o", "note": "Cr³⁺।"},
        ],
        assumptions=["অষ্টতলকীয়; শুধু CFT"],
        questions=[
            {
                "examType": "Admission",
                "question": "d⁶ low-spin (t₂g⁶)-এর CFSE?",
                "answer": r"-2.4\Delta_o",
            }
        ],
        trick="t₂g: −0.4; e_g: +0.6 — গুণে যোগ।",
        memorize_steps=["CFSE=(−0.4 n_t + 0.6 n_e)Δ_o"],
        related=["crystal-field-splitting", "efs-crystal-field-split"],
        importance=3,
        order=110,
    ),
    formula(
        id="huckel-rule",
        chapter="organic-chem",
        title="Hückel's Rule of Aromaticity",
        title_bn="হুকেলের সূত্র (অ্যারোমেটিসিটি)",
        summary="সমতল চক্রাকার সম্পৃক্ত π ব্যবস্থায় 4n+2 ইলেকট্রন = অ্যারোমেটিক",
        latex=r"(4n+2)\ \pi\ \text{electrons},\ n=0,1,2,\ldots",
        symbols=[
            {"symbol": "n", "meaning": "পূর্ণ সংখ্যা ০,১,২…", "unit": "—"},
            {"symbol": "4n+2", "meaning": "অ্যারোমেটিক π ইলেকট্রন সংখ্যা", "unit": "—"},
        ],
        lead="বেনজিন (৬=4·1+2), সাইক্লোপেন্টাডাইয়েনাইল অ্যানায়ন (৬) অ্যারোমেটিক।",
        steps=[
            {"title": "শর্ত", "latex": r"4n+2\ \pi\ e^-", "note": "চক্রাকার, সমতল, সম্পৃক্ত p অরবিটাল।"},
            {"title": "অ্যান্টিঅ্যারোমেটিক", "latex": r"4n\ \pi\ e^-", "note": "অস্থিতিশীল (যেমন সাইক্লোবিউটাডাইইন)।"},
        ],
        assumptions=["সমতল conjugated ring"],
        questions=[
            {
                "examType": "HSC",
                "question": "বেনজিনে π ইলেকট্রন সংখ্যা হুকেল মেনে?",
                "answer": r"6=4(1)+2",
            }
        ],
        trick="অ্যারোমেটিক = 2,6,10,14… (4n+2)। 4n = অ্যান্টি।",
        memorize_steps=["4n+2 = aromatic", "সমতল + conjugated"],
        related=["sn1-sn2-mechanism", "grignard-reaction"],
        importance=3,
        order=290,
    ),
    formula(
        id="soap-saponification",
        chapter="organic-chem",
        title="Saponification (Soap Formation)",
        title_bn="সাবান তৈরি (স্যপোনিফিকেশন)",
        summary="ফ্যাট/অয়েল + NaOH → সাবান (RCOONa) + গ্লিসারল",
        latex=r"\mathrm{Fat}+3\mathrm{NaOH}\rightarrow 3\mathrm{RCOONa}+\mathrm{glycerol}",
        symbols=[
            {"symbol": "RCOONa", "meaning": "সাবান (সোডিয়াম কার্বক্সিলেট)", "unit": "—"},
            {"symbol": "\\mathrm{NaOH}", "meaning": "ক্ষার (সাধারণত)", "unit": "—"},
        ],
        lead="এস্টারের ক্ষারীয় জলবিশ্লেষণ — শিল্প ও HSC জৈব।",
        steps=[
            {"title": "বিক্রিয়া", "latex": r"\mathrm{RCOOR}'+\mathrm{NaOH}\rightarrow\mathrm{RCOONa}+\mathrm{R}'OH", "note": "ট্রাইগ্লিসারাইডে তিন এস্টার।"},
        ],
        assumptions=["উত্তপ্ত ক্ষারীয় মাধ্যম"],
        questions=[
            {
                "examType": "HSC",
                "question": "স্যaponification-এর উপজাত কী?",
                "answer": r"\text{গ্লিসারল}",
            }
        ],
        trick="ফ্যাট + ক্ষার = সাবান + গ্লিসারল।",
        memorize_steps=["ক্ষারীয় hydrolysis = saponification"],
        related=["esterification", "grignard-reaction"],
        importance=2,
        order=300,
    ),
    formula(
        id="isoelectric-point",
        chapter="organic-chem",
        title="Isoelectric Point (pI)",
        title_bn="আইসোইলেকট্রিক বিন্দু",
        summary="pI = (pKa₁ + pKa₂)/2 — অ্যামিনো অ্যাসিডের নেট চার্জ শূন্য",
        latex=r"\mathrm{pI}=\dfrac{\mathrm{p}K_{a1}+\mathrm{p}K_{a2}}{2}",
        symbols=[
            {"symbol": "\\mathrm{pI}", "meaning": "আইসোইলেকট্রিক pH", "unit": "—"},
            {"symbol": "\\mathrm{p}K_{a1}, \\mathrm{p}K_{a2}", "meaning": "দ্বিমেরু আয়নের সংশ্লিষ্ট pKa", "unit": "—"},
        ],
        lead="pH = pI হলে অ্যামিনো অ্যাসিড জুইটারআয়ন, নেট চার্জ ০ — তড়িৎপ্রবাহে স্থির।",
        steps=[
            {"title": "নিস্তারক অ্যামিনো অ্যাসিড", "latex": r"\mathrm{pI}=(\\mathrm{p}K_{a}(\\mathrm{COOH})+\\mathrm{p}K_{a}(\\mathrm{NH}_3^+))/2", "note": "অম্লীয়/ক্ষারীয় পাশে ভিন্ন জোড়া।"},
        ],
        assumptions=["একক α-অ্যামিনো অ্যাসিড"],
        questions=[
            {
                "examType": "Medical",
                "question": "pH = pI হলে নেট চার্জ কত?",
                "answer": r"0",
            }
        ],
        trick="pI = দুই প্রাসঙ্গিক pKa-এর গড় — এখানে নেট চার্জ শূন্য।",
        memorize_steps=["pI=(pKa1+pKa2)/2", "pH=pI → চার্জ ০"],
        related=["buffer-henderson", "ph-weak-acid"],
        importance=2,
        order=310,
    ),
    formula(
        id="hardy-schulze",
        chapter="surface-chemistry",
        title="Hardy–Schulze Rule",
        title_bn="হার্ডি–শুলজে নিয়ম",
        summary="কয়ালয়েড অধঃক্ষেপণ ক্ষমতা ∝ বিপরীত আয়নের চার্জের ঘাত",
        latex=r"\text{flocculating power}\\propto |z|^n\\ (\\text{বিপরীত আয়ন})",
        symbols=[
            {"symbol": "z", "meaning": "বিপরীত আয়নের চার্জ সংখ্যা", "unit": "—"},
            {"symbol": "\\text{flocculation}", "meaning": "কয়ালয়েড জমাট/অধঃক্ষেপ", "unit": "—"},
        ],
        lead="As₂S₃ (−) কয়ালয়েডে Al³⁺ > Ba²⁺ > Na⁺ শক্তি।",
        steps=[
            {"title": "নিয়ম", "latex": r"\\mathrm{Al}^{3+}>\\mathrm{Ba}^{2+}>\\mathrm{Na}^{+}", "note": "চার্জ বাড়লে অল্প ঘনমাত্রায়ই জমাট।"},
        ],
        assumptions=["লাইওফোবিক সল"],
        questions=[
            {
                "examType": "HSC",
                "question": "ঋণাত্মক সলে কোন আয়ন সবচেয়ে কার্যকর?",
                "answer": r"\\text{সর্বোচ্চ ধনাত্মক চার্জের আয়ন (যেমন Al}^{3+})",
            }
        ],
        trick="বিপরীত চার্জ↑ → জমাট ক্ষমতা↑ — Hardy–Schulze।",
        memorize_steps=["flocculating power ∝ charge"],
        related=["freundlich-isotherm", "langmuir-isotherm"],
        importance=2,
        order=90,
    ),
    formula(
        id="radius-ratio-rule",
        chapter="solid-state-chemistry",
        title="Radius Ratio Rule",
        title_bn="ব্যাসার্ধ অনুপাত নিয়ম",
        summary="r₊/r₋ থেকে সমন্বয় সংখ্যা ও গঠন অনুমান",
        latex=r"\rho=\dfrac{r_+}{r_-};\ \rho<0.155\\ (\\mathrm{CN}=2)\\ \\cdots\\ \\rho>0.732\\ (\\mathrm{CN}=8)",
        symbols=[
            {"symbol": "r_+, r_-", "meaning": "ক্যাটায়ন ও অ্যানায়ন ব্যাসার্ধ", "unit": "pm"},
            {"symbol": "\\rho", "meaning": "ব্যাসার্ধ অনুপাত", "unit": "—"},
            {"symbol": "\\mathrm{CN}", "meaning": "সমন্বয় সংখ্যা", "unit": "—"},
        ],
        lead="বড় অ্যানায়নের ফাঁকে ক্যাটায়ন বসার জ্যামিতি।",
        steps=[
            {"title": "সীমা", "latex": r"0.225\\text{–}0.414:\\ \\mathrm{CN}=4\\ (\\text{tetra})", "note": "0.414–0.732: CN=6 (octa)।"},
            {"title": "উচ্চ", "latex": r">0.732:\\ \\mathrm{CN}=8\\ (\\text{bcc-type})", "note": "CsCl।"},
        ],
        assumptions=["আয়নিক কঠিন; শক্ত গোলক মডেল"],
        questions=[
            {
                "examType": "Admission",
                "question": "ρ = 0.5 হলে সম্ভাব্য CN?",
                "answer": r"6\\ (\\text{অষ্টতলকীয়})",
            }
        ],
        trick="ρ ছোট = কম CN; ρ বড় = বেশি CN।",
        memorize_steps=["ρ=r₊/r₋", "0.414–0.732 → CN 6"],
        related=["packing-efficiency", "bragg-law-chem"],
        importance=2,
        order=110,
    ),
    formula(
        id="chromatography-rf",
        chapter="qualitative-chem",
        title="Chromatography Retention Factor",
        title_bn="ক্রোমাটোগ্রাফি R_f মান",
        summary="R_f = স্পটের দূরত্ব / দ্রাবকের দূরত্ব",
        latex=r"R_f=\dfrac{\text{distance moved by spot}}{\text{distance moved by solvent}}",
        symbols=[
            {"symbol": "R_f", "meaning": "রিটেনশন ফ্যাক্টর", "unit": "— (০–১)"},
        ],
        lead="পেপার/টিএলসি-তে যৌগ শনাক্তকরণের তুলনামূলক মান।",
        steps=[
            {"title": "সূত্র", "latex": r"R_f=d_{\mathrm{spot}}/d_{\mathrm{solvent}}", "note": "সবসময় ≤1।"},
        ],
        assumptions=["একই দ্রাবক ও তাপমাত্রা"],
        questions=[
            {
                "examType": "HSC",
                "question": "দ্রাবক 10 cm, স্পট 4 cm। R_f?",
                "answer": r"R_f=0.4",
            }
        ],
        trick="R_f = স্পট/সলভেন্ট — ১-এর বেশি হয় না।",
        memorize_steps=["R_f = spot / solvent front"],
        related=["quantum-numbers"],
        importance=2,
        order=280,
    ),
    formula(
        id="mass-defect-binding",
        chapter="nuclear-chemistry",
        title="Mass Defect & Binding Energy",
        title_bn="ভর ত্রুটি ও বন্ধন শক্তি",
        summary="Δm = Z m_p + (A−Z) m_n − M; BE = Δm c²",
        latex=r"\Delta m=Zm_p+(A-Z)m_n-M,\quad BE=\Delta m\,c^2",
        symbols=[
            {"symbol": "\\Delta m", "meaning": "ভর ত্রুটি", "unit": "u বা kg"},
            {"symbol": "BE", "meaning": "বন্ধন শক্তি", "unit": "MeV"},
            {"symbol": "M", "meaning": "নিউক্লিয়াসের প্রকৃত ভর", "unit": "u"},
        ],
        lead="নিউক্লিয়াসের ভর আলাদা নিউক্লিয়নের যোগফলের চেয়ে কম — শক্তি বন্ধনে।",
        steps=[
            {"title": "ভর ত্রুটি", "latex": r"\\Delta m=Zm_p+(A-Z)m_n-M", "note": "1 u ≈ 931 MeV।"},
            {"title": "বন্ধন শক্তি", "latex": r"BE=\\Delta m\\times931\\ \\mathrm{MeV/u}", "note": "প্রতি নিউক্লিয়ন BE স্থিতিশীলতা মাপে।"},
        ],
        assumptions=["পারমাণবিক ভর এককে হিসাব"],
        questions=[
            {
                "examType": "Admission",
                "question": "1 u ভর ত্রুটির শক্তি সমতুল্য?",
                "answer": r"931\\ \\mathrm{MeV}",
            }
        ],
        trick="Δm×931 MeV = বন্ধন শক্তি। ভর কম = শক্তি বেরিয়েছে।",
        memorize_steps=["Δm = যোগফল − প্রকৃত", "BE=Δm×931 MeV"],
        related=["half-life-chem", "radioactive-decay-law-chem"],
        importance=3,
        order=110,
    ),
    formula(
        id="ideal-gas-chem",
        chapter="chemical-equilibrium",
        title="Ideal Gas Equation (Chemistry)",
        title_bn="আদর্শ গ্যাস সমীকরণ",
        summary="PV = nRT — রসায়নের গ্যাস গণনার ভিত্তি",
        latex=r"PV=nRT",
        symbols=[
            {"symbol": "P, V", "meaning": "চাপ ও আয়তন", "unit": "atm, L"},
            {"symbol": "n", "meaning": "মোল সংখ্যা", "unit": "mol"},
            {"symbol": "R", "meaning": "গ্যাস ধ্রুবক 0.0821", "unit": "L·atm/(mol·K)"},
            {"symbol": "T", "meaning": "পরম তাপমাত্রা", "unit": "K"},
        ],
        lead="মোল, চাপ, আয়তন, তাপমাত্রা এক সূত্রে — টাইট্রেশন/গ্যাস স্টয়কিওমেট্রিতে।",
        steps=[
            {"title": "সূত্র", "latex": r"PV=nRT", "note": "STP-তে 1 mol ≈ 22.4 L।"},
        ],
        assumptions=["আদর্শ গ্যাস"],
        questions=[
            {
                "examType": "HSC",
                "question": "n=1, P=1 atm, T=273 K। V?",
                "answer": r"V\\approx22.4\\ \\mathrm{L}",
            }
        ],
        trick="PV=nRT — মোল বের করতে V/22.4 (STP)।",
        memorize_steps=["PV=nRT", "R=0.0821 L·atm/mol·K"],
        related=["mole-concept", "hess-law"],
        importance=3,
        order=380,
    ),
]


def main() -> None:
    # Fix related after all written: first write with filtered related, then refresh
    for data in NEW:
        write(data)
    # second pass: update related now that new ids exist
    for data in NEW:
        path = ROOT / "chapters" / data["chapter"] / "formulas" / f"{data['id']}.json"
        raw = json.loads(path.read_text(encoding="utf-8"))
        # re-resolve related from original intent
        wanted = None
        for d in NEW:
            if d["id"] == raw["id"]:
                # get from source definition via file related field we stored
                wanted = d.get("related")
                break
        if wanted is not None:
            # recreate full related list from formula() call - stored already filtered
            # Expand: reload from NEW originals
            pass
    # Rebuild related properly
    originals = {d["id"]: d for d in NEW}
    # Re-read intended related from formula bodies - we need to store them
    # Simpler: hardcode refresh map
    refresh = {
        "henrys-law": ["raoult-law", "osmotic-pressure"],
        "ph-weak-acid": ["buffer-henderson", "ka-kb-relation", "common-ion-effect"],
        "solubility-from-ksp": ["precipitation-ksp", "common-ion-effect"],
        "precipitation-ksp": ["solubility-from-ksp", "common-ion-effect"],
        "common-ion-effect": ["le-chatelier", "buffer-henderson", "solubility-from-ksp"],
        "clausius-clapeyron": ["van-t-hoff", "hess-law"],
        "kirchhoff-enthalpy": ["hess-law", "gibbs-helmholtz"],
        "gibbs-helmholtz": ["van-t-hoff", "hess-law"],
        "half-life-second-order": ["first-order-half-life", "activation-energy-arrhenius-plot"],
        "collision-frequency-theory": ["activation-energy-arrhenius-plot", "half-life-second-order"],
        "cell-emf-series": ["nernst-equation", "galvanic-cell"],
        "faraday-first-law": ["nernst-equation", "galvanic-cell"],
        "beer-lambert": ["molarity-definition", "percentage-yield"],
        "percentage-yield": ["limiting-reagent-calc", "atom-economy"],
        "atom-economy": ["percentage-yield", "limiting-reagent-calc"],
        "cfse-octahedral": ["crystal-field-splitting"],
        "huckel-rule": ["sn1-sn2-mechanism", "grignard-reaction"],
        "soap-saponification": ["grignard-reaction"],
        "isoelectric-point": ["buffer-henderson", "ph-weak-acid"],
        "hardy-schulze": ["freundlich-isotherm", "langmuir-isotherm"],
        "radius-ratio-rule": ["packing-efficiency"],
        "chromatography-rf": ["quantum-numbers"],
        "mass-defect-binding": ["half-life-chem", "radioactive-decay-law-chem"],
        "ideal-gas-chem": ["mole-concept", "hess-law"],
    }
    for fid, rels in refresh.items():
        matches = list(ROOT.rglob(f"{fid}.json"))
        if not matches:
            continue
        path = matches[0]
        data = json.loads(path.read_text(encoding="utf-8"))
        data["related"] = [r for r in rels if r in ALL_IDS and r != fid]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Done. Added {len(NEW)} chemistry formulas.")


if __name__ == "__main__":
    main()
