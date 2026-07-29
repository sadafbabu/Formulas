#!/usr/bin/env python3
"""Physics quality pass: fix wrong formulas, retire dups, upgrade high-yield stubs."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHYS = ROOT / "content/subjects/physics"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find_id(fid: str) -> Path | None:
    matches = list(PHYS.rglob(f"{fid}.json"))
    return matches[0] if matches else None


def all_formula_paths() -> list[Path]:
    return list((ROOT / "content/subjects").rglob("formulas/*.json"))


def remap_related(retire: dict[str, str]) -> int:
    """Replace retired ids in every related[] across all subjects. Returns touch count."""
    touched = 0
    for path in all_formula_paths():
        data = load(path)
        related = data.get("related") or []
        if not related:
            continue
        new_rel: list[str] = []
        changed = False
        for rid in related:
            if rid in retire:
                replacement = retire[rid]
                changed = True
                if replacement and replacement != data["id"] and replacement not in new_rel:
                    new_rel.append(replacement)
            elif rid not in new_rel:
                new_rel.append(rid)
        if changed:
            data["related"] = new_rel
            save(path, data)
            touched += 1
    return touched


def delete_formula(fid: str) -> None:
    path = find_id(fid)
    if path and path.exists():
        path.unlink()
        print(f"  deleted {fid}")


def put(fid: str, **updates) -> None:
    path = find_id(fid)
    if not path:
        raise SystemExit(f"missing formula: {fid}")
    data = load(path)
    data.update(updates)
    # keep star tag in sync
    if "importance" in updates:
        tags = [t for t in data.get("tags", []) if not str(t).endswith("-star")]
        tags.append(f"{data['importance']}-star")
        data["tags"] = tags
    save(path, data)
    print(f"  updated {fid}")


# ---------------------------------------------------------------------------
# 1) Retire near-exact duplicates (keep stronger card)
# ---------------------------------------------------------------------------
RETIRE = {
    # weaker -> keep
    "planetary-escape-speed": "escape-velocity-planet",
    "hubble-recession-law": "hubble-law",
    "v-omega-r": "angular-linear-relation",
    "centripetal-force-mv2r": "centripetal-force",
    "ampere-force-parallel-wires": "parallel-wires",
    "thermal-conduction-rate": "heat-conduction",
}

print("Remapping related links for retired ids…")
print(f"  remapped in {remap_related(RETIRE)} files")
print("Deleting retired duplicates…")
for dead in RETIRE:
    delete_formula(dead)

# bump kept parallel-wires importance (was 1-star while stub was 3-star)
pw = find_id("parallel-wires")
if pw:
    d = load(pw)
    d["importance"] = 3
    tags = [t for t in d.get("tags", []) if not str(t).endswith("-star")]
    for need in ("hsc", "eng-admission", "medical", "varsity"):
        if need not in tags:
            tags.append(need)
    tags.append("3-star")
    d["tags"] = tags
    if "ampere-force-parallel-wires" not in (d.get("related") or []):
        # already remapped away
        pass
    related = d.get("related") or []
    for extra in ("lorentz", "force-on-wire", "wire-field"):
        if extra not in related and find_id(extra):
            related.append(extra)
    d["related"] = related
    save(pw, d)
    print("  upgraded parallel-wires to 3-star")

# ---------------------------------------------------------------------------
# 2) Correctness fixes
# ---------------------------------------------------------------------------
print("Correctness fixes…")

put(
    "magnification-mirror-lens",
    title="Lateral Magnification (Mirror & Lens)",
    titleBn="পার্শ্বীয় বিবর্ধন (দর্পণ ও লেন্স)",
    summary="m = h′/h = −v/u; লেন্সে m = f/(f−u) (কার্টেসিয়ান চিহ্নসহ)",
    latex=r"m=\dfrac{h'}{h}=-\dfrac{v}{u},\quad m=\dfrac{f}{f-u}\ (\text{লেন্স})",
    symbols=[
        {"symbol": "m", "meaning": "পার্শ্বীয় বিবর্ধন (ঋণাত্মক = উল্টো)", "unit": "—"},
        {"symbol": "h', h", "meaning": "প্রতিবিম্ব ও বস্তুর উচ্চতা", "unit": "m"},
        {"symbol": "v, u", "meaning": "প্রতিবিম্ব ও বস্তুর দূরত্ব (চিহ্নসহ)", "unit": "m"},
        {"symbol": "f", "meaning": "ফোকাস দূরত্ব", "unit": "m"},
    ],
    derivation={
        "lead": "সদৃশ ত্রিভুজ থেকে m = h′/h = −v/u। লেন্স সূত্রে v বসিয়ে m = f/(f−u)।",
        "steps": [
            {
                "title": "জ্যামিতি",
                "latex": r"m=\dfrac{h'}{h}=-\dfrac{v}{u}",
                "note": "ঋণাত্মক m মানে উল্টো প্রতিবিম্ব; |m|>1 বিবর্ধিত।",
            },
            {
                "title": "লেন্সে f দিয়ে",
                "latex": r"\dfrac1v-\dfrac1u=\dfrac1f \Rightarrow m=\dfrac{f}{f-u}",
                "note": "কার্টেসিয়ান চিহ্ন: বাস্তব বস্তুতে u ঋণাত্মক হলে সূত্র অনুযায়ী চিহ্ন মেলে।",
            },
        ],
        "assumptions": ["পাতলা লেন্স / গোলীয় দর্পণ; প্যারাক্সিয়াল রশ্মি"],
    },
    questions=[
        {
            "examType": "HSC",
            "question": "একটি অবতল দর্পণে u = −30 cm, v = −60 cm হলে বিবর্ধন কত? প্রতিবিম্ব কেমন?",
            "answer": r"m=-v/u=-(-60)/(-30)=-2;\ \text{উল্টো ও দ্বিগুণ}",
        }
    ],
    memorize={
        "trick": "m = −v/u সবসময়; |m|>1 মানে বড়। ঋণাত্মক = উল্টো।",
        "steps": ["দর্পণ/লেন্স দুটোতেই m = −v/u", "লেন্সে বিকল্প: m = f/(f−u)"],
    },
)

put(
    "glass-slab-lateral-shift",
    title="Lateral Shift by Glass Slab",
    titleBn="কাচের স্ল্যাবে পার্শ্ব সরণ",
    summary="d = t sin(i−r)/cos r; ক্ষুদ্র কোণে d ≈ t(1−1/n) sin i",
    latex=r"d=t\,\dfrac{\sin(i-r)}{\cos r}\approx t\left(1-\dfrac{1}{n}\right)\sin i",
    symbols=[
        {"symbol": "t", "meaning": "স্ল্যাবের পুরুত্ব", "unit": "m"},
        {"symbol": "i, r", "meaning": "আপতন ও প্রতিসরণ কোণ", "unit": "rad বা °"},
        {"symbol": "n", "meaning": "স্ল্যাবের প্রতিসরাঙ্ক", "unit": "—"},
        {"symbol": "d", "meaning": "পার্শ্ব সরণ", "unit": "m"},
    ],
    derivation={
        "lead": "স্ল্যাব রশ্মি সমান্তরাল রাখে কিন্তু পার্শ্বে সরায়। লম্ব আপতনে (i=0) সরণ শূন্য।",
        "steps": [
            {
                "title": "জ্যামিতিক সরণ",
                "latex": r"d=t\,\dfrac{\sin(i-r)}{\cos r}",
                "note": "প্রতিসরণ: n = sin i / sin r।",
            },
            {
                "title": "ক্ষুদ্র কোণ / near-normal",
                "latex": r"d\approx t\left(1-\dfrac{1}{n}\right)\sin i",
                "note": "শুধু t(1−1/n) লেখা ভুল — sin i বাদ গেলে লম্ব আপতনেও সরণ থাকার মতো মনে হয়।",
            },
        ],
        "assumptions": ["সমান্তরাল মুখ; বায়ু–কাচ–বায়ু; একবর্ণী আলো"],
    },
    questions=[
        {
            "examType": "Admission",
            "question": "n=1.5, t=6 cm, i=30° হলে পার্শ্ব সরণের আসন্ন মান কত? (sin 30°=1/2)",
            "answer": r"d\approx 6(1-1/1.5)(1/2)=6\cdot\tfrac13\cdot\tfrac12=1\\ \mathrm{cm}",
        }
    ],
    memorize={
        "trick": "লম্বে সরণ ০; আনুমানিক d ≈ t(1−1/n)sin i — sin i ভুলো না।",
        "steps": [],
    },
)

put(
    "oblique-collision",
    title="Oblique Collision",
    titleBn="তির্যক সংঘর্ষ",
    summary="স্পর্শক উপাংশ অপরিবর্তিত; অভিলম্ব বরাবর 1D সংঘর্ষ",
    latex=r"v_{1t}=u_{1t},\ v_{2t}=u_{2t};\quad m_1u_{1n}+m_2u_{2n}=m_1v_{1n}+m_2v_{2n}",
    symbols=[
        {"symbol": "u_{it}, v_{it}", "meaning": "i-তম বস্তুর স্পর্শক বেগ উপাংশ", "unit": "m/s"},
        {"symbol": "u_{in}, v_{in}", "meaning": "অভিলম্ব (line of impact) উপাংশ", "unit": "m/s"},
        {"symbol": "m_1, m_2", "meaning": "দুই বস্তুর ভর", "unit": "kg"},
        {"symbol": "e", "meaning": "পুনরুদ্ধার গুণাঙ্ক (প্রয়োজনে)", "unit": "—"},
    ],
    derivation={
        "lead": "মসৃণ গোলকের সংঘর্ষে আবেগ শুধু সাধারণ অভিলম্ব বরাবর — স্পর্শকে বল নেই।",
        "steps": [
            {
                "title": "স্পর্শক",
                "latex": r"v_{1t}=u_{1t},\quad v_{2t}=u_{2t}",
                "note": "প্রতিটি কণার স্পর্শক উপাংশ আলাদাভাবে অপরিবর্তিত।",
            },
            {
                "title": "অভিলম্ব — ভরবেগ",
                "latex": r"m_1u_{1n}+m_2u_{2n}=m_1v_{1n}+m_2v_{2n}",
                "note": "অভিলম্বে একমাত্রিক সংঘর্ষের মতো।",
            },
            {
                "title": "পুনরুদ্ধার গুণাঙ্ক",
                "latex": r"e=\dfrac{v_{2n}-v_{1n}}{u_{1n}-u_{2n}}",
                "note": "স্থিতিস্থাপক: e=1; সম্পূর্ণ অস্থিতিস্থাপক: e=0।",
            },
        ],
        "assumptions": ["মসৃণ তল / ঘর্ষণহীন স্পর্শ; আবেগ অভিলম্ব বরাবর"],
    },
    questions=[
        {
            "examType": "Admission",
            "question": "তির্যক সংঘর্ষে কোন উপাংশ অপরিবর্তিত থাকে?",
            "answer": r"\text{স্পর্শক (tangential) উপাংশ}",
        }
    ],
    memorize={
        "trick": "Tangent একই থাকে; Normal-এ 1D collision + e।",
        "steps": [],
    },
    related=["elastic-collision", "momentum-impulse"],
)

put(
    "coaxial-cable-field",
    title="Coaxial Cable Magnetic Field",
    titleBn="কো-অ্যাক্সিয়াল ক্যাবলের চৌম্বক ক্ষেত্র",
    summary="ভিতরে ∝ r; ফাঁকে ∝ 1/r; বাইরে B=0 (রিটার্ন কারেন্ট)",
    latex=r"B=\dfrac{\mu_0 I r}{2\pi a^2}\ (r<a),\quad \dfrac{\mu_0 I}{2\pi r}\ (a<r<b),\quad 0\ (r>b)",
    symbols=[
        {"symbol": "a", "meaning": "অভ্যন্তরীণ পরিবাহীর ব্যাসার্ধ", "unit": "m"},
        {"symbol": "b", "meaning": "বাহ্যিক শিল্ডের ব্যাসার্ধ", "unit": "m"},
        {"symbol": "I", "meaning": "অভ্যন্তরে +I, শিল্ডে −I", "unit": "A"},
        {"symbol": "r", "meaning": "অক্ষ থেকে দূরত্ব", "unit": "m"},
        {"symbol": "B", "meaning": "চৌম্বক ক্ষেত্র", "unit": "T"},
    ],
    derivation={
        "lead": "অ্যাম্পিয়ারের সূত্র ∮B·dl = μ₀ I_enc — তিন অঞ্চলে আলাদা I_enc।",
        "steps": [
            {
                "title": "r < a (নিরেট তারের ভিতর)",
                "latex": r"I_{\mathrm{enc}}=I\frac{r^2}{a^2}\Rightarrow B=\dfrac{\mu_0 I r}{2\pi a^2}",
                "note": "প্রবাহ সমানভাবে বিস্তৃত ধরে।",
            },
            {
                "title": "a < r < b (দুই পরিবাহীর মাঝে)",
                "latex": r"I_{\mathrm{enc}}=I\Rightarrow B=\dfrac{\mu_0 I}{2\pi r}",
                "note": "দীর্ঘ সরল তারের মতো।",
            },
            {
                "title": "r > b (ক্যাবলের বাইরে)",
                "latex": r"I_{\mathrm{enc}}=I+(-I)=0\Rightarrow B=0",
                "note": "এজন্যই কো-অ্যাক্সিয়াল শিল্ডিং দেয়।",
            },
        ],
        "assumptions": ["অসীম দীর্ঘ; স্থির প্রবাহ; শিল্ডে সমান বিপরীত প্রবাহ"],
    },
    questions=[
        {
            "examType": "BUET Admission",
            "question": "কো-অ্যাক্সিয়াল ক্যাবলের বাইরে (r>b) B কত? কেন?",
            "answer": r"B=0;\ I_{\mathrm{enc}}=I-I=0",
        }
    ],
    memorize={
        "trick": "ভিতরে ∝r, মাঝে ∝1/r, বাইরে ০।",
        "steps": ["বাইরে মোট ঘেরা প্রবাহ শূন্য → B=0"],
    },
    related=["amperes-law", "wire-field"],
)

put(
    "magnetic-hysteresis-loss",
    title="Hysteresis Power Loss",
    titleBn="হিস্টেরেসিস শক্তি অপচয়",
    summary="প্রতি চক্রে শক্তি = V×(B–H loop area); ক্ষমতা = f গুণ",
    latex=r"U_{\mathrm{cycle}}=V\oint H\,dB,\quad P_{\mathrm{hys}}=f\,V\times(\text{B–H loop area})",
    symbols=[
        {"symbol": "U_{\\mathrm{cycle}}", "meaning": "এক চক্রে মোট শক্তি অপচয়", "unit": "J"},
        {"symbol": "P_{\\mathrm{hys}}", "meaning": "গড় হিস্টেরেসিস ক্ষমতা", "unit": "W"},
        {"symbol": "V", "meaning": "কোরের আয়তন", "unit": "m³"},
        {"symbol": "f", "meaning": "চক্র কম্পাঙ্ক", "unit": "Hz"},
        {"symbol": "\\oint H\\,dB", "meaning": "B–H লুপের ক্ষেত্রফল", "unit": "J/m³"},
    ],
    derivation={
        "lead": "একক আয়তনে প্রতি চক্রে কাজ = লুপের ক্ষেত্রফল; ক্ষমতা পেতে f ও V দিয়ে গুণ।",
        "steps": [
            {
                "title": "চক্রীয় কাজ",
                "latex": r"u=\oint H\,dB,\quad U_{\mathrm{cycle}}=V u",
                "note": "নরম লোহার লুপ চিকন → কম অপচয়।",
            },
            {
                "title": "গড় ক্ষমতা",
                "latex": r"P_{\mathrm{hys}}=f U_{\mathrm{cycle}}=f V\times(\text{loop area})",
                "note": "P একক ওয়াট (W), শক্তি জুল (J) নয়।",
            },
        ],
        "assumptions": ["পর্যাবৃত্ত AC চৌম্বক চক্র; সমসত্ত্ব কোর"],
    },
    questions=[
        {
            "examType": "Admission",
            "question": "V=0.002 m³, loop area=250 J/m³, f=50 Hz। ১ ঘণ্টায় মোট অপচয় কত?",
            "answer": r"P=0.002\times50\times250=25\\mathrm{W};\ E=25\times3600=90\\mathrm{kJ}",
        }
    ],
    memorize={
        "trick": "অপচয় শক্তি/চক্র = V×লুপ; ক্ষমতা = f×তা। চিকন লুপ = কম অপচয়।",
        "steps": [],
    },
)

put(
    "pair-production",
    title="Pair Production",
    titleBn="জোড় উৎপাদন",
    summary="γ → e⁻ + e⁺; ন্যূনতম Eγ = 2m_e c² = 1.022 MeV (নিউক্লিয়াসের কাছে)",
    latex=r"\gamma\to e^-+e^+,\quad E_\gamma\ge 2m_ec^2=1.022\,\mathrm{MeV}",
    symbols=[
        {"symbol": "E_\\gamma", "meaning": "ফোটনের শক্তি", "unit": "MeV"},
        {"symbol": "m_e c^2", "meaning": "ইলেকট্রনের বিশ্রাম শক্তি", "unit": "0.511 MeV"},
        {"symbol": "e^-, e^+", "meaning": "ইলেকট্রন–পজিট্রন জোড়", "unit": "—"},
    ],
    derivation={
        "lead": "শক্তি ও ভরবেগ সংরক্ষণে নিউক্লিয়াস প্রয়োজন; থ্রেশহোল্ড ২×০.৫১১ MeV।",
        "steps": [
            {
                "title": "ভর–শক্তি",
                "latex": r"E_{\min}=2m_ec^2=1.022\,\mathrm{MeV}",
                "note": "অতিরিক্ত শক্তি KE হিসেবে জোড়ে যায়।",
            },
            {
                "title": "বিপরীত প্রক্রিয়া",
                "latex": r"e^-+e^+\to 2\gamma\ (\text{annihilation})",
                "note": "ধ্বংসে সাধারণত দুইটি ০.৫১১ MeV ফোটন।",
            },
        ],
        "assumptions": ["নিউক্লিয়াসের কাছে ঘটে; শূন্যে অসম্ভব (ভরবেগ)"],
    },
    questions=[
        {
            "examType": "HSC",
            "question": "জোড় উৎপাদনের ন্যূনতম ফোটন শক্তি কত?",
            "answer": r"1.022\,\mathrm{MeV}=2m_ec^2",
        }
    ],
    memorize={
        "trick": "১.০২২ MeV = দুই ইলেকট্রনের বিশ্রাম শক্তি; পরে annihilation → ২γ।",
        "steps": [],
    },
    related=["mass-energy-photoelectric", "de-broglie-wavelength", "stopping-potential"],
)

put(
    "optical-fiber",
    title="Optical Fibre Numerical Aperture",
    titleBn="অপটিক্যাল ফাইবার ও NA",
    summary="NA = √(n₁²−n₂²) = n₀ sin i_a (বায়ুতে n₀=1 → NA=sin i_a)",
    latex=r"\mathrm{NA}=\sqrt{n_1^2-n_2^2}=n_0\sin i_a",
    symbols=[
        {"symbol": "n_1", "meaning": "কোরের প্রতিসরাঙ্ক", "unit": "—"},
        {"symbol": "n_2", "meaning": "ক্ল্যাডিংয়ের প্রতিসরাঙ্ক", "unit": "—"},
        {"symbol": "n_0", "meaning": "বাহ্যিক মাধ্যম (সাধারণত বায়ু=1)", "unit": "—"},
        {"symbol": "i_a", "meaning": "গ্রহণ কোণ (acceptance angle)", "unit": "°"},
        {"symbol": "\\mathrm{NA}", "meaning": "সাংখ্যিক অ্যাপারচার", "unit": "—"},
    ],
    derivation={
        "lead": "কোর–ক্ল্যাডিং সীমায় TIR; বাইরের মাধ্যম থেকে সর্বোচ্চ গ্রহণ কোণ i_a।",
        "steps": [
            {
                "title": "সমালোচক কোণ",
                "latex": r"\sin c=\dfrac{n_2}{n_1}",
                "note": "ক্ল্যাডিংয়ে TIR-এর শর্ত।",
            },
            {
                "title": "NA",
                "latex": r"n_0\sin i_a=\sqrt{n_1^2-n_2^2}=\mathrm{NA}",
                "note": "বায়ুতে n₀=1 হলে NA=sin i_a।",
            },
        ],
        "assumptions": ["ধাপ-সূচক ফাইবার; একবর্ণী; প্যারাক্সিয়াল"],
    },
    questions=[
        {
            "examType": "Admission",
            "question": "n₁=1.50, n₂=1.40, বায়ু থেকে আলো। NA ও i_a কত?",
            "answer": r"\mathrm{NA}=\sqrt{1.5^2-1.4^2}=\sqrt{0.29}\approx0.54;\ i_a=\arcsin(0.54)",
        }
    ],
    memorize={
        "trick": "বড় NA = বেশি আলো ধরে; বায়ুতে NA=sin i_a।",
        "steps": [],
    },
    related=["total-internal-reflection", "critical-angle"],
)

put(
    "helical-path-magnetic",
    title="Helical Path in Magnetic Field",
    titleBn="চৌম্বক ক্ষেত্রে হেলিক্স পথ",
    summary="r = mv_⊥/(|q|B); T = 2πm/(|q|B); pitch = v_∥ T",
    latex=r"r=\dfrac{mv_\perp}{|q|B},\quad T=\dfrac{2\pi m}{|q|B},\quad p=v_\parallel T",
    symbols=[
        {"symbol": "v_\\perp", "meaning": "B-এর লম্ব বেগ উপাংশ", "unit": "m/s"},
        {"symbol": "v_\\parallel", "meaning": "B-এর সমান্তরাল উপাংশ", "unit": "m/s"},
        {"symbol": "|q|", "meaning": "চার্জের মান", "unit": "C"},
        {"symbol": "p", "meaning": "হেলিক্সের পিচ", "unit": "m"},
        {"symbol": "T", "meaning": "সাইক্লোট্রন পর্যায়কাল", "unit": "s"},
    ],
    derivation={
        "lead": "θ কোণে প্রবেশ → পথ হেলিক্স। |q| ব্যবহার করো যাতে চিহ্ন ব্যাসার্ধে না ঢোকে।",
        "steps": [
            {
                "title": "ব্যাসার্ধ",
                "latex": r"r=\dfrac{mv\sin\theta}{|q|B}",
                "note": "v_⊥ = v sinθ।",
            },
            {
                "title": "পিচ",
                "latex": r"p=v\cos\theta\cdot T=\dfrac{2\pi m v_\parallel}{|q|B}",
                "note": "এক পাকে অক্ষীয় অগ্রগতি।",
            },
        ],
        "assumptions": ["অভিন্ন B; শুধু চৌম্বক বল; অ-আপেক্ষিক"],
    },
    questions=[
        {
            "examType": "Admission",
            "question": "B-এর সমান্তরালে চার্জ ছাড়লে পথ কী?",
            "answer": r"\text{সরলরেখা}\ (F=0)",
        }
    ],
    memorize={
        "trick": "সমান্তরাল → সরল; লম্ব → বৃত্ত; কোণ → হেলিক্স। r,T-এ |q|।",
        "steps": [],
    },
    related=["lorentz", "cyclotron-radius", "cyclotron-freq"],
)

put(
    "group-cells-max-power",
    title="Grouping of Cells for Max Power",
    titleBn="কোষ বিন্যাস ও সর্বোচ্চ ক্ষমতা",
    summary="সর্বোচ্চ পাওয়ার যখন R = r_eq; m×n কোষে r_eq = nr/m",
    latex=r"P_{\max}\ \text{when}\ R=r_{\mathrm{eq}}=\dfrac{nr}{m}\ (N=mn),\quad I=\dfrac{nE}{nr+mR}",
    symbols=[
        {"symbol": "n", "meaning": "প্রতি সারিতে সিরিজ কোষ", "unit": "—"},
        {"symbol": "m", "meaning": "সমান্তরাল সারির সংখ্যা", "unit": "—"},
        {"symbol": "N=mn", "meaning": "মোট কোষ", "unit": "—"},
        {"symbol": "E, r", "meaning": "প্রতি কোষের emf ও অভ্যন্তরীণ রোধ", "unit": "V, Ω"},
        {"symbol": "R", "meaning": "বাহ্যিক রোধ", "unit": "Ω"},
    ],
    derivation={
        "lead": "মিশ্র বিন্যাসে সমতুল্য emf = nE, সমতুল্য অভ্যন্তরীণ রোধ = nr/m।",
        "steps": [
            {
                "title": "সমতুল্য বর্তনী",
                "latex": r"E_{\mathrm{eq}}=nE,\quad r_{\mathrm{eq}}=\dfrac{nr}{m},\quad I=\dfrac{nE}{nr/m+R}",
                "note": "I = nE / (nr + mR) রূপেও লেখা যায়।",
            },
            {
                "title": "সর্বোচ্চ ক্ষমতা",
                "latex": r"R=r_{\mathrm{eq}}=\dfrac{nr}{m}",
                "note": "ম্যাচিং কন্ডিশন: বাহ্যিক রোধ = সমতুল্য অভ্যন্তরীণ রোধ।",
            },
        ],
        "assumptions": ["অভিন্ন কোষ; কোনো লিকেজ নেই"],
    },
    questions=[
        {
            "examType": "HSC",
            "question": "R = r_eq হলে বাহ্যিক রোধে ক্ষমতা কেন সর্বোচ্চ?",
            "answer": r"P=I^2R;\ I=\dfrac{E_{\mathrm{eq}}}{r_{\mathrm{eq}}+R}\Rightarrow P\ \max\ \text{at}\ R=r_{\mathrm{eq}}",
        }
    ],
    memorize={
        "trick": "ম্যাচ করো: R = nr/m। সিরিজ বেশি → r_eq বাড়ে।",
        "steps": [],
    },
    related=["cells-series-parallel", "ohms-law"],
)

put(
    "rc-charging",
    title="RC Charging",
    titleBn="RC চার্জিং",
    summary="q = Q(1−e^(−t/τ)), τ = RC; t=τ-এ ~৬৩% চার্জ",
    latex=r"q=Q(1-e^{-t/\tau}),\quad \tau=RC,\quad Q=CV",
    symbols=[
        {"symbol": "q(t)", "meaning": "t সময়ে ধারকের চার্জ", "unit": "C"},
        {"symbol": "Q=CV", "meaning": "চূড়ান্ত চার্জ", "unit": "C"},
        {"symbol": "\\tau=RC", "meaning": "সময় ধ্রুবক", "unit": "s"},
        {"symbol": "V", "meaning": "ব্যাটারির emf", "unit": "V"},
    ],
    derivation={
        "lead": "KVL: V = q/C + IR → ডিফারেনশিয়াল সমীকরণ সমাধান।",
        "steps": [
            {
                "title": "চার্জিং",
                "latex": r"q=Q(1-e^{-t/RC}),\quad i=\dfrac{V}{R}e^{-t/RC}",
                "note": "t=0-এ i সর্বোচ্চ; t→∞-এ q→Q, i→0।",
            },
            {
                "title": "ডিসচার্জিং",
                "latex": r"q=Qe^{-t/RC}",
                "note": "একই τ; প্রতি τ-এ অবশিষ্ট ≈ ৩৭%।",
            },
        ],
        "assumptions": ["ধ্রুব R,C; আদর্শ ব্যাটারি; t=0-এ খালি ধারক"],
    },
    questions=[
        {
            "examType": "HSC",
            "question": "R=1 MΩ, C=1 μF। τ কত? t=τ-এ চার্জের অংশ?",
            "answer": r"\tau=RC=1\\mathrm{s};\ q/Q=1-e^{-1}\\approx0.63",
        }
    ],
    memorize={
        "trick": "τ=RC; এক τ-এ ৬৩% চার্জ, পাঁচ τ-এ প্রায় পূর্ণ।",
        "steps": [],
    },
    related=["cells-series-parallel", "ohms-law"],
)

# Differentiate 1D relative velocity (was identical latex to 2D)
put(
    "relative-velocity-1d",
    title="Relative Velocity (1D)",
    titleBn="আপেক্ষিক বেগ (একমাত্রিক)",
    summary="একই রেখায়: v_AB = v_A − v_B (চিহ্নসহ)",
    latex=r"v_{AB}=v_A-v_B\quad(\text{1D, চিহ্নসহ})",
    symbols=[
        {"symbol": "v_A, v_B", "meaning": "ভূমি সাপেক্ষে বেগ (চিহ্নসহ)", "unit": "m/s"},
        {"symbol": "v_{AB}", "meaning": "B সাপেক্ষে A-এর বেগ", "unit": "m/s"},
    ],
    derivation={
        "lead": "একই সরলরেখায় চিহ্ন ঠিক রাখলে বিয়োগই যথেষ্ট।",
        "steps": [
            {
                "title": "সংজ্ঞা",
                "latex": r"v_{AB}=v_A-v_B",
                "note": "ধনাত্মক দিক আগে ঠিক করো।",
            },
            {
                "title": "বিপরীত",
                "latex": r"v_{BA}=-v_{AB}",
                "note": "আপেক্ষিক বেগের দিক উল্টো হয়।",
            },
        ],
        "assumptions": ["একমাত্রিক গতি; ধ্রুব বেগ বা তাৎক্ষণিক বেগ"],
    },
    questions=[
        {
            "examType": "HSC",
            "question": "A: +20 m/s, B: +5 m/s। B সাপেক্ষে A-এর বেগ?",
            "answer": r"v_{AB}=20-5=15\\mathrm{m/s}",
        }
    ],
    memorize={
        "trick": "আপেক্ষিক = নিজের − অন্যের (একই চিহ্ন নিয়মে)।",
        "steps": [],
    },
    related=["relative-velocity-2d", "rain-man-relative"],
)

# ---------------------------------------------------------------------------
# 3) High-yield stub upgrades
# ---------------------------------------------------------------------------
print("Upgrading high-yield stubs…")

UPGRADES: dict[str, dict] = {
    "atwood-machine": {
        "summary": "m₁>m₂ হলে a=(m₁−m₂)g/(m₁+m₂); T=2m₁m₂g/(m₁+m₂)",
        "symbols": [
            {"symbol": "m_1, m_2", "meaning": "দুই ভর (m₁>m₂ ধরা)", "unit": "kg"},
            {"symbol": "a", "meaning": "সিস্টেমের ত্বরণ", "unit": "m/s²"},
            {"symbol": "T", "meaning": "দড়ির টান", "unit": "N"},
            {"symbol": "g", "meaning": "অভিকর্ষজ ত্বরণ", "unit": "m/s²"},
        ],
        "derivation": {
            "lead": "নিউটনের সূত্র: m₁g−T=m₁a, T−m₂g=m₂a — যোগ/বিয়োগে a ও T।",
            "steps": [
                {
                    "title": "ত্বরণ",
                    "latex": r"a=\dfrac{(m_1-m_2)g}{m_1+m_2}",
                    "note": "ভরপার্থক্য/মোটভর × g।",
                },
                {
                    "title": "টান",
                    "latex": r"T=\dfrac{2m_1m_2}{m_1+m_2}g",
                    "note": "T সবসময় ছোট ভরের ওজনের চেয়ে বেশি, বড়টির চেয়ে কম।",
                },
            ],
            "assumptions": ["ভরহীন ঘর্ষণহীন কপিকল; অটুট দড়ি; g অভিন্ন"],
        },
        "questions": [
            {
                "examType": "Admission",
                "question": "m₁=5 kg, m₂=3 kg। a ও T কত? (g=10)",
                "answer": r"a=\dfrac{2}{8}\cdot10=2.5\\mathrm{m/s^2},\ T=\dfrac{2\cdot5\cdot3}{8}\cdot10=37.5\\mathrm{N}",
            }
        ],
        "memorize": {
            "trick": "a = Δm·g / Σm; T = 2μg যেখানে μ = সমতুল্য ভর m₁m₂/(m₁+m₂)।",
            "steps": [],
        },
        "related": ["momentum-impulse", "inclined-plane-connected"],
    },
    "meter-bridge": {
        "summary": "হুইটস্টোন: X = R·l/(100−l); l = জকির অবস্থান (cm)",
        "symbols": [
            {"symbol": "X", "meaning": "অজানা রোধ", "unit": "Ω"},
            {"symbol": "R", "meaning": "জানা রোধ বাক্স", "unit": "Ω"},
            {"symbol": "l", "meaning": "বাম অংশের দৈর্ঘ্য (জকি)", "unit": "cm"},
            {"symbol": "100-l", "meaning": "ডান অংশের দৈর্ঘ্য", "unit": "cm"},
        ],
        "derivation": {
            "lead": "মিটার তারের রোধ দৈর্ঘ্যের সমানুপাতিক → হুইটস্টোন অনুপাত।",
            "steps": [
                {
                    "title": "অনুপাত",
                    "latex": r"\dfrac{P}{Q}=\dfrac{l}{100-l}",
                    "note": "P,Q তারের দুই অংশের রোধ।",
                },
                {
                    "title": "অজানা রোধ",
                    "latex": r"X=R\dfrac{l}{100-l}",
                    "note": "X যে বাহুতে, l সেই দিকের দৈর্ঘ্য।",
                },
            ],
            "assumptions": ["একসমান তার; সংযোগ রোধ নগণ্য; নাল বিন্দুতে গ্যালভানোমিটার"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "R=2 Ω, l=40 cm হলে X কত?",
                "answer": r"X=2\cdot\dfrac{40}{60}=\\dfrac{4}{3}\\Omega",
            }
        ],
        "memorize": {
            "trick": "X/R = l/(100−l) — l সেন্টিমিটারে।",
            "steps": [],
        },
        "related": ["wheatstone-bridge", "ohms-law"],
    },
    "einstein-photoelectric": {
        "summary": "K_max = hf − φ = eV₀; কাট-অফ f₀ = φ/h",
        "latex": r"K_{\max}=hf-\phi=h(f-f_0)=eV_0",
        "symbols": [
            {"symbol": "h", "meaning": "প্ল্যাঙ্ক ধ্রুবক", "unit": "J·s"},
            {"symbol": "f, f_0", "meaning": "আলোর কম্পাঙ্ক ও থ্রেশহোল্ড", "unit": "Hz"},
            {"symbol": "\\phi", "meaning": "কাজফল (work function)", "unit": "J বা eV"},
            {"symbol": "V_0", "meaning": "স্টপিং বিভব", "unit": "V"},
            {"symbol": "K_{\\max}", "meaning": "সর্বোচ্চ গতিশক্তি", "unit": "J"},
        ],
        "derivation": {
            "lead": "এক ফোটন এক ইলেকট্রনকে φ শক্তি দিয়ে মুক্ত করে; বাদবাকি KE।",
            "steps": [
                {
                    "title": "আইনস্টাইন সমীকরণ",
                    "latex": r"hf=\phi+K_{\max}",
                    "note": "তিব্রতা বাড়লে ইলেকট্রন সংখ্যা বাড়ে, K_max নয়।",
                },
                {
                    "title": "স্টপিং পটেনশিয়াল",
                    "latex": r"K_{\max}=eV_0=h(f-f_0)",
                    "note": "V₀–f রেখার ঢাল = h/e।",
                },
            ],
            "assumptions": ["এক ফোটন–এক ইলেকট্রন; তাপীয় নির্গমন নগণ্য"],
        },
        "questions": [
            {
                "examType": "Admission",
                "question": "φ=2 eV, λ=400 nm। K_max? (hc≈1240 eV·nm)",
                "answer": r"hf=1240/400=3.1\\mathrm{eV};\ K_{\max}=3.1-2=1.1\\mathrm{eV}",
            }
        ],
        "memorize": {
            "trick": "hf = φ + K_max; f₀=φ/h; K_max=eV₀।",
            "steps": [],
        },
        "related": ["stopping-potential", "photoelectric-threshold", "de-broglie-wavelength"],
    },
    "doppler-effect-general": {
        "summary": "f′ = f(v±v_o)/(v±v_s); কাছে এলে কম্পাঙ্ক বাড়ে",
        "symbols": [
            {"symbol": "f, f'", "meaning": "প্রকৃত ও শ্রুত কম্পাঙ্ক", "unit": "Hz"},
            {"symbol": "v", "meaning": "শব্দের বেগ মাধ্যমে", "unit": "m/s"},
            {"symbol": "v_o", "meaning": "পর্যবেক্ষকের বেগ", "unit": "m/s"},
            {"symbol": "v_s", "meaning": "উৎসের বেগ", "unit": "m/s"},
        ],
        "derivation": {
            "lead": "পর্যবেক্ষক কাছে → লবতে +; উৎস কাছে → হরে − (তরঙ্গদৈর্ঘ্য কমে)।",
            "steps": [
                {
                    "title": "সাধারণ সূত্র",
                    "latex": r"f'=f\,\dfrac{v\pm v_o}{v\pm v_s}",
                    "note": "চিহ্ন: কাছে আসা = কম্পাঙ্ক বাড়ে।",
                },
                {
                    "title": "উদাহরণ — উৎস কাছে",
                    "latex": r"f'=f\dfrac{v}{v-v_s}",
                    "note": "পর্যবেক্ষক স্থির।",
                },
            ],
            "assumptions": ["নিশ্চল মাধ্যম; v_s < v; শব্দ/যান্ত্রিক তরঙ্গ"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "উৎস 340 Hz, v=340 m/s, v_s=20 m/s কাছে আসছে। f′?",
                "answer": r"f'=340\cdot\dfrac{340}{340-20}=340\cdot\dfrac{340}{320}=361.25\\mathrm{Hz}",
            }
        ],
        "memorize": {
            "trick": "NUM: observer towards +; DEN: source towards −।",
            "steps": [],
        },
        "related": ["echo-formula", "beats-frequency", "wave-v-f-lambda"],
    },
    "organ-pipe-open": {
        "summary": "মুক্ত পাইপ: f_n = n v/(2L); সব গুণিতক",
        "symbols": [
            {"symbol": "L", "meaning": "পাইপের দৈর্ঘ্য", "unit": "m"},
            {"symbol": "v", "meaning": "শব্দের বেগ", "unit": "m/s"},
            {"symbol": "n", "meaning": "হারমোনিক ক্রম (১,২,৩…)", "unit": "—"},
            {"symbol": "f_1", "meaning": "মূল সুর = v/(2L)", "unit": "Hz"},
        ],
        "derivation": {
            "lead": "দুই প্রান্তে প্রসারণ-প্রকোষ্ঠ → L = n λ/2।",
            "steps": [
                {
                    "title": "তরঙ্গদৈর্ঘ্য",
                    "latex": r"L=n\dfrac{\lambda}{2}\Rightarrow \lambda=\dfrac{2L}{n}",
                    "note": "n=1,2,3,…",
                },
                {
                    "title": "কম্পাঙ্ক",
                    "latex": r"f_n=n\dfrac{v}{2L}",
                    "note": "সব পূর্ণ গুণিতক উপস্থিত।",
                },
            ],
            "assumptions": ["প্রান্ত সংশোধন নগণ্য; অনুরণন"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "L=0.5 m, v=340 m/s। মূল সুর?",
                "answer": r"f_1=v/(2L)=340\\mathrm{Hz}",
            }
        ],
        "memorize": {
            "trick": "Open = সব হারমোনিক; f₁=v/2L।",
            "steps": [],
        },
        "related": ["organ-pipe-closed", "beats-frequency", "wave-v-f-lambda"],
    },
    "organ-pipe-closed": {
        "summary": "বন্ধ পাইপ: f_n = (2n−1)v/(4L); শুধু বিজোড়",
        "symbols": [
            {"symbol": "L", "meaning": "পাইপের দৈর্ঘ্য", "unit": "m"},
            {"symbol": "v", "meaning": "শব্দের বেগ", "unit": "m/s"},
            {"symbol": "n", "meaning": "ক্রম ১,২,৩… → ১ম,৩ম,৫ম…", "unit": "—"},
            {"symbol": "f_1", "meaning": "মূল সুর = v/(4L)", "unit": "Hz"},
        ],
        "derivation": {
            "lead": "এক প্রান্ত বদ্ধ (নিস্পন্দ) → L = (2n−1)λ/4।",
            "steps": [
                {
                    "title": "তরঙ্গদৈর্ঘ্য",
                    "latex": r"L=(2n-1)\dfrac{\lambda}{4}",
                    "note": "শুধু বিজোড় গুণিতক।",
                },
                {
                    "title": "কম্পাঙ্ক",
                    "latex": r"f_n=(2n-1)\dfrac{v}{4L}",
                    "note": "মূল সুর খোলা পাইপের অর্ধেক (একই L)।",
                },
            ],
            "assumptions": ["প্রান্ত সংশোধন নগণ্য"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "একই L ও v-তে বন্ধ পাইপের f₁ খোলা পাইপের f₁-এর কতগুণ?",
                "answer": r"f_{1,\mathrm{closed}}=v/4L=\tfrac12 f_{1,\mathrm{open}}",
            }
        ],
        "memorize": {
            "trick": "Closed = শুধু বিজোড়; f₁=v/4L।",
            "steps": [],
        },
        "related": ["organ-pipe-open", "beats-frequency", "doppler-effect-general"],
    },
    "banking-of-road": {
        "summary": "ঘর্ষণসহ ব্যাংকিং: tan θ = (v²±μrg)/(rg∓μv²)",
        "latex": r"\tan\theta=\dfrac{v^2\pm\mu r g}{rg\mp\mu v^2}",
        "symbols": [
            {"symbol": "\\theta", "meaning": "ব্যাংকিং কোণ", "unit": "°"},
            {"symbol": "v", "meaning": "গাড়ির বেগ", "unit": "m/s"},
            {"symbol": "r", "meaning": "বাঁকের ব্যাসার্ধ", "unit": "m"},
            {"symbol": "\\mu", "meaning": "ঘর্ষণ গুণাঙ্ক", "unit": "—"},
        ],
        "derivation": {
            "lead": "N ও ঘর্ষণের উপাংশ কেন্দ্রমুখী বল জোগায়।",
            "steps": [
                {
                    "title": "ঘর্ষণহীন (আদর্শ)",
                    "latex": r"\tan\theta=\dfrac{v^2}{rg}",
                    "note": "নির্দিষ্ট ডিজাইন স্পিড।",
                },
                {
                    "title": "ঘর্ষণসহ সীমা",
                    "latex": r"v_{\max}^2=rg\dfrac{\tan\theta+\mu}{1-\mu\tan\theta}",
                    "note": "উপরের চিহ্ন: উঁচু দিকে স্লিপ রোধ।",
                },
            ],
            "assumptions": ["বৃত্তাকার বাঁক; অভিন্ন বেগ"],
        },
        "questions": [
            {
                "examType": "Admission",
                "question": "μ=0, r=100 m, v=20 m/s। θ?",
                "answer": r"\tan\theta=v^2/rg=400/(100\cdot10)=0.4",
            }
        ],
        "memorize": {
            "trick": "আদর্শ: tanθ=v²/rg। ঘর্ষণ থাকলে গতির সীমা বাড়ে।",
            "steps": [],
        },
        "related": ["banking-of-road-ideal", "centripetal-force"],
    },
    "banking-of-road-ideal": {
        "summary": "ঘর্ষণহীন আদর্শ ব্যাংকিং: tan θ = v²/(rg)",
        "latex": r"\tan\theta=\dfrac{v^2}{rg},\quad v=\sqrt{rg\tan\theta}",
        "symbols": [
            {"symbol": "\\theta", "meaning": "ব্যাংকিং কোণ", "unit": "°"},
            {"symbol": "v", "meaning": "ডিজাইন বেগ", "unit": "m/s"},
            {"symbol": "r", "meaning": "ব্যাসার্ধ", "unit": "m"},
            {"symbol": "g", "meaning": "অভিকর্ষজ ত্বরণ", "unit": "m/s²"},
        ],
        "derivation": {
            "lead": "N sinθ = mv²/r, N cosθ = mg → tanθ = v²/(rg)।",
            "steps": [
                {
                    "title": "উপাংশ",
                    "latex": r"N\sin\theta=\dfrac{mv^2}{r},\quad N\cos\theta=mg",
                    "note": "ভাগ করলে ঘর্ষণ ছাড়াই কেন্দ্রমুখী বল।",
                },
                {
                    "title": "সূত্র",
                    "latex": r"\tan\theta=\dfrac{v^2}{rg}",
                    "note": "শুধু এই বেগে স্লিপ হয় না।",
                },
            ],
            "assumptions": ["μ=0; স্থির বৃত্তাকার গতি"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "θ=45°, r=50 m, g=10। নিরাপদ v?",
                "answer": r"v=\sqrt{rg}=\sqrt{500}\\approx22.4\\mathrm{m/s}",
            }
        ],
        "memorize": {
            "trick": "tanθ = v²/rg — আদর্শ ব্যাংকিং।",
            "steps": [],
        },
        "related": ["banking-of-road", "centripetal-force"],
    },
    "gauss-law": {
        "summary": "∮E·dA = Q_enc/ε₀ — প্রতিসম ক্ষেত্রে E বের করার চাবিকাঠি",
        "latex": r"\oint\vec E\cdot d\vec A=\dfrac{Q_{\mathrm{enc}}}{\varepsilon_0}",
        "symbols": [
            {"symbol": "\\vec E", "meaning": "তড়িৎ ক্ষেত্র", "unit": "N/C"},
            {"symbol": "d\\vec A", "meaning": "ক্ষেত্রফল উপাংশ (বাইরের দিকে)", "unit": "m²"},
            {"symbol": "Q_{\\mathrm{enc}}", "meaning": "বন্ধ পৃষ্ঠে ঘেরা চার্জ", "unit": "C"},
            {"symbol": "\\varepsilon_0", "meaning": "শূন্যস্থানের পারমিটিভিটি", "unit": "C²/N·m²"},
        ],
        "derivation": {
            "lead": "ফ্লাক্স শুধু ভিতরের চার্জের উপর নির্ভর করে; প্রতিসম গাউসিয়ান পৃষ্ঠে E বের হয়।",
            "steps": [
                {
                    "title": "সূত্র",
                    "latex": r"\Phi_E=\oint\vec E\cdot d\vec A=\dfrac{Q_{\mathrm{enc}}}{\varepsilon_0}",
                    "note": "বাইরের চার্জ ফ্লাক্সে অবদান রাখে না।",
                },
                {
                    "title": "বিন্দু চার্জ",
                    "latex": r"E\cdot4\pi r^2=\dfrac{q}{\varepsilon_0}\Rightarrow E=\dfrac{kq}{r^2}",
                    "note": "কুলম্বের সূত্রের পুনরুদ্ধার।",
                },
            ],
            "assumptions": ["স্থির তড়িৎ; উপযুক্ত প্রতিসাম্য"],
        },
        "questions": [
            {
                "examType": "Admission",
                "question": "অসীম সমতল σ চার্জ ঘনত্বে E?",
                "answer": r"E=\\sigma/(2\\varepsilon_0)",
            }
        ],
        "memorize": {
            "trick": "ফ্লাক্স = Q_enc/ε₀; প্রতিসাম্য থাকলে E বের করো।",
            "steps": [],
        },
        "related": ["electric-field", "coulombs-law"],
    },
    "critical-angle": {
        "summary": "sin c = n₂/n₁ (n₁>n₂); বায়ুতে sin c = 1/μ",
        "latex": r"\sin c=\dfrac{n_2}{n_1}=\dfrac{1}{\mu}\ (\text{কাচ→বায়ু})",
        "symbols": [
            {"symbol": "c", "meaning": "সমালোচক কোণ", "unit": "°"},
            {"symbol": "n_1, n_2", "meaning": "ঘন ও হালকা মাধ্যমের প্রতিসরাঙ্ক", "unit": "—"},
            {"symbol": "\\mu", "meaning": "ঘন মাধ্যমের আপেক্ষিক প্রতিসরাঙ্ক", "unit": "—"},
        ],
        "derivation": {
            "lead": "i=c হলে r=90° → Snell: n₁ sin c = n₂ · 1।",
            "steps": [
                {
                    "title": "স্নেল",
                    "latex": r"n_1\sin c=n_2\sin90^\circ\Rightarrow\sin c=\dfrac{n_2}{n_1}",
                    "note": "i>c হলে পূর্ণ অভ্যন্তরীণ প্রতিফলন।",
                },
            ],
            "assumptions": ["ঘন → হালকা; সমতল সীমানা"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "μ=√2 হলে কাচ→বায়ুতে c?",
                "answer": r"\sin c=1/\\sqrt{2}\\Rightarrow c=45^\\circ",
            }
        ],
        "memorize": {
            "trick": "sin c = 1/μ (বায়ুতে); i>c → TIR।",
            "steps": [],
        },
        "related": ["total-internal-reflection", "snell-law", "optical-fiber"],
    },
    "apparent-depth": {
        "summary": "আপাত গভীরতা = বাস্তব / μ; সরণ = t(1−1/μ)",
        "latex": r"d_{\mathrm{app}}=\dfrac{d}{\mu},\quad \text{shift}=t\left(1-\dfrac{1}{\mu}\right)",
        "symbols": [
            {"symbol": "d", "meaning": "বাস্তব গভীরতা", "unit": "m"},
            {"symbol": "d_{\\mathrm{app}}", "meaning": "আপাত গভীরতা", "unit": "m"},
            {"symbol": "\\mu", "meaning": "প্রতিসরাঙ্ক", "unit": "—"},
            {"symbol": "t", "meaning": "পুরুত্ব / গভীরতা", "unit": "m"},
        ],
        "derivation": {
            "lead": "লম্বের কাছাকাছি রশ্মিতে প্রতিসরণে গভীরতা কমে দেখায়।",
            "steps": [
                {
                    "title": "আপাত গভীরতা",
                    "latex": r"d_{\mathrm{app}}=\dfrac{d}{\mu}",
                    "note": "পানি μ≈4/3 → আপাত ≈ ¾ বাস্তব।",
                },
                {
                    "title": "উল্লম্ব সরণ",
                    "latex": r"\Delta=t-t/\mu=t(1-1/\mu)",
                    "note": "এটি ল্যাটেরাল শিফট নয় — উল্লম্ব অপটিক্যাল শিফট।",
                },
            ],
            "assumptions": ["প্রায় লম্ব দৃষ্টি; সমতল পৃষ্ঠ"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "৪ m গভীর পুল (μ=4/3) আপাতে কত?",
                "answer": r"d_{\mathrm{app}}=4/(4/3)=3\\mathrm{m}",
            }
        ],
        "memorize": {
            "trick": "আপাত = বাস্তব/μ; সরণ = t(1−1/μ)।",
            "steps": [],
        },
        "related": ["snell-law", "glass-slab-lateral-shift", "critical-angle"],
    },
    "photoelectric-threshold": {
        "summary": "f₀ = φ/h; λ₀ = hc/φ — এর নিচে কোনো নির্গমন নেই",
        "latex": r"f_0=\dfrac{\phi}{h},\quad \lambda_0=\dfrac{hc}{\phi}",
        "symbols": [
            {"symbol": "f_0, \\lambda_0", "meaning": "থ্রেশহোল্ড কম্পাঙ্ক ও তরঙ্গদৈর্ঘ্য", "unit": "Hz, m"},
            {"symbol": "\\phi", "meaning": "কাজফল", "unit": "J বা eV"},
            {"symbol": "h, c", "meaning": "প্ল্যাঙ্ক ধ্রুবক ও আলোর বেগ", "unit": "J·s, m/s"},
        ],
        "derivation": {
            "lead": "K_max=0 সীমায় hf₀=φ।",
            "steps": [
                {
                    "title": "থ্রেশহোল্ড",
                    "latex": r"hf_0=\phi\Rightarrow f_0=\phi/h,\ \lambda_0=hc/\phi",
                    "note": "তিব্রতা যতই বাড়ুক, f<f₀ হলে ইলেকট্রন বেরোয় না।",
                },
            ],
            "assumptions": ["ধাতুর পৃষ্ঠ পরিষ্কার; একক ফোটন শোষণ"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "φ=3.1 eV। λ₀? (hc=1240 eV·nm)",
                "answer": r"\\lambda_0=1240/3.1=400\\mathrm{nm}",
            }
        ],
        "memorize": {
            "trick": "কাট-অফ: f₀=φ/h, λ₀=hc/φ।",
            "steps": [],
        },
        "related": ["einstein-photoelectric", "stopping-potential"],
    },
    "wave-v-f-lambda": {
        "summary": "তরঙ্গের মৌলিক সম্পর্ক: v = fλ = ω/k",
        "latex": r"v=f\lambda=\dfrac{\omega}{k}",
        "symbols": [
            {"symbol": "v", "meaning": "তরঙ্গ বেগ", "unit": "m/s"},
            {"symbol": "f", "meaning": "কম্পাঙ্ক", "unit": "Hz"},
            {"symbol": "\\lambda", "meaning": "তরঙ্গদৈর্ঘ্য", "unit": "m"},
            {"symbol": "\\omega, k", "meaning": "কৌণিক কম্পাঙ্ক ও তরঙ্গ সংখ্যা", "unit": "rad/s, rad/m"},
        ],
        "derivation": {
            "lead": "এক সেকেন্ডে fটি তরঙ্গদৈর্ঘ্য অতিক্রম → দূরত্ব fλ।",
            "steps": [
                {
                    "title": "মৌলিক",
                    "latex": r"v=f\lambda",
                    "note": "সব প্রগতিশীল তরঙ্গে প্রযোজ্য।",
                },
                {
                    "title": "কোণীয় রূপ",
                    "latex": r"\omega=2\pi f,\ k=2\pi/\lambda\Rightarrow v=\omega/k",
                    "note": "দশা বেগ।",
                },
            ],
            "assumptions": ["অবিচ্ছिন্ন মাধ্যম; একবর্ণী তরঙ্গ"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "f=500 Hz, λ=0.68 m। v?",
                "answer": r"v=500\\times0.68=340\\mathrm{m/s}",
            }
        ],
        "memorize": {
            "trick": "v=fλ — সব তরঙ্গের বেসিক।",
            "steps": [],
        },
        "related": ["wave-speed-string", "transverse-wave-equation"],
    },
    "wave-speed-string": {
        "summary": "দড়িতে তরঙ্গবেগ v = √(T/μ)",
        "latex": r"v=\sqrt{\dfrac{T}{\mu}},\quad \mu=\dfrac{m}{L}",
        "symbols": [
            {"symbol": "T", "meaning": "দড়ির টান", "unit": "N"},
            {"symbol": "\\mu", "meaning": "একক দৈর্ঘ্যের ভর", "unit": "kg/m"},
            {"symbol": "v", "meaning": "তরঙ্গবেগ", "unit": "m/s"},
        ],
        "derivation": {
            "lead": "ছোট উপাদানের নেট বল থেকে তরঙ্গ সমীকরণ → v² = T/μ।",
            "steps": [
                {
                    "title": "সূত্র",
                    "latex": r"v=\sqrt{T/\mu}",
                    "note": "টান বাড়লে দ্রুত; ভারী দড়ি ধীর।",
                },
            ],
            "assumptions": ["আদর্শ নমনীয় দড়ি; ক্ষুদ্র প্রশস্ততা"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "T=100 N, μ=0.01 kg/m। v?",
                "answer": r"v=\\sqrt{100/0.01}=100\\mathrm{m/s}",
            }
        ],
        "memorize": {
            "trick": "v=√(T/μ) — টান↑ বেগ↑, μ↑ বেগ↓।",
            "steps": [],
        },
        "related": ["wave-v-f-lambda", "transverse-wave-equation"],
    },
    "activity-mean-life": {
        "summary": "A = λN = A₀ e^(−λt); τ = 1/λ = T½/ln2",
        "latex": r"A=\lambda N=A_0e^{-\lambda t},\quad \tau=\dfrac{1}{\lambda}=\dfrac{T_{1/2}}{\ln 2}",
        "symbols": [
            {"symbol": "A", "meaning": "সক্রিয়তা (ক্ষয়/সেকেন্ড)", "unit": "Bq"},
            {"symbol": "\\lambda", "meaning": "ক্ষয় ধ্রুবক", "unit": "s⁻¹"},
            {"symbol": "\\tau", "meaning": "গড় আয়ু", "unit": "s"},
            {"symbol": "T_{1/2}", "meaning": "অর্ধায়ু", "unit": "s"},
        ],
        "derivation": {
            "lead": "A = −dN/dt = λN; গড় আয়ু τ = 1/λ > T½।",
            "steps": [
                {
                    "title": "সক্রিয়তা",
                    "latex": r"A=\lambda N=A_0e^{-\lambda t}",
                    "note": "N ও A একই হারে ক্ষয় হয়।",
                },
                {
                    "title": "গড় আয়ু",
                    "latex": r"\tau=1/\lambda=T_{1/2}/\ln2\approx1.44\,T_{1/2}",
                    "note": "τ > T½।",
                },
            ],
            "assumptions": ["একক ক্ষয় মোড; বৃহৎ N"],
        },
        "questions": [
            {
                "examType": "Admission",
                "question": "T½=5 দিন। τ কত?",
                "answer": r"\\tau=5/\\ln2\\approx7.21\\ \\mathrm{day}",
            }
        ],
        "memorize": {
            "trick": "A=λN; τ=1/λ≈1.44 T½।",
            "steps": [],
        },
        "related": ["radioactive-decay", "half-life-chem"],
    },
    "bohr-energy-levels": {
        "summary": "E_n = −13.6/n² eV (হাইড্রোজেন); ΔE = hf",
        "latex": r"E_n=-\dfrac{13.6}{n^2}\,\mathrm{eV},\quad hf=E_i-E_f",
        "symbols": [
            {"symbol": "n", "meaning": "প্রধান কোয়ান্টাম সংখ্যা", "unit": "—"},
            {"symbol": "E_n", "meaning": "n-তম কক্ষের শক্তি", "unit": "eV"},
            {"symbol": "h f", "meaning": "নির্গত/শোষিত ফোটন শক্তি", "unit": "eV"},
        ],
        "derivation": {
            "lead": "কোয়ান্টাইজড কক্ষে মোট শক্তি ঋণাত্মক; n→∞ এ E→0 (আয়নীকরণ)।",
            "steps": [
                {
                    "title": "শক্তি স্তর",
                    "latex": r"E_n=-\dfrac{13.6\,Z^2}{n^2}\,\mathrm{eV}",
                    "note": "হাইড্রোজেনে Z=1।",
                },
                {
                    "title": "বর্ণালি",
                    "latex": r"\dfrac{1}{\lambda}=R\left(\dfrac{1}{n_f^2}-\dfrac{1}{n_i^2}\right)",
                    "note": "রিডবার্গ সূত্রের সাথে মিল।",
                },
            ],
            "assumptions": ["এক-ইলেকট্রন পরমাণু; বোর মডেল"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "n=2 → n=1 এ নির্গত শক্তি?",
                "answer": r"\\Delta E=13.6(1-1/4)=10.2\\mathrm{eV}",
            }
        ],
        "memorize": {
            "trick": "E_n=−13.6/n² eV; আয়নীকরণ = 13.6 eV।",
            "steps": [],
        },
        "related": ["bohr-frequency-condition", "bohr-radius-hydrogen"],
    },
    "cells-series-parallel": {
        "summary": "সিরিজ: E_eq=nE, r_eq=nr; সমান্তরাল: E_eq=E, r_eq=r/m",
        "latex": r"\text{series: }E_{\mathrm{eq}}=nE,\ r_{\mathrm{eq}}=nr;\quad\text{parallel: }E_{\mathrm{eq}}=E,\ r_{\mathrm{eq}}=r/m",
        "symbols": [
            {"symbol": "n", "meaning": "সিরিজ কোষ সংখ্যা", "unit": "—"},
            {"symbol": "m", "meaning": "সমান্তরাল শাখা", "unit": "—"},
            {"symbol": "E, r", "meaning": "এক কোষের emf ও অভ্যন্তরীণ রোধ", "unit": "V, Ω"},
        ],
        "derivation": {
            "lead": "সিরিজে emf ও r যোগ; সমান্তরালে emf একই, r ভাগ।",
            "steps": [
                {
                    "title": "সিরিজ",
                    "latex": r"E_{\mathrm{eq}}=nE,\quad r_{\mathrm{eq}}=nr",
                    "note": "বড় ভোল্টেজ চাইলে সিরিজ।",
                },
                {
                    "title": "সমান্তরাল",
                    "latex": r"E_{\mathrm{eq}}=E,\quad r_{\mathrm{eq}}=r/m",
                    "note": "বড় প্রবাহ / কম অভ্যন্তরীণ রোধ।",
                },
            ],
            "assumptions": ["অভিন্ন কোষ"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "৪টি কোষ সিরিজে, প্রতিটি E=1.5 V, r=0.5 Ω। E_eq, r_eq?",
                "answer": r"E_{\mathrm{eq}}=6\\mathrm{V},\ r_{\mathrm{eq}}=2\\Omega",
            }
        ],
        "memorize": {
            "trick": "Series: যোগ; Parallel: E এক, r ভাগ।",
            "steps": [],
        },
        "related": ["group-cells-max-power", "ohms-law"],
    },
    "vertical-circle-min-speed": {
        "summary": "উপরে ন্যূনতম v = √(gR); নিচে √(5gR)",
        "latex": r"v_{\mathrm{top}}=\sqrt{gR},\quad v_{\mathrm{bottom}}=\sqrt{5gR}",
        "symbols": [
            {"symbol": "R", "meaning": "বৃত্তের ব্যাসার্ধ", "unit": "m"},
            {"symbol": "v_{\\mathrm{top}}", "meaning": "উপরের ন্যূনতম বেগ", "unit": "m/s"},
            {"symbol": "v_{\\mathrm{bottom}}", "meaning": "নিচের সংশ্লিষ্ট বেগ", "unit": "m/s"},
        ],
        "derivation": {
            "lead": "উপরে N+mg = mv²/R; N≥0 → v²≥gR। শক্তি সংরক্ষণে নিচের বেগ।",
            "steps": [
                {
                    "title": "উপর",
                    "latex": r"v_t=\sqrt{gR}",
                    "note": "ঠিক সীমায় N=0।",
                },
                {
                    "title": "নিচ",
                    "latex": r"\tfrac12mv_b^2=\tfrac12mv_t^2+mg(2R)\Rightarrow v_b=\sqrt{5gR}",
                    "note": "উচ্চতা পার্থক্য 2R।",
                },
            ],
            "assumptions": ["দড়ি/ট্র্যাক; ঘর্ষণহীন; কণা মডেল"],
        },
        "questions": [
            {
                "examType": "Admission",
                "question": "R=2.5 m, g=10। উপরে ন্যূনতম v?",
                "answer": r"v=\\sqrt{25}=5\\mathrm{m/s}",
            }
        ],
        "memorize": {
            "trick": "Top √(gR), Bottom √(5gR)।",
            "steps": [],
        },
        "related": ["vertical-circle-tension", "centripetal-force"],
    },
    "lens-formula": {
        "summary": "পাতলা লেন্স: 1/v − 1/u = 1/f (কার্টেসিয়ান)",
        "latex": r"\dfrac{1}{v}-\dfrac{1}{u}=\dfrac{1}{f}",
        "symbols": [
            {"symbol": "u", "meaning": "বস্তুর দূরত্ব (চিহ্নসহ)", "unit": "m"},
            {"symbol": "v", "meaning": "প্রতিবিম্বের দূরত্ব", "unit": "m"},
            {"symbol": "f", "meaning": "ফোকাস দূরত্ব (+ উত্তল)", "unit": "m"},
        ],
        "derivation": {
            "lead": "দর্পণের 1/v+1/u=1/f থেকে আলাদা — লেন্সে বিয়োগ।",
            "steps": [
                {
                    "title": "সূত্র",
                    "latex": r"\dfrac{1}{v}-\dfrac{1}{u}=\dfrac{1}{f}",
                    "note": "উত্তল f>0; অবতল f<0 (কার্টেসিয়ান)।",
                },
            ],
            "assumptions": ["পাতলা লেন্স; প্যারাক্সিয়াল"],
        },
        "questions": [
            {
                "examType": "HSC",
                "question": "f=20 cm, u=−30 cm। v?",
                "answer": r"1/v=1/f+1/u=1/20-1/30=1/60\\Rightarrow v=60\\mathrm{cm}",
            }
        ],
        "memorize": {
            "trick": "লেন্স: 1/v − 1/u = 1/f। দর্পণে যোগ।",
            "steps": [],
        },
        "related": ["lens-makers-formula", "magnification-mirror-lens", "mirror-formula"],
    },
}

for fid, patch in UPGRADES.items():
    path = find_id(fid)
    if not path:
        print(f"  skip missing {fid}")
        continue
    data = load(path)
    data.update(patch)
    # sanitize related to existing ids
    all_ids = {load(p)["id"] for p in all_formula_paths()}
    # include just-deleted? already deleted
    related = []
    for rid in data.get("related") or []:
        if rid in all_ids and rid != data["id"] and rid not in related:
            related.append(rid)
    data["related"] = related
    save(path, data)
    print(f"  upgraded {fid}")

# Fix radioactive-decay related to prefer physics companions (keep chem cross-links OK)
rd = find_id("radioactive-decay")
if rd:
    d = load(rd)
    prefer = [
        "activity-mean-life",
        "mass-energy-photoelectric",
        "de-broglie-wavelength",
        "half-life-chem",
        "radioactive-decay-law-chem",
    ]
    all_ids = {load(p)["id"] for p in all_formula_paths()}
    d["related"] = [x for x in prefer if x in all_ids]
    save(rd, d)
    print("  retuned radioactive-decay related")

# electric-dipole: keep chem dipole-moment but add physics companions
ed = find_id("electric-dipole")
if ed:
    d = load(ed)
    all_ids = {load(p)["id"] for p in all_formula_paths()}
    prefer = ["coulombs-law", "electric-field", "electric-potential", "dipole-moment", "gauss-law"]
    d["related"] = [x for x in prefer if x in all_ids]
    save(ed, d)
    print("  retuned electric-dipole related")

# uncertainty: add physics peers alongside chem quantum-numbers
up = find_id("uncertainty-principle")
if up:
    d = load(up)
    all_ids = {load(p)["id"] for p in all_formula_paths()}
    prefer = ["de-broglie-wavelength", "bohr-radius-hydrogen", "bohr-energy-levels", "quantum-numbers"]
    d["related"] = [x for x in prefer if x in all_ids]
    save(up, d)
    print("  retuned uncertainty-principle related")

print("Done.")
