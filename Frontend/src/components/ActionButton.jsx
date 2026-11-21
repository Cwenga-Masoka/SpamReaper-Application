import Icon from './Icon'
import {
  BUTTON_SIZE,
  BUTTON_SIZE_CLASS,
  BUTTON_VARIANT,
  BUTTON_VARIANT_CLASS,
} from '../constants/buttons'

const BASE_CLASSES =
  'flex items-center justify-center rounded-full font-semibold transition-colors disabled:pointer-events-none disabled:opacity-60'

function ActionButton({
  label,
  iconName,
  onClick,
  variant = BUTTON_VARIANT.SECONDARY,
  size = BUTTON_SIZE.REGULAR,
  isDisabled = false,
}) {
  const { button, icon } = BUTTON_SIZE_CLASS[size]

  return (
    <button
      type="button"
      onClick={onClick}
      disabled={isDisabled}
      className={`${BASE_CLASSES} ${button} ${BUTTON_VARIANT_CLASS[variant]}`}
    >
      <Icon name={iconName} className={icon} />
      {label}
    </button>
  )
}

export default ActionButton