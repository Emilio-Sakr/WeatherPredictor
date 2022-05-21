from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URI = "postgresql://postgres:instanceofHonor@localhost:5432/WeatherAppDB"

engine = create_engine(DATABASE_URI)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()