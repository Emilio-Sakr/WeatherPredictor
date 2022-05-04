from re import A
from fastapi import FastAPI
from WeatherPredictorApi.routers import cities
from WeatherPredictorApi.auth import userauth


def createApp():
    app = FastAPI()

    app.include_router(
        cities.Cities,
        prefix='/cities'
    )
    
    app.include_router(
        userauth.Auth,
        prefix='/user'
    )

    return app