import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

try:
    # Lokal ishga tushirishda `.env` avtomatik yuklanishi uchun (ixtiyoriy).
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()
except Exception:
    pass

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./free_books.db",
)

_engine_kwargs = {}
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(SQLALCHEMY_DATABASE_URL, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
