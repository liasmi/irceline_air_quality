import pandas as pd
import logging
from datetime import datetime, timedelta
from ingestion.api_client import IRCELINEClient

logger = logging.getLogger(__name__)

def build_timespan(days=30):
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    # return f"{start.isoformat()}Z/{end.isoformat()}Z"
    return "2026-01-01T00:00:00Z/2026-01-02T00:00:00Z"


def fetch_measurements(timeseries_phenomena,timespan=None):
    """Fetch measurements data for given timeseries-phenomenon pairs.
    
    Args:
        timeseries_phenomena: Dict of {timeseries_id: phenomenon_id} to fetch
        timespan: The timespan for which to fetch data
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