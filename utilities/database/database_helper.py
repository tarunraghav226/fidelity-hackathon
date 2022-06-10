from fastapi.encoders import jsonable_encoder
from typing import Any, Generator, Optional
from sqlalchemy.orm import Session

from db.session import SessionLocal
from models import User
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


def create_user(db: Session, obj_in: UserCreate) -> User:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = User(**obj_in_data)  
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
