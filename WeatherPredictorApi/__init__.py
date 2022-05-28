from fastapi import FastAPI, Depends
from WeatherPredictorApi.auth.authbearer import JWTBearer
from WeatherPredictorApi.routers import cities
from WeatherPredictorApi.routers.internal import internalcities
from WeatherPredictorApi.auth import userauth
from WeatherPredictorApi.routers import ws
from WeatherPredictorApi.SQLApp.database import Base, engine

Base.metadata.create_all(bind=engine)

def createApp():
    app = FastAPI()

    @app.get('/')
    def welcome():
        return {'Api':'WeatherPredictorApi', 'docs':'path:<domain>/docs'}

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

    app.include_router(
        internalcities.Cities,
        prefix='/internal',
        tags=['admin']
    )

    return app