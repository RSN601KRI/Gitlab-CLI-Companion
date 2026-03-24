import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
GITLAB_URL = os.getenv("GITLAB_URL")

headers = {
    "PRIVATE-TOKEN": GITLAB_TOKEN
}

def get_projects():
    url = f"{GITLAB_URL}/projects"
    return requests.get(url, headers=headers).json()

def get_merge_requests(project_id):
    url = f"{GITLAB_URL}/projects/{project_id}/merge_requests"
    return requests.get(url, headers=headers).json()

def post_mr_comment(project_id, mr_iid, message):
    url = f"{GITLAB_URL}/projects/{project_id}/merge_requests/{mr_iid}/notes"
    return requests.post(url, headers=headers, json={"body": message}).json()