from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from maraudersmap.config import Settings


@lru_cache()
def get_settings():
    return Settings()


engine = create_engine(get_settings().DATABASE_CONNECTION_STRING)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
