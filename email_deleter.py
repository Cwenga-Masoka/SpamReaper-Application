from gmail_auth import get_access_token
from tracker_db import delete_record

import requests

GMAIL_API_BASE = 'https://gmail.googleapis.com/gmail/v1/users/me'

def trash_email(email_id: str) -> bool:
    """
    Moves a single email to Gmail's Trash folder using a direct
    HTTP POST request instead of the old library call.
    """

    try:
        # We get a fresh, valid access token for this operation
        access_token = get_access_token()

        headers = {'Authorization': f'Bearer {access_token}'}

        # trash is a POST request with no extra data needed —
        # the email ID in the URL is all Gmail needs to know what to trash
        response = requests.post(
            f'{GMAIL_API_BASE}/messages/{email_id}/trash',
            headers=headers
        )

        response.raise_for_status()

        delete_record(email_id)

        print(f"Successfully trashed email with ID {email_id}")
        return True

    except Exception as e:
        print(f"Error trashing email {email_id}: {e}")
        return False

def untrash_email(email_id: str) -> bool:
    """
    Restores a single email from Gmail's Trash back to the inbox.
    Only works if the email is still in Trash — Gmail permanently
    deletes trashed items after 30 days.
    """
    try:
        access_token = get_access_token()
        headers = {'Authorization': f'Bearer {access_token}'}

        # untrash is a POST request — same pattern as trash but opposite endpoint
        response = requests.post(
            f'{GMAIL_API_BASE}/messages/{email_id}/untrash',
            headers=headers
        )

        response.raise_for_status()
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

def trash_multiple_emails(email_id_list: list) -> dict:
    """
    Trashes multiple emails at once.
    """

    results = {
        "succeeded": [],
        "failed": []
    }

    for email_id in email_id_list:
        if trash_email(email_id):
            results["succeeded"].append(email_id)
        else:
            results["failed"].append(email_id)

    print(f"Trash complete — Succeeded: {len(results['succeeded'])}, Failed: {len(results['failed'])}")

    return results


