import tagsJson from '../../content/tags.json'
import physicsMeta from '../../content/subjects/physics/meta.json'
import magneticMeta from '../../content/subjects/physics/chapters/magnetic-current/meta.json'

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
  { id: 'physics', slug: 'physics', name: 'Physics', nameBn: 'পদার্থবিজ্ঞান', icon: '⚛️', color: '#38bdf8', order: 1 },
  { id: 'chemistry', slug: 'chemistry', name: 'Chemistry', nameBn: 'রসায়ন', icon: '🧪', color: '#22c55e', order: 2 },
  { id: 'math', slug: 'math', name: 'Higher Math', nameBn: 'উচ্চতর গণিত', icon: '📐', color: '#a855f7', order: 3 },
]

export const allChapters: ChapterMeta[] = [
  // Physics 2nd Paper
  { id: 'magnetic-current', slug: 'magnetic-current', name: 'Magnetic Effects of Current & Magnetism', nameBn: 'তড়িৎ প্রবাহের চৌম্বক ক্রিয়া ও চুম্বকত্ব', subjectId: 'physics', paperId: '2nd-paper', order: 4, formulaCount: 35, isReady: true },
  { id: 'thermodynamics', slug: 'thermodynamics', name: 'Thermodynamics', nameBn: 'তাপগতিবিদ্যা', subjectId: 'physics', paperId: '2nd-paper', order: 1, formulaCount: 18, isReady: false },
  { id: 'static-electricity', slug: 'static-electricity', name: 'Static Electricity', nameBn: 'স্থির তড়িৎ', subjectId: 'physics', paperId: '2nd-paper', order: 2, formulaCount: 22, isReady: false },
  { id: 'current-electricity', slug: 'current-electricity', name: 'Current Electricity', nameBn: 'চল তড়িৎ', subjectId: 'physics', paperId: '2nd-paper', order: 3, formulaCount: 24, isReady: false },
  { id: 'induction-ac', slug: 'induction-ac', name: 'Electromagnetic Induction & AC', nameBn: 'তড়িচ্চৌম্বক আবেশ ও পর্যায়বৃত্ত প্রবাহ', subjectId: 'physics', paperId: '2nd-paper', order: 5, formulaCount: 16, isReady: false },
  { id: 'modern-physics', slug: 'modern-physics', name: 'Modern Physics', nameBn: 'আধুনিক পদার্থবিজ্ঞানের সূচনা', subjectId: 'physics', paperId: '2nd-paper', order: 8, formulaCount: 20, isReady: false },

  // Physics 1st Paper
  { id: 'vector', slug: 'vector', name: 'Vector', nameBn: 'ভেক্টর', subjectId: 'physics', paperId: '1st-paper', order: 2, formulaCount: 15, isReady: false },
  { id: 'dynamics', slug: 'dynamics', name: 'Newtonian Mechanics', nameBn: 'নিউটনীয় বলবিদ্যা', subjectId: 'physics', paperId: '1st-paper', order: 4, formulaCount: 18, isReady: false },
  { id: 'work-energy', slug: 'work-energy', name: 'Work, Energy & Power', nameBn: 'কাজ, ক্ষমতা ও শক্তি', subjectId: 'physics', paperId: '1st-paper', order: 5, formulaCount: 14, isReady: false },
  { id: 'gravitation', slug: 'gravitation', name: 'Gravitation & Gravity', nameBn: 'মহাকর্ষ ও অভিকর্ষ', subjectId: 'physics', paperId: '1st-paper', order: 6, formulaCount: 16, isReady: false },
  
  // Chemistry
  { id: 'qualitative-chem', slug: 'qualitative-chem', name: 'Qualitative Chemistry', nameBn: 'গুণগত রসায়ন', subjectId: 'chemistry', paperId: '1st-paper', order: 2, formulaCount: 12, isReady: false },
  { id: 'electrochemistry', slug: 'electrochemistry', name: 'Electrochemistry', nameBn: 'তড়িৎ রসায়ন', subjectId: 'chemistry', paperId: '2nd-paper', order: 4, formulaCount: 14, isReady: false },

  // Math
  { id: 'straight-lines', slug: 'straight-lines', name: 'Straight Lines', nameBn: 'সরলরেখা', subjectId: 'math', paperId: '1st-paper', order: 3, formulaCount: 25, isReady: false },
  { id: 'calculus', slug: 'calculus', name: 'Calculus & Integration', nameBn: 'ক্যালকুলাস ও যোগজীকরণ', subjectId: 'math', paperId: '1st-paper', order: 9, formulaCount: 30, isReady: false },
]

export const chapters: ChapterMeta[] = [magneticMeta as ChapterMeta]
export const defaultChapterId = 'magnetic-current'

export const formulas: Formula[] = [
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
