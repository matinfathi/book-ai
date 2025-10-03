from datetime import datetime
from zoneinfo import ZoneInfo

from sqlmodel import SQLModel, Field, Relationship


class Restaurant(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    address: str | None = None
    phone: str | None = None

    owner_id: int = Field(foreign_key="user.pk_id")
    food_items: list["FoodItem"] | None = Relationship(back_populates="restaurant")


class FoodItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    image: str | None = None

    restaurant_fk: int = Field(foreign_key="restaurant.id")
    restaurant: "Restaurant" = Relationship(back_populates="food_items")


class Order(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_fk: int = Field(foreign_key="user.id")

    created_at: datetime = Field(default_factory=lambda: datetime.now(ZoneInfo("Asia/Tehran")))
    items: list["OrderItem"] = Relationship(back_populates="order")


class OrderItem(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    order_fk: int = Field(foreign_key="order.id")
    fooditem_fk: int = Field(foreign_key="fooditem.id")
    order: "Order" = Relationship(back_populates="items")

    quantity: int
