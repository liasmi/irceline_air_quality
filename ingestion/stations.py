"""Station data extraction module for IRCELINE air quality monitoring stations.

This module provides functionality to fetch and process monitoring station
metadata from the IRCELINE API, including station locations and identifiers.
"""

import pandas as pd
import logging
from ingestion.api_client import IRCELINEClient
from ingestion.config import pipeline_config

logger = logging.getLogger(__name__)


def fetch_stations():
    """Fetch and process monitoring station data from IRCELINE API.

    Retrieves all available monitoring stations with their geographic coordinates
    and metadata, then transforms the data into a clean pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame with columns:
            - station_id: Unique station identifier
            - station_label: Human-readable station name
            - longitude: Station longitude coordinate
            - latitude: Station latitude coordinate
    """
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