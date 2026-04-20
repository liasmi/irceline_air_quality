"""IRCELINE API Client for air quality data retrieval.

This module provides a client class for interacting with the IRCELINE Sensor
Observation Service (SOS) API to fetch air quality data including stations,
phenomena, timeseries metadata, and measurement data.
"""

import requests
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from ingestion.config import api_config

logger = logging.getLogger(__name__)


class IRCELINEClient:
    """Client for IRCELINE Sensor Observation Service API.

    Provides methods to fetch various types of air quality data from the
    IRCELINE SOS API with automatic retry logic and logging.

    Attributes:
        base_url (str): Base URL for the IRCELINE API
        session (requests.Session): HTTP session for making requests
    """

    def __init__(self):
        """Initialize the IRCELINE API client.

        Sets up the base URL and HTTP session for API requests.
        """
        self.base_url = api_config.base_url
        self.session = requests.Session()
        logger.info("Initializing IRCELINEClient")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential())
    def _get(self, endpoint, params=None):
        """Make a GET request to the API with retry logic.

        Args:
            endpoint (str): API endpoint path (without base URL)
            params (dict, optional): Query parameters for the request

        Returns:
            dict: JSON response from the API

        Raises:
            requests.HTTPError: If the API returns an error status
        """
        url = f"{self.base_url}{endpoint}"
        logger.debug(f"Making GET request to {url}")
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_stations(self):
        """Fetch all monitoring station metadata.

        Returns:
            list: List of station objects with geometry and properties
        """
        logger.info("Fetching stations")
        return self._get("/stations")

    def get_phenomena(self):
        """Fetch all pollutant/phenomenon definitions.

        Returns:
            list: List of phenomenon objects with IDs and labels
        """
        logger.info("Fetching phenomena")
        return self._get("/phenomena")

    def get_timeseries(self):
        """Fetch all timeseries metadata.

        Returns:
            list: List of timeseries objects with IDs and basic info
        """
        logger.info("Fetching timeseries")
        return self._get("/timeseries")

    def get_timeseries_metadata(self, ts_id):
        """Fetch detailed metadata for a specific timeseries.

        Args:
            ts_id (str): Timeseries identifier

        Returns:
            dict: Detailed timeseries metadata including station and phenomenon info
        """
        logger.info(f"Fetching metadata for timeseries {ts_id}")
        return self._get(f"/timeseries/{ts_id}")

    def get_timeseries_data(self, ts_id, timespan, phenomenon_id=None):
        """Fetch measurement data for a specific timeseries and time range.

        Args:
            ts_id (str): Timeseries identifier
            timespan (str): Time range in ISO format (e.g., "2026-01-01T00:00:00Z/2026-01-02T00:00:00Z")
            phenomenon_id (str, optional): Specific phenomenon ID to filter by

        Returns:
            dict: Timeseries data with values array containing timestamp-value pairs
        """
        logger.info(f"Fetching data for timeseries {ts_id} with timespan {timespan}")
        params = {"timespan": timespan}
        if phenomenon_id:
            params["phenomenon"] = phenomenon_id
        return self._get(f"/timeseries/{ts_id}/getData", params)