#tasks: 1) fetch amazon data (extract), 2) clean data (transform) 3) create and store data in a table (load)
#operators: Python and Postgres Operator
#hooks -  allow connection from Airflow to external dbs.
#dependencies:

from airflow import DAG
from datetime import datetime, timedelta

