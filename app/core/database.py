from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres.gpnpykpetfthniswqgsk:ZBa9moa6i2lBj3Xq@aws-0-sa-east-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from app.models.schema import User, Post

Base.metadata.create_all(bind=engine)