import sqlite3

from storage.flagged_emails import FlaggedMessageRepository

DATABASE_NAME = "spamreaper.db"
SAMPLE_AGES_IN_DAYS = {"test-1": 0, "test-2": 3, "test-3": 4, "test-4": 5, "test-5": 7}

repository = FlaggedMessageRepository(DATABASE_NAME)
repository.initialize_db()

for sms_id in SAMPLE_AGES_IN_DAYS:
    repository.flag_message(
        sms_id,
        f"Sender {sms_id} <{sms_id}@example.com>",
        "Preview text",
        f"Subject for {sms_id}",
    )

connection = sqlite3.connect(DATABASE_NAME)
for sms_id, age_in_days in SAMPLE_AGES_IN_DAYS.items():
    connection.execute(
        "UPDATE flagged_messages SET flagged_on = date('now', 'localtime', ?) WHERE sms_id = ?",
        (f"-{age_in_days} days", sms_id),
    )
connection.commit()
connection.close()