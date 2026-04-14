import requests
import pandas as pd
from ingestion.loader import load_to_bq

URL = "https://geo.irceline.be/sos/api/v1/phenomena"


def fetch_phenomena():
    data = requests.get(URL).json()

    records = []

    for p in data:
        records.append({
            "phenomenon_id": p.get("id"),
            "label": p.get("label"),
            "uom": p.get("uom"),
        })

    return pd.DataFrame(records)


if __name__ == "__main__":
    df = fetch_phenomena()
    load_to_bq(df, "phenomena")