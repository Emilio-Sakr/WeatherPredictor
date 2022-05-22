from sqlalchemy import Column, Float, Integer, String

from .database import Base

class user(Base):
    __tablename__='users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    salt = Column(String)

class city(Base):
    __tablename__='cities'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    def __init__(self, name, latitude, longitude):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

    def __city__(self):
        return {'id':self.id, self.name:[self.latitude, self.longitude]}



