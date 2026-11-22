const BASE_CLASSES =
  'flex shrink-0 items-center gap-2 rounded-full px-5 py-2.5 text-sm font-semibold shadow-sm transition-all active:scale-95'
const ACTIVE_CLASSES = 'bg-primary text-on-primary'
const INACTIVE_CLASSES =
  'border border-outline-variant/30 bg-surface-container-lowest text-on-surface-variant'
const COUNT_BASE_CLASSES = 'rounded-full px-2 py-0.5 text-xs'

function FilterChip({ label, count, countClass, isActive, onSelect }) {
  const stateClasses = isActive ? ACTIVE_CLASSES : INACTIVE_CLASSES

  return (
    <button
      type="button"
      onClick={onSelect}
      aria-pressed={isActive}
      className={`${BASE_CLASSES} ${stateClasses}`}
    >
      {label}
      <span className={`${COUNT_BASE_CLASSES} ${countClass}`}>{count}</span>
    </button>
  )
}

export default FilterChip