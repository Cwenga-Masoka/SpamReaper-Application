import { ALL_FILTER, SEARCHABLE_FIELDS } from '../constants/filters'
import { getUrgency } from './urgency'

function matchesFilter(email, activeFilter) {
  return activeFilter === ALL_FILTER || getUrgency(email.daysLeft) === activeFilter
}

function matchesSearch(email, query) {
  return SEARCHABLE_FIELDS.some((field) => email[field].toLowerCase().includes(query))
}

export function filterEmails(emails, activeFilter, searchText) {
  const query = searchText.trim().toLowerCase()
  return emails.filter(
    (email) => matchesFilter(email, activeFilter) && matchesSearch(email, query),
  )
}

export function countEmailsByFilter(emails) {
  return emails.reduce(
    (counts, { daysLeft }) => {
      const urgency = getUrgency(daysLeft)
      return { ...counts, [urgency]: (counts[urgency] ?? 0) + 1 }
    },
    { [ALL_FILTER]: emails.length },
  )
}