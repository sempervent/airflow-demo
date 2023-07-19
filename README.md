# airflow-demo
An Airflow demo for writing DAGS

## Requirements
- Docker
- Docker Compose

## Getting Started
1. Clone this repository to your local machine:
```bash
git clone https://github.com/sempervent/airflow-demo.git
```
2. Navigate to the repository directory:
```bash
cd airflow-demo
```
3. Build and start the Docker Compose services:
```bash
docker-compose up -d
```
This will start a PostgreSQL database, an Airflow webserver, and an Airflow scheduler.
4. Access the Airflow web interface at http://localhost:8080.

## Setting Up Connections
The example DAG uses Airflow's SimpleHttpOperator and PostgresOperator, which require HTTP and Postgres connections respectively. You need to set up these connections in Airflow:

1. Open the Airflow web interface at http://localhost:8080.
2. Click on the Admin link in the top navigation bar.
3. Click on the Connections link in the drop-down menu.
4. Click on the Create button to create a new connection.

For the HTTP connection:

* Set the Conn Id to http_default.
* Set the Conn Type to HTTP.
* Set the Host to the URL of the HTTP service.

For the Postgres connection:

* Set the Conn Id to postgres_default.
* Set the Conn Type to Postgres.
* Set the Host, Schema, Login, and Password to match your Postgres database settings.

## Usage
The dags directory contains Python files that define Airflow DAGs. Each DAG represents a workflow of tasks. You can add your own DAG files to the dags directory.

The sample DAG in dags/my_dag.py includes examples of several Airflow features:

* BashOperator: Executes a bash command.
* PythonOperator: Calls a Python function.
* SimpleHttpOperator: Sends an HTTP request and pushes the response to XCom.
* PostgresOperator: Executes a SQL command in a PostgreSQL database.
* Error handling: The DAG includes a function that will be called if a task fails.
* Task dependencies: The tasks have dependencies that define the order in which they run.

To run the sample DAG:

1. Remove the entry for `dummy_dag.py` in the `dags/.airflowignore` folder.
2. Open the Airflow web interface at http://localhost:8080.
3. Click on the DAGs link in the top navigation bar.
4. Find the my_dag DAG in the list and click on its Play button to start a new run.

## Stopping the services
To stop the Docker Compose services, run:
```bash
docker-compose down
```


## Notes
This demo is intended for development and testing purposes only. It should not be used in a production environment.
The docker-compose.yaml file includes a Fernet key for encrypting and decrypting connection passwords. 
You should generate your own Fernet key and replace the existing one in the docker-compose.yaml file.