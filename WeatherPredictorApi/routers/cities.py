from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
import json
import requests
from WeatherPredictorApi.auth.authbearer import JWTBearer
from WeatherPredictorApi.SQLApp.crud import getCity, getAllCities
from sqlalchemy.orm import Session
from WeatherPredictorApi.SQLApp.database import get_db

Cities = APIRouter()

data_path = './WeatherPredictorApi/data'

def findCitiesJson():
    try:
        cities = open(f'{data_path}/cities.json')
        citiesData = json.load(cities)
    except:
        raise HTTPException(status_code=404, detail="Item not found")
    return citiesData

@Cities.get('/items')
async def getCities(db: Session = Depends(get_db)):
    return getAllCities(db)

@Cities.get('/location/{city}')
async def getLocation(city: str, db: Session = Depends(get_db)):
    return getCity(db, city)

@Cities.get('/weather/{city}')
async def getWeather(city: str, db: Session = Depends(get_db)) -> Dict:
    try:
        cityobj = getCity(db, city)
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={cityobj.latitude}&longitude={cityobj.longitude}&current_weather=true').json()
        return {'temperature':response['current_weather']['temperature'],'unit':'celsius'}
    except: HTTPException(status_code=404, details='city not found in database')

@Cities.get('/weather/{day}/{city}', dependencies = [Depends(JWTBearer())])
async def getWeather(day: int, city: str, db: Session = Depends(get_db)) -> Dict[str,int]:
    if day < -2 or day > 6:
        raise HTTPException(status_code=404, detail='specified day should be between -2 and 6')
    else:
        cityobj = getCity(db, city)
        day+=2
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={cityobj.latitude}&longitude={cityobj.longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=EET&past_days=2').json()
        daily = response['daily']
        return {
        'max_temperature':int(daily['temperature_2m_max'][day]), 'min_temperature': int(daily['temperature_2m_min'][day]),
        'average_temperature':(int(daily['temperature_2m_max'][day])-int(daily['temperature_2m_min'][day]))/2,
        }