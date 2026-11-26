from typing import Final

BACKEND_BASE_URL: Final = "http://localhost:8000"
CALLBACK_PATH: Final = "/api/auth/callback"
REDIRECT_URI: Final = BACKEND_BASE_URL + CALLBACK_PATH
FRONTEND_BASE_URL: Final = "http://localhost:5173"

AUTH_URL: Final = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL: Final = "https://oauth2.googleapis.com/token"

GMAIL_SCOPE: Final = "https://www.googleapis.com/auth/gmail.modify"
SCOPES: Final = (GMAIL_SCOPE, "openid", "email", "profile")

CLIENT_SECRET_FILE: Final = "web_client_secret.json"
CLIENT_SECRET_ROOT_KEY: Final = "web"
CLIENT_ID_KEY: Final = "client_id"
CLIENT_SECRET_KEY: Final = "client_secret"

TOKEN_FILE: Final = "gmail_token.json"
ACCESS_TOKEN_KEY: Final = "access_token"
REFRESH_TOKEN_KEY: Final = "refresh_token"
EXPIRES_IN_KEY: Final = "expires_in"
SAVED_AT_KEY: Final = "saved_at"

TOKEN_EXPIRY_MARGIN_SECONDS: Final = 60
REQUEST_TIMEOUT_SECONDS: Final = 10
LOGIN_REJECTED_STATUS_CODES: Final = (400, 401)
STATE_BYTES: Final = 32

USERINFO_URL: Final = "https://openidconnect.googleapis.com/v1/userinfo"
PROFILE_NAME_KEY: Final = "name"
PROFILE_PICTURE_KEY: Final = "picture"
PROFILE_EMAIL_KEY: Final = "email"

PROFILE_EMAIL_VERIFIED_KEY: Final = "email_verified"

SESSION_COOKIE_NAME: Final = "spamreaper_session"
SESSION_EMAIL_KEY: Final = "owner_email"
SESSION_MAX_AGE_DAYS: Final = 7
SECONDS_PER_DAY: Final = 24 * 60 * 60
SESSION_MAX_AGE_SECONDS: Final = SESSION_MAX_AGE_DAYS * SECONDS_PER_DAY
SESSION_SAME_SITE: Final = "lax"
SESSION_HTTPS_ONLY: Final = False  # set to True when the app goes online with HTTPS