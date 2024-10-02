from datetime import datetime
from typing import List

from sqlalchemy import DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.db import Base
from app.services.enums import Status


class Order(Base):
    """Модель Заказа"""

    create_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    status: Mapped[Status] = mapped_column(
        Enum(Status), default=Status.in_process
    )

    order_item: Mapped[List['OrderItem']] = relationship(
        back_populates='order', lazy='selectin'
    )
