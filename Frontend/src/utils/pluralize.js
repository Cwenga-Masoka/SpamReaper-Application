const SINGLE_COUNT = 1

export function pluralize(count, singular, plural) {
  return count === SINGLE_COUNT ? singular : plural
}