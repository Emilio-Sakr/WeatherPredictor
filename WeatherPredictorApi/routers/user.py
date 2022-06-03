from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from WeatherPredictorApi import schemas, database, utils, models, Oauth2

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordRequestForm

user = APIRouter()

@user.post('/sign-up', response_model=schemas.Userout)
async def CreateUser(user: schemas.User, db: Session = Depends(database.get_db)):

    checkUser(user, db)

    hashed = utils.hash(user.password)
    newUser = models.User(username= user.username, email=user.email, password= hashed)
    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    return newUser

@user.post('/sign-in')
def getUser(user_credentials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    if not utils.dehash(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

    token = Oauth2.create_jwt_token(data={"email":user.email})

    return {"access_token": token, "token_type": "bearer"}



def checkUser(user: schemas.User, db: Session):
    dbuser = db.query(models.User).filter(models.User.email == user.email)

    if dbuser:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Email already signed')

    return False