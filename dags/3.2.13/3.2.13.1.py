from airflow import DAG
from datetime import timedelta
from airflow.utils.dates import days_ago
from airflow.operators.dummy import DummyOperator

# Создадим объект класса DAG с указанием start_date
dag = DAG(
    '3.2.13.1',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1)
)

# Создадим несколько шагов
t1 = DummyOperator(task_id='echo_1', dag=dag)
t2 = DummyOperator(task_id='echo_2', dag=dag)