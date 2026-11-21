import sqlite3
from datetime import datetime

class FlaggedMessageRepository:
    def __init__(self, db_name: str = "spamreaper.db"):
        """
        Manages database operations strictly for flagged spam messages.
        """
        self.db_name = db_name

    def _get_connection(self):
        conn = sqlite3.connect(self.db_name, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_db(self):
        """
        Creates the flagged_messages table if it doesn't exist.
        """
        conn = self._get_connection()
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
        conn.commit()

        try:
            cursor.execute("ALTER TABLE flagged_messages ADD COLUMN subject TEXT")
            conn.commit()
        except Exception:
            pass

        conn.close()

    def flag_message(self, sms_id, sender, preview, subject=""):
        conn = self._get_connection()
        cursor = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")

        cursor.execute("""
            INSERT OR IGNORE INTO flagged_messages (sms_id, sender, subject, preview, flagged_on)
            VALUES (?, ?, ?, ?, ?)
        """, (sms_id, sender, subject, preview, today))
        conn.commit()
        conn.close()

    def flag_messages_bulk(self, emails: list):
        if not emails:
            return

        conn = self._get_connection()
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

    def get_all_flagged_messages(self):
        conn = self._get_connection()
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

    def get_all_known_ids(self) -> set:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT sms_id FROM flagged_messages")
        rows = cursor.fetchall()
        conn.close()

        return {row["sms_id"] for row in rows}

    def get_flagged_message(self, sms_id):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM flagged_messages
            WHERE sms_id = ?
        """, (sms_id,))

        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    def mark_keep(self, sms_id):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE flagged_messages
            SET keep = 1
            WHERE sms_id = ?
        """, (sms_id,))
        
        conn.commit()
        conn.close()

    def delete_record(self, sms_id):
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM flagged_messages
            WHERE sms_id = ?
        """, (sms_id,))
        
        conn.commit()
        conn.close()

    def delete_records_bulk(self, sms_ids):
        if not sms_ids:
            return

        conn = self._get_connection()
        cursor = conn.cursor()
        placeholders = ",".join("?" for _ in sms_ids)

        cursor.execute(f"""
            DELETE FROM flagged_messages
            WHERE sms_id IN ({placeholders})
        """, sms_ids)

        conn.commit()
        conn.close()