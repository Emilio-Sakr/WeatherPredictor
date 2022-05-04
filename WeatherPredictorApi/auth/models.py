from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    full_name : str = Field(...)
    email : EmailStr = Field(...)
    password : str = Field(...)

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
