from collections.abc import Callable
from typing import Final

SUCCEEDED_KEY: Final = "succeeded"
FAILED_KEY: Final = "failed"


def run_for_each(
    email_ids: list[str],
    action: Callable[[str], bool],
) -> dict[str, list[str]]:
    """Runs the action for every email id and sorts the ids by the result."""
    results: dict[str, list[str]] = {SUCCEEDED_KEY: [], FAILED_KEY: []}

    for email_id in email_ids:
        outcome_key = SUCCEEDED_KEY if action(email_id) else FAILED_KEY
        results[outcome_key].append(email_id)

    return results