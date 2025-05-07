from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:A5Oa21JRQr8v7zTh@db.gpnpykpetfthniswqgsk.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from app.models.schema import User, Post

Base.metadata.create_all(bind=engine)