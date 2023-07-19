from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

def _print_date(date, **context):
    print("The date is: ", date)

def _get_date(ti, **context):
    date = ti.xcom_pull(task_ids='get_date_in_iso')
    Variable.set("iso_date", date)

args = {
    'owner': 'airflow',
    'start_date': days_ago(2),
}

with DAG(
    'date_dag',
    default_args=args,
    description='A simple date DAG',
    schedule_interval=None,
) as dag:

    get_date = BashOperator(
        task_id='get_date_in_iso',
        bash_command='date -u +"%Y-%m-%dT%H:%M:%SZ"',
        xcom_push=True,
    )

    save_date = PythonOperator(
        task_id='save_date',
        python_callable=_get_date,
        provide_context=True,
    )

    print_date = PythonOperator(
        task_id='print_date',
        python_callable=_print_date,
        op_kwargs={'date': Variable.get("iso_date")},
    )

    get_date >> save_date >> print_date
