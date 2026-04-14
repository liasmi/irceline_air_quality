"""
One-time discovery script to confirm phenomenon IDs from IRCELINE API.
Run this before anything else to validate the IDs in config.py

Usage: 
    cd air_quality_flanders
    python -m ingestion.utils.discover_phenomena
"""
from collections import defaultdict
from loguru import logger
from ingestion.api_client import IRCELINEClient
from ingestion.config import pipeline_config


def discover_phenomena():
    client = IRCELINEClient()

    logger.info("Fetching timeseries sample to discover phenomenon IDs...")
    all_ts = client.get_timeseries()
    logger.info(f"Total timeseries returned: {len(all_ts)}")

    # Collect all unique phenomena found
    # structure: { phenomenon_id: {"labels": set(), "count": int} }
    phenomena_found = defaultdict(lambda: {"labels": set(), "count": 0})

    for ts in all_ts:
        params = ts.get("parameters", {})
        phenomenon = params.get("phenomenon", {})
        p_id    = str(phenomenon.get("id", ""))
        p_label = phenomenon.get("label", "")

        if p_id:
            phenomena_found[p_id]["labels"].add(p_label)
            phenomena_found[p_id]["count"] += 1

    # Print all discovered phenomena
    print("\n" + "=" * 60)
    print("ALL PHENOMENA DISCOVERED")
    print("=" * 60)
    print(f"{'ID':<10} {'COUNT':<8} LABEL")
    print("-" * 60)
    for p_id, data in sorted(phenomena_found.items(), key=lambda x: x[1]["count"], reverse=True):
        labels = " | ".join(data["labels"])
        print(f"{p_id:<10} {data['count']:<8} {labels}")

    # Cross-check against our config
    print("\n" + "=" * 60)
    print("CROSS-CHECK WITH CONFIG")
    print("=" * 60)
    for name, configured_id in pipeline_config.target_phenomena.items():
        if configured_id in phenomena_found:
            labels = " | ".join(phenomena_found[configured_id]["labels"])
            count  = phenomena_found[configured_id]["count"]
            print(f"[OK] {name:<6} ID={configured_id:<6} count={count:<5} label={labels}")
        else:
            print(f"[!!] {name:<6} ID={configured_id:<6} NOT FOUND in API response")


if __name__ == "__main__":
    discover_phenomena()