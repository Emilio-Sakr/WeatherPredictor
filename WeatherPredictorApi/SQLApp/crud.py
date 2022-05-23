from sqlalchemy.orm import Session

from . import database

from .schemas import *
from . import models

import bcrypt

def recreate_database():
    database.Base.metadata.drop_all(database.engine)
    database.Base.metadata.create_all(database.engine)

def getUserByEmail(db: Session, email: str):
    return db.query(models.user).filter(models.user.email == email).first()


def getUserById(db: Session, id : int):
    return db.query(models.user).filter(models.user.id == id).first()


def getAllUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user).offset(skip).limit(limit).all()

    
def createUser(db: Session, user: UserCreate):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(user.password, salt)
    dbUser = models.user(email=user.email, password=hashed, username=user.username, salt=salt)
    db.add(dbUser)
    return dbUser


def getCity(db: Session, name : str):
    return db.query(models.city).filter(models.city.name == name).first()

def getAllCities(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.city).offset(skip).limit(limit).all()

def deleteCityById(db: Session, id: int):
    return db.query(models.city).filter(models.city.id == id).delete()

def deleteAllCities(db: Session):
    i = db.query(models.city).order_by(models.city.id.desc()).first()
    if i:
        last =  int(i.id)
        for o in range(last+1):
            deleteCityById(db, o)
        return 'cities eraised'
    else:
        return 'empty'

def createCity(db: Session, city: cityCreate):
    dbCity = models.city(name= city.name, latitude=city.latitude, longitude= city.longitude)
    db.add(dbCity)
    return dbCity
