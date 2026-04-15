# IRCELINE Air Quality Pipeline

## Overview

This repository collects IRCELINE air quality data, loads it into MySQL, and provides analysis assets and a DBT project for modeling.

Key components:
- `ingestion/`: Python extraction and loading pipeline
- `ingestion/dags/`: Airflow DAG for orchestration
- `air_quality_project/`: DBT project for modeling and marts
- `analysis/deep_analysis.ipynb`: exploratory notebook for pollution analysis
- `.env`: local database and environment configuration

## Project structure

- `ingestion/`
  - `api_client.py`: IRCELINE API client
  - `config.py`: environment and pipeline configuration
  - `orchestration.py`: main ingestion flow
  - `loaders/mysql_loader.py`: load DataFrames into MySQL
  - `timeseries_meta.py`, `measurements.py`, `stations.py`, `phenomena.py`: extraction modules
  - `dags/ingestion_dag.py`: Airflow DAG definition
- `air_quality_project/`: DBT project files, models, and compiled DAG assets
- `analysis/`: notebook-based analysis and visualization
- `.env`: local application secrets and database settings

## Prerequisites

- Python 3.11 (recommended)
- Windows PowerShell or WSL for easier Airflow support
- MySQL server accessible from your machine
- Git if cloning the repository

## Setup

### 1. Create and activate a virtual environment

```powershell
cd "c:\Users\pc\Documents\Myprojects\irceline\irceline_air_quality"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

### 2. Install project dependencies

```powershell
python -m pip install -r requirements.txt
```

If you plan to use notebooks or VS Code notebook rendering, also install:

```powershell
python -m pip install --upgrade notebook nbformat ipykernel
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

Run the ingestion script directly from the repo root:

```powershell
python ingestion\orchestration.py
```

This currently executes the station ingestion flow and writes results to the configured MySQL database.

### What it loads

- `raw_stations`: pulled from `fetch_stations()`
- The rest of the pipeline (`phenomena`, `timeseries`, `measurements`) is present in code but currently commented out for incremental testing.

## Airflow orchestration

The repository includes an Airflow DAG at `ingestion/dags/ingestion_dag.py`.

### Install Airflow in the same venv

```powershell
python -m pip install "apache-airflow==2.8.1" --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-2.8.1/constraints-3.11.txt"
```

> On Windows, Airflow may be easier to run in WSL if you encounter package or scheduler issues.

### Configure Airflow

Set the Airflow home path and copy the DAG:

```powershell
$env:AIRFLOW_HOME = "c:\Users\pc\Documents\Myprojects\irceline\irceline_air_quality\airflow_home"
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

Run the webserver in one terminal and the scheduler in another:

```powershell
airflow webserver --port 8080
airflow scheduler
```

Then open:

```text
http://localhost:8080
```

### Trigger the DAG

Manual trigger:

```powershell
airflow dags trigger irceline_ingestion
```

Trigger with a custom timespan:

```powershell
airflow dags trigger -c "{\"timespan\":\"2026-04-14T00:00:00Z/2026-04-15T00:00:00Z\"}" irceline_ingestion
```

### DAG behavior

- Default schedule: `@daily`
- If no `timespan` is passed, it uses the current UTC date from midnight to midnight
- If `timespan` is provided in DAG config, it uses that value

## Analysis

Open the notebook for interactive analysis:

```powershell
code analysis\deep_analysis.ipynb
```

The `analysis/deep_analysis.ipynb` notebook connects to MySQL and visualizes the mart tables.

### Notebook environment

Make sure the venv is active and that `nbformat`, `notebook`, and `ipykernel` are installed.

## Optional: DBT project

The `air_quality_project/` folder contains a DBT project for model development and marts.

If you have DBT installed, run:

```powershell
dbt deps
cd air_quality_project
dbt run
```

## Troubleshooting

### Common issues

- `AirflowConfigException: Cannot use relative path`: set `AIRFLOW__CORE__SQL_ALCHEMY_CONN` to an absolute `sqlite:////...` URI
- `nbformat` rendering errors in notebooks: install `nbformat` and `notebook`
- `df.to_sql` MySQL errors: ensure `pymysql` and `SQLAlchemy` are installed and `.env` is configured correctly

### Environment notes

- Always run Python commands from the activated `.venv`
- Keep `.env` secrets local and never commit them

## Next steps

1. Validate MySQL connectivity
2. Run ingestion directly
3. Start Airflow and confirm DAG discovery
4. Use the notebook to validate mart data
5. Optionally expand the ingestion pipeline by enabling `phenomena`, `timeseries`, and `measurements`
