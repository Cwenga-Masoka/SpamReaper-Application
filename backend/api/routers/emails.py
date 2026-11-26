from fastapi import APIRouter, Depends

from api.constants import STATUS_SUCCESS, ErrorMessage, Route, Tag
from api.converters import to_spam_email_response
from api.dependencies import LOGIN_REQUIRED, get_db_repo, get_history_repo
from api.error_handling import bad_request
from api.schemas import EmailIdsRequest, SpamEmailResponse
from gmail.email_deleter import (
    trash_email,
    trash_multiple_emails,
    untrash_email,
    untrash_multiple_emails,
)
from gmail.email_reader import get_spam_emails
from storage.flagged_emails import FlaggedMessageRepository
from spam.retention import get_days_before_deletion
from storage.action_history import ActionHistoryRepository
from spam.email_keeper import keep_email, keep_multiple_emails

router = APIRouter(tags=[Tag.EMAILS], dependencies=LOGIN_REQUIRED)

@router.get(Route.FLAGGED, response_model=list[SpamEmailResponse])
def get_flagged_messages(
    db: FlaggedMessageRepository = Depends(get_db_repo),
    days_before_deletion: int = Depends(get_days_before_deletion),
):
    """Returns all pending flagged spam messages for review."""
    messages = db.get_all_flagged_messages()
    return [to_spam_email_response(message, days_before_deletion) for message in messages]


@router.post(Route.SCAN)
def trigger_scan(db: FlaggedMessageRepository = Depends(get_db_repo)):
    """Manually triggers an inbox scan for new spam emails."""
    spam_emails = get_spam_emails(db)
    if spam_emails:
        db.flag_messages_bulk(spam_emails)
    return {"status": STATUS_SUCCESS, "new_spam_found": len(spam_emails)}


@router.post(Route.TRASH_BULK)
def trash_bulk_emails(
    payload: EmailIdsRequest,
    db: FlaggedMessageRepository = Depends(get_db_repo),
    history_repo: ActionHistoryRepository = Depends(get_history_repo),
):
    """Trashes multiple emails at once from the React dashboard."""
    result = trash_multiple_emails(payload.email_ids, db, history_repo)
    return {"status": STATUS_SUCCESS, "result": result}


@router.post(Route.TRASH_ONE)
def trash_single_email(
    email_id: str,
    db: FlaggedMessageRepository = Depends(get_db_repo),
    history_repo: ActionHistoryRepository = Depends(get_history_repo),
):
    """Moves a single email to Gmail trash and removes it from tracking."""
    if not trash_email(email_id, db, history_repo):
        raise bad_request(ErrorMessage.TRASH_FAILED)
    return {"status": STATUS_SUCCESS, "email_id": email_id}

@router.post(Route.UNTRASH_BULK)
def restore_bulk_emails(
    payload: EmailIdsRequest,
    db: FlaggedMessageRepository = Depends(get_db_repo),
    history_repo: ActionHistoryRepository = Depends(get_history_repo),
):
    """Restores multiple emails from Gmail trash and marks them as kept."""
    result = untrash_multiple_emails(payload.email_ids, db, history_repo)
    return {"status": STATUS_SUCCESS, "result": result}


@router.post(Route.UNTRASH_ONE)
def restore_single_email(
    email_id: str,
    db: FlaggedMessageRepository = Depends(get_db_repo),
    history_repo: ActionHistoryRepository = Depends(get_history_repo),
):
    """Restores an email from Gmail trash back to the inbox and marks it as kept."""
    if not untrash_email(email_id, db, history_repo):
        raise bad_request(ErrorMessage.RESTORE_FAILED)
    return {"status": STATUS_SUCCESS, "email_id": email_id}

@router.post(Route.KEEP_BULK)
def mark_messages_to_keep(
    payload: EmailIdsRequest,
    db: FlaggedMessageRepository = Depends(get_db_repo),
    history_repo: ActionHistoryRepository = Depends(get_history_repo),
):
    """Marks multiple emails as safe at once."""
    result = keep_multiple_emails(payload.email_ids, db, history_repo)
    return {"status": STATUS_SUCCESS, "result": result}

@router.post(Route.KEEP)
def mark_message_to_keep(
    email_id: str,
    db: FlaggedMessageRepository = Depends(get_db_repo),
):
    """Marks an email as safe so SpamReaper never deletes it."""
    db.mark_keep(email_id)
    return {"status": STATUS_SUCCESS, "email_id": email_id}