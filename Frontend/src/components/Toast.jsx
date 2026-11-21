import Icon from './Icon'

const VISIBLE_CLASSES = 'opacity-100 -translate-y-2'
const HIDDEN_CLASSES = 'opacity-0 pointer-events-none'

function Toast({ message, iconName, isVisible }) {
  const visibilityClasses = isVisible ? VISIBLE_CLASSES : HIDDEN_CLASSES

  return (
    <div
      role="status"
      className={`fixed bottom-24 left-1/2 z-40 flex -translate-x-1/2 items-center gap-2 rounded-full bg-inverse-surface px-4 py-2.5 text-inverse-on-surface shadow-lg transition-all duration-300 ${visibilityClasses}`}
    >
      <Icon name={iconName} className="text-lg" />
      <span className="text-sm">{message}</span>
    </div>
  )
}

export default Toast