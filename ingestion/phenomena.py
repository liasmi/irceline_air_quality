"""Phenomena data extraction module for IRCELINE air quality pollutants.

This module provides functionality to fetch and process pollutant/phenomenon
definitions from the IRCELINE API, including pollutant types and identifiers.
"""

import pandas as pd
import logging
from ingestion.api_client import IRCELINEClient

logger = logging.getLogger(__name__)


def fetch_phenomena():
    """Fetch and process pollutant phenomena data from IRCELINE API.

    Retrieves all available pollutant/phenomenon definitions with their
    identifiers and labels, then transforms into a clean pandas DataFrame.

    Returns:
        pd.DataFrame: DataFrame with columns:
            - phenomenon_id: Unique phenomenon identifier
            - label: Human-readable phenomenon name
    """
    logger.info("Fetching phenomena from API")
    client = IRCELINEClient()
    data = client.get_phenomena()

    records = []

    for p in data:
        records.append({
            "phenomenon_id": p.get("id"),
            "label": p.get("label")
        })

    df = pd.DataFrame(records)
    logger.info(f"Processed {len(records)} phenomena")
    return df

