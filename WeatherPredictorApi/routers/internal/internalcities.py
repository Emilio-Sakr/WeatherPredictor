from fastapi import APIRouter, Body, Depends
from WeatherPredictorApi.SQLApp.crud import createCity, deleteAllCities
from WeatherPredictorApi.SQLApp.schemas import cityCreate
from WeatherPredictorApi.SQLApp.database import get_db
from sqlalchemy.orm import Session
from WeatherPredictorApi.data.supplyinfo import createAll

Cities = APIRouter()

@Cities.post('/create-city')
def createCity(db: Session = Depends(get_db), city: cityCreate = Body(...)):
    return createCity(db, city)

@Cities.post('/initiate-json-cities')
def createJsonCities(db: Session = Depends(get_db)):
    try:
        createAll(db)
        return 'initiated'
    except: return 'error occured'

@Cities.delete('/delete-all-cities')
def createJsonCities(db: Session = Depends(get_db)):
    try:
        return deleteAllCities(db)
    except: return 'error occured'

@Cities.delete('/delete/{city}')
def deleteCity( city: str ):
    try: 
        deleteCity(city)
        return f'{city} deleted'
    except: return 'error occured'


     
