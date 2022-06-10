from typing import Dict, List
from sqlalchemy.orm.session import Session

from models import CommunityMember
from schemas import community_schema
from utilities.database import database_helper

def get_community_members_map(members: List[CommunityMember]) -> Dict[str, bool]:
    map: Dict[str, bool] = dict()
    for member in members:
        map[member.email] = True
    return map


def get_community_members(db: Session) -> List[CommunityMember]:
    members = database_helper.get_community_members(db)
    members = [community_schema.CommunityMember(email=member.email) for member in members ]
    return members
