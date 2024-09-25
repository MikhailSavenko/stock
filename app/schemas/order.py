from typing import List
from pydantic import BaseModel, Field
from app.schemas.order_item import OrderItemDB
from app.services.enums import Status
from datetime import datetime


class OrderBase(BaseModel):
    status: Status = Status.in_process


class OrderCreate(OrderBase):
    order_item: List[int]


class OrderDB(OrderBase):
    id: int
    order_item: List[OrderItemDB]
    create_at: datetime

    class Config:
        from_attributes = True


class OrderUpdate(OrderBase):
    pass