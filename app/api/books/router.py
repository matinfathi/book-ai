from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session

from .models import Book
from .schemas import BookCreate, BookRead
from app.db.session import get_session


router = APIRouter()


@router.get("/")
async def list_books(session: Annotated[Session, Depends(get_session)]) -> dict[str, list[BookRead]]:
    book_list = session.exec(select(Book)).all()
    return {"books": book_list}


@router.post("/")
async def add_book(
    book: BookCreate | list[BookCreate], session: Annotated[Session, Depends(get_session)]
) -> dict[str, str | BookRead | list[BookRead]]:
    book_list = book if isinstance(book, list) else [book]
    message = ""
    db_books = []
    for b in book_list:
        duplicate_check = select(Book).where(Book.title == b.title, Book.author == b.author, Book.year == b.year)
        if session.exec(duplicate_check).first():
            message += f"{b.title}, "
            continue
        db_books.append(Book(**b.model_dump()))

    session.add_all(db_books)
    session.commit()
    for b in db_books:
        session.refresh(b)
    return {
        "message": "Books [" + message.strip(", ") + "] were duplicate, added rest successfully."
        if message
        else "All Books added successfully",
        "book": db_books if isinstance(book, list) else db_books[0],
    }


@router.get("/{book_id}")
async def get_book(book_id: int, session: Annotated[Session, Depends(get_session)]) -> BookRead:
    book = session.get(Book, book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.delete("/{book_id}")
async def delete_book(book_id: int, session: Annotated[Session, Depends(get_session)]) -> dict[str, str]:
    db_book = session.get(Book, book_id)
    if db_book:
        session.delete(db_book)
        session.commit()
        return {"message": "Book deleted successfully"}

    raise HTTPException(status_code=404, detail="Book not found")


@router.put("/{book_id}")
async def update_book(
    book_id: int, book: BookCreate, session: Annotated[Session, Depends(get_session)]
) -> dict[str, str | BookRead]:
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
