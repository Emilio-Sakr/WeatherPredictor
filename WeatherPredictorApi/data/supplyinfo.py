from fastapi import Depends
from WeatherPredictorApi.SQLApp.database import get_db
from WeatherPredictorApi.SQLApp.crud import createCity
from WeatherPredictorApi.SQLApp.schemas import cityCreate
from sqlalchemy.orm import Session
import json

base_path = './WeatherPredictorApi/data'

def createAll(db: Session):
    try:
        with open(f'{base_path}/cities.json') as f:
            data = json.load(f)
            for i, j in data.items():
                print(i)
                print(j)
                city = cityCreate(name = i, latitude = j[0], longitude = j[1])
                createCity(db, city)
    except Exception as e:
        print(e)