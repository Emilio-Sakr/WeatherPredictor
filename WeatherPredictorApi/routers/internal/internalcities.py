from fastapi import APIRouter, Body, Depends
from WeatherPredictorApi.SQLApp.crud import createCity, deleteAllCities, deleteCityById
from WeatherPredictorApi.SQLApp.schemas import cityCreate
from WeatherPredictorApi.SQLApp.database import get_db
from sqlalchemy.orm import Session
from WeatherPredictorApi.data.supplyinfo import createAll

from WeatherPredictorApi.auth.authbearer import JWTBearer

Cities = APIRouter(dependencies = [Depends(JWTBearer())])

@Cities.post('/create-city')
def create(db: Session = Depends(get_db), city: cityCreate = Body(...)):
    return createCity(db, city)

@Cities.post('/initiate-json-cities')
def createJsonCities(db: Session = Depends(get_db)):
    createAll(db)
    return 'initiated'

@Cities.delete('/delete-all-cities')
def createJsonCities(db: Session = Depends(get_db)):
    return deleteAllCities(db)

@Cities.delete('/delete/{id}')
def deleteCity(id: int, db: Session = Depends(get_db)):
    return deleteCityById(db, id)



#, dependencies = [Depends(JWTBearer())]

     
