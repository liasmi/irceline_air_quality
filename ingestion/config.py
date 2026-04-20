"""Configuration settings for the IRCELINE air quality ingestion pipeline.

This module defines configuration classes and instances for API endpoints,
database connections, and pipeline parameters. Settings are loaded from
environment variables with sensible defaults.
"""

import os
import logging
from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import List

load_dotenv()

logger = logging.getLogger(__name__)


@dataclass
class APIConfig:
    """Configuration for IRCELINE API endpoints and settings.

    Attributes:
        base_url (str): Base URL for the IRCELINE SOS API
        stations_endpoint (str): Endpoint path for stations
        timeseries_endpoint (str): Endpoint path for timeseries
        timeout (int): Request timeout in seconds
        max_retries (int): Maximum number of retry attempts
    """
    base_url: str = "https://geo.irceline.be/sos/api/v1"
    stations_endpoint: str = "/stations"
    timeseries_endpoint: str = "/timeseries"
    timeout: int = 30
    max_retries: int = 3


@dataclass
class MySQLConfig:
    """Configuration for MySQL database connection.

    Attributes:
        host (str): Database host address
        port (int): Database port number
        database (str): Database name
        username (str): Database username
        password (str): Database password
    """
    host: str = os.getenv("MYSQL_HOST", "localhost")
    port: int = int(os.getenv("MYSQL_PORT", "3306"))
    database: str = os.getenv("MYSQL_DATABASE", "air_quality_db")
    username: str = os.getenv("MYSQL_USERNAME", "root")
    password: str = os.getenv("MYSQL_PASSWORD", "")


@dataclass
class PipelineConfig:
    """Configuration for the ingestion pipeline behavior.

    Attributes:
        target_phenomena_ids (List[str]): List of phenomenon IDs to process
        flanders_bbox (dict): Geographic bounding box for Flanders region
    """
    target_phenomena_ids: List[str] = field(default_factory=lambda: [
        "5",     # PM10
        "6001",  # PM2.5
        "8",     # NO2
        "71",    # CO2
        "1"      # SO2
    ])

    flanders_bbox = {
        "min_lat": 50.68,
        "max_lat": 51.51,
        "min_lon": 2.54,
        "max_lon": 5.92
    }

api_config = APIConfig()
mysql_config = MySQLConfig()
pipeline_config = PipelineConfig()

logger.info("Configuration loaded successfully")