import os
import pandas as pd
from dotenv import load_dotenv
from ingestion.api_client import IrcelineClient
from ingestion.loaders.bigquery_loader import BQLoader
from ingestion.config import (
    PROJECT_ID, 
    STATIONS_TABLE, 
    TIMESERIES_TABLE, 
    API_BASE_URL
)

def clean_dataframe(df):
    """
    Cleans the dataframe to ensure BigQuery compatibility.
    Flattens nested objects and ensures correct string formatting.
    """
    # Convert dictionaries/lists to strings to prevent BQ Schema errors
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            df[col] = df[col].astype(str)
    return df

def run_ingestion():
    # 1. Setup
    print("--- Starting Ingestion Process ---")
    load_dotenv()
    
    client = IrcelineClient(API_BASE_URL)
    loader = BQLoader(PROJECT_ID)

    # 2. Process Stations
    try:
        print(f"Fetching stations from {API_BASE_URL}...")
        stations_raw = client.get_stations()
        stations_df = pd.json_normalize(stations_raw)
        
        # Filter for relevant columns to keep the raw table manageable
        stations_df = clean_dataframe(stations_df)
        
        print(f"Loading stations to {STATIONS_TABLE}...")
        loader.load_dataframe(stations_df, STATIONS_TABLE)
    except Exception as e:
        print(f"Error processing stations: {e}")

    # 3. Process Timeseries
    try:
        print(f"Fetching timeseries data...")
        # We fetch expanded timeseries to get the 'lastValue' directly
        ts_raw = client.get_timeseries()
        ts_df = pd.json_normalize(ts_raw)
        
        # Map internal IDs to the requested parameters for easier dbt modeling
        # Filter logic can be added here or in dbt (dbt is preferred for ELT)
        ts_df = clean_dataframe(ts_df)
        
        print(f"Loading timeseries to {TIMESERIES_TABLE}...")
        loader.load_dataframe(ts_df, TIMESERIES_TABLE)
    except Exception as e:
        print(f"Error processing timeseries: {e}")

    print("--- Ingestion Complete ---")

if __name__ == "__main__":
    run_ingestion()