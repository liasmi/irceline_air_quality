import pandas as pd
from ingestion.api_client import IRCELINEClient
from ingestion.utils.is_in_flanders import is_in_flanders
from ingestion.config import pipeline_config

def fetch_stations():

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

    return pd.DataFrame(records)