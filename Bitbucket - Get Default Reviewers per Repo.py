import requests
from requests.auth import HTTPBasicAuth
import json

# Add your Bitbucket credentials
BITBUCKET_USERNAME = 'BITBUCKET USERNAME'
BITBUCKET_APP_PASSWORD = 'APP PASSWORD'

WORKSPACE = 'WORKSPACE'
REPO_SLUGS = [
  'repo1',
  'repo2'
]

# Function to get default reviewers
def get_default_reviewers(repo_slug):
    url = f"https://api.bitbucket.org/2.0/repositories/{WORKSPACE}/{repo_slug}/default-reviewers"
    response = requests.get(url, auth=HTTPBasicAuth(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
    response.raise_for_status()  # Raise an error for bad status codes
    return response.json()

# Function to save data as JSON
def save_as_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Loop through each repository and save default reviewers
for repo in REPO_SLUGS:
    try:
        reviewers = get_default_reviewers(repo)
        save_as_json(reviewers, f"{repo}_default_reviewers.json")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching default reviewers for {repo}: {e}")
