from fastapi import FastAPI
from WeatherPredictorApi.routers import cities, internal, user



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
        user.user,
        prefix='/user'
    )

    app.include_router(
        internal.internal,
        prefix='/admin',
        tags=['admin']
    )

    return app