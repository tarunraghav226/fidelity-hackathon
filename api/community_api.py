from fastapi import APIRouter, Depends, status

from schemas.community_schema import CheckUserInCommunityPayload, ListCommunityMembersPayload, CommunityMember

from models import User

from utilities.authentication.authentication_helper import jwt_auth_required
from utilities.common.common_helper import get_community_members_map

from utilities.database import database_helper

router = APIRouter(prefix="/community", tags=["communities"])

@router.get('/check-user-in-community', summary="Checks user has joined any community or not", response_model=CheckUserInCommunityPayload)
async def check_user_in_community(user: User = Depends(jwt_auth_required), 
                        db = Depends(database_helper.get_db)) -> CheckUserInCommunityPayload:
    is_in_community = database_helper.is_user_in_community(db, user)
    return CheckUserInCommunityPayload(status=status.HTTP_200_OK, is_in_community=is_in_community)


@router.post('add-user-in-community', summary="Adds user to community", response_model=ListCommunityMembersPayload)
async def add_user_in_community(user: User = Depends(jwt_auth_required), 
                        db = Depends(database_helper.get_db)) -> ListCommunityMembersPayload:
    members = database_helper.get_community_members(db)
    members = [CommunityMember(email=member.email) for member in members ]
    community_members_map = get_community_members_map(members=members)
    
    if user.email in community_members_map:
        print(members)
        return ListCommunityMembersPayload(status=200, members=members)
    
    database_helper.add_user_in_community(db, user.email)
    members.append(CommunityMember(email=user.email))
    return ListCommunityMembersPayload(status=200, members=members)

