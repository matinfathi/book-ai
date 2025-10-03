from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    author: str
    year: int | None


class BookRead(BookCreate):
    id: int
    owner_id: int


class BookReadWithUser(BookRead):
    owner: "UserRead"  # type: ignore # noqa: F821

    class Config:
        from_attributes = True


from app.api.users.schemas import UserRead
BookReadWithUser.model_rebuild()
