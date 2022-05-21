from typing import List
from fastapi import APIRouter, HTTPException, Body
from WeatherPredictorApi.auth.models import UserLoginSchema
from .authhandler import signJWT, decodeJWT
from .models import UserSchema
from WeatherPredictorApi.SQLApp.crud import getUserByEmail

Auth = APIRouter()

data_path = './WeatherPredictorApi/data'

users = list()

def checkIfUserIsPresent(data: UserSchema):
    for user in users:
        if user.email == data.email:
            return True
    return False

@Auth.post('/create-token')
async def createUser(user: UserSchema = Body(...)):
    if checkIfUserIsPresent(user):
        raise HTTPException(status_code=404, detail='user already present')
    users.append(user) #momenatrely
    return signJWT(user.email)

def validate(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@Auth.post('/validate')
async def getToken(user : UserLoginSchema = Body(...)):
    if validate(user):
        return signJWT(user.email)
    raise HTTPException(status_code=404, detail='Wrong login credentials')