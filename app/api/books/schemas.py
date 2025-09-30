from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    year: int | None


class BookRead(BookCreate):
    id: int
    owner_id: int
