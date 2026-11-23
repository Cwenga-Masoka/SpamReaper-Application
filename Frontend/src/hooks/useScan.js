import { useCallback, useState } from 'react'
import { TOAST_KIND } from '../constants/messages'
import { scanInbox } from '../services/api'
import { reportFailure } from '../utils/actionFailure'

export function useScan({ showToast, onScanDone, onNotLoggedIn }) {
  const [isScanning, setIsScanning] = useState(false)

  const scan = useCallback(async () => {
    setIsScanning(true)

    try {
      await scanInbox()
      showToast(TOAST_KIND.SCANNED)
      await onScanDone()
    } catch (error) {
      reportFailure(error, { showToast, onNotLoggedIn })
    } finally {
      setIsScanning(false)
    }
  }, [showToast, onScanDone])

  return { scan, isScanning }
}