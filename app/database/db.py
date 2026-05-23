import os

from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = (

    f"postgresql://"

    f"{os.getenv('POSTGRES_USER')}:"

    f"{os.getenv('POSTGRES_PASSWORD')}@"

    f"{os.getenv('POSTGRES_HOST')}:"

    f"{os.getenv('POSTGRES_PORT')}/"

    f"{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(

    autocommit=False,

    autoflush=False,

    bind=engine
)

Base = declarative_base()

# ----------------------------------------
# AUTO CREATE TABLES
# ----------------------------------------

from app.database.models import *

Base.metadata.create_all(
    bind=engine
)