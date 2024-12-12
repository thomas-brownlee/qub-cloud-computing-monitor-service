import requests
import json
import os

GITLAB_URL = os.getenv('GITLAB_URL')
GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
PROJECT_ID = os.getenv('PROJECT_ID')


def create_gitlab_issue(title, description, labels=None):
    """Creates a new issue on GitLab."""

    url = f"{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/issues"

    headers = {
        "Authorization": f"Bearer {GITLAB_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "title": title,
        "description": description
    }

    if labels:
        data["labels"] = ",".join(labels)

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        issue_data = response.json()
        print(f"Issue created successfully! ID: {issue_data['iid']}, URL: {issue_data['web_url']}")
    except requests.exceptions.RequestException as e:
        print(f"Error creating issue: {e}")
        if response.content:
             print(f"Response content: {response.content}")
        return None

def generate_issue(service_name, host_address):
    issue_title = f"Service Down: {service_name}"
    issue_description = f"Service Down: {service_name}, Service host address on cluster is: {host_address}"
    issue_labels = ["api", "service down"]  # Example labels
    create_gitlab_issue(issue_title, issue_description, issue_labels)