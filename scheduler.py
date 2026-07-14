#Threading will let us run the scheduler in the background
import threading

# time gives us the sleep() function which pauses execution
# we use this to make our scheduler check once evry 24 hours
import time

# datetime will allow us to work with dates and time in Python
from datetime import datetime

# We then import all the modules that we have already built
from email_reader import get_spam_emails       # reads spam from Gmail
from tracker_db import flag_message, flag_messages_bulk, get_messages_due_for_deletion
from email_deleter import trash_multiple_emails # deletes confirmed spam
from notifier import send_reminder_notification
from config_manager import get_setting, save_setting

def run_daily_scan(force=False):
    try:
        import time
        last_scan = get_setting("last_scan_at") or 0
        hours_since_scan = (time.time() - last_scan) / 3600

        if not force and hours_since_scan < 23:
            print(f"Scan skipped — last scan was {hours_since_scan:.1f} hours ago.")
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: _notify_scan_complete())
            return

        print(f"Running daily scan at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        spam_emails = get_spam_emails()

        if not spam_emails:
            print("No spam emails found today.")
        else:
            flag_messages_bulk(spam_emails)
            print(f"Flagged {len(spam_emails)} spam emails.")

        save_setting("last_scan_at", time.time())

        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: _notify_scan_complete())

    except Exception as e:
        error_msg = str(e)
        print(f"Scan failed: {error_msg}")
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: _notify_scan_failed(error_msg))

def _notify_scan_complete():
    from kivymd.app import MDApp
    from review_screen import ReviewScreen
    app = MDApp.get_running_app()
    if app and app.root:
        for widget in app.root.walk():
            if isinstance(widget, ReviewScreen):
                widget._scan_running = False
                widget._initial_scan_done = True
                if hasattr(widget, '_loading_event') and widget._loading_event:
                    widget._loading_event.cancel()
                    widget._loading_event = None
                for icon_id in ("sync_icon_inbox", "sync_icon_history", "sync_icon_settings"):
                    if icon_id in app.root.ids:
                        app.root.ids[icon_id].icon = "sync"
                widget.refresh_list()
                break

def _notify_scan_failed(error_msg):
    """Called on main thread when a scan fails — shows error in inbox."""
    from kivymd.app import MDApp
    from review_screen import ReviewScreen
    app = MDApp.get_running_app()
    if app and app.root:
        for widget in app.root.walk():
            if isinstance(widget, ReviewScreen):
                widget._scan_running = False
                widget._initial_scan_done = True
                if hasattr(widget, '_loading_event') and widget._loading_event:
                    widget._loading_event.cancel()
                    widget._loading_event = None
                for icon_id in ("sync_icon_inbox", "sync_icon_history", "sync_icon_settings"):
                    if icon_id in app.root.ids:
                        app.root.ids[icon_id].icon = "sync"
                widget.show_scan_error(error_msg)
                break

def check_for_deletions():
    """
    Checks our tracking database for messages that have been
    flagged fro more than 5 day and handles them accordingly.
    - If it is exactly day 5, we send a reminder notification to the user about the pending deletion
    - If it is more than day 5, we delete the message from Android and remove it from our tracking database
    """

    #Fetch all messages that are 5+ days old and not marked to keep
    due_messages = get_messages_due_for_deletion()

    # If nothing is due for deletion, we have nothing to do
    if not due_messages:
        print("No messages due for deletion today.")
        return
    
    # We separate messages into two groups:
    # 1. Messages that are exactly 5 days old - we will send a reminder notification for these
    # 2. Messages that are more than 5 days old - we will delete these automatically

    notify_list = []
    delete_list = []

    # We get today's date to comapare against the flagged date of each message
    today = datetime.now().date()

    for message in due_messages:
        # Parse the flagged_on date string int o a date object
        # strptime() converts a string to a datetime object based on the format we specify
        flagged_date = datetime.strptime(message["flagged_on"], "%Y-%m-%d").date()

        # Calculate how old the flagged message is in days
        days_old = (today - flagged_date).days

        if days_old == 5:
            notify_list.append(message)
        
        elif days_old > 5:
            delete_list.append(message)

    if notify_list:
        print(f"Sending reminder notifications for {len(notify_list)} messages that are due for deletion in 24 hours.")
        send_reminder_notification(notify_list)

    if delete_list:
        print(f"Auto deleting {len(delete_list)} emails past day 5.")
        ids_to_delete = [msg["sms_id"] for msg in delete_list]
        trash_multiple_emails(ids_to_delete)

def scheduler_loop():
    """
    Runs forever in the background, executing our scans
    and deletion check once every 24 hours.
    This runs on a separate threads so that the app UI stays repsonsive.
    """

    while True:
        run_daily_scan()
        check_for_deletions()

        # Sleep for 24 hours before running again
        print("Scheduler sleeping for 24 hours...")
        hours = get_setting("scan_interval_hours") or 24
        time.sleep(hours * 3600) 

def start_scheduler():
    """
    This is the function we call from our main app to start the scheduler.
    It creates a new thread that runs the scheduler_loop() function in the background.
    deamon=True means that this thread will automatically close when the main app closes, 
    so we don't have to worry about it running forever after the user exits the app.
    """

    scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
    # We set daemon=True so that this thread will automatically close when the main app closes

    scheduler_thread.start()
    print("Scheduler started in background thread.")


