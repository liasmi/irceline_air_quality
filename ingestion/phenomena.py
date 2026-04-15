import requests
import pandas as pd

URL = "https://geo.irceline.be/sos/api/v1/phenomena"


def fetch_phenomena():
    data = requests.get(URL).json()

    records = []

    for p in data:
        records.append({
            "phenomenon_id": p.get("id"),
            "label": p.get("label")
        })

    return pd.DataFrame(records)

