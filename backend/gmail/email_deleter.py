from auth.gmail_auth import get_access_token
from storage.action_history import ActionHistoryRepository
from storage.flagged_emails import FlaggedMessageRepository
from storage.history_constants import HistoryAction
from typing import Optional
import requests

GMAIL_API_BASE = 'https://gmail.googleapis.com/gmail/v1/users/me'


def _move_to_gmail_trash(email_id: str):
    access_token = get_access_token()
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.post(
        f'{GMAIL_API_BASE}/messages/{email_id}/trash',
        headers=headers
    )
    response.raise_for_status()


def _record_deletion(history_repo: ActionHistoryRepository, flagged_message: Optional[dict]):
    if flagged_message is None:
        return

    history_repo.log_flagged_message(flagged_message, HistoryAction.DELETED)


def trash_email(
    email_id: str,
    db_repo: Optional[FlaggedMessageRepository] = None,
    history_repo: Optional[ActionHistoryRepository] = None,
) -> bool:
    """
    Moves a single email to Gmail's Trash folder, records it in the action
    history, and removes it from the flagged list.
    """
    if db_repo is None:
        db_repo = FlaggedMessageRepository()
    if history_repo is None:
        history_repo = ActionHistoryRepository()

    try:
        flagged_message = db_repo.get_flagged_message(email_id)

        _move_to_gmail_trash(email_id)
        _record_deletion(history_repo, flagged_message)
        db_repo.delete_record(email_id)

        print(f"Successfully trashed email with ID {email_id}")
        return True

    except Exception as e:
        print(f"Error trashing email {email_id}: {e}")
        return False


def untrash_email(email_id: str, history_repo: Optional[ActionHistoryRepository] = None) -> bool:
    """
    Restores a single email from Gmail's Trash back to the inbox and removes
    its "deleted" entry from the action history.
    Only works if the email is still in Trash — Gmail permanently
    deletes trashed items after 30 days.
    """
    if history_repo is None:
        history_repo = ActionHistoryRepository()

    try:
        access_token = get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}

        response = requests.post(
            f'{GMAIL_API_BASE}/messages/{email_id}/untrash',
            headers=headers
        )

        response.raise_for_status()
        history_repo.delete_history_record(email_id)

        print(f"Successfully restored email with ID {email_id}")
        return True

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            # Email no longer exists in Trash — permanently deleted by Gmail
            print(f"Email {email_id} no longer in Trash — may have been permanently deleted")
        else:
            print(f"Error restoring email {email_id}: {e}")
        return False

    except Exception as e:
        print(f"Error restoring email {email_id}: {e}")
        return False


def trash_multiple_emails(
    email_id_list: list,
    db_repo: Optional[FlaggedMessageRepository] = None,
    history_repo: Optional[ActionHistoryRepository] = None,
) -> dict:
    """
    Trashes multiple emails at once.
    """
    if db_repo is None:
        db_repo = FlaggedMessageRepository()
    if history_repo is None:
        history_repo = ActionHistoryRepository()

    results = {
        "succeeded": [],
        "failed": []
    }

    for email_id in email_id_list:
        if trash_email(email_id, db_repo, history_repo):
            results["succeeded"].append(email_id)
        else:
            results["failed"].append(email_id)

    print(f"Trash complete — Succeeded: {len(results['succeeded'])}, Failed: {len(results['failed'])}")

    return results


def untrash_multiple_emails(
    email_id_list: list,
    history_repo: Optional[ActionHistoryRepository] = None,
) -> dict:
    """
    Restores multiple emails from Trash at once.
    """
    if history_repo is None:
        history_repo = ActionHistoryRepository()

    results = {
        "succeeded": [],
        "failed": []
    }
    for email_id in email_id_list:
        if untrash_email(email_id, history_repo):
            results["succeeded"].append(email_id)
        else:
            results["failed"].append(email_id)

    print(f"Restore complete — Succeeded: {len(results['succeeded'])}, Failed: {len(results['failed'])}")
    return results