import platform
from datetime import datetime

def format_notification_message(messages: list) -> str:
    header = f"{len(messages)} spam message(s) will be deleted tomorrow.\n"
    preview_lines = []
    for message in messages[:3]:
        line = f"From: {message['sender']}: {message['preview'][:30]}..."
        preview_lines.append(line)

    if len(messages) > 3:
        preview_lines.append(f"...and {len(messages) - 3} more messages.")

    full_message = header + "\n".join(preview_lines)
    return full_message

def send_reminder_notification(messages: list):
    """
    Sends a native Android push notification reminding the user
    that their flagged messages are about to be deleted.
    The user can tap the notificcation to open SpamReaper and review them
    """
    # If somehow this got called with an empty list we do nothing
    if not messages:
        print("No messages to notify about.")
        return
    
    #We only send this notification on Android on PC it is just printed for testing purposes
    if platform.system() != "Linux":
        print("--- NOTIFICATION SIMULATION (PC mode) ---")
        print(f"Title: SpamReaper — Messages Pending Deletion")
        print(f"Body: {format_notification_message(messages)}")
        print("-----------------------------------------")
        return
    try:
        from plyer import notification  # type: ignore
        message_body = format_notification_message(messages)

        #notification.notify() is the plyer function that actually
        #sends the notification to the Android notification bar
        notification.notify(
            # The bold title at the top of the notification
            title = "SpamReaper - Messages Pending Deletion",

            # The body text below the title
            message = message_body,

            # The name of the app shown in the notification bar
            app_name="SpamReaper",

            # How long the notification stays on screen in seconds
            # 0 means it stays until the user dismisses it manually
            timeout=0    
        )

        print(f"Reminder notification sent at {datetime.now().strftime('%H:%M:%S')}")

    except Exception as e:
        #If the notification fails for any reason it is logged but the app does not crash
        print(f"Failed to send notification: {e}")

def send_test_notification():
    """
    Sends a fake test notification using dummy data.
    Useful for checking that your notification system works
    before you deploy to a real Android device.
    """

    # We create two fake message dictionaries that look exactly
    # like what our real database would return
    dummy_messages = [
        {
            "sms_id": "001",
            "sender": "+27831234567",
            "preview": "Congratulations you have won a R5000 prize",
            "flagged_on": "2026-04-02"
        },
        {
            "sms_id": "002",
            "sender": "56789",
            "preview": "Your account has been suspended click here",
            "flagged_on": "2026-04-02"
        }
    ]

    # We call the real notification function with our fake data
    send_reminder_notification(dummy_messages)