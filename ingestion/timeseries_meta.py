import pandas as pd
import time
import logging
from ingestion.api_client import IRCELINEClient
from ingestion.config import pipeline_config

logger = logging.getLogger(__name__)

def fetch_timeseries():
    """Fetch timeseries metadata.
    
    Args:
        station_ids: Optional list of station IDs to filter by (Flanders stations)
    """
    logger.info("Fetching timeseries metadata")
    client = IRCELINEClient()
    ts_list = client.get_timeseries()

    records = []

    for ts in ts_list:
        ts_id = ts["id"]
        logger.debug(f"Processing timeseries {ts_id}")

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

    df = pd.DataFrame(records)
    logger.info(f"Processed {len(records)} timeseries")
    return df