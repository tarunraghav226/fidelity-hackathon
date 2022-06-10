from pydantic import BaseModel

class CheckUserInCommunityPayload(BaseModel):
    status: int
    is_in_community: bool
