import pandas as pd
import time
from ingestion.api_client import IRCELINEClient
from ingestion.config import pipeline_config

def fetch_timeseries():
    """Fetch timeseries metadata.
    
    Args:
        station_ids: Optional list of station IDs to filter by (Flanders stations)
    """
    client = IRCELINEClient()
    ts_list = client.get_timeseries()

    records = []

    for ts in ts_list:
        ts_id = ts["id"]

        detail = client.get_timeseries_metadata(ts_id)

        phenomenon = detail["parameters"]["phenomenon"]
        phenomenon_id = phenomenon["id"]


        station = detail["station"]["properties"]
        station_id = station["id"]
        

        records.append({
            "timeseries_id": ts_id,
            "station_id": station_id,
            "phenomenon_id": phenomenon_id,
            "pollutant": phenomenon["label"],
            "uom": detail["uom"]
        })

        time.sleep(0.2)

    return pd.DataFrame(records)