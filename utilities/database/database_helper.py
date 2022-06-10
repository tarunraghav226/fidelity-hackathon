from fastapi.encoders import jsonable_encoder
from typing import Any, Generator, List, Optional
from sqlalchemy.orm import Session

from db.session import SessionLocal
from models import User, CommunityMember
from schemas.user_schema import UserCreate


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_user_by_email(db: Session, email: Any) -> Optional[User]:
    return (
            db.query(User)
                .filter(User.email == email)
                .first()
            )


def get_user_by_id(db: Session, id: int) -> Optional[User]:
    return (
            db.query(User)
                .filter(User.id == id)
                .first()
            )


def create_user(db: Session, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = User(**obj_in_data)  
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


def is_user_in_community(db: Session, user: User) -> bool:
    return len(db.query(CommunityMember).filter(CommunityMember.email == user.email).all()) == 1


def get_community_members(
        db: Session
    ) -> List[CommunityMember]:
        return (
            db.query(CommunityMember)
            .all()
        )

def add_user_in_community(db: Session, email: str):
    db_obj = CommunityMember(email=email)  
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj