import { formatPendingSummary, getGreetingForHour } from '../utils/greetingText'

function Greeting({ userName, pendingCount, action, hour = new Date().getHours() }) {
  const { text, emoji } = getGreetingForHour(hour)

  return (
    <section className="mt-7 mb-4 flex items-start justify-between">
      <div className="flex flex-col">
        <h2 className="mb-2flex items-center gap-1.5 text-[29px] font-semibold leading-[30px] tracking-tight text-on-surface">
          {text}, {userName}
          <span aria-hidden="true" className="animate-pulse text-2xl text-secondary">
            {emoji}
          </span>
        </h2>
        <p className="text-lg text-on-surface-variant">
          {formatPendingSummary(pendingCount)}
        </p>
      </div>
      {action}
    </section>
  )
}

export default Greeting