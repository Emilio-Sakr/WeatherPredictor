from fastapi import FastAPI
import json



def createApp():
    app = FastAPI()

    cities = open('./WeatherPredictorApi/data.json')
    citiesData = json.load(cities)

    @app.get('/cities')
    def getCities():
        return citiesData

    return app