export const URGENCY = Object.freeze({
    URGENT: 'urgent',
    SOON: 'soon',
    LATER: 'later',
  })
  
  export const URGENT_MAX_DAYS_LEFT = 1
  export const SOON_MAX_DAYS_LEFT = 3
  
  export const URGENCY_BORDER_CLASS = Object.freeze({
    [URGENCY.URGENT]: 'border-urgency-urgent',
    [URGENCY.SOON]: 'border-urgency-soon',
    [URGENCY.LATER]: 'border-urgency-later',
  })
  
  export const URGENCY_BADGE_CLASS = Object.freeze({
    [URGENCY.URGENT]: 'bg-tertiary-fixed text-tertiary-dark',
    [URGENCY.SOON]: 'bg-secondary-container text-on-secondary-container',
    [URGENCY.LATER]: 'bg-surface-container text-on-surface-variant',
  })