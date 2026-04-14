from google.cloud import bigquery
from ingestion.config import bq_config

client = bigquery.Client.from_service_account_json(
    bq_config.credentials_path
)

def load_to_bq(df, table_name):

    # Check if dataframe is empty
    if df.empty:
        print(f"⚠️  Skipping {table_name}: DataFrame is empty")
        return

    table_id = f"{bq_config.project_id}.{bq_config.dataset_raw}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        write_disposition="WRITE_TRUNCATE"  # Replace table if it exists
    )
    
    try:
        job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()
        print(f"✅ Loaded {len(df)} rows into {table_id}")
    except Exception as e:
        print(f"❌ Error loading {table_name}: {e}")
        print(f"   DataFrame shape: {df.shape}")
        print(f"   DataFrame columns: {df.columns.tolist()}")
        raise