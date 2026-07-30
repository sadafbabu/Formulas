#!/usr/bin/env python3
"""
Repolish auto-template content left by upgrade-memorize-full.py.

Targets:
  - memorize.steps starting with 'সূত্র:' / 'চিহ্ন মনে রাখো' / 'কী কাজে লাগে'
  - questions with 'কখন ব্যবহার করবে'
  - symbols meaning ending with 'সম্পর্কিত রাশি'
  - derivation steps with identical latex (মূল সূত্র + প্রয়োগ)

Usage:
  python3 scripts/repolish-template-content.py --importance 3
  python3 scripts/repolish-template-content.py --importance 1,2
  python3 scripts/repolish-template-content.py --all
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "subjects"

SYMBOL_MEANINGS: dict[str, tuple[str, str]] = {
    "F": ("বল", "N"),
    "f": ("কম্পাঙ্ক / বল (প্রসঙ্গমতে)", "Hz বা N"),
    "m": ("ভর", "kg"),
    "M": ("ভর / মোলার ভর", "kg বা g/mol"),
    "a": ("ত্বরণ", "m/s²"),
    "v": ("বেগ", "m/s"),
    "u": ("আদি বেগ", "m/s"),
    "s": ("সরণ", "m"),
    "t": ("সময়", "s"),
    "T": ("পর্যায়কাল / তাপমাত্রা", "s বা K"),
    "P": ("চাপ / ক্ষমতা", "Pa বা W"),
    "p": ("ভরবেগ / চাপ", "kg·m/s বা Pa"),
    "E": ("শক্তি / তড়িৎক্ষেত্র", "J বা N/C"),
    "U": ("বিভব শক্তি", "J"),
    "K": ("গতিশক্তি / ধ্রুবক", "J"),
    "W": ("কাজ", "J"),
    "Q": ("তাপ / চার্জ", "J বা C"),
    "q": ("চার্জ", "C"),
    "I": ("তড়িৎ প্রবাহ / জড়তার ভ্রামক", "A বা kg·m²"),
    "V": ("বিভব / আয়তন", "V বা m³"),
    "R": ("রোধ / গ্যাস ধ্রুবক / ব্যাসার্ধ", "Ω বা J/(mol·K) বা m"),
    "r": ("ব্যাসার্ধ / দূরত্ব", "m"),
    "L": ("দৈর্ঘ্য / আবেশ / ল্যাটেন্ট", "m বা H"),
    "C": ("ধারণক্ষমতা / ধারকত্ব", "F বা J/K"),
    "n": ("মোল সংখ্যা / কোটি", "mol"),
    "N": ("কণা সংখ্যা", "1"),
    "g": ("অভিকর্ষজ ত্বরণ", "m/s²"),
    "h": ("উচ্চতা / প্ল্যাঙ্ক ধ্রুবক", "m বা J·s"),
    "H": ("চৌম্বক ক্ষেত্র / এনথ্যালপি", "A/m বা J"),
    "B": ("চৌম্বক ক্ষেত্র", "T"),
    "omega": ("কৌণিক বেগ", "rad/s"),
    "theta": ("কোণ", "rad"),
    "phi": ("দশা / ফ্লাক্স", "rad বা Wb"),
    "lambda": ("তরঙ্গদৈর্ঘ্য / ক্ষয় ধ্রুবক", "m বা 1/s"),
    "mu": ("প্রতিসরাঙ্ক / চৌম্বক ভ্রামক", "—"),
    "rho": ("ঘনত্ব / রোধাঙ্ক", "kg/m³ বা Ω·m"),
    "sigma": ("স্ট্রেস / স্টেফান ধ্রুবক / পরিবাহিতা", "—"),
    "alpha": ("কোণ / প্রসারণ গুণাঙ্ক", "—"),
    "beta": ("কোণ / ক্ষেত্র প্রসারণ", "—"),
    "gamma": ("আয়তন প্রসারণ / আপেক্ষিকতা", "—"),
    "eta": ("সান্দ্রতা / দক্ষতা", "Pa·s বা 1"),
    "kappa": ("বক্রতা / পরিবাহিতা", "—"),
    "Delta": ("পরিবর্তন", "—"),
    "pi": ("পাই", "1"),
    "c": ("আলোর বেগ / আপেক্ষিক তাপ", "m/s বা J/(kg·K)"),
    "k": ("বল ধ্রুবক / বোল্টজম্যান / তরঙ্গ সংখ্যা", "—"),
    "A": ("ক্ষেত্রফল / বিস্তার", "m²"),
    "d": ("দূরত্ব / ব্যাস", "m"),
    "x": ("অবস্থান / অজানা", "m"),
    "y": ("অবস্থান", "m"),
    "z": ("অবস্থান", "m"),
    "G": ("মহাকর্ষ ধ্রুবক", "N·m²/kg²"),
    "e": ("ইলেকট্রন চার্জ / ভিত্তি", "C"),
    "S": ("এনট্রপি / পৃষ্ঠটান", "J/K বা N/m"),
    "Z": ("পারমাণবিক সংখ্যা / প্রতিবন্ধকতা", "1 বা Ω"),
    "J": ("তড়িৎ ঘনত্ব", "A/m²"),
    "D": ("দূরত্ব / তড়িৎ সরণ", "m"),
    "w": ("ভর / কোণীয়", "kg"),
    "X": ("রিয়েক্ট্যান্স", "Ω"),
    "Y": ("ইয়ং গুণাঙ্ক / অ্যাডমিট্যান্স", "Pa বা S"),
}


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_template_steps(steps: list) -> bool:
    if not steps:
        return True
    joined = " | ".join(str(s) for s in steps)
    return (
        any(str(s).startswith("সূত্র:") for s in steps)
        or "চিহ্ন মনে রাখো" in joined
        or any(str(s).startswith("কী কাজে লাগে:") for s in steps)
    )


def is_template_question(qs: list) -> bool:
    if not qs:
        return True
    return any(
        ("কখন ব্যবহার করবে?" in (q.get("question") or ""))
        or (q.get("question") or "").strip().endswith("মূল সম্পর্ক কী?")
        for q in qs
    )


def is_stub_symbol_meanings(syms: list) -> bool:
    if not syms:
        return True
    return any("সম্পর্কিত রাশি" in str(s.get("meaning", "")) for s in syms)


def is_dup_derivation(der: dict) -> bool:
    steps = der.get("steps") or []
    if len(steps) < 2:
        return True
    return (steps[0].get("latex") or "") == (steps[1].get("latex") or "")


def clean_sym_key(symbol: str) -> str:
    s = symbol.strip()
    s = re.sub(r"^\\", "", s)
    s = re.sub(r"[_^].*$", "", s)
    s = re.sub(r"[{}]", "", s)
    return s


def meaning_for_symbol(symbol: str) -> tuple[str, str]:
    key = clean_sym_key(symbol)
    if key in SYMBOL_MEANINGS:
        return SYMBOL_MEANINGS[key]
    # greek commands
    low = key.lower()
    for name, pair in SYMBOL_MEANINGS.items():
        if name.lower() == low:
            return pair
    return (f"{symbol} (সূত্রের রাশি)", "—")


def polish_symbols(data: dict) -> bool:
    syms = data.get("symbols") or []
    if not is_stub_symbol_meanings(syms):
        return False
    new = []
    for s in syms:
        sym = str(s.get("symbol", "?")).strip() or "?"
        meaning = str(s.get("meaning", ""))
        unit = str(s.get("unit") or "—")
        if "সম্পর্কিত রাশি" in meaning or len(meaning) < 4:
            m, u = meaning_for_symbol(sym)
            meaning = m
            if unit in ("—", "", "সূত্রানুযায়ী"):
                unit = u
        new.append({"symbol": sym, "meaning": meaning, "unit": unit})
        if "value" in s and s["value"] is not None:
            new[-1]["value"] = s["value"]
    data["symbols"] = new
    return True


def polish_memorize(data: dict) -> bool:
    mem = dict(data.get("memorize") or {})
    steps = list(mem.get("steps") or [])
    if not is_template_steps(steps):
        return False
    title_bn = data.get("titleBn") or data.get("title") or data["id"]
    trick = (mem.get("trick") or "").strip()
    summary = (data.get("summary") or "").strip()
    latex = (data.get("latex") or "").strip()

    new_steps: list[str] = []
    # 1) Conceptual cue from trick (strip trailing latex-only bits)
    if trick:
        cue = re.sub(r"\s+", " ", trick).strip()
        if len(cue) > 110:
            cue = cue[:107] + "…"
        new_steps.append(cue)
    elif summary:
        new_steps.append(summary[:110])
    else:
        new_steps.append(f"{title_bn} এর মূল ধারণা মনে রাখো")

    # 2) When to use
    new_steps.append(f"প্রশ্নে {title_bn} প্রসঙ্গ দেখলে এই সম্পর্ক বসাও")

    # 3) Check units / limits
    syms = data.get("symbols") or []
    if syms:
        top = ", ".join(str(s.get("symbol")) for s in syms[:3])
        new_steps.append(f"রাশি মিলিয়ে নাও: {top} — একক যাচাই করো")
    else:
        new_steps.append("একক ও চিহ্ন মিলিয়ে উত্তর যাচাই করো")

    # Avoid dumping raw latex as a step
    data["memorize"] = {"trick": trick or f"{title_bn} মনে রাখার কৌশল", "steps": new_steps[:4]}
    # silence unused
    _ = latex
    return True


def polish_questions(data: dict) -> bool:
    qs = data.get("questions") or []
    if not is_template_question(qs):
        return False
    title_bn = data.get("titleBn") or data.get("title") or data["id"]
    latex = (data.get("latex") or "").strip()
    trick = ((data.get("memorize") or {}).get("trick") or "").strip()
    summary = (data.get("summary") or "").strip()

    answer_parts = []
    if latex:
        answer_parts.append(latex)
    answer = answer_parts[0] if answer_parts else r"\text{" + title_bn[:60] + "}"

    data["questions"] = [
        {
            "examType": "HSC / Admission",
            "question": f"{title_bn} এর মূল সূত্র কী? কোন ধরনের সমস্যায় এটি লাগে?",
            "answer": answer,
        }
    ]
    # Concept answer as plain-friendly kaTeX text
    concept = trick or summary
    if concept and not re.search(r"\\\\|\\frac|\\sum|\\int", concept):
        safe = concept.replace("\\", "").replace("{", "").replace("}", "")[:120]
        data["questions"].append(
            {
                "examType": "Concept",
                "question": f"{title_bn} দিয়ে কী নির্ণয়/বোঝা যায়?",
                "answer": r"\text{" + safe + "}",
            }
        )
    return True


def polish_derivation(data: dict) -> bool:
    der = data.get("derivation") or {}
    if not is_dup_derivation(der):
        # still normalize body→latex if needed
        return False
    title_bn = data.get("titleBn") or data.get("title") or data["id"]
    latex = (data.get("latex") or "").strip() or r"\text{" + title_bn[:40] + "}"
    lead = (der.get("lead") or data.get("summary") or title_bn).strip()
    assumptions = der.get("assumptions") if isinstance(der.get("assumptions"), list) else []
    trick = ((data.get("memorize") or {}).get("trick") or "").strip()

    step2_note = trick[:120] if trick else "রাশি চিনে সূত্রে বসাও; সীমা ও একক যাচাই করো।"
    data["derivation"] = {
        "lead": lead if len(lead) >= 20 else f"{title_bn} এর মূল সম্পর্ক।",
        "steps": [
            {
                "title": "মূল সূত্র",
                "latex": latex,
                "note": f"{title_bn} এর প্রাথমিক রূপ।",
            },
            {
                "title": "মনে রাখা ও প্রয়োগ",
                "latex": r"\text{identify quantities } \rightarrow \text{ substitute}",
                "note": step2_note,
            },
        ],
        "assumptions": assumptions,
    }
    return True


def needs_polish(data: dict) -> bool:
    mem = data.get("memorize") or {}
    return (
        is_template_steps(mem.get("steps") or [])
        or is_template_question(data.get("questions") or [])
        or is_stub_symbol_meanings(data.get("symbols") or [])
        or is_dup_derivation(data.get("derivation") or {})
    )


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--importance", default="")
    ap.add_argument("--subject", choices=["physics", "chemistry", "math"])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    imp_set = None
    if args.importance:
        imp_set = {int(x) for x in args.importance.split(",") if x.strip()}
    if not args.all and imp_set is None and not args.subject:
        print("Specify --importance, --subject, or --all")
        return

    updated = 0
    for path in sorted(ROOT.rglob("formulas/*.json")):
        subject = path.relative_to(ROOT).parts[0]
        if args.subject and subject != args.subject:
            continue
        data = load(path)
        imp = data.get("importance", 2)
        if imp_set is not None and imp not in imp_set:
            continue
        if not needs_polish(data):
            continue
        changed = False
        changed |= polish_memorize(data)
        changed |= polish_symbols(data)
        changed |= polish_questions(data)
        changed |= polish_derivation(data)
        if changed:
            updated += 1
            if not args.dry_run:
                save(path, data)
    print(f"Repolished {updated} formulas" + (" (dry-run)" if args.dry_run else ""))


if __name__ == "__main__":
    main()
