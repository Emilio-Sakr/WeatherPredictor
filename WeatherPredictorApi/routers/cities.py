from fastapi import APIRouter, HTTPException
import json
import requests

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
async def getCities():
    cities = list()
    for key, value in findCitiesJson().items():
        cities.append(key)
    return cities

@Cities.get('/location/{city}')
async def getLocation(city: str):
    allCitiesJson = findCitiesJson()
    if city not in allCitiesJson:
        raise HTTPException(status_code=404, detail="City not available")
    else:
        return allCitiesJson[city]

@Cities.get('/weather/{city}')
async def getWeather(city: str):
    allCitiesJson = findCitiesJson()
    if city not in allCitiesJson:
        raise HTTPException(status_code=404, detail="City not available")
    else:
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={allCitiesJson[city][0]}&longitude={allCitiesJson[city][1]}&current_weather=true').json()
        return {'temperature':response['current_weather']['temperature'],'unit':'celsius'}

@Cities.get('/weather/{day}/{city}')
async def getWeather(day: int, city: str):
    if day < -2 or day > 6:
        raise HTTPException(status_code=404, detail='specified past day should be between -2 and 6')
    allCitiesJson = findCitiesJson()
    if city not in allCitiesJson:
        raise HTTPException(status_code=404, detail="City not available")
    else:
        day+=2
        response = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={allCitiesJson[city][0]}&longitude={allCitiesJson[city][1]}&daily=temperature_2m_max,temperature_2m_min&timezone=EET&past_days=2').json()
        daily = response['daily']
        return {
        'max_temperature':daily['temperature_2m_max'][day], 'min_temperature': daily['temperature_2m_min'][day],
        'average_temperature':(int(daily['temperature_2m_max'][day])-int(daily['temperature_2m_min'][day]))/2,
        }

    