from pydantic import BaseModel, EmailStr, Field

#User
class UserBase(BaseModel):
    email: EmailStr = Field(...)

class UserCreate(UserBase):
    username: str = Field(...)
    password: str = Field(...)

class User(UserBase):
    id: int

    class config:
        orm_mode = True


#City
class cityCreate(BaseModel):
    name: str = Field(...)
    latitude: float = Field(...)
    longitude: float = Field(...)
