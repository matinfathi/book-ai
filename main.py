from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()


class Book(BaseModel):
    title: str
    author: str
    year: int

book_list = {
    1: Book(title="1984", author="George Orwell", year=1949),
    2: Book(title="To Kill a Mockingbird", author="Harper Lee", year=1960),
    3: Book(title="The Great Gatsby", author="F. Scott Fitzgerald", year=1925),
}


@app.get("/list-books", tags=["Books"])
def list_books():
    return {"books": book_list}


@app.get("/get-book/{book_id}", tags=["Books"])
def get_book(book_id: int) -> Book:
    book = book_list.get(book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/add-book/{book_id}", tags=["Books"])
def add_book(book_id: int, book: Book):
    if book_id in book_list:
        raise HTTPException(status_code=400, detail="Book ID already exists")
    book_list[book_id] = book
    return {"message": "Book added successfully", "book": book}


@app.delete("/delete-book/{book_id}", tags=["Books"])
def delete_book(book_id: int):
    if book_id in book_list:
        del book_list[book_id]
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/update-book/{book_id}", tags=["Books"])
def update_book(book_id: int, book: Book):
    if book_id in book_list:
        book_list[book_id] = book
        return {"message": "Book updated successfully", "book": book}
    raise HTTPException(status_code=404, detail="Book not found")
