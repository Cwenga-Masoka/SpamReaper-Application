import Icon from './Icon'
import { SCAN_ICON, SCAN_LABEL, SPINNING_CLASS } from '../constants/scan'

function ScanButton({ onScan, isScanning }) {
  const label = isScanning ? SCAN_LABEL.SCANNING : SCAN_LABEL.IDLE
  const spinClass = isScanning ? SPINNING_CLASS : ''

  return (
    <button
      type="button"
      onClick={onScan}
      disabled={isScanning}
      aria-label={label}
      className="flex h-15 w-15 items-center justify-center rounded-full bg-surface-container text-primary shadow-sm transition-colors hover:bg-primary-fixed disabled:opacity-60"
    >
      <Icon name={SCAN_ICON} className={`text-3xl ${spinClass}`} />
    </button>
  )
}

export default ScanButton