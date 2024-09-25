from pydantic import BaseModel

from app.schemas.product import ProductDB


class OrderItemBase(BaseModel):
    item_quantity: int


class OrderItemCreate(OrderItemBase):
    product_id: int
    

class OrderItemDB(OrderItemBase):
    id: int
    product: ProductDB

    class Config:
        from_attributes = True