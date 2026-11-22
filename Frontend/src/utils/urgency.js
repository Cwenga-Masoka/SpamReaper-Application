import {
    SOON_MAX_DAYS_LEFT,
    URGENCY,
    URGENT_MAX_DAYS_LEFT,
  } from '../constants/urgency'
  
  export function getUrgency(daysLeft) {
    if (daysLeft <= URGENT_MAX_DAYS_LEFT) {
      return URGENCY.URGENT
    }
    if (daysLeft <= SOON_MAX_DAYS_LEFT) {
      return URGENCY.SOON
    }
    return URGENCY.LATER
  }