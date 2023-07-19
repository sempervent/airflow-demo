echo -e "AIRFLOW_UID=$(id -u)" > .env || echo "AIRFLOW_UID=50000" > .env
