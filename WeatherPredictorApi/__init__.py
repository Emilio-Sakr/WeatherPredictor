from fastapi import FastAPI
from WeatherPredictorApi.routers import cities



def createApp():
    app = FastAPI()

    app.include_router(
        cities.Cities,
        prefix='/cities'
    )

    return app