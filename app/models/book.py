from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int | None = None
