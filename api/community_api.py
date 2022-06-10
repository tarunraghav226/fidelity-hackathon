import imp
from fastapi import APIRouter, Depends, FastAPI, status, HTTPException
from fastapi.responses import RedirectResponse

from schemas.authentication_schema import UserSignUpPayload
from schemas.user_schema import UserCreate, UserCreateResponse
from schemas.community_schema import CheckUserInCommunityPayload

from models import User

from utilities.authentication.authentication_helper import jwt_auth_required
from uuid import uuid4

from utilities.database import database_helper

router = APIRouter(prefix="/community", tags=["communities"])

@router.post('/check-user-in-community', summary="Checks user has joined any community or not", response_model=CheckUserInCommunityPayload)
async def check_user_in_community(user: User = Depends(jwt_auth_required), 
                        db = Depends(database_helper.get_db)) -> CheckUserInCommunityPayload:
    is_in_community = database_helper.is_user_in_community(db, user)
    return CheckUserInCommunityPayload(status=status.HTTP_200_OK, is_in_community=is_in_community)
