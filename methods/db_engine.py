import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(override=True)

POSTGRES_DB_URI = f"""postgresql://{os.getenv('DB_DEV_USERNAME')}:{os.getenv('DB_DEV_PASSWORD')}@{os.getenv('DB_DEV_HOST')}:{os.getenv('DB_DEV_PORT')}/{os.getenv('DB_DEV_NAME')}"""

engine = create_engine(POSTGRES_DB_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


## https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency
## Dependency:
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session():
    return SessionLocal()


def get_engine():
    return engine


def get_database_url():
    return POSTGRES_DB_URI
