export const MORNING_START_HOUR = 5
export const AFTERNOON_START_HOUR = 12
export const EVENING_START_HOUR = 18

export const GREETING = Object.freeze({
  MORNING: Object.freeze({ text: 'Good morning', emoji: '☀️' }),
  AFTERNOON: Object.freeze({ text: 'Good afternoon', emoji: '🌤️' }),
  EVENING: Object.freeze({ text: 'Good evening', emoji: '🌙' }),
})

export const ITEM_LABEL = Object.freeze({
  SINGULAR: 'item',
  PLURAL: 'items',
})

export const PENDING_SUMMARY_SUFFIX = 'awaiting review before auto-trash'