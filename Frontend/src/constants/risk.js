  export const RISK_LEVEL = Object.freeze({
    HIGH: 'high',
    MEDIUM: 'medium',
    LOW: 'low',
  })
  
  export const RISK_BORDER_CLASS = Object.freeze({
    [RISK_LEVEL.HIGH]: 'border-risk-high',
    [RISK_LEVEL.MEDIUM]: 'border-risk-medium',
    [RISK_LEVEL.LOW]: 'border-risk-low',
  })

  export const RISK_BADGE_CLASS = Object.freeze({
    [RISK_LEVEL.HIGH]: 'bg-tertiary-fixed text-tertiary-dark',
    [RISK_LEVEL.MEDIUM]: 'bg-secondary-container text-on-secondary-container',
    [RISK_LEVEL.LOW]: 'bg-surface-container text-on-surface-variant',
  })