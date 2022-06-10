from typing import Dict, List

from models import CommunityMember

def get_community_members_map(members: List[CommunityMember]) -> Dict[str, bool]:
    map: Dict[str, bool] = dict()
    for member in members:
        map[member.email] = True
    return map

