from auth.constants import ACCESS_TOKEN_KEY, PROFILE_EMAIL_KEY, PROFILE_EMAIL_VERIFIED_KEY
from auth.errors import NOT_OWNER_MESSAGE, NotOwnerError
from auth.gmail_auth import exchange_code_for_tokens
from auth.token_store import save_token
from auth.user_profile import fetch_user_profile


def is_owner(profile: dict, owner_email: str) -> bool:
    """True only when Google says the email is verified and it is the owner's."""
    email = str(profile.get(PROFILE_EMAIL_KEY, "")).strip().lower()
    return profile.get(PROFILE_EMAIL_VERIFIED_KEY) is True and email == owner_email


def complete_owner_login(auth_code: str, owner_email: str) -> None:
    """
    Trades the one-time code for tokens, checks the Google account is the owner's,
    and only then saves the tokens. Raises NotOwnerError for anyone else.
    """
    token_data = exchange_code_for_tokens(auth_code)
    profile = fetch_user_profile(token_data[ACCESS_TOKEN_KEY])
    if not is_owner(profile, owner_email):
        raise NotOwnerError(NOT_OWNER_MESSAGE)
    save_token(token_data)