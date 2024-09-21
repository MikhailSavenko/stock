from typing import List
from sqlalchemy import String, Text, Numeric, Integer
from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Product(Base):
    """Модель товара"""
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    cost: Mapped[float] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer)

    order_item: Mapped[List['OrderItem']] = relationship(back_populates='product')