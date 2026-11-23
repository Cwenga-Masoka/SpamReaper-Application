from typing import Final

NOT_LOGGED_IN_MESSAGE: Final = "Not logged in yet — please connect your Gmail account first."
LOGIN_EXPIRED_MESSAGE: Final = "Your Gmail login expired — please connect your Gmail account again."


class NotLoggedInError(Exception):
    """Raised when there is no usable Gmail login."""