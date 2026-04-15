from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from ingestion.orchestration import run as run_ingestion_pipeline


def resolve_timespan(dag_run=None):
    if dag_run and getattr(dag_run, "conf", None):
        timespan = dag_run.conf.get("timespan")
        if timespan:
            return timespan

    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return f"{start.isoformat()}Z/{end.isoformat()}Z"


def execute_ingestion(dag_run=None):
    timespan = resolve_timespan(dag_run=dag_run)
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
