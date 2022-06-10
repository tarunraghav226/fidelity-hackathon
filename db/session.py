import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

dotenv_path = '.env'
load_dotenv(dotenv_path)

engine = create_engine(
    os.environ["DATABASE_URL"],
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)