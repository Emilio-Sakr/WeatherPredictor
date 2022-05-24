from typing import List
from fastapi import APIRouter, HTTPException, Body, Depends
from WeatherPredictorApi.SQLApp.schemas import UserCreate, UserBase
from .authhandler import signJWT, decodeJWT

from WeatherPredictorApi.SQLApp.database import get_db
from sqlalchemy.orm import Session

from WeatherPredictorApi.SQLApp.crud import dehashpassword, createUser, getAllUsers # deleteUser

Auth = APIRouter()

data_path = './WeatherPredictorApi/data'


def checkIfUserIsPresent(data: UserCreate, db : Session = Depends(get_db)):
    for user in getAllUsers(db):
        if user.email == data.email:
            return True
    return False

@Auth.post('/create-token')
async def sign_up(db: Session = Depends(get_db), user: UserCreate = Body(...)):
    if checkIfUserIsPresent(user, db):
        raise HTTPException(status_code=409, detail='user already present')
    createUser(db, user)
    return signJWT(user.email)


def validate(data: UserBase, db: Session = Depends(get_db)):
    for user in getAllUsers(db):
        if user.email == data.email and dehashpassword(data, user):
            return True
    return False

@Auth.post('/validate')
async def sign_in(db: Session = Depends(get_db), user : UserBase = Body(...)):
    if validate(user, db):
        return signJWT(user.email)
    raise HTTPException(status_code=401, detail='Wrong login credentials')

# @Auth.delete('delete/{email}')
# async def delete(email: str, db: Session = Depends(get_db)):
#     return deleteUser(db, email)