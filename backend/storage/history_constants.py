from enum import StrEnum
from typing import Final

GMAIL_TRASH_RETENTION_DAYS: Final = 30


class HistoryAction(StrEnum):
    DELETED = "deleted"
    KEPT = "kept"