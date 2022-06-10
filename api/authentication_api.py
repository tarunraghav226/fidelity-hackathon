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
    access_token = authentication_helper.get_access_token(user)
    refresh_token = authentication_helper.get_refresh_token(user)
    return UserCreateResponse(access_token=access_token, refresh_token=refresh_token)
