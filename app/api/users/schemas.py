from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str | None = None
    image_path: str | None = None


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    hashed_password: str


class UserUpdate(UserBase):
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    image_path: str | None = None


class UserInDB(UserRead):
    hashed_password: str
