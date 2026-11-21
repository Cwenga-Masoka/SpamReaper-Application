import ActionButton from './ActionButton'
import { BUTTON_SIZE, BUTTON_VARIANT } from '../constants/buttons'
import {
  BULK_KEEP_ACTION,
  BULK_TRASH_ACTION,
  SELECT_ALL_LABEL,
} from '../constants/bulkActions'

function BulkActionBar({
  selectedCount,
  areAllSelected,
  onToggleSelectAll,
  onTrashSelected,
  onKeepSelected,
}) {
  const hasSelection = selectedCount > 0

  return (
    <div className="flex items-center justify-between px-1 py-1">
      <label className="flex cursor-pointer items-center gap-4">
        <input
          type="checkbox"
          checked={areAllSelected}
          onChange={onToggleSelectAll}
          className="h-5 w-5 cursor-pointer accent-primary"
        />
        <span className="select-none text-xl font-semibold text-on-surface-variant">
          {SELECT_ALL_LABEL} ({selectedCount})
        </span>
      </label>

      <div className="flex h-15 items-center gap-4">
        <ActionButton
          {...BULK_TRASH_ACTION}
          size={BUTTON_SIZE.COMPACT}
          variant={BUTTON_VARIANT.DANGER}
          isDisabled={!hasSelection}
          onClick={onTrashSelected}
        />
        <ActionButton
          {...BULK_KEEP_ACTION}
          size={BUTTON_SIZE.COMPACT}
          isDisabled={!hasSelection}
          onClick={onKeepSelected}
        />
      </div>
    </div>
  )
}

export default BulkActionBar