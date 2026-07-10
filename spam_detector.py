# We import 're', which stands for 'regular expressions'
# It lest us search for patterns in text, which is useful for finding specific words or phrases
import re

from config_manager import get_setting

def contains_spam_keywords(message_text: str) -> bool:
    """
    Checks if the given text contains any spam keywords.
    Keywords are read from config fresh on every call so that
    changes made in Settings take effect immediately without
    requiring an app restart.
    """
    keywords = get_setting("spam_keywords") or []
    message_lower = message_text.lower()

    for keyword in keywords:
        if re.search(keyword, message_lower, re.IGNORECASE):
            return True

    return False

def is_suspicious_sender(sender: str) -> bool:
    """
    This function checks if the sender's phone number is suspicious.
    It returns True if the number is likely to be a spam sender, otherwise it returns False.
    """
    # re.fullmatch() chacks if the entire sender string matches this pattern
    # \d means "any digit (0-9)"
    # {4, 6} means "between 4 and 6 of them"
    # So this matches senders like "1234", "567890", "123456", etc., which are common formats for spam senders
    if re.fullmatch(r"\d{4,6}", sender.strip()):

        # If the sender is a short numeric code, we consider it suspicious
        return True
    
    # If the sender looks lika a normal number or saved contact name, we consider it not suspicious
    return False

def is_spam(sender, message_text, subject=""):
    """
    This is the main spam check function
    Takes as sender and the message text and returns True if the message is likely to be spam, otherwise returns False
    This is the only function that other files need to import and use.
    """
    if contains_spam_keywords(subject):
        return True
    
    if contains_spam_keywords(message_text):
        return True
    
    # If the content looked clean, we then check if the sender looked sus
    # A sus sender is enough to flag the message
    if is_suspicious_sender(sender):
        return True
    
    # If both checks passed, we consider the message safe
    return False

def is_spam_quick(sender: str, subject: str) -> bool:
    """
    Fast first-pass check using only sender and subject.
    No body needed — used during metadata-only scan pass.
    """
    if contains_spam_keywords(subject):
        return True
    if is_suspicious_sender(sender):
        return True
    return False