from sqlalchemy.orm import Session

from . import database

from .schemas import *
from . import models

import bcrypt

def recreate_database():
    database.Base.metadata.drop_all(database.engine)
    database.Base.metadata.create_all(database.engine)

def getUserByEmail(db: Session, email= str):
    return db.query(models.user).filter(models.user.email == email).first()

def getUserById(db: Session, id = int):
    return db.query(models.user).filter(models.user.id == id).first()

def getAllUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user).offset(skip).limit(limit).all()
    
def createUser(db: Session, user: UserCreate):
    if getUserByEmail(db, user):
        return 'Email already registered'
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(user.password, salt)
    dbUser = models.user(email=user.email, password=hashed, username=user.username, salt=salt)
    db.add(dbUser)
    db.commit()
    db.refresh(dbUser)
    return dbUser


def getCity(db: Session, name = str):
    return db.query(models.city).filter(models.city.name == name).first()

def getAllCities(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.city).offset(skip).limit(limit).all()

def deleteCity(db: Session, name = str):
    db.query(models.city).filter(models.city.name == name).delete()

def createCity(db: Session, city = cityCreate):
    if getCity(db, city.name):
        return 'city already registered'
    dbCity = models.city(name= city.name, latitude=city.latitude, longitude= city.longitude)
    db.add(dbCity)
    db.commit()
    db.refresh(dbCity)
    return dbCity
