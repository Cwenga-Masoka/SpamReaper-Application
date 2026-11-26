import json
import time
from urllib.parse import urlencode

import requests

from auth.constants import (
    ACCESS_TOKEN_KEY,
    AUTH_URL,
    CLIENT_ID_KEY,
    CLIENT_SECRET_FILE,
    CLIENT_SECRET_KEY,
    CLIENT_SECRET_ROOT_KEY,
    EXPIRES_IN_KEY,
    LOGIN_REJECTED_STATUS_CODES,
    REDIRECT_URI,
    REFRESH_TOKEN_KEY,
    REQUEST_TIMEOUT_SECONDS,
    SAVED_AT_KEY,
    SCOPES,
    TOKEN_EXPIRY_MARGIN_SECONDS,
    TOKEN_URL,
)
from auth.errors import LOGIN_EXPIRED_MESSAGE, NOT_LOGGED_IN_MESSAGE, NotLoggedInError
from auth.token_store import load_token, save_token


def load_client_credentials() -> tuple[str, str]:
    """Reads the client id and secret from the downloaded Web client file."""
    with open(CLIENT_SECRET_FILE, "r") as file:
        client_info = json.load(file)[CLIENT_SECRET_ROOT_KEY]
    return client_info[CLIENT_ID_KEY], client_info[CLIENT_SECRET_KEY]


def build_authorization_url(state: str) -> str:
    """Builds the Google address where the person is sent to allow access."""
    client_id, _ = load_client_credentials()
    params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "state": state,
    }
    return f"{AUTH_URL}?{urlencode(params)}"


def _request_tokens(payload: dict) -> dict:
    """Asks Google's token address for tokens, adding the client id and secret."""
    client_id, client_secret = load_client_credentials()
    response = requests.post(
        TOKEN_URL,
        data={**payload, "client_id": client_id, "client_secret": client_secret},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def exchange_code_for_tokens(auth_code: str) -> dict:
    """Trades the one-time code from Google for tokens. Does not save them."""
    return _request_tokens(
        {
            "code": auth_code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
        }
    )


def _refresh_token_data(token_data: dict) -> dict:
    """Gets a new access token with the refresh token, and saves it."""
    refresh_token = token_data.get(REFRESH_TOKEN_KEY)
    if refresh_token is None:
        raise NotLoggedInError(LOGIN_EXPIRED_MESSAGE)

    try:
        new_token_data = _request_tokens(
            {"refresh_token": refresh_token, "grant_type": "refresh_token"}
        )
    except requests.HTTPError as error:
        if error.response.status_code in LOGIN_REJECTED_STATUS_CODES:
            raise NotLoggedInError(LOGIN_EXPIRED_MESSAGE) from error
        raise

    merged_token_data = {**new_token_data, REFRESH_TOKEN_KEY: refresh_token}
    save_token(merged_token_data)
    return merged_token_data


def _is_fresh(token_data: dict) -> bool:
    age_seconds = time.time() - token_data[SAVED_AT_KEY]
    return age_seconds < token_data[EXPIRES_IN_KEY] - TOKEN_EXPIRY_MARGIN_SECONDS


def get_access_token() -> str:
    """
    The function other files call to get a valid access token.
    Refreshes the token when it is about to expire.
    Raises NotLoggedInError when there is no login, or it can no longer be renewed.
    """
    token_data = load_token()
    if token_data is None:
        raise NotLoggedInError(NOT_LOGGED_IN_MESSAGE)

    if _is_fresh(token_data):
        return token_data[ACCESS_TOKEN_KEY]

    return _refresh_token_data(token_data)[ACCESS_TOKEN_KEY]