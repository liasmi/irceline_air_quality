import requests
from tenacity import retry, stop_after_attempt, wait_exponential
from ingestion.config import api_config

class IRCELINEClient:

    def __init__(self):
        self.base_url = api_config.base_url
        self.session = requests.Session()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def _get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_stations(self):
        return self._get("/stations")

    def get_timeseries(self):
        return self._get("/timeseries")

    def get_timeseries_metadata(self, ts_id):
        return self._get(f"/timeseries/{ts_id}")

    def get_timeseries_data(self, ts_id, timespan, phenomenon_id=None):
        params = {"timespan": timespan}
        if phenomenon_id:
            params["phenomenon"] = phenomenon_id
        return self._get(f"/timeseries/{ts_id}/getData", params)