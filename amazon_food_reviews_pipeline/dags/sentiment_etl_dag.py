"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

import os

"""

import pandas as pd
import random
import kagglehub
from kagglehub import KaggleDatasetAdapter


# Set the path to the file you'd like to load
reviews_file_path = "Reviews.csv"
temp_daily_path = '../data/daily_sample.csv'

# Load the latest version
df = kagglehub.dataset_load(
  KaggleDatasetAdapter.PANDAS,
  "snap/amazon-fine-food-reviews",
  reviews_file_path,
  # Provide any additional arguments like 
  # sql_query or pandas_kwargs. See the 
  # documenation for more information:
  # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)

def extract_daily_sample(df):
    df_sample = df.sample(n=500, random_state=random.randint(1, 1000))
    df_sample.to_csv(temp_daily_path, index=False)
    print(df_sample.head())

#print("First 5 records:\n", df.head())

extract_daily_sample(df)

