#!/usr/bin/env python3
"""Soften leftover soft-template phrasing across formula JSON files.

Targets:
  - memorize.steps: 'কাজ:' / 'চিহ্ন ঠিক আছে তো?' prefixes
  - derivation steps with identify→substitute latex
  - questions ending with 'সংক্ষেপে কী কাজে লাগে?'
  - very short generic tricks (expand slightly when stubby)
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "subjects"

IDENTIFY_LATEX = re.compile(
    r"\\text\{identify quantities\s*\}\s*\\rightarrow\s*\\text\{\s*substitute\s*\}",
    re.I,
)
SOFT_Q_TAIL = re.compile(r"\s*সংক্ষেপে কী কাজে লাগে\?\s*$")
KAJ_PREFIX = re.compile(r"^কাজ:\s*")
CHINH_PREFIX = re.compile(r"^চিহ্ন ঠিক আছে তো\?\s*")


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def soften_steps(steps: list[str], title_bn: str) -> list[str]:
    out: list[str] = []
    for i, raw in enumerate(steps):
        s = str(raw).strip()
        if KAJ_PREFIX.match(s):
            body = KAJ_PREFIX.sub("", s).strip()
            variants = [
                f"প্রয়োগ: {body}",
                f"মনে রাখো — {body}",
                f"পরীক্ষায়: {body}",
            ]
            s = variants[i % len(variants)]
        elif CHINH_PREFIX.match(s):
            body = CHINH_PREFIX.sub("", s).strip()
            if body:
                s = f"চিহ্ন চেক: {body}"
            else:
                s = f"চিহ্ন ও একক মিলিয়ে নাও — {title_bn}"
        out.append(s)
    return out


def soften_derivation(data: dict) -> bool:
    der = data.get("derivation")
    if not isinstance(der, dict):
        return False
    steps = der.get("steps")
    if not isinstance(steps, list):
        return False
    latex_main = (data.get("latex") or "").strip()
    title_bn = data.get("titleBn") or data.get("title") or "সূত্র"
    changed = False
    for step in steps:
        if not isinstance(step, dict):
            continue
        lx = step.get("latex") or ""
        if not IDENTIFY_LATEX.search(lx):
            continue
        note = (step.get("note") or "").strip()
        step["title"] = step.get("title") or "প্রয়োগের ধাপ"
        step["latex"] = latex_main or r"\text{রাশি চিহ্নিত করো}"
        if not note:
            step["note"] = f"{title_bn} — দেওয়া রাশি বসিয়ে সমাধান করো।"
        elif "identify" in note.lower() or "substitute" in note.lower():
            step["note"] = f"{title_bn}: প্রদত্ত মান বসিয়ে ফলাফল বের করো।"
        # else keep the useful Bangla note already present
        changed = True
    return changed


def soften_questions(data: dict) -> bool:
    qs = data.get("questions")
    if not isinstance(qs, list):
        return False
    title_bn = data.get("titleBn") or data.get("title") or "এই সূত্র"
    latex = (data.get("latex") or "").strip()
    changed = False
    for q in qs:
        if not isinstance(q, dict):
            continue
        question = str(q.get("question") or "")
        if not SOFT_Q_TAIL.search(question):
            continue
        base = SOFT_Q_TAIL.sub("", question).strip()
        # Prefer concrete exam-style prompts
        if "মূল সূত্র কী" in base:
            q["question"] = f"{title_bn} লিখো এবং একটি ব্যবহার উল্লেখ করো।"
        else:
            q["question"] = f"{base} — কখন ব্যবহার করবে?"
        ans = str(q.get("answer") or "").strip()
        if not ans and latex:
            q["answer"] = latex
        changed = True
    return changed


def soften_trick(data: dict) -> bool:
    mem = data.get("memorize")
    if not isinstance(mem, dict):
        return False
    trick = str(mem.get("trick") or "").strip()
    if not trick or len(trick) >= 36:
        return False
    # Already dense one-liners are fine if they look intentional (have math-ish chars)
    if any(ch in trick for ch in ("=", "Δ", "→", "−", "+", "/", "β", "π", "μ")):
        return False
    title_bn = data.get("titleBn") or data.get("title") or "সূত্র"
    mem["trick"] = f"{trick} — {title_bn} মনে রাখার চাবিকাঠি।"
    return True


def process(path: Path) -> bool:
    data = load(path)
    changed = False

    mem = data.get("memorize")
    if isinstance(mem, dict) and isinstance(mem.get("steps"), list):
        title_bn = data.get("titleBn") or data.get("title") or "সূত্র"
        new_steps = soften_steps([str(s) for s in mem["steps"]], title_bn)
        if new_steps != mem["steps"]:
            mem["steps"] = new_steps
            changed = True

    if soften_derivation(data):
        changed = True
    if soften_questions(data):
        changed = True
    if soften_trick(data):
        changed = True

    if changed:
        save(path, data)
    return changed


def main() -> None:
    files = sorted(ROOT.rglob("*.json"))
    n = 0
    for p in files:
        if process(p):
            n += 1
    print(f"softened {n} / {len(files)} formulas")


if __name__ == "__main__":
    main()
