import Icon from './Icon'
import { SEARCH_ICON, SEARCH_LABEL, SEARCH_PLACEHOLDER } from '../constants/filters'

function SearchBar({ value, onChange }) {
  return (
    <div className="relative flex h-15 w-full items-center">
      <Icon
        name={SEARCH_ICON}
        className="pointer-events-none absolute left-4 text-3xl text-outline"
      />
      <input
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={SEARCH_PLACEHOLDER}
        aria-label={SEARCH_LABEL}
        className="h-15 w-full rounded-full border border-outline-variant/40 bg-surface-container-lowest pl-11 pr-4 text-xl text-on-surface shadow-sm placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary-container/40"
      />
    </div>
  )
}

export default SearchBar