#!/usr/bin/env python3
"""Polish stub formula JSON: related links, better questions, clearer symbols."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "subjects"
TEMPLATE_Q = re.compile(r"এর মূল সূত্রটি লেখো।?\s*$")


def load_all():
    by_chapter: dict[str, list[tuple[Path, dict]]] = defaultdict(list)
    for path in sorted(ROOT.glob("*/chapters/*/formulas/*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        by_chapter[data["chapter"]].append((path, data))
    return by_chapter


def is_placeholder_symbols(symbols: list) -> bool:
    if not symbols:
        return True
    if len(symbols) == 1 and symbols[0].get("symbol") in {"—", "-", "সূত্র"}:
        return True
    meaning = str(symbols[0].get("meaning", ""))
    return "প্রধান চলকসমূহ" in meaning


def enrich_symbols(data: dict) -> None:
    if not is_placeholder_symbols(data.get("symbols", [])):
        return
    latex = data.get("latex", "")
    # Prefer readable tokens from latex (letters, \\vec v, \\mu, etc.)
    tokens = re.findall(
        r"\\(?:vec|mathrm|text|operatorname)\{([^}]+)\}|\\([A-Za-z]+)|([A-Za-z])",
        latex,
    )
    flat = []
    for a, b, c in tokens:
        t = (a or b or c).strip()
        if t and t not in flat and t.lower() not in {"quad", "qquad", "left", "right", "frac", "text", "mathrm", "operatorname", "begin", "end", "cases", "cdot", "times", "approx", "propto", "infty", "ln", "log", "sin", "cos", "tan", "sec", "min", "max", "to", "ne", "ge", "le", "pm", "mp"}:
            flat.append(t)
        if len(flat) >= 4:
            break
    if not flat:
        flat = ["সূত্র"]
    data["symbols"] = [
        {
            "symbol": ", ".join(flat[:4]),
            "meaning": data.get("summary") or data.get("titleBn") or "মূল চলক",
            "unit": "সূত্রানুযায়ী",
        }
    ]


def enrich_question(data: dict) -> None:
    questions = data.get("questions") or []
    if not questions:
        return
    q0 = questions[0]
    question = q0.get("question", "")
    answer = q0.get("answer", "")
    latex = data.get("latex", "")
    trick = (data.get("memorize") or {}).get("trick", "").strip()
    if TEMPLATE_Q.search(question) or answer.strip() == latex.strip():
        q0["question"] = (
            f"{data['titleBn']} — সূত্রটি লেখো এবং কীভাবে মনে রাখবে সংক্ষেপে বলো।"
        )
        if trick:
            q0["answer"] = f"{latex}\\quad(\\text{{{trick[:80]}}})"
            # If Bangla in \text breaks KaTeX, keep latex + separate - validator renders answer
            # Bangla inside \text can work in KaTeX. If fails validation, fall back.
            q0["answer"] = latex
            q0["question"] = (
                f"{data['titleBn']} এর সূত্রটি লেখো। (ইঙ্গিত: {trick[:60]})"
            )
        else:
            q0["answer"] = latex
            q0["question"] = f"{data['titleBn']} — প্রয়োগযোগ্য মূল সূত্রটি কী?"


def enrich_lead(data: dict) -> None:
    der = data.get("derivation") or {}
    lead = (der.get("lead") or "").strip()
    trick = (data.get("memorize") or {}).get("trick", "").strip()
    summary = (data.get("summary") or "").strip()
    if len(lead) < 24 and trick:
        der["lead"] = trick if len(trick) >= 24 else f"{summary} — {trick}"
        data["derivation"] = der
    elif len(lead) < 12 and summary:
        der["lead"] = f"{data.get('titleBn', '')}: {summary}"
        data["derivation"] = der


def fill_related(by_chapter: dict[str, list[tuple[Path, dict]]]) -> int:
    changed = 0
    for chapter, items in by_chapter.items():
        items_sorted = sorted(items, key=lambda x: x[1].get("order", 0))
        ids = [d["id"] for _, d in items_sorted]
        for i, (path, data) in enumerate(items_sorted):
            related = list(data.get("related") or [])
            if related:
                continue
            neighbors = []
            if i > 0:
                neighbors.append(ids[i - 1])
            if i + 1 < len(ids):
                neighbors.append(ids[i + 1])
            if i > 1:
                neighbors.append(ids[i - 2])
            if i + 2 < len(ids) and len(neighbors) < 3:
                neighbors.append(ids[i + 2])
            # unique, not self
            seen = set()
            clean = []
            for rid in neighbors:
                if rid != data["id"] and rid not in seen:
                    seen.add(rid)
                    clean.append(rid)
            data["related"] = clean[:3]
            changed += 1
    return changed


# Known cross-chapter / duplicate pairs to link both ways
CROSS = [
    ("integration-by-parts", "integral-by-parts-ilate"),
    ("implicit-differentiation", "implicit-diff"),
    ("radioactive-decay", "radioactive-decay-law-chem"),
    ("radioactive-decay", "half-life-chem"),
    ("circle-equation", "circle-general-equation"),
    ("product-quotient-rule", "product-rule-diff"),
    ("differentiation-chain-rule", "chain-rule-diff"),
]


def link_cross(by_id: dict[str, tuple[Path, dict]]) -> int:
    n = 0
    for a, b in CROSS:
        if a not in by_id or b not in by_id:
            continue
        for src, dst in ((a, b), (b, a)):
            path, data = by_id[src]
            rel = list(data.get("related") or [])
            if dst not in rel:
                rel.insert(0, dst)
                data["related"] = rel[:4]
                n += 1
    return n


def main():
    by_chapter = load_all()
    related_n = fill_related(by_chapter)
    by_id = {}
    for items in by_chapter.values():
        for path, data in items:
            by_id[data["id"]] = (path, data)
    cross_n = link_cross(by_id)

    written = 0
    for path, data in by_id.values():
        before = json.dumps(data, ensure_ascii=False, sort_keys=True)
        enrich_symbols(data)
        enrich_question(data)
        enrich_lead(data)
        after = json.dumps(data, ensure_ascii=False, sort_keys=True)
        if before != after or True:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            written += 1

    print(f"related filled: {related_n}, cross-links: {cross_n}, files written: {written}")


if __name__ == "__main__":
    main()
