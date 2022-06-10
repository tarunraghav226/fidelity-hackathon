from fastapi import APIRouter, Depends, FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse

from schemas.authentication_schema import UserSignUpPayload
from schemas.user_schema import UserCreate, UserCreateResponse
from utilities.authentication.authentication_helper import authentication_helper
from uuid import uuid4

from utilities.database import database_helper

router = APIRouter(prefix="/users", tags=["users"])

@router.post('/signup', summary="Create new user", response_model=UserCreateResponse)
async def create_user(data: UserSignUpPayload, db = Depends(database_helper.get_db)) -> UserCreate:
    user = database_helper.get_user_by_email(db, data.email)
    if user is not None:
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user_create_obj = UserCreate(email=data.email, password=authentication_helper.get_hashed_password(data.password))
    user = database_helper.create_user(db, user_create_obj)
    return authentication_helper.get_tokens(user)


@router.post("/login", summary="Login user", response_model=UserCreateResponse)
async def login_user(data: UserSignUpPayload, db = Depends(database_helper.get_db)) -> UserCreate:
    user = database_helper.get_user_by_email(db, data.email)
    if user is None or not authentication_helper.verify_password(data.password, user.password):
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email/password does not match."
        )
    return authentication_helper.get_tokens(user)

