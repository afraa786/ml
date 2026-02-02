from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from sclalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./test.db"

# we will now create a session
# session local = ek facotry hai for creating the database sessions
# a session is like a workscape for database operations
# autocommit = false, we dont want autosave as of now we want the control of the commands
# autoflush = false, to the database we dont want to flush the changes automatically

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # only for SQLite
)

# Engine = connection to the database
# check_same_thread=False is needed for SQLite with FastAPI
# (allows multiple threads to use the same connection)

SessionLoccal = sessionmaker (
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db # to give the session to the endpoint
    finally:
        db.close() 

