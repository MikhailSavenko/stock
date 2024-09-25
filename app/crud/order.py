from .base import CRUDBase
from app.models import Order
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDOrder(CRUDBase):
    async def create(self, session: AsyncSession):
        """Создает новый заказ"""
        db_obj = self.model()
        print(db_obj)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    
order_crud = CRUDOrder(Order)