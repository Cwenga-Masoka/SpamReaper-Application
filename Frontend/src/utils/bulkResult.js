import { BULK_RESPONSE_KEY } from '../constants/api'

export function hasFailedItems(response) {
  const failedIds = response[BULK_RESPONSE_KEY.RESULT]?.[BULK_RESPONSE_KEY.FAILED] ?? []
  return failedIds.length > 0
}