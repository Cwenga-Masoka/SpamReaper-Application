from typing import Final

from fastapi import Depends, Request

from auth.constants import SESSION_EMAIL_KEY
from auth.errors import NOT_LOGGED_IN_MESSAGE, NotLoggedInError
from auth.session_settings import SessionSettings, get_session_settings
from storage.action_history import ActionHistoryRepository
from storage.flagged_emails import FlaggedMessageRepository


def get_db_repo():
    return FlaggedMessageRepository()


def get_history_repo():
    return ActionHistoryRepository()


def require_login(
    request: Request,
    settings: SessionSettings = Depends(get_session_settings),
) -> None:
    """Lets the request through only when it carries the owner's login cookie."""
    if request.session.get(SESSION_EMAIL_KEY) != settings.owner_email:
        raise NotLoggedInError(NOT_LOGGED_IN_MESSAGE)


LOGIN_REQUIRED: Final = (Depends(require_login),)