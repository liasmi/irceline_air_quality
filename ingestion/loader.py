from google.cloud import bigquery
import os
from dotenv import load_dotenv

load_dotenv()

client = bigquery.Client()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET = os.getenv("DATASET_RAW")


def load_to_bq(df, table_name):
    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"

    job = client.load_table_from_dataframe(df, table_id)
    job.result()

    print(f"Loaded {len(df)} rows → {table_id}")