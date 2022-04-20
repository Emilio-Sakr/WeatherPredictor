from fastapi import APIRouter, HTTPException
import json

Cities = APIRouter()

@Cities.get('/items')
async def getCities():
    try:
        cities = open('./WeatherPredictorApi/data/cities.json')
        citiesData = json.load(cities)
    except:
        raise HTTPException(status_code=404, detail="Item not found")

    return citiesData
