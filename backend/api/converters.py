from email.errors import HeaderParseError
from email.header import decode_header, make_header
from email.utils import parseaddr

from api.schemas import SpamEmailResponse
from spam.retention import calculate_days_left


def _decode_header_text(text: str) -> str:
    try:
        return str(make_header(decode_header(text)))
    except (LookupError, UnicodeError, HeaderParseError):
        return text


def split_sender(raw_sender: str) -> tuple[str, str]:
    name, address = parseaddr(raw_sender)
    display_name = _decode_header_text(name) or address or raw_sender
    return display_name, address or raw_sender


def to_spam_email_response(message: dict, days_before_deletion: int) -> SpamEmailResponse:
    sender_name, sender_address = split_sender(message["sender"])
    return SpamEmailResponse(
        id=message["sms_id"],
        sender_name=sender_name,
        sender_address=sender_address,
        subject=_decode_header_text(message["subject"] or ""),
        preview=message["preview"] or "",
        days_left=calculate_days_left(message["days_old"], days_before_deletion),
    )