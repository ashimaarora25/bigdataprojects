Source Amazon Books data, install Airflow and PGAdmin on a Docker container, use Aitflow to schedule Extract, Transform, and Load (ETL) of Amazon Books data into a Postgres SQL database. 

a. Activate virtual env:  python3 -m venv venv
                          source venv/bin
b. Deploy Airflow on Docker Compose: https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
    b1. curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.5/docker-compose.yaml'
    b2. mkdir -p ./dags ./logs ./plugins ./config
        echo -e "AIRFLOW_UID=$(id -u)" > .env
    b3. AIRFLOW_UID=50000
c. Initialize database: docker compose up airflow-init
If docker doesn't exist: brew install docker

d. Check localhost:8080
e. Get pg-admin to run Postgres on Docker container - add details for pg-admin in the yml file, check localhost:5050
f. When registering server in Postgres, do docker ls and get the associated ID, and then docker inspect <ID>
g. Add amazonbooks database
h. Go to Airflow, add connection to new database we created. 



1. Install Airlow on Docker
2. Install Postgres and PgAdmin on DockerPgAdmin on Docker
3. Create a DAG

