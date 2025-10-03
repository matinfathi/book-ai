from datetime import datetime

from pydantic import BaseModel


#############################################################
class RestaurantCreate(BaseModel):
    name: str
    owner_id: int
    address: str | None
    phone: str | None


class RestaurantRead(RestaurantCreate):
    id: int

    food_items: list["FoodItemRead"] | None

#############################################################
class FoodItemCreate(BaseModel):
    name: str
    description: str | None
    image: str | None

    restaurant_fk: int


class FoodItemRead(BaseModel):
    id: int
    name: str
    description: str | None
    image: str | None

    restaurant: "RestaurantRead"

#############################################################
class OrderCreate(BaseModel):
    user_fk: int

    items: list["OrderItemRead"]


class OrderRead(OrderCreate):
    id: int
    created_at: datetime

#############################################################
class OrderItemCreate(BaseModel):
    order_fk: int
    fooditem_fk: int
    quantity: int


class OrderItemRead(OrderItemCreate):
    id: int
    order: "OrderRead"

