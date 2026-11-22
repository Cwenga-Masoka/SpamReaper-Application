import { useCallback, useState } from 'react'
import { TOAST_KIND } from '../constants/messages'
import { scanInbox } from '../services/api'

export function useScan({ showToast, onScanDone }) {
  const [isScanning, setIsScanning] = useState(false)

  const scan = useCallback(async () => {
    setIsScanning(true)

    try {
      await scanInbox()
      showToast(TOAST_KIND.SCANNED)
      await onScanDone()
    } catch {
      showToast(TOAST_KIND.FAILED)
    } finally {
      setIsScanning(false)
    }
  }, [showToast, onScanDone])

  return { scan, isScanning }
}