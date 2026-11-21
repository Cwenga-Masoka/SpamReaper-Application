import sqlite3
from datetime import datetime
from storage.history_constants import GMAIL_TRASH_RETENTION_DAYS, HistoryAction

class ActionHistoryRepository:
    def __init__(self, db_name: str = "spamreaper.db"):
        """
        Manages database operations strictly for action history logs.
        This isolates history tracking from flagged spam management.
        """
        self.db_name = db_name

    def _get_connection(self):
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_db(self):
        """
        Creates the action_history table if it doesn't exist.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

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
        conn.close()

    def log_action(self, sms_id: str, sender: str, subject: str, preview: str, action: str):
        """
        Records an action taken on a flagged email into the history table.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT INTO action_history (sms_id, sender, subject, preview, action, actioned_on)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (sms_id, sender, subject, preview, action, today))

        conn.commit()
        conn.close()

    def get_action_history(self) -> list:
        """
        Returns all history records ordered most recent first,
        calculating days until permanent deletion in Gmail.
        """
        conn = self._get_connection()
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

            if record["action"] == HistoryAction.DELETED:
                record["days_until_permanent"] = max(0, GMAIL_TRASH_RETENTION_DAYS - days_since)
            else:
                record["days_until_permanent"] = None

            results.append(record)

        return results

    def delete_history_record(self, sms_id: str):
        """
        Removes a record from action_history.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM action_history
            WHERE sms_id = ?
        """, (sms_id,))

        conn.commit()
        conn.close()

    def clear_action_history(self):
        """
        Permanently removes every record from action_history.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM action_history")
        conn.commit()
        conn.close()

    def delete_history_records_bulk(self, sms_ids: list):
        """
        Removes multiple history records at once.
        """
        if not sms_ids:
            return
        conn = self._get_connection()
        cursor = conn.cursor()
        placeholders = ",".join("?" for _ in sms_ids)
        cursor.execute(f"""
            DELETE FROM action_history
            WHERE sms_id IN ({placeholders})
        """, sms_ids)
        conn.commit()
        conn.close()