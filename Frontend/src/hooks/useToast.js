import { useCallback, useEffect, useRef, useState } from 'react'
import { TOAST_DURATION_MS } from '../constants/timings'
import { TOAST_ICON, TOAST_KIND, TOAST_MESSAGE } from '../constants/messages'

export function useToast() {
  const [toastKind, setToastKind] = useState(TOAST_KIND.TRASHED)
  const [isVisible, setIsVisible] = useState(false)
  const hideTimerRef = useRef(null)

  const showToast = useCallback((kind) => {
    clearTimeout(hideTimerRef.current)
    setToastKind(kind)
    setIsVisible(true)
    hideTimerRef.current = setTimeout(() => setIsVisible(false), TOAST_DURATION_MS)
  }, [])

  useEffect(() => () => clearTimeout(hideTimerRef.current), [])

  const toastProps = {
    message: TOAST_MESSAGE[toastKind],
    iconName: TOAST_ICON[toastKind],
    isVisible,
  }

  return { toastProps, showToast }
}