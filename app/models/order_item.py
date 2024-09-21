from app.core.db import Base
from sqlalchemy import String, Text, Numeric, Integer

from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderItem(Base):
    """Элемент заказа"""
    order_id: Mapped
    product_id:
    count_products: 
