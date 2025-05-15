from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

env = os.environ
usuario = env.get("user")
contraseña = env.get("pswrd")
host = env.get("host")
puerto = env.get("puerto")
db = env.get("db")

DATABASE_URL = f"postgresql://{usuario}:{contraseña}@{host}:{puerto}/{db}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from app.models.schema import User, Post

Base.metadata.create_all(bind=engine)