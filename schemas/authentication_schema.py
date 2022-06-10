from datetime import datetime
from pydantic import BaseModel
from pydantic import EmailStr

class UserSignUpPayload(BaseModel):
    email: EmailStr
    password: str


class TokenPayload(BaseModel):
    sub: str
    exp: int 
