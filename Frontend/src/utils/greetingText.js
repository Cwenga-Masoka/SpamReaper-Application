import {
    AFTERNOON_START_HOUR,
    EVENING_START_HOUR,
    GREETING,
    ITEM_LABEL,
    MORNING_START_HOUR,
    PENDING_SUMMARY_SUFFIX,
  } from '../constants/greeting'
  import { pluralize } from './pluralize'
  
  export function getGreetingForHour(hour) {
    if (hour >= MORNING_START_HOUR && hour < AFTERNOON_START_HOUR) {
      return GREETING.MORNING
    }
    if (hour >= AFTERNOON_START_HOUR && hour < EVENING_START_HOUR) {
      return GREETING.AFTERNOON
    }
    return GREETING.EVENING
  }
  
  export function formatPendingSummary(count) {
    const itemLabel = pluralize(count, ITEM_LABEL.SINGULAR, ITEM_LABEL.PLURAL)
    return `${count} ${itemLabel} ${PENDING_SUMMARY_SUFFIX}`
  }