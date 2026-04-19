import pandas as pd
import logging
from ingestion.api_client import IRCELINEClient
from ingestion.config import pipeline_config

logger = logging.getLogger(__name__)

def fetch_stations():

    logger.info("Fetching stations from API")
    client = IRCELINEClient()
    stations = client.get_stations()

    records = []

    for s in stations:
        coords = s["geometry"]["coordinates"]
        lon, lat = coords[0], coords[1]

        records.append({
            "station_id": s["properties"]["id"],
            "station_label": s["properties"]["label"],
            "longitude": lon,
            "latitude": lat
        })

    df = pd.DataFrame(records)
    logger.info(f"Processed {len(records)} stations")
    return df