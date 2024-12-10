"""
Holds the authentication for the email api

Credit module created using :
    * google gmail api docs https://developers.google.com/gmail/api/quickstart/python#
    * chat-gpt added support on debugging the major coding issue
"""

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
project_folder = os.getenv("PYTHONPATH")


def authenticate_gmail():
    """Authenticate and get Gmail API service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_bread_crumb = (
                f"{project_folder}/monitor/email_service/credentials.json"
            )
            flow = InstalledAppFlow.from_client_secrets_file(creds_bread_crumb, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run.
        with open("token.json", "w", encoding="utf-8", errors="ignore") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)
