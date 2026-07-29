#!/usr/bin/env python3
"""Upgrade weak memorize.trick into mnemonic-style tips (Bangla + cue)."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "subjects"

# Curated mnemonic upgrades keyed by formula id.
TRICKS: dict[str, dict] = {
    "kinematic-equation-v": {
        "trick": "বেগ বাড়ে সময় দিয়ে: v = u + at — ‘আদি + ত্বরণ×সময়’।",
        "steps": ["u দিয়ে শুরু", "প্রতি সেকেন্ডে a যোগ"],
    },
    "kinematic-equation-s": {
        "trick": "সরণ = আদি×সময় + অর্ধেক ত্বরণ×সময়² — ‘ut + ½at²’ গান করে মনে রাখো।",
        "steps": ["প্রথম অংশ ut", "দ্বিতীয় ½at²"],
    },
    "kinematic-equation-v2": {
        "trick": "সময় নেই? v² = u² + 2as — ‘দুই অ্যাস’ মনে রাখো।",
        "steps": ["t বাদ", "2as যোগ"],
    },
    "heat-capacity-specific": {
        "trick": "Q = mcΔT — ‘মোল নয়, ভর×c×তাপমাত্রা’। পানি c≈4200।",
        "steps": ["m×c×ΔT", "দশাবদলে আলাদা L/H"],
    },
    "bohr-frequency-condition": {
        "trick": "ফোটন শক্তি = স্তরের ফারাক: hf = ΔE — সিঁড়ি থেকে লাফ।",
        "steps": ["উঁচু→নিচু = নির্গমন", "নিচু→উঁচু = শোষণ"],
    },
    "continuity-fluid": {
        "trick": "পাইপ সরু = বেগ বেশি: Av = ধ্রুব — ‘এরিয়া×বেগ এক’।",
        "steps": ["A₁v₁=A₂v₂", "বার্নোলিতে চাপ কমে"],
    },
    "centripetal-acceleration": {
        "trick": "কেন্দ্রে টানে: a_c = v²/r = ω²r — বড় বেগ/ছোট r = বেশি টান।",
        "steps": ["দিক কেন্দ্রে", "F=ma_c"],
    },
    "youngs-modulus": {
        "trick": "Y = FL/(AΔL) — ‘বল×দৈর্ঘ্য / ক্ষেত্র×প্রসারণ’; ইস্পাত শক্ত = Y বড়।",
        "steps": ["stress/strain", "একক Pa"],
    },
    "lc-resonance-freq": {
        "trick": "অনুরণন: f₀ = 1/(2π√LC) — L·C গুণের বর্গমূল ভাগ।",
        "steps": ["X_L=X_C", "Z_min=R"],
    },
    "capillary-rise": {
        "trick": "সরু নল = বেশি উঠে: h = 2S cosθ/(ρgr) — r ছোট h বড়।",
        "steps": ["পারদে পতন (θ>90°)", "পানিতে উত্থান"],
    },
    "stokes-law": {
        "trick": "সান্দ্র বল 6πηrv; প্রান্তিক বেগ ∝ r² — বড় গোলক দ্রুত পড়ে।",
        "steps": ["F=6πηrv", "v_t∝r²"],
    },
    "bernoulli-equation": {
        "trick": "বেগ বাড়লে চাপ কমে — বিমান ডানা ও ভেঞ্চুরির একই গল্প।",
        "steps": ["P+½ρv²+ρgh ধ্রুব", "উচ্চতা এক হলে সরল"],
    },
    "ac-power-factor": {
        "trick": "cosφ = R/Z — শুধু রোধ কাজ করে; P=VI cosφ।",
        "steps": ["φ=0 হলে PF=1", "শুধু L/C তে PF=0"],
    },
    "activity-mean-life": {
        "trick": "A=λN; গড় আয়ু τ≈1.44×অর্ধায়ু — τ > T½ সবসময়।",
        "steps": ["A∝N", "τ=1/λ"],
    },
    "gravitational-pe": {
        "trick": "∞-এ শূন্য, কাছে ঋণাত্মক: U=−GMm/r; ছোট উচ্চতায় mgh।",
        "steps": ["রকেটে −GMm/r", "টাওয়ারে mgh"],
    },
    "center-of-mass": {
        "trick": "ভরকেন্দ্র = ভর-ওজনকৃত গড় অবস্থান — ভারী দিক টানে।",
        "steps": ["x=Σmx/Σm", "বাহ্যিক বলহীন v_cm ধ্রুব"],
    },
    "work-by-constant-force": {
        "trick": "W=Fs cosθ — লম্ব বল কাজ করে না (θ=90°→0)।",
        "steps": ["cos0=1 সর্বোচ্চ", "বিপরীত বল ঋণাত্মক কাজ"],
    },
    "displacement-velocity-accel": {
        "trick": "সরণ→বেগ→ত্বরণ = একবার করে অবকলন: v=ds/dt, a=dv/dt।",
        "steps": ["ঢাল = নিচের রাশি", "লেখচিত্রে পড়ো"],
    },
    "graph-slope-area": {
        "trick": "s–t ঢাল=বেগ; v–t ঢাল=ত্বরণ; v–t ক্ষেত্রফল=সরণ।",
        "steps": ["ঢাল নিচে যাও", "ক্ষেত্রফল সরণ"],
    },
    "poiseuille-law": {
        "trick": "Q∝r⁴ — নল একটু চওড়া হলে প্রবাহ অনেক বাড়ে।",
        "steps": ["Q=πΔPr⁴/(8ηL)", "রক্তনালীর কথা ভাবো"],
    },
    "surface-tension": {
        "trick": "S=F/l; সাবান ফিল্মে দুই পৃষ্ঠ → F=2Sl।",
        "steps": ["একক N/m", "কাজ=S×ΔA"],
    },
    "excess-pressure-bubble": {
        "trick": "ফোঁটা 2S/r, সাবান বুদবুদ 4S/r — সাবানে দুই দেয়াল।",
        "steps": ["এক পৃষ্ঠ=২", "দুই পৃষ্ঠ=৪"],
    },
    "hookes-law-stress-strain": {
        "trick": "স্থিতিস্থাপক সীমায় stress∝strain; Y=stress/strain।",
        "steps": ["রৈখিক অংশ হুক", "সীমার বাইরে ভাঙে"],
    },
    "hydrostatic-pressure": {
        "trick": "গভীরতা বাড়লে চাপ বাড়ে: P=ρgh — প্রতি 10 m পানি ≈1 atm।",
        "steps": ["গেজ=ρgh", "পরম=P₀+ρgh"],
    },
    "angular-linear-relation": {
        "trick": "v=ωr — চাকা বড় হলে একই ω-তে প্রান্ত দ্রুত।",
        "steps": ["a_t=αr", "a_c=ω²r"],
    },
    "angular-kinematics": {
        "trick": "রৈখিক সূত্রের ক্লোন: v→ω, a→α, s→θ।",
        "steps": ["ω=ω₀+αt", "θ=ω₀t+½αt²"],
    },
    "acceleration-due-to-gravity": {
        "trick": "g=GM/R²; উচ্চতায় g′=g[R/(R+h)]² — উপরে গেলে হালকা।",
        "steps": ["পৃষ্ঠে GM/R²", "h=R হলে g/4"],
    },
    "vertical-circle-min-speed": {
        "trick": "উপরে √(gR), নিচে √(5gR) — ‘১ আর ৫’ মনে রাখো।",
        "steps": ["উপরে N=0 সীমা", "শক্তি দিয়ে নিচ"],
    },
    "vertical-circle-tension": {
        "trick": "নিচে টান বেশি (mv²/r+mg), উপরে কম (mv²/r−mg)।",
        "steps": ["নিচে যোগ", "উপরে বিয়োগ"],
    },
    "rolling-motion": {
        "trick": "শুদ্ধ গড়ানো: v=ωR; মোট KE = ½mv²(1+I/mR²)।",
        "steps": ["স্লিপ নেই", "হুপে I=mR² → K=mv²"],
    },
    "compound-pendulum": {
        "trick": "T=2π√(I/mgd) — সরল দোলকের L_eq=I/(md)।",
        "steps": ["ক্ষুদ্র কোণ", "I=m(k²+d²)"],
    },
    "wave-v-f-lambda": {
        "trick": "সব তরঙ্গের বেসিক: v=fλ — কম্পাঙ্ক×তরঙ্গদৈর্ঘ্য।",
        "steps": ["v=ω/kও", "মাধ্যম বদলালে v বদলায়"],
    },
    "wave-speed-string": {
        "trick": "দড়িতে v=√(T/μ) — টান↑ দ্রুত, ভারী দড়ি ধীর।",
        "steps": ["T টান", "μ=m/L"],
    },
    "organ-pipe-open": {
        "trick": "খোলা পাইপ: সব হারমোনিক; f₁=v/(2L)।",
        "steps": ["n=1,2,3…", "বন্ধের দ্বিগুণ মূল সুর"],
    },
    "organ-pipe-closed": {
        "trick": "বন্ধ পাইপ: শুধু বিজোড়; f₁=v/(4L) — খোলার অর্ধেক।",
        "steps": ["1,3,5…", "λ/4 মূল"],
    },
    "doppler-effect-general": {
        "trick": "কাছে এলে কম্পাঙ্ক বাড়ে: লবে পর্যবেক্ষক +, হরে উৎস −।",
        "steps": ["NUM: observer towards +", "DEN: source towards −"],
    },
    "einstein-photoelectric": {
        "trick": "hf = φ + K_max — ফোটনের বাড়তি শক্তিই গতিশক্তি; V₀ দিয়ে মাপো।",
        "steps": ["f₀=φ/h", "K_max=eV₀"],
    },
    "atwood-machine": {
        "trick": "a = Δm·g/Σm; T = 2m₁m₂g/(m₁+m₂) — পার্থক্য ত্বরণ, গুণফল টান।",
        "steps": ["ভারী দিকে a", "T মাঝামাঝি"],
    },
    "meter-bridge": {
        "trick": "X = R·l/(100−l) — জকির সেন্টিমিটারই অনুপাত।",
        "steps": ["হুইটস্টোন", "l বাম দৈর্ঘ্য"],
    },
    "ph-weak-acid": {
        "trick": "দুর্বল অ্যাসিড: [H⁺]=√(K_a c) — শক্তিশালীতে সোজা c।",
        "steps": ["α≪1", "pH=−log[H⁺]"],
    },
    "solubility-from-ksp": {
        "trick": "AB→√Ksp; AB₂→∛(Ksp/4) — চার্জ গুণে ভুলো না।",
        "steps": ["AgCl: s²", "CaF₂: 4s³"],
    },
    "common-ion-effect": {
        "trick": "একই আয়ন যোগ = বিয়োজন/দ্রাব্যতা কমে — বাফারের চাবিকাঠি।",
        "steps": ["Le Chatelier বামে", "ধোয়ায় ব্যবহার"],
    },
    "gibbs-helmholtz": {
        "trick": "ΔG=ΔH−TΔS; ΔG°=−RT ln K — ঋণাত্মক ΔG মানে চলে।",
        "steps": ["ΔG<0 স্বতঃস্ফূর্ত", "বড় K→ঋণাত্মক ΔG°"],
    },
    "cell-emf-series": {
        "trick": "E°_cell = E°_ক্যাথোড − E°_অ্যানোড — বড় বিজারণ বিভব = ক্যাথোড।",
        "steps": ["Zn–Cu = 1.10 V", "E°>0 গ্যালভানিক"],
    },
    "faraday-first-law": {
        "trick": "m=ZIt — চার্জ যত, জমা তত; Z=E/F।",
        "steps": ["Q=It", "m=MIt/(nF)"],
    },
    "huckel-rule": {
        "trick": "অ্যারোমেটিক = 4n+2 π ইলেকট্রন (২,৬,১০…) — বেনজিন ৬।",
        "steps": ["সমতল চক্র", "4n = অ্যান্টি"],
    },
    "cfse-octahedral": {
        "trick": "t₂g −0.4, e_g +0.6 — গুণে যোগ করো Δ_o।",
        "steps": ["d³ → −1.2Δ_o", "জোড় শক্তি আলাদা"],
    },
    "henrys-law": {
        "trick": "সোডা বোতল: চাপ↑ → গ্যাস বেশি দ্রবে; খুললে বুদবুদ। P=K_H x।",
        "steps": ["চাপ∝দ্রাব্যতা", "গরমে কমে"],
    },
    "percentage-yield": {
        "trick": "% yield = যা পেয়েছ / যা পাওয়ার কথা × 100।",
        "steps": ["সীমায়ক → theo", "actual/theo"],
    },
    "mass-defect-binding": {
        "trick": "ভর কম = শক্তি বেরিয়েছে: BE = Δm × 931 MeV।",
        "steps": ["Δm=যোগফল−প্রকৃত", "প্রতি নিউক্লিয়ন BE"],
    },
    "ideal-gas-chem": {
        "trick": "PV=nRT — STP-তে ১ মোল ≈ ২২.৪ L।",
        "steps": ["R=0.0821", "n=PV/RT"],
    },
    "nernst-equation": {
        "trick": "২৫°C-এ E = E° − (0.059/n) log Q — Q বাড়লে E কমে।",
        "steps": ["n=ইলেকট্রন", "log10 ব্যবহার"],
    },
    "le-chatelier": {
        "trick": "চাপ দিলে সাম্য চাপ কমায় যেদিকে — Le Chatelier ‘বিরোধিতা’ করে।",
        "steps": ["তাপ যোগ = এন্ডো দিকে", "ঘনমাত্রা↑ বিপরীত দিকে"],
    },
    "henderson-hasselbalch": {
        "trick": "pH = pKa + log([salt]/[acid]) — বাফারে লবণ/অ্যাসিড অনুপাত।",
        "steps": ["সমান হলে pH=pKa", "ক্ষার বাফারে pOH রূপ"],
    },
}


def main() -> None:
    updated = 0
    for fid, patch in TRICKS.items():
        matches = list(ROOT.rglob(f"formulas/{fid}.json"))
        if not matches:
            print("skip", fid)
            continue
        path = matches[0]
        data = json.loads(path.read_text(encoding="utf-8"))
        memo = data.get("memorize") or {}
        memo["trick"] = patch["trick"]
        if patch.get("steps"):
            memo["steps"] = patch["steps"]
        data["memorize"] = memo
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        updated += 1
    print(f"Updated memorize tips: {updated}")


if __name__ == "__main__":
    main()
