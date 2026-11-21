from typing import Final

from settings.config_manager import get_default_config, get_setting

DAYS_BEFORE_DELETION_KEY: Final = "days_before_deletion"
REMINDER_LEAD_DAYS: Final = 1


def get_days_before_deletion() -> int:
    saved_value = get_setting(DAYS_BEFORE_DELETION_KEY)
    if saved_value is not None:
        return saved_value
    return get_default_config()[DAYS_BEFORE_DELETION_KEY]


def calculate_days_left(days_old: int, days_before_deletion: int) -> int:
    return max(0, days_before_deletion - days_old)


def is_due_for_reminder(days_old: int, days_before_deletion: int) -> bool:
    return days_old == days_before_deletion - REMINDER_LEAD_DAYS


def is_due_for_deletion(days_old: int, days_before_deletion: int) -> bool:
    return days_old >= days_before_deletion