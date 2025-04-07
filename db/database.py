# phonebook/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///phonebook.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

def init_db() -> None:
    """
    Initialize the database by creating all tables.
    """
    # Import orm_models so that they are registered with Base.
    from db import orm_models
    Base.metadata.create_all(bind=engine)
