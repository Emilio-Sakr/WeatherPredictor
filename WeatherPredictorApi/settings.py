from datetime import datetime
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_uri: str
    secret: str
    algorithm: str
    expire: int

    class Config:
        env_file = ".env"