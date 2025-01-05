import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Handle Heroku database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL or "sqlite:///./wine.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
