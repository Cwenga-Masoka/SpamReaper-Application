import { RISK_BADGE_CLASS, RISK_LEVEL } from './risk'

export const ALL_FILTER = 'all'

export const FILTER_OPTIONS = Object.freeze([
  Object.freeze({ value: ALL_FILTER, label: 'All' }),
  Object.freeze({ value: RISK_LEVEL.HIGH, label: 'High Risk' }),
  Object.freeze({ value: RISK_LEVEL.MEDIUM, label: 'Medium Risk' }),
  Object.freeze({ value: RISK_LEVEL.LOW, label: 'Low Risk' }),
])

export const COUNT_BADGE_CLASS = Object.freeze({
  [ALL_FILTER]: 'bg-surface-container text-on-surface-variant',
  ...RISK_BADGE_CLASS,
})

export const ACTIVE_COUNT_CLASS = 'bg-primary-container text-on-primary-container'

export const SEARCHABLE_FIELDS = Object.freeze(['senderName', 'senderAddress', 'subject', 'preview'])

export const SEARCH_ICON = 'search'
export const SEARCH_PLACEHOLDER = 'Search sender, subject, keywords...'
export const SEARCH_LABEL = 'Search emails'
export const FILTER_GROUP_LABEL = 'Filter by risk level'