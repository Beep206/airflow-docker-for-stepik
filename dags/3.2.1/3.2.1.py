import pandas as pd
import sqlite3
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

def extract_data(url, tmp_file, **context):
    pd.read_csv(url).to_csv(tmp_file)

def transform_data(group, agreg, tmp_file, tmp_agg_file, **context):
    data = pd.read_csv(tmp_file)
    data.groupby(group).agg(agreg).reset_index().to_csv(tmp_agg_file)

def load_data(tmp_file, table_name, db_path, **context):
    conn = sqlite3.connect(db_path)
    data = pd.read_csv(tmp_file)
    data["insert_time"] = pd.to_datetime("now")
    data.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
}

with DAG(
    dag_id='3.2.1',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    extract_data_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={
            'url': 'https://raw.githubusercontent.com/dm-novikov/stepik_airflow_course/main/data/data.csv',
            'tmp_file': '/tmp/file.csv'
        },
    )

    transform_data_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_kwargs={
            'tmp_file': '/tmp/file.csv',
            'tmp_agg_file': '/tmp/file_agg.csv',
            'group': ['A', 'B', 'C'],
            'agreg': {"D": sum}
        },
    )

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        op_kwargs={
            'tmp_file': '/tmp/file_agg.csv',
            'table_name': 'example_table',
            'db_path': '/opt/airflow/dags/3.2.1/example.db',
        },
    )

    extract_data_task >> transform_data_task >> load_data_task
