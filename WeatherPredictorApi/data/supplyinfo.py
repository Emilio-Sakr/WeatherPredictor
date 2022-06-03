from fastapi import Depends
from WeatherPredictorApi import schemas, models
from sqlalchemy.orm import Session
import json

base_path = './WeatherPredictorApi/data'

def createAll(db: Session):
    try:
        with open(f'{base_path}/cities.json') as f:
            data = json.load(f)
            for i, j in data.items():
                city = schemas.CityCreate(name = i, lat = float(j[0]), long = float(j[1]))
                createCity(db, city)
    except Exception as e:
        print(f'error {e}')

def createCity(db: Session, city: schemas.CityCreate):
    dbCity = models.City(name= city.name, latitude=city.lat, longitude= city.long)
    db.add(dbCity)
    db.commit()
    db.refresh(dbCity)
    return dbCity