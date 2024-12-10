"""
Handles the email service

File mostly taken from gmails api documentations https://developers.google.com/gmail/api/quickstart/python
And chat-gpt added support on debugging the major coding issues

"""
# pylint: skip-file

import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_gmail():
    """Authenticate and get Gmail API service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            path_to_credentials = "C://Git_source/monitoring/monitor/email_service/credentials.json"
            flow = InstalledAppFlow.from_client_secrets_file(path_to_credentials, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

def create_email_message(sender, to, subject_local, message_text):
    """Create an email message."""
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject_local
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw}

def send_email(service_local, user_id, email_message_local):
    """Send an email using the Gmail API."""
    try:
        message = service_local.users().messages().send(userId=user_id, body=email_message_local).execute()
        print(f"Message sent! Message ID: {message['id']}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    # Authenticate and get Gmail API service
    service = authenticate_gmail()

    # Create and send an email
    sender_email = "qubeditoronservice@gmail.com"
    recipient_email = "thomasabrownlee@gmail.com"
    subject = "Test Email from Gmail API"
    body = "This is a test email sent from Python using the Gmail API."

    email_message = create_email_message(sender_email, recipient_email, subject, body)
    send_email(service, "me", email_message)
