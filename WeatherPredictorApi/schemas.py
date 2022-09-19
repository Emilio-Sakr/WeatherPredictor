from datetime import datetime
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class Userout(BaseModel):
    username: str

    class Config:
        orm_mode = True

class token:
    email: EmailStr
    expire: datetime

class CityCreate(BaseModel):
    name: str
    long: float
    lat: float