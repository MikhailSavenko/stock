from app.core.db import Base
from sqlalchemy import ForeignKey, Integer

from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderItem(Base):
    """Элемент заказа"""
    order_id: Mapped[int] = mapped_column(ForeignKey('order.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('product.id'), nullable=False)
    item_quantity: Mapped[int] = mapped_column(Integer, default=1)

    order: Mapped['Order'] = relationship(back_populates='order_item')
    product: Mapped['Product'] = relationship(back_populates='product')
