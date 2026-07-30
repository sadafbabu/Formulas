#!/usr/bin/env python3
"""
Upgrade weak memorize + stub summary/symbols/questions across the catalog.

Usage:
  python3 scripts/upgrade-memorize-full.py --subject physics --importance 3
  python3 scripts/upgrade-memorize-full.py --subject chemistry --importance 3
  python3 scripts/upgrade-memorize-full.py --subject math --importance 3
  python3 scripts/upgrade-memorize-full.py --importance 1,2
  python3 scripts/upgrade-memorize-full.py --all
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content" / "subjects"

# Curated high-quality memorize overrides (id -> {trick, steps})
CURATED: dict[str, dict] = {
    "wiens-displacement-law": {
        "trick": "গরম হলে নীলচে (λ ছোট), ঠান্ডা হলে লালচে — λ_max T = ধ্রুবক b।",
        "steps": ["T বাড়লে λ_max কমে", "b ≈ 2.90×10⁻³ m·K", "সূর্য ~5800 K → দৃশ্যমান"],
    },
    "adiabatic-process": {
        "trick": "রুদ্ধতাপীয়: PV^γ ধ্রুব; কাজ W = (P₁V₁−P₂V₂)/(γ−1)।",
        "steps": ["তাপ আদান-প্রদান নেই (Q=0)", "PV^γ, TV^{γ−1} ধ্রুব", "ΔU = −W"],
    },
    "isobaric-isochoric": {
        "trick": "সমআয়তনে কাজ শূন্য; সমচাপে W = PΔV।",
        "steps": ["Isochor: ΔV=0 → W=0", "Isobar: W=PΔV", "ΔU সবসময় nC_vΔT"],
    },
    "area-volume-expansion": {
        "trick": "রৈখিক α → ক্ষেত্র ২α → আয়তন ৩α।",
        "steps": ["ΔL = αLΔT", "β ≈ 2α", "γ ≈ 3α"],
    },
    "heat-conduction": {
        "trick": "তাপ হার Ohm-এর মতো: H = kAΔT/L — A↑ H↑, L↑ H↓।",
        "steps": ["H ∝ A ও ΔT", "H ∝ 1/L", "k = পদার্থের পরিবাহিতা"],
    },
    "static-equilibrium-conditions": {
        "trick": "সাম্যাবস্থা = নেট বল শূন্য + নেট টর্ক শূন্য।",
        "steps": ["ΣF = 0 (স্থানান্তর নেই)", "Στ = 0 (ঘূর্ণন নেই)", "যেকোনো বিন্দু থেকে টর্ক"],
    },
    "stefan-boltzmann-law": {
        "trick": "বিকিরণ ক্ষমতা ∝ T⁴ — দ্বিগুণ তাপমাত্রায় ১৬ গুণ শক্তি।",
        "steps": ["P = σAT⁴", "σ = 5.67×10⁻⁸", "নেট: σA(T⁴−T₀⁴)"],
    },
    "latent-heat": {
        "trick": "দশা বদলে তাপমাত্রা না বাড়লেও Q = mL লাগে।",
        "steps": ["বরফ গলন L_f", "পানি বাষ্প L_v", "Q=mL (ΔT=0)"],
    },
    "newton-cooling": {
        "trick": "ঠান্ডা হওয়ার হার ∝ (T−T₀) — পার্থক্য যত বড় তত দ্রুত।",
        "steps": ["dT/dt = −k(T−T₀)", "বক্ররেখা সূচকীয়", "ছোট পার্থক্যে ধীর"],
    },
}


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, data: dict) -> None:
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_weak_memorize(data: dict) -> bool:
    mem = data.get("memorize") or {}
    trick = (mem.get("trick") or "").strip()
    steps = mem.get("steps") or []
    return (not trick) or len(trick) < 30 or len(steps) < 2


def is_stub_summary(data: dict) -> bool:
    s = (data.get("summary") or "").strip()
    if len(s) < 24:
        return True
    # mostly symbols/operators
    if re.fullmatch(r"[=≈∝A-Za-z0-9\\{}_^+\-−Δλπσμγβα\s./()]+", s):
        return True
    return False


def is_stub_symbols(data: dict) -> bool:
    syms = data.get("symbols") or []
    if not syms:
        return True
    for s in syms:
        if "," in str(s.get("symbol", "")):
            return True
        if s.get("unit") == "সূত্রানুযায়ী":
            return True
    if len(syms) == 1 and len(str(syms[0].get("meaning", ""))) < 8:
        return True
    return False


def is_template_question(data: dict) -> bool:
    qs = data.get("questions") or []
    if not qs:
        return True
    for q in qs:
        text = q.get("question") or ""
        if "সূত্রটি লেখো" in text or "ইঙ্গিত:" in text or len(text.strip()) < 12:
            return True
    return False


def split_symbol_blob(symbol: str, meaning: str, unit: str) -> list[dict]:
    """Split 'Q, m, L' style blobs into separate rows."""
    parts = [p.strip() for p in re.split(r"\s*,\s*", symbol) if p.strip()]
    if len(parts) <= 1:
        return [{"symbol": symbol, "meaning": meaning or symbol, "unit": unit if unit != "সূত্রানুযায়ী" else "—"}]
    # try to split meaning on ; or ,
    meanings = re.split(r"[;|]|,\s*", meaning) if meaning else []
    meanings = [m.strip() for m in meanings if m.strip()]
    out = []
    for i, part in enumerate(parts):
        # skip pure words that look like latex commands leftovers
        if part.lower() in {"tfrac", "dfrac", "text", "mathrm", "left", "right"}:
            continue
        m = meanings[i] if i < len(meanings) else f"{part} সম্পর্কিত রাশি"
        out.append({"symbol": part, "meaning": m, "unit": "—" if unit == "সূত্রানুযায়ী" else unit})
    return out or [{"symbol": symbol, "meaning": meaning or "সূত্রের রাশি", "unit": "—"}]


def extract_latex_symbols(latex: str) -> list[str]:
    """Pull likely symbol tokens from latex for stub repair."""
    cleaned = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", latex)
    cleaned = re.sub(r"\\text\{([^}]*)\}", r"\1", cleaned)
    tokens = re.findall(
        r"\\[A-Za-z]+(?:_\{[^}]+\}|_[A-Za-z0-9]+)?|[A-Za-z](?:_\{[^}]+\}|_[A-Za-z0-9]+)?",
        cleaned,
    )
    skip = {
        "frac",
        "dfrac",
        "tfrac",
        "left",
        "right",
        "cdot",
        "times",
        "approx",
        "quad",
        "qquad",
        "sin",
        "cos",
        "tan",
        "log",
        "ln",
        "exp",
        "sum",
        "prod",
        "int",
        "max",
        "min",
        "const",
        "text",
        "mathrm",
        "mathbf",
        "ce",
    }
    out = []
    for t in tokens:
        base = re.sub(r"^\\", "", t)
        base = re.sub(r"_.*", "", base)
        if base.lower() in skip or len(base) > 12:
            continue
        if t not in out:
            out.append(t)
        if len(out) >= 5:
            break
    return out


def upgrade_memorize(data: dict) -> bool:
    fid = data["id"]
    if fid in CURATED:
        data["memorize"] = {
            "trick": CURATED[fid]["trick"],
            "steps": CURATED[fid]["steps"],
        }
        return True

    mem = dict(data.get("memorize") or {})
    trick = (mem.get("trick") or "").strip()
    steps = list(mem.get("steps") or [])
    title_bn = data.get("titleBn") or data.get("title") or fid
    summary = (data.get("summary") or "").strip()
    latex = (data.get("latex") or "").strip()
    changed = False

    if len(trick) < 30:
        # Expand short trick
        cue = summary if len(summary) >= 20 and not is_stub_summary(data) else latex
        if cue and cue not in trick:
            trick = f"{trick} {cue}".strip() if trick else f"{title_bn}: {cue}"
        if len(trick) < 30:
            trick = f"{title_bn} মনে রাখো — মূল সূত্র প্রয়োগ করো।"
        # trim overly long
        if len(trick) > 160:
            trick = trick[:157] + "…"
        changed = True

    if len(steps) < 2:
        new_steps: list[str] = []
        # Derive simple recall steps
        if latex:
            new_steps.append(f"সূত্র: {latex[:80]}{'…' if len(latex) > 80 else ''}")
        if summary and not is_stub_summary({"summary": summary}):
            new_steps.append(summary[:100])
        else:
            new_steps.append(f"কী কাজে লাগে: {title_bn}")
        # Symbol cue
        syms = data.get("symbols") or []
        if syms:
            names = ", ".join(str(s.get("symbol", "")) for s in syms[:3])
            new_steps.append(f"চিহ্ন মনে রাখো: {names}")
        else:
            new_steps.append("একক ও চিহ্ন মিলিয়ে যাচাই করো")
        # Keep unique, max 4
        cleaned = []
        for s in new_steps:
            s = s.strip()
            if s and s not in cleaned:
                cleaned.append(s)
        steps = cleaned[:4]
        if len(steps) < 2:
            steps = [
                f"{title_bn} এর মূল সম্পর্ক মনে রাখো",
                "প্রশ্নে রাশি চিনে সূত্রে বসাও",
            ]
        changed = True

    if changed:
        data["memorize"] = {"trick": trick, "steps": steps}
    return changed


def upgrade_summary(data: dict) -> bool:
    if not is_stub_summary(data):
        return False
    title_bn = data.get("titleBn") or data.get("title") or data["id"]
    latex = (data.get("latex") or "").strip()
    trick = ((data.get("memorize") or {}).get("trick") or "").strip()
    # Prefer expanding from trick if readable
    if trick and len(trick) >= 24 and not re.fullmatch(r"[=≈A-Za-z0-9\\{}_^+\-−\s]+", trick):
        data["summary"] = trick if len(trick) <= 140 else trick[:137] + "…"
        return True
    if latex:
        data["summary"] = f"{title_bn} — মূল সম্পর্ক: {latex[:90]}{'…' if len(latex) > 90 else ''}"
    else:
        data["summary"] = f"{title_bn} সম্পর্কিত মূল সূত্র ও প্রয়োগ।"
    return True


def upgrade_symbols(data: dict) -> bool:
    if not is_stub_symbols(data):
        return False
    syms = data.get("symbols") or []
    new_syms: list[dict] = []
    if syms and any("," in str(s.get("symbol", "")) for s in syms):
        for s in syms:
            new_syms.extend(
                split_symbol_blob(
                    str(s.get("symbol", "")),
                    str(s.get("meaning", "")),
                    str(s.get("unit", "—")),
                )
            )
    elif syms and any(s.get("unit") == "সূত্রানুযায়ী" for s in syms):
        for s in syms:
            unit = s.get("unit") or "—"
            if unit == "সূত্রানুযায়ী":
                unit = "—"
            meaning = s.get("meaning") or "সূত্রের রাশি"
            if "," in str(s.get("symbol", "")):
                new_syms.extend(split_symbol_blob(str(s["symbol"]), str(meaning), unit))
            else:
                new_syms.append({"symbol": s.get("symbol", "?"), "meaning": meaning, "unit": unit})
    else:
        # generate from latex
        tokens = extract_latex_symbols(data.get("latex") or "")
        for t in tokens:
            new_syms.append({"symbol": t, "meaning": f"{t} রাশি", "unit": "—"})
        if not new_syms and syms:
            new_syms = [
                {
                    "symbol": str(syms[0].get("symbol", "x")),
                    "meaning": str(syms[0].get("meaning") or "মূল রাশি"),
                    "unit": "—",
                }
            ]
        elif not new_syms:
            new_syms = [{"symbol": "x", "meaning": "সূত্রের মূল রাশি", "unit": "—"}]

    # dedupe by symbol
    seen = set()
    deduped = []
    for s in new_syms:
        key = s["symbol"]
        if key in seen:
            continue
        seen.add(key)
        deduped.append(s)
    data["symbols"] = deduped[:8]
    return True


def upgrade_questions(data: dict) -> bool:
    if not is_template_question(data):
        return False
    title_bn = data.get("titleBn") or data.get("title") or data["id"]
    latex = (data.get("latex") or "").strip()
    answer = latex if latex else title_bn
    # Keep existing non-template if any; else replace
    qs = [
        q
        for q in (data.get("questions") or [])
        if q.get("question")
        and "সূত্রটি লেখো" not in q["question"]
        and "ইঙ্গিত:" not in q["question"]
        and len(q["question"].strip()) >= 12
    ]
    if not qs:
        qs = [
            {
                "examType": "HSC / Admission",
                "question": f"{title_bn} কখন ব্যবহার করবে? মূল সম্পর্ক কী?",
                "answer": answer[:200],
            }
        ]
    data["questions"] = qs
    return True


def upgrade_derivation(data: dict) -> bool:
    der = data.get("derivation") or {}
    steps = list(der.get("steps") or [])
    lead = (der.get("lead") or "").strip()
    assumptions = der.get("assumptions")
    if not isinstance(assumptions, list):
        assumptions = []
    changed = False
    title_bn = data.get("titleBn") or data.get("title") or data["id"]
    latex = (data.get("latex") or "").strip()
    summary = (data.get("summary") or "").strip()

    if len(lead) < 30:
        lead = summary if len(summary) >= 30 else f"{title_bn} এর মূল সম্পর্ক ও প্রয়োগ।"
        changed = True

    # Normalize steps to title/latex/note
    norm_steps = []
    for st in steps:
        if not isinstance(st, dict):
            continue
        title = st.get("title") or "ধাপ"
        lx = st.get("latex") or ""
        note = st.get("note") or st.get("body") or ""
        if not lx and note and re.search(r"[\\^_{}]", note):
            # body held latex
            lx = note
            note = st.get("note") if st.get("body") else title_bn
        if not lx:
            lx = latex or r"\text{" + title_bn[:40] + "}"
        if not note:
            note = "সূত্র প্রয়োগের ধাপ।"
        norm_steps.append({"title": title, "latex": lx, "note": note})

    if len(norm_steps) < 2:
        norm_steps = [
            {
                "title": "মূল সূত্র",
                "latex": latex or r"\text{" + title_bn[:40] + "}",
                "note": lead[:120] if lead else f"{title_bn} এর মূল রূপ।",
            },
            {
                "title": "প্রয়োগ",
                "latex": latex or r"\text{apply}",
                "note": "রাশি চিনে সূত্রে বসাও; একক মিলিয়ে যাচাই করো।",
            },
        ]
        changed = True
    elif steps != norm_steps:
        changed = True

    if changed:
        data["derivation"] = {
            "lead": lead,
            "steps": norm_steps,
            "assumptions": assumptions,
        }
    return changed


def iter_formulas():
    for p in sorted(ROOT.rglob("formulas/*.json")):
        yield p, load(p)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--subject", choices=["physics", "chemistry", "math"])
    ap.add_argument("--importance", default="", help="e.g. 3 or 1,2")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    imp_set = None
    if args.importance:
        imp_set = {int(x) for x in args.importance.split(",") if x.strip()}

    updated = 0
    touched_ids = []
    for path, data in iter_formulas():
        subject = path.parts[-4] if path.parts[-3] == "chapters" else path.parts[-5]
        # path: subjects/<subj>/chapters/<ch>/formulas/<id>.json
        subject = path.relative_to(ROOT).parts[0]
        if args.subject and subject != args.subject:
            continue
        imp = data.get("importance", 2)
        if imp_set is not None and imp not in imp_set:
            continue
        if not args.all and imp_set is None and not args.subject:
            print("Specify --subject/--importance or --all")
            return

        changed = False
        if is_weak_memorize(data):
            changed |= upgrade_memorize(data)
        if is_stub_summary(data):
            changed |= upgrade_summary(data)
        if is_stub_symbols(data):
            changed |= upgrade_symbols(data)
        if is_template_question(data):
            changed |= upgrade_questions(data)
        # Always normalize weak derivation for selected set
        der = data.get("derivation") or {}
        if len(der.get("steps") or []) < 2 or len((der.get("lead") or "").strip()) < 30:
            changed |= upgrade_derivation(data)
        # Also fix derivation step shape if body-only
        elif any("body" in (st or {}) and "latex" not in (st or {}) for st in der.get("steps") or []):
            changed |= upgrade_derivation(data)

        # Ensure star tag matches importance
        tags = [t for t in data.get("tags", []) if not str(t).endswith("-star")]
        star = f"{imp}-star"
        if star not in tags:
            tags.append(star)
            data["tags"] = tags
            changed = True
        else:
            # ensure only one star tag
            data["tags"] = [t for t in tags if not str(t).endswith("-star")] + [star]

        if changed:
            updated += 1
            touched_ids.append(data["id"])
            if not args.dry_run:
                save(path, data)

    print(f"Updated {updated} formulas" + (" (dry-run)" if args.dry_run else ""))
    if updated and updated <= 40:
        print("ids:", ", ".join(touched_ids))


if __name__ == "__main__":
    main()
