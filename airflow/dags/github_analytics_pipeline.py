from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "owner": "apoorva",
    "start_date": datetime(2026, 1, 1),
}

with DAG(
    dag_id="github_analytics_pipeline",
    default_args=default_args,
    schedule="@daily",
    catchup=False,
) as dag:

    ingestion_task = BashOperator(
        task_id="github_ingestion",
        bash_command="""
        cd /Users/chakuli/Projects/engineering-analytics-platform &&
        source venv/bin/activate &&
        python ingestion/github_repos_ingestion.py
        """
    )

    dbt_run_task = BashOperator(
        task_id="dbt_run",
        bash_command="""
        cd /Users/chakuli/Projects/engineering-analytics-platform/dbt_project/engineering_analytics_dbt &&
        source ../../venv/bin/activate &&
        dbt run
        """
    )

    dbt_test_task = BashOperator(
        task_id="dbt_test",
        bash_command="""
        cd /Users/chakuli/Projects/engineering-analytics-platform/dbt_project/engineering_analytics_dbt &&
        source ../../venv/bin/activate &&
        dbt test
        """
    )

    ingestion_task >> dbt_run_task >> dbt_test_task