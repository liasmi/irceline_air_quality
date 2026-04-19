import requests
import pandas as pd
import logging

logger = logging.getLogger(__name__)

URL = "https://geo.irceline.be/sos/api/v1/phenomena"


def fetch_phenomena():
    logger.info("Fetching phenomena from API")
    data = requests.get(URL).json()

    records = []

    for p in data:
        records.append({
            "phenomenon_id": p.get("id"),
            "label": p.get("label")
        })

    df = pd.DataFrame(records)
    logger.info(f"Processed {len(records)} phenomena")
    return df

