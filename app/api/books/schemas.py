from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    year: int | None


class BookRead(BookCreate):
    id: int
    owner_id: int
    owner: "UserRead"  # type: ignore # noqa: F821

    class Config:
        from_attributes = True


from app.api.users.schemas import UserRead
BookRead.model_rebuild()
