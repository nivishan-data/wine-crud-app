from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("Connection to the database was successful!")
else:
    print("DATABASE_URL is not set.")
