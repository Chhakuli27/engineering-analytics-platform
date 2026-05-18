from google.cloud import bigquery
import os

# Set path to service account key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "credentials/gcp-service-account.json"
)

# Initialize BigQuery client
client = bigquery.Client()

# Test query
query = """
SELECT 'BigQuery connection successful!' AS message
"""

query_job = client.query(query)

for row in query_job:
    print(row["message"])