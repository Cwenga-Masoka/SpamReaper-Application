import { useCallback } from 'react'
import { TOAST_KIND } from '../constants/messages'
import { keepEmail, keepEmails, trashEmail, trashEmails } from '../services/api'
import { hasFailedItems } from '../utils/bulkResult'

export function useEmailActions({ showToast, onActionDone }) {
  const runAction = useCallback(
    async (action, target, successKind) => {
      try {
        const response = await action(target)
        showToast(hasFailedItems(response) ? TOAST_KIND.FAILED : successKind)
        await onActionDone()
      } catch {
        showToast(TOAST_KIND.FAILED)
      }
    },
    [showToast, onActionDone],
  )

  const keep = useCallback(
    (id) => runAction(keepEmail, id, TOAST_KIND.KEPT),
    [runAction],
  )

  const trash = useCallback(
    (id) => runAction(trashEmail, id, TOAST_KIND.TRASHED),
    [runAction],
  )

  const keepMany = useCallback(
    (ids) => runAction(keepEmails, ids, TOAST_KIND.KEPT),
    [runAction],
  )

  const trashMany = useCallback(
    (ids) => runAction(trashEmails, ids, TOAST_KIND.TRASHED),
    [runAction],
  )

  return { keep, trash, keepMany, trashMany }
}