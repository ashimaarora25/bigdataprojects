#tasks: 1) fetch amazon data (extract), 2) clean data (transform) 3) create and store data in a table (load)
#operators: Python and Postgres Operator
#hooks -  allow connection from Airflow to external dbs.
#dependencies:

from airflow import DAG
from datetime import datetime, timedelta
import time, random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


headers = {
    "Referer": 'https://www.amazon.com/',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/117.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
}
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 25),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'fetch_and_store_amazon_books',
    default_args=default_args,
    description='A simple DAG to fetch books data from Amazon and store it in Postgres',
    schedule_interval=timedelta(days=1),

)

def get_amazon_data_books(num_books, ti):
    # Base URL of the Amazon search results for data science books
    base_url = "https://www.amazon.com/s?k=data+engineering+books"

    books = []
    seen_titles = set()  # To keep track of seen titles

    page = 1

    while len(books) < num_books:
        url = f"{base_url}&page={page}"
        
        # Send a request to the URL
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the request with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Find book containers 
            book_containers = soup.find_all("div", {"class": "s-result-item", "data-component-type": "s-search-result"})
            
            # Loop through the book containers and extract data
            for book in book_containers:
                title = book.find("span", {"class": "a-text-normal"})
                author = book.find("a", {"class": "a-link-normal"}) 
                price = book.find("span", {"class": "a-price-whole"})
                rating = book.find("span", {"class": "a-icon-alt"})
                
                book_title = title.get_text(strip=True) if title else "N/A"
                book_author = author.get_text(strip=True) if author else "N/A"
                book_price = price.get_text(strip=True) if price else "N/A"
                book_rating = rating.get_text(strip=True) if rating else "N/A"
                    
                # Check if title has been seen before
                if book_title!="N/A" and book_title not in seen_titles:
                        seen_titles.add(book_title)
                        books.append({
                            "Title": book_title,
                            "Author": book_author,
                            "Price": book_price,
                            "Rating": book_rating,
                        })
                                    # Increment the page number for the next iteration
            page += 1
            # Random short sleep to avoid being detected as a bot
            time.sleep(random.uniform(1, 3))
        else:
            print("Failed to retrieve the page")
            break

    # Limit to the requested number of books
        
    books = books[:num_books]
    
    # Convert the list of dictionaries into a DataFrame
    df = pd.DataFrame(books)
    print(df)
        
    # Remove duplicates based on 'Title' column
    df.drop_duplicates(subset="Title", inplace=True)
    
    # Push the DataFrame to XCom
    ti.xcom_push(key='book_data', value=df.to_dict('records'))


    #3) create and store data in table on postgres (load)
    
def insert_book_data_into_postgres(ti):
    #Pull the books data
    book_data = ti.xcom_pull(key='book_data', task_ids='fetch_book_data')
    if not book_data:
        raise ValueError("No book data found")

    insert_books = SQLExecuteQueryOperator(
    task_id='insert_books',
    conn_id='books_connection',
    sql="""
        INSERT INTO books (title, authors, price, rating)
        VALUES (%s, %s, %s, %s)
    """,
    parameters=[
        (book['Title'], book['Author'], book['Price'], book['Rating'])
        for book in book_data
    ],
    )

#tasks
fetch_book_data_task = PythonOperator(
    task_id='fetch_book_data',
    python_callable=get_amazon_data_books,
    op_args=[50], #num books to fetch
    dag=dag,

)
create_table_task = SQLExecuteQueryOperator(
    task_id='create_table',
    conn_id='books_connection',
    sql="""
    CREATE TABLE IF NOT EXISTS books (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        authors TEXT,
        price TEXT,
        rating TEXT
    );
    """,
    dag=dag,
)

insert_book_data_task = PythonOperator(
    task_id='insert_book_data',
    python_callable=insert_book_data_into_postgres,
    dag=dag,
)

#dependencies

fetch_book_data_task >> create_table_task >> insert_book_data_task
                