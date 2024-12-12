import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Path to your service account key file
PROJECT_FOLDER = os.getenv("PROJECT_DIRECTORY")
SERVICE_ACCOUNT_FILE = f'{PROJECT_FOLDER}\monitor\src\email_service\credentials.json'

# Define the required scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def authenticate_gmail():
    """Authenticate using service account credentials and get Gmail API service."""
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    
    # If you need to impersonate another user (e.g., send emails from another user's Gmail account), use:
    # creds = creds.with_subject('user@example.com')
    
    return build('gmail', 'v1', credentials=creds)

# Example usage
service = authenticate_gmail()
# Now you can use the Gmail API service to send emails, etc.