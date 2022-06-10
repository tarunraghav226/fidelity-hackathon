from typing import List
from pydantic import BaseModel, EmailStr

class CheckUserInCommunityPayload(BaseModel):
    status: int
    is_in_community: bool


class CommunityMember(BaseModel):
    email: EmailStr


class ListCommunityMembersPayload(BaseModel):
    status: int
    members: List[CommunityMember]
