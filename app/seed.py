# app/seed.py

import pandas as pd
from .database import SessionLocal
from .models import Wine
from .models import Base, engine

def seed_data(csv_path: str):
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    df = pd.read_csv(csv_path)  # Use default comma delimiter
    df.columns = [c.strip().replace(' ', '_') for c in df.columns]
    df.columns = df.columns.str.replace(' ', '_')  # Ensure spaces are replaced
    print("Columns in DataFrame:", df.columns.tolist())  # Print column names for debugging
    
    session = SessionLocal()

    for _, row in df.iterrows():
        wine = Wine(
            fixed_acidity=row['fixed_acidity'],
            volatile_acidity=row['volatile_acidity'],
            citric_acid=row['citric_acid'],
            residual_sugar=row['residual_sugar'],
            chlorides=row['chlorides'],
            free_sulfur_dioxide=row['free_sulfur_dioxide'],
            total_sulfur_dioxide=row['total_sulfur_dioxide'],
            density=row['density'],
            pH=row['pH'],
            sulphates=row['sulphates'],
            alcohol=row['alcohol'],
            quality=int(row['quality'])
        )
        print(f"Adding wine: {wine}")  # Print the wine object being added
        session.add(wine)
        print("Committing session...")  # Indicate that the session is being committed
    session.commit()
    session.close()

if __name__ == "__main__":
    seed_data("app/docs/winequality-red.csv")
