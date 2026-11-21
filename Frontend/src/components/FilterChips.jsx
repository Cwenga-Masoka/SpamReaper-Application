import FilterChip from './FilterChip'
import {
  ACTIVE_COUNT_CLASS,
  COUNT_BADGE_CLASS,
  FILTER_GROUP_LABEL,
  FILTER_OPTIONS,
} from '../constants/filters'

function FilterChips({ counts, activeFilter, onChange }) {
  return (
    <div
      role="group"
      aria-label={FILTER_GROUP_LABEL}
      className="flex items-center gap-6 overflow-x-auto pt-3 pb-3 [scrollbar-width:none] [&::-webkit-scrollbar]:hidden"
    >
      {FILTER_OPTIONS.map(({ value, label }) => {
        const isActive = value === activeFilter

        return (
          <FilterChip
            key={value}
            label={label}
            count={counts[value] ?? 0}
            countClass={isActive ? ACTIVE_COUNT_CLASS : COUNT_BADGE_CLASS[value]}
            isActive={isActive}
            onSelect={() => onChange(value)}
          />
        )
      })}
    </div>
  )
}

export default FilterChips