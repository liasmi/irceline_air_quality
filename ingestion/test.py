from ingestion.stations import fetch_stations
from ingestion.timeseries_meta import fetch_timeseries
from ingestion.measurements import fetch_measurements
from ingestion.loaders.mysql_loader import load_to_mysql
from ingestion.api_client import IRCELINEClient


def run():

    print("Stations...")
    stations = fetch_stations()
    load_to_mysql(stations, "raw_stations")

    print("Timeseries...")
    # Pass station_ids to fetch only Flanders timeseries
    ts = fetch_timeseries(station_ids=stations["station_id"].tolist())
    load_to_mysql(ts, "raw_timeseries")

    print("Measurements...")
    measurements = fetch_measurements(ts["timeseries_id"].tolist(), phenomenon_ids=ts["phenomenon_id"].unique().tolist())
    print(f"   Fetched {len(measurements)} measurement records")
    print(f"   Shape: {measurements.shape}")
    if not measurements.empty:
        print(f"   Columns: {measurements.columns.tolist()}")
    load_to_mysql(measurements, "raw_measurements")

    print("DONE")

if __name__ == "__main__":
    # Uncomment to test April 2026 data
    # test_timeseries_data_april()
    
    run()