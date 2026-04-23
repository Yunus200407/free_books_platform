import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQL ulanish formati: 
# postgresql://user:password@postgresserver/db_name
# Namuna:
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:1234@localhost:5432/free_books_db",
)

# engine yaratish (SQLite dagi 'check_same_thread' bu yerda kerak emas)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
