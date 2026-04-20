"""Measurement data extraction module for IRCELINE air quality observations.

This module provides functionality to fetch and process air quality measurement
data from the IRCELINE API for specified timeseries and time ranges.
"""

import pandas as pd
import logging
from datetime import datetime, timedelta
from ingestion.api_client import IRCELINEClient

logger = logging.getLogger(__name__)


def build_timespan(days=30):
    """Build a timespan string for the last N days.

    Args:
        days (int): Number of days to go back from now

    Returns:
        str: Timespan string in ISO format
    """
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    # return f"{start.isoformat()}Z/{end.isoformat()}Z"
    return "2026-01-01T00:00:00Z/2026-01-02T00:00:00Z"


def fetch_measurements(timeseries_phenomena, timespan=None):
    """Fetch measurement data for given timeseries-phenomenon pairs.

    Retrieves air quality measurement observations for specified timeseries
    within the given time range. Each measurement includes timestamp and value.

    Args:
        timeseries_phenomena: Dict of {timeseries_id: phenomenon_id} to fetch
        timespan: The timespan for which to fetch data in ISO format.
                 Defaults to a fixed range if not provided.

    Returns:
        pd.DataFrame: DataFrame with columns:
            - timeseries_id: Timeseries identifier
            - phenomenon_id: Phenomenon identifier
            - timestamp: Measurement timestamp (milliseconds since epoch)
            - value: Measured air quality value
    """
    logger.info(f"Fetching measurements for {len(timeseries_phenomena)} timeseries with timespan {timespan}")
    client = IRCELINEClient()
    # timespan = build_timespan()

    records = []

    for ts_id, pid in timeseries_phenomena.items():
        logger.debug(f"Fetching data for timeseries {ts_id}")
        data = client.get_timeseries_data(ts_id, timespan, phenomenon_id=pid)

        # API returns values as list of dicts: [{'timestamp': ms, 'value': float}, ...]
        values = data.get("values", [])

        for v in values:
            records.append({
                "timeseries_id": ts_id,
                "phenomenon_id": pid,
                "timestamp": v["timestamp"],
                "value": v["value"]
            })

    df = pd.DataFrame(records)
    logger.info(f"Fetched {len(records)} measurement records")
    return df