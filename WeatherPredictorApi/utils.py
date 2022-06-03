from xmlrpc.client import Boolean
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password):
    return pwd_context.hash(password)

def dehash(password, hashed_password) -> Boolean:
    return pwd_context.verify(password, hashed_password)