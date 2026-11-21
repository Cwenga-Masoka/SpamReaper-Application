export const BUTTON_VARIANT = Object.freeze({
    SECONDARY: 'secondary',
    DANGER: 'danger',
  })
  
  export const BUTTON_VARIANT_CLASS = Object.freeze({
    [BUTTON_VARIANT.SECONDARY]: 'bg-surface-container text-primary hover:bg-primary-fixed',
    [BUTTON_VARIANT.DANGER]: 'bg-tertiary text-on-tertiary shadow-sm hover:bg-tertiary-dark',
  })
  
  export const BUTTON_SIZE = Object.freeze({
    REGULAR: 'regular',
    COMPACT: 'compact',
  })
  
  export const BUTTON_SIZE_CLASS = Object.freeze({
    [BUTTON_SIZE.REGULAR]: Object.freeze({
      button: 'gap-2 px-4 py-2.5 text-sm',
      icon: 'text-lg',
    }),
    [BUTTON_SIZE.COMPACT]: Object.freeze({
      button: 'gap-1.5 px-3.5 py-1.5 text-xs',
      icon: 'text-base',
    }),
  })