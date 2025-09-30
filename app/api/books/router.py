from typing import Annotated, Any

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session

from .models import Book
from .schemas import BookCreate, BookRead
from app.db.session import get_session
from app.core.security import get_current_user


book_router = APIRouter()


@book_router.get("/")
async def list_books(
        current_user: Annotated[Any, Depends(get_current_user)],
        session: Annotated[Session, Depends(get_session)]) -> list[BookRead]:
    if current_user.is_superuser:
        books = session.exec(select(Book)).all()
    else:
        books = session.exec(select(Book).where(Book.owner_id == current_user.pk_id)).all()
    return books


@book_router.post("/")
async def add_book(current_user: Annotated[Any, Depends(get_current_user)],
                   book: BookCreate | list[BookCreate],
                   session: Annotated[Session, Depends(get_session)]) -> dict[str, str | BookRead | list[BookRead]]:
    book_list = book if isinstance(book, list) else [book]
    message = ""
    db_books = []
    for b in book_list:
        data = b.model_dump()
        data["owner_id"] = current_user.pk_id
        db_books.append(Book(**data))

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


@book_router.get("/{book_id}")
async def get_book(current_user: Annotated[Any, Depends(get_current_user)],
                   book_id: int, session: Annotated[Session, Depends(get_session)]) -> BookRead:
    db_book = session.exec(select(Book).where(Book.id == book_id, Book.owner_id == current_user.pk_id))
    if db_book:
        return db_book
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete("/{book_id}")
async def delete_book(current_user: Annotated[Any, Depends(get_current_user)],
                      book_id: int, session: Annotated[Session, Depends(get_session)]) -> dict[str, str]:
    db_book = session.exec(select(Book).where(Book.id == book_id)).first()
    if db_book.owner_id != current_user.pk_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permission")
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(db_book)
    session.commit()
    return {"message": "Book deleted successfully"}


@book_router.put("/{book_id}")
async def update_book(book_id: int, book: BookCreate, session: Annotated[Session, Depends(get_session)],
                      current_user: Annotated[Any, Depends(get_current_user)]) -> dict[str, str | BookRead]:
    db_book = session.exec(select(Book).where(Book.id == book_id)).first()
    if db_book.owner_id != current_user.pk_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permission")
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_book.title = book.title
    db_book.author = book.author
    db_book.year = book.year

    session.add(db_book)
    session.commit()

    session.refresh(db_book)

    return {"message": "Book updated successfully", "book": db_book}
