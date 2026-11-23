import { TOAST_KIND } from '../constants/messages'
import { NotLoggedInError } from '../services/errors'

export function reportFailure(error, { showToast, onNotLoggedIn }) {
  if (error instanceof NotLoggedInError) {
    onNotLoggedIn()
    return
  }

  showToast(TOAST_KIND.FAILED)
}