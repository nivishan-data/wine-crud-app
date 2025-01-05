# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def get_wines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Wine).offset(skip).limit(limit).all()

def get_wine(db: Session, wine_id: int):
    return db.query(models.Wine).filter(models.Wine.id == wine_id).first()

def create_wine(db: Session, wine: schemas.WineCreate):
    db_wine = models.Wine(**wine.dict())
    db.add(db_wine)
    db.commit()
    db.refresh(db_wine)
    return db_wine

def update_wine(db: Session, db_wine: models.Wine, updates: schemas.WineUpdate):
    for field, value in updates.dict(exclude_unset=True).items():
        setattr(db_wine, field, value)
    db.commit()
    db.refresh(db_wine)
    return db_wine

def delete_wine(db: Session, db_wine: models.Wine):
    db.delete(db_wine)
    db.commit()
    return db_wine
