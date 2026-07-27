import tagsJson from '../../content/tags.json'
import physicsMeta from '../../content/subjects/physics/meta.json'
import magneticMeta from '../../content/subjects/physics/chapters/magnetic-current/meta.json'
import thermoMeta from '../../content/subjects/physics/chapters/thermodynamics/meta.json'
import staticMeta from '../../content/subjects/physics/chapters/static-electricity/meta.json'
import currentMeta from '../../content/subjects/physics/chapters/current-electricity/meta.json'
import vectorMeta from '../../content/subjects/physics/chapters/vector/meta.json'
import dynamicsMeta from '../../content/subjects/physics/chapters/dynamics/meta.json'
import workEnergyMeta from '../../content/subjects/physics/chapters/work-energy/meta.json'
import gravitationMeta from '../../content/subjects/physics/chapters/gravitation/meta.json'
import inductionAcMeta from '../../content/subjects/physics/chapters/induction-ac/meta.json'
import modernPhysicsMeta from '../../content/subjects/physics/chapters/modern-physics/meta.json'
import qualitativeMeta from '../../content/subjects/chemistry/chapters/qualitative-chem/meta.json'
import electrochemMeta from '../../content/subjects/chemistry/chapters/electrochemistry/meta.json'
import chemEquilibriumMeta from '../../content/subjects/chemistry/chapters/chemical-equilibrium/meta.json'

import straightLinesMeta from '../../content/subjects/math/chapters/straight-lines/meta.json'
import calculusMeta from '../../content/subjects/math/chapters/calculus/meta.json'
import complexNumbersMeta from '../../content/subjects/math/chapters/complex-numbers/meta.json'

import periodicMotionMeta from '../../content/subjects/physics/chapters/periodic-motion/meta.json'
import semiconductorMeta from '../../content/subjects/physics/chapters/semiconductor/meta.json'

import shmTimePeriod from '../../content/subjects/physics/chapters/periodic-motion/formulas/shm-time-period.json'
import transistorAlphaBeta from '../../content/subjects/physics/chapters/semiconductor/formulas/transistor-alpha-beta.json'
import kpKcRelation from '../../content/subjects/chemistry/chapters/chemical-equilibrium/formulas/kp-kc-relation.json'
import complexModulusArgument from '../../content/subjects/math/chapters/complex-numbers/formulas/complex-modulus-argument.json'


import bohrAtomModel from '../../content/subjects/chemistry/chapters/qualitative-chem/formulas/bohr-atom-model.json'
import solubilityProduct from '../../content/subjects/chemistry/chapters/qualitative-chem/formulas/solubility-product.json'

import faradaysElectrolysis from '../../content/subjects/chemistry/chapters/electrochemistry/formulas/faradays-electrolysis.json'
import nernstEquation from '../../content/subjects/chemistry/chapters/electrochemistry/formulas/nernst-equation.json'

import perpendicularDistance from '../../content/subjects/math/chapters/straight-lines/formulas/perpendicular-distance.json'
import straightLineAngle from '../../content/subjects/math/chapters/straight-lines/formulas/straight-line-angle.json'

import integrationByParts from '../../content/subjects/math/chapters/calculus/formulas/integration-by-parts.json'
import differentiationChainRule from '../../content/subjects/math/chapters/calculus/formulas/differentiation-chain-rule.json'


import newtonsGravitation from '../../content/subjects/physics/chapters/gravitation/formulas/newtons-gravitation.json'
import escapeVelocity from '../../content/subjects/physics/chapters/gravitation/formulas/escape-velocity.json'
import orbitalVelocity from '../../content/subjects/physics/chapters/gravitation/formulas/orbital-velocity.json'

import faradaysLaw from '../../content/subjects/physics/chapters/induction-ac/formulas/faradays-law.json'
import acRmsValues from '../../content/subjects/physics/chapters/induction-ac/formulas/ac-rms-values.json'

import massEnergyPhotoelectric from '../../content/subjects/physics/chapters/modern-physics/formulas/mass-energy-photoelectric.json'

import centripetalForce from '../../content/subjects/physics/chapters/dynamics/formulas/centripetal-force.json'
import torqueAngularAcc from '../../content/subjects/physics/chapters/dynamics/formulas/torque-angular-acc.json'
import bankedRoad from '../../content/subjects/physics/chapters/dynamics/formulas/banked-road.json'

import kineticEnergy from '../../content/subjects/physics/chapters/work-energy/formulas/kinetic-energy.json'
import potentialEnergySpring from '../../content/subjects/physics/chapters/work-energy/formulas/potential-energy-spring.json'

import ohmsLaw from '../../content/subjects/physics/chapters/current-electricity/formulas/ohms-law.json'
import wheatstoneBridge from '../../content/subjects/physics/chapters/current-electricity/formulas/wheatstone-bridge.json'

import vectorResultant from '../../content/subjects/physics/chapters/vector/formulas/vector-resultant.json'
import vectorDotProduct from '../../content/subjects/physics/chapters/vector/formulas/vector-dot-product.json'
import vectorCrossArea from '../../content/subjects/physics/chapters/vector/formulas/vector-cross-area.json'

import firstLawThermo from '../../content/subjects/physics/chapters/thermodynamics/formulas/first-law-thermo.json'
import isothermalWork from '../../content/subjects/physics/chapters/thermodynamics/formulas/isothermal-work.json'
import carnaudEfficiency from '../../content/subjects/physics/chapters/thermodynamics/formulas/carnaud-efficiency.json'
import cpCvRelation from '../../content/subjects/physics/chapters/thermodynamics/formulas/cp-cv-relation.json'

import coulombsLaw from '../../content/subjects/physics/chapters/static-electricity/formulas/coulombs-law.json'
import electricPotential from '../../content/subjects/physics/chapters/static-electricity/formulas/electric-potential.json'
import capacitorEnergy from '../../content/subjects/physics/chapters/static-electricity/formulas/capacitor-energy.json'

import kirchhoffsLaws from '../../content/subjects/physics/chapters/current-electricity/formulas/kirchhoffs-laws.json'
import transformerRatio from '../../content/subjects/physics/chapters/induction-ac/formulas/transformer-ratio.json'
import radioactiveDecay from '../../content/subjects/physics/chapters/modern-physics/formulas/radioactive-decay.json'
import biotSavart from '../../content/subjects/physics/chapters/magnetic-current/formulas/biot-savart.json'
import wireField from '../../content/subjects/physics/chapters/magnetic-current/formulas/wire-field.json'
import straightWireFinite from '../../content/subjects/physics/chapters/magnetic-current/formulas/straight-wire-finite.json'
import loopCenter from '../../content/subjects/physics/chapters/magnetic-current/formulas/loop-center.json'
import loopAxis from '../../content/subjects/physics/chapters/magnetic-current/formulas/loop-axis.json'
import arcCenter from '../../content/subjects/physics/chapters/magnetic-current/formulas/arc-center.json'
import solenoid from '../../content/subjects/physics/chapters/magnetic-current/formulas/solenoid.json'
import toroid from '../../content/subjects/physics/chapters/magnetic-current/formulas/toroid.json'
import forceOnWire from '../../content/subjects/physics/chapters/magnetic-current/formulas/force-on-wire.json'
import parallelWires from '../../content/subjects/physics/chapters/magnetic-current/formulas/parallel-wires.json'
import lorentz from '../../content/subjects/physics/chapters/magnetic-current/formulas/lorentz.json'
import velocitySelector from '../../content/subjects/physics/chapters/magnetic-current/formulas/velocity-selector.json'
import magneticMoment from '../../content/subjects/physics/chapters/magnetic-current/formulas/magnetic-moment.json'
import torqueLoop from '../../content/subjects/physics/chapters/magnetic-current/formulas/torque-loop.json'
import magneticWork from '../../content/subjects/physics/chapters/magnetic-current/formulas/magnetic-work.json'
import magneticPotentialEnergy from '../../content/subjects/physics/chapters/magnetic-current/formulas/magnetic-potential-energy.json'
import amperesLaw from '../../content/subjects/physics/chapters/magnetic-current/formulas/amperes-law.json'
import cyclotronRadius from '../../content/subjects/physics/chapters/magnetic-current/formulas/cyclotron-radius.json'
import cyclotronFreq from '../../content/subjects/physics/chapters/magnetic-current/formulas/cyclotron-freq.json'
import movingChargeEnergy from '../../content/subjects/physics/chapters/magnetic-current/formulas/moving-charge-energy.json'
import galvanometerAmmeter from '../../content/subjects/physics/chapters/magnetic-current/formulas/galvanometer-ammeter.json'
import galvanometerVoltmeter from '../../content/subjects/physics/chapters/magnetic-current/formulas/galvanometer-voltmeter.json'
import tangentGalvanometer from '../../content/subjects/physics/chapters/magnetic-current/formulas/tangent-galvanometer.json'
import earthMagnetism from '../../content/subjects/physics/chapters/magnetic-current/formulas/earth-magnetism.json'
import barMagnetField from '../../content/subjects/physics/chapters/magnetic-current/formulas/bar-magnet-field.json'
import magneticFlux from '../../content/subjects/physics/chapters/magnetic-current/formulas/magnetic-flux.json'
import hallEffect from '../../content/subjects/physics/chapters/magnetic-current/formulas/hall-effect.json'
import magneticIntensity from '../../content/subjects/physics/chapters/magnetic-current/formulas/magnetic-intensity.json'
import bohrMagneton from '../../content/subjects/physics/chapters/magnetic-current/formulas/bohr-magneton.json'
import magneticForceChargeAngle from '../../content/subjects/physics/chapters/magnetic-current/formulas/magnetic-force-charge-angle.json'
import curieLaw from '../../content/subjects/physics/chapters/magnetic-current/formulas/curie-law.json'
import magneticHysteresisLoss from '../../content/subjects/physics/chapters/magnetic-current/formulas/magnetic-hysteresis-loss.json'
import coaxialCableField from '../../content/subjects/physics/chapters/magnetic-current/formulas/coaxial-cable-field.json'
import magneticDipoleVibration from '../../content/subjects/physics/chapters/magnetic-current/formulas/magnetic-dipole-vibration.json'
import electromagneticMassSpectrometer from '../../content/subjects/physics/chapters/magnetic-current/formulas/electromagnetic-mass-spectrometer.json'

import type {
  BookPage,
  ChapterMeta,
  Formula,
  PaperMeta,
  SubjectMeta,
  Tag,
  TagId,
} from './types'

export const tags = tagsJson as Tag[]
export const subject: SubjectMeta = physicsMeta as SubjectMeta

export const papers: PaperMeta[] = [
  { id: '1st-paper', name: '1st Paper', nameBn: '১ম পত্র' },
  { id: '2nd-paper', name: '2nd Paper', nameBn: '২য় পত্র' },
]

export const subjectsList: SubjectMeta[] = [
  { id: 'physics', slug: 'physics', name: 'Physics', nameBn: 'পদার্থবিজ্ঞান', icon: '', color: '#ffffff', order: 1 },
  { id: 'chemistry', slug: 'chemistry', name: 'Chemistry', nameBn: 'রসায়ন', icon: '', color: '#ffffff', order: 2 },
  { id: 'math', slug: 'math', name: 'Higher Math', nameBn: 'উচ্চতর গণিত', icon: '', color: '#ffffff', order: 3 },
]

export const allChapters: ChapterMeta[] = [
  // Physics 2nd Paper
  { id: 'magnetic-current', slug: 'magnetic-current', name: 'Magnetic Effects of Current & Magnetism', nameBn: 'তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব', subjectId: 'physics', paperId: '2nd-paper', order: 4, formulaCount: 35, isReady: true },
  { id: 'thermodynamics', slug: 'thermodynamics', name: 'Thermodynamics', nameBn: 'তাপগতিবিদ্যা', subjectId: 'physics', paperId: '2nd-paper', order: 1, formulaCount: 4, isReady: true },
  { id: 'static-electricity', slug: 'static-electricity', name: 'Static Electricity', nameBn: 'স্থির তড়িৎ', subjectId: 'physics', paperId: '2nd-paper', order: 2, formulaCount: 3, isReady: true },
  { id: 'current-electricity', slug: 'current-electricity', name: 'Current Electricity', nameBn: 'চল তড়িৎ', subjectId: 'physics', paperId: '2nd-paper', order: 3, formulaCount: 3, isReady: true },
  { id: 'induction-ac', slug: 'induction-ac', name: 'Electromagnetic Induction & AC', nameBn: 'তড়িচ্চৌম্বক আবেশ ও পর্যায়বৃত্ত প্রবাহ', subjectId: 'physics', paperId: '2nd-paper', order: 5, formulaCount: 3, isReady: true },
  { id: 'modern-physics', slug: 'modern-physics', name: 'Modern Physics', nameBn: 'আধুনিক পদার্থবিজ্ঞানের সূচনা', subjectId: 'physics', paperId: '2nd-paper', order: 8, formulaCount: 2, isReady: true },

  // Physics 1st Paper
  { id: 'vector', slug: 'vector', name: 'Vector', nameBn: 'ভেক্টর', subjectId: 'physics', paperId: '1st-paper', order: 2, formulaCount: 3, isReady: true },
  { id: 'dynamics', slug: 'dynamics', name: 'Newtonian Mechanics', nameBn: 'নিউটনীয় বলবিদ্যা', subjectId: 'physics', paperId: '1st-paper', order: 4, formulaCount: 3, isReady: true },
  { id: 'work-energy', slug: 'work-energy', name: 'Work, Energy & Power', nameBn: 'কাজ, ক্ষমতা ও শক্তি', subjectId: 'physics', paperId: '1st-paper', order: 5, formulaCount: 2, isReady: true },
  { id: 'gravitation', slug: 'gravitation', name: 'Gravitation & Gravity', nameBn: 'মহাকর্ষ ও অভিকর্ষ', subjectId: 'physics', paperId: '1st-paper', order: 6, formulaCount: 3, isReady: true },
  { id: 'periodic-motion', slug: 'periodic-motion', name: 'Periodic Motion & SHM', nameBn: 'পর্যায়বৃত্ত গতি', subjectId: 'physics', paperId: '1st-paper', order: 8, formulaCount: 1, isReady: true },

  // Physics 2nd Paper (Extra)
  { id: 'semiconductor', slug: 'semiconductor', name: 'Semiconductor & Electronics', nameBn: 'সেমিকন্ডাক্টর ও ইলেকট্রনিক্স', subjectId: 'physics', paperId: '2nd-paper', order: 10, formulaCount: 1, isReady: true },
  
  // Chemistry
  { id: 'qualitative-chem', slug: 'qualitative-chem', name: 'Qualitative Chemistry', nameBn: 'গুণগত রসায়ন', subjectId: 'chemistry', paperId: '1st-paper', order: 2, formulaCount: 2, isReady: true },
  { id: 'chemical-equilibrium', slug: 'chemical-equilibrium', name: 'Chemical Equilibrium & Kinetics', nameBn: 'রাসায়নিক পরিবর্তন ও সাম্যাবস্থা', subjectId: 'chemistry', paperId: '1st-paper', order: 4, formulaCount: 1, isReady: true },
  { id: 'electrochemistry', slug: 'electrochemistry', name: 'Electrochemistry', nameBn: 'তড়িৎ রসায়ন', subjectId: 'chemistry', paperId: '2nd-paper', order: 4, formulaCount: 2, isReady: true },

  // Math
  { id: 'straight-lines', slug: 'straight-lines', name: 'Straight Lines', nameBn: 'সরলরেখা', subjectId: 'math', paperId: '1st-paper', order: 3, formulaCount: 2, isReady: true },
  { id: 'calculus', slug: 'calculus', name: 'Calculus & Integration', nameBn: 'ক্যালকুলাস ও যোগজীকরণ', subjectId: 'math', paperId: '1st-paper', order: 9, formulaCount: 2, isReady: true },
  { id: 'complex-numbers', slug: 'complex-numbers', name: 'Complex Numbers', nameBn: 'জটিল সংখ্যা', subjectId: 'math', paperId: '2nd-paper', order: 3, formulaCount: 1, isReady: true },

]

export const chapters: ChapterMeta[] = [
  magneticMeta,
  thermoMeta,
  staticMeta,
  currentMeta,
  vectorMeta,
  dynamicsMeta,
  workEnergyMeta,
  gravitationMeta,
  inductionAcMeta,
  modernPhysicsMeta,
  qualitativeMeta,
  electrochemMeta,
  straightLinesMeta,
  calculusMeta,
  periodicMotionMeta,
  semiconductorMeta,
  chemEquilibriumMeta,
  complexNumbersMeta,
] as ChapterMeta[]
export const defaultChapterId = 'magnetic-current'

export const formulas: Formula[] = [
  shmTimePeriod,
  transistorAlphaBeta,
  kpKcRelation,
  complexModulusArgument,

  solubilityProduct,
  nernstEquation,
  straightLineAngle,
  differentiationChainRule,

  vectorCrossArea,
  bankedRoad,
  potentialEnergySpring,
  orbitalVelocity,

  cpCvRelation,
  capacitorEnergy,
  kirchhoffsLaws,
  transformerRatio,
  radioactiveDecay,

  bohrAtomModel,
  faradaysElectrolysis,
  perpendicularDistance,
  integrationByParts,

  newtonsGravitation,
  escapeVelocity,
  faradaysLaw,
  acRmsValues,
  massEnergyPhotoelectric,

  centripetalForce,
  torqueAngularAcc,
  kineticEnergy,

  ohmsLaw,
  wheatstoneBridge,

  vectorResultant,
  vectorDotProduct,

  coulombsLaw,
  electricPotential,

  firstLawThermo,
  isothermalWork,
  carnaudEfficiency,

  biotSavart,
  wireField,
  straightWireFinite,
  loopCenter,
  loopAxis,
  arcCenter,
  solenoid,
  toroid,
  forceOnWire,
  parallelWires,
  lorentz,
  velocitySelector,
  magneticMoment,
  torqueLoop,
  magneticWork,
  magneticPotentialEnergy,
  amperesLaw,
  cyclotronRadius,
  cyclotronFreq,
  movingChargeEnergy,
  galvanometerAmmeter,
  galvanometerVoltmeter,
  tangentGalvanometer,
  earthMagnetism,
  barMagnetField,
  magneticFlux,
  hallEffect,
  magneticIntensity,
  bohrMagneton,
  magneticForceChargeAngle,
  curieLaw,
  magneticHysteresisLoss,
  coaxialCableField,
  magneticDipoleVibration,
  electromagneticMassSpectrometer,
] as Formula[]

const tagMap = new Map(tags.map((t) => [t.id, t]))
const chapterMap = new Map(allChapters.map((c) => [c.id, c]))

export function getTag(id: TagId): Tag | undefined {
  return tagMap.get(id)
}

export function getChapter(id: string): ChapterMeta | undefined {
  return chapterMap.get(id)
}

export function getFormula(id: string): Formula | undefined {
  return formulas.find((f) => f.id === id)
}

export function formulasForChapter(chapterId: string = defaultChapterId): Formula[] {
  return formulas.filter((f) => f.chapter === chapterId)
}

/** Compact pack — perPage varies by layout mode */
export function buildPages(items: Formula[], perPage = 7): BookPage[] {
  const pages: BookPage[] = []
  for (let i = 0; i < items.length; i += perPage) {
    pages.push({
      pageNumber: pages.length + 1,
      formulas: items.slice(i, i + perPage),
    })
  }
  return pages
}

export const samplePages = buildPages(formulasForChapter())
