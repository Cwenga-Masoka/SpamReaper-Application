import { RISK_BADGE_CLASS } from '../constants/risk'
import { getInitial } from '../utils/text'

function SenderInfo({ name, address, riskLevel }) {
  return (
    <div className="flex min-w-0 items-center gap-3">
      <div
        aria-hidden="true"
        className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-full text-2xl font-bold ${RISK_BADGE_CLASS[riskLevel]}`}
      >
        {getInitial(name)}
      </div>
      <div className="flex min-w-0 flex-col">
        <span className="truncate text-xl font-semibold text-on-surface">{name}</span>
        <span className="truncate text-[15px] text-outline">&lt;{address}&gt;</span>
      </div>
    </div>
  )
}

export default SenderInfo