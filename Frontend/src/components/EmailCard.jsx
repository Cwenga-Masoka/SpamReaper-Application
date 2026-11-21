import ActionButton from './ActionButton'
import DaysLeftBadge from './DaysLeftBadge'
import SenderInfo from './SenderInfo'
import { BUTTON_VARIANT } from '../constants/buttons'
import {
  KEEP_ACTION,
  SELECT_EMAIL_LABEL_PREFIX,
  TRASH_ACTION,
} from '../constants/emailCard'
import { RISK_BORDER_CLASS } from '../constants/risk'

function EmailCard({ email, isSelected, onToggleSelect, onKeep, onTrash }) {
  const { id, senderName, senderAddress, subject, preview, riskLevel, daysLeft } = email

  return (
    <article
      className={`flex flex-col gap-9 rounded-card border-4 bg-surface-container-lowest p-5 shadow-soft ${RISK_BORDER_CLASS[riskLevel]}`}
    >
      <div className="flex items-center gap-7">
        <input
          type="checkbox"
          checked={isSelected}
          onChange={() => onToggleSelect(id)}
          aria-label={`${SELECT_EMAIL_LABEL_PREFIX} ${senderName}`}
          className="h-5 w-5 shrink-0 cursor-pointer accent-primary"
        />
        <SenderInfo 
          name={senderName} 
          address={senderAddress} 
          riskLevel={riskLevel} 
        />
      </div>

      <div className="flex flex-col gap-1">
        <h3 className="line-clamp-1 text-[19px] font-semibold leading-snug text-on-surface">
          {subject}
        </h3>
        <p className="line-clamp-2 text-[16px] text-on-surface-variant">{preview}</p>
      </div>

      <DaysLeftBadge daysLeft={daysLeft} riskLevel={riskLevel} />

      <div className="grid grid-cols-2 gap-4">
        <ActionButton {...KEEP_ACTION} onClick={() => onKeep(id)} />
        <ActionButton
          {...TRASH_ACTION}
          variant={BUTTON_VARIANT.DANGER}
          onClick={() => onTrash(id)}
        />
      </div>
    </article>
  )
}

export default EmailCard