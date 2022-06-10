import os
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from dotenv import load_dotenv

from .authentication_interface import AuthenticationInterface
from models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

dotenv_path = '.env'
load_dotenv(dotenv_path)

ACCESS_TOKEN_EXPIRE_MINUTES = 60  
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 
ALGORITHM = os.environ["ALGORITHM"]
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']   
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']


class AuthenticationHelper(AuthenticationInterface):
    def get_access_token(self, user: User) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(user.id)}
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
        return encoded_jwt


    def get_refresh_token(self, user: User) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(user.id)}
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
        return encoded_jwt


    def verify_jwt_token(self, token: str) -> User:
        return super().verify_jwt_token()


    def get_hashed_password(self, password: str) -> str:
        return password_context.hash(password)


    def verify_password(self, password: str, hashed_pass: str) -> bool:
        return password_context.verify(password, hashed_pass)


authentication_helper = AuthenticationHelper()
