from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session

from app.models import Book
from app.schemas import BookCreate, BookRead
from app.db.session import get_session


router = APIRouter()


@router.get("/")
async def list_books(session: Session = Depends(get_session)) -> dict[str, list[BookRead]]:
    book_list = session.exec(select(Book)).all()
    return {"books": book_list}


@router.get("/{book_id}")
async def get_book(book_id: int, session: Session = Depends(get_session)) -> BookRead:
    book = session.get(Book, book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.post("/")
async def add_book(book: BookCreate, session: Session = Depends(get_session)) -> dict[str, str | BookRead]:
    db_book = Book.model_validate(book)
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return {"message": "Book added successfully", "book": db_book}


@router.delete("/{book_id}")
async def delete_book(book_id: int, session: Session = Depends(get_session)) -> dict[str, str]:
    db_book = session.get(Book, book_id)
    if db_book:
        session.delete(db_book)
        session.commit()
        return {"message": "Book deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Book not found")


@router.put("/{book_id}")
async def update_book(book_id: int, book: BookCreate, session: Session = Depends(get_session)) -> dict[str, str | BookRead]:
    db_book = session.get(Book, book_id)
    if db_book:
        db_book.title = book.title
        db_book.author = book.author
        db_book.year = book.year

        session.add(db_book)
        session.commit()

        session.refresh(db_book)

        return {"message": "Book updated successfully", "book": db_book}
    
    raise HTTPException(status_code=404, detail="Book not found")
