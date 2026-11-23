import json
import time
from pathlib import Path

from auth.constants import SAVED_AT_KEY, TOKEN_FILE


def save_token(token_data: dict) -> None:
    """Saves the token to disk, together with the time it was saved."""
    token_with_time = {**token_data, SAVED_AT_KEY: time.time()}
    Path(TOKEN_FILE).write_text(json.dumps(token_with_time))


def load_token() -> dict | None:
    """Returns the saved token, or None if there is none or it cannot be read."""
    token_path = Path(TOKEN_FILE)
    if not token_path.exists():
        return None

    try:
        return json.loads(token_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None