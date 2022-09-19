from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from WeatherPredictorApi import schemas, database, models

from WeatherPredictorApi.data.supplyinfo import createAll

internal = APIRouter()

@internal.post('/create-city')
def create(db: Session = Depends(database.get_db), city: schemas.CityCreate = Body(...)):
    return createCity(db, city)

@internal.post('/initiate-json-cities')
def createJsonCities(db: Session = Depends(database.get_db)):
    createAll(db)
    return 'initiated'

@internal.delete('/delete-all-cities')
def createJsonCities(db: Session = Depends(database.get_db)):
    return deleteAllCities(db)

@internal.delete('/delete/{id}')
def deleteCity(id: int, db: Session = Depends(database.get_db)):
    return deleteCityById(db, id)






def createCity(db: Session, city: schemas.CityCreate):
    dbCity = models.City(name= city.name, latitude=city.lat, longitude= city.long)
    db.add(dbCity)
    db.commit()
    db.refresh(dbCity)
    return dbCity

def deleteCityById(db: Session, id: int):
    c = db.query(models.City).filter(models.City.id == id).delete()
    db.commit()
    return c

def deleteAllCities(db: Session):
    i = db.query(models.City).order_by(models.City.id.desc()).first()
    if i:
        last =  int(i.id)
        for o in range(last+1):
            deleteCityById(db, o)
        return 'cities eraised'
    else:
        return 'empty'