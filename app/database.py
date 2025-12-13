from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

#loading env variables form .env
load_dotenv()

#Db url from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Render uses postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

#creating db engine
engine = create_engine(DATABASE_URL)

#creating session
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

#base class for model
Base = declarative_base()

#func to get db session for fastapi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()