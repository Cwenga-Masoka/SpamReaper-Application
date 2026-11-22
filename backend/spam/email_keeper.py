from storage.action_history import ActionHistoryRepository
from storage.flagged_emails import FlaggedMessageRepository
from storage.history_constants import HistoryAction
from spam.bulk import run_for_each


def keep_email(
    email_id: str,
    db_repo: FlaggedMessageRepository,
    history_repo: ActionHistoryRepository,
) -> bool:
    """
    Marks a flagged email as safe and records it in the action history.
    Returns False if the email is not in the flagged list.
    """
    flagged_message = db_repo.get_flagged_message(email_id)
    if flagged_message is None:
        return False

    history_repo.log_flagged_message(flagged_message, HistoryAction.KEPT)
    db_repo.mark_keep(email_id)
    return True


def keep_multiple_emails(
    email_ids: list[str],
    db_repo: FlaggedMessageRepository,
    history_repo: ActionHistoryRepository,
) -> dict[str, list[str]]:
    """Marks several flagged emails as safe. Returns which ids worked and which failed."""
    return run_for_each(
        email_ids,
        lambda email_id: keep_email(email_id, db_repo, history_repo),
    )