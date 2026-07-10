# We import our token function instead of the old service-building function
from gmail_auth import get_access_token
from concurrent.futures import ThreadPoolExecutor
from spam_detector import is_spam, is_spam_quick
from tracker_db import get_all_known_ids
import requests
import base64

from typing import List, Dict

# The base URL for all Gmail API calls — we'll build on top of this
GMAIL_API_BASE = 'https://gmail.googleapis.com/gmail/v1/users/me'

def get_inbox_message_ids(access_token: str, max_results=50) -> List[str]:
    """
    Asks Gmail for a list of message IDs currently in the inbox.
    This is now a plain HTTP GET request instead of a library call.
    """

    # Every Gmail API call needs this header to prove who's asking
    headers = {'Authorization': f'Bearer {access_token}'}

    # params become the ?key=value parts of the URL
    # requests builds this for us automatically when we pass a dictionary
    params = {
        'labelIds': 'INBOX',
        'maxResults': max_results
    }

    response = requests.get(
        f'{GMAIL_API_BASE}/messages',
        headers=headers,
        params=params
    )

    # This raises an error automatically if Gmail responds with
    # anything other than a success status code (200)
    response.raise_for_status()

    data = response.json()

    # Same defensive .get() pattern as before — an empty inbox
    # might not include a 'messages' key at all
    messages = data.get('messages', [])

    return [msg['id'] for msg in messages]

def get_message_metadata(access_token: str, message_id: str) -> Dict:
    """
    Fetches only the sender and subject of an email — no body.
    Much faster than get_message_details() since it downloads
    a fraction of the data. Used for the first-pass spam check.
    """
    headers = {'Authorization': f'Bearer {access_token}'}

    params = {
        'format': 'metadata',
        'metadataHeaders': ['From', 'Subject']
    }

    response = requests.get(
        f'{GMAIL_API_BASE}/messages/{message_id}',
        headers=headers,
        params=params
    )
    response.raise_for_status()

    message = response.json()
    headers_list = message['payload']['headers']

    sender = ''
    subject = ''

    for header in headers_list:
        if header['name'] == 'From':
            sender = header['value']
        elif header['name'] == 'Subject':
            subject = header['value']

    return {
        'email_id': message_id,
        'sender': sender,
        'subject': subject,
        'body': ''  # body not fetched yet
    }


def get_message_details(access_token: str, message_id: str) -> Dict:
    """
    Fetches the full details of a single email by its ID.
    """

    headers = {'Authorization': f'Bearer {access_token}'}

    params = {'format': 'full'}

    response = requests.get(
        f'{GMAIL_API_BASE}/messages/{message_id}',
        headers=headers,
        params=params
    )

    response.raise_for_status()

    message = response.json()

    headers_list = message['payload']['headers']

    sender = ''
    subject = ''

    for header in headers_list:
        if header['name'] == 'From':
            sender = header['value']
        elif header['name'] == 'Subject':
            subject = header['value']

    body_text = extract_body_text(message['payload'])

    return {
        'email_id': message_id,
        'sender': sender,
        'subject': subject,
        'body': body_text
    }

def extract_body_text(payload: Dict) -> str:
    """
    Digs into Gmail's payload structure to find and decode the
    actual readable text of an email. No changes needed here —
    this works on the raw JSON structure regardless of how we fetched it.
    """

    if 'body' in payload and payload['body'].get('data'):
        return decode_base64(payload['body']['data'])

    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                if part['body'].get('data'):
                    return decode_base64(part['body']['data'])

        for part in payload['parts']:
            if part['body'].get('data'):
                return decode_base64(part['body']['data'])

    return ''


def decode_base64(data: str) -> str:
    """
    Gmail encodes email body content in a URL-safe base64 format.
    """
    decoded_bytes = base64.urlsafe_b64decode(data)
    return decoded_bytes.decode('utf-8', errors='ignore')

def clean_body_text(raw_text: str) -> str:
    """
    Strips HTML tags, collapses whitespace, and truncates the body
    to a readable preview length before storing in the database.
    """
    import re
    text = re.sub(r'<[^>]+>', ' ', raw_text)
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&#39;', "'").replace('&quot;', '"')
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) > 200:
        text = text[:200] + "..."
    return text

def get_spam_emails() -> List[Dict]:
    """
    Two-pass spam detection, now with concurrent fetching within each pass:
    Pass 1 — fetch metadata (sender + subject) for all new inbox emails,
             several requests at a time instead of one-by-one.
    Pass 2 — for emails not flagged yet, fetch full body concurrently too.
    """
    access_token = get_access_token()
    message_ids = get_inbox_message_ids(access_token)

    known_ids = get_all_known_ids()
    message_ids = [mid for mid in message_ids if mid not in known_ids]

    if not message_ids:
        print("All inbox emails already scanned — nothing new to check.")
        return []

    # Pass 1 — metadata only, fetched concurrently (10 at a time is a safe
    # default — enough to speed things up without hammering Gmail's API)
    with ThreadPoolExecutor(max_workers=10) as executor:
        metas = list(executor.map(
            lambda mid: get_message_metadata(access_token, mid),
            message_ids
        ))

    spam_emails = []
    needs_body_check = []

    for meta in metas:
        if is_spam_quick(meta['sender'], meta['subject']):
            spam_emails.append(meta)
        else:
            needs_body_check.append(meta)

    # Pass 2 — full body fetch, also concurrent, only for unconfirmed emails
    if needs_body_check:
        with ThreadPoolExecutor(max_workers=10) as executor:
            details_list = list(executor.map(
                lambda m: get_message_details(access_token, m['email_id']),
                needs_body_check
            ))

        for details in details_list:
            if is_spam(details['sender'], details['body'], details['subject']):
                details['body'] = clean_body_text(details['body'])
                spam_emails.append(details)

    # For pass-1 confirmed spam, we still need bodies for the preview text —
    # fetch those concurrently too instead of one at a time
    needs_preview = [
        (i, meta) for i, meta in enumerate(spam_emails) if not meta['body']
    ]
    if needs_preview:
        with ThreadPoolExecutor(max_workers=10) as executor:
            fetched = list(executor.map(
                lambda item: get_message_details(access_token, item[1]['email_id']),
                needs_preview
            ))

        for (i, meta), details in zip(needs_preview, fetched):
            spam_emails[i]['body'] = clean_body_text(details['body'])
            spam_emails[i]['subject'] = details['subject']
            spam_emails[i]['sender'] = details['sender']

    return spam_emails