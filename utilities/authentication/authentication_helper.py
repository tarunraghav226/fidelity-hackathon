import os
from typing import Optional, Union
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from fastapi import Header
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv

from .authentication_interface import AuthenticationInterface
from models import User
from schemas.user_schema import UserCreateResponse
from schemas.authentication_schema import TokenPayload
from utilities.database import database_helper

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

    def get_tokens(self, user: User) -> UserCreateResponse:
        access_token = self.get_access_token(user)
        refresh_token = self.get_refresh_token(user)
        return UserCreateResponse(access_token=access_token, refresh_token=refresh_token)


authentication_helper = AuthenticationHelper()


def jwt_auth_required(
        x_auth_token: Optional[str] = Header(...),
        db: Session = Depends(database_helper.get_db)
    ) -> User:
        if not x_auth_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Authentication token required"
            )
        try:
            payload = jwt.decode(
                x_auth_token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
            )
            token_data = TokenPayload(**payload)

            if datetime.fromtimestamp(token_data.exp) < datetime.now():
                raise HTTPException(
                    status_code = status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            current_user = database_helper.get_user_by_id(db, int(token_data.sub))
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials or expired token.",
                )
            return current_user
        except(jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )