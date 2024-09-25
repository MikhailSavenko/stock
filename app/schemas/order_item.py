from pydantic import BaseModel

from app.schemas.product import ProductDB


class OrderItemDB(BaseModel):
    id: int
    product: ProductDB
    item_quantity: int

    class Config:
        from_attributes = True