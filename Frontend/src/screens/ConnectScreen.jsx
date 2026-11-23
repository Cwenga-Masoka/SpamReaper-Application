import ActionButton from '../components/ActionButton'
import Icon from '../components/Icon'
import { APP_LOGO_ICON } from '../constants/branding'
import { CONNECT_SCREEN } from '../constants/auth'
import { LOGIN_URL } from '../constants/api'

const SCREEN_CLASSES =
  'flex min-h-screen flex-col items-center justify-center gap-4 bg-surface p-6 text-center font-sans text-on-surface'

const goToLogin = () => window.location.assign(LOGIN_URL)

function ConnectScreen() {
  return (
    <div className={SCREEN_CLASSES}>
      <Icon name={APP_LOGO_ICON} className="text-6xl text-primary" />
      <h1 className="text-[22px] font-semibold tracking-tight">{CONNECT_SCREEN.TITLE}</h1>
      <p className="max-w-sm text-sm text-on-surface-variant">
        {CONNECT_SCREEN.DESCRIPTION}
      </p>
      <ActionButton {...CONNECT_SCREEN.BUTTON} onClick={goToLogin} />
    </div>
  )
}

export default ConnectScreen