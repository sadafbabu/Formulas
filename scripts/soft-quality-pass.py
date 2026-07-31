#!/usr/bin/env python3
"""
Soft quality pass: fake derivations, wrong symbols, echoed memorize/questions,
summary/trick/lead echoes, and known mangled answers.

Usage:
  python3 scripts/soft-quality-pass.py --importance 3
  python3 scripts/soft-quality-pass.py --importance 2
  python3 scripts/soft-quality-pass.py --importance 1
  python3 scripts/soft-quality-pass.py --all
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "subjects"

OPERATOR_SYMBOLS = {
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
}

JUNK_SYMBOL_RE = re.compile(
    r"^(open-chain|cyclic|hemiacetal|pyranose|furanose|main:|text)",
    re.I,
)

SOFT_Q_RE = re.compile(
    r"(লিখো এবং একটি ব্যবহার|দিয়ে কী নির্ণয়|মূল সূত্র কী\? এক লাইনে|সংক্ষেপে কী কাজে লাগে|কোন ধরনের সমস্যায় এটি লাগে)",
)

ECHO_STEP_RE = re.compile(r"^(মনে রাখো —|প্রয়োগ:|পরীক্ষায়:|চিহ্ন চেক:|কাজ:)")

PHYS = {
    "F": ("বল", "N"),
    "f": ("কম্পাঙ্ক / ঘর্ষণ বল", "Hz বা N"),
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
    "r": ("ব্যাসার্ধ / দূরত্ব", "m"),
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
    "rho": ("ঘনত্ব / রোধাঙ্ক", "kg/m³ বা Ω·m"),
    "alpha": ("কোণ / প্রসারণ গুণাঙ্ক", "—"),
    "eta": ("সান্দ্রতা / দক্ষতা", "Pa·s"),
    "c": ("আলোর বেগ", "m/s"),
    "k": ("বল ধ্রুবক / তরঙ্গ সংখ্যা", "—"),
    "A": ("ক্ষেত্রফল / বিস্তার", "m²"),
    "G": ("মহাকর্ষ ধ্রুবক", "N·m²/kg²"),
    "n": ("প্রতিসরাঙ্ক / মোল", "—"),
    "N": ("কুণ্ডলীর পাক / কণা সংখ্যা", "—"),
    "phi": ("চৌম্বক ফ্লাক্স / দশা", "Wb বা rad"),
    "sigma": ("স্ট্রেস / স্টেফান ধ্রুবক", "—"),
    "Delta": ("পরিবর্তন", "—"),
}

CHEM = {
    "H": ("এনথ্যালপি", "J বা kJ"),
    "S": ("এনট্রপি", "J/K"),
    "G": ("গিবস মুক্ত শক্তি", "J"),
    "E": ("বন্ধন শক্তি / কোশ বিভব", "J বা V"),
    "T": ("পরম তাপমাত্রা", "K"),
    "P": ("চাপ", "Pa বা atm"),
    "V": ("আয়তন", "L বা m³"),
    "n": ("মোল সংখ্যা", "mol"),
    "N": ("কণা সংখ্যা", "—"),
    "R": ("সার্বজনীন গ্যাস ধ্রুবক", "J/(mol·K)"),
    "K": ("সাম্য ধ্রুবক / হার ধ্রুবক", "—"),
    "k": ("হার ধ্রুবক", "—"),
    "c": ("ঘনমাত্রা", "mol/L"),
    "C": ("ঘনমাত্রা / তাপধারণ", "mol/L বা J/K"),
    "Q": ("বিক্রিয়া ভাগফল / তাপ", "—"),
    "q": ("তাপ", "J"),
    "m": ("ভর", "g বা kg"),
    "M": ("মোলার ভর", "g/mol"),
    "t": ("সময়", "s"),
    "A": ("প্রাক-এক্সপোনেনশিয়াল / ক্ষেত্রফল", "—"),
    "Ea": ("সক্রিয়ন শক্তি", "J/mol"),
    "pH": ("হাইড্রোজেন আয়ন সূচক", "—"),
    "Ka": ("অ্যাসিড বিয়োজন ধ্রুবক", "—"),
    "Kb": ("বেস বিয়োজন ধ্রুবক", "—"),
    "Kw": ("পানির আয়নিক গুণফল", "—"),
    "mu": ("দ্বিমেরু ভ্রামক", "D"),
    "Delta": ("পরিবর্তন", "—"),
    "alpha": ("বিয়োজন মাত্রা", "—"),
    "beta": ("বাফার ক্ষমতা", "—"),
    "I": ("আয়নিক শক্তি / প্রবাহ", "—"),
    "F": ("ফ্যারাডে ধ্রুবক", "C/mol"),
    "Ecell": ("কোশ বিভব", "V"),
    "Z": ("পারমাণবিক সংখ্যা", "—"),
    "w": ("ভর / কাজ", "g বা J"),
}

MATH = {
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
    "t": ("প্যারামিটার / সময়", "—"),
    "theta": ("কোণ", "rad"),
    "phi": ("কোণ", "rad"),
    "Delta": ("পরিবর্তন", "—"),
    "Sigma": ("সমষ্টি", "—"),
    "lim": ("সীমা", "—"),
    "dx": ("অন্তরক", "—"),
    "dy": ("অন্তরক", "—"),
}


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def subject_of(path: Path) -> str:
    return path.relative_to(ROOT).parts[0]


def clean_sym_key(symbol: str) -> str:
    s = symbol.strip()
    s = re.sub(r"^\\", "", s)
    s = re.sub(r"[_^].*$", "", s)
    s = re.sub(r"[{}]", "", s)
    return s


def meaning_for(symbol: str, subject: str) -> tuple[str, str] | None:
    key = clean_sym_key(symbol)
    if not key or key in OPERATOR_SYMBOLS or JUNK_SYMBOL_RE.match(key):
        return None
    table = PHYS if subject == "physics" else CHEM if subject == "chemistry" else MATH
    if key in table:
        return table[key]
    low = key.lower()
    for name, pair in table.items():
        if name.lower() == low:
            return pair
    # Keep existing-looking chem formulas like NH_3
    if re.search(r"[A-Z][a-z]?\d|_\{", symbol):
        return (f"{symbol} (রাসায়নিক রাশি)", "—") if subject == "chemistry" else (f"{symbol}", "—")
    return (f"{key} (সূত্রের রাশি)", "—")


def polish_symbols(data: dict, subject: str) -> bool:
    syms = data.get("symbols") or []
    if not syms:
        return False
    new = []
    changed = False
    for s in syms:
        sym = str(s.get("symbol", "")).strip()
        if not sym:
            changed = True
            continue
        key = clean_sym_key(sym)
        if key in OPERATOR_SYMBOLS or JUNK_SYMBOL_RE.match(sym) or " " in sym and len(sym) > 18:
            changed = True
            continue
        meaning = str(s.get("meaning") or "")
        unit = str(s.get("unit") or "—")
        mapped = meaning_for(sym, subject)
        if mapped is None:
            changed = True
            continue
        m, u = mapped
        # Fix cross-domain / stub meanings
        bad = (
            "সম্পর্কিত রাশি" in meaning
            or "(সূত্রের রাশি)" in meaning
            or (subject == "chemistry" and "চৌম্বক" in meaning and key in ("H", "B"))
            or (subject == "math" and meaning in ("ত্বরণ", "ভর", "বেগ", "সময়") and key in ("a", "m", "v", "t"))
            or (subject == "chemistry" and "তড়িৎক্ষেত্র" in meaning and key == "E")
            or len(meaning) < 3
        )
        if bad:
            meaning, unit = m, u if unit in ("—", "", "সূত্রানুযায়ী") else unit
            changed = True
        entry = {"symbol": sym, "meaning": meaning, "unit": unit}
        if "value" in s and s["value"] is not None:
            entry["value"] = s["value"]
        new.append(entry)
    if not new and syms:
        title = data.get("titleBn") or data.get("title") or data.get("id") or "সূত্র"
        data["symbols"] = [
            {"symbol": r"\text{key}", "meaning": f"{title} এর মূল রাশি", "unit": "—"}
        ]
        return True
    if changed or new != syms:
        data["symbols"] = new
        return True
    return False


def polish_fields_echo(data: dict) -> bool:
    title = data.get("titleBn") or data.get("title") or data["id"]
    summary = (data.get("summary") or "").strip()
    mem = dict(data.get("memorize") or {})
    trick = (mem.get("trick") or "").strip()
    der = dict(data.get("derivation") or {})
    lead = (der.get("lead") or "").strip()
    changed = False

    if not summary:
        summary = f"{title} সংক্রান্ত মূল সম্পর্ক।"
        data["summary"] = summary
        changed = True

    if not trick:
        trick = summary
        mem["trick"] = trick
        changed = True

    # Split identical triple
    if summary and trick == summary and (not lead or lead == summary):
        data["summary"] = f"{title}: {summary}" if not summary.startswith(title) else summary
        mem["trick"] = trick if len(trick) >= 12 else f"{title} মনে রাখার চাবিকাঠি।"
        der["lead"] = f"{title} প্রয়োগের আগে রাশি ও একক ঠিক করে নাও।"
        if "steps" not in der:
            der["steps"] = []
        if "assumptions" not in der or not isinstance(der.get("assumptions"), list):
            der["assumptions"] = []
        data["memorize"] = mem
        data["derivation"] = der
        changed = True
    elif lead == summary == trick and summary:
        der["lead"] = f"{title} এর সম্পর্ক বসানোর আগে প্রদত্ত রাশি চিহ্নিত করো।"
        data["derivation"] = der
        changed = True

    if mem != (data.get("memorize") or {}):
        data["memorize"] = mem
    return changed


def polish_memorize_steps(data: dict) -> bool:
    mem = dict(data.get("memorize") or {})
    steps = [str(s) for s in (mem.get("steps") or [])]
    trick = (mem.get("trick") or "").strip()
    title = data.get("titleBn") or data.get("title") or data["id"]
    summary = (data.get("summary") or "").strip()
    soft = (
        not steps
        or len(steps) < 2
        or any(ECHO_STEP_RE.match(s) for s in steps)
        or (trick and any(s == trick or s == f"মনে রাখো — {trick}" for s in steps))
        or any(s.startswith("চিহ্ন চেক:") for s in steps)
    )
    if not soft:
        return False

    cue = trick or summary or f"{title} এর মূল ধারণা"
    if len(cue) > 110:
        cue = cue[:107] + "…"
    new_steps = [
        cue,
        f"প্রশ্নে {title} বা একই রাশি দেখলে এই সূত্র বসাও।",
    ]
    syms = data.get("symbols") or []
    good = [s for s in syms if s.get("meaning") and "(সূত্রের রাশি)" not in str(s.get("meaning"))]
    if good:
        bits = ", ".join(f"{s.get('symbol')}={s.get('meaning')}" for s in good[:2])
        new_steps.append(f"রাশি মিলিয়ে নাও: {bits}।")
    else:
        new_steps.append("একক, চিহ্ন ও সীমাবদ্ধতা যাচাই করে উত্তর লেখো।")

    mem["steps"] = new_steps[:4]
    if not mem.get("trick"):
        mem["trick"] = cue
    data["memorize"] = mem
    return True


def polish_questions(data: dict) -> bool:
    qs = list(data.get("questions") or [])
    title = data.get("titleBn") or data.get("title") or data["id"]
    latex = (data.get("latex") or "").strip()
    trick = ((data.get("memorize") or {}).get("trick") or "").strip()
    summary = (data.get("summary") or "").strip()
    changed = False

    new_qs = []
    for q in qs:
        question = str(q.get("question") or "")
        answer = str(q.get("answer") or "")
        # Fix mangled answers missing backslashes
        if re.search(r"\btext[a-zA-Z]", answer) and "\\text" not in answer:
            answer = latex or (r"\text{" + (trick or summary or title)[:80] + "}")
            changed = True
        if SOFT_Q_RE.search(question):
            question = f"{title} কোন পরিস্থিতিতে লাগে? একটি উদাহরণ দাও।"
            if latex and trick:
                answer = f"{latex}\\text{{ — }}{trick[:80]}"
            elif latex:
                answer = latex
            else:
                safe = (trick or summary or title).replace("\\", "")[:100]
                answer = r"\text{" + safe + "}"
            changed = True
        new_qs.append(
            {
                "examType": q.get("examType") or "HSC / Admission",
                "question": question,
                "answer": answer,
            }
        )

    if not new_qs:
        new_qs = [
            {
                "examType": "HSC / Admission",
                "question": f"{title} কোন পরিস্থিতিতে লাগে? একটি উদাহরণ দাও।",
                "answer": latex or r"\text{" + title[:60] + "}",
            }
        ]
        changed = True

    # Ensure a concept question exists and isn't soft-duplicated
    has_concept = any((q.get("examType") or "").lower().startswith("concept") for q in new_qs)
    if not has_concept and (trick or summary):
        safe = (trick or summary).replace("\\", "").replace("{", "").replace("}", "")[:120]
        new_qs.append(
            {
                "examType": "Concept",
                "question": f"{title} দিয়ে কী বোঝা যায় / সাধারণ ভুল কী?",
                "answer": r"\text{" + safe + "}",
            }
        )
        changed = True

    if changed:
        data["questions"] = new_qs
    return changed


def polish_derivation(data: dict, subject: str) -> bool:
    der = dict(data.get("derivation") or {})
    steps = list(der.get("steps") or [])
    latex = (data.get("latex") or "").strip()
    title = data.get("titleBn") or data.get("title") or data["id"]
    trick = ((data.get("memorize") or {}).get("trick") or "").strip()
    summary = (data.get("summary") or "").strip()
    lead = (der.get("lead") or "").strip()

    dup = len(steps) >= 2 and (steps[0].get("latex") or "") == (steps[1].get("latex") or "")
    thin = len(steps) < 2 or any(
        "প্রাথমিক রূপ" in str(s.get("note") or "") for s in steps
    )
    if not dup and not thin and steps:
        # still fix empty assumptions lightly
        assumptions = der.get("assumptions")
        if isinstance(assumptions, list) and len(assumptions) == 0:
            der["assumptions"] = default_assumptions(subject, title)
            data["derivation"] = der
            return True
        return False

    if not lead or lead == summary == trick:
        lead = f"{title} প্রয়োগের আগে প্রদত্ত রাশি ও একক ঠিক করো।"

    step1_note = summary if summary and summary != trick else f"{title} এর মূল সম্পর্ক।"
    step2_note = trick[:140] if trick else "দেওয়া মান বসিয়ে ফলাফল বের করো; একক যাচাই করো।"

    apply_latex = r"\text{রাশি চিহ্নিত করো} \rightarrow \text{সূত্রে মান বসাও}"
    # Ensure different from main latex
    if apply_latex == latex:
        apply_latex = r"\text{প্রয়োগ} \rightarrow \text{ফলাফল}"

    der["lead"] = lead
    der["steps"] = [
        {
            "title": "মূল সূত্র",
            "latex": latex or r"\text{" + title[:40] + "}",
            "note": step1_note[:160],
        },
        {
            "title": "প্রয়োগের ধাপ",
            "latex": apply_latex,
            "note": step2_note[:160],
        },
    ]
    assumptions = der.get("assumptions")
    if not isinstance(assumptions, list) or len(assumptions) == 0:
        der["assumptions"] = default_assumptions(subject, title)
    data["derivation"] = der
    return True


def default_assumptions(subject: str, title: str) -> list[str]:
    if subject == "physics":
        return ["SI একক ব্যবহার করো", "প্রশ্নে উল্লিখিত আদর্শ শর্ত প্রযোজ্য"]
    if subject == "chemistry":
        return ["প্রমিত/প্রদত্ত তাপমাত্রা-চাপ ধরো", "প্রতিক্রিয়া/গঠন প্রশ্নে দেওয়া তথ্য অনুসরণ করো"]
    return ["প্রদত্ত শর্ত ও ডোমেইন মেনে চলো", f"{title} এর সংজ্ঞা অনুযায়ী সীমাবদ্ধতা দেখো"]


def fix_known_mangled(data: dict) -> bool:
    fid = data.get("id")
    if fid == "glucose-open-cyclic":
        data["latex"] = r"\text{open-chain aldehyde} \rightleftharpoons \text{cyclic hemiacetal (pyranose)}"
        data["summary"] = "D-গ্লুকোজ মুক্ত অ্যালডিহাইড ও চক্রাকার পাইরানোজ রূপে সাম্যে থাকে।"
        data["symbols"] = [
            {"symbol": r"\mathrm{CHO}", "meaning": "অ্যালডিহাইড গ্রুপ (মুক্ত শিকল)", "unit": "—"},
            {"symbol": "pyranose", "meaning": "ছয়-সদস্যবিশিষ্ট চক্রাকার হেমিঅ্যাসিটাল", "unit": "—"},
        ]
        data["memorize"] = {
            "trick": "D-গ্লুকোজ মূলত পাইরানোজ; মুক্ত↔চক্রাকার সাম্য।",
            "steps": [
                "মুক্ত অ্যালডিহাইড ও চক্রাকার হেমিঅ্যাসিটাল সাম্যে থাকে।",
                "প্রশ্নে গ্লুকোজ গঠন/মিউটারোটেশন দেখলে এই সাম্য মনে রাখো।",
                "পাইরানোজ = ছয় সদস্য; ফিউরানোজ = পাঁচ সদস্য।",
            ],
        }
        data["derivation"] = {
            "lead": "অ্যালডিহাইডের সাথে OH যুক্ত হয়ে চক্রাকার হেমিঅ্যাসিটাল গঠিত হয়।",
            "steps": [
                {
                    "title": "সাম্য",
                    "latex": r"\text{open-chain} \rightleftharpoons \text{pyranose}",
                    "note": "দ্রবণে দুই রূপ সহাবস্থান করে।",
                },
                {
                    "title": "মনে রাখা",
                    "latex": r"\text{D-glucose mainly pyranose}",
                    "note": "HSC/মেডিকেলে পাইরানোজই প্রধান রূপ।",
                },
            ],
            "assumptions": ["জলে দ্রবীভূত অবস্থা", "প্রমিত তাপমাত্রা"],
        }
        data["questions"] = [
            {
                "examType": "HSC / Admission",
                "question": "গ্লুকোজের মুক্ত ও চক্রাকার রূপের সম্পর্ক কী?",
                "answer": r"\text{open-chain aldehyde} \rightleftharpoons \text{cyclic hemiacetal (pyranose)}",
            },
            {
                "examType": "Concept",
                "question": "D-গ্লুকোজ দ্রবণে কোন রূপ প্রধান?",
                "answer": r"\text{pyranose (six-membered cyclic hemiacetal)}",
            },
        ]
        return True

    if fid == "cement-composition":
        data["latex"] = r"\mathrm{CaO},\,\mathrm{SiO_2},\,\mathrm{Al_2O_3},\,\mathrm{Fe_2O_3}"
        data["summary"] = "পোর্টল্যান্ড সিমেন্টের প্রধান অক্সাইড: CaO, SiO₂, Al₂O₃, Fe₂O₃।"
        data["symbols"] = [
            {"symbol": r"\mathrm{CaO}", "meaning": "ক্যালসিয়াম অক্সাইড", "unit": "—"},
            {"symbol": r"\mathrm{SiO_2}", "meaning": "সিলিকা", "unit": "—"},
            {"symbol": r"\mathrm{Al_2O_3}", "meaning": "অ্যালুমিনা", "unit": "—"},
            {"symbol": r"\mathrm{Fe_2O_3}", "meaning": "আয়রন অক্সাইড", "unit": "—"},
        ]
        data["memorize"] = {
            "trick": "CaO + SiO₂ + Al₂O₃ + Fe₂O₃ — সিমেন্টের মূল অক্সাইড।",
            "steps": [
                "প্রধান চার অক্সাইড মনে রাখো: Ca–Si–Al–Fe।",
                "জলযোগে হাইড্রেশন → সেটিং ও শক্তি বৃদ্ধি।",
                "অনুপাত বদলালে সেটিং সময় ও শক্তি বদলায়।",
            ],
        }
        data["derivation"] = {
            "lead": "কাঁচামাল তাপজাত হয়ে এই অক্সাইডগুলো দেয়।",
            "steps": [
                {
                    "title": "প্রধান উপাদান",
                    "latex": r"\mathrm{CaO},\,\mathrm{SiO_2},\,\mathrm{Al_2O_3},\,\mathrm{Fe_2O_3}",
                    "note": "পোর্টল্যান্ড সিমেন্টের মূল অক্সাইডসমূহ।",
                },
                {
                    "title": "প্রয়োগ",
                    "latex": r"\text{hydration} \rightarrow \text{setting}",
                    "note": "জলযোগে সেটিং ও হাইড্রেশন।",
                },
            ],
            "assumptions": ["সাধারণ পোর্টল্যান্ড সিমেন্ট"],
        }
        data["questions"] = [
            {
                "examType": "HSC / Admission",
                "question": "পোর্টল্যান্ড সিমেন্টের প্রধান অক্সাইডগুলো কী কী?",
                "answer": r"\mathrm{CaO},\,\mathrm{SiO_2},\,\mathrm{Al_2O_3},\,\mathrm{Fe_2O_3}",
            },
            {
                "examType": "Concept",
                "question": "সিমেন্টে জল যোগ করলে কী ঘটে?",
                "answer": r"\text{hydration এবং setting শুরু হয়}",
            },
        ]
        return True

    if fid == "ostwald-nh3-oxidation":
        data["summary"] = "অস্টওয়াল্ড প্রক্রিয়ায় Pt অনুঘটকে NH₃ জারিত হয়ে NO হয়; পরে HNO₃ তৈরি।"
        data["symbols"] = [
            {"symbol": r"\mathrm{NH_3}", "meaning": "অ্যামোনিয়া", "unit": "—"},
            {"symbol": r"\mathrm{O_2}", "meaning": "অক্সিজেন", "unit": "—"},
            {"symbol": r"\mathrm{Pt}", "meaning": "প্ল্যাটিনাম অনুঘটক", "unit": "—"},
            {"symbol": r"\mathrm{NO}", "meaning": "নাইট্রিক অক্সাইড", "unit": "—"},
        ]
        data["memorize"] = {
            "trick": "NH₃ → NO (Pt) → পরে HNO₃ — অস্টওয়াল্ড।",
            "steps": [
                "৪ NH₃ + ৫ O₂ → ৪ NO + ৬ H₂O (Pt)।",
                "নাইট্রিক অ্যাসিড শিল্পে এই ধাপই চাবিকাঠি।",
                "অনুঘটক Pt এবং উচ্চ তাপমাত্রা মনে রাখো।",
            ],
        }
        data["derivation"] = {
            "lead": "অ্যামোনিয়ার অনুঘটকীয় জারণে নাইট্রিক অক্সাইড পাওয়া যায়।",
            "steps": [
                {
                    "title": "জারণ সমীকরণ",
                    "latex": r"4\mathrm{NH_3}+5\mathrm{O_2}\xrightarrow{\mathrm{Pt}}4\mathrm{NO}+6\mathrm{H_2O}",
                    "note": "অস্টওয়াল্ডের মূল ধাপ।",
                },
                {
                    "title": "শিল্প প্রয়োগ",
                    "latex": r"\mathrm{NO} \rightarrow \mathrm{HNO_3}",
                    "note": "NO থেকে ধাপে ধাপে নাইট্রিক অ্যাসিড।",
                },
            ],
            "assumptions": ["Pt অনুঘটক", "উচ্চ তাপমাত্রা"],
        }
        data["questions"] = [
            {
                "examType": "HSC / Admission",
                "question": "অস্টওয়াল্ড প্রক্রিয়ার NH₃ জারণ সমীকরণ লেখো।",
                "answer": r"4\mathrm{NH_3}+5\mathrm{O_2}\xrightarrow{\mathrm{Pt}}4\mathrm{NO}+6\mathrm{H_2O}",
            },
            {
                "examType": "Concept",
                "question": "এই জারণ শেষে শিল্পে কী উৎপাদিত হয়?",
                "answer": r"\text{নাইট্রিক অ্যাসিড (HNO}_3\text{)}",
            },
        ]
        return True

    if fid == "limit-evaluation":
        # Keep good question; fix stubby symbol if needed
        syms = data.get("symbols") or []
        cleaned = []
        for s in syms:
            sym = str(s.get("symbol") or "")
            if "infty" in sym and "(সূত্রের রাশি)" in str(s.get("meaning") or ""):
                cleaned.append({"symbol": r"\infty/\infty", "meaning": "অনির্ণয় রূপ", "unit": "—"})
            else:
                cleaned.append(s)
        data["symbols"] = cleaned
        der = data.get("derivation") or {}
        steps = der.get("steps") or []
        if len(steps) >= 2 and (steps[0].get("latex") or "") == (steps[1].get("latex") or ""):
            data["derivation"] = {
                "lead": "০/০ বা ∞/∞ রূপে L'Hôpital: অবকলন নিয়ে সীমা নাও।",
                "steps": [
                    {
                        "title": "শর্ত",
                        "latex": r"\lim_{x\to a}\frac{f(x)}{g(x)}\ \text{ is } 0/0 \text{ or } \infty/\infty",
                        "note": "অনির্ণয় রূপ চিহ্নিত করো।",
                    },
                    {
                        "title": "L'Hôpital",
                        "latex": r"\lim_{x\to a}\frac{f(x)}{g(x)}=\lim_{x\to a}\frac{f'(x)}{g'(x)}",
                        "note": "অবকলন করে পুনরায় সীমা নির্ণয়।",
                    },
                ],
                "assumptions": ["f,g অবকলনযোগ্য", "ডিনোমিনেটরের অবকলন ≠ ০"],
            }
        return True

    return False


def process(path: Path) -> bool:
    data = load(path)
    subject = subject_of(path)
    changed = False
    if fix_known_mangled(data):
        changed = True
    changed |= polish_symbols(data, subject)
    changed |= polish_fields_echo(data)
    changed |= polish_memorize_steps(data)
    changed |= polish_questions(data)
    changed |= polish_derivation(data, subject)
    if changed:
        save(path, data)
    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--importance", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    imp_set = None
    if args.importance:
        imp_set = {int(x) for x in args.importance.split(",") if x.strip()}
    if not args.all and imp_set is None:
        print("Specify --importance or --all")
        return

    n = 0
    total = 0
    for path in sorted(ROOT.rglob("formulas/*.json")):
        data = load(path)
        imp = int(data.get("importance") or 2)
        if imp_set is not None and imp not in imp_set:
            continue
        total += 1
        if args.dry_run:
            # still run logic on a copy
            before = json.dumps(data, ensure_ascii=False, sort_keys=True)
            subject = subject_of(path)
            fix_known_mangled(data)
            polish_symbols(data, subject)
            polish_fields_echo(data)
            polish_memorize_steps(data)
            polish_questions(data)
            polish_derivation(data, subject)
            after = json.dumps(data, ensure_ascii=False, sort_keys=True)
            if before != after:
                n += 1
        else:
            if process(path):
                n += 1
    print(f"soft-quality-pass: updated {n} / {total}" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
