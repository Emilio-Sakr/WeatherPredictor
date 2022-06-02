from psycopg2 import Timestamp
from sqlalchemy import Float, Column, String, Integer, DateTime
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer ,primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)