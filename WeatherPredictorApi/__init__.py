from re import A
from fastapi import FastAPI
from WeatherPredictorApi.routers import cities
from WeatherPredictorApi.auth import userauth
from WeatherPredictorApi.routers import ws
from WeatherPredictorApi.SQLApp.database import Base, engine

Base.metadata.create_all(bind=engine)

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

    app.include_router(
        ws.ws,
        prefix='/ws'
    )

    return app