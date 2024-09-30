from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.schemas.order_item import OrderItemCreate, OrderItemDB
from app.services.enums import Status


class OrderBase(BaseModel):
    pass


class OrderCreate(OrderBase):
    order_item: List[OrderItemCreate]


class OrderDB(OrderBase):
    id: int
    order_item: List[OrderItemDB]
    status: Status = Status.in_process
    create_at: datetime

    class Config:
        from_attributes = True


class OrderUpdate(OrderBase):
    status: Status = Status.in_process


class OrderUpdateDB(OrderBase):
    id: int
    status: Status
