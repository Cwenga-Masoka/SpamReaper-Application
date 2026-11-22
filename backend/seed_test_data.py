import sqlite3
from contextlib import closing
from datetime import datetime, timedelta
from typing import Final, NamedTuple

from storage.flagged_emails import FlaggedMessageRepository

DATE_FORMAT: Final = "%Y-%m-%d"
SEED_ID_PREFIX: Final = "seed-"

DELETE_SEEDS_SQL: Final = "DELETE FROM flagged_messages WHERE sms_id LIKE ?"
INSERT_SEED_SQL: Final = """
    INSERT INTO flagged_messages (sms_id, sender, subject, preview, flagged_on)
    VALUES (?, ?, ?, ?, ?)
"""


class SeedEmail(NamedTuple):
    sms_id: str
    sender: str
    subject: str
    preview: str
    age_in_days: int


SEED_EMAILS: Final = (
    SeedEmail(
        f"{SEED_ID_PREFIX}1",
        "Apex Crypto Signals <newsletter@apex-signals.io>",
        "Instant 500x Whale Alert: Act within 2 hours!",
        "Join our VIP Telegram channel to reap maximum yield.",
        4,
    ),
    SeedEmail(
        f"{SEED_ID_PREFIX}2",
        "CloudHosting Billing <support@billing-renewal.net>",
        "Urgent: Your VPS server #9021 will be terminated",
        "Immediate payment required. Update your credentials now.",
        3,
    ),
    SeedEmail(
        f"{SEED_ID_PREFIX}3",
        "MegaRetail Deals <promotions@daily-fashion.com>",
        "Final clearance! Up to 80% off linen shirts",
        "Shop our warehouse sale before inventory runs out.",
        2,
    ),
    SeedEmail(
        f"{SEED_ID_PREFIX}4",
        "Prize Center <winner@lucky-draw-now.org>",
        "You have been selected for a free gift card",
        "Claim your reward today by confirming your details.",
        1,
    ),
    SeedEmail(
        f"{SEED_ID_PREFIX}5",
        "Quick Loans <offers@fast-cash-today.biz>",
        "Pre-approved: borrow up to R50,000 in minutes",
        "No credit check needed. Apply in two clicks.",
        0,
    ),
)


def calculate_flagged_date(age_in_days: int) -> str:
    return (datetime.now() - timedelta(days=age_in_days)).strftime(DATE_FORMAT)


def to_row(email: SeedEmail) -> tuple:
    return (
        email.sms_id,
        email.sender,
        email.subject,
        email.preview,
        calculate_flagged_date(email.age_in_days),
    )


def seed_flagged_emails() -> None:
    repository = FlaggedMessageRepository()
    repository.initialize_db()

    with closing(sqlite3.connect(repository.db_name)) as connection:
        connection.execute(DELETE_SEEDS_SQL, (f"{SEED_ID_PREFIX}%",))
        connection.executemany(INSERT_SEED_SQL, [to_row(email) for email in SEED_EMAILS])
        connection.commit()

    print(f"Seeded {len(SEED_EMAILS)} test emails.")


if __name__ == "__main__":
    seed_flagged_emails()