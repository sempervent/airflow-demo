from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta

# Define a function that we'll use with the PythonOperator
def format_url(ti):
    # The PythonOperator can be used to execute a Python function.
    # This function pulls the date from XCom, formats it into a URL, and pushes the URL to XCom.
    date = ti.xcom_pull(task_ids='get_date')
    return f'https://myservice.com/api/{date}.json'

# The on_failure_callback function will be called when a task fails.
def alert_on_failure(context):
    # Here you could put code to send an alert, e.g. send a message to a Slack channel.
    pass

# Define the DAG
with DAG('my_dag',
         start_date=datetime(2022, 1, 1),
         default_args={'retries': 3, 'retry_delay': timedelta(minutes=5), 'email_on_failure': True},
         description='A DAG that demonstrates several Airflow features') as dag:

    # The BashOperator executes a bash command. The get_date task gets the current date and time.
    get_date = BashOperator(task_id='get_date',
                            bash_command='date +%FT%H:%M:%S(%Z)',
                            do_xcom_push=True,  # Push the result to XCom.
                            on_failure_callback=alert_on_failure)  # Call alert_on_failure if this task fails.

    # The PythonOperator calls a Python function. The format_url task formats the date into a URL.
    format_url_op = PythonOperator(task_id='format_url',
                                   python_callable=format_url,
                                   provide_context=True)

    # The SimpleHttpOperator sends an HTTP request and can push the response to XCom.
    retrieve_data = SimpleHttpOperator(task_id='retrieve_data',
                                       method='GET',
                                       endpoint="{{ task_instance.xcom_pull('format_url') }}",
                                       response_check=lambda response: response.status_code == 200,
                                       xcom_push=True)

    # The PostgresOperator executes a SQL command in a Postgres database.
    store_data = PostgresOperator(task_id='store_data',
                                  sql="INSERT INTO my_table (data) VALUES ({{ task_instance.xcom_pull('retrieve_data') }})",
                                  postgres_conn_id='my_postgres_conn',
                                  autocommit=True)

    # Define the dependencies between the tasks. Each task will wait for its dependencies to finish successfully before starting.
    get_date >> format_url_op >> retrieve_data >> store_data
