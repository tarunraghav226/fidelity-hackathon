from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserCreateResponse(BaseModel):
    access_token: str
    refresh_token: str
