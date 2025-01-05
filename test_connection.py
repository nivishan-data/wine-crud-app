import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    try:
        connection = psycopg2.connect(DATABASE_URL)
        print("Connection to the database was successful!")
    except Exception as e:
        print(f"Error connecting to the database: {e}")
else:
    print("DATABASE_URL is not set.")
