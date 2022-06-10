from enum import unique
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = "users"    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True)
    password = Column(String)


class CommunityMember(Base):
    __tablename__ = "communitymembers"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, ForeignKey("users.email", ondelete="CASCADE"), unique=True, index=True)
