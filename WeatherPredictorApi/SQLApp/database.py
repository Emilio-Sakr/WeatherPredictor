from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2

Base = declarative_base()

DATABASE_URI = "postgresql+psycopg2://postgres:instanceofHonor@localhost:5432/WeatherAppDB"

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(engine, autocommit=False, autoflush=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()