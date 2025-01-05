# app/main.py

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine
from .seed import seed_data  # Import the seed_data function

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wine Quality API",
    description="An API for managing the Wine Quality dataset, with a simple UI.",
    version="1.0.0"
)

# Mount static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure Jinja2 templates
templates = Jinja2Templates(directory="app/templates")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Renders a basic home page with a table of wines and a form to create new wines.
    """
    return templates.TemplateResponse("index.html", {"request": request})

seed_data("app/docs/winequality-red.csv")  # Seed the data from the CSV file

@app.get("/wines", response_model=list[schemas.Wine])
def read_wines(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    wines = crud.get_wines(db, skip=skip, limit=limit)
    return wines

@app.get("/wines/{wine_id}", response_model=schemas.Wine)
def read_wine(wine_id: int, db: Session = Depends(get_db)):
    db_wine = crud.get_wine(db, wine_id=wine_id)
    if not db_wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    return db_wine

@app.post("/wines", response_model=schemas.Wine)
def create_new_wine(wine: schemas.WineCreate, db: Session = Depends(get_db)):
    return crud.create_wine(db, wine)

@app.put("/wines/{wine_id}", response_model=schemas.Wine)
def update_existing_wine(wine_id: int, updates: schemas.WineUpdate, db: Session = Depends(get_db)):
    db_wine = crud.get_wine(db, wine_id=wine_id)
    if not db_wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    return crud.update_wine(db, db_wine, updates)

@app.delete("/wines/{wine_id}")
def delete_existing_wine(wine_id: int, db: Session = Depends(get_db)):
    db_wine = crud.get_wine(db, wine_id=wine_id)
    if not db_wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    crud.delete_wine(db, db_wine)
    return {"message": "Wine deleted successfully"}
