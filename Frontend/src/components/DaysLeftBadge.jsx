import Icon from './Icon'
import { DAYS_LEFT_ICON } from '../constants/emailCard'
import { URGENCY_BADGE_CLASS } from '../constants/urgency'
import { formatDaysLeft } from '../utils/emailText'

function DaysLeftBadge({ daysLeft, urgency }) {
  return (
    <div
      className={`flex w-fit items-center gap-1.5 rounded-full px-5 py-1.5 text-[16px] font-semibold ${URGENCY_BADGE_CLASS[urgency]}`}
    >
      <Icon name={DAYS_LEFT_ICON} className="text-xl" />
      <span>{formatDaysLeft(daysLeft)}</span>
    </div>
  )
}

export default DaysLeftBadge