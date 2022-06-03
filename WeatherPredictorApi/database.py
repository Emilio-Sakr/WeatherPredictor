from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .settings import Settings

Base = declarative_base()

settings = Settings()

engine = create_engine(settings.database_uri)

SessionLocal = sessionmaker(engine, autocommit=False, autoflush=True)

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

