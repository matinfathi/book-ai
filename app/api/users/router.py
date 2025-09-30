from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from .schemas import UserCreate, UserRead, UserUpdate
from .models import User
from app.core.security import get_current_user, get_password_hash
from app.db.session import get_session


user_router = APIRouter()


@user_router.get("/list")
async def get_users(current_user: Annotated[UserRead, Depends(get_current_user)],
                    session: Annotated[Session, Depends(get_session)]) -> list[UserRead]:
    return session.exec(select(User)).all() if current_user.is_superuser else []


@user_router.post("/")
async def create_user(user_in: UserCreate, session: Annotated[Session, Depends(get_session)]) -> UserRead:
    data = user_in.model_dump()
    hashed_password = get_password_hash(data.pop("password"))
    data["hashed_password"] = hashed_password

    db_user = User(**data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@user_router.get("/{user_id}")
async def get_user(
        user_id: int,
        current_user: Annotated[UserRead, Depends(get_current_user)],
        session: Annotated[Session, Depends(get_session)]) -> UserRead:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions.")

    db_user = session.get(User, user_id)

    if db_user:
        return db_user

    raise HTTPException(status_code=404, detail="User not found.")


@user_router.delete("/{user_id}")
async def delete_user(
        user_id: int,
        current_user: Annotated[UserRead, Depends(get_current_user)],
        session: Annotated[Session, Depends(get_session)],
) -> dict[str, str]:
    if current_user.pk_id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions.")

    db_user = session.get(User, user_id)

    if db_user:
        session.delete(db_user)
        session.commit()
        return {"message": "User deleted successfully."}

    raise HTTPException(status_code=404, detail="User not found.")


@user_router.patch("/{user_id}")
async def update_user(
    user_id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    session: Annotated[Session, Depends(get_session)],
    user_update: UserUpdate,
) -> dict[str, str | UserRead]:
    if current_user.pk_id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions.")

    db_user = session.get(User, user_id)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    update_data = user_update.model_dump(exclude_unset=True)
    print(update_data)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return {"message": "user updated successfully.", "user": db_user}


@user_router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_user)],
):
    return current_user
