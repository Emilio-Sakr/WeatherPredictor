from jose import JWTError, jwt
import time
from . import schemas, models, settings, database
from fastapi import Depends, status ,HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

settings = settings.Settings()

secret = settings.secret
algorithm = settings.algorithm
access_token_expire_seconds = settings.expire

def create_jwt_token(data: dict):
    encode = data.copy()
    expire = time.localtime(time.time() + access_token_expire_seconds)

    encode.update({"expire": expire})

    encoded = jwt.encode(encode ,secret ,algorithm)

    return encoded

def verify_jwt_token(token: str, exception):
    try:
        decoded = jwt.decode(token, secret, algorithms=[algorithm])
        email : str = decoded.get('user.email')
        if email is None:
            raise exception
        token_data = schemas.token(email=email)
    except JWTError:
        raise exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Couldn\'t validate credentials',  headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_jwt_token(token, exception)

    user = db.query(models.User).filter(models.User.email==token_data)

    return user