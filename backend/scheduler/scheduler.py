import threading
import time
from datetime import datetime
from typing import Optional
from auth.errors import NotLoggedInError
from gmail.email_reader import get_spam_emails
from storage.flagged_emails import FlaggedMessageRepository
from gmail.email_deleter import trash_multiple_emails
from notifications.notifier import send_reminder_notification
from settings.config_manager import get_setting, save_setting
from spam.retention import get_days_before_deletion, is_due_for_deletion, is_due_for_reminder
from storage.action_history import ActionHistoryRepository

class SpamWorkflowService:
    """
    Encapsulates the business logic for scanning spam and checking deletions.
    Adheres to the Single Responsibility Principle by separating business rules from timing/threading.
    """
    def __init__(
        self,
        db_repo: Optional[FlaggedMessageRepository] = None,
        history_repo: Optional[ActionHistoryRepository] = None,
    ):
        self.db_repo = db_repo or FlaggedMessageRepository()
        self.history_repo = history_repo or ActionHistoryRepository()
    
    def run_daily_scan(self, force=False):
        """Runs the daily scan, fetching new spam emails and saving them via the repository."""
        try:
            last_scan = get_setting("last_scan_at") or 0
            hours_since_scan = (time.time() - last_scan) / 3600

            if not force and hours_since_scan < 23:
                print(f"Scan skipped — last scan was {hours_since_scan:.1f} hours ago.")
                return

            print(f"Running daily scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Pass the repository into get_spam_emails for proper dependency injection
            spam_emails = get_spam_emails(self.db_repo)

            if not spam_emails:
                print("No spam emails found today.")
            else:
                self.db_repo.flag_messages_bulk(spam_emails)
                print(f"Flagged {len(spam_emails)} spam emails.")

            save_setting("last_scan_at", time.time())

        except Exception as e:
            print(f"Scan failed: {str(e)}")

    def check_for_deletions(self):
        """Sends reminders and trashes messages according to the retention rules."""
        days_before_deletion = get_days_before_deletion()
        messages = self.db_repo.get_all_flagged_messages()

        notify_list = [
            message for message in messages
            if is_due_for_reminder(message["days_old"], days_before_deletion)
        ]
        delete_list = [
            message for message in messages
            if is_due_for_deletion(message["days_old"], days_before_deletion)
        ]

        if not notify_list and not delete_list:
            print("No messages due for deletion today.")
            return

        if notify_list:
            print(f"Sending reminder notifications for {len(notify_list)} messages.")
            send_reminder_notification(notify_list)

        if delete_list:
            print(f"Auto deleting {len(delete_list)} emails that reached the deletion limit.")
            ids_to_delete = [message["sms_id"] for message in delete_list]
            trash_multiple_emails(ids_to_delete, self.db_repo, self.history_repo)
            
def scheduler_loop():
    """
    Runs forever in the background, executing our scan and deletion checks on a timer.
    This runs on a separate thread so that the app backend stays responsive.
    """
    workflow = SpamWorkflowService()

    while True:
        workflow.run_daily_scan()
        try:
            workflow.check_for_deletions()
        except NotLoggedInError:
            print("Skipping deletions: not logged in to Gmail.")

        print("Scheduler sleeping for 24 hours...")
        hours = get_setting("scan_interval_hours") or 24
        time.sleep(hours * 3600) 


def start_scheduler():
    """
    Starts the scheduler loop in a background daemon thread.
    """
    scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
    scheduler_thread.start()
    print("Scheduler started in background thread.")