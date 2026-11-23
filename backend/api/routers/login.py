from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from api.constants import ErrorMessage, Route, Tag
from api.converters import to_current_user_response
from api.error_handling import bad_request
from api.schemas import CurrentUserResponse
from auth.constants import FRONTEND_BASE_URL
from auth.gmail_auth import build_authorization_url, complete_login
from auth.login_state import consume_state, create_state
from auth.user_profile import fetch_user_profile

router = APIRouter(tags=[Tag.AUTH])


@router.get(Route.AUTH_LOGIN)
def start_login():
    """Sends the browser to Google, where the person allows access to Gmail."""
    return RedirectResponse(build_authorization_url(create_state()))


@router.get(Route.AUTH_CALLBACK)
def finish_login(code: str | None = None, state: str | None = None):
    """Receives the person back from Google, saves the login, and returns to the page."""
    if not consume_state(state):
        raise bad_request(ErrorMessage.INVALID_LOGIN_STATE)

    if code is not None:
        complete_login(code)

    return RedirectResponse(FRONTEND_BASE_URL)


@router.get(Route.AUTH_ME, response_model=CurrentUserResponse)
def get_current_user():
    """Returns the name and picture of the person who is logged in."""
    return to_current_user_response(fetch_user_profile())