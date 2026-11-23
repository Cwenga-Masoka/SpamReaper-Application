import secrets

from auth.constants import STATE_BYTES

_pending_states: set[str] = set()


def create_state() -> str:
    """Creates a random code that proves the login came back from the one we started."""
    state = secrets.token_urlsafe(STATE_BYTES)
    _pending_states.add(state)
    return state


def consume_state(state: str | None) -> bool:
    """Returns True once for a code we created, then forgets it."""
    if state is None:
        return False

    try:
        _pending_states.remove(state)
    except KeyError:
        return False
    return True