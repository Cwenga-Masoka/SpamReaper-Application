import requests

from auth.constants import REQUEST_TIMEOUT_SECONDS, USERINFO_URL
from auth.gmail_auth import get_access_token


def fetch_user_profile() -> dict:
    """Asks Google for the name, picture and email of the person who is logged in."""
    response = requests.get(
        USERINFO_URL,
        headers={"Authorization": f"Bearer {get_access_token()}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()