# IRCELINE Air Quality Pipeline

## Overview

This repository collects IRCELINE air quality data, loads it into MySQL, and provides a DBT project for modeling and business consumption.

The project includes:
- `ingestion/`: Python extraction and MySQL loading pipeline
- `ingestion/dags/`: Airflow DAG for orchestration
- `air_quality_project/`: DBT project with staging, dimensional marts, and consumption tables
- `analysis/`: notebook-based analysis and generated charts
- `airflow_home/`: Airflow runtime environment and logs
- `logs/`: pipeline logs

## IRCELINE APIs

The ingestion pipeline calls the IRCELINE Sensor Observation Service (SOS) API at `https://geo.irceline.be/sos/api/v1`.

Main endpoints used:
- `/stations` for station metadata
- `/phenomena` for pollutant and phenomenon definitions
- `/timeseries` for timeseries metadata
- `/timeseries/{timeseries_id}` for single timeseries metadata
- `/timeseries/{timeseries_id}/getData` for timeseries observations
  - query parameters: `timespan`, and optional `phenomenon`

API documentation:
- https://geo.irceline.be/sos/static/doc/api-doc/index.html

## What was analyzed

The notebook `analysis/deep_analysis.ipynb` was used to explore air quality data and generate chart artifacts for:
- station coverage and monitoring distribution
- polluted city ranking in Flanders
- hourly pollution profiles for Antwerpen and Steenokkerzeel
- city pollution profiles for Antwerpen, Steenokkerzeel, and Vilvoorde

### Generated charts and reports

- `analysis/monitoring_stations_distribution.html`
- `analysis/polluted_cities_flanders.html`
- `analysis/polluted_cities_flanders_bar2.html`
- `analysis/Antwerpen_hourly_pollution_2026-01-01.html`
- `analysis/Steenokkerzeel_hourly_pollution_2026-01-01.html`
- `analysis/Air_Quality_Profile_Antwerpen.html`
- `analysis/Air_Quality_Profile_Steenokkerzeel.html`
- `analysis/Air_Quality_Profile_Vilvoorde.html`
- `analysis/newplot.png`

## Dimensional model

The DBT project builds a dimensional model with the following tables:

### Dimensions

- `dim_pollutant`
  - `phenomenon_id`
  - `phenomenon_name`
  - `pollutant_type`

- `dim_station`
  - `station_id`
  - `station_name`
  - `city_name`
  - `latitude`
  - `longitude`

- `dim_time`
  - `timestamp`
  - `measured_at_timestamp`
  - `measured_at_date`
  - `hour`

### Fact

- `fact_air_quality`
  - `measurement_id`
  - `timestamp`
  - `station_id`
  - `phenomenon_id`
  - `measurement_value`

`fact_air_quality` is built by joining staged measurements with station metadata and pollutant definitions.

## Consumption tables

The DBT consumption layer provides business-focused outputs:

- `consumption_city_avg`
  - average pollution by city and pollutant type
  - station-level averages and variance from city average

- `consumption_city_hourly_pollution`
  - hourly average pollution for each city, pollutant, date, and hour

- `consumption_city_station_coverage`
  - station coverage and monitoring availability by city and pollutant

- `consumption_top10_polluting_cities`
  - top 10 most polluted cities by average pollutant value

- `consumption_city_nbr_station`
  - pollution ranking combined with station counts

## Project structure

- `ingestion/`
  - `api_client.py`: IRCELINE API client
  - `config.py`: environment configuration and pipeline settings
  - `orchestration.py`: main ingestion flow
  - `loaders/mysql_loader.py`: utility for loading data into MySQL
  - `stations.py`, `phenomena.py`, `timeseries_meta.py`, `measurements.py`: extractors for source data
  - `dags/ingestion_dag.py`: Airflow DAG definition

- `air_quality_project/`
  - `dbt_project.yml`: DBT project configuration
  - `profiles.yml`: DBT connection profiles
  - `models/`
    - `010_sources/`: source definitions for raw tables
    - `020_staging/`: staging models for cleaned IRCELINE source data
    - `030_intermediate/`: intermediate models
    - `040_marts/`: dimension and fact models
    - `050_consumption/`: business consumption models

- `analysis/`
  - `deep_analysis.ipynb`: exploratory notebook
  - generated HTML reports and chart image files

- `airflow_home/`
  - Airflow runtime folder and scheduler logs

- `logs/`
  - pipeline and execution logs

## Prerequisites

- Python 3.11 (recommended)
- MySQL server accessible from your machine
- Git if cloning the repository

## Logging

The ingestion pipeline uses Python's built-in logging module for monitoring and debugging.

- Logs are configured at INFO level by default in `orchestration.py`
- Change to DEBUG for more detailed output: `logging.basicConfig(level=logging.DEBUG, ...)`
- Logs include timestamps, module names, levels, and messages

## Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

### 2. Install project dependencies

```powershell
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create or update `.env` at the repository root with your database connection values:

```dotenv
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=air_quality_db
MYSQL_USERNAME=
MYSQL_PASSWORD=
MARTHOUSE_DATABASE=air_quality_db_mart
```

> Keep `.env` local and do not commit secrets.

## Running the ingestion pipeline

### Direct execution

```powershell
python ingestion\orchestration.py
```

This executes the ingestion flow and writes results into the configured MySQL database.

## Airflow orchestration

The repository includes an Airflow DAG at `ingestion/dags/ingestion_dag.py`.

### Install Airflow in the same venv

```powershell
python -m pip install "apache-airflow==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.11.txt"
```

### Configure Airflow

```powershell
$env:AIRFLOW_HOME = "\airflow_home"
md $env:AIRFLOW_HOME\dags
copy .\ingestion\dags\ingestion_dag.py $env:AIRFLOW_HOME\dags\
```

If you use SQLite for Airflow metadata, make sure the connection is absolute in `airflow.cfg` or via environment variable:

```powershell
$env:AIRFLOW__CORE__SQL_ALCHEMY_CONN = "sqlite:////c:/Users/pc/Documents/Myprojects/irceline/irceline_air_quality/airflow_home/airflow.db"
```

### Initialize Airflow

```powershell
airflow db init
airflow users create --username admin --firstname Admin --lastname User --role Admin --email admin@example.com
```

### Start Airflow

```powershell
airflow webserver --port 8080
airflow scheduler
```

Then open:

```text
http://localhost:8080
```

### Trigger the DAG

```powershell
airflow dags trigger irceline_ingestion
```

Manual trigger with a custom timespan:

```powershell
airflow dags trigger -c "{\"timespan\":\"2026-04-14T00:00:00Z/2026-04-15T00:00:00Z\"}" irceline_ingestion
```

## DBT project

From `air_quality_project/`:

```powershell
cd air_quality_project
dbt deps
dbt run
```

## Analysis

Open the notebook for interactive analysis:

```powershell
code analysis\deep_analysis.ipynb
```

## Troubleshooting

- Use activated `.venv` for Python commands
- Keep `.env` secrets local
- Ensure MySQL is reachable and credentials are valid

## Next steps

1. Validate MySQL connectivity
2. Run ingestion directly
3. Confirm Airflow DAG discovery
4. Use the notebook to validate mart and consumption outputs
5. Expand ingestion to cover all source tables
