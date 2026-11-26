from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api.constants import (
    APP_TITLE,
    APP_VERSION,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOWED_HEADERS,
    CORS_ALLOWED_METHODS,
    CORS_ALLOWED_ORIGINS,
)
from api.error_handling import convert_not_logged_in_to_401, convert_unexpected_errors_to_500
from api.lifespan import lifespan
from api.routers import app_settings, emails, history, login, root
from auth.constants import (
    SESSION_COOKIE_NAME,
    SESSION_HTTPS_ONLY,
    SESSION_MAX_AGE_SECONDS,
    SESSION_SAME_SITE,
)
from auth.errors import NotLoggedInError
from auth.session_settings import get_session_settings

app = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan)

app.add_exception_handler(NotLoggedInError, convert_not_logged_in_to_401)

# Added BEFORE the CORS middleware, so it sits inside it. That way, even
# error responses still get the CORS headers and the browser can read them.
app.add_middleware(BaseHTTPMiddleware, dispatch=convert_unexpected_errors_to_500)

app.add_middleware(
    SessionMiddleware,
    secret_key=get_session_settings().secret_key,
    session_cookie=SESSION_COOKIE_NAME,
    max_age=SESSION_MAX_AGE_SECONDS,
    same_site=SESSION_SAME_SITE,
    https_only=SESSION_HTTPS_ONLY,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ALLOWED_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOWED_METHODS,
    allow_headers=CORS_ALLOWED_HEADERS,
)

app.include_router(root.router)
app.include_router(emails.router)
app.include_router(history.router)
app.include_router(login.router)
app.include_router(app_settings.router)