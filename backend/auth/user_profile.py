import requests

from auth.constants import REQUEST_TIMEOUT_SECONDS, USERINFO_URL


def fetch_user_profile(access_token: str) -> dict:
    """Asks Google for the name, picture and email of the person the token belongs to."""
    response = requests.get(
        USERINFO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()