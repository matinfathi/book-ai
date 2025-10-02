from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    pk_id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    first_name: str
    last_name: str | None = None
    image_path: str | None = None
    hashed_password: str
    is_superuser: bool = Field(default=False)

    books: list["Book"] = Relationship(back_populates="owner")  # type: ignore # noqa: F821
