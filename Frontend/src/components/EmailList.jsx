import ActionButton from './ActionButton'
import EmailCard from './EmailCard'
import StatusMessage from './StatusMessage'
import { EMAIL_LIST_MESSAGE, RETRY_ACTION } from '../constants/emailList'

function EmailList({
  emails,
  isLoading,
  hasError,
  onRetry,
  isSelected,
  onToggleSelect,
  onKeep,
  onTrash,
}) {
  if (isLoading) {
    return <StatusMessage message={EMAIL_LIST_MESSAGE.LOADING} />
  }

  if (hasError) {
    return (
      <StatusMessage message={EMAIL_LIST_MESSAGE.ERROR}>
        <ActionButton {...RETRY_ACTION} onClick={onRetry} />
      </StatusMessage>
    )
  }

  if (emails.length === 0) {
    return <StatusMessage message={EMAIL_LIST_MESSAGE.EMPTY} />
  }

  return emails.map((email) => (
    <EmailCard
      key={email.id}
      email={email}
      isSelected={isSelected(email.id)}
      onToggleSelect={onToggleSelect}
      onKeep={onKeep}
      onTrash={onTrash}
    />
  ))
}

export default EmailList