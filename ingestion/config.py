import os
from dotenv import load_dotenv
from dataclasses import dataclass, field
from typing import List

load_dotenv()

@dataclass
class APIConfig:
    base_url: str = "https://geo.irceline.be/sos/api/v1"
    stations_endpoint: str = "/stations"
    timeseries_endpoint: str = "/timeseries"
    timeout: int = 30
    max_retries: int = 3


@dataclass
class MySQLConfig:
    host: str = os.getenv("MYSQL_HOST", "localhost")
    port: int = int(os.getenv("MYSQL_PORT", "3306"))
    database: str = os.getenv("MYSQL_DATABASE", "air_quality_db")
    username: str = os.getenv("MYSQL_USERNAME", "root")
    password: str = os.getenv("MYSQL_PASSWORD", "")


@dataclass
class PipelineConfig:
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