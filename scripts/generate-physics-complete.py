#!/usr/bin/env python3
"""Add high-yield missing HSC/admission Physics formulas + polish weak stubs."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "subjects" / "physics"
EXISTING = {p.stem for p in ROOT.glob("chapters/*/formulas/*.json")}


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
    if id in EXISTING:
        raise SystemExit(f"duplicate id already on disk: {id}")
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
        "derivation": {
            "lead": lead,
            "steps": steps,
            "assumptions": assumptions,
        },
        "questions": questions,
        "memorize": {"trick": trick, "steps": memorize_steps or []},
        "subjects": ["physics"],
        "related": [r for r in (related or []) if r != id],
    }


def write(data: dict) -> None:
    out = ROOT / "chapters" / data["chapter"] / "formulas"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{data['id']}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    EXISTING.add(data["id"])
    print(f"+ {data['chapter']}/{data['id']}")


NEW: list[dict] = [
    # —— measurement ——
    formula(
        id="error-propagation-sum-difference",
        chapter="measurement",
        title="Error Propagation — Sum & Difference",
        title_bn="যোগ–বিয়োগে ত্রুটি সঞ্চারণ",
        summary="যোগ/বিয়োগে পরম ত্রুটি যোগ হয়",
        latex="\\Delta(x\\pm y)=\\Delta x+\\Delta y",
        symbols=[
            {"symbol": "\\Delta x", "meaning": "x-এর পরম ত্রুটি", "unit": "x-এর একক"},
            {"symbol": "\\Delta y", "meaning": "y-এর পরম ত্রুটি", "unit": "y-এর একক"},
        ],
        lead="পরম ত্রুটি যোগ–বিয়োগে সর্বদা যোগ হয়; গুণ–ভাগে আপেক্ষিক ত্রুটি যোগ হয়।",
        steps=[
            {"title": "যোগ", "latex": "\\Delta(x+y)=\\Delta x+\\Delta y", "note": "সর্বোচ্চ সম্ভাব্য ত্রুটি ধরা হয়।"},
            {"title": "বিয়োগ", "latex": "\\Delta(x-y)=\\Delta x+\\Delta y", "note": "বিয়োগেও পরম ত্রুটি যোগই হয়।"},
        ],
        assumptions=["ত্রুটিগুলো স্বাধীন ও সর্বোচ্চ সীমা হিসেবে নেওয়া"],
        questions=[
            {
                "examType": "HSC",
                "question": "x = (20.0 ± 0.1) cm ও y = (12.0 ± 0.2) cm হলে (x − y)-এর ত্রুটি কত?",
                "answer": "\\Delta(x-y)=0.1+0.2=0.3\\ \\text{cm};\\quad x-y=(8.0\\pm 0.3)\\ \\text{cm}",
            }
        ],
        trick="যোগ–বিয়োগ → পরম ত্রুটি যোগ; গুণ–ভাগ → আপেক্ষিক ত্রুটি যোগ।",
        related=["error-propagation-product", "percentage-error", "absolute-relative-error"],
        importance=3,
        order=110,
    ),
    formula(
        id="instrument-zero-error-correction",
        chapter="measurement",
        title="Zero Error Correction",
        title_bn="শূন্য ত্রুটি সংশোধন",
        summary="সংশোধিত পাঠ = পরিমাপিত পাঠ − শূন্য ত্রুটি",
        latex="\\text{corrected reading}=\\text{observed}-(\\pm e_0)",
        symbols=[
            {"symbol": "e_0", "meaning": "শূন্য ত্রুটি", "unit": "যন্ত্রের একক"},
        ],
        lead="যন্ত্রের শূন্য মিল না থাকলে সব পাঠে শূন্য ত্রুটি সংশোধন করতে হয়।",
        steps=[
            {
                "title": "ধনাত্মক শূন্য ত্রুটি",
                "latex": "e_0>0\\Rightarrow \\text{corrected}=\\text{observed}-e_0",
                "note": "শূন্যের ডানে মিল → ধনাত্মক শূন্য ত্রুটি।",
            },
            {
                "title": "ঋণাত্মক শূন্য ত্রুটি",
                "latex": "e_0<0\\Rightarrow \\text{corrected}=\\text{observed}+|e_0|",
                "note": "শূন্যের বামে মিল → ঋণাত্মক শূন্য ত্রুটি।",
            },
        ],
        assumptions=["ভার্নিয়ার/স্ক্রু গেজে শূন্য সংশোধন প্রযোজ্য"],
        questions=[
            {
                "examType": "Admission",
                "question": "স্ক্রু গেজের পাঠ 5.28 mm ও ধনাত্মক শূন্য ত্রুটি 0.02 mm হলে প্রকৃত মান কত?",
                "answer": "5.28-0.02=5.26\\ \\text{mm}",
            }
        ],
        trick="ধনাত্মক শূন্য ত্রুটি বিয়োগ; ঋণাত্মক হলে যোগ।",
        related=["least-count-vernier", "screw-gauge-least-count"],
        importance=3,
        order=120,
    ),
    # —— vector ——
    formula(
        id="position-vector-section-formula",
        chapter="vector",
        title="Section Formula (Position Vector)",
        title_bn="অবস্থান ভেক্টর — বিভাজন সূত্র",
        summary="m:n অনুপাতে বিভাজক বিন্দুর অবস্থান ভেক্টর",
        latex="\\vec r=\\frac{n\\vec r_1+m\\vec r_2}{m+n}",
        symbols=[
            {"symbol": "\\vec r_1,\\vec r_2", "meaning": "A ও B-এর অবস্থান ভেক্টর", "unit": "m"},
            {"symbol": "m:n", "meaning": "অভ্যন্তরীণ বিভাজন অনুপাত", "unit": "—"},
        ],
        lead="A ও B-কে m:n অনুপাতে অভ্যন্তরে বিভাজক বিন্দুর অবস্থান ভেক্টর।",
        steps=[
            {
                "title": "অভ্যন্তরীণ বিভাজন",
                "latex": "\\vec r=\\frac{n\\vec r_A+m\\vec r_B}{m+n}",
                "note": "m দূরের বিন্দুর ওজন, n কাছের।",
            },
            {
                "title": "মধ্যবিন্দু",
                "latex": "m=n=1\\Rightarrow \\vec r=\\frac{\\vec r_A+\\vec r_B}{2}",
                "note": "মধ্যবিন্দুতে গড়।",
            },
        ],
        assumptions=["অভ্যন্তরীণ বিভাজন; বাহ্যিক বিভাজনে চিহ্ন বদলায়"],
        questions=[
            {
                "examType": "HSC",
                "question": "\\(\\vec r_A=\\hat i+2\\hat j\\), \\(\\vec r_B=3\\hat i+4\\hat j\\)। AB-এর মধ্যবিন্দু কী?",
                "answer": "\\vec r=\\frac{(1+3)\\hat i+(2+4)\\hat j}{2}=2\\hat i+3\\hat j",
            }
        ],
        trick="মধ্যবিন্দু = দুই অবস্থান ভেক্টরের গড়।",
        related=["unit-vector", "vector-addition-laws"],
        importance=2,
        order=110,
    ),
    formula(
        id="vector-component-resolution",
        chapter="vector",
        title="Resolution of a Vector",
        title_bn="ভেক্টরের উপাংশ বিশ্লেষণ",
        summary="সমতলীয় ভেক্টরের x–y উপাংশ",
        latex="A_x=A\\cos\\theta,\\quad A_y=A\\sin\\theta,\\quad A=\\sqrt{A_x^2+A_y^2}",
        symbols=[
            {"symbol": "A", "meaning": "ভেক্টরের মান", "unit": "ভেক্টরের একক"},
            {"symbol": "\\theta", "meaning": "x-অক্ষের সাথে কোণ", "unit": "rad বা °"},
        ],
        lead="যেকোনো সমতলীয় ভেক্টরকে লম্ব উপাংশে ভাঙা যায়।",
        steps=[
            {"title": "উপাংশ", "latex": "A_x=A\\cos\\theta,\\ A_y=A\\sin\\theta", "note": "θ x-অক্ষ থেকে।"},
            {"title": "মান ও দিক", "latex": "A=\\sqrt{A_x^2+A_y^2},\\ \\tan\\theta=A_y/A_x", "note": "কোয়াড্রেন্ট অনুসারে θ।"},
        ],
        assumptions=["দ্বিমাত্রিক কার্তেসীয় অক্ষ"],
        questions=[
            {
                "examType": "Admission",
                "question": "10 N বল x-অক্ষের সাথে 60° কোণে থাকলে Fx ও Fy কত?",
                "answer": "F_x=10\\cos60^\\circ=5\\ \\text{N},\\ F_y=10\\sin60^\\circ=5\\sqrt{3}\\ \\text{N}",
            }
        ],
        trick="কোসাইন = সংলগ্ন উপাংশ; সাইন = বিপরীত উপাংশ।",
        related=["vector-dot-product", "unit-vector", "vector-resultant"],
        importance=3,
        order=120,
    ),
    # —— motion-kinematics ——
    formula(
        id="vertical-motion-gravity",
        chapter="motion-kinematics",
        title="Vertical Motion under Gravity",
        title_bn="অভিকর্ষে উল্লম্ব গতি",
        summary="উল্লম্ব নিক্ষেপ ও মুক্তপতনের সূত্র",
        latex="v=u-gt,\\quad h=ut-\\tfrac12 gt^2,\\quad v^2=u^2-2gh",
        symbols=[
            {"symbol": "u", "meaning": "প্রাথমিক বেগ (উর্ধ্বমুখী +)", "unit": "m/s"},
            {"symbol": "g", "meaning": "অভিকর্ষজ ত্বরণ", "unit": "m/s²"},
            {"symbol": "h", "meaning": "উচ্চতা/সরণ", "unit": "m"},
        ],
        lead="উর্ধ্বমুখী ধনাত্মক নিলে অভিকর্ষ −g; সর্বোচ্চ উচ্চতায় v = 0।",
        steps=[
            {"title": "সর্বোচ্চ উচ্চতা", "latex": "H=\\frac{u^2}{2g}", "note": "v=0 বসিয়ে।"},
            {"title": "মোট সময় (উঠা–নামা)", "latex": "T=\\frac{2u}{g}", "note": "একই বিন্দুতে ফিরতে।"},
        ],
        assumptions=["বায়ু বাধা নেই; g ধ্রুব"],
        questions=[
            {
                "examType": "HSC",
                "question": "20 m/s বেগে উল্লম্বে নিক্ষেপ করলে সর্বোচ্চ উচ্চতা কত? (g = 10 m/s²)",
                "answer": "H=\\frac{20^2}{2\\times10}=20\\ \\text{m}",
            }
        ],
        trick="H = u²/(2g); মোট সময় = 2u/g।",
        related=["kinematic-equation-v2", "kinematic-equation-s", "projectile-motion"],
        importance=3,
        order=110,
    ),
    formula(
        id="relative-velocity-2d",
        chapter="motion-kinematics",
        title="Two-Dimensional Relative Velocity",
        title_bn="দ্বিমাত্রিক আপেক্ষিক বেগ",
        summary="\\(\\vec v_{AB}=\\vec v_A-\\vec v_B\\)",
        latex="\\vec v_{AB}=\\vec v_A-\\vec v_B",
        symbols=[
            {"symbol": "\\vec v_A", "meaning": "A-এর বেগ", "unit": "m/s"},
            {"symbol": "\\vec v_{AB}", "meaning": "B-এর সাপেক্ষে A-এর বেগ", "unit": "m/s"},
        ],
        lead="B-এর সাপেক্ষে A দেখতে B-এর বেগ বিয়োগ করো।",
        steps=[
            {"title": "ভেক্টর বিয়োগ", "latex": "\\vec v_{AB}=\\vec v_A-\\vec v_B", "note": "উপাংশে ভাঙে হিসাব সহজ।"},
            {
                "title": "মান",
                "latex": "|\\vec v_{AB}|=\\sqrt{(v_{Ax}-v_{Bx})^2+(v_{Ay}-v_{By})^2}",
                "note": "দিক tan⁻¹ দিয়ে।",
            },
        ],
        assumptions=["জড় কাঠামো; একই সময়ে পরিমাপ"],
        questions=[
            {
                "examType": "Admission",
                "question": "A পূর্বে 3 m/s, B উত্তরে 4 m/s। B-এর সাপেক্ষে A-এর বেগের মান কত?",
                "answer": "|\\vec v_{AB}|=\\sqrt{3^2+(-4)^2}=5\\ \\text{m/s}",
            }
        ],
        trick="আপেক্ষিক বেগ = নিজের − অন্যের।",
        related=["relative-velocity-1d", "river-boat-crossing", "rain-man-relative"],
        importance=3,
        order=120,
    ),
    # —— dynamics ——
    formula(
        id="apparent-weight-elevator",
        chapter="dynamics",
        title="Apparent Weight in an Elevator",
        title_bn="লিফটে আপাত ওজন",
        summary="উঠতে W′ = m(g+a), নামতে W′ = m(g−a)",
        latex="W'=m(g\\pm a)",
        symbols=[
            {"symbol": "W'", "meaning": "আপাত ওজন / নর্মাল বল", "unit": "N"},
            {"symbol": "a", "meaning": "লিফটের ত্বরণ", "unit": "m/s²"},
        ],
        lead="লিফটের ত্বরণের দিক অনুসারে আপাত ওজন বাড়ে বা কমে।",
        steps=[
            {"title": "উর্ধ্ব ত্বরণ", "latex": "N-mg=ma\\Rightarrow N=m(g+a)", "note": "উঠতে ভারী লাগে।"},
            {"title": "নিম্ন ত্বরণ", "latex": "mg-N=ma\\Rightarrow N=m(g-a)", "note": "নামতে হালকা লাগে।"},
            {"title": "মুক্তপতন", "latex": "a=g\\Rightarrow N=0", "note": "ওজনহীনতা।"},
        ],
        assumptions=["লিফটের মেঝেতে দাঁড়ানো; বায়ু বাধা নেই"],
        questions=[
            {
                "examType": "BUET",
                "question": "60 kg ব্যক্তি 2 m/s² ত্বরণে উঠছে। আপাত ওজন কত? (g = 10)",
                "answer": "N=60(10+2)=720\\ \\text{N}",
            }
        ],
        trick="উঠলে +a, নামলে −a; মুক্তপতনে N = 0।",
        related=["newtons-laws", "friction"],
        importance=3,
        order=170,
    ),
    formula(
        id="static-equilibrium-conditions",
        chapter="dynamics",
        title="Conditions of Equilibrium",
        title_bn="সাম্যাবস্থার শর্ত",
        summary="নেট বল ও নেট টর্ক শূন্য",
        latex="\\sum \\vec F=0,\\quad \\sum \\vec\\tau=0",
        symbols=[
            {"symbol": "\\sum F", "meaning": "মোট বল", "unit": "N"},
            {"symbol": "\\sum\\tau", "meaning": "মোট টর্ক", "unit": "N·m"},
        ],
        lead="স্থির সাম্যাবস্থায় রৈখিক ও ঘূর্ণন উভয় ত্বরণ শূন্য।",
        steps=[
            {"title": "রৈখিক", "latex": "\\sum F_x=0,\\ \\sum F_y=0", "note": "উপাংশে আলাদা।"},
            {"title": "ঘূর্ণন", "latex": "\\sum\\tau=0", "note": "যেকোনো বিন্দুতে টর্ক শূন্য।"},
        ],
        assumptions=["স্থির বা সমবেগে চলমান; জড় কাঠামো"],
        questions=[
            {
                "examType": "HSC",
                "question": "একটি দণ্ড সাম্যাবস্থায় থাকার দুই শর্ত কী?",
                "answer": "\\sum\\vec F=0\\ \\text{এবং}\\ \\sum\\vec\\tau=0",
            }
        ],
        trick="বল শূন্য + টর্ক শূন্য = সাম্যাবস্থা।",
        related=["torque-angular-acc", "center-of-mass"],
        importance=3,
        order=180,
    ),
    formula(
        id="inclined-plane-connected",
        chapter="dynamics",
        title="Connected Bodies on Incline",
        title_bn="আনত তলে সংযুক্ত বস্তু",
        summary="দুই ভরের ত্বরণ ও টান",
        latex="a=\\frac{(m_1\\sin\\theta_1-m_2\\sin\\theta_2)g}{m_1+m_2}",
        symbols=[
            {"symbol": "m_1,m_2", "meaning": "দুই বস্তুর ভর", "unit": "kg"},
            {"symbol": "\\theta", "meaning": "আনতির কোণ", "unit": "°"},
            {"symbol": "T", "meaning": "দড়ির টান", "unit": "N"},
        ],
        lead="ঘর্ষণহীন আনত তলে সংযুক্ত বস্তুর নেট চালক বল / মোট ভর = ত্বরণ।",
        steps=[
            {
                "title": "ত্বরণ",
                "latex": "a=\\dfrac{(m_1\\sin\\theta_1-m_2\\sin\\theta_2)g}{m_1+m_2}",
                "note": "যে দিকে বড় উপাংশ সেদিকে গতি।",
            },
            {
                "title": "টান",
                "latex": "T=\\dfrac{m_1 m_2 g(\\sin\\theta_1+\\sin\\theta_2)}{m_1+m_2}",
                "note": "এক তলে হলে θ₂ = 0 বা আলাদা কেস।",
            },
        ],
        assumptions=["ঘর্ষণহীন; দড়ি হালকা ও অপ্রসারণযোগ্য"],
        questions=[
            {
                "examType": "Admission",
                "question": "একই আনতি 30°-এর দুই তলে m ও 2m সংযুক্ত। ত্বরণের দিক কোনটির দিকে?",
                "answer": "2m\\sin30>m\\sin30\\Rightarrow 2m\\ \\text{এর দিকে}",
            }
        ],
        trick="Atwood-এর মতো: নেট (mg sinθ) / মোট m।",
        related=["atwood-machine", "friction", "newtons-laws"],
        importance=2,
        order=190,
    ),
    # —— work-energy ——
    formula(
        id="power-force-velocity",
        chapter="work-energy",
        title="Instantaneous Power",
        title_bn="তাৎক্ষণিক ক্ষমতা",
        summary="P = F·v",
        latex="P=\\vec F\\cdot\\vec v=Fv\\cos\\theta",
        symbols=[
            {"symbol": "P", "meaning": "ক্ষমতা", "unit": "W (J/s)"},
            {"symbol": "\\vec F", "meaning": "বল", "unit": "N"},
            {"symbol": "\\vec v", "meaning": "বেগ", "unit": "m/s"},
        ],
        lead="কাজের হারই ক্ষমতা; তাৎক্ষণিকে P = F·v।",
        steps=[
            {"title": "সংজ্ঞা", "latex": "P=\\dfrac{dW}{dt}", "note": "গড় ক্ষমতা W/t।"},
            {"title": "বল–বেগ", "latex": "P=\\vec F\\cdot\\vec v", "note": "θ কোণে Fv cosθ।"},
        ],
        assumptions=["একই মুহূর্তের F ও v"],
        questions=[
            {
                "examType": "HSC",
                "question": "20 N বল বস্তুকে 4 m/s বেগে চালালে ক্ষমতা কত? (সমরেখ)",
                "answer": "P=Fv=20\\times4=80\\ \\text{W}",
            }
        ],
        trick="P = Fv — একক Watt।",
        related=["work-by-constant-force", "power-efficiency", "kinetic-energy"],
        importance=3,
        order=120,
    ),
    formula(
        id="collision-ke-loss",
        chapter="work-energy",
        title="KE Loss in Inelastic Collision",
        title_bn="অস্থিতিস্থাপক সংঘর্ষে গতিশক্তি ক্ষয়",
        summary="ভরবেগ সংরক্ষিত, গতিশক্তি কমে",
        latex="\\Delta K=\\tfrac12\\mu v_{\\text{rel}}^2(1-e^2)",
        symbols=[
            {"symbol": "e", "meaning": "পুনরুদ্ধার গুণাঙ্ক", "unit": "—"},
            {"symbol": "\\mu", "meaning": "হারিত ভর = m₁m₂/(m₁+m₂)", "unit": "kg"},
        ],
        lead="e < 1 হলে গতিশক্তির অংশ তাপ/বিকৃতিতে যায়।",
        steps=[
            {
                "title": "সম্পূর্ণ অস্থিতিস্থাপক",
                "latex": "e=0,\\ v=\\dfrac{m_1u_1+m_2u_2}{m_1+m_2}",
                "note": "একসাথে চলে।",
            },
            {
                "title": "ক্ষয়",
                "latex": "\\Delta K=K_i-K_f>0",
                "note": "e=1 হলে ΔK = 0।",
            },
        ],
        assumptions=["বাহ্যিক বল নেই (ভরবেগ সংরক্ষণ)"],
        questions=[
            {
                "examType": "Admission",
                "question": "সম্পূর্ণ অস্থিতিস্থাপক সংঘর্ষে কী সংরক্ষিত থাকে?",
                "answer": "\\text{শুধু ভরবেগ; গতিশক্তি সংরক্ষিত নয়}",
            }
        ],
        trick="e=1 স্থিতিস্থাপক; e=0 সম্পূর্ণ অস্থিতিস্থাপক।",
        related=["coefficient-restitution", "elastic-collision", "work-theorem"],
        importance=2,
        order=130,
    ),
    # —— circular-motion ——
    formula(
        id="banked-road-with-friction",
        chapter="circular-motion",
        title="Banked Road with Friction",
        title_bn="ঘর্ষণযুক্ত বাঁকানো রাস্তা",
        summary="সীমাবেগের পরিসর",
        latex="v_{\\max}=\\sqrt{rg\\tan(\\theta+\\phi)},\\quad v_{\\min}=\\sqrt{rg\\tan(\\theta-\\phi)}",
        symbols=[
            {"symbol": "\\theta", "meaning": "ব্যাংকিং কোণ", "unit": "°"},
            {"symbol": "\\phi", "meaning": "ঘর্ষণ কোণ (\\(\\tan\\phi=\\mu\\))", "unit": "°"},
            {"symbol": "r", "meaning": "বক্রতার ব্যাসার্ধ", "unit": "m"},
        ],
        lead="ঘর্ষণ থাকলে নিরাপদ গতির একটি পরিসর থাকে।",
        steps=[
            {
                "title": "ঘর্ষণহীন আদর্শ",
                "latex": "v_0=\\sqrt{rg\\tan\\theta}",
                "note": "μ = 0 কেস।",
            },
            {
                "title": "সীমা",
                "latex": "v_{\\max}=\\sqrt{rg\\tan(\\theta+\\phi)},\\ v_{\\min}=\\sqrt{rg\\tan(\\theta-\\phi)}",
                "note": "উপরে চড়া/নিচে নামার প্রবণতায় ঘর্ষণের দিক বদলায়।",
            },
        ],
        assumptions=["গাড়ি পিছলে না গেলে সীমান্ত; বাঁক অনুভূমিক বৃত্ত"],
        questions=[
            {
                "examType": "BUET",
                "question": "ঘর্ষণহীন বাঁকানো রাস্তায় নিরাপদ বেগের সূত্র কী?",
                "answer": "v=\\sqrt{rg\\tan\\theta}",
            }
        ],
        trick="μ=0 → √(rg tanθ); ঘর্ষণে ±φ।",
        related=["banking-of-road", "banking-of-road-ideal", "centripetal-force-mv2r"],
        importance=3,
        order=130,
    ),
    # —— gravitation ——
    formula(
        id="sphere-shell-gravity",
        chapter="gravitation",
        title="Gravity of Sphere & Shell",
        title_bn="গোলক ও খোলকের মহাকর্ষ",
        summary="খোলকের বাইরে বিন্দু ভরের মতো; ভিতরে ক্ষেত্র শূন্য",
        latex="g(r)=\\begin{cases}GM/r^2 & r\\ge R\\\\ 0 & \\text{shell }r<R\\\\ GMr/R^3 & \\text{solid }r\\le R\\end{cases}",
        symbols=[
            {"symbol": "R", "meaning": "ব্যাসার্ধ", "unit": "m"},
            {"symbol": "r", "meaning": "কেন্দ্র থেকে দূরত্ব", "unit": "m"},
            {"symbol": "M", "meaning": "মোট ভর", "unit": "kg"},
        ],
        lead="গাউসের মহাকর্ষীয় রূপ: খোলকের ভিতরে ক্ষেত্র শূন্য; কঠিন গোলকের ভিতরে r অনুপাতে।",
        steps=[
            {"title": "খোলক বাইরে", "latex": "g=GM/r^2", "note": "বিন্দু ভরের মতো।"},
            {"title": "খোলক ভিতরে", "latex": "g=0", "note": "নেট ক্ষেত্র বাতিল।"},
            {"title": "কঠিন গোলক ভিতরে", "latex": "g=GMr/R^3", "note": "আবদ্ধ ভর ∝ r³।"},
        ],
        assumptions=["সমঘনত্ব; গোলীয় প্রতিসাম্য"],
        questions=[
            {
                "examType": "HSC",
                "question": "পাতলা গোলীয় খোলকের কেন্দ্রে মহাকর্ষীয় ক্ষেত্রের মান কত?",
                "answer": "0",
            }
        ],
        trick="খোলকের ভিতর g = 0; কঠিনে কেন্দ্রেও 0, পৃষ্ঠে সর্বোচ্চ।",
        related=["newtons-gravitation", "gravitational-intensity", "acceleration-due-to-gravity"],
        importance=3,
        order=120,
    ),
    formula(
        id="satellite-weightlessness",
        chapter="gravitation",
        title="Weightlessness in Satellite",
        title_bn="উপগ্রহে ওজনহীনতা",
        summary="অভিকর্ষই কেন্দ্রমুখী বল — আপাত ওজন শূন্য",
        latex="N=0\\quad(\\text{orbital free fall})",
        symbols=[
            {"symbol": "N", "meaning": "আপাত ওজন / নর্মাল বল", "unit": "N"},
            {"symbol": "g'", "meaning": "কক্ষপথে কার্যকরী g", "unit": "m/s²"},
        ],
        lead="উপগ্রহ ও নভোচারী একই ত্বরণে মুক্তপতনে — পরস্পরের ওপর নর্মাল বল শূন্য।",
        steps=[
            {"title": "কেন্দ্রমুখী", "latex": "\\frac{GMm}{r^2}=\\frac{mv^2}{r}", "note": "অভিকর্ষই প্রয়োজনীয় বল।"},
            {"title": "আপাত ওজন", "latex": "W'=m(g-a)=0", "note": "a = g (মুক্তপতন)।"},
        ],
        assumptions=["বৃত্তাকার কক্ষ; বায়ুঘর্ষণ নেই"],
        questions=[
            {
                "examType": "Admission",
                "question": "উপগ্রহে ওজনহীনতা মানে কি অভিকর্ষ শূন্য?",
                "answer": "\\text{না — অভিকর্ষ আছে; আপাত ওজন শূন্য}",
            }
        ],
        trick="ওজনহীনতা ≠ অভিকর্ষহীনতা; মুক্তপতন।",
        related=["orbital-velocity", "satellite-energy", "escape-velocity"],
        importance=2,
        order=130,
    ),
    # —— properties-of-matter ——
    formula(
        id="elastic-energy-density",
        chapter="properties-of-matter",
        title="Elastic Energy Density",
        title_bn="স্থিতিস্থাপক শক্তি ঘনত্ব",
        summary="u = ½ × stress × strain",
        latex="u=\\tfrac12\\times\\text{stress}\\times\\text{strain}=\\frac{Y(\\Delta L)^2}{2L^2}",
        symbols=[
            {"symbol": "u", "meaning": "একক আয়তনে শক্তি", "unit": "J/m³"},
            {"symbol": "Y", "meaning": "ইয়ং গুণাঙ্ক", "unit": "N/m²"},
        ],
        lead="স্থিতিস্থাপক বিকৃতিতে সঞ্চিত শক্তি = বক্রের নিচের ক্ষেত্রফল।",
        steps=[
            {"title": "ঘনত্ব", "latex": "u=\\tfrac12\\sigma\\varepsilon", "note": "σ = stress, ε = strain।"},
            {"title": "মোট শক্তি", "latex": "U=\\tfrac12\\times\\text{stress}\\times\\text{strain}\\times V", "note": "V = আয়তন।"},
        ],
        assumptions=["হুকের সূত্রের সীমার মধ্যে; স্থিতিস্থাপক"],
        questions=[
            {
                "examType": "HSC",
                "question": "Stress 2×10⁸ N/m² ও strain 10⁻³ হলে শক্তি ঘনত্ব কত?",
                "answer": "u=\\tfrac12\\times2\\times10^8\\times10^{-3}=10^5\\ \\text{J/m}^3",
            }
        ],
        trick="u = ½ × stress × strain — ত্রিভুজের ক্ষেত্রফল।",
        related=["hookes-law-stress-strain", "youngs-modulus"],
        importance=3,
        order=150,
    ),
    formula(
        id="poisson-ratio",
        chapter="properties-of-matter",
        title="Poisson's Ratio",
        title_bn="পয়সনের অনুপাত",
        summary="পার্শ্বীয় বিকৃতি / দৈর্ঘ্যিক বিকৃতি",
        latex="\\sigma=-\\dfrac{\\text{lateral strain}}{\\text{longitudinal strain}}",
        symbols=[
            {"symbol": "\\sigma", "meaning": "পয়সন অনুপাত", "unit": "মাত্রাহীন"},
            {"symbol": "\\Delta D/D", "meaning": "পার্শ্বীয় বিকৃতি", "unit": "—"},
        ],
        lead="টান দিলে লম্বা হয় ও চিকন হয় — অনুপাতই পয়সন।",
        steps=[
            {"title": "সংজ্ঞা", "latex": "\\sigma=\\dfrac{\\Delta D/D}{\\Delta L/L}", "note": "ঋণ চিহ্ন প্রায়ই বাদ দিয়ে মান নেওয়া হয়।"},
            {"title": "সীমা", "latex": "0<\\sigma<0.5", "note": "আদর্শ অসংকোচনযোগ্যে σ → 0.5।"},
        ],
        assumptions=["ইলাস্টিক সীমা; সমসত্ব পদার্থ"],
        questions=[
            {
                "examType": "Admission",
                "question": "দৈর্ঘ্যিক বিকৃতি 0.02 ও ব্যাসের বিকৃতি 0.005 হলে σ কত?",
                "answer": "\\sigma=0.005/0.02=0.25",
            }
        ],
        trick="পার্শ্ব ÷ দৈর্ঘ্য — সাধারণত 0.2–0.4।",
        related=["youngs-modulus", "bulk-shear-modulus", "hookes-law-stress-strain"],
        importance=2,
        order=160,
    ),
    formula(
        id="reynolds-number",
        chapter="properties-of-matter",
        title="Reynolds Number",
        title_bn="রেনল্ডস সংখ্যা",
        summary="প্রবাহ স্তরিত না বিশৃঙ্খল নির্দেশক",
        latex="R_e=\\dfrac{\\rho vd}{\\eta}",
        symbols=[
            {"symbol": "R_e", "meaning": "রেনল্ডস সংখ্যা", "unit": "মাত্রাহীন"},
            {"symbol": "\\eta", "meaning": "সান্দ্রতা গুণাঙ্ক", "unit": "Pa·s"},
            {"symbol": "d", "meaning": "বৈশিষ্ট্য দৈর্ঘ্য/ব্যাস", "unit": "m"},
        ],
        lead="Re ছোট → স্তরিত; বড় → টার্বুলেন্ট।",
        steps=[
            {"title": "সংজ্ঞা", "latex": "R_e=\\rho vd/\\eta", "note": "জড় বল / সান্দ্র বল।"},
            {"title": "সীমা (নলে)", "latex": "R_e<2000\\ \\text{স্তরিত};\\ >4000\\ \\text{বিশৃঙ্খল}", "note": "মাঝে পরিবর্তনশীল।"},
        ],
        assumptions=["নল/প্রবাহের বৈশিষ্ট্য দৈর্ঘ্য d"],
        questions=[
            {
                "examType": "HSC",
                "question": "রেনল্ডস সংখ্যার সূত্র কী?",
                "answer": "R_e=\\rho v d/\\eta",
            }
        ],
        trick="Re = ρvd/η — সান্দ্রতা বাড়লে Re কমে।",
        related=["stokes-law", "poiseuille-law", "bernoulli-equation"],
        importance=2,
        order=170,
    ),
    # —— periodic-motion ——
    formula(
        id="spring-combination-shm",
        chapter="periodic-motion",
        title="SHM — Series & Parallel Springs",
        title_bn="শ্রেণি ও সমান্তরাল স্প্রিং",
        summary="কার্যকর k দিয়ে T = 2π√(m/k)",
        latex="\\frac{1}{k_s}=\\frac{1}{k_1}+\\frac{1}{k_2},\\quad k_p=k_1+k_2",
        symbols=[
            {"symbol": "k_s", "meaning": "শ্রেণি সমতুল্য", "unit": "N/m"},
            {"symbol": "k_p", "meaning": "সমান্তরাল সমতুল্য", "unit": "N/m"},
        ],
        lead="রোধের মতো: শ্রেণিতে নরম, সমান্তরালে শক্ত।",
        steps=[
            {"title": "শ্রেণি", "latex": "k_s=\\dfrac{k_1k_2}{k_1+k_2}", "note": "টান সমান, প্রসারণ যোগ।"},
            {"title": "সমান্তরাল", "latex": "k_p=k_1+k_2", "note": "প্রসারণ সমান, বল যোগ।"},
            {"title": "পর্যায়কাল", "latex": "T=2\\pi\\sqrt{m/k_{\\text{eq}}}", "note": "k বড় হলে T ছোট।"},
        ],
        assumptions=["ভরহীন স্প্রিং; হুকের সূত্র"],
        questions=[
            {
                "examType": "Admission",
                "question": "দুই সমান k শ্রেণিতে যুক্ত। সমতুল্য k কত?",
                "answer": "k_s=k/2",
            }
        ],
        trick="শ্রেণি → k কমে; সমান্তরাল → k বাড়ে।",
        related=["shm-time-period", "shm-equations", "potential-energy-spring"],
        importance=3,
        order=120,
    ),
    formula(
        id="pendulum-accelerating-lift",
        chapter="periodic-motion",
        title="Pendulum in Accelerating Lift",
        title_bn="ত্বরিত লিফটে দোলক",
        summary="কার্যকর g′ দিয়ে পর্যায়কাল",
        latex="T=2\\pi\\sqrt{\\ell/g_{\\text{eff}}}",
        symbols=[
            {"symbol": "g_{\\text{eff}}", "meaning": "কার্যকর অভিকর্ষ", "unit": "m/s²"},
            {"symbol": "\\ell", "meaning": "দোলকের দৈর্ঘ্য", "unit": "m"},
        ],
        lead="লিফটের ত্বরণ অনুসারে g_eff বদলায়।",
        steps=[
            {"title": "উর্ধ্ব a", "latex": "g_{\\text{eff}}=g+a", "note": "T কমে।"},
            {"title": "নিম্ন a", "latex": "g_{\\text{eff}}=g-a", "note": "T বাড়ে।"},
            {"title": "মুক্তপতন", "latex": "g_{\\text{eff}}=0\\Rightarrow T\\to\\infty", "note": "দোলন বন্ধ।"},
        ],
        assumptions=["ক্ষুদ্র কোণ; সরল দোলক"],
        questions=[
            {
                "examType": "HSC",
                "question": "লিফট মুক্তপতনে থাকলে দোলকের পর্যায়কাল কী হয়?",
                "answer": "T\\to\\infty\\ (\\text{দোলন হয় না})",
            }
        ],
        trick="উঠলে g+a; নামলে g−a; পতনে দোলন নেই।",
        related=["shm-time-period", "apparent-weight-elevator", "compound-pendulum"],
        importance=2,
        order=130,
    ),
    # —— waves ——
    formula(
        id="newton-laplace-sound",
        chapter="waves",
        title="Newton–Laplace Speed of Sound",
        title_bn="নিউটন–ল্যাপ্লাস শব্দের বেগ",
        summary="v = √(γP/ρ)",
        latex="v=\\sqrt{\\dfrac{\\gamma P}{\\rho}}=\\sqrt{\\dfrac{\\gamma RT}{M}}",
        symbols=[
            {"symbol": "\\gamma", "meaning": "Cp/Cv", "unit": "—"},
            {"symbol": "P", "meaning": "চাপ", "unit": "Pa"},
            {"symbol": "\\rho", "meaning": "ঘনত্ব", "unit": "kg/m³"},
        ],
        lead="নিউটন ধরেছিলেন সমতাপ; ল্যাপ্লাস সমতাপ নয় — অ্যাডিয়াবেটিক সংশোধন γ।",
        steps=[
            {"title": "নিউটন", "latex": "v=\\sqrt{P/\\rho}", "note": "পরীক্ষার চেয়ে কম।"},
            {"title": "ল্যাপ্লাস", "latex": "v=\\sqrt{\\gamma P/\\rho}", "note": "γ > 1 বলে বেগ বাড়ে।"},
        ],
        assumptions=["আদর্শ গ্যাস; অ্যাডিয়াবেটিক সংকোচন–প্রসারণ"],
        questions=[
            {
                "examType": "HSC",
                "question": "বায়ুতে শব্দের বেগের ল্যাপ্লাস সূত্র কী?",
                "answer": "v=\\sqrt{\\gamma P/\\rho}",
            }
        ],
        trick="γ যোগ করো — নিউটন থেকে ল্যাপ্লাস।",
        related=["wave-v-f-lambda", "ideal-gas-equation", "cp-cv-relation"],
        importance=3,
        order=120,
    ),
    formula(
        id="sound-speed-temperature",
        chapter="waves",
        title="Sound Speed vs Temperature",
        title_bn="তাপমাত্রায় শব্দের বেগ",
        summary="v ∝ √T",
        latex="\\dfrac{v_2}{v_1}=\\sqrt{\\dfrac{T_2}{T_1}},\\quad v_t=v_0\\sqrt{1+\\dfrac{t}{273}}",
        symbols=[
            {"symbol": "T", "meaning": "পরম তাপমাত্রা", "unit": "K"},
            {"symbol": "t", "meaning": "সেলসিয়াস তাপমাত্রা", "unit": "°C"},
        ],
        lead="চাপ বাড়লে ρও বাড়ে — প্রধান প্রভাব তাপমাত্রা।",
        steps=[
            {"title": "অনুপাত", "latex": "v\\propto\\sqrt{T}", "note": "T কেলভিনে।"},
            {
                "title": "০°C থেকে",
                "latex": "v_t\\approx 331\\sqrt{1+t/273}\\ \\text{m/s}",
                "note": "প্রায় 0.6 m/s প্রতি °C বৃদ্ধি।",
            },
        ],
        assumptions=["শুষ্ক বায়ু; আদর্শ গ্যাস আচরণ"],
        questions=[
            {
                "examType": "Admission",
                "question": "0°C-এ 330 m/s হলে 27°C-এ আনুমানিক বেগ কত?",
                "answer": "v=330\\sqrt{300/273}\\approx346\\ \\text{m/s}",
            }
        ],
        trick="তাপমাত্রা দ্বিগুণ (K) → বেগ √2 গুণ।",
        related=["newton-laplace-sound", "doppler-effect-general"],
        importance=2,
        order=130,
    ),
    # —— ideal-gas ——
    formula(
        id="vdw-critical-constants",
        chapter="ideal-gas",
        title="van der Waals Critical Constants",
        title_bn="ভ্যান ডার ওয়ালস সংকট ধ্রুবক",
        summary="Tc, Pc, Vc এবং a, b সম্পর্ক",
        latex="T_c=\\dfrac{8a}{27Rb},\\quad P_c=\\dfrac{a}{27b^2},\\quad V_c=3b",
        symbols=[
            {"symbol": "a", "meaning": "আকর্ষণ সংশোধন", "unit": "Pa·m⁶/mol²"},
            {"symbol": "b", "meaning": "আয়তন সংশোধন", "unit": "m³/mol"},
        ],
        lead="সংকট বিন্দুতে আইসোথার্মে অনুভূমিক বিন্দু অফ ইনফ্লেকশন।",
        steps=[
            {"title": "Vc", "latex": "V_c=3b", "note": "এক মোলের জন্য।"},
            {"title": "Pc, Tc", "latex": "P_c=a/(27b^2),\\ T_c=8a/(27Rb)", "note": "(∂P/∂V)_T = 0।"},
        ],
        assumptions=["এক মোল গ্যাস; ভ্যান ডার ওয়ালস সমীকরণ"],
        questions=[
            {
                "examType": "HSC",
                "question": "Vc ও b-এর সম্পর্ক কী?",
                "answer": "V_c=3b",
            }
        ],
        trick="Vc = 3b; Tc-তে 8a/(27Rb)।",
        related=["van-der-waals", "ideal-gas-equation"],
        importance=2,
        order=110,
    ),
    # —— thermodynamics ——
    formula(
        id="area-volume-expansion",
        chapter="thermodynamics",
        title="Area & Volume Expansion",
        title_bn="ক্ষেত্র ও আয়তন প্রসারণ",
        summary="β ≈ 2α, γ ≈ 3α",
        latex="\\Delta A=\\beta A\\Delta T,\\quad \\Delta V=\\gamma V\\Delta T;\\ \\beta\\approx2\\alpha,\\ \\gamma\\approx3\\alpha",
        symbols=[
            {"symbol": "\\alpha", "meaning": "রৈখিক প্রসারণ গুণাঙ্ক", "unit": "/°C"},
            {"symbol": "\\beta", "meaning": "ক্ষেত্র প্রসারণ গুণাঙ্ক", "unit": "/°C"},
            {"symbol": "\\gamma", "meaning": "আয়তন প্রসারণ গুণাঙ্ক", "unit": "/°C"},
        ],
        lead="প্রতি মাত্রায় α — ক্ষেত্রে ২, আয়তনে ৩।",
        steps=[
            {"title": "রৈখিক", "latex": "\\Delta L=\\alpha L\\Delta T", "note": "এক দিক।"},
            {"title": "সম্পর্ক", "latex": "\\beta=2\\alpha,\\ \\gamma=3\\alpha", "note": "আইসোট্রপিক কঠিন।"},
        ],
        assumptions=["ক্ষুদ্র ΔT; সমসত্ব প্রসারণ"],
        questions=[
            {
                "examType": "HSC",
                "question": "α = 1.2×10⁻⁵ /°C হলে γ কত?",
                "answer": "\\gamma=3\\alpha=3.6\\times10^{-5}/^\\circ\\text{C}",
            }
        ],
        trick="α → 2α → 3α (লাইন–এরিয়া–ভলিউম)।",
        related=["thermal-expansion-linear", "calorimetry"],
        importance=3,
        order=180,
    ),
    formula(
        id="wiens-displacement-law",
        chapter="thermodynamics",
        title="Wien's Displacement Law",
        title_bn="ভিয়েনের স্থানচ্যুতি সূত্র",
        summary="λ_max T = b",
        latex="\\lambda_{\\max} T=b\\approx2.90\\times10^{-3}\\ \\text{m·K}",
        symbols=[
            {"symbol": "\\lambda_{\\max}", "meaning": "সর্বোচ্চ তীব্রতার তরঙ্গদৈর্ঘ্য", "unit": "m"},
            {"symbol": "T", "meaning": "পরম তাপমাত্রা", "unit": "K"},
            {"symbol": "b", "meaning": "ভিয়েন ধ্রুবক", "unit": "m·K"},
        ],
        lead="গরম হলে বিকিরণের চূড়া ছোট তরঙ্গদৈর্ঘ্যে সরে।",
        steps=[
            {"title": "সূত্র", "latex": "\\lambda_{\\max}=b/T", "note": "T বাড়লে λ_max কমে।"},
        ],
        assumptions=["কৃষ্ণবস্তু বিকিরণ"],
        questions=[
            {
                "examType": "Admission",
                "question": "সূর্যের পৃষ্ঠ ~5800 K। λ_max আনুমানিক কত?",
                "answer": "\\lambda_{\\max}\\approx2.9\\times10^{-3}/5800\\approx500\\ \\text{nm}",
            }
        ],
        trick="গরম → নীলচে; ঠান্ডা → লালচে।",
        related=["stefan-boltzmann-law", "newton-cooling"],
        importance=3,
        order=190,
    ),
    formula(
        id="net-radiation-exchange",
        chapter="thermodynamics",
        title="Net Radiation Exchange",
        title_bn="নিট তাপীয় বিকিরণ",
        summary="P_net = εσA(T⁴ − T₀⁴)",
        latex="P_{\\mathrm{net}}=e\\sigma A(T^4-T_0^4)",
        symbols=[
            {"symbol": "T", "meaning": "বস্তুর তাপমাত্রা", "unit": "K"},
            {"symbol": "T_0", "meaning": "পারিপার্শ্বিক তাপমাত্রা", "unit": "K"},
            {"symbol": "e", "meaning": "উৎসরতা", "unit": "—"},
        ],
        lead="বিকিরণ ও শোষণ দুটোই চলে — নিট = পার্থক্য।",
        steps=[
            {"title": "নিট ক্ষমতা", "latex": "P=e\\sigma A(T^4-T_0^4)", "note": "T > T₀ হলে শীতল হয়।"},
        ],
        assumptions=["কৃষ্ণবস্তুর কাছাকাছি; ε = absorptivity"],
        questions=[
            {
                "examType": "HSC",
                "question": "পারিপার্শ্বিকের সমান তাপমাত্রায় নিট বিকিরণ কত?",
                "answer": "0\\ (T=T_0)",
            }
        ],
        trick="T⁴ − T₀⁴ — শুধু T⁴ নয়।",
        related=["stefan-boltzmann-law", "wiens-displacement-law"],
        importance=2,
        order=200,
    ),
    # —— static-electricity ——
    formula(
        id="charged-sphere-field-potential",
        chapter="static-electricity",
        title="Field & Potential of Charged Sphere",
        title_bn="আহিত গোলকের ক্ষেত্র ও বিভব",
        summary="বাইরে বিন্দু চার্জের মতো; পরিবাহীর ভিতরে E = 0",
        latex="E=\\dfrac{kq}{r^2}\\ (r\\ge R);\\quad E=0\\ (r<R\\ \\text{conductor})",
        symbols=[
            {"symbol": "R", "meaning": "গোলকের ব্যাসার্ধ", "unit": "m"},
            {"symbol": "q", "meaning": "মোট চার্জ", "unit": "C"},
            {"symbol": "V", "meaning": "বিভব", "unit": "V"},
        ],
        lead="গাউস সূত্র: পরিবাহী গোলকের ভিতরে ক্ষেত্র শূন্য; বাইরে বিন্দু চার্জ।",
        steps=[
            {"title": "ক্ষেত্র বাইরে", "latex": "E=kq/r^2", "note": "r ≥ R।"},
            {"title": "বিভব বাইরে", "latex": "V=kq/r", "note": "অসীমে V = 0।"},
            {"title": "পৃষ্ঠ ও ভিতর", "latex": "V_{\\text{surface}}=kq/R=\\text{const inside}", "note": "পরিবাহীতে সমবিভব।"},
        ],
        assumptions=["গোলীয় প্রতিসাম্য; স্থির চার্জ"],
        questions=[
            {
                "examType": "HSC",
                "question": "আহিত পরিবাহী গোলকের কেন্দ্রে E কত?",
                "answer": "E=0",
            }
        ],
        trick="ভিতরে E = 0, V = ধ্রুব (পরিবাহী)।",
        related=["gauss-law", "electric-field", "electric-potential"],
        importance=3,
        order=150,
    ),
    formula(
        id="capacitor-plate-force",
        chapter="static-electricity",
        title="Force between Capacitor Plates",
        title_bn="ধারকের পাতদ্বয়ের আকর্ষণ বল",
        summary="F = Q²/(2ε₀A)",
        latex="F=\\dfrac{Q^2}{2\\varepsilon_0 A}=\\tfrac12 QE",
        symbols=[
            {"symbol": "Q", "meaning": "পাতের চার্জ", "unit": "C"},
            {"symbol": "A", "meaning": "পাতের ক্ষেত্রফল", "unit": "m²"},
            {"symbol": "F", "meaning": "আকর্ষণ বল", "unit": "N"},
        ],
        lead="বিপরীত চার্জে পাতদ্বয় একে অপরকে আকর্ষণ করে।",
        steps=[
            {"title": "চাপ", "latex": "P=\\tfrac12\\varepsilon_0 E^2", "note": "তড়িৎচাপ।"},
            {"title": "বল", "latex": "F=PA=Q^2/(2\\varepsilon_0 A)", "note": "Q = σA।"},
        ],
        assumptions=["সমান্তরাল পাত; প্রান্ত প্রভাব উপেক্ষিত"],
        questions=[
            {
                "examType": "Admission",
                "question": "ধারকের পাতদ্বয়ের বলের সূত্র কী?",
                "answer": "F=Q^2/(2\\varepsilon_0 A)",
            }
        ],
        trick="F = Q²/(2ε₀A) — চার্জ বাড়লে বল বাড়ে।",
        related=["capacitor-parallel-plate", "capacitor-energy", "dielectric-capacitor"],
        importance=2,
        order=160,
    ),
    # —— current-electricity ——
    formula(
        id="maximum-power-transfer",
        chapter="current-electricity",
        title="Maximum Power Transfer",
        title_bn="সর্বাধিক ক্ষমতা স্থানান্তর",
        summary="R_L = r হলে P_max",
        latex="P_{\\max}=\\dfrac{\\mathcal{E}^2}{4r}\\quad(R_L=r)",
        symbols=[
            {"symbol": "R_L", "meaning": "লোড রোধ", "unit": "Ω"},
            {"symbol": "r", "meaning": "অভ্যন্তরীণ রোধ", "unit": "Ω"},
            {"symbol": "\\mathcal{E}", "meaning": "তড়িচ্চালক বল", "unit": "V"},
        ],
        lead="লোড = অভ্যন্তরীণ রোধে লোডে সর্বোচ্চ ক্ষমতা।",
        steps=[
            {"title": "ক্ষমতা", "latex": "P=I^2 R_L=\\dfrac{\\mathcal{E}^2 R_L}{(R_L+r)^2}", "note": "I = ε/(R_L+r)।"},
            {"title": "শর্ত", "latex": "dP/dR_L=0\\Rightarrow R_L=r", "note": "তখন P_max = ε²/(4r)।"},
        ],
        assumptions=["ধ্রুব ε ও r; DC সার্কিট"],
        questions=[
            {
                "examType": "HSC",
                "question": "ε = 12 V, r = 2 Ω। সর্বোচ্চ ক্ষমতা কত?",
                "answer": "P_{\\max}=12^2/(4\\times2)=18\\ \\text{W}",
            }
        ],
        trick="R_L = r → P_max = ε²/4r।",
        related=["emf-internal-resistance", "joule-heating", "cells-series-parallel"],
        importance=3,
        order=150,
    ),
    # —— magnetic-current ——
    formula(
        id="helical-path-magnetic",
        chapter="magnetic-current",
        title="Helical Path in Magnetic Field",
        title_bn="চৌম্বক ক্ষেত্রে হেলিক্স পথ",
        summary="সমান্তরাল উপাংশ অপরিবর্তিত; লম্ব উপাংশে বৃত্ত",
        latex="r=\\dfrac{mv_\\perp}{qB},\\quad T=\\dfrac{2\\pi m}{qB},\\quad p=v_\\parallel T",
        symbols=[
            {"symbol": "v_\\perp", "meaning": "B-এর লম্ব বেগ উপাংশ", "unit": "m/s"},
            {"symbol": "v_\\parallel", "meaning": "B-এর সমান্তরাল উপাংশ", "unit": "m/s"},
            {"symbol": "p", "meaning": "পিচ", "unit": "m"},
        ],
        lead="θ কোণে প্রবেশ করলে পথ হেলিক্স — বৃত্ত + অক্ষীয় গতি।",
        steps=[
            {"title": "ব্যাসার্ধ", "latex": "r=mv\\sin\\theta/(qB)", "note": "v_⊥ = v sinθ।"},
            {"title": "পিচ", "latex": "p=v\\cos\\theta\\cdot T", "note": "এক পাক্কে অক্ষীয় অগ্রগতি।"},
        ],
        assumptions=["অভিন্ন B; শুধু চৌম্বক বল"],
        questions=[
            {
                "examType": "Admission",
                "question": "B-এর সমান্তরালে চার্জ ছাড়লে পথ কী?",
                "answer": "\\text{সরলরেখা (F=0)}",
            }
        ],
        trick="সমান্তরাল → সরল; লম্ব → বৃত্ত; কোণ → হেলিক্স।",
        related=["lorentz", "cyclotron-radius", "cyclotron-freq"],
        importance=3,
        order=370,
    ),
    # —— induction-ac ——
    formula(
        id="ac-generator-emf",
        chapter="induction-ac",
        title="AC Generator EMF",
        title_bn="AC জেনারেটরের তড়িচ্চালক বল",
        summary="ε = ε₀ sinωt",
        latex="\\mathcal{E}=NBA\\omega\\sin\\omega t=\\mathcal{E}_0\\sin\\omega t",
        symbols=[
            {"symbol": "N", "meaning": "কুণ্ডলীর পাক সংখ্যা", "unit": "—"},
            {"symbol": "A", "meaning": "ক্ষেত্রফল", "unit": "m²"},
            {"symbol": "\\omega", "meaning": "কৌণিক কম্পাঙ্ক", "unit": "rad/s"},
        ],
        lead="ঘূর্ণায়মান কুণ্ডলীতে ফ্লাক্সের পরিবর্তন → পর্যাবৃত্ত emf।",
        steps=[
            {"title": "ফ্লাক্স", "latex": "\\Phi=BA\\cos\\omega t", "note": "θ = ωt।"},
            {"title": "ফ্যারাডে", "latex": "\\mathcal{E}=-N d\\Phi/dt=NBA\\omega\\sin\\omega t", "note": "ε₀ = NBAω।"},
        ],
        assumptions=["অভিন্ন B; ধ্রুব ω"],
        questions=[
            {
                "examType": "HSC",
                "question": "AC জেনারেটরের চূড়া emf-এর সূত্র কী?",
                "answer": "\\mathcal{E}_0=NBA\\omega",
            }
        ],
        trick="ε₀ = NBAω — ঘূর্ণন দ্রুত হলে emf বাড়ে।",
        related=["faradays-law", "motional-emf", "ac-rms-values"],
        importance=3,
        order=180,
    ),
    formula(
        id="inductor-energy",
        chapter="induction-ac",
        title="Energy Stored in Inductor",
        title_bn="আবেশকে সঞ্চিত শক্তি",
        summary="U = ½ LI²",
        latex="U=\\tfrac12 L I^2",
        symbols=[
            {"symbol": "L", "meaning": "স্বয়ং আবেশ গুণাঙ্ক", "unit": "H"},
            {"symbol": "I", "meaning": "প্রবাহ", "unit": "A"},
            {"symbol": "U", "meaning": "চৌম্বক শক্তি", "unit": "J"},
        ],
        lead="ধারকের ½CV²-এর চৌম্বক প্রতিরূপ।",
        steps=[
            {"title": "শক্তি", "latex": "U=\\int\\mathcal{E}I\\,dt=\\tfrac12 LI^2", "note": "ε = L dI/dt।"},
        ],
        assumptions=["রৈখিক আবেশক; কেবল L"],
        questions=[
            {
                "examType": "Admission",
                "question": "L = 2 H, I = 3 A হলে সঞ্চিত শক্তি কত?",
                "answer": "U=\\tfrac12\\times2\\times9=9\\ \\text{J}",
            }
        ],
        trick="ধারক ½CV²; আবেশক ½LI²।",
        related=["self-inductance", "capacitor-energy", "lr-cr-transient"],
        importance=3,
        order=190,
    ),
    formula(
        id="lcr-q-factor",
        chapter="induction-ac",
        title="Q Factor & Bandwidth of LCR",
        title_bn="LCR-এর Q গুণক ও ব্যান্ডউইডথ",
        summary="Q = ω₀L/R; Δω = R/L",
        latex="Q=\\dfrac{\\omega_0 L}{R}=\\dfrac{1}{R}\\sqrt{\\dfrac{L}{C}},\\quad \\Delta\\omega=\\dfrac{R}{L}",
        symbols=[
            {"symbol": "Q", "meaning": "গুণমান গুণক", "unit": "—"},
            {"symbol": "\\Delta\\omega", "meaning": "ব্যান্ডউইডথ", "unit": "rad/s"},
        ],
        lead="Q বড় = তীক্ষ্ণ অনুরণন; ব্যান্ডউইডথ ছোট।",
        steps=[
            {"title": "Q", "latex": "Q=\\omega_0 L/R", "note": "অনুরণনে।"},
            {"title": "ব্যান্ডউইডথ", "latex": "\\Delta f=f_0/Q", "note": "অর্ধ-ক্ষমতা বিন্দুদ্বয়ের ব্যবধান।"},
        ],
        assumptions=["শ্রেণি LCR; ছোট ক্ষয়"],
        questions=[
            {
                "examType": "HSC",
                "question": "Q ও ব্যান্ডউইডথের সম্পর্ক কী?",
                "answer": "\\Delta\\omega=\\omega_0/Q\\ (=R/L)",
            }
        ],
        trick="Q বাড়লে অনুরণন তীক্ষ্ণ, ব্যান্ড সরু।",
        related=["resonance-frequency", "ac-impedance", "lc-resonance-freq"],
        importance=2,
        order=200,
    ),
    # —— geometric-optics ——
    formula(
        id="glass-slab-lateral-shift",
        chapter="geometric-optics",
        title="Lateral Shift by Glass Slab",
        title_bn="কাচের স্ল্যাবে পার্শ্ব সরণ",
        summary="t(1 − 1/μ) sin i / cos r",
        latex="d=t\\,\\dfrac{\\sin(i-r)}{\\cos r}\\approx t\\left(1-\\dfrac{1}{n}\\right)\\ (\\text{near-normal})",
        symbols=[
            {"symbol": "t", "meaning": "স্ল্যাবের পুরুত্ব", "unit": "m"},
            {"symbol": "n", "meaning": "প্রতিসরাঙ্ক", "unit": "—"},
            {"symbol": "d", "meaning": "পার্শ্ব সরণ", "unit": "m"},
        ],
        lead="স্ল্যাব রশ্মি সমান্তরাল রাখে কিন্তু পার্শ্বে সরায়।",
        steps=[
            {
                "title": "সরণ",
                "latex": "d=t\\,\\dfrac{\\sin(i-r)}{\\cos r}",
                "note": "প্রায় ব্যবহার্য রূপ।",
            },
            {
                "title": "ক্ষুদ্র কোণ",
                "latex": "d\\approx t(1-1/n)",
                "note": "লম্বের কাছাকাছি আপতনে।",
            },
        ],
        assumptions=["সমান্তরাল মুখ; বায়ু–কাচ–বায়ু"],
        questions=[
            {
                "examType": "HSC",
                "question": "লম্ব আপতনের কাছাকাছি পার্শ্ব সরণের সরল সূত্র কী?",
                "answer": "d\\approx t(1-1/n)",
            }
        ],
        trick="মোটা স্ল্যাব বা বড় n → বেশি সরণ।",
        related=["snell-law", "apparent-depth", "critical-angle"],
        importance=2,
        order=170,
    ),
    formula(
        id="prism-dispersive-power",
        chapter="geometric-optics",
        title="Dispersive Power of Prism",
        title_bn="প্রিজমের বিচ্ছুরণ ক্ষমতা",
        summary="ω = (μv − μr)/(μy − 1)",
        latex="\\omega=\\dfrac{\\mu_v-\\mu_r}{\\mu-1}=\\dfrac{\\delta_v-\\delta_r}{\\delta}",
        symbols=[
            {"symbol": "\\mu_v,\\mu_r", "meaning": "বেগুনি ও লালের প্রতিসরাঙ্ক", "unit": "—"},
            {"symbol": "\\omega", "meaning": "বিচ্ছুরণ ক্ষমতা", "unit": "—"},
        ],
        lead="কৌণিক বিচ্ছুরণ / গড় বিচ্যুতি = বিচ্ছুরণ ক্ষমতা।",
        steps=[
            {"title": "বিচ্যুতি", "latex": "\\delta=(\\mu-1)A", "note": "পাতলা প্রিজম।"},
            {"title": "বিচ্ছুরণ", "latex": "\\delta_v-\\delta_r=(\\mu_v-\\mu_r)A", "note": "ω = (δv−δr)/δ।"},
        ],
        assumptions=["পাতলা প্রিজম; ক্ষুদ্র কোণ"],
        questions=[
            {
                "examType": "Admission",
                "question": "বিচ্ছুরণ ক্ষমতার সূত্র কী?",
                "answer": "\\omega=(\\mu_v-\\mu_r)/(\\mu-1)",
            }
        ],
        trick="(μv−μr) ÷ (μ−1) — উপাদানের ধর্ম।",
        related=["prism-deviation", "snell-law"],
        importance=2,
        order=180,
    ),
    # —— wave-optics ——
    formula(
        id="ydse-fringe-shift-plate",
        chapter="wave-optics",
        title="YDSE Fringe Shift by Thin Plate",
        title_bn="পাতলা পাতের YDSE ডোরা সরণ",
        summary="সরণ = (μ − 1)t D/d",
        latex="\\Delta y=\\dfrac{(\\mu-1)t\\,D}{d}",
        symbols=[
            {"symbol": "t", "meaning": "পাতের পুরুত্ব", "unit": "m"},
            {"symbol": "\\mu", "meaning": "পাতের প্রতিসরাঙ্ক", "unit": "—"},
            {"symbol": "D", "meaning": "স্লিট থেকে পর্দা", "unit": "m"},
            {"symbol": "d", "meaning": "স্লিট ব্যবধান", "unit": "m"},
        ],
        lead="এক পথে অপটিক্যাল পথ বাড়লে পুরো প্যাটার্ন সরে।",
        steps=[
            {"title": "পথ বৃদ্ধি", "latex": "(\\mu-1)t", "note": "বায়ুর বদলে কাচ।"},
            {"title": "সরণ", "latex": "\\Delta y=(\\mu-1)t\\cdot D/d", "note": "যে পথে পাত, সেদিকে কেন্দ্র সরে।"},
        ],
        assumptions=["পাতলা পাত; এক স্লিটের সামনে"],
        questions=[
            {
                "examType": "BUET",
                "question": "YDSE-এ পাতলা পাত বসালে কেন্দ্রীয় উজ্জ্বল ডোরা কোন দিকে সরে?",
                "answer": "\\text{যে স্লিটের সামনে পাত সেদিকে}",
            }
        ],
        trick="সরণ = (μ−1)t · (D/d)।",
        related=["youngs-double-slit", "interference-conditions", "optical-path-phase"],
        importance=3,
        order=120,
    ),
    formula(
        id="single-slit-central-width",
        chapter="wave-optics",
        title="Central Maximum Width (Single Slit)",
        title_bn="একক স্লিটে কেন্দ্রীয় চূড়ার প্রস্থ",
        summary="β₀ = 2λD/a",
        latex="\\beta_0=\\dfrac{2\\lambda D}{a}",
        symbols=[
            {"symbol": "a", "meaning": "স্লিট প্রস্থ", "unit": "m"},
            {"symbol": "\\beta_0", "meaning": "কেন্দ্রীয় উজ্জ্বলতার প্রস্থ", "unit": "m"},
        ],
        lead="প্রথম নিম্নদ্বয়ের ব্যবধানই কেন্দ্রীয় চূড়ার প্রস্থ।",
        steps=[
            {"title": "প্রথম নিম্ন", "latex": "a\\sin\\theta=\\lambda", "note": "θ ≈ y/D।"},
            {"title": "প্রস্থ", "latex": "\\beta_0=2\\lambda D/a", "note": "পার্শ্ব চূড়া অর্ধেক চওড়া।"},
        ],
        assumptions=["Fraunhofer অপবর্তন; ক্ষুদ্র কোণ"],
        questions=[
            {
                "examType": "HSC",
                "question": "কেন্দ্রীয় চূড়ার প্রস্থের সূত্র কী?",
                "answer": "\\beta_0=2\\lambda D/a",
            }
        ],
        trick="কেন্দ্রীয় = ২ × (λD/a)।",
        related=["single-slit-diffraction", "diffraction-grating"],
        importance=2,
        order=130,
    ),
    # —— modern-physics ——
    formula(
        id="rydberg-formula",
        chapter="modern-physics",
        title="Rydberg Formula",
        title_bn="রিডবার্গ সূত্র",
        summary="হাইড্রোজেন বর্ণালির তরঙ্গ সংখ্যা",
        latex="\\dfrac{1}{\\lambda}=R\\left(\\dfrac{1}{n_1^2}-\\dfrac{1}{n_2^2}\\right)",
        symbols=[
            {"symbol": "R", "meaning": "রিডবার্গ ধ্রুবক", "unit": "m⁻¹"},
            {"symbol": "n_1,n_2", "meaning": "স্তর সংখ্যা (n₂ > n₁)", "unit": "—"},
        ],
        lead="n₂ → n₁ অবক্ষয়ে নির্দিষ্ট তরঙ্গদৈর্ঘ্য।",
        steps=[
            {"title": "লাইম্যান", "latex": "n_1=1\\ (\\text{UV})", "note": "গ্রাউন্ড স্টেটে।"},
            {"title": "বালমার", "latex": "n_1=2\\ (\\text{দৃশ্য})", "note": "Hα, Hβ…"},
            {"title": "পাসচেন", "latex": "n_1=3\\ (\\text{IR})", "note": "অবলোহিত।"},
        ],
        assumptions=["হাইড্রোজেনসদৃশ; নিশ্চল নিউক্লিয়াস"],
        questions=[
            {
                "examType": "HSC",
                "question": "বালমার সিরিজে n₁ কত?",
                "answer": "n_1=2",
            }
        ],
        trick="লাইম্যান 1, বালমার 2, পাসচেন 3।",
        related=["bohr-energy-levels", "bohr-frequency-condition", "bohr-radius-hydrogen"],
        importance=3,
        order=180,
    ),
    formula(
        id="relativistic-energy-momentum",
        chapter="modern-physics",
        title="Relativistic Energy–Momentum",
        title_bn="আপেক্ষিকতাবাদী শক্তি–ভরবেগ",
        summary="E² = p²c² + m²c⁴",
        latex="E^2=p^2 c^2+m^2 c^4,\\quad E=\\gamma mc^2",
        symbols=[
            {"symbol": "E", "meaning": "মোট শক্তি", "unit": "J"},
            {"symbol": "p", "meaning": "ভরবেগ", "unit": "kg·m/s"},
            {"symbol": "\\gamma", "meaning": "1/√(1−v²/c²)", "unit": "—"},
        ],
        lead="বিশ্রাম শক্তি mc²; ফোটনে m = 0 → E = pc।",
        steps=[
            {"title": "লরেন্টজ", "latex": "\\gamma=1/\\sqrt{1-v^2/c^2}", "note": "v → c এ γ → ∞।"},
            {"title": "সম্পর্ক", "latex": "E^2=p^2c^2+m^2c^4", "note": "KE = E − mc²।"},
        ],
        assumptions=["বিশেষ আপেক্ষিকতা"],
        questions=[
            {
                "examType": "Admission",
                "question": "ফোটনের শক্তি–ভরবেগ সম্পর্ক কী?",
                "answer": "E=pc\\ (m=0)",
            }
        ],
        trick="E² = p²c² + (mc²)² — পিথাগোরাস।",
        related=["mass-energy-photoelectric", "de-broglie-wavelength", "compton-effect"],
        importance=3,
        order=190,
    ),
    formula(
        id="time-dilation-length-contraction",
        chapter="modern-physics",
        title="Time Dilation & Length Contraction",
        title_bn="কাল দীর্ঘায়ন ও দৈর্ঘ্য সংকোচন",
        summary="Δt = γ Δt₀; L = L₀/γ",
        latex="\\Delta t=\\gamma\\Delta t_0,\\quad L=L_0\\sqrt{1-v^2/c^2}",
        symbols=[
            {"symbol": "\\Delta t_0", "meaning": "প্রকৃত সময়", "unit": "s"},
            {"symbol": "L_0", "meaning": "প্রকৃত দৈর্ঘ্য", "unit": "m"},
            {"symbol": "v", "meaning": "আপেক্ষিক বেগ", "unit": "m/s"},
        ],
        lead="চলমান ঘড়ি ধীর; চলমান দণ্ড গতির দিকে ছোট।",
        steps=[
            {"title": "কাল", "latex": "\\Delta t=\\gamma\\Delta t_0", "note": "প্রকৃত সময় স্থির ঘড়িতে।"},
            {"title": "দৈর্ঘ্য", "latex": "L=L_0/\\gamma", "note": "শুধু গতির সমান্তরালে।"},
        ],
        assumptions=["জড় কাঠামো; বিশেষ আপেক্ষিকতা"],
        questions=[
            {
                "examType": "HSC",
                "question": "গতির লম্ব দিকে দৈর্ঘ্য সংকোচন হয় কি?",
                "answer": "\\text{না — শুধু সমান্তরালে}",
            }
        ],
        trick="চলমান ঘড়ি ধীর; চলমান দণ্ড ছোট।",
        related=["relativistic-energy-momentum", "mass-energy-photoelectric"],
        importance=3,
        order=200,
    ),
    formula(
        id="nuclear-radius-density",
        chapter="modern-physics",
        title="Nuclear Radius & Density",
        title_bn="নিউক্লিয়াসের ব্যাসার্ধ ও ঘনত্ব",
        summary="R = R₀ A^(1/3); ঘনত্ব প্রায় ধ্রুব",
        latex="R=R_0 A^{1/3},\\quad \\rho\\approx\\text{constant}",
        symbols=[
            {"symbol": "A", "meaning": "ভর সংখ্যা", "unit": "—"},
            {"symbol": "R_0", "meaning": "≈ 1.2 fm", "unit": "m"},
        ],
        lead="আয়তন ∝ A বলে ঘনত্ব প্রায় সব নিউক্লিয়াসে সমান।",
        steps=[
            {"title": "ব্যাসার্ধ", "latex": "R=R_0 A^{1/3}", "note": "R₀ ≈ 1.2×10⁻¹⁵ m।"},
            {"title": "ঘনত্ব", "latex": "\\rho=\\dfrac{A m_p}{\\tfrac43\\pi R^3}\\approx\\text{const}", "note": "~10¹⁷ kg/m³।"},
        ],
        assumptions=["গোলীয় নিউক্লিয়াস"],
        questions=[
            {
                "examType": "Admission",
                "question": "A চারগুণ হলে R কতগুণ হয়?",
                "answer": "R\\propto A^{1/3}\\Rightarrow 4^{1/3}\\approx1.6\\ \\text{গুণ}",
            }
        ],
        trick="R ∝ A^(1/3) — ঘনত্ব প্রায় ধ্রুব।",
        related=["mass-defect-binding-energy", "radioactive-decay", "nuclear-reactions"],
        importance=2,
        order=210,
    ),
    # —— semiconductor ——
    formula(
        id="full-wave-rectifier",
        chapter="semiconductor",
        title="Full-Wave Rectifier",
        title_bn="পূর্ণতরঙ্গ দিষ্টকারক",
        summary="DC গড় ও দক্ষতা",
        latex="I_{\\dc}=\\dfrac{2I_0}{\\pi},\\quad \\eta\\approx81.2\\%",
        symbols=[
            {"symbol": "I_0", "meaning": "চূড়া প্রবাহ", "unit": "A"},
            {"symbol": "\\eta", "meaning": "দিষ্টকরণ দক্ষতা", "unit": "%"},
        ],
        lead="উভয় অর্ধচক্রই ব্যবহার — অর্ধতরঙ্গের দ্বিগুণ গড়।",
        steps=[
            {"title": "গড়", "latex": "I_{\\dc}=2I_0/\\pi", "note": "অর্ধতরঙ্গে I₀/π।"},
            {"title": "দক্ষতা", "latex": "\\eta=P_{\\dc}/P_{\\ac}\\approx81.2\\%", "note": "অর্ধে ~40.6%।"},
        ],
        assumptions=["আদর্শ ডায়োড; রোধক লোড"],
        questions=[
            {
                "examType": "HSC",
                "question": "পূর্ণতরঙ্গ দিষ্টকারকের আদর্শ দক্ষতা আনুমানিক কত?",
                "answer": "81.2\\%",
            }
        ],
        trick="পূর্ণ ≈ ৮১%; অর্ধ ≈ ৪১%।",
        related=["half-wave-rectifier", "pn-junction-diode", "rectifier-ripple"],
        importance=3,
        order=140,
    ),
    formula(
        id="transistor-current-gains",
        chapter="semiconductor",
        title="Transistor α and β Relation",
        title_bn="ট্রানজিস্টর α–β সম্পর্ক",
        summary="β = α/(1−α)",
        latex="\\beta=\\dfrac{\\alpha}{1-\\alpha},\\quad \\alpha=\\dfrac{\\beta}{1+\\beta},\\quad I_E=I_B+I_C",
        symbols=[
            {"symbol": "\\alpha", "meaning": "I_C/I_E", "unit": "—"},
            {"symbol": "\\beta", "meaning": "I_C/I_B", "unit": "—"},
        ],
        lead="α ≈ 0.98–0.99; β সাধারণত 50–200।",
        steps=[
            {"title": "সংজ্ঞা", "latex": "\\alpha=I_C/I_E,\\ \\beta=I_C/I_B", "note": "CE-তে β।"},
            {"title": "সম্পর্ক", "latex": "\\beta=\\alpha/(1-\\alpha)", "note": "I_E = I_B + I_C থেকে।"},
        ],
        assumptions=["সক্রিয় অঞ্চল; npn/pnp"],
        questions=[
            {
                "examType": "Admission",
                "question": "α = 0.98 হলে β কত?",
                "answer": "\\beta=0.98/0.02=49",
            }
        ],
        trick="β = α/(1−α) — α 1-এর কাছে হলে β বড়।",
        related=["transistor-alpha-beta", "transistor-ce-relations", "amplifier-gain"],
        importance=3,
        order=150,
    ),
    # —— astronomy ——
    formula(
        id="schwarzschild-radius",
        chapter="astronomy",
        title="Schwarzschild Radius",
        title_bn="শোয়ার্জশিল্ড ব্যাসার্ধ",
        summary="কৃষ্ণগহ্বরের ঘটনা দিগন্ত",
        latex="R_s=\\dfrac{2GM}{c^2}",
        symbols=[
            {"symbol": "R_s", "meaning": "শোয়ার্জশিল্ড ব্যাসার্ধ", "unit": "m"},
            {"symbol": "M", "meaning": "ভর", "unit": "kg"},
        ],
        lead="পালানোর বেগ = c হলে যে ব্যাসার্ধ — ঘটনা দিগন্ত।",
        steps=[
            {"title": "escape = c", "latex": "\\sqrt{2GM/R}=c\\Rightarrow R=2GM/c^2", "note": "নিউটনীয় আভাস; আপেক্ষিকতায় একই রূপ।"},
        ],
        assumptions=["স্থির, ঘূর্ণনহীন কৃষ্ণগহ্বর"],
        questions=[
            {
                "examType": "HSC",
                "question": "শোয়ার্জশিল্ড ব্যাসার্ধের সূত্র কী?",
                "answer": "R_s=2GM/c^2",
            }
        ],
        trick="R_s = 2GM/c² — সূর্যের ≈ 3 km।",
        related=["escape-velocity-planet", "hubble-law", "planetary-escape-speed"],
        importance=2,
        order=110,
    ),
    formula(
        id="cosmological-redshift",
        chapter="astronomy",
        title="Cosmological Redshift & Hubble Age",
        title_bn="মহাজাগতিক লোহিত সরণ ও হাবল বয়স",
        summary="z ≈ v/c; t_H ≈ 1/H₀",
        latex="z=\\dfrac{\\Delta\\lambda}{\\lambda}\\approx\\dfrac{v}{c},\\quad t_H\\approx\\dfrac{1}{H_0}",
        symbols=[
            {"symbol": "z", "meaning": "লোহিত সরণ", "unit": "—"},
            {"symbol": "H_0", "meaning": "হাবল ধ্রুবক", "unit": "s⁻¹ বা km/s/Mpc"},
        ],
        lead="দূর ছায়াপথের আলো লাল সরে — সম্প্রসারণের প্রমাণ।",
        steps=[
            {"title": "লোহিত সরণ", "latex": "z=\\Delta\\lambda/\\lambda\\approx v/c\\ (v\\ll c)", "note": "ডপলার আভাস।"},
            {"title": "হাবল বয়স", "latex": "t_H=1/H_0", "note": "আনুমানিক মহাবিশ্বের বয়স।"},
        ],
        assumptions=["নিম্ন z; হাবল প্রবাহ প্রধান"],
        questions=[
            {
                "examType": "Admission",
                "question": "হাবল বয়সের সরল আনুমানিক সূত্র কী?",
                "answer": "t_H\\approx1/H_0",
            }
        ],
        trick="z ≈ v/c; বয়স ≈ 1/H₀।",
        related=["hubble-law", "parallax-distance"],
        importance=2,
        order=120,
    ),
]


def polish_file(path: Path) -> bool:
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = False

    # Fix fresnel typo
    if data.get("id") == "fresnel-biprism" and "anel" in data.get("titleBn", ""):
        data["titleBn"] = "ফ্রেসনেল বাইপ্রিজম"
        changed = True

    # Improve continuity-equation
    if data.get("id") == "continuity-equation":
        data.update(
            {
                "summary": "অসংকোচনযোগ্য স্থির প্রবাহে A₁v₁ = A₂v₂",
                "latex": "A_1 v_1=A_2 v_2\\quad(\\rho\\ \\text{ধ্রুব}\\Rightarrow \\rho Av=\\text{const})",
                "symbols": [
                    {"symbol": "A", "meaning": "প্রস্থচ্ছেদের ক্ষেত্রফল", "unit": "m²"},
                    {"symbol": "v", "meaning": "প্রবাহ বেগ", "unit": "m/s"},
                    {"symbol": "\\rho", "meaning": "ঘনত্ব", "unit": "kg/m³"},
                ],
                "derivation": {
                    "lead": "একই সময়ে প্রবেশ ও নির্গমন ভর সমান — ভর সংরক্ষণ।",
                    "steps": [
                        {
                            "title": "ভর হার",
                            "latex": "\\dot m=\\rho A v",
                            "note": "Δt সময়ে ভর = ρA v Δt।",
                        },
                        {
                            "title": "অসংকোচনযোগ্য",
                            "latex": "A_1 v_1=A_2 v_2",
                            "note": "সরু স্থানে বেগ বেশি।",
                        },
                    ],
                    "assumptions": ["স্থির প্রবাহ", "অসংকোচনযোগ্য তরল", "একই নলপথ"],
                },
                "questions": [
                    {
                        "examType": "HSC",
                        "question": "নলের ব্যাস অর্ধেক হলে অসংকোচনযোগ্য প্রবাহে বেগ কতগুণ হয়?",
                        "answer": "A\\propto d^2\\Rightarrow A_2=A_1/4\\Rightarrow v_2=4v_1",
                    }
                ],
                "memorize": {
                    "trick": "সরু জায়গায় বেগ বেশি — Av ধ্রুব।",
                    "steps": ["ভর হার ρAv ধ্রুব", "ρ ধ্রুব হলে Av ধ্রুব"],
                },
                "related": ["bernoulli-equation", "torricelli-theorem", "continuity-fluid"],
                "importance": 3,
                "tags": tags(3),
            }
        )
        changed = True

    if data.get("id") == "continuity-fluid":
        # Point to the stronger twin; enrich lightly
        data["summary"] = "ধারাবাহিকতা: ভর প্রবাহ সংরক্ষণ (continuity-equation দেখুন)"
        data["related"] = list(
            dict.fromkeys((data.get("related") or []) + ["continuity-equation", "bernoulli-equation"])
        )
        data["questions"] = [
            {
                "examType": "Admission",
                "question": "অসংকোচনযোগ্য প্রবাহে A₁ = 2A₂ হলে v₂/v₁ কত?",
                "answer": "v_2/v_1=A_1/A_2=2",
            }
        ]
        changed = True

    if data.get("id") == "hubble-law":
        data.update(
            {
                "summary": "ছায়াপথের দূরত্বের সাথে প্রত্যাগমন বেগ সমানুপাতিক",
                "latex": "v=H_0 d",
                "symbols": [
                    {"symbol": "v", "meaning": "প্রত্যাগমন বেগ", "unit": "km/s"},
                    {"symbol": "H_0", "meaning": "হাবল ধ্রুবক", "unit": "km/s/Mpc"},
                    {"symbol": "d", "meaning": "দূরত্ব", "unit": "Mpc"},
                ],
                "derivation": {
                    "lead": "মহাবিশ্ব সম্প্রসারণে দূর ছায়াপথ দ্রুত সরে — হাবলের সূত্র।",
                    "steps": [
                        {"title": "সূত্র", "latex": "v=H_0 d", "note": "নিম্ন লোহিত সরণে প্রযোজ্য।"},
                        {
                            "title": "বয়স আভাস",
                            "latex": "t_H\\approx1/H_0",
                            "note": "হাবল সময় ≈ মহাবিশ্বের বয়স।",
                        },
                    ],
                    "assumptions": ["হাবল প্রবাহ প্রধান", "নিম্ন z"],
                },
                "questions": [
                    {
                        "examType": "HSC",
                        "question": "H₀ = 70 km/s/Mpc ও d = 10 Mpc হলে v কত?",
                        "answer": "v=70\\times10=700\\ \\text{km/s}",
                    }
                ],
                "memorize": {
                    "trick": "দূরত্ব বাড়লে প্রত্যাগমন বেগ বাড়ে — v = H₀d।",
                    "steps": ["v সমানুপাতিক d", "H₀ ≈ 70 km/s/Mpc"],
                },
                "related": [
                    "cosmological-redshift",
                    "parallax-distance",
                    "hubble-recession-law",
                ],
                "importance": 3,
                "tags": tags(3),
            }
        )
        changed = True

    if data.get("id") == "hubble-recession-law":
        data["title"] = "Hubble Recession (Detail)"
        data["titleBn"] = "হাবল প্রত্যাগমন — বিস্তারিত"
        data["summary"] = "v = H₀d; H₀-এর একক ও ব্যবহার"
        data["related"] = list(
            dict.fromkeys((data.get("related") or []) + ["hubble-law", "cosmological-redshift"])
        )
        data["questions"] = [
            {
                "examType": "Admission",
                "question": "H₀-এর প্রচলিত একক কী?",
                "answer": "\\text{km/s/Mpc}",
            }
        ]
        changed = True

    if data.get("id") == "heat-conduction":
        data.update(
            {
                "summary": "তাপ পরিবহণ হার — ফুরিয়ার সূত্র",
                "latex": "\\dfrac{dQ}{dt}=kA\\dfrac{\\Delta T}{L}",
                "symbols": [
                    {"symbol": "k", "meaning": "তাপ পরিবাহিতা", "unit": "W/(m·K)"},
                    {"symbol": "A", "meaning": "প্রস্থচ্ছেদ", "unit": "m²"},
                    {"symbol": "L", "meaning": "পুরুত্ব", "unit": "m"},
                    {"symbol": "\\Delta T", "meaning": "তাপমাত্রা পার্থক্য", "unit": "K"},
                ],
                "derivation": {
                    "lead": "তাপ উষ্ণ থেকে শীতল দিকে প্রবাহিত হয় — হার ক্ষেত্রফল ও ঢালের সমানুপাতিক।",
                    "steps": [
                        {
                            "title": "ফুরিয়ার",
                            "latex": "H=kA\\Delta T/L",
                            "note": "H = dQ/dt।",
                        },
                        {
                            "title": "শ্রেণি স্ল্যাব",
                            "latex": "H=\\dfrac{A\\Delta T_{\\total}}{\\sum(L_i/k_i)}",
                            "note": "তাপ রোধ যোগ।",
                        },
                    ],
                    "assumptions": ["স্থির অবস্থা", "একমাত্রিক প্রবাহ"],
                },
                "questions": [
                    {
                        "examType": "HSC",
                        "question": "A ও ΔT দ্বিগুণ, L অপরিবর্তিত থাকলে H কতগুণ?",
                        "answer": "H\\propto A\\Delta T\\Rightarrow 4\\ \\text{গুণ}",
                    }
                ],
                "related": ["thermal-conduction-rate", "newton-cooling", "stefan-boltzmann-law"],
                "importance": 3,
                "tags": tags(3),
            }
        )
        changed = True

    if data.get("id") == "charge-potential-energy":
        # Remove unrelated Gauss content if present in lead
        lead = data.get("derivation", {}).get("lead", "")
        if "Gauss" in lead or "গাউস" in lead or "gauss" in lead.lower():
            data["derivation"]["lead"] = (
                "বিন্দু চার্জসমূহের ব্যবস্থায় স্থিতিশক্তি — অসীম থেকে জড়ো করার কাজ।"
            )
            changed = True
        data["latex"] = "U=\\dfrac{1}{4\\pi\\varepsilon_0}\\sum_{i<j}\\dfrac{q_i q_j}{r_{ij}}"
        data["summary"] = "বিন্দু চার্জ ব্যবস্থার স্থিতিশক্তি"
        data["symbols"] = [
            {"symbol": "U", "meaning": "স্থিতিশক্তি", "unit": "J"},
            {"symbol": "q_i,q_j", "meaning": "চার্জদ্বয়", "unit": "C"},
            {"symbol": "r_{ij}", "meaning": "দূরত্ব", "unit": "m"},
        ]
        data["questions"] = [
            {
                "examType": "HSC",
                "question": "দুই সমান q চার্জ r দূরে থাকলে U কত?",
                "answer": "U=\\dfrac{1}{4\\pi\\varepsilon_0}\\dfrac{q^2}{r}",
            }
        ]
        data["related"] = ["coulombs-law", "electric-potential", "capacitor-energy"]
        changed = True

    if data.get("id") == "percentage-error":
        data["symbols"] = [
            {"symbol": "\\Delta x", "meaning": "পরম ত্রুটি", "unit": "x-এর একক"},
            {"symbol": "x", "meaning": "পরিমাপিত মান", "unit": "—"},
            {"symbol": "\\delta x\\%", "meaning": "শতকরা ত্রুটি", "unit": "%"},
        ]
        data["questions"] = [
            {
                "examType": "HSC",
                "question": "x = 50.0 ± 0.5 হলে শতকরা ত্রুটি কত?",
                "answer": "\\delta x\\%=(0.5/50)\\times100\\%=1\\%",
            }
        ]
        data["related"] = [
            "absolute-relative-error",
            "error-propagation-sum-difference",
            "error-propagation-product",
        ]
        changed = True

    # Fix glass-slab latex if we wrote a bad one - handled in NEW list carefully
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def fix_glass_slab_latex():
    """Sanitize any accidental bad latex in glass-slab if written."""
    path = ROOT / "chapters/geometric-optics/formulas/glass-slab-lateral-shift.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    data["latex"] = (
        "d=t\\,\\dfrac{\\sin(i-r)}{\\cos r}"
        "\\approx t\\left(1-\\dfrac{1}{n}\\right)\\ (\\text{near-normal})"
    )
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    for item in NEW:
        write(item)
    fix_glass_slab_latex()

    polished = 0
    for path in sorted(ROOT.glob("chapters/*/formulas/*.json")):
        if polish_file(path):
            polished += 1
            print(f"~ polish {path.parent.parent.name}/{path.stem}")

    print(f"\nDone. Added {len(NEW)} new, polished {polished} existing.")


if __name__ == "__main__":
    main()
