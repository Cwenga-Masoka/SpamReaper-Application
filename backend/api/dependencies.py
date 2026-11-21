from storage.action_history import ActionHistoryRepository
from storage.flagged_emails import FlaggedMessageRepository


def get_db_repo():
    return FlaggedMessageRepository()


def get_history_repo():
    return ActionHistoryRepository()