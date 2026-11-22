import BulkActionBar from '../components/BulkActionBar'
import EmailList from '../components/EmailList'
import FilterChips from '../components/FilterChips'
import Greeting from '../components/Greeting'
import Header from '../components/Header'
import ScanButton from '../components/ScanButton'
import SearchBar from '../components/SearchBar'
import Toast from '../components/Toast'
import { NO_EMAILS } from '../constants/inbox'
import { TEMPORARY_USER } from '../constants/user'
import { useEmailActions } from '../hooks/useEmailActions'
import { useFetch } from '../hooks/useFetch'
import { useInboxFilters } from '../hooks/useInboxFilters'
import { useScan } from '../hooks/useScan'
import { useSelection } from '../hooks/useSelection'
import { useToast } from '../hooks/useToast'
import { fetchFlaggedEmails } from '../services/api'

const PAGE_CLASSES =
  'flex min-h-screen flex-col gap-4 bg-surface p-4 pt-24 font-sans text-on-surface'

function HomeScreen() {
  const { data: emails, isLoading, hasError, reload } = useFetch(
    fetchFlaggedEmails,
    NO_EMAILS,
  )
  const {
    searchText,
    setSearchText,
    activeFilter,
    setActiveFilter,
    visibleEmails,
    counts,
  } = useInboxFilters(emails)
  const {
    selectedIds,
    selectedCount,
    areAllSelected,
    isSelected,
    toggleSelect,
    toggleSelectAll,
  } = useSelection(visibleEmails.map((email) => email.id))
  const { toastProps, showToast } = useToast()
  const { keep, trash, keepMany, trashMany } = useEmailActions({
    showToast,
    onActionDone: reload,
  })
  const { scan, isScanning } = useScan({ showToast, onScanDone: reload })

  const hasVisibleEmails = visibleEmails.length > 0

  return (
    <div className={PAGE_CLASSES}>
      <Header userName={TEMPORARY_USER.name} avatarUrl={TEMPORARY_USER.avatarUrl} />
      <Greeting
        userName={TEMPORARY_USER.name}
        pendingCount={emails.length}
        action={<ScanButton onScan={scan} isScanning={isScanning} />}
      />
      <SearchBar value={searchText} onChange={setSearchText} />
      <FilterChips
        counts={counts}
        activeFilter={activeFilter}
        onChange={setActiveFilter}
      />
      {hasVisibleEmails && (
        <BulkActionBar
          selectedCount={selectedCount}
          areAllSelected={areAllSelected}
          onToggleSelectAll={toggleSelectAll}
          onTrashSelected={() => trashMany(selectedIds)}
          onKeepSelected={() => keepMany(selectedIds)}
        />
      )}
      <EmailList
        emails={visibleEmails}
        isLoading={isLoading}
        hasError={hasError}
        onRetry={reload}
        isSelected={isSelected}
        onToggleSelect={toggleSelect}
        onKeep={keep}
        onTrash={trash}
      />
      <Toast {...toastProps} />
    </div>
  )
}

export default HomeScreen