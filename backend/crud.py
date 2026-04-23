from sqlalchemy.orm import Session

from backend import models, schemas

# 1. ID bo'yicha bitta kitobni topish
def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

# 2. Barcha kitoblar ro'yxatini olish
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

# 3. Yangi kitob qo'shish
def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(
        title=book.title,
        author=book.author,
        genre=book.genre,
        file_path=book.file_path
    )
    db.add(db_book)          # Bazaga qo'shish navbatiga qo'yish
    db.commit()              # O'zgarishlarni tasdiqlash (saqlash)
    db.refresh(db_book)      # Bazadagi yangi ID va ma'lumotlarni qayta yuklash
    return db_book

# 4. Yuklab olish sonini oshirish
def increment_download_count(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db_book.download_count += 1
        db.commit()
        db.refresh(db_book)
    return db_book
