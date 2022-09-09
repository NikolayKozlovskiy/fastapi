# how it was created  alembic revision --autogenerate -m "add automaticly votes table"
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base
# The big problem is that is we use sqlalchemy it will go through checking if the table has alreasy existed, if not creates a new one, 
# but it won't modify the new one (or may it has been changed&&&)
class Post(Base): 
  __tablename__ = "posts"
  id=Column(Integer, primary_key=True, nullable=False)
  title=Column(String, nullable=False)
  content=Column(String, nullable=False)
  published=Column(Boolean, nullable=False, server_default="TRUE")
  created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  # it will automaticly fetch the user based on owner_id
  owner = relationship('User')

class User(Base): 
  __tablename__ = 'users'
  id=Column(Integer, primary_key=True, nullable=False)
  email=Column(String, nullable=False, unique=True)
  password=Column(String, nullable=False)
  created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Vote(Base): 
  __tablename__ = 'votes'
  user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True)
  post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), primary_key=True)
