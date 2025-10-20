import logging
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

logger = logging.getLogger(__name__)


def example_task():
    """Example Python task."""
    logger.info("Hello from Airflow!")
    return "Task completed successfully"


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "example_dag",
    default_args=default_args,
    description="A simple example DAG",
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=["example"],
) as dag:
    python_task = PythonOperator(
        task_id="python_task",
        python_callable=example_task,
    )

    bash_task = BashOperator(
        task_id="bash_task",
        bash_command='echo "Hello from Bash!"',
    )

    python_task >> bash_task
