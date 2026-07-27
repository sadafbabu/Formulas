import tagsJson from '../../content/tags.json'
import physicsMeta from '../../content/subjects/physics/meta.json'
import magneticMeta from '../../content/subjects/physics/chapters/magnetic-current/meta.json'

import biotSavart from '../../content/subjects/physics/chapters/magnetic-current/formulas/biot-savart.json'
import wireField from '../../content/subjects/physics/chapters/magnetic-current/formulas/wire-field.json'
import loopCenter from '../../content/subjects/physics/chapters/magnetic-current/formulas/loop-center.json'
import loopAxis from '../../content/subjects/physics/chapters/magnetic-current/formulas/loop-axis.json'
import solenoid from '../../content/subjects/physics/chapters/magnetic-current/formulas/solenoid.json'
import toroid from '../../content/subjects/physics/chapters/magnetic-current/formulas/toroid.json'
import forceOnWire from '../../content/subjects/physics/chapters/magnetic-current/formulas/force-on-wire.json'
import parallelWires from '../../content/subjects/physics/chapters/magnetic-current/formulas/parallel-wires.json'
import lorentz from '../../content/subjects/physics/chapters/magnetic-current/formulas/lorentz.json'
import magneticMoment from '../../content/subjects/physics/chapters/magnetic-current/formulas/magnetic-moment.json'
import torqueLoop from '../../content/subjects/physics/chapters/magnetic-current/formulas/torque-loop.json'
import amperesLaw from '../../content/subjects/physics/chapters/magnetic-current/formulas/amperes-law.json'
import cyclotronRadius from '../../content/subjects/physics/chapters/magnetic-current/formulas/cyclotron-radius.json'
import cyclotronFreq from '../../content/subjects/physics/chapters/magnetic-current/formulas/cyclotron-freq.json'

import type {
  BookPage,
  ChapterMeta,
  Formula,
  SubjectMeta,
  Tag,
  TagId,
} from './types'

export const tags = tagsJson as Tag[]
export const subject: SubjectMeta = physicsMeta as SubjectMeta

export const chapters: ChapterMeta[] = [magneticMeta as ChapterMeta]

/** Default / primary chapter for the book view */
export const defaultChapterId = 'magnetic-current'

export const formulas: Formula[] = [
  biotSavart,
  wireField,
  loopCenter,
  loopAxis,
  solenoid,
  toroid,
  forceOnWire,
  parallelWires,
  lorentz,
  magneticMoment,
  torqueLoop,
  amperesLaw,
  cyclotronRadius,
  cyclotronFreq,
] as Formula[]

const tagMap = new Map(tags.map((t) => [t.id, t]))
const chapterMap = new Map(chapters.map((c) => [c.id, c]))

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
