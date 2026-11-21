from unittest.mock import patch

from gmail.email_deleter import trash_email
from storage.action_history import ActionHistoryRepository
from storage.flagged_emails import FlaggedMessageRepository

TEST_ID = "test-history-1"

flagged_repo = FlaggedMessageRepository()
history_repo = ActionHistoryRepository()
flagged_repo.initialize_db()
history_repo.initialize_db()

flagged_repo.flag_message(TEST_ID, "Test Sender <test@example.com>", "Preview text", "Test subject")

with patch("gmail.email_deleter._move_to_gmail_trash"):
    print("trash_email returned:", trash_email(TEST_ID, flagged_repo, history_repo))

print("still flagged:", flagged_repo.get_flagged_message(TEST_ID))
print([record for record in history_repo.get_action_history() if record["sms_id"] == TEST_ID])
history_repo.delete_history_record(TEST_ID)