#!/usr/bin/env python3
"""Chemistry structural polish — correct app schema only.

Schema rules (from src/data/types.ts + validate-content.mjs):
- chapter must match folder name and catalog.ts
- tags: only hsc/eng-admission/medical/varsity/{1,2,3}-star
- importance: 1|2|3
- derivation: {lead, steps:[{title,latex,note}], assumptions:[]}
- memorize: {trick, steps?}
- questions: [{examType, question, answer}] — answer is bare KaTeX (no \\( \\))
- symbols: [{symbol, meaning, unit}]
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHEM = ROOT / "content" / "subjects" / "chemistry" / "chapters"
STD_TAGS = ["hsc", "eng-admission", "medical", "varsity"]


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def save(p: Path, data: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_formula(chapter: str, data: dict) -> None:
    data = {**data, "chapter": chapter, "subjects": ["chemistry"]}
    save(CHEM / chapter / "formulas" / f"{data['id']}.json", data)


def fix_fragmented_answers() -> None:
    patches = {
        "functional-groups": {
            "answer": r"\ce{-COOH}\ \text{কার্বক্সিলিক অম্ল গোষ্ঠী};\ \text{৩ কার্বন শৃঙ্খল}\ \Rightarrow\ \text{প্রোপানয়িক অম্ল (propanoic acid)}"
        },
        "lewis-structure": {
            "answer": r"\ce{O=C=O}\text{ — কার্বনে নিঃসঙ্গ জোড় নেই, ২টি দ্বিবন্ধন (৪টি বন্ধন জোড়া), রৈখিক আকৃতি, বন্ধন কোণ }180^\circ"
        },
    }
    for fid, patch in patches.items():
        matches = list(CHEM.glob(f"*/formulas/{fid}.json"))
        if not matches:
            print("missing", fid)
            continue
        data = load(matches[0])
        for q in data.get("questions", []):
            for k, v in patch.items():
                if k in q or k == "answer":
                    q["answer"] = patch["answer"]
        save(matches[0], data)
        print("fixed answer", fid)


def improve_organic_existing() -> None:
    patches = {
        "functional-groups": {
            "latex": r"\ce{-OH},\;\ce{-CHO},\;\ce{>C=O},\;\ce{-COOH},\;\ce{-NH2},\;\ce{-X}",
            "summary": "ফাংশনাল গোষ্ঠী যৌগের রাসায়নিক ধর্ম নির্ধারণ করে—অ্যালকোহল, অ্যালডিহাইড, কিটোন, অ্যাসিড, অ্যামাইন, হ্যালাইড।",
            "related": [
                "structural-condensed-formula",
                "homologous-series",
                "iupac-naming-rules",
                "bond-line-formula",
                "isomerism",
                "sn1-sn2-mechanism",
            ],
        },
        "isomerism": {
            "latex": r"\text{same MF, different structure/arrangement}",
            "summary": "একই আণবিক সংকেত, ভিন্ন গঠন বা বিন্যাস—চেইন, অবস্থান, ফাংশনাল, জ্যামিতিক, আলোকীয়।",
            "related": [
                "functional-groups",
                "structural-condensed-formula",
                "homologous-series",
                "hydrocarbon-general-formula",
                "sn1-sn2-mechanism",
            ],
        },
        "hybridization-shapes": {
            "latex": r"sp^3\ \text{tetrahedral},\ sp^2\ \text{trigonal planar},\ sp\ \text{linear}",
            "summary": "হাইব্রিডাইজেশন থেকে আকৃতি: sp³ টেট্রাহেড্রাল, sp² ত্রিভুজাকার সমতল, sp সরলরেখিক।",
        },
        "lewis-structure": {
            "latex": r"\text{valence }e^- =\text{ group number (main group)};\ \text{octet}=8",
            "summary": "লুইস কাঠামোতে যোজ্যতা ইলেকট্রন জোড় ও অষ্টক নিয়ম দিয়ে বন্ধন আঁকা হয়।",
            "related": [
                "hybridization-shapes",
                "formal-charge",
                "vsepr-theory",
                "structural-condensed-formula",
            ],
        },
        "sn1-sn2-mechanism": {
            "latex": r"\mathrm{S_N1}:\ \mathrm{rate}=k[\mathrm{RX}]\qquad \mathrm{S_N2}:\ \mathrm{rate}=k[\mathrm{RX}][\mathrm{Nu}]",
            "summary": "SN1: একঅণুক, কার্বোক্যাটায়ন, রেসিমাইজেশন। SN2: দ্বিঅণুক, পশ্চাদপসরণ, ইনভার্শন।",
            "importance": 3,
            "tags": STD_TAGS + ["3-star"],
            "derivation": {
                "lead": "নিউক্লিওফিলিক প্রতিস্থাপনের দুই প্রধান পথ SN1 ও SN2—হার সমীকরণ ও স্টেরিওরসায়ন আলাদা।",
                "steps": [
                    {
                        "title": "SN1 (unimolecular)",
                        "latex": r"\mathrm{rate}=k[\mathrm{RX}]",
                        "note": "ধীর ধাপ: RX ভেঙে কার্বোক্যাটায়ন; ৩° > ২° > ১°; পোলার প্রোটিক দ্রাবক; প্রায় রেসিমিক মিশ্রণ।",
                    },
                    {
                        "title": "SN2 (bimolecular)",
                        "latex": r"\mathrm{rate}=k[\mathrm{RX}][\mathrm{Nu}]",
                        "note": "এক ধাপে Nu পেছন থেকে আক্রমণ; ১° > ২° > ৩°; পোলার অ্যাপ্রোটিক; Walden inversion।",
                    },
                ],
                "assumptions": ["প্রতিযোগী elimination উপেক্ষা; সাধারণ অ্যালকাইল হ্যালাইড"],
            },
            "questions": [
                {
                    "examType": "HSC / Medical",
                    "question": r"মিথাইল হ্যালাইডে কোন পথ দ্রুত — SN1 না SN2? হার সূত্র কী?",
                    "answer": r"\text{SN2 দ্রুত; }\mathrm{rate}=k[\mathrm{RX}][\mathrm{Nu}]",
                },
                {
                    "examType": "Admission",
                    "question": r"৩° অ্যালকাইল হ্যালাইডে SN1 প্রাধান্য পায় কেন?",
                    "answer": r"\text{৩° কার্বোক্যাটায়ন স্থিতিশীল; SN1 হার কেবল }[\mathrm{RX}]\text{ নির্ভর}",
                },
            ],
            "memorize": {
                "trick": "SN1 = ৩° + কার্বোক্যাটায়ন; SN2 = ১° + পেছন আক্রমণ। সংখ্যাটাই ক্রম।",
                "steps": [
                    "SN1: rate = k[RX]; ৩° > ২° > ১°",
                    "SN2: rate = k[RX][Nu]; ১° > ২° > ৩°",
                    "প্রোটিক → SN1; অ্যাপ্রোটিক → SN2",
                ],
            },
            "related": [
                "functional-groups",
                "isomerism",
                "markovnikov-rule",
                "elimination-e1",
                "elimination-e2",
            ],
        },
    }
    all_ids = {p.stem for p in CHEM.glob("*/formulas/*.json")}
    for fid, patch in patches.items():
        matches = list(CHEM.glob(f"*/formulas/{fid}.json"))
        if not matches:
            print("missing", fid)
            continue
        data = load(matches[0])
        for k, v in patch.items():
            if k == "related":
                data["related"] = [r for r in v if r in all_ids or r in patches]
            else:
                data[k] = v
        # ensure star tag matches importance
        imp = data.get("importance", 3)
        data["tags"] = [t for t in data.get("tags", STD_TAGS) if not str(t).endswith("-star")]
        if not any(t in data["tags"] for t in STD_TAGS):
            data["tags"] = list(STD_TAGS)
        data["tags"] = [t for t in data["tags"] if not str(t).endswith("-star")]
        data["tags"].append(f"{imp}-star")
        save(matches[0], data)
        print("improved", fid)


def add_structural_cards() -> None:
    # remove wrong-folder leftovers if any
    bad = CHEM / "organic-chemistry"
    if bad.exists():
        shutil.rmtree(bad)
        print("removed", bad)

    cards = [
        {
            "id": "structural-condensed-formula",
            "title": "Structural & Condensed Formula",
            "titleBn": "গঠনিক ও সংক্ষিপ্ত সংকেত",
            "latex": r"\mathrm{CH_3CH_2OH}\ \equiv\ \mathrm{C_2H_5OH}\ \equiv\ \text{ethanol}",
            "summary": "গঠনিক সংকেত পরমাণুর সংযোগ দেখায়; condensed formula শিকল সংক্ষেপে লেখে—আইসোমার আলাদা করতে অপরিহার্য।",
            "tags": STD_TAGS + ["3-star"],
            "importance": 3,
            "order": 15,
            "symbols": [
                {"symbol": r"\mathrm{CH_3-}", "meaning": "মিথাইল গোষ্ঠী", "unit": "—"},
                {"symbol": r"\mathrm{-OH}", "meaning": "হাইড্রক্সিল গোষ্ঠী", "unit": "—"},
                {"symbol": "MF", "meaning": "আণবিক সংকেত (শুধু পরমাণু সংখ্যা)", "unit": "—"},
            ],
            "derivation": {
                "lead": "অর্গানিক রসায়নে একই যৌগ তিনভাবে লেখা যায়—molecular, structural, condensed।",
                "steps": [
                    {
                        "title": "Molecular formula",
                        "latex": r"\mathrm{C_2H_6O}",
                        "note": "শুধু পরমাণুর সংখ্যা—ইথানল ও ডাইমিথাইল ইথার একই MF!",
                    },
                    {
                        "title": "Structural formula",
                        "latex": r"\mathrm{CH_3{-}CH_2{-}OH}",
                        "note": "প্রতিটি বন্ধন দেখায়; connectivity স্পষ্ট।",
                    },
                    {
                        "title": "Condensed formula",
                        "latex": r"\mathrm{CH_3CH_2OH}\ \text{or}\ \mathrm{C_2H_5OH}",
                        "note": "শিকল গোষ্ঠী একত্রে লেখা—দ্রুত ও পরীক্ষায় সুবিধাজনক।",
                    },
                ],
                "assumptions": ["আইসোমার আলাদা করতে MF যথেষ্ট নয়"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"ইথানলের condensed সংকেত কী?",
                    "answer": r"\mathrm{CH_3CH_2OH}\ \text{বা}\ \mathrm{C_2H_5OH}",
                },
                {
                    "examType": "Admission",
                    "question": r"কেন \(\mathrm{C_2H_6O}\) দিয়ে যৌগের নাম নিশ্চিত করা যায় না?",
                    "answer": r"\text{আইসোমার: ইথানল }\mathrm{CH_3CH_2OH}\text{ ও ডাইমিথাইল ইথার }\mathrm{CH_3OCH_3}",
                },
            ],
            "memorize": {
                "trick": "Molecular = কী আছে; Structural = কীভাবে জোড়া; Condensed = ছোট করে লেখা।",
                "steps": [
                    "MF শুধু সংখ্যা দেয়",
                    "Structural connectivity দেখায়",
                    "Condensed = পরীক্ষার ছোট লেখা",
                ],
            },
            "related": [
                "functional-groups",
                "isomerism",
                "homologous-series",
                "bond-line-formula",
                "iupac-naming-rules",
            ],
        },
        {
            "id": "homologous-series",
            "title": "Homologous Series",
            "titleBn": "সমগোত্রীয় শ্রেণি",
            "latex": r"\mathrm{C_nH_{2n+2}}\ (\text{alkane}),\quad \Delta=\mathrm{CH_2}",
            "summary": r"সমগোত্রীয় শ্রেণিতে পরপর সদস্যদের মধ্যে \(\mathrm{CH_2}\) পার্থক্য; একই ফাংশনাল গোষ্ঠী ও সাধারণ সূত্র।",
            "tags": STD_TAGS + ["3-star"],
            "importance": 3,
            "order": 16,
            "symbols": [
                {"symbol": "n", "meaning": "কার্বন সংখ্যা", "unit": "—"},
                {"symbol": r"\mathrm{CH_2}", "meaning": "মিথিলিন গোষ্ঠী (শ্রেণি ব্যবধান)", "unit": "—"},
            ],
            "derivation": {
                "lead": "একই ফাংশনাল গোষ্ঠী ও সাধারণ সূত্রের যৌগসমূহ সমগোত্রীয় শ্রেণি গঠন করে।",
                "steps": [
                    {
                        "title": "Alkane / Alkene / Alkyne",
                        "latex": r"\mathrm{C_nH_{2n+2}},\ \mathrm{C_nH_{2n}},\ \mathrm{C_nH_{2n-2}}",
                        "note": r"পরপর সদস্যে ব্যবধান সবসময় \(\mathrm{CH_2}\)।",
                    },
                    {
                        "title": "Alcohol",
                        "latex": r"\mathrm{C_nH_{2n+1}OH}",
                        "note": r"\(\mathrm{CH_3OH},\ \mathrm{C_2H_5OH},\ \mathrm{C_3H_7OH},\ldots\)",
                    },
                    {
                        "title": "ধর্ম",
                        "latex": r"\text{chem. similar};\ \text{bp/mp rise with }n",
                        "note": r"রাসায়নিক ধর্ম সাদৃশ্য; ভৌত ধর্ম \(\mathrm{CH_2}\) যোগে ধীরে বাড়ে।",
                    },
                ],
                "assumptions": ["খোলা শিকল হাইড্রোকার্বন/অ্যালকোহল শ্রেণি"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"অ্যালকেনের সাধারণ সূত্র কী?",
                    "answer": r"\mathrm{C_nH_{2n+2}}",
                },
                {
                    "examType": "Admission",
                    "question": r"\(\mathrm{C_3H_7OH}\) এর পরবর্তী সমগোত্র কোনটি?",
                    "answer": r"\mathrm{C_4H_9OH}\ (\mathrm{CH_2}\ \text{যোগ})",
                },
            ],
            "memorize": {
                "trick": "Alkane 2n+2, Alkene 2n, Alkyne 2n−2; ব্যবধান সবসময় CH₂।",
                "steps": ["সাধারণ সূত্র মনে রাখো", "পরের সদস্য = +CH₂", "একই ফাংশনাল গোষ্ঠী"],
            },
            "related": [
                "structural-condensed-formula",
                "functional-groups",
                "hydrocarbon-general-formula",
                "iupac-naming-rules",
            ],
        },
        {
            "id": "hydrocarbon-general-formula",
            "title": "Hydrocarbon General Formulas",
            "titleBn": "হাইড্রোকার্বনের সাধারণ সূত্র",
            "latex": r"\text{alkane }\mathrm{C_nH_{2n+2}},\ \text{alkene }\mathrm{C_nH_{2n}},\ \text{alkyne }\mathrm{C_nH_{2n-2}}",
            "summary": "অ্যালকেন/অ্যালকিন/অ্যালকাইনের সাধারণ সূত্র—অসম্পৃক্ততা ও H-সংখ্যা নির্ণয়ে।",
            "tags": STD_TAGS + ["3-star"],
            "importance": 3,
            "order": 17,
            "symbols": [
                {"symbol": "n", "meaning": "কার্বন সংখ্যা (≥1 alkane; ≥2 alkene/alkyne)", "unit": "—"},
                {"symbol": "DU", "meaning": "degree of unsaturation (আনুমানিক)", "unit": "—"},
            ],
            "derivation": {
                "lead": "খোলা শিকল হাইড্রোকার্বনের H-সংখ্যা দ্বিবন্ধন/ত্রিবন্ধন অনুযায়ী কমে।",
                "steps": [
                    {
                        "title": "Alkane (সম্পৃক্ত)",
                        "latex": r"\mathrm{C_nH_{2n+2}}",
                        "note": "শুধু একক বন্ধন—সর্বোচ্চ H।",
                    },
                    {
                        "title": "Alkene / Alkyne",
                        "latex": r"\mathrm{C_nH_{2n}}\ /\ \mathrm{C_nH_{2n-2}}",
                        "note": "এক দ্বিবন্ধনে ২ H কম; এক ত্রিবন্ধনে ৪ H কম।",
                    },
                    {
                        "title": "Degree of unsaturation",
                        "latex": r"\mathrm{DU}=\dfrac{2n+2-H}{2}",
                        "note": "heteroatom থাকলে আলাদা হিসাব লাগে।",
                    },
                ],
                "assumptions": ["খোলা শিকল; এক দ্বি/ত্রিবন্ধন"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"৪ কার্বন অ্যালকাইনের সূত্র?",
                    "answer": r"\mathrm{C_4H_6}",
                },
                {
                    "examType": "Admission",
                    "question": r"\(\mathrm{C_5H_{10}}\) কোন শ্রেণি?",
                    "answer": r"\text{অ্যালকিন }(\mathrm{C_nH_{2n}})",
                },
            ],
            "memorize": {
                "trick": "+2 saturated; 2n এক দ্বিবন্ধন; 2n−2 এক ত্রিবন্ধন।",
                "steps": ["2n+2 = alkane", "2n = alkene", "2n−2 = alkyne"],
            },
            "related": ["homologous-series", "structural-condensed-formula", "isomerism"],
        },
        {
            "id": "bond-line-formula",
            "title": "Bond-line (Skeletal) Formula",
            "titleBn": "বন্ধন-রেখা / কঙ্কাল সংকেত",
            "latex": r"\text{zigzag line}\ \equiv\ \mathrm{C{-}C}\ \text{chain (H hidden)}",
            "summary": "কোণ = কার্বন; রেখা = বন্ধন; H সাধারণত দেখানো হয় না—দ্রুত অর্গানিক অঙ্কন।",
            "tags": STD_TAGS + ["3-star"],
            "importance": 3,
            "order": 18,
            "symbols": [
                {"symbol": "vertex", "meaning": "কার্বন পরমাণু", "unit": "—"},
                {"symbol": "line end", "meaning": r"মিথাইল \(\mathrm{CH_3}\)", "unit": "—"},
            ],
            "derivation": {
                "lead": "Bond-line formula-তে শুধু C–C কঙ্কাল আঁকা হয়; H অনুমান করা হয়।",
                "steps": [
                    {
                        "title": "নিয়ম",
                        "latex": r"\text{each bend/end}=C;\ \text{H fills valence to }4",
                        "note": "প্রতিটি কোণ ও রেখার প্রান্তে একটি C।",
                    },
                    {
                        "title": "উদাহরণ",
                        "latex": r"\text{pentane zigzag}\ \Rightarrow\ \mathrm{C_5H_{12}}",
                        "note": "৫টি কোণ/প্রান্ত = ৫ কার্বন।",
                    },
                    {
                        "title": "ফাংশনাল গোষ্ঠী",
                        "latex": r"\mathrm{O},\,\mathrm{N},\,\mathrm{Cl}\ \text{shown};\ \text{double/triple drawn}",
                        "note": "heteroatom ও বহুবন্ধন স্পষ্ট লিখতে হয়।",
                    },
                ],
                "assumptions": ["কার্বনের যোজ্যতা ৪"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"Bond-line-এ প্রতিটি বাঁক কী নির্দেশ করে?",
                    "answer": r"\text{একটি কার্বন পরমাণু}",
                },
                {
                    "examType": "Admission",
                    "question": r"হেক্সেনের skeletal শিকলে কয়টি C?",
                    "answer": r"6",
                },
            ],
            "memorize": {
                "trick": "কোণ = C, প্রান্ত = C, H লুকানো; heteroatom দেখাও।",
                "steps": ["Bend = carbon", "H is silent", "Show O/N/X"],
            },
            "related": [
                "structural-condensed-formula",
                "functional-groups",
                "hybridization-shapes",
            ],
        },
        {
            "id": "iupac-naming-rules",
            "title": "IUPAC Naming (Basics)",
            "titleBn": "IUPAC নামকরণ (মৌলিক)",
            "latex": r"\text{prefix}+\text{root}+\text{suffix}\ (\text{e.g. 2-methylbutane})",
            "summary": "দীর্ঘতম শিকল = root; ফাংশনাল গোষ্ঠী = suffix; সাবস্টিটুয়েন্ট = prefix; সর্বনিম্ন সংখ্যা।",
            "tags": STD_TAGS + ["3-star"],
            "importance": 3,
            "order": 19,
            "symbols": [
                {"symbol": "root", "meaning": "প্রধান শিকল (meth, eth, prop…)", "unit": "—"},
                {"symbol": "suffix", "meaning": "-ane / -ene / -ol / -oic acid…", "unit": "—"},
                {"symbol": "prefix", "meaning": "alkyl, halo ইত্যাদি", "unit": "—"},
            ],
            "derivation": {
                "lead": "IUPAC নাম তিন অংশে: prefix (শাখা) + root (শিকল) + suffix (মূল গোষ্ঠী)।",
                "steps": [
                    {
                        "title": "দীর্ঘতম শিকল",
                        "latex": r"\text{longest chain with functional group}",
                        "note": "ফাংশনাল গোষ্ঠীসহ সবচেয়ে বড় C-শিকল বেছে নাও।",
                    },
                    {
                        "title": "সংখ্যায়ন",
                        "latex": r"\text{lowest set of locants}",
                        "note": "ফাংশনাল গোষ্ঠী/দ্বিবন্ধন সর্বনিম্ন নম্বর পায়।",
                    },
                    {
                        "title": "উদাহরণ",
                        "latex": r"\mathrm{CH_3CH(CH_3)CH_2CH_3}\ \rightarrow\ \text{2-methylbutane}",
                        "note": "prefix alphabetical; di/tri গণনায় উপেক্ষা।",
                    },
                ],
                "assumptions": ["মৌলিক খোলা-শিকল যৌগ"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"অ্যালকোহলের IUPAC suffix কী?",
                    "answer": r"\text{-ol}",
                },
                {
                    "examType": "Admission",
                    "question": r"\(\mathrm{CH_3CH_2CH_3}\) এর IUPAC নাম?",
                    "answer": r"\text{propane / প্রোপেন}",
                },
            ],
            "memorize": {
                "trick": "Longest chain → number low → prefixes ABC → suffix for main group।",
                "steps": ["Find chain", "Number low", "Name the rest"],
            },
            "related": [
                "functional-groups",
                "homologous-series",
                "structural-condensed-formula",
                "isomerism",
            ],
        },
    ]

    existing = {p.stem for p in CHEM.glob("*/formulas/*.json")}
    for card in cards:
        if card["id"] in existing:
            # overwrite with correct schema in right chapter
            pass
        write_formula("organic-chem", card)
        existing.add(card["id"])
        print("wrote", card["id"])


def polish_stubs() -> None:
    """Upgrade weak 3-star stubs with real details (correct schema)."""
    upgrades: dict[str, dict] = {
        "raoult-law": {
            "latex": r"p_A = x_A\,p_A^\circ",
            "summary": "রাউল্টের সূত্র: দ্রবণে উদ্বায়ী উপাদানের আংশিক চাপ = মোল ভগ্নাংশ × বিশুদ্ধ বাষ্পচাপ।",
            "symbols": [
                {"symbol": r"p_A", "meaning": "A-এর আংশিক বাষ্পচাপ", "unit": "Pa"},
                {"symbol": r"x_A", "meaning": "দ্রবণে A-এর মোল ভগ্নাংশ", "unit": "1"},
                {"symbol": r"p_A^\circ", "meaning": "বিশুদ্ধ A-এর বাষ্পচাপ", "unit": "Pa"},
            ],
            "derivation": {
                "lead": "আদর্শ দ্রবণে প্রতিটি উদ্বায়ী উপাদানের বাষ্পচাপ তার মোল ভগ্নাংশের সমানুপাতিক।",
                "steps": [
                    {
                        "title": "আংশিক চাপ",
                        "latex": r"p_A = x_A p_A^\circ",
                        "note": r"বিশুদ্ধ তরলের বাষ্পচাপ \(p^\circ\); দ্রবণে কমে যায়।",
                    },
                    {
                        "title": "মোট চাপ (দ্বৈত)",
                        "latex": r"p_{\mathrm{total}} = x_A p_A^\circ + x_B p_B^\circ",
                        "note": r"অস্থায়ী দ্রবে \(p = x_{\mathrm{solvent}} p^\circ\) (বাষ্পচাপ হ্রাস)।",
                    },
                ],
                "assumptions": ["আদর্শ দ্রবণ", "ধ্রুব তাপমাত্রা"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"\(x_A=0.4\), \(p_A^\circ=2\,\mathrm{kPa}\) হলে \(p_A\)?",
                    "answer": r"0.8\,\mathrm{kPa}",
                },
                {
                    "examType": "Admission",
                    "question": r"আদর্শ দ্বৈত মিশ্রণে মোট বাষ্পচাপের সূত্র?",
                    "answer": r"p_{\mathrm{total}}=x_A p_A^\circ+x_B p_B^\circ",
                },
            ],
            "memorize": {
                "trick": "আংশিক চাপ = মোল ভাগ × বিশুদ্ধ চাপ (p = x · p°)।",
                "steps": ["x বের করো", "বিশুদ্ধ p° দিয়ে গুণ", "সব উদ্বায়ীর যোগফল = মোট p"],
            },
            "related": ["osmotic-pressure", "relative-lowering-vapour-pressure", "henrys-law"],
        },
        "osmotic-pressure": {
            "latex": r"\Pi = cRT = \dfrac{n}{V}RT",
            "summary": r"অসমোটিক চাপ \(\Pi=cRT\); তনু দ্রবণের মোলার গণনায় ব্যবহৃত।",
            "symbols": [
                {"symbol": r"\Pi", "meaning": "অসমোটিক চাপ", "unit": "Pa"},
                {"symbol": "c", "meaning": "মোলার ঘনমাত্রা", "unit": "mol m⁻³ বা mol L⁻¹"},
                {"symbol": "R", "meaning": "গ্যাস ধ্রুবক", "unit": "J/(mol·K) বা L·atm/(mol·K)"},
                {"symbol": "T", "meaning": "পরম তাপমাত্রা", "unit": "K"},
            ],
            "derivation": {
                "lead": "অর্ধভেদ্য পর্দার দুই পাশে দ্রবণ–দ্রবকের চাপ পার্থক্যই অসমোটিক চাপ—van 't Hoff সূত্র।",
                "steps": [
                    {
                        "title": "van 't Hoff",
                        "latex": r"\Pi V = nRT",
                        "note": "তনু দ্রবণে আদর্শ গ্যাসের মতো আচরণ।",
                    },
                    {
                        "title": "ঘনমাত্রা রূপ",
                        "latex": r"\Pi = cRT,\quad c=n/V",
                        "note": r"মোলার ভর: \(M=\dfrac{wRT}{\Pi V}\)।",
                    },
                ],
                "assumptions": ["তনু দ্রবণ", "অর্ধভেদ্য পর্দা আদর্শ"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"\(c=0.1\,\mathrm{mol\,L^{-1}}\), \(T=300\,\mathrm{K}\), \(R=0.082\,\mathrm{L\,atm\,K^{-1}\,mol^{-1}}\) হলে \(\Pi\)?",
                    "answer": r"2.46\,\mathrm{atm}",
                }
            ],
            "memorize": {
                "trick": "অসমোসিস ≈ আদর্শ গ্যাস: ΠV = nRT → Π = cRT।",
                "steps": ["c বা n/V নাও", "T কেলভিনে", "Π = cRT"],
            },
            "related": ["raoult-law", "molarity-molality", "vant-hoff-factor"],
        },
        "mole-concept-basic": {
            "latex": r"n = \dfrac{m}{M} = \dfrac{N}{N_A}",
            "summary": r"মোল সংখ্যা = ভর/মোলার ভর = কণা সংখ্যা/\(N_A\)।",
            "symbols": [
                {"symbol": "n", "meaning": "মোল সংখ্যা", "unit": "mol"},
                {"symbol": "m", "meaning": "ভর", "unit": "g"},
                {"symbol": "M", "meaning": "মোলার ভর", "unit": "g/mol"},
                {"symbol": "N", "meaning": "কণা সংখ্যা", "unit": "1"},
                {
                    "symbol": r"N_A",
                    "meaning": r"অ্যাভোগাড্রো সংখ্যা \(6.022\times10^{23}\,\mathrm{mol^{-1}}\)",
                    "unit": "mol⁻¹",
                },
            ],
            "derivation": {
                "lead": r"১ মোল = \(N_A\)টি কণা; ভরের সাথে যোগসূত্র মোলার ভর।",
                "steps": [
                    {
                        "title": "ভর থেকে মোল",
                        "latex": r"n = m/M",
                        "note": "গ্রাম ÷ গ্রাম/মোল।",
                    },
                    {
                        "title": "কণা থেকে মোল",
                        "latex": r"n = N/N_A",
                        "note": r"STP আনুমানিক: \(n=V/22.4\,\mathrm{L}\) (পুরনো STP)।",
                    },
                ],
                "assumptions": [],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"\(18\,\mathrm{g}\) পানিতে কত মোল? (\(M=18\))",
                    "answer": r"1\,\mathrm{mol}",
                },
                {
                    "examType": "Admission",
                    "question": r"\(0.5\,\mathrm{mol}\)-এ অণু সংখ্যা?",
                    "answer": r"3.011\times10^{23}",
                },
            ],
            "memorize": {
                "trick": "মোল সেতু: ভর ↔ মোল ↔ কণা (m/M = N/N_A = n)।",
                "steps": ["ভর÷M", "কণা÷N_A", "দুটোই মোল"],
            },
            "related": [
                "molarity-molality",
                "mole-avogadro",
                "empirical-molecular-formula",
                "percentage-composition",
            ],
        },
        "molarity-molality": {
            "latex": r"M=\dfrac{n}{V_{\mathrm{L}}},\quad m=\dfrac{n}{w_{\mathrm{kg}}}",
            "summary": "মোলারিটি = মোল/লিটার দ্রবণ (T-নির্ভর); মোলালিটি = মোল/কেজি দ্রবক (T-স্বাধীন)।",
            "symbols": [
                {"symbol": "M", "meaning": "মোলারিটি", "unit": "mol/L"},
                {"symbol": "m", "meaning": "মোলালিটি", "unit": "mol/kg"},
                {"symbol": "n", "meaning": "দ্রবের মোল", "unit": "mol"},
            ],
            "derivation": {
                "lead": "ঘনমাত্রার দুই প্রধান একক—আয়তনভিত্তিক (M) ও ভরভিত্তিক (m)।",
                "steps": [
                    {
                        "title": "Molarity",
                        "latex": r"M = n_{\mathrm{solute}}/V_{\mathrm{solution}}(\mathrm{L})",
                        "note": r"পাতলাকরণ: \(M_1V_1=M_2V_2\)।",
                    },
                    {
                        "title": "Molality",
                        "latex": r"m = n_{\mathrm{solute}}/w_{\mathrm{solvent}}(\mathrm{kg})",
                        "note": "কলেগেটিভ ধর্মে সুবিধাজনক—ভর তাপমাত্রায় বদলায় না।",
                    },
                ],
                "assumptions": [],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"\(0.5\,\mathrm{mol}\) দ্রব \(2\,\mathrm{L}\) দ্রবণে—মোলারিটি?",
                    "answer": r"0.25\,\mathrm{M}",
                },
                {
                    "examType": "Admission",
                    "question": r"\(0.2\,\mathrm{mol}\) দ্রব \(500\,\mathrm{g}\) দ্রবকে—মোলালিটি?",
                    "answer": r"0.4\,\mathrm{mol\,kg^{-1}}",
                },
            ],
            "memorize": {
                "trick": "M → Litre of Solution; m → mass (kg) of solvent।",
                "steps": ["M = moles/L solution", "m = moles/kg solvent", "m তাপমাত্রা-স্বাধীন"],
            },
            "related": ["mole-concept-basic", "raoult-law", "osmotic-pressure"],
        },
        "ph-strong-acid": {
            "latex": r"\mathrm{pH}=-\log_{10}[\mathrm{H^+}]",
            "summary": r"সবল অ্যাসিডে \([\mathrm{H^{+}}]\approx C\); \(\mathrm{pH}=-\log C\) (তনু, সম্পূর্ণ আয়নিত)।",
            "symbols": [
                {"symbol": r"\mathrm{pH}", "meaning": "হাইড্রোজেন আয়ন সূচক", "unit": "1"},
                {"symbol": r"[\mathrm{H^+}]", "meaning": "হাইড্রোজেন আয়ন ঘনমাত্রা", "unit": "mol/L"},
            ],
            "derivation": {
                "lead": "pH স্কেল অম্লত্ব পরিমাপ করে; সবল অ্যাসিড সম্পূর্ণ আয়নিত।",
                "steps": [
                    {
                        "title": "সংজ্ঞা",
                        "latex": r"\mathrm{pH}=-\log_{10}[\mathrm{H^+}]",
                        "note": r"\(25^\circ\mathrm{C}\)-এ \(\mathrm{pH}+\mathrm{pOH}=14\)।",
                    },
                    {
                        "title": "সবল অ্যাসিড",
                        "latex": r"[\mathrm{H^+}]\approx C\quad\Rightarrow\quad\mathrm{pH}=-\log C",
                        "note": r"\(\mathrm{HA}\to\mathrm{H^+}+\mathrm{A^-}\) সম্পূর্ণ।",
                    },
                ],
                "assumptions": ["তনু দ্রবণ; জলের স্ব-আয়নন উপেক্ষিত"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"\(0.01\,\mathrm{M}\) \(\mathrm{HCl}\)-এর pH?",
                    "answer": r"2",
                }
            ],
            "memorize": {
                "trick": "সবল অ্যাসিড: pH = −log C।",
                "steps": ["[H⁺] ≈ C", "pH = −log C", "pH + pOH = 14"],
            },
            "related": ["ph-weak-acid", "henderson-hasselbalch", "common-ion-effect"],
        },
        "hess-law": {
            "latex": r"\Delta H_{\mathrm{rxn}}=\sum \Delta H_{\mathrm{steps}}",
            "summary": r"হেসের সূত্র: মোট এনথ্যালপি পরিবর্তন পথ-স্বাধীন—ধাপগুলোর \(\Delta H\) যোগফল।",
            "symbols": [
                {"symbol": r"\Delta H", "meaning": "এনথ্যালপি পরিবর্তন", "unit": "kJ/mol"},
            ],
            "derivation": {
                "lead": "এনথ্যালপি অবস্থা ফাংশন; সরাসরি বিক্রিয়া না মিললে চক্র দিয়ে হিসাব।",
                "steps": [
                    {
                        "title": "পথ স্বাধীনতা",
                        "latex": r"\Delta H_{\mathrm{direct}}=\Delta H_1+\Delta H_2+\cdots",
                        "note": "ধাপগুলোর এনথ্যালপি যোগ করো।",
                    },
                    {
                        "title": "গঠন এনথ্যালপি",
                        "latex": r"\Delta H_{\mathrm{rxn}}=\sum\Delta H_f^\circ(\mathrm{prod})-\sum\Delta H_f^\circ(\mathrm{react})",
                        "note": "Hess-এর ব্যবহারিক রূপ।",
                    },
                ],
                "assumptions": ["ধ্রুব চাপ; একই প্রাথমিক ও চূড়ান্ত অবস্থা"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"A→B এর \(\Delta H=10\), B→C এর \(\Delta H=5\) হলে A→C?",
                    "answer": r"15\ \text{(একই একক)}",
                }
            ],
            "memorize": {
                "trick": "Hess: যোগ করো ধাপের ΔH — পথ আলাদা হলেও মোট একই।",
                "steps": ["চক্র আঁকো", "ধাপের ΔH যোগ", "উল্টো ধাপে চিহ্ন বদলাও"],
            },
            "related": ["bond-enthalpy", "hess-gibbs", "kirchhoff-enthalpy"],
        },
        "henderson-hasselbalch": {
            "latex": r"\mathrm{pH}=\mathrm{p}K_a+\log_{10}\dfrac{[\mathrm{A^-}]}{[\mathrm{HA}]}",
            "summary": r"বাফার pH: \(\mathrm{pH}=\mathrm{p}K_a+\log([\mathrm{salt}]/[\mathrm{acid}])\)।",
            "symbols": [
                {"symbol": r"\mathrm{p}K_a", "meaning": r"\(-\log K_a\)", "unit": "1"},
                {"symbol": r"[\mathrm{A^-}]", "meaning": "লবণ/ক্ষারক রূপ", "unit": "mol/L"},
                {"symbol": r"[\mathrm{HA}]", "meaning": "দুর্বল অ্যাসিড", "unit": "mol/L"},
            ],
            "derivation": {
                "lead": "দুর্বল অ্যাসিড–তার লবণের বাফারে Henderson–Hasselbalch ব্যবহার হয়।",
                "steps": [
                    {
                        "title": "Ka থেকে",
                        "latex": r"K_a=\dfrac{[\mathrm{H^+}][\mathrm{A^-}]}{[\mathrm{HA}]}",
                        "note": "লগ নিয়ে সাজাও।",
                    },
                    {
                        "title": "HH সমীকরণ",
                        "latex": r"\mathrm{pH}=\mathrm{p}K_a+\log\dfrac{[\mathrm{A^-}]}{[\mathrm{HA}]}",
                        "note": "অল্প অ্যাসিড/ক্ষার যোগে অনুপাত প্রায় স্থির → pH স্থির।",
                    },
                ],
                "assumptions": ["তনু বাফার; কার্যকলাপ ≈ ঘনমাত্রা"],
            },
            "questions": [
                {
                    "examType": "HSC",
                    "question": r"[HA]=[A⁻], pKa=4.7 হলে pH?",
                    "answer": r"4.7",
                }
            ],
            "memorize": {
                "trick": "বাফারে pH ≈ pKa যখন acid = salt; HH: pH = pKa + log(salt/acid)।",
                "steps": ["pKa জানো", "salt/acid অনুপাত", "log যোগ"],
            },
            "related": ["ph-weak-acid", "ph-strong-acid", "common-ion-effect"],
        },
    }

    all_ids = {p.stem for p in CHEM.glob("*/formulas/*.json")}
    # include cards we're about to add
    all_ids.update(
        {
            "structural-condensed-formula",
            "homologous-series",
            "hydrocarbon-general-formula",
            "bond-line-formula",
            "iupac-naming-rules",
        }
    )

    for fid, patch in upgrades.items():
        matches = list(CHEM.glob(f"*/formulas/{fid}.json"))
        if not matches:
            print("missing stub", fid)
            continue
        data = load(matches[0])
        for k, v in patch.items():
            if k == "related":
                data["related"] = [r for r in v if r in all_ids and r != fid]
            else:
                data[k] = v
        imp = data.get("importance", 3)
        tags = [t for t in data.get("tags", list(STD_TAGS)) if not str(t).endswith("-star")]
        if not tags:
            tags = list(STD_TAGS)
        tags.append(f"{imp}-star")
        data["tags"] = tags
        save(matches[0], data)
        print("polished", fid)


def scan_fragmented() -> list[str]:
    bad = []
    for p in CHEM.glob("*/formulas/*.json"):
        data = load(p)
        for q in data.get("questions", []):
            val = q.get("answer", "")
            frags = re.findall(r"\\text\{([^}]*)\}", val)
            # Bangla short fragments
            short = [f for f in frags if any("\u0980" <= c <= "\u09ff" for c in f) and len(f) <= 3]
            if len(short) >= 3:
                bad.append(f"{data['id']}: {val[:90]}")
    return bad


def filter_related_everywhere() -> None:
    """Drop related links that don't exist yet / self-links; keep graph clean."""
    all_ids = {p.stem for p in CHEM.glob("*/formulas/*.json")}
    n = 0
    for p in CHEM.glob("*/formulas/*.json"):
        data = load(p)
        before = list(data.get("related", []))
        after = [r for r in before if r in all_ids and r != data["id"]]
        if after != before:
            data["related"] = after
            save(p, data)
            n += 1
    print("related cleaned on", n, "files")


def main() -> None:
    fix_fragmented_answers()
    add_structural_cards()
    polish_stubs()
    improve_organic_existing()
    filter_related_everywhere()
    print("=== fragmented after ===")
    for b in scan_fragmented():
        print(" ", b)
    print("chemistry formulas:", len(list(CHEM.glob("*/formulas/*.json"))))


if __name__ == "__main__":
    main()
