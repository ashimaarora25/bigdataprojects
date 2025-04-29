Amazon Books Data Pipeline with Airflow + Docker + Postgres

This project builds an end-to-end data pipeline that:

    1. Fetches Amazon Data Engineering books via web scraping (Extract)
    2. Stores the cleaned data into a PostgreSQL database (Transform + Load)
    3. Runs Apache Airflow DAGs to automate the flow 
    4. The entire project setup runs inside Docker containers for easy setup

Tech Stack Used: 

    Apache Airflow (workflow orchestration)
    PostgreSQL (data storage)
    Docker & Docker Compose (containerization)
    Python (scraping with requests, BeautifulSoup, pandas)



Setup Instructions: 

1. Clone the repository: 
    https://github.com/ashimaarora25/bigdataprojects.git
    cd amazonbooksdata

2. Start Docker Containers:
    docker-compose up airflow-init
    docker-compose up

3. Access Airflow UI:
    Navigate to http://localhost:8080 and login with:
    Username: airflow
    Password: airflow

4. Trigger the DAG
    Turn on and manually trigger the fetch_and_store_amazon_books DAG from the Airflow UI.

5. Check your Postgres DB
    Connect to your Postgres database at http://localhost:5050, and check the books table under amazon_books database.


Other details: 

Creating and activating Virtual Env:  

   python3 -m venv venv
   source venv/bin

Deploying  Airflow on Docker Compose: 

https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

Acknowledgements:

This project was inspired by the below video by Sunjana in Data
 https://www.youtube.com/watch?v=3xyoM28B40Y
