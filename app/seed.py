import os
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from .database import SessionLocal
from .models import Wine
from .models import Base, engine

def seed_data(csv_path: str):
    """
    Seed the database with wine data from a CSV file.
    
    Args:
        csv_path (str): Path to the CSV file containing wine data
    """
    try:
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)
        
        # Handle both absolute and relative paths
        if not os.path.isabs(csv_path):
            csv_path = os.path.join(os.path.dirname(__file__), '..', csv_path)
        
        print(f"Reading CSV file from: {csv_path}")
        df = pd.read_csv(csv_path)
        df.columns = [c.strip().replace(' ', '_') for c in df.columns]
        print("Columns in DataFrame:", df.columns.tolist())
        
        session = SessionLocal()
        try:
            # Check if data already exists
            existing_count = session.query(Wine).count()
            if existing_count > 0:
                print(f"Database already contains {existing_count} records. Skipping seeding.")
                return
            
            # Batch insert for better performance
            wines = []
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
                wines.append(wine)
            
            session.bulk_save_objects(wines)
            session.commit()
            print(f"Successfully seeded {len(wines)} wine records")
            
        except SQLAlchemyError as e:
            print(f"Database error occurred: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()
            
    except Exception as e:
        print(f"Error occurred during seeding: {str(e)}")
        raise

if __name__ == "__main__":
    seed_data("app/docs/winequality-red.csv")
