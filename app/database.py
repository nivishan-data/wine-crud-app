import os
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import time

# Handle Heroku database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Add retry logic for database connection
max_retries = 3
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        engine = create_engine(
            DATABASE_URL or "sqlite:///./wine.db",
            pool_pre_ping=True,  # Enable connection health checks
            pool_recycle=300,    # Recycle connections every 5 minutes
        )
        # Test the connection
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        break
    except OperationalError as e:
        if attempt == max_retries - 1:
            raise Exception(f"Failed to connect to database after {max_retries} attempts: {str(e)}")
        print(f"Database connection attempt {attempt + 1} failed, retrying in {retry_delay} seconds...")
        time.sleep(retry_delay)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Add event listener for connection errors
@event.listens_for(engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        return

    try:
        connection.scalar(("SELECT 1"))
    except Exception:
        connection.invalidate()
        raise
