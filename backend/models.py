from sqlalchemy import Column, Integer, String

from backend.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    genre = Column(String)
    file_path = Column(String)
    download_count = Column(Integer, default=0) # Yuklashlar soni
