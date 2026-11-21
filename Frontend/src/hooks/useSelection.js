import { useState } from 'react'

export function useSelection(visibleIds) {
  const [selectedSet, setSelectedSet] = useState(() => new Set())

  const selectedIds = visibleIds.filter((id) => selectedSet.has(id))
  const areAllSelected = visibleIds.length > 0 && selectedIds.length === visibleIds.length

  const updateSelection = (change) =>
    setSelectedSet((previous) => {
      const next = new Set(previous)
      change(next)
      return next
    })

  const toggleSelect = (id) =>
    updateSelection((set) => (set.has(id) ? set.delete(id) : set.add(id)))

  const toggleSelectAll = () =>
    updateSelection((set) => {
      visibleIds.forEach((id) => (areAllSelected ? set.delete(id) : set.add(id)))
    })

  const clearSelection = () => setSelectedSet(new Set())

  return {
    selectedIds,
    selectedCount: selectedIds.length,
    areAllSelected,
    isSelected: (id) => selectedSet.has(id),
    toggleSelect,
    toggleSelectAll,
    clearSelection,
  }
}