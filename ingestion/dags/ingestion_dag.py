"""Airflow DAG definition for IRCELINE air quality data ingestion.

This module defines an Apache Airflow DAG that orchestrates the periodic
ingestion of air quality data from IRCELINE APIs into MySQL database.
"""

from datetime import datetime, timedelta
import logging

from airflow import DAG
from airflow.operators.python import PythonOperator

from ingestion.orchestration import run as run_ingestion_pipeline

logger = logging.getLogger(__name__)


def resolve_timespan(dag_run=None):
    """Resolve the timespan for data ingestion based on DAG run context.

    If a timespan is provided in the DAG run configuration, use it.
    Otherwise, default to the previous day's data.

    Args:
        dag_run: Airflow DAG run context object

    Returns:
        str: Timespan string in ISO format (start/end)
    """
    if dag_run and getattr(dag_run, "conf", None):
        timespan = dag_run.conf.get("timespan")
        if timespan:
            return timespan

    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return f"{start.isoformat()}Z/{end.isoformat()}Z"


def execute_ingestion(dag_run=None):
    """Execute the ingestion pipeline with resolved timespan.

    Args:
        dag_run: Airflow DAG run context object
    """
    timespan = resolve_timespan(dag_run=dag_run)
    logger.info(f"Executing ingestion with timespan: {timespan}")
    print(f"Using timespan: {timespan}")
    run_ingestion_pipeline(timespan=timespan)


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="irceline_ingestion",
    description="Ingest IRCELINE air quality data and load into MySQL.",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=default_args,
    tags=["ingestion", "irceline"],
) as dag:
    run_ingestion = PythonOperator(
        task_id="run_ingestion_orchestration",
        python_callable=execute_ingestion,
        provide_context=True,
    )
