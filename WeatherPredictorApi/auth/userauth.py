from typing import List
from fastapi import APIRouter, HTTPException, Body, Depends
from WeatherPredictorApi.SQLApp.schemas import UserCreate, UserBase
from .authhandler import signJWT, decodeJWT

from WeatherPredictorApi.SQLApp.database import get_db
from sqlalchemy.orm import Session

from WeatherPredictorApi.SQLApp.crud import getUserByEmail, createUser, getAllUsers

Auth = APIRouter()

data_path = './WeatherPredictorApi/data'


def checkIfUserIsPresent(data: UserCreate, db : Session = Depends(get_db)):
    for user in getAllUsers(db):
        if user.email == data.email:
            return True
    return False

@Auth.post('/create-token')
async def createUser(user: UserCreate = Body(...), db: Session = Depends(get_db)):
    if checkIfUserIsPresent(user, db):
        raise HTTPException(status_code=404, detail='user already present')
    createUser(db, user)
    return signJWT(user.email)

def validate(data: UserBase, db: Session = Depends(get_db)):
    for user in getAllUsers(db):
        if user.email == data.email and user.password == data.password:
            return True
    return False

@Auth.post('/validate')
async def getToken(user : UserBase = Body(...), db: Session = Depends(get_db)):
    if validate(user, db):
        return signJWT(user.email)
    raise HTTPException(status_code=404, detail='Wrong login credentials')