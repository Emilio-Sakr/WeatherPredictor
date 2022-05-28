from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .authhandler import decodeJWT

from WeatherPredictorApi.SQLApp.database import get_db
from sqlalchemy.orm import Session

from WeatherPredictorApi.SQLApp.crud import getAllUsers

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request, db: Session = Depends(get_db)):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials, db):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str, db: Session) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            for user in getAllUsers(db):
                if user.email == payload["email"]:
                    isTokenValid = True
                    return isTokenValid
        return isTokenValid

#https://learnings.desipenguin.com/post/rolechecker-with-fastapi/