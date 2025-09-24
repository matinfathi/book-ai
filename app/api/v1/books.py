from fastapi import APIRouter, HTTPException



router = APIRouter()


@router.get("/", tags=["Books"])
async def list_books():
    return {"books": book_list}


@router.get("/{book_id}", tags=["Books"])
async def get_book(book_id: int) -> Book:
    book = book_list.get(book_id)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")


@router.post("/{book_id}", tags=["Books"])
async def add_book(book_id: int, book: Book):
    if book_id in book_list:
        raise HTTPException(status_code=400, detail="Book ID already exists")
    book_list[book_id] = book
    return {"message": "Book added successfully", "book": book}


@router.delete("/{book_id}", tags=["Books"])
async def delete_book(book_id: int):
    if book_id in book_list:
        del book_list[book_id]
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")


@router.put("/{book_id}", tags=["Books"])
async def update_book(book_id: int, book: Book):
    if book_id in book_list:
        book_list[book_id] = book
        return {"message": "Book updated successfully", "book": book}
    raise HTTPException(status_code=404, detail="Book not found")
