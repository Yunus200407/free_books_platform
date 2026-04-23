# Python bazaviy obrazi
FROM python:3.11-slim

# Ishchi papkani belgilash
WORKDIR /app

# PostgreSQL drayveri uchun kerakli tizim kutubxonalarini o'rnatish
RUN apt-get update && apt-get install -y libpq-dev gcc

# Kutubxonalar ro'yxatini nusxalash va o'rnatish
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Backend kodlarini nusxalash
COPY backend ./backend

# FastAPI'ni ishga tushirish
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
