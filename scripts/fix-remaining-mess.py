#!/usr/bin/env python3
"""
Fix remaining messy content: junk symbols, apply-latex derivations,
generic assumptions, thin related links.

Usage:
  python3 scripts/fix-remaining-mess.py --all
  python3 scripts/fix-remaining-mess.py --importance 3
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "subjects"

DROP_KEYS = {
    "sum",
    "prod",
    "int",
    "oint",
    "partial",
    "nabla",
    "rightarrow",
    "leftarrow",
    "leftrightarrow",
    "Rightarrow",
    "Leftarrow",
    "Leftrightarrow",
    "xrightarrow",
    "rightleftharpoons",
    "to",
    "mapsto",
    "cdot",
    "times",
    "div",
    "pm",
    "mp",
    "approx",
    "equiv",
    "propto",
    "infty",
    "cdots",
    "ldots",
    "main:",
    "text",
    "key",
    "circ",
    "or",
    "and",
    "quad",
    "qquad",
    "left",
    "right",
    "big",
    "Big",
    "mathrm",
    "operatorname",
    "displaystyle",
    "textstyle",
}

# Single-letter junk only when meaning is stubby
DROP_IF_STUB = {"o", "O"}

APPLY_LATEX_RE = re.compile(r"রাশি চিহ্নিত করো")
GENERIC_ASSUM_RE = re.compile(
    r"(SI একক ব্যবহার করো|প্রমিত/প্রদত্ত তাপমাত্রা-চাপ ধরো|প্রদত্ত শর্ত ও ডোমেইন মেনে চলো|প্রতিক্রিয়া/গঠন প্রশ্নে দেওয়া তথ্য অনুসরণ করো|HSC/ভর্তি পর্যায়ে প্রচলিত আদর্শ শর্ত)"
)

PHYS_MAP = {
    "F": ("বল", "N"),
    "f": ("কম্পাঙ্ক / ঘর্ষণ", "Hz বা N"),
    "m": ("ভর", "kg"),
    "M": ("ভর", "kg"),
    "a": ("ত্বরণ", "m/s²"),
    "v": ("বেগ", "m/s"),
    "u": ("আদি বেগ", "m/s"),
    "s": ("সরণ", "m"),
    "t": ("সময়", "s"),
    "T": ("পর্যায়কাল / তাপমাত্রা", "s বা K"),
    "P": ("চাপ / ক্ষমতা", "Pa বা W"),
    "p": ("ভরবেগ", "kg·m/s"),
    "E": ("শক্তি / তড়িৎক্ষেত্র", "J বা N/C"),
    "U": ("বিভব শক্তি", "J"),
    "K": ("গতিশক্তি", "J"),
    "W": ("কাজ", "J"),
    "Q": ("তাপ / চার্জ", "J বা C"),
    "q": ("চার্জ", "C"),
    "I": ("তড়িৎ প্রবাহ", "A"),
    "V": ("বিভব", "V"),
    "R": ("রোধ / ব্যাসার্ধ", "Ω বা m"),
    "r": ("ব্যাসার্ধ", "m"),
    "L": ("দৈর্ঘ্য / আবেশ", "m বা H"),
    "C": ("ধারকত্ব", "F"),
    "B": ("চৌম্বক ক্ষেত্র", "T"),
    "H": ("চৌম্বক ক্ষেত্র প্রাবল্য", "A/m"),
    "g": ("অভিকর্ষজ ত্বরণ", "m/s²"),
    "h": ("উচ্চতা / প্ল্যাঙ্ক", "m বা J·s"),
    "omega": ("কৌণিক বেগ", "rad/s"),
    "theta": ("কোণ", "rad"),
    "lambda": ("তরঙ্গদৈর্ঘ্য", "m"),
    "mu": ("প্রতিসরাঙ্ক / চৌম্বক ভ্রামক", "—"),
    "rho": ("ঘনত্ব", "kg/m³"),
    "alpha": ("কোণ / প্রসারণ", "—"),
    "eta": ("সান্দ্রতা / দক্ষতা", "Pa·s"),
    "c": ("আলোর বেগ", "m/s"),
    "k": ("বল ধ্রুবক", "N/m"),
    "A": ("ক্ষেত্রফল / বিস্তার", "m²"),
    "G": ("মহাকর্ষ ধ্রুবক", "N·m²/kg²"),
    "n": ("প্রতিসরাঙ্ক", "—"),
    "N": ("পাক সংখ্যা", "—"),
    "phi": ("ফ্লাক্স / দশা", "Wb"),
    "Delta": ("পরিবর্তন", "—"),
    "e": ("ইলেকট্রন চার্জ", "C"),
    "CN": ("সমন্বয় সংখ্যা", "—"),
    "S": ("এনট্রপি / পৃষ্ঠটান", "J/K বা N/m"),
}

CHEM_MAP = {
    "H": ("এনথ্যালপি", "J বা kJ"),
    "S": ("এনট্রপি", "J/K"),
    "G": ("গিবস মুক্ত শক্তি", "J"),
    "E": ("বন্ধন শক্তি / কোশ বিভব", "J বা V"),
    "T": ("পরম তাপমাত্রা", "K"),
    "P": ("চাপ", "Pa বা atm"),
    "V": ("আয়তন", "L বা m³"),
    "n": ("মোল সংখ্যা", "mol"),
    "N": ("কণা সংখ্যা", "—"),
    "R": ("গ্যাস ধ্রুবক", "J/(mol·K)"),
    "K": ("সাম্য / হার ধ্রুবক", "—"),
    "k": ("হার ধ্রুবক", "—"),
    "c": ("ঘনমাত্রা", "mol/L"),
    "C": ("ঘনমাত্রা", "mol/L"),
    "Q": ("বিক্রিয়া ভাগফল", "—"),
    "q": ("তাপ", "J"),
    "m": ("ভর", "g"),
    "M": ("মোলার ভর", "g/mol"),
    "t": ("সময়", "s"),
    "A": ("প্রাক-এক্সপোনেনশিয়াল", "—"),
    "Ea": ("সক্রিয়ন শক্তি", "J/mol"),
    "pH": ("pH", "—"),
    "Ka": ("অ্যাসিড বিয়োজন ধ্রুবক", "—"),
    "Kb": ("বেস বিয়োজন ধ্রুবক", "—"),
    "Kw": ("পানির আয়নিক গুণফল", "—"),
    "Ksp": ("দ্রাব্যতা গুণফল", "—"),
    "Kp": ("চাপ সাম্য ধ্রুবক", "—"),
    "Kc": ("ঘনমাত্রা সাম্য ধ্রুবক", "—"),
    "mu": ("দ্বিমেরু ভ্রামক", "D"),
    "Delta": ("পরিবর্তন", "—"),
    "alpha": ("বিয়োজন মাত্রা", "—"),
    "beta": ("বাফার ক্ষমতা", "—"),
    "I": ("আয়নিক শক্তি", "—"),
    "F": ("ফ্যারাডে ধ্রুবক", "C/mol"),
    "Z": ("পারমাণবিক সংখ্যা", "—"),
    "CN": ("সমন্বয় সংখ্যা", "—"),
    "[A]": ("ঘনমাত্রা A", "mol/L"),
    "[B]": ("ঘনমাত্রা B", "mol/L"),
    "[C]": ("ঘনমাত্রা C", "mol/L"),
    "[D]": ("ঘনমাত্রা D", "mol/L"),
    "[H+]": ("হাইড্রোজেন আয়ন ঘনমাত্রা", "mol/L"),
    "[OH-]": ("হাইড্রক্সাইড ঘনমাত্রা", "mol/L"),
}

MATH_MAP = {
    "x": ("স্বাধীন চলক", "—"),
    "y": ("নির্ভর চলক", "—"),
    "z": ("চলক", "—"),
    "a": ("সহগ / ধ্রুবক", "—"),
    "b": ("সহগ / ধ্রুবক", "—"),
    "c": ("সহগ / ধ্রুবক", "—"),
    "n": ("পদসংখ্যা / ঘাত", "—"),
    "m": ("সারি / ঘাত", "—"),
    "r": ("অনুপাত / ব্যাসার্ধ", "—"),
    "A": ("ম্যাট্রিক্স / ক্ষেত্রফল", "—"),
    "B": ("ম্যাট্রিক্স", "—"),
    "I": ("একক ম্যাট্রিক্স", "—"),
    "P": ("সম্ভাব্যতা", "—"),
    "f": ("ফাংশন", "—"),
    "g": ("ফাংশন", "—"),
    "t": ("প্যারামিটার", "—"),
    "theta": ("কোণ", "rad"),
    "phi": ("কোণ", "rad"),
    "Delta": ("পরিবর্তন", "—"),
    "S": ("বৃত্ত সমীকরণ / সমষ্টি", "—"),
    "S1": ("প্রথম বৃত্ত", "—"),
    "S2": ("দ্বিতীয় বৃত্ত", "—"),
    "lim": ("সীমা", "—"),
}

CHAPTER_ASSUMPTIONS: dict[str, list[str]] = {
    "measurement": ["SI একক ও মাত্রিক সামঞ্জস্য বজায় রাখো"],
    "vector": ["ভেক্টর যোগ জ্যামিতিক/বিশ্লেষণিক নিয়মে"],
    "dynamics": ["ধ্রুব ভর; বাহ্যিক বল নেট হিসাবে নাও"],
    "newtonian-mechanics": ["ধ্রুব ভর; অজড় কাঠামোয় নিউটনের সূত্র"],
    "work-energy": ["কাজ-শক্তি উপপাদ্য যান্ত্রিক শক্তির জন্য"],
    "circular-motion": ["বৃত্তাকার পথে |v| ধ্রুব ধরলে কেন্দ্রমুখী ত্বরণ v²/r"],
    "gravitation": ["বিন্দু ভর / গোলাকার প্রতিসম ভর বণ্টন"],
    "properties-of-matter": ["ক্ষুদ্র বিকৃতি; হুকের সূত্রের সীমায়"],
    "thermodynamics": ["আদর্শ গ্যাস / প্রত্যাবর্তী ধাপ যেখানে প্রযোজ্য"],
    "waves": ["ছোট বিস্তার; রৈখিক মাধ্যম"],
    "optics": ["প্যারাক্সিয়াল রশ্মি (ছোট কোণ)"],
    "electrostatics": ["বিন্দু চার্জ / স্থির অবস্থা"],
    "current-electricity": ["ধ্রুব তাপমাত্রায় ওহমীয় রোধ"],
    "magnetism": ["স্থির প্রবাহ / স্থির ক্ষেত্র আনুমানিক"],
    "emi": ["ফ্যারাডের সূত্র; ফ্লাক্সের চিহ্ন সাবধানে"],
    "ac": ["সাইনসয়েডাল স্থিতিশীল অবস্থা"],
    "modern-physics": ["প্রদত্ত কোয়ান্টাম/আপেক্ষিকতা শর্ত"],
    "chemical-bonding": ["লুইস/VSEPR আনুমানিক; ব্যতিক্রম আলাদা"],
    "chemical-equilibrium": ["ধ্রুব T; আদর্শ আচরণ আনুমানিক"],
    "electrochemistry": ["প্রমিত/প্রদত্ত তাপমাত্রা; আদর্শ দ্রবণ আনুমানিক"],
    "colligative-properties": ["অত্যধিক লঘু দ্রবণ"],
    "coordination-chemistry": ["ওয়ার্নার/CFSE আনুমানিক মডেল"],
    "organic-chem": ["প্রদত্ত কাঠামো ও স্টেরিও রসায়ন"],
    "nuclear-chemistry": ["প্রথম ক্রম ক্ষয় ধরো যেখানে প্রযোজ্য"],
    "solid-state-chemistry": ["আদর্শ স্ফটিক জালি আনুমানিক"],
    "surface-chemistry": ["প্রদত্ত তাপমাত্রা-চাপে"],
    "industrial-chemistry": ["শিল্প প্রক্রিয়ার প্রধান ধাপ"],
    "environmental-chemistry": ["বায়ুমণ্ডলীয় প্রমিত শর্ত আনুমানিক"],
    "qualitative-chem": ["প্রদত্ত পরীক্ষার শর্ত"],
    "quantitative-chem": ["মোল ধারণা ও ভর সংরক্ষণ"],
    "matrix-determinant": ["বর্গ ম্যাট্রিক্স যেখানে নির্ণায়ক লাগে"],
    "calculus": ["ডোমেইনে ফাংশন অবকলন/যোগজযোগ্য"],
    "conic": ["মানক অবস্থানে কনিক"],
    "straight-line": ["দ্বিতীয় মাত্রার কার্তেসীয় তল"],
    "circle": ["কার্তেসীয় তলে বৃত্ত"],
    "trigonometry": ["কোণের প্রদত্ত একক (ডিগ্রি/রেডিয়ান) মেনে চলো"],
    "probability": ["সমসম্ভাব্য নমুনা জগৎ যেখানে বলা"],
    "linear-programming": ["রৈখিক সীমাবদ্ধতা; উত্তল সম্ভাব্য ক্ষেত্র"],
    "vector-3d": ["ত্রিমাত্রিক কার্তেসীয় স্থানাঙ্ক"],
    "differential-equation": ["প্রদত্ত আদি মান / শর্ত"],
    "statics": ["স্থির সাম্য; ধ্রুব বল"],
}


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def subject_of(path: Path) -> str:
    return path.relative_to(ROOT).parts[0]


def clean_key(symbol: str) -> str:
    s = symbol.strip()
    s = re.sub(r"^\\", "", s)
    # keep bracket concentrations like [A]
    if s.startswith("[") and s.endswith("]"):
        return s
    s = re.sub(r"[_^].*$", "", s)
    s = re.sub(r"[{}]", "", s)
    return s


def is_junk_symbol(sym: str, meaning: str) -> bool:
    raw = sym.strip()
    if not raw:
        return True
    if "text{key}" in raw or raw in (r"\text{key}", "key"):
        return True
    if " " in raw and len(raw) > 12 and not raw.startswith("["):
        if re.search(r"(order|open-chain|cyclic|main:)", raw, re.I):
            return True
    key = clean_key(raw)
    if key in DROP_KEYS:
        return True
    if key in DROP_IF_STUB and ("সূত্রের রাশি" in meaning or len(meaning) < 4):
        return True
    return False


def map_meaning(sym: str, subject: str) -> tuple[str, str] | None:
    key = clean_key(sym)
    table = PHYS_MAP if subject == "physics" else CHEM_MAP if subject == "chemistry" else MATH_MAP
    if key in table:
        return table[key]
    # Delta X forms
    if key.startswith("Delta") and len(key) > 5:
        rest = key[5:]
        if rest in table:
            base_m, base_u = table[rest]
            return (f"{base_m} এর পরিবর্তন", base_u)
    low = key.lower()
    for name, pair in table.items():
        if name.lower() == low:
            return pair
    if key.startswith("[") and key.endswith("]"):
        inner = key[1:-1]
        return (f"{inner} এর ঘনমাত্রা", "mol/L")
    if re.match(r"^[A-Z][a-z]?(\d|_)", key) or "mathrm" in sym:
        return (f"{sym} (রাসায়নিক রাশি)", "—") if subject == "chemistry" else (sym, "—")
    if re.match(r"^[A-Za-z][A-Za-z0-9]*$", key) and len(key) <= 6:
        return (f"{key}", "—")
    return None


def extract_symbols_from_latex(latex: str, subject: str) -> list[dict]:
    """Pull a few plausible symbols from latex when list was emptied."""
    found: list[str] = []
    for m in re.finditer(r"\\([A-Za-z]+)", latex):
        cmd = m.group(1)
        if cmd in DROP_KEYS or cmd in {
            "frac",
            "dfrac",
            "sqrt",
            "left",
            "right",
            "text",
            "mathrm",
            "mathbf",
            "operatorname",
            "over",
            "overline",
            "underline",
            "hat",
            "vec",
            "dot",
            "ddot",
            "bar",
            "tilde",
            "widehat",
            "overrightarrow",
            "begin",
            "end",
            "ce",
        }:
            continue
        if cmd not in found:
            found.append(cmd)
    for m in re.finditer(r"(?<![A-Za-z\\])([A-Za-z])(?![A-Za-z])", latex):
        ch = m.group(1)
        if ch.lower() in {"e"} and subject == "math":
            continue
        if ch not in found and ch not in DROP_IF_STUB:
            found.append(ch)
    for m in re.finditer(r"\[[A-Za-z0-9+-]+\]", latex):
        tok = m.group(0)
        if tok not in found:
            found.append(tok)

    out = []
    for sym in found[:4]:
        mapped = map_meaning(sym, subject)
        if not mapped:
            continue
        meaning, unit = mapped
        out.append({"symbol": sym if sym.startswith("[") else (sym if len(sym) == 1 else f"\\{sym}" if sym.isalpha() and sym.islower() is False and len(sym) > 1 else sym), "meaning": meaning, "unit": unit})
    # Normalize symbol display
    cleaned = []
    for s in out:
        sym = s["symbol"]
        if re.match(r"^[A-Za-z]+$", sym) and len(sym) > 1 and sym[0].islower():
            sym = "\\" + sym
        cleaned.append({"symbol": sym, "meaning": s["meaning"], "unit": s["unit"]})
    return cleaned


def fix_stub_special(data: dict) -> bool:
    """Hand-fix the 3 known stubSymbols audit failures."""
    fid = data.get("id")
    if fid == "coordination-number":
        data["symbols"] = [
            {"symbol": "CN", "meaning": "সমন্বয় সংখ্যা (ligands সংখ্যা)", "unit": "—"},
            {"symbol": r"\mathrm{M}", "meaning": "কেন্দ্রীয় ধাতু আয়ন", "unit": "—"},
        ]
        return True
    if fid == "common-chord-circles":
        data["symbols"] = [
            {"symbol": "S_1", "meaning": "প্রথম বৃত্তের সমীকরণ", "unit": "—"},
            {"symbol": "S_2", "meaning": "দ্বিতীয় বৃত্তের সমীকরণ", "unit": "—"},
            {"symbol": "S_1-S_2", "meaning": "সাধারণ জ্যা এর সমীকরণ", "unit": "—"},
        ]
        return True
    if fid == "integral-trig-basic":
        data["symbols"] = [
            {"symbol": "x", "meaning": "কোণ / চলক", "unit": "rad"},
            {"symbol": r"\sin x", "meaning": "সাইন ফাংশন", "unit": "—"},
            {"symbol": r"\cos x", "meaning": "কসাইন ফাংশন", "unit": "—"},
        ]
        return True
    return False


def polish_symbols(data: dict, subject: str) -> bool:
    if fix_stub_special(data):
        return True
    syms = list(data.get("symbols") or [])
    changed = False
    new = []
    for s in syms:
        sym = str(s.get("symbol") or "").strip()
        meaning = str(s.get("meaning") or "")
        unit = str(s.get("unit") or "—")
        if is_junk_symbol(sym, meaning):
            changed = True
            continue
        mapped = map_meaning(sym, subject)
        if "সূত্রের রাশি" in meaning or len(meaning) < 3:
            if mapped:
                meaning, u = mapped
                if unit in ("—", "", "সূত্রানুযায়ী", "T") and u:
                    unit = u
                changed = True
            else:
                # drop unmappable stubs
                changed = True
                continue
        entry = {"symbol": sym, "meaning": meaning, "unit": unit}
        if "value" in s and s["value"] is not None:
            entry["value"] = s["value"]
        new.append(entry)

    if not new:
        extracted = extract_symbols_from_latex(data.get("latex") or "", subject)
        if extracted:
            new = extracted
            changed = True
        else:
            title = data.get("titleBn") or data.get("title") or data["id"]
            # Prefer a real letter from titleBn latin latex rather than text{key}
            latex = data.get("latex") or ""
            extracted = extract_symbols_from_latex(latex, subject)
            if extracted:
                new = extracted
            else:
                new = [
                    {
                        "symbol": "n" if subject != "physics" else "F",
                        "meaning": f"{title} এর প্রধান রাশি",
                        "unit": "—",
                    }
                ]
            changed = True

    # Dedup by clean key
    seen = set()
    deduped = []
    for s in new:
        k = clean_key(str(s["symbol"]))
        if k in seen:
            changed = True
            continue
        seen.add(k)
        deduped.append(s)

    if changed or deduped != syms:
        data["symbols"] = deduped
        return True
    return False


def assumptions_for(chapter: str, subject: str, title: str) -> list[str]:
    if chapter in CHAPTER_ASSUMPTIONS:
        return list(CHAPTER_ASSUMPTIONS[chapter])
    # fuzzy chapter id contains
    for key, vals in CHAPTER_ASSUMPTIONS.items():
        if key in chapter or chapter in key:
            return list(vals)
    if subject == "physics":
        return [f"{title}: প্রদত্ত শর্ত ও SI একক মেনে চলো"]
    if subject == "chemistry":
        return [f"{title}: প্রদত্ত তাপমাত্রা/চাপ ও স্টকিওমেট্রি মেনে চলো"]
    return [f"{title}: প্রদত্ত ডোমেইন ও শর্ত মেনে চলো"]


def polish_derivation(data: dict, subject: str) -> bool:
    der = dict(data.get("derivation") or {})
    steps = list(der.get("steps") or [])
    latex = (data.get("latex") or "").strip()
    title = data.get("titleBn") or data.get("title") or data["id"]
    trick = ((data.get("memorize") or {}).get("trick") or "").strip()
    summary = (data.get("summary") or "").strip()
    chapter = data.get("chapter") or ""
    changed = False

    needs_step2 = False
    if len(steps) >= 2 and APPLY_LATEX_RE.search(str(steps[1].get("latex") or "")):
        needs_step2 = True
    if len(steps) >= 2 and (steps[0].get("latex") or "") == (steps[1].get("latex") or ""):
        needs_step2 = True

    if needs_step2 or len(steps) < 2:
        lead = (der.get("lead") or "").strip()
        if not lead or "রাশি ও একক ঠিক" in lead:
            lead = f"{title}: প্রদত্ত মান বসিয়ে সম্পর্ক প্রয়োগ করো।"
        note1 = summary or f"{title} এর মূল সম্পর্ক।"
        note2 = trick or f"{title} থেকে চাহিদামতো রাশি নির্ণয় করো।"
        # Distinct step-2 latex tied to the formula title (valid KaTeX)
        safe_title = re.sub(r"[{}\\_^$&#%]", "", title)
        safe_title = re.sub(r"\s+", " ", safe_title).strip()[:36] or "সূত্র"
        step2_latex = rf"\text{{{safe_title}: প্রয়োগ}} \rightarrow \text{{ফলাফল}}"
        if step2_latex == latex:
            step2_latex = r"\text{মান বসাও} \rightarrow \text{ফলাফল যাচাই}"
        der["lead"] = lead
        der["steps"] = [
            {
                "title": "মূল সূত্র",
                "latex": latex or rf"\text{{{safe_title}}}",
                "note": note1[:160],
            },
            {
                "title": "প্রয়োগ",
                "latex": step2_latex,
                "note": note2[:160],
            },
        ]
        changed = True
        steps = der["steps"]

    assum = der.get("assumptions")
    if not isinstance(assum, list) or not assum or any(GENERIC_ASSUM_RE.search(str(a)) for a in assum):
        der["assumptions"] = assumptions_for(chapter, subject, title)
        changed = True

    if changed:
        data["derivation"] = der
    return changed


def polish_related(data: dict, by_chapter: dict[str, list[dict]]) -> bool:
    related = list(data.get("related") or [])
    # drop self / invalid later by IDs present
    chapter = data.get("chapter")
    fid = data.get("id")
    siblings = by_chapter.get(chapter or "", [])
    valid_ids = {x["id"] for x in siblings}
    related = [r for r in related if r in valid_ids and r != fid]
    if len(related) >= 2:
        if related != (data.get("related") or []):
            data["related"] = related[:5]
            return True
        return False

    # pick nearest by order
    me = next((x for x in siblings if x["id"] == fid), None)
    if not me:
        return False
    ordered = sorted(siblings, key=lambda x: abs((x.get("order") or 0) - (me.get("order") or 0)))
    picks = []
    for s in ordered:
        if s["id"] == fid:
            continue
        picks.append(s["id"])
        if len(picks) >= 3:
            break
    # merge existing first
    merged = []
    for r in related + picks:
        if r not in merged and r != fid:
            merged.append(r)
    if len(merged) >= 2:
        data["related"] = merged[:4]
        return True
    if merged:
        data["related"] = merged
        return True
    return False


def process(path: Path, by_chapter: dict[str, list[dict]]) -> bool:
    data = load(path)
    subject = subject_of(path)
    changed = False
    changed |= polish_symbols(data, subject)
    changed |= polish_derivation(data, subject)
    changed |= polish_related(data, by_chapter)
    if changed:
        save(path, data)
    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--importance", default="")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    imp_set = None
    if args.importance:
        imp_set = {int(x) for x in args.importance.split(",") if x.strip()}
    if not args.all and imp_set is None:
        print("Specify --importance or --all")
        return

    paths = sorted(ROOT.rglob("formulas/*.json"))
    # index by chapter for related
    by_chapter: dict[str, list[dict]] = defaultdict(list)
    metas = []
    for p in paths:
        d = load(p)
        meta = {
            "id": d.get("id"),
            "chapter": d.get("chapter"),
            "order": d.get("order") or 0,
            "importance": int(d.get("importance") or 2),
            "path": p,
        }
        metas.append(meta)
        if meta["chapter"] and meta["id"]:
            by_chapter[meta["chapter"]].append(meta)

    n = 0
    total = 0
    for meta in metas:
        if imp_set is not None and meta["importance"] not in imp_set:
            continue
        total += 1
        if process(meta["path"], by_chapter):
            n += 1
    print(f"fix-remaining-mess: updated {n} / {total}")


if __name__ == "__main__":
    main()
