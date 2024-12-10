"""
Creates the basic format of the email
"""

import base64
from email.mime.text import MIMEText


def create_email_message(sender, to, subject_local, message_text):
    """Create an email message."""
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject_local
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}
