from sqlmodel import SQLModel, Field, Relationship


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    author: str
    year: int | None = None

    owner_id: int = Field(foreign_key="user.pk_id")
    owner: "User" = Relationship(back_populates="books")  # type: ignore # noqa: F821
