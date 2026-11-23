import ActionButton from './components/ActionButton'
import StatusMessage from './components/StatusMessage'
import { APP_STATUS_MESSAGE } from './constants/auth'
import { RETRY_ACTION } from './constants/emailList'
import { useCurrentUser } from './hooks/useCurrentUser'
import ConnectScreen from './screens/ConnectScreen'
import HomeScreen from './screens/HomeScreen'

const GATE_CLASSES = 'min-h-screen bg-surface font-sans text-on-surface'

function App() {
  const { user, isLoggedOut, hasError, reload } = useCurrentUser()

  if (isLoggedOut) {
    return <ConnectScreen />
  }

  if (user) {
    return <HomeScreen user={user} onNotLoggedIn={reload} />
  }

  return (
    <div className={GATE_CLASSES}>
      <StatusMessage
        message={hasError ? APP_STATUS_MESSAGE.ERROR : APP_STATUS_MESSAGE.LOADING}
      >
        {hasError && <ActionButton {...RETRY_ACTION} onClick={reload} />}
      </StatusMessage>
    </div>
  )
}

export default App