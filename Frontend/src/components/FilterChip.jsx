const BASE_CLASSES =
  'flex shrink-0 items-center gap-1.5 rounded-full px-3.5 py-1.5 text-xs font-semibold shadow-sm transition-all active:scale-95'
const ACTIVE_CLASSES = 'bg-primary text-on-primary'
const INACTIVE_CLASSES =
  'border border-outline-variant/30 bg-surface-container-lowest text-on-surface-variant'

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
      <span className={`rounded-full h-8 w-13 text-[23px] ${countClass}`}>{count}</span>
    </button>
  )
}

export default FilterChip