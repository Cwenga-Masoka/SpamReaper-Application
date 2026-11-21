import { useState } from 'react'
import EmailCard from './components/EmailCard'
import FilterChips from './components/FilterChips'
import Greeting from './components/Greeting'
import Header from './components/Header'
import ScanButton from './components/ScanButton'
import SearchBar from './components/SearchBar'
import { ALL_FILTER } from './constants/filters'
import { RISK_LEVEL } from './constants/risk'
import { countEmailsByFilter, filterEmails } from './utils/emailFilters'
import BulkActionBar from './components/BulkActionBar'
import Toast from './components/Toast'
import { useSelection } from './hooks/useSelection'
import { useToast } from './hooks/useToast'
import { TOAST_KIND } from './constants/messages'

const SAMPLE_EMAILS = [
  { id: '1', senderName: 'Apex Crypto Signals', senderAddress: 'newsletter@apex-signals.io', subject: 'Instant 500x Whale Alert: Act within 2 hours!', preview: 'Join our VIP Telegram channel to reap maximum yield.', riskLevel: RISK_LEVEL.HIGH, daysLeft: 1 },
  { id: '2', senderName: 'CloudHosting Billing', senderAddress: 'support@billing-renewal.net', subject: 'Urgent: Your VPS server #9021 will be terminated', preview: 'Immediate payment required. Update your credentials now.', riskLevel: RISK_LEVEL.MEDIUM, daysLeft: 2 },
  { id: '3', senderName: 'MegaRetail Deals', senderAddress: 'promotions@daily-fashion.com', subject: 'Final clearance! Up to 80% off linen shirts', preview: 'Shop our warehouse sale before inventory runs out.', riskLevel: RISK_LEVEL.LOW, daysLeft: 3 },
]

function App() {
  const [searchText, setSearchText] = useState('')
  const [activeFilter, setActiveFilter] = useState(ALL_FILTER)
  const [isScanning, setIsScanning] = useState(false)

  const visibleEmails = filterEmails(SAMPLE_EMAILS, activeFilter, searchText)

  const { toastProps, showToast } = useToast()
  const {
    selectedCount,
    areAllSelected,
    isSelected,
    toggleSelect,
    toggleSelectAll,
    clearSelection,
  } = useSelection(visibleEmails.map((email) => email.id))

  const handleBulkAction = (toastKind) => {
    showToast(toastKind)
    clearSelection()
  }

  const FAKE_SCAN_DURATION_MS = 2000

  const startFakeScan = () => {
    setIsScanning(true)
    setTimeout(() => setIsScanning(false), FAKE_SCAN_DURATION_MS)
  }

  return (
    <div className="flex min-h-screen flex-col gap-4 bg-surface p-4 pt-24 font-sans text-on-surface">
      <Header userName="Elena" />
      <Greeting
        userName="Elena"
        pendingCount={SAMPLE_EMAILS.length}
        action={<ScanButton onScan={startFakeScan} isScanning={isScanning} />}
      />
      <SearchBar value={searchText} onChange={setSearchText} />
      <FilterChips
        counts={countEmailsByFilter(SAMPLE_EMAILS)}
        activeFilter={activeFilter}
        onChange={setActiveFilter}
      />

      <BulkActionBar
        selectedCount={selectedCount}
        areAllSelected={areAllSelected}
        onToggleSelectAll={toggleSelectAll}
        onTrashSelected={() => handleBulkAction(TOAST_KIND.TRASHED)}
        onKeepSelected={() => handleBulkAction(TOAST_KIND.KEPT)}
      />

      {visibleEmails.map((email) => (
        <EmailCard
          key={email.id}
          email={email}
          isSelected={isSelected(email.id)}
          onToggleSelect={toggleSelect}
          onKeep={() => {}}
          onTrash={() => {}}
        />
      ))}

      <Toast {...toastProps} />
    </div>
  )
}

export default App