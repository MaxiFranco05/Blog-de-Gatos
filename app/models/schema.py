from sqlalchemy import Column, Integer, String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from app.core.database import Base
from datetime import datetime
from typing import List, Optional
import random

### BASE SCHEMAS

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    profile_pic = Column(String(255), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now())

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    img = Column(String(255), nullable=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=func.now())
    last_update = Column(DateTime, default=func.now())

    author = relationship("User", back_populates="posts")

### END BASE SCHEMAS

### BASEMODEL SCHEMAS

class NewPost(BaseModel):
    title: str
    content: str
    author_id: int

class NewUser(BaseModel):
    username: str
    email: str
    password: str

class AuthUser(BaseModel):
    username: str
    password: str

class PostSchema(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    created_at: datetime
    last_update: datetime

    model_config = {
        "from_attributes": True}

class UserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime
    last_update: datetime

    model_config = {
        "from_attributes": True}
### END BASEMODEL SCHEMAS