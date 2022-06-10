from pydantic import BaseModel
from pydantic import EmailStr

class UserSignUpPayload(BaseModel):
    email: EmailStr
    password: str
