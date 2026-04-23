import os
from pathlib import Path
from urllib.parse import urlparse

import httpx
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from backend import crud, models, schemas
from backend.database import SessionLocal, engine

app = FastAPI(title="Free Books Platform")


@app.on_event("startup")
def _create_tables():
    # DB mavjud bo'lmasa ham server ishga tushib ketsin (Docker/DB tayyor bo'lgach qayta urinish mumkin).
    try:
        models.Base.metadata.create_all(bind=engine)
    except Exception:
        pass

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_project_root = Path(__file__).resolve().parents[1]
_frontend_dir = _project_root / "frontend"
if _frontend_dir.is_dir():
    app.mount("/frontend", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", include_in_schema=False)
def root():
    if _frontend_dir.is_dir():
        return RedirectResponse(url="/frontend/")
    return RedirectResponse(url="/docs")




@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=list[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_books(db, skip=skip, limit=limit)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")
    return db_book


@app.get("/download/{book_id}")
def download_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Kitob topilmadi")

    file_path = (db_book.file_path or "").strip()

    # Remote file (URL) bo'lsa: server orqali stream qilib "download" qildirib yuboramiz.
    parsed = urlparse(file_path)
    if parsed.scheme in {"http", "https"}:
        def _iter_remote():
            with httpx.Client(follow_redirects=True, timeout=60.0) as client:
                with client.stream("GET", file_path) as r:
                    r.raise_for_status()
                    for chunk in r.iter_bytes():
                        if chunk:
                            yield chunk

        crud.increment_download_count(db, book_id=book_id)
        return StreamingResponse(
            _iter_remote(),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{db_book.title}.pdf"'},
        )

    # Local file bo'lsa: bir nechta ehtimoliy joydan topamiz.
    candidates: list[Path] = []
    p = Path(file_path)
    if p.is_absolute():
        candidates.append(p)
    else:
        rel = Path(file_path.lstrip("/\\").lstrip("./"))
        candidates.append(_project_root / rel)
        candidates.append(_project_root / "uploads" / rel)
        candidates.append(_project_root / "uploads" / rel.name)

    resolved = next((c for c in candidates if c.exists()), None)
    if resolved is None:
        raise HTTPException(status_code=404, detail="Fayl serverda topilmadi")

    crud.increment_download_count(db, book_id=book_id)
    return FileResponse(
        path=str(resolved),
        filename=f"{db_book.title}.pdf",
        media_type="application/pdf",
    )
