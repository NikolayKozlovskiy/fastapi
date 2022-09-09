import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .config import settings
# 'postgres://<username>:<password>@<ip-addres>/dbname'
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
# once we create an instance of the SessionLocal class, this instance will be the actual database session.
SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Later we will inherit from this class to create each of the database models or classes (the ORM models):
Base = declarative_base()
# Dependency
# session is responsible for talking with out DB, everytime we make a query, then we close DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()