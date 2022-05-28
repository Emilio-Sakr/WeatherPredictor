from fastapi import HTTPException, Depends

from .authhandler import decodeJWT
from WeatherPredictorApi.auth.authbearer import JWTBearer

from WeatherPredictorApi.SQLApp.crud import getAllUsers

admins = ['admin']

class RoleChecker:
    def __init__(self, allowedRoles : list) -> None:
        self.allowedRoles=allowedRoles

    def __call__(self, token = Depends(JWTBearer()), users = Depends(getAllUsers)):
        email = decodeJWT(token)["email"]
        for user in users:
            if user.email == email:
                if not user.role in self.allowedRoles:
                    raise HTTPException(status_code=403, detail='Operation not permitted')