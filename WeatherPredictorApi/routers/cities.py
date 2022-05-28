from typing import Dict
from fastapi import APIRouter, HTTPException, Depends
import requests

from WeatherPredictorApi.SQLApp.crud import getCity, getAllCities
from sqlalchemy.orm import Session
from WeatherPredictorApi.SQLApp.database import get_db
from WeatherPredictorApi.auth.authbearer import JWTBearer

Cities = APIRouter(dependencies=[Depends(JWTBearer())])

@Cities.get('/items')
async def getCities(db: Session = Depends(get_db)):
    return getAllCities(db)

@Cities.get('/location/{city}')
async def getLocation(city: str, db: Session = Depends(get_db)):
    city = getCity(db, city)
    if city: return city
    else: raise HTTPException(status_code=404, detail='city does not exist')

@Cities.get('/weather/{city}')
async def getWeather(city: str, db: Session = Depends(get_db)) -> Dict:
    city = getCity(db, city)
    if city:
        try: 
            response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={city.latitude}&longitude={city.longitude}&current_weather=true').json()
            return {'temperature':response['current_weather']['temperature'],'unit':'celsius'}
        except: HTTPException(status_code=404, detail='weather for this city is not available')
    else: raise HTTPException(status_code=404, detail='city does not exist')

@Cities.get('/weather/{day}/{city}')
async def getWeather(day: int, city: str, db: Session = Depends(get_db)) -> Dict[str,int]:
    if day < -2 or day > 6:
        raise HTTPException(status_code=404, detail='specified day should be between -2 and 6')
    else:
        city = getCity(db, city)
        if city:
            try:
                day+=2
                response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={city.latitude}&longitude={city.longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=EET&past_days=2').json()
                daily = response['daily']
                return {
                'max_temperature':int(daily['temperature_2m_max'][day]), 'min_temperature': int(daily['temperature_2m_min'][day]),
                'average_temperature':(int(daily['temperature_2m_max'][day])+int(daily['temperature_2m_min'][day]))/2,
                }
            except: HTTPException(status_code=404, detail='weather for this city is not available')
        else: raise HTTPException(status_code=404, detail='city does not exist')