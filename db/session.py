import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dotenv_path = '.env'
load_dotenv(dotenv_path)

engine = create_engine(
    "postgresql://jcnhbrnyselsea:f6b18d6e67c448fbccf89de1e550e439d1d1850cffc98bb7112f7bf28dbc58d6@ec2-52-30-67-143.eu-west-1.compute.amazonaws.com:5432/ddi9g9es2dg3r0",
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)