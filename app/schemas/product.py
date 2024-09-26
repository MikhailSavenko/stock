from pydantic import BaseModel, Field
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(min_length=1)
    cost: float
    quantity: int

    class Config:
        extra = 'forbid'


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, min_length=1)
    cost: Optional[float] = None
    quantity: Optional[int] = None


class ProductDB(ProductBase):
    id: int
    pass

    class Config:
        from_attributes = True