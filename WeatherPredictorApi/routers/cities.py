from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, status
import json

import requests
from sqlalchemy.orm import Session
from WeatherPredictorApi import Oauth2, database, models

Cities = APIRouter()

def notFound(word):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{word} not found')

@Cities.get('/items')
async def getCities(db: Session = Depends(database.get_db), skip: None | int = 0, limit: None | int = 100):
    cities = db.query(models.City).offset(skip).limit(limit).all()
    if cities is None:
        raise notFound('items')
    return cities

@Cities.get('/city')
async def getCity(name : str, db: Session = Depends(database.get_db)):
    city = db.query(models.City).filter(models.City.name == name).first()
    if city is None:
        raise notFound('name')
    return city

@Cities.get('/weather/')
async def getWeather(name: str, db: Session = Depends(database.get_db)) -> Dict:
    city = db.query(models.City).filter(models.City.name == name).first()
    if city:
        try: 
            response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={city.latitude}&longitude={city.longitude}&current_weather=true').json()
            return {'temperature':response['current_weather']['temperature'],'unit':'celsius'}
        except: HTTPException(status_code=404, detail='weather for this city is not available')
    else: raise notFound('name')

@Cities.get('/weather/{day}')
async def getWeather(day: int, name: str, db: Session = Depends(database.get_db)) -> Dict[str,int]:
    if day < -2 or day > 6:
        raise HTTPException(status_code=404, detail='specified day should be between -2 and 6')
    else:
        city = db.query(models.City).filter(models.City.name == name).first()
        if city:
            try:
                day+=2
                response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={city.latitude}&longitude={city.longitude}&daily=temperature_2m_max,temperature_2m_min&timezone=EET&past_days=2').json()
                daily = response['daily']
                return {
                'max_temperature':int(daily['temperature_2m_max'][day]), 'min_temperature': int(daily['temperature_2m_min'][day]),
                'average_temperature':(int(daily['temperature_2m_max'][day])+int(daily['temperature_2m_min'][day]))/2,
                }
            except: notFound('weather for this name is ')
        else: raise notFound('name')