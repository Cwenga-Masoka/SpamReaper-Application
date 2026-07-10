# Tracker Database
# This is our foundation. Before we can track spam messages, delete them, or send reminders, we need a place to store the state of every flagged message

import sqlite3
import os
from datetime import datetime

# The name of our local database file
DB_NAME = "spamreaper.db"
def get_connectio():
    """
    Create (or opens) a database file and returns a connection.
    We use check_same_thread=False because kivy runs on multiple threads
    """

    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    return conn

def initialize_db():

    """
    Creates the flagged_messages table if it doesn't exist. This table will store the message ID, the time it was flagged, and whether it will be deleted or not.
    Safe to call every time the app starts - it will not overwrite existing data.
    """
    conn = get_connectio()
    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS flagged_messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            sms_id      TEXT UNIQUE NOT NULL,
            sender      TEXT NOT NULL,
            subject     TEXT,
            preview     TEXT,
            flagged_on  TEXT NOT NULL,
            keep        INTEGER DEFAULT 0
        )
    """)

    # Create action_history table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS action_history (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            sms_id          TEXT NOT NULL,
            sender          TEXT NOT NULL,
            subject         TEXT,
            preview         TEXT,
            action          TEXT NOT NULL,
            actioned_on     TEXT NOT NULL
        )
    """)
    conn.commit()

    try:
        cursor.execute("ALTER TABLE flagged_messages ADD COLUMN subject TEXT")
        conn.commit()
        print("Migration: added subject column")
    except Exception:
        # Column already exists — this is expected on all runs after the first
        pass

    conn.commit()
    conn.close()

def flag_message(sms_id, sender, preview, subject=""):
    """
    Adds a new spam message to our tracking database.
    If the message is already flagged, we skip it (INSERT or IGNORE).
    """
    conn = get_connectio()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT OR IGNORE INTO flagged_messages (sms_id, sender, subject, preview, flagged_on)
        VALUES (?, ?, ?, ?, ?)
    """, (sms_id, sender, subject, preview, today))
    conn.commit()
    conn.close()

def flag_messages_bulk(emails: list):
    """
    Adds multiple spam emails to the tracking database in a single
    database operation instead of one connection per email.
    Each item in emails should have keys:
    email_id, sender, subject, body (used as preview).
    Already-flagged emails are silently skipped (INSERT OR IGNORE).
    """
    if not emails:
        return

    conn = get_connectio()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    rows = [
        (
            email["email_id"],
            email["sender"],
            email.get("subject", ""),
            email.get("body", ""),
            today
        )
        for email in emails
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO flagged_messages
        (sms_id, sender, subject, preview, flagged_on)
        VALUES (?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()

def get_messages_due_for_deletion():
    """
    Returns all messages that have been flagged for 5 or more days
    and that the user has not marked to keep.
    Date filtering is done in SQLite rather than Python — much more
    efficient since only matching rows are transferred to memory.
    """
    conn = get_connectio()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM flagged_messages
        WHERE keep = 0
        AND date(flagged_on) <= date('now', '-5 days')
    """)

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]

def get_all_flagged_messages():
    """
    Returns every flagged message that the user has NOT marked to keep,
    regardless of how many days old it is. This is what the UI uses
    to show the full pending review list, not just ones about to be deleted.
    Each result includes a calculated 'days_old' field so the UI can
    show a countdown without needing to do date math itself.
    """

    conn = get_connectio()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM flagged_messages
        WHERE keep = 0
        ORDER BY flagged_on ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    today = datetime.now().date()

    results = []
    for row in rows:
        flagged_date = datetime.strptime(row["flagged_on"], "%Y-%m-%d").date()
        days_old = (today - flagged_date).days

        message = dict(row)
        message["days_old"] = days_old
        results.append(message)

    return results

def get_all_known_ids() -> set:
    """
    Returns a set of all email IDs currently tracked in the database
    — both pending and kept. Used to skip already-seen emails during
    scanning so we don't re-check emails we've already processed.
    """
    conn = get_connectio()
    cursor = conn.cursor()

    cursor.execute("SELECT sms_id FROM flagged_messages")
    rows = cursor.fetchall()
    conn.close()

    return {row["sms_id"] for row in rows}

def mark_keep(sms_id):
    """
    Mark a message as keep - SpamReaper will never delete this message.
    The user triggers this from the rewiev screen in the app
    """

    conn = get_connectio()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE flagged_messages
        SET keep = 1
        WHERE sms_id = ?
    """, (sms_id,))
    
    conn.commit()
    conn.close()

def delete_record(sms_id):
    """
    Removes a message from the database. 
    We call this after we have deleted the message from the phone, 
    so we no longer need to track it.
    NOTE: This does not delete the message from the phone, it only removes it from our tracking database.
    The actual SMS deletion i handle by sms_deleter.py
    """

    conn = get_connectio()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM flagged_messages
        WHERE sms_id = ?
    """, (sms_id,))
    
    conn.commit()
    conn.close()

def delete_records_bulk(sms_ids):
    """
    Removes multiple message records from our tracking database at once.
    Used after a 'Clear' or 'Wipe Today' bulk action trashes several
    emails via Gmail, so we can clean up our local records in one pass
    instead of one database connection per email.
    """
    if not sms_ids:
        return

    conn = get_connectio()
    cursor = conn.cursor()

    # We build a placeholder string like "?,?,?" matching the number of IDs
    placeholders = ",".join("?" for _ in sms_ids)

    cursor.execute(f"""
        DELETE FROM flagged_messages
        WHERE sms_id IN ({placeholders})
    """, sms_ids)

    conn.commit()
    conn.close()

def log_action(sms_id, sender, subject, preview, action):
    """
    Records an action taken on a flagged email into the history table.
    action should be either 'deleted' or 'kept'.
    Called whenever an email is trashed or marked safe.
    """
    conn = get_connectio()
    cursor = conn.cursor()

    today = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""
        INSERT INTO action_history (sms_id, sender, subject, preview, action, actioned_on)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (sms_id, sender, subject, preview, action, today))

    conn.commit()
    conn.close()

def get_action_history():
    """
    Returns all history records ordered most recent first.
    Calculates days_until_permanent for deleted emails —
    Gmail keeps trashed items for 30 days before purging them.
    """
    conn = get_connectio()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM action_history
        ORDER BY actioned_on DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    today = datetime.now().date()
    results = []

    for row in rows:
        record = dict(row)
        actioned_date = datetime.strptime(record["actioned_on"], "%Y-%m-%d").date()
        days_since = (today - actioned_date).days

        if record["action"] == "deleted":
            record["days_until_permanent"] = max(0, 30 - days_since)
        else:
            # Kept emails are never auto-deleted — no countdown needed
            record["days_until_permanent"] = None

        results.append(record)

    return results

def delete_history_record(sms_id):
    """
    Removes a record from action_history after a restore or permanent delete action.
    """
    conn = get_connectio()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM action_history
        WHERE sms_id = ?
    """, (sms_id,))

    conn.commit()
    conn.close()
