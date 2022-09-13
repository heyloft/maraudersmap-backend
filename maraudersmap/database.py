from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from maraudersmap.config import Settings


@lru_cache()
def get_settings():
    return Settings()


SQLALCHEMY_DATABASE_URL = get_settings().DATABASE_CONNECTION_STRING.replace(
    # SQLAlchemy 1.4 removed deprecated 'postgres://',
    # but fly.io still uses it...
    "postgres://",
    "postgresql://",
    1,
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
