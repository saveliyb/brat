from sqlalchemy import create_engine
from sqlalchemy.orm.decl_api import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ
from server.config import start

start()

DATABASE_URL = environ.get("DB_URL")

# TODO change echo value to True
engine = create_engine(DATABASE_URL, echo="debug")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
