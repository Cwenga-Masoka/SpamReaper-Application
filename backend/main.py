from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from api.constants import (
    APP_TITLE,
    APP_VERSION,
    CORS_ALLOW_CREDENTIALS,
    CORS_ALLOWED_HEADERS,
    CORS_ALLOWED_METHODS,
    CORS_ALLOWED_ORIGINS,
)
from api.error_handling import convert_unexpected_errors_to_500
from api.lifespan import lifespan
from api.routers import app_settings, emails, history, root

app = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan)

# Added BEFORE the CORS middleware, so it sits inside it. That way, even
# error responses still get the CORS headers and the browser can read them.
app.add_middleware(BaseHTTPMiddleware, dispatch=convert_unexpected_errors_to_500)

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
app.include_router(app_settings.router)