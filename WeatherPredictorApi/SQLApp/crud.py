from sqlalchemy.orm import Session

from . import database

from .schemas import *
from . import models

import bcrypt

def recreate_database():
    database.Base.metadata.drop_all(database.engine)
    database.Base.metadata.create_all(database.engine)

def getUserByEmail(db: Session, email: str):
    try: return db.query(models.user).filter(models.user.email == email).first()
    except: return False

def getUserById(db: Session, id : int):
    try: return db.query(models.user).filter(models.user.id == id).first()
    except: return False

def getAllUsers(db: Session, skip: int = 0, limit: int = 100):
    try: return db.query(models.user).offset(skip).limit(limit).all()
    except: return False
    
def createUser(db: Session, user: UserCreate):
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(user.password, salt)
        dbUser = models.user(email=user.email, password=hashed, username=user.username, salt=salt)
        db.add(dbUser)
        db.commit()
        db.refresh(dbUser)
        return dbUser
    except: return False


def getCity(db: Session, name : str):
    try: return db.query(models.city).filter(models.city.name == name).first()
    except: return False

def getAllCities(db: Session, skip: int = 0, limit: int = 1000):
    try: return db.query(models.city).offset(skip).limit(limit).all()
    except: return False

def deleteCityById(db: Session, id: int):
    try:
        city = db.query(models.city).filter(models.city.id == id).first()
        db.delete(city)
        db.commit()
        db.refresh(city)
    except: return False

def deleteAllCities(db: Session):
    try:
        i = db.query(models.city).order_by(models.city.id.desc()).first()
        for o in range(i):
            deleteCityById(db, i)
            i-=1
    except: return False

def createCity(db: Session, city: cityCreate):
    try:
        dbCity = models.city(name= city.name, latitude=city.latitude, longitude= city.longitude)
        db.add(dbCity)
        db.commit()
        db.refresh(dbCity)
        return dbCity
    except: return False
