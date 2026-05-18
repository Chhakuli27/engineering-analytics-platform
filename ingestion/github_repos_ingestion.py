import os
import requests
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "credentials/gcp-service-account.json"
)

# Read GitHub token
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# GitHub API headers
headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Spotify repositories API endpoint
url = "https://api.github.com/orgs/spotify/repos"

# Fetch data
response = requests.get(url, headers=headers)

# Convert response to JSON
repos = response.json()

# Extract important fields
repo_data = []

for repo in repos:
    repo_data.append({
        "repo_name": repo["name"],
        "description": repo["description"],
        "language": repo["language"],
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "created_at": repo["created_at"],
        "updated_at": repo["updated_at"]
    })

# Create DataFrame
df = pd.DataFrame(repo_data)

# Preview data
print(df.head())

# Initialize BigQuery client
client = bigquery.Client()

# BigQuery table ID
table_id = (
    "engineering-analytics-platform."
    "engineering_analytics.github_repositories"
)

# Load data into BigQuery
job = client.load_table_from_dataframe(df, table_id)

# Wait for completion
job.result()

print("Data successfully loaded into BigQuery!")