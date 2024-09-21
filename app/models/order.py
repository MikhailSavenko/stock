from typing import List
from sqlalchemy import DateTime, Enum
from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from app.models.order_item import OrderItem
from app.services.enums import Status


class Order(Base):
    """Модель Заказа"""
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    status: Mapped[Status] = mapped_column(Enum(), default=Status.IN_PROCESS)

    order_item: Mapped[List['OrderItem']] = relationship(back_populates='order')