import { URGENCY, URGENCY_BADGE_CLASS } from './urgency'

export const ALL_FILTER = 'all'

export const FILTER_OPTIONS = Object.freeze([
  Object.freeze({ value: ALL_FILTER, label: 'All' }),
  Object.freeze({ value: URGENCY.URGENT, label: 'Urgent' }),
  Object.freeze({ value: URGENCY.SOON, label: 'Soon' }),
  Object.freeze({ value: URGENCY.LATER, label: 'Later' }),
])

export const COUNT_BADGE_CLASS = Object.freeze({
  [ALL_FILTER]: 'bg-surface-container text-on-surface-variant',
  ...URGENCY_BADGE_CLASS,
})

export const ACTIVE_COUNT_CLASS = 'bg-primary-container text-on-primary-container'

export const SEARCHABLE_FIELDS = Object.freeze(['senderName', 'senderAddress', 'subject', 'preview'])

export const SEARCH_ICON = 'search'
export const SEARCH_PLACEHOLDER = 'Search sender, subject, keywords...'
export const SEARCH_LABEL = 'Search emails'
export const FILTER_GROUP_LABEL = 'Filter by urgency'