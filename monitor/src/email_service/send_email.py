"""
Runs the send email after the elements are built

Credit module created using :
    * google gmail api docs https://developers.google.com/gmail/api/quickstart/python#
    * chat-gpt added support on debugging the major coding issue
"""

from google.auth.exceptions import RefreshError
from googleapiclient.errors import HttpError


def send_email(service_local, user_id, email_message_local):
    """Send an email using the Gmail API."""
    try:
        message = (
            service_local.users()
            .messages()
            .send(userId=user_id, body=email_message_local)
            .execute()
        )
        print(f"Message sent! Message ID: {message['id']}")
    except HttpError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except RefreshError as auth_err:
        print(f"Authentication error occurred: {auth_err}")
    except TimeoutError as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except ValueError as val_err:
        print(f"Value error occurred: {val_err}")
