from pydantic import BaseModel

# 1. Umumiy maydonlar (Hamma joyda ishlatiladi)
class BookBase(BaseModel):
    title: str
    author: str
    genre: str
    file_path: str

# 2. Kitob yaratish uchun (Faqat ma'lumot yuborishda)
class BookCreate(BookBase):
    pass  # BookBase'dagi hamma narsa bu yerda ham bor

# 3. Bazadan o'qish uchun (ID va yuklashlar soni bilan birga)
class Book(BookBase):
    id: int
    download_count: int

    class Config:
        # Bu qator SQLAlchemy modellari bilan Pydantic o'rtasida 
        # "tushunmovchilik" bo'lmasligi uchun kerak
        from_attributes = True
