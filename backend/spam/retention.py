from typing import Final

from settings.config_manager import get_setting_or_default

DAYS_BEFORE_DELETION_KEY: Final = "days_before_deletion"
AUTO_DELETE_ENABLED_KEY: Final = "auto_delete_enabled"
REMINDER_LEAD_DAYS: Final = 1


def get_days_before_deletion() -> int:
    return get_setting_or_default(DAYS_BEFORE_DELETION_KEY)


def is_auto_delete_enabled() -> bool:
    return get_setting_or_default(AUTO_DELETE_ENABLED_KEY)


def calculate_days_left(days_old: int, days_before_deletion: int) -> int:
    return max(0, days_before_deletion - days_old)


def is_due_for_reminder(days_old: int, days_before_deletion: int) -> bool:
    return days_old == days_before_deletion - REMINDER_LEAD_DAYS


def is_due_for_deletion(days_old: int, days_before_deletion: int) -> bool:
    return days_old >= days_before_deletion