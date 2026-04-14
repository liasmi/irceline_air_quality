import pandas as pd
from datetime import datetime, timedelta
from ingestion.api_client import IRCELINEClient

def build_timespan(days=30):
    end = datetime.utcnow()
    start = end - timedelta(days=days)
    # return f"{start.isoformat()}Z/{end.isoformat()}Z"
    return "2026-01-01T00:00:00Z/2026-01-02T00:00:00Z"


def fetch_measurements(timeseries_ids, phenomenon_ids=None):
    """Fetch measurements data for given timeseries.
    
    Args:
        timeseries_ids: List of timeseries IDs to fetch
        phenomenon_ids: Optional list of phenomenon IDs to filter via API params
    """
    client = IRCELINEClient()
    timespan = build_timespan()

    records = []

    for ts_id in timeseries_ids:
        # Get phenomenon_id for this timeseries if filtering is enabled
        if phenomenon_ids:
            # Pass phenomenon_ids one by one via API params
            for pid in phenomenon_ids:
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
        else:
            data = client.get_timeseries_data(ts_id, timespan)

            # API returns values as list of dicts: [{'timestamp': ms, 'value': float}, ...]
            values = data.get("values", [])

            for v in values:
                records.append({
                    "timeseries_id": ts_id,
                    "timestamp": v["timestamp"],
                    "value": v["value"]
                })

    return pd.DataFrame(records)