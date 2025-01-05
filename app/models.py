# app/models.py

from sqlalchemy import Column, Integer, Float
from .database import engine, SessionLocal
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Wine(Base):
    __tablename__ = 'wines'
    
    id = Column(Integer, primary_key=True, index=True)
    fixed_acidity = Column(Float)
    volatile_acidity = Column(Float)
    citric_acid = Column(Float)
    residual_sugar = Column(Float)
    chlorides = Column(Float)
    free_sulfur_dioxide = Column(Float)
    total_sulfur_dioxide = Column(Float)
    density = Column(Float)
    pH = Column(Float)
    sulphates = Column(Float)
    alcohol = Column(Float)
    quality = Column(Integer)

# Create the table
Base.metadata.create_all(bind=engine)
