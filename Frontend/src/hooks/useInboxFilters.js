import { useState } from 'react'
import { ALL_FILTER } from '../constants/filters'
import { countEmailsByFilter, filterEmails } from '../utils/emailFilters'

export function useInboxFilters(emails) {
  const [searchText, setSearchText] = useState('')
  const [activeFilter, setActiveFilter] = useState(ALL_FILTER)

  return {
    searchText,
    setSearchText,
    activeFilter,
    setActiveFilter,
    visibleEmails: filterEmails(emails, activeFilter, searchText),
    counts: countEmailsByFilter(emails),
  }
}