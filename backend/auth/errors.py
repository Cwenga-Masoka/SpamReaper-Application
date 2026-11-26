from typing import Final

NOT_LOGGED_IN_MESSAGE: Final = "Not logged in yet — please connect your Gmail account first."
LOGIN_EXPIRED_MESSAGE: Final = "Your Gmail login expired — please connect your Gmail account again."
NOT_OWNER_MESSAGE: Final = "This Google account is not allowed to use this SpamReaper."


class NotLoggedInError(Exception):
    """Raised when there is no usable Gmail login."""

class NotOwnerError(Exception):
    """Raised when someone other than the owner tries to log in."""