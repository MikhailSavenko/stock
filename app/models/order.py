from sqlalchemy import DateTime, Enum
from app.core.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.services.enums import Status


class Order(Base):
    """Модель Заказа"""
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now(timezone.utc))
    status: Mapped[Status] = mapped_column(Enum(Status), default=Status.IN_PROCESS)