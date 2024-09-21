from app.core.db import Base
from sqlalchemy import ForeignKey, Integer

from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.product import Product
from app.models.order import Order


class OrderItem(Base):
    """Элемент заказа"""
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=False)
    count_products: Mapped[int] = mapped_column(Integer, default=1)

    order: Mapped['Order'] = relationship(back_populates='order_item')
    product = Mapped['Product'] = relationship(back_populates='product')
