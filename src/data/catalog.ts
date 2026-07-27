import tagsJson from '../../content/tags.json'
import physicsMeta from '../../content/subjects/physics/meta.json'
import newtonsSecond from '../../content/subjects/physics/formulas/newtons-second.json'
import kineticEnergy from '../../content/subjects/physics/formulas/kinetic-energy.json'
import momentum from '../../content/subjects/physics/formulas/momentum.json'
import impulse from '../../content/subjects/physics/formulas/impulse.json'
import workEnergy from '../../content/subjects/physics/formulas/work-energy.json'
import type { BookPage, Formula, SubjectMeta, Tag, TagId } from './types'

export const tags = tagsJson as Tag[]

export const subject: SubjectMeta = physicsMeta as SubjectMeta

/** Sample chapter formulas — average density for a typical A5 page pair */
export const formulas: Formula[] = [
  newtonsSecond,
  momentum,
  impulse,
  kineticEnergy,
  workEnergy,
] as Formula[]

const tagMap = new Map(tags.map((t) => [t.id, t]))

export function getTag(id: TagId): Tag | undefined {
  return tagMap.get(id)
}

export function getFormula(id: string): Formula | undefined {
  return formulas.find((f) => f.id === id)
}

/**
 * Pack formulas into A5 pages.
 * Average template: ~2–3 formulas per page (title + latex + summary + tags).
 */
export function buildPages(items: Formula[] = formulas): BookPage[] {
  const perPage = 2
  const pages: BookPage[] = []
  for (let i = 0; i < items.length; i += perPage) {
    pages.push({
      pageNumber: pages.length + 1,
      formulas: items.slice(i, i + perPage),
    })
  }
  return pages
}

export const samplePages = buildPages()
