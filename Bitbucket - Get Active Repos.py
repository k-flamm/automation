import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timezone
import csv

# Authentication
BITBUCKET_USERNAME = 'bitbucket_username'
BITBUCKET_APP_PASSWORD = 'app_password'

# List of all projects
PROJECTS = []

# The date we want to compare to (beginning of the audit period)
ACTIVE_SINCE_DATE = ""
# Reformatting the above data to match the date format from the Bitbucket API response
active_since_date = datetime.strptime(ACTIVE_SINCE_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc)

# Method that gets all ACTIVE repositories in a project (active = last modified on or after above ACTIVE_SINCE_DATE)
def get_repositories_per_project(project, active_since_date):
    all_active_repos = []

    url = f"https://api.bitbucket.org/2.0/repositories/WORKSPACE?q=project.key=\"{project}\""
    while url:
        response = requests.get(url, auth=HTTPBasicAuth(BITBUCKET_USERNAME, BITBUCKET_APP_PASSWORD))
        repos = response.json()

        for repo in repos ['values']:
            full_name = repo['full_name']
            last_updated_on = datetime.strptime(repo['updated_on'], '%Y-%m-%dT%H:%M:%S.%f%z')

            if last_updated_on >= active_since_date:
                all_active_repos.append({
                    'full_name': full_name,
                    'updated_on': last_updated_on
                })
        url = repos.get('next')

    # Sorts my repo name
    all_active_repos = sorted(all_active_repos, key=lambda x: x['full_name'])
    return all_active_repos

# Loops through each project, gets the active repos, and exports the information for each project into a separate CSV
for project in PROJECTS: 
    active_repos = get_repositories_per_project(project, active_since_date)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_csv = f'{project}_{timestamp}_active_repositories.csv'

    # Write the results to the CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Repository', 'Last Modified'])

        for repo in active_repos:
            writer.writerow([repo['full_name'], repo['updated_on']])

    active_repos = get_repositories_per_project(project, active_since_date)
