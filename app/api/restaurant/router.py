from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session

from app.db.session import get_session
from app.core.security import get_current_user
from .schemas import RestaurantRead, RestaurantCreate
from .models import Restaurant


restaurant_router = APIRouter()


@restaurant_router.get("/", tags=["Restaurant"])
def list_restaurant(session: Annotated[Session, Depends(get_session)],
                    current_user: Annotated[Any, Depends(get_current_user)]) -> list[RestaurantRead]:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permission")

    return session.exec(select(Restaurant)).all()


@restaurant_router.get("/{restaurant_id}", tags=["Restaurant"])
def get_restaurant_by_id(
        restaurant_id: int, session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[Any, Depends(get_current_user)]) -> RestaurantRead:
    db_restaurant = session.exec(select(Restaurant).where(Restaurant.id == restaurant_id)).first()
    if not db_restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if not current_user.is_superuser and current_user.pk_id != db_restaurant.id:
        raise HTTPException(status_code=403, detail="Not enough permission")

    return db_restaurant


@restaurant_router.post("/", tags=["Restaurant"])
def add_restaurant(
        restaurant: RestaurantCreate, session: Annotated[Session, Depends(get_session)],
        current_user: Annotated[Any, Depends(get_current_user)]) -> list[RestaurantRead]:
    pass
