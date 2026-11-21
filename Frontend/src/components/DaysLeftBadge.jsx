import Icon from './Icon'
import { DAYS_LEFT_ICON } from '../constants/emailCard'
import { RISK_BADGE_CLASS } from '../constants/risk'
import { formatDaysLeft } from '../utils/emailText'

function DaysLeftBadge({ daysLeft, riskLevel }) {
  return (
    <div
      className={`flex w-fit items-center gap-1.5 rounded-full px-5 py-1.5 text-[16px] font-semibold ${RISK_BADGE_CLASS[riskLevel]}`}
    >
      <Icon name={DAYS_LEFT_ICON} className="text-xl" />
      <span>{formatDaysLeft(daysLeft)}</span>
    </div>
  )
}

export default DaysLeftBadge