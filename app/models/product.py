from typing import List

from sqlalchemy import Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Product(Base):
    """Модель товара"""

    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    cost: Mapped[float] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(Integer)

    order_item: Mapped[List['OrderItem']] = relationship(
        back_populates='product'
    )
