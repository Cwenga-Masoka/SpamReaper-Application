from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse

from api.constants import STATUS_SUCCESS, ErrorMessage, Route, Tag
from api.converters import to_current_user_response
from api.dependencies import LOGIN_REQUIRED
from api.error_handling import bad_request, forbidden
from api.schemas import CurrentUserResponse
from auth.constants import FRONTEND_BASE_URL, SESSION_EMAIL_KEY
from auth.errors import NotOwnerError
from auth.gmail_auth import build_authorization_url, get_access_token
from auth.login_state import consume_state, create_state
from auth.owner_login import complete_owner_login
from auth.session_settings import SessionSettings, get_session_settings
from auth.user_profile import fetch_user_profile

router = APIRouter(tags=[Tag.AUTH])


@router.get(Route.AUTH_LOGIN)
def start_login():
    """Sends the browser to Google, where the person allows access to Gmail."""
    return RedirectResponse(build_authorization_url(create_state()))


@router.get(Route.AUTH_CALLBACK)
def finish_login(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    settings: SessionSettings = Depends(get_session_settings),
):
    """
    Receives the person back from Google. Only the owner's Google account is
    accepted: the login is saved and a session cookie is set. Then returns to the page.
    """
    if not consume_state(state):
        raise bad_request(ErrorMessage.INVALID_LOGIN_STATE)

    if code is not None:
        try:
            complete_owner_login(code, settings.owner_email)
        except NotOwnerError as error:
            raise forbidden(str(error)) from error
        request.session[SESSION_EMAIL_KEY] = settings.owner_email

    return RedirectResponse(FRONTEND_BASE_URL)


@router.get(Route.AUTH_ME, response_model=CurrentUserResponse, dependencies=LOGIN_REQUIRED)
def get_current_user():
    """Returns the name and picture of the person who is logged in."""
    return to_current_user_response(fetch_user_profile(get_access_token()))


@router.post(Route.AUTH_LOGOUT)
def logout(request: Request):
    """Ends the browser session. The Gmail connection stays, so the scheduler keeps working."""
    request.session.clear()
    return {"status": STATUS_SUCCESS}