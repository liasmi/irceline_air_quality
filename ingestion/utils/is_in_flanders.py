
"""Geographic utility functions for Flanders region validation.

This module provides functions to determine if geographic coordinates
fall within the Flanders region boundaries for air quality monitoring.
"""

import logging

logger = logging.getLogger(__name__)


def is_in_flanders(lat, lon):
    """Check if coordinates are within Flanders region boundaries.

    Flanders region boundaries (approximate):
    - Latitude: 50.68° to 51.51° N
    - Longitude: 2.54° to 5.92° E

    Args:
        lat (float): Latitude coordinate
        lon (float): Longitude coordinate

    Returns:
        bool: True if coordinates are within Flanders, False otherwise
    """
    flanders_bounds = {
        "min_lat": 50.68,
        "max_lat": 51.51,
        "min_lon": 2.54,
        "max_lon": 5.92
    }

    return (flanders_bounds["min_lat"] <= lat <= flanders_bounds["max_lat"] and
            flanders_bounds["min_lon"] <= lon <= flanders_bounds["max_lon"])


def is_in_flanders_bbox(lon, lat, bbox):
    """Check if coordinates are within a specified bounding box.

    Args:
        lon (float): Longitude coordinate
        lat (float): Latitude coordinate
        bbox (dict): Bounding box with min_lon, max_lon, min_lat, max_lat keys

    Returns:
        bool: True if coordinates are within the bounding box, False otherwise
    """
    return (
        bbox["min_lon"] <= lon <= bbox["max_lon"] and
        bbox["min_lat"] <= lat <= bbox["max_lat"]
    )