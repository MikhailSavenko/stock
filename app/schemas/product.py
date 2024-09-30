from pydantic import BaseModel, Field


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
    name: str = Field(..., min_length=1, max_length=50)
    description: str = Field(..., min_length=1)
    cost: float
    quantity: int = Field(..., ge=0)


class ProductDB(ProductBase):
    id: int
    pass

    class Config:
        from_attributes = True
