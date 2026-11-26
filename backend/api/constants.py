from enum import StrEnum
from typing import Final
from auth.constants import CALLBACK_PATH, FRONTEND_BASE_URL
from spam.retention import DAYS_BEFORE_DELETION_KEY

APP_TITLE: Final = "SpamReaper API"
APP_VERSION: Final = "2.0.0"
WELCOME_MESSAGE: Final = "Welcome to SpamReaper API — Backend is running securely."
HISTORY_CLEARED_MESSAGE: Final = "History cleared."
STATUS_SUCCESS: Final = "success"

CORS_ALLOWED_ORIGINS: Final = (FRONTEND_BASE_URL,)
CORS_ALLOWED_METHODS: Final = ("GET", "POST", "DELETE")
CORS_ALLOWED_HEADERS: Final = ("Content-Type",)
CORS_ALLOW_CREDENTIALS: Final = True

API_PREFIX: Final = "/api"


class Route(StrEnum):
    ROOT = "/"
    FLAGGED = API_PREFIX + "/flagged"
    SCAN = API_PREFIX + "/scan"
    TRASH_BULK = API_PREFIX + "/trash/bulk"
    TRASH_ONE = API_PREFIX + "/trash/{email_id}"
    UNTRASH_BULK = API_PREFIX + "/untrash/bulk"
    UNTRASH_ONE = API_PREFIX + "/untrash/{email_id}"
    KEEP_BULK = API_PREFIX + "/keep/bulk"
    KEEP = API_PREFIX + "/keep/{email_id}"
    HISTORY = API_PREFIX + "/history"
    HISTORY_ITEM = API_PREFIX + "/history/{sms_id}"
    SETTINGS = API_PREFIX + "/settings"
    AUTH_LOGIN = API_PREFIX + "/auth/login"
    AUTH_ME = API_PREFIX + "/auth/me"
    AUTH_LOGOUT = API_PREFIX + "/auth/logout"
    AUTH_CALLBACK = CALLBACK_PATH


class ErrorMessage(StrEnum):
    INVALID_LOGIN_STATE = "Login could not be verified. Please try connecting again."
    TRASH_FAILED = "Failed to trash email."
    RESTORE_FAILED = "Failed to restore email."
    KEEP_FAILED = "Failed to keep email."
    SETTING_UPDATE_FAILED = "Failed to update setting '{key}'."
    INTERNAL_ERROR = "Something went wrong on the server."

class EditableSetting(StrEnum):
    DAYS_BEFORE_DELETION = DAYS_BEFORE_DELETION_KEY
    SCAN_INTERVAL_HOURS = "scan_interval_hours"
    MAX_NOTIFICATION_PREVIEWS = "max_notification_previews"
    SPAM_KEYWORDS = "spam_keywords"
    AUTO_DELETE_ENABLED = "auto_delete_enabled"
    NOTIFICATION_ENABLED = "notification_enabled"

class Tag(StrEnum):
    GENERAL = "general"
    EMAILS = "emails"
    HISTORY = "history"
    SETTINGS = "settings"
    AUTH = "auth"