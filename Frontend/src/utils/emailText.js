import { DAY_LABEL, DAYS_LEFT_SUFFIX } from '../constants/emailCard'
import { pluralize } from './pluralize'

export function formatDaysLeft(daysLeft) {
  const dayLabel = pluralize(daysLeft, DAY_LABEL.SINGULAR, DAY_LABEL.PLURAL)
  return `${daysLeft} ${dayLabel} ${DAYS_LEFT_SUFFIX}`
}